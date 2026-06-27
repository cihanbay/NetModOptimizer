package com.veo.optimizer.core

import android.content.Context
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Port of the `crash` module: dump uncaught exceptions to a file. */
object Crash {
    fun install(ctx: Context) {
        val prev = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { t, e ->
            runCatching { write(ctx, e.stackTraceToString()) }
            prev?.uncaughtException(t, e)
        }
    }

    fun write(ctx: Context, tb: String): String {
        val dir = File(ctx.filesDir, "crashes").apply { mkdirs() }
        val ts = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        val f = File(dir, "crash_$ts.txt")
        f.writeText(tb)
        return f.absolutePath
    }
}
