package com.veo.optimizer.ui.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.qr.QrEncoder
import com.veo.optimizer.ui.theme.Theme

/** QR dialog (port of desktop show_qr). Encodes [text] into a scannable QR. */
@Composable
fun QrDialog(text: String, title: String, onDismiss: () -> Unit) {
    val p = Theme.palette
    val bmp = remember(text) { runCatching { QrEncoder.bitmap(text, 640).asImageBitmap() }.getOrNull() }
    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = { TextButton(onClick = onDismiss) { Text("Close") } },
        title = { Text(title, fontWeight = FontWeight.Bold) },
        text = {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                if (bmp != null)
                    Image(bitmap = bmp, contentDescription = "QR", modifier = Modifier.size(240.dp))
                else
                    Text("Could not render QR (content too large).", color = p.fg3, fontSize = 12.sp)
                Text(if (text.length > 64) text.take(64) + "…" else text,
                    color = p.fg3, fontSize = 11.sp, modifier = Modifier.padding(top = 8.dp))
            }
        },
    )
}

/** Card container (port of _card/_colored_card). */
@Composable
fun SectionCard(modifier: Modifier = Modifier, accent: Color? = null, content: @Composable ColumnScope.() -> Unit) {
    val p = Theme.palette
    Column(
        modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(accent ?: p.bgCard)
            .border(1.dp, p.border, RoundedCornerShape(12.dp))
            .padding(12.dp),
        content = content,
    )
}

/** Section title row. */
@Composable
fun CardTitle(text: String, sub: String? = null) {
    val p = Theme.palette
    Column {
        Text(text, color = p.fg1, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
        if (sub != null) Text(sub, color = p.fg3, fontSize = 12.sp)
    }
}

/** Metric tile (port of _metric_box / _stat_box). */
@Composable
fun MetricBox(title: String, value: String, color: Color, modifier: Modifier = Modifier, icon: String = "") {
    val p = Theme.palette
    Column(
        modifier
            .clip(RoundedCornerShape(10.dp))
            .background(p.bgCard)
            .border(1.dp, p.border, RoundedCornerShape(10.dp))
            .padding(horizontal = 10.dp, vertical = 8.dp),
    ) {
        Text("$icon $title".trim(), color = p.fg3, fontSize = 10.sp)
        Text(value, color = color, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    }
}

/** Colored status dot (port of _status_dot). */
@Composable
fun StatusDot(color: Color, size: Int = 10) {
    Box(Modifier.size(size.dp).clip(CircleShape).background(color))
}

/** ping/speed chip. */
@Composable
fun Chip(text: String, color: Color) {
    val p = Theme.palette
    Box(
        Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(color.copy(alpha = 0.15f))
            .padding(horizontal = 8.dp, vertical = 3.dp),
    ) { Text(text, color = color, fontSize = 12.sp, fontWeight = FontWeight.Medium) }
}

@Composable
fun LabeledRow(label: String, value: String) {
    val p = Theme.palette
    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, color = p.fg3, fontSize = 13.sp)
        Text(value, color = p.fg1, fontSize = 13.sp, fontWeight = FontWeight.Medium)
    }
}
