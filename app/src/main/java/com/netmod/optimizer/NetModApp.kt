package com.netmod.optimizer

import android.app.Application
import com.netmod.optimizer.core.Crash

class NetModApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Crash.install(this)   // port of the `crash` module
    }
}
