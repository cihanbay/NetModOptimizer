package com.netmod.optimizer.core

import android.content.Context
import kotlinx.serialization.json.Json
import java.io.File

/**
 * Port of the `persistence` module. The desktop app wrote profiles.json next
 * to the script; on Android we use the app's private filesDir.
 */
object Persistence {
    private val json = Json {
        ignoreUnknownKeys = true
        encodeDefaults = true
        prettyPrint = false
    }

    private fun file(ctx: Context) = File(ctx.filesDir, "profiles.json")

    fun save(ctx: Context, store: ProfileStore): Boolean = runCatching {
        val tmp = File(ctx.filesDir, "profiles.json.tmp")
        tmp.writeText(json.encodeToString(ProfileStore.serializer(), store))
        tmp.copyTo(file(ctx), overwrite = true)
        tmp.delete()
        true
    }.getOrElse { false }

    fun load(ctx: Context): ProfileStore {
        val f = file(ctx)
        if (!f.exists()) return defaultStore()
        return runCatching {
            json.decodeFromString(ProfileStore.serializer(), f.readText())
                .also { if (it.profiles.isEmpty()) it.profiles.add(ConfigProfile(name = "Default")) }
        }.getOrElse { defaultStore() }
    }

    private fun defaultStore() = ProfileStore(
        profiles = mutableListOf(ConfigProfile(name = "Default")),
        index = 0,
    )
}
