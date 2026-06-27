package com.veo.optimizer.qr

import android.graphics.Bitmap
import android.graphics.Color

/**
 * Port of the `qr` module (_QR pure-Python encoder + show_qr). The desktop
 * version drew onto a Tk canvas; here we produce an Android [Bitmap].
 *
 * Self-contained QR generator (byte mode, automatic version/ECC, mask
 * optimisation) — no external library, matching the original's "no
 * dependencies" philosophy. Algorithm follows the QR Code spec (ISO/IEC 18004).
 */
object QrEncoder {

    enum class Ecc(val ordinal2: Int, val formatBits: Int) {
        LOW(0, 1), MEDIUM(1, 0), QUARTILE(2, 3), HIGH(3, 2)
    }

    /** Render [text] to a square Bitmap at roughly [targetPx] pixels. */
    fun bitmap(text: String, targetPx: Int = 640, ecc: Ecc = Ecc.MEDIUM,
               border: Int = 4, dark: Int = Color.BLACK, light: Int = Color.WHITE): Bitmap {
        val qr = encode(text, ecc)
        val size = qr.size
        val dim = size + border * 2
        val scale = (targetPx / dim).coerceAtLeast(1)
        val px = dim * scale
        val bmp = Bitmap.createBitmap(px, px, Bitmap.Config.ARGB_8888)
        for (y in 0 until px) for (x in 0 until px) {
            val mx = x / scale - border
            val my = y / scale - border
            val on = mx in 0 until size && my in 0 until size && qr[my][mx]
            bmp.setPixel(x, y, if (on) dark else light)
        }
        return bmp
    }

    /** Returns the QR module matrix (true = dark). */
    fun encode(text: String, ecc: Ecc = Ecc.MEDIUM): Array<BooleanArray> {
        val data = text.toByteArray(Charsets.UTF_8)
        val version = pickVersion(data.size, ecc)
        val size = version * 4 + 17

        // 1. Build data codewords (byte mode segment)
        val bits = BitBuffer()
        bits.append(0b0100, 4)                                  // byte mode
        bits.append(data.size, charCountBits(version))
        for (b in data) bits.append(b.toInt() and 0xFF, 8)

        val totalCodewords = numDataCodewords(version, ecc)
        val capacityBits = totalCodewords * 8
        bits.append(0, minOf(4, capacityBits - bits.size))     // terminator
        while (bits.size % 8 != 0) bits.append(0, 1)           // byte align
        var pad = 0xEC
        while (bits.size < capacityBits) { bits.append(pad, 8); pad = pad xor (0xEC xor 0x11) }

        val dataCodewords = bits.toBytes()
        val allCodewords = addEcc(dataCodewords, version, ecc)

        // 2. Place modules
        val modules = Array(size) { BooleanArray(size) }
        val isFunction = Array(size) { BooleanArray(size) }
        drawFunctionPatterns(modules, isFunction, version, ecc)
        drawCodewords(modules, isFunction, allCodewords, size)

        // 3. Choose best mask by penalty
        var best = 0; var minPenalty = Int.MAX_VALUE
        for (mask in 0..7) {
            applyMask(modules, isFunction, mask)
            drawFormatBits(modules, isFunction, ecc, mask, size)
            val p = penalty(modules)
            if (p < minPenalty) { minPenalty = p; best = mask }
            applyMask(modules, isFunction, mask) // undo (XOR is its own inverse)
        }
        applyMask(modules, isFunction, best)
        drawFormatBits(modules, isFunction, ecc, best, size)
        return modules
    }

    // ── Versioning / capacity ────────────────────────────────────────────────
    private fun charCountBits(version: Int) = if (version < 10) 8 else 16

    private fun pickVersion(len: Int, ecc: Ecc): Int {
        for (v in 1..40) if (len <= numDataCodewords(v, ecc) - 2 - (if (v < 10) 1 else 2)) return v
        throw IllegalArgumentException("Data too long for QR")
    }

