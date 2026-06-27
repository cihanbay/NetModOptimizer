package com.veo.optimizer

import android.app.Application
import com.veo.optimizer.core.Crash

class VEOApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Crash.install(this)   // port of the `crash` module
    }
}