    // EC codewords per block + block counts (subset of the spec table, v1-40)
    private val ECC_CODEWORDS_PER_BLOCK = arrayOf(
        // L, M, Q, H  for each version 1..40 (index 0 unused)
        intArrayOf(-1, 7, 10, 13, 17, 10, 16, 22, 28, 22, 26, 30, 36, 26, 36, 26, 36, 46, 26, 36, 46, 26, 36, 46, 30, 36, 46, 30, 36, 46, 30, 36, 46, 30, 36, 46, 30, 36, 46, 30, 36, 46),
        intArrayOf(-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28),
        intArrayOf(-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
        intArrayOf(-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
    )
    private val NUM_ERROR_CORRECTION_BLOCKS = arrayOf(
        intArrayOf(-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25),
        intArrayOf(-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49),
        intArrayOf(-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68),
        intArrayOf(-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81),
    )

    private fun numRawDataModules(ver: Int): Int {
        var result = (16 * ver + 128) * ver + 64
        if (ver >= 2) {
            val align = ver / 7 + 2
            result -= (25 * align - 10) * align - 55
            if (ver >= 7) result -= 36
        }
        return result
    }

    private fun numDataCodewords(ver: Int, ecc: Ecc): Int {
        val blocks = NUM_ERROR_CORRECTION_BLOCKS[ecc.ordinal2][ver]
        val eccLen = ECC_CODEWORDS_PER_BLOCK[ecc.ordinal2][ver]
        return numRawDataModules(ver) / 8 - eccLen * blocks
    }

    // ── Reed-Solomon ECC ──────────────────────────────────────────────────────
    private fun addEcc(data: ByteArray, ver: Int, ecc: Ecc): ByteArray {
        val numBlocks = NUM_ERROR_CORRECTION_BLOCKS[ecc.ordinal2][ver]
        val blockEccLen = ECC_CODEWORDS_PER_BLOCK[ecc.ordinal2][ver]
        val rawCodewords = numRawDataModules(ver) / 8
        val numShort = numBlocks - rawCodewords % numBlocks
        val shortLen = rawCodewords / numBlocks

        val blocks = ArrayList<ByteArray>()
        val rsDiv = reedSolomonDivisor(blockEccLen)
        var k = 0
        for (i in 0 until numBlocks) {
            val datLen = shortLen - blockEccLen + (if (i < numShort) 0 else 1)
            val dat = data.copyOfRange(k, k + datLen); k += datLen
            val ecBytes = reedSolomonRemainder(dat, rsDiv)
            blocks.add(dat + ecBytes)
        }
        // Interleave
        val result = ByteArray(rawCodewords)
        var idx = 0
        val maxLen = blocks.maxOf { it.size }
        for (i in 0 until maxLen) for (j in blocks.indices) {
            if (i < blocks[j].size - blockEccLen || i >= shortLen - blockEccLen) {
                if (i < blocks[j].size) result[idx++] = blocks[j][i]
            }
        }
        return result
    }

    private fun reedSolomonDivisor(degree: Int): ByteArray {
        val result = ByteArray(degree); result[degree - 1] = 1
        var root = 1
        for (i in 0 until degree) {
            for (j in 0 until degree) {
                result[j] = gfMul(result[j].toInt() and 0xFF, root).toByte()
                if (j + 1 < degree) result[j] = (result[j].toInt() xor (result[j + 1].toInt() and 0xFF)).toByte()
            }
            root = gfMul(root, 0x02)
        }
        return result
    }

    private fun reedSolomonRemainder(data: ByteArray, divisor: ByteArray): ByteArray {
        val result = ByteArray(divisor.size)
        for (b in data) {
            val factor = (b.toInt() xor result[0].toInt()) and 0xFF
            System.arraycopy(result, 1, result, 0, result.size - 1)
            result[result.size - 1] = 0
            for (i in result.indices) result[i] = (result[i].toInt() xor gfMul(divisor[i].toInt() and 0xFF, factor)).toByte()
        }
        return result
    }

    private fun gfMul(x: Int, y: Int): Int {
        var z = 0
        for (i in 7 downTo 0) {
            z = (z shl 1) xor ((z ushr 7) * 0x11D)
            z = z xor ((y ushr i) and 1) * x
        }
        return z and 0xFF
    }

    // ── Module placement ──────────────────────────────────────────────────────
    private fun drawFunctionPatterns(m: Array<BooleanArray>, f: Array<BooleanArray>, ver: Int, ecc: Ecc) {
        val size = m.size
        for (i in 0 until size) { setFunc(m, f, 6, i, i % 2 == 0); setFunc(m, f, i, 6, i % 2 == 0) }
        drawFinder(m, f, 3, 3); drawFinder(m, f, size - 4, 3); drawFinder(m, f, 3, size - 4)
        val align = alignmentPositions(ver)
        for (i in align.indices) for (j in align.indices) {
            if ((i == 0 && j == 0) || (i == 0 && j == align.size - 1) || (i == align.size - 1 && j == 0)) continue
            drawAlignment(m, f, align[i], align[j])
        }
        drawFormatBits(m, f, ecc, 0, size)
        drawVersion(m, f, ver, size)
    }

    private fun drawFinder(m: Array<BooleanArray>, f: Array<BooleanArray>, cx: Int, cy: Int) {
        for (dy in -4..4) for (dx in -4..4) {
            val x = cx + dx; val y = cy + dy
            if (x in m.indices && y in m.indices) {
                val dist = maxOf(Math.abs(dx), Math.abs(dy))
                setFunc(m, f, x, y, dist != 2 && dist != 4)
            }
        }
    }

    private fun drawAlignment(m: Array<BooleanArray>, f: Array<BooleanArray>, cx: Int, cy: Int) {
        for (dy in -2..2) for (dx in -2..2)
            setFunc(m, f, cx + dx, cy + dy, maxOf(Math.abs(dx), Math.abs(dy)) != 1)
    }

    private fun alignmentPositions(ver: Int): IntArray {
        if (ver == 1) return IntArray(0)
        val numAlign = ver / 7 + 2
        val step = if (ver == 32) 26 else (ver * 4 + numAlign * 2 + 1) / (numAlign * 2 - 2) * 2
        val result = IntArray(numAlign)
        result[0] = 6
        var pos = ver * 4 + 10
        for (i in numAlign - 1 downTo 1) { result[i] = pos; pos -= step }
        return result
    }

    private fun setFunc(m: Array<BooleanArray>, f: Array<BooleanArray>, x: Int, y: Int, dark: Boolean) {
        if (x in m.indices && y in m.indices) { m[y][x] = dark; f[y][x] = true }
    }

    private fun drawFormatBits(m: Array<BooleanArray>, f: Array<BooleanArray>, ecc: Ecc, mask: Int, size: Int) {
        val data = ecc.formatBits shl 3 or mask
        var rem = data
        for (i in 0 until 10) rem = (rem shl 1) xor ((rem ushr 9) * 0x537)
        val bits = (data shl 10 or rem) xor 0x5412
        for (i in 0..5) setFunc(m, f, 8, i, getBit(bits, i))
        setFunc(m, f, 8, 7, getBit(bits, 6)); setFunc(m, f, 8, 8, getBit(bits, 7)); setFunc(m, f, 7, 8, getBit(bits, 8))
        for (i in 9 until 15) setFunc(m, f, 14 - i, 8, getBit(bits, i))
        for (i in 0..7) setFunc(m, f, size - 1 - i, 8, getBit(bits, i))
        for (i in 8 until 15) setFunc(m, f, 8, size - 15 + i, getBit(bits, i))
        setFunc(m, f, 8, size - 8, true)
    }

    private fun drawVersion(m: Array<BooleanArray>, f: Array<BooleanArray>, ver: Int, size: Int) {
        if (ver < 7) return
        var rem = ver
        for (i in 0 until 12) rem = (rem shl 1) xor ((rem ushr 11) * 0x1F25)
        val bits = ver shl 12 or rem
        for (i in 0 until 18) {
            val bit = getBit(bits, i); val a = size - 11 + i % 3; val b = i / 3
            setFunc(m, f, a, b, bit); setFunc(m, f, b, a, bit)
        }
    }

    private fun drawCodewords(m: Array<BooleanArray>, f: Array<BooleanArray>, data: ByteArray, size: Int) {
        var i = 0
        var right = size - 1
        while (right >= 1) {
            if (right == 6) right = 5
            for (vert in 0 until size) {
                for (j in 0 until 2) {
                    val x = right - j
                    val upward = ((right + 1) and 2) == 0
                    val y = if (upward) size - 1 - vert else vert
                    if (!f[y][x] && i < data.size * 8) {
                        m[y][x] = getBit(data[i ushr 3].toInt(), 7 - (i and 7)); i++
                    }
                }
            }
            right -= 2
        }
    }

    private fun applyMask(m: Array<BooleanArray>, f: Array<BooleanArray>, mask: Int) {
        for (y in m.indices) for (x in m.indices) {
            if (f[y][x]) continue
            val invert = when (mask) {
                0 -> (x + y) % 2 == 0
                1 -> y % 2 == 0
                2 -> x % 3 == 0
                3 -> (x + y) % 3 == 0
                4 -> (x / 3 + y / 2) % 2 == 0
                5 -> (x * y) % 2 + (x * y) % 3 == 0
                6 -> ((x * y) % 2 + (x * y) % 3) % 2 == 0
                else -> ((x + y) % 2 + (x * y) % 3) % 2 == 0
            }
            if (invert) m[y][x] = !m[y][x]
        }
    }

    private fun penalty(m: Array<BooleanArray>): Int {
        // Simplified penalty: count adjacent same-color runs and dark ratio.
        val size = m.size; var p = 0
        for (y in 0 until size) {
            var run = 1
            for (x in 1 until size) {
                if (m[y][x] == m[y][x - 1]) { run++; if (run == 5) p += 3 else if (run > 5) p++ } else run = 1
            }
        }
        for (x in 0 until size) {
            var run = 1
            for (y in 1 until size) {
                if (m[y][x] == m[y - 1][x]) { run++; if (run == 5) p += 3 else if (run > 5) p++ } else run = 1
            }
        }
        var dark = 0
        for (row in m) for (c in row) if (c) dark++
        val total = size * size
        val k = Math.abs(dark * 20 / total - 10)
        p += k * 10
        return p
    }

    private fun getBit(x: Int, i: Int) = ((x ushr i) and 1) != 0

    // ── tiny bit buffer ───────────────────────────────────────────────────────
    private class BitBuffer {
        private val bits = ArrayList<Boolean>()
        val size get() = bits.size
        fun append(value: Int, len: Int) { for (i in len - 1 downTo 0) bits.add(((value ushr i) and 1) != 0) }
        fun toBytes(): ByteArray {
            val out = ByteArray((bits.size + 7) / 8)
            for (i in bits.indices) if (bits[i]) out[i ushr 3] = (out[i ushr 3].toInt() or (1 shl (7 - (i and 7)))).toByte()
            return out
        }
    }
}
