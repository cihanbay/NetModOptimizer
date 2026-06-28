#!/usr/bin/env python3
"""
VEO v4
Single-file compiled version (complete.pyw)
"""

import asyncio
import atexit
import base64 as _b64
import ipaddress
import json
import os
import platform
import queue
import re
import secrets as _sec
import shutil
import socket
import ssl
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import tkinter as tk
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from tkinter import ttk, filedialog, messagebox
from typing import Any, Dict, List, Optional, Tuple
import uuid as _uuid_mod




# ============================================================
#  Module: constants
# ============================================================


import sys

# ── Dimensions ──────────────────────────────────────────────────
APP_W, APP_H = 1120, 700
SIDEBAR_W    = 64

# ── Theme state (mutable) ───────────────────────────────────────
_theme = "light"  # "dark" or "light"

def set_theme(name: str):
    global _theme
    _theme = name
    # Update all color globals
    _apply_theme()

def get_theme() -> str:
    return _theme

# ══════════════════════════════════════════════════════════════════
#  Light Theme (Default)
# ══════════════════════════════════════════════════════════════════

_LIGHT = {
    "BG":           "#f4f5f7",
    "BG_CARD":      "#ffffff",
    "BG_SIDEBAR":   "#1e1e2e",
    "BG_HOVER":     "#eaeaea",
    "BG_INPUT":     "#ffffff",
    "BG_HEADER":    "#ffffff",
    "BORDER":       "#dde0e8",
    "BORDER_HOVER": "#ccd0d8",
    "BORDER_FOCUS": "#FA7567",
    "ACCENT":       "#FA7567",
    "ACCD":         "#e06050",
    "ACCENT_GLOW":  "#FA756725",
    "GREEN":        "#1db954",
    "GREEN_DIM":    "#16a34a",
    "ORANGE":       "#f0960a",
    "ORANGE_DIM":   "#e08600",
    "RED_C":        "#e03030",
    "RED_DIM":      "#c02020",
    "BLUE":         "#2979ff",
    "TEAL":         "#00b4ab",
    "PURPLE":       "#7c4dff",
    "CYAN":         "#00bcd4",
    "FG1":          "#1a1a2e",
    "FG2":          "#444466",
    "FG3":          "#9999bb",
    "FG4":          "#bbbbcc",
    "STATUS_BG":    "#e8e8e8",
    "SIDEBAR":      "#1e1e2e",
    "CARD":         "#ffffff",
    "DARK":         "#0d1117",
    "CARD_BG_1":    "#e3f2fd",
    "CARD_BG_2":    "#e8f5e9",
    "CARD_BG_3":    "#fff3e0",
    "CARD_BG_4":    "#fce4ec",
    "CARD_BG_5":    "#f3e5f5",
    "NAV_ACTIVE_BG":"#1a3a5c",   # active sidebar tab background (light)
}

# ══════════════════════════════════════════════════════════════════
#  Dark Theme — Samsung One UI Eye Comfort Style
# ══════════════════════════════════════════════════════════════════

_DARK = {
    # Warm dark theme - soft charcoal/brown surfaces with an amber-orange
    # accent. Avoids the cold near-black look; sections read as warm gray.
    "BG":           "#1c1916",   # warm charcoal app background
    "BG_CARD":      "#272220",   # warm gray-brown card / section
    "BG_SIDEBAR":   "#171311",   # deep warm sidebar
    "BG_HOVER":     "#352d27",   # warm hover
    "BG_INPUT":     "#231f1c",   # input field
    "BG_HEADER":    "#221d19",   # header strip
    "BORDER":       "#3b342d",   # warm border
    "BORDER_HOVER": "#4e453b",
    "BORDER_FOCUS": "#eb9457",   # orange focus ring
    "ACCENT":       "#eb9457",   # warm orange accent (selection, highlights)
    "ACCD":         "#d67b3d",   # darker orange (pressed)
    "ACCENT_GLOW":  "#eb945725",
    "GREEN":        "#8cb46a",   # warm sage green
    "GREEN_DIM":    "#7aa35a",
    "ORANGE":       "#e7a44f",   # amber
    "ORANGE_DIM":   "#d8933e",
    "RED_C":        "#e07c5e",   # terracotta red
    "RED_DIM":      "#cc6b4e",
    "BLUE":         "#74a6c4",   # softened info blue (cool contrast)
    "TEAL":         "#5fb3a1",   # warm teal
    "PURPLE":       "#bb8fc6",   # warm lavender
    "CYAN":         "#6fb3bd",
    "FG1":          "#f5ede2",   # warm off-white text
    "FG2":          "#d2c6b6",   # warm light gray
    "FG3":          "#9b9081",   # warm muted
    "FG4":          "#645b50",   # warm faint
    "STATUS_BG":    "#171311",
    "SIDEBAR":      "#171311",
    "CARD":         "#272220",
    "DARK":         "#1c1916",
    "CARD_BG_1":    "#23262e",  # blue-tinted card accent
    "CARD_BG_2":    "#262c1d",  # green-tinted card accent
    "CARD_BG_3":    "#312719",  # orange-tinted card accent
    "CARD_BG_4":    "#312018",  # red-tinted card accent
    "CARD_BG_5":    "#2b232f",  # purple-tinted card accent
    "NAV_ACTIVE_BG":"#3d2c1a",  # active sidebar tab background (warm, dark)
}

# ══════════════════════════════════════════════════════════════════
#  Active palette (initially light)
# ══════════════════════════════════════════════════════════════════

BG           = "#f4f5f7"
BG_CARD      = "#ffffff"
BG_SIDEBAR   = "#1e1e2e"
BG_HOVER     = "#eaeaea"
BG_INPUT     = "#ffffff"
BG_HEADER    = "#ffffff"
BORDER       = "#dde0e8"
BORDER_HOVER = "#ccd0d8"
BORDER_FOCUS = "#FA7567"
ACCENT       = "#FA7567"
ACCD         = "#e06050"
ACCENT_GLOW  = "#FA756725"
GREEN        = "#1db954"
GREEN_DIM    = "#16a34a"
ORANGE       = "#f0960a"
ORANGE_DIM   = "#e08600"
RED_C        = "#e03030"
RED_DIM      = "#c02020"
BLUE         = "#2979ff"
TEAL         = "#00b4ab"
PURPLE       = "#7c4dff"
CYAN         = "#00bcd4"
FG1          = "#1a1a2e"
FG2          = "#444466"
FG3          = "#9999bb"
FG4          = "#bbbbcc"
STATUS_BG    = "#e8e8e8"
SIDEBAR      = "#1e1e2e"
CARD         = "#ffffff"
DARK         = "#0d1117"
CARD_BG_1    = "#e3f2fd"
CARD_BG_2    = "#e8f5e9"
CARD_BG_3    = "#fff3e0"
CARD_BG_4    = "#fce4ec"
CARD_BG_5    = "#f3e5f5"
NAV_ACTIVE_BG= "#1a3a5c"
CONNECTED    = GREEN
DISCONNECTED = FG3
CONNECTING   = ORANGE


def _apply_theme():
    global BG, BG_CARD, BG_SIDEBAR, BG_HOVER, BG_INPUT, BG_HEADER
    global BORDER, BORDER_HOVER, BORDER_FOCUS
    global ACCENT, ACCD, ACCENT_GLOW
    global GREEN, GREEN_DIM, ORANGE, ORANGE_DIM, RED_C, RED_DIM
    global BLUE, TEAL, PURPLE, CYAN
    global FG1, FG2, FG3, FG4
    global STATUS_BG, SIDEBAR, CARD, DARK
    global CONNECTED, DISCONNECTED, CONNECTING
    global CARD_BG_1, CARD_BG_2, CARD_BG_3, CARD_BG_4, CARD_BG_5
    global NAV_ACTIVE_BG

    pal = _DARK if _theme == "dark" else _LIGHT
    BG           = pal["BG"]
    BG_CARD      = pal["BG_CARD"]
    BG_SIDEBAR   = pal["BG_SIDEBAR"]
    BG_HOVER     = pal["BG_HOVER"]
    BG_INPUT     = pal["BG_INPUT"]
    BG_HEADER    = pal["BG_HEADER"]
    BORDER       = pal["BORDER"]
    BORDER_HOVER = pal["BORDER_HOVER"]
    BORDER_FOCUS = pal["BORDER_FOCUS"]
    ACCENT       = pal["ACCENT"]
    ACCD         = pal["ACCD"]
    ACCENT_GLOW  = pal.get("ACCENT_GLOW", "#1976d225")
    GREEN        = pal["GREEN"]
    GREEN_DIM    = pal["GREEN_DIM"]
    ORANGE       = pal["ORANGE"]
    ORANGE_DIM   = pal["ORANGE_DIM"]
    RED_C        = pal["RED_C"]
    RED_DIM      = pal["RED_DIM"]
    BLUE         = pal["BLUE"]
    TEAL         = pal["TEAL"]
    PURPLE       = pal["PURPLE"]
    CYAN         = pal["CYAN"]
    FG1          = pal["FG1"]
    FG2          = pal["FG2"]
    FG3          = pal["FG3"]
    FG4          = pal["FG4"]
    STATUS_BG    = pal["STATUS_BG"]
    SIDEBAR      = pal["SIDEBAR"]
    CARD         = pal["CARD"]
    DARK         = pal["DARK"]
    CARD_BG_1    = pal["CARD_BG_1"]
    CARD_BG_2    = pal["CARD_BG_2"]
    CARD_BG_3    = pal["CARD_BG_3"]
    CARD_BG_4    = pal["CARD_BG_4"]
    CARD_BG_5    = pal["CARD_BG_5"]
    NAV_ACTIVE_BG= pal.get("NAV_ACTIVE_BG", "#1a3a5c")
    CONNECTED    = GREEN
    DISCONNECTED = FG3
    CONNECTING   = ORANGE

# ── Cloudflare / provider IP ranges ─────────────────────────────
CLOUDFLARE_RANGES = (
    "173.245.48.0/20,103.21.244.0/22,103.22.200.0/22,103.31.4.0/22,"
    "141.101.64.0/18,108.162.192.0/18,190.93.240.0/20,188.114.96.0/20,"
    "197.234.240.0/22,198.41.128.0/17,162.158.0.0/15,104.16.0.0/13,"
    "104.24.0.0/14,172.64.0.0/13,131.0.72.0/22"
)

PROVIDER_RANGES = {
    "Custom":                              "",
    "CF 173.245.48.0/20":                  "173.245.48.0/20",
    "CF 103.21.244.0/22":                  "103.21.244.0/22",
    "CF 141.101.64.0/18":                  "141.101.64.0/18",
    "CF 108.162.192.0/18":                 "108.162.192.0/18",
    "CF 190.93.240.0/20":                  "190.93.240.0/20",
    "CF 188.114.96.0/20":                  "188.114.96.0/20",
    "CF 197.234.240.0/22":                 "197.234.240.0/22",
    "CF 131.0.72.0/22":                    "131.0.72.0/22",
    "CF 103.31.4.0/22":                    "103.31.4.0/22",
    "CF 103.22.200.0/22":                  "103.22.200.0/22",
    "CF 162.158.0.0/15 (big)":            "162.158.0.0/15",
    "CF 198.41.128.0/17 (big)":           "198.41.128.0/17",
    "CF 104.16.0.0/16 (a)":              "104.16.0.0/16",
    "CF 104.17.0.0/16 (b)":              "104.17.0.0/16",
    "CF 104.18.0.0/16 (c)":              "104.18.0.0/16",
    "CF 104.19.0.0/16 (d)":              "104.19.0.0/16",
    "CF 104.20.0.0/14":                   "104.20.0.0/14",
    "CF 104.24.0.0/14":                   "104.24.0.0/14",
    "CF 172.64.0.0/16 (a)":              "172.64.0.0/16",
    "CF 172.65.0.0/16 (b)":              "172.65.0.0/16",
    "CF 172.66.0.0/16 (c)":              "172.66.0.0/16",
    "CF 172.67.0.0/16 (d)":              "172.67.0.0/16",
    "CF All (small ranges)":              (
        "173.245.48.0/20,103.21.244.0/22,103.22.200.0/22,103.31.4.0/22,"
        "141.101.64.0/18,108.162.192.0/18,190.93.240.0/20,188.114.96.0/20,"
        "197.234.240.0/22,162.158.0.0/15,198.41.128.0/17,"
        "104.16.0.0/16,104.17.0.0/16,104.18.0.0/16,104.19.0.0/16,"
        "104.20.0.0/14,104.24.0.0/14,"
        "172.64.0.0/16,172.65.0.0/16,172.66.0.0/16,172.67.0.0/16,"
        "131.0.72.0/22"
    ),
    "Vercel Edge (76.76.21/24)":           "76.76.21.0/24",
    "Vercel Broad (76.76/16)":             "76.76.0.0/16",
    "Fastly":                              (
        "151.101.0.0/16,157.52.64.0/18,167.82.0.0/17,"
        "185.31.16.0/22,199.232.0.0/16,103.245.222.0/24,199.27.72.0/21"
    ),
    "Netlify":                             "netlify.app",
}

CF_PORTS    = [443, 8443, 2053, 2083, 2087, 2096]
DL_TEST_URL = "https://speed.cloudflare.com/__down?bytes=3000000"
UL_TEST_URL = "https://speed.cloudflare.com/__up"

# ══════════════════════════════════════════════════════════════════
#  Typography
# ══════════════════════════════════════════════════════════════════

# ── Font families ───────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"
MONO_FAMILY  = "Cascadia Code"

# ── Font tuples ─────────────────────────────────────────────────
FT = (FONT_FAMILY, 14, "bold")     # Page title
FH = (FONT_FAMILY, 10, "bold")     # Section heading
FB = (FONT_FAMILY, 9)              # Body text
FS = (FONT_FAMILY, 8)              # Small text
FM = (MONO_FAMILY, 8)             # Monospace (logs, IPs)
FI = ("Segoe UI Emoji", 14)        # Sidebar icons
FI_SMALL = ("Segoe UI Emoji", 16)  # Sidebar tab icons (a bit larger)

# ── Status bar font ────────────────────────────────────────────
F_STATUS = (FONT_FAMILY, 8)
F_STATUS_BOLD = (FONT_FAMILY, 8, "bold")
F_SPEED  = (MONO_FAMILY, 10, "bold")


# ══════════════════════════════════════════════════════════════════
#  Formatting helpers
# ══════════════════════════════════════════════════════════════════

def _fmt_bytes(b: int) -> str:
    if b < 1024:      return f"{b} B"
    if b < 1024**2:   return f"{b/1024:.1f} KB"
    if b < 1024**3:   return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def _fmt_speed(bps: float) -> str:
    if bps < 1024:      return f"{bps:.0f} B/s"
    if bps < 1024**2:   return f"{bps/1024:.1f} KB/s"
    return f"{bps/1024**2:.2f} MB/s"

def _fmt_speed_short(bps: float) -> str:
    if bps < 1024:        return f"{bps:.0f} B"
    if bps < 1024**2:     return f"{bps/1024:.1f}K"
    return f"{bps/1024**2:.1f}M"


# ============================================================
#  Module: crash
# ============================================================


import os
import sys


def _crash(tb: str) -> str:
    base = (os.path.dirname(os.path.abspath(__file__))
            if not getattr(sys, "frozen", False)
            else os.path.dirname(sys.executable))
    p = os.path.join(base, "crash.log")
    try:
        with open(p, "w", encoding="utf-8") as f: f.write(tb)
    except Exception: pass
    return p


# ============================================================
#  Module: models
# ============================================================


from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProbeResult:
    ip:        str
    port:      int
    mode:      str
    ping_ms:   Optional[float]
    error:     Optional[str]
    tcp_ms:    Optional[float] = field(default=None)
    icmp_ms:   Optional[float] = field(default=None)
    dl_mbps:   Optional[float] = field(default=None)
    up_mbps:   Optional[float] = field(default=None)
    lat_ms:    Optional[float] = field(default=None)
    tested:    bool            = field(default=False)
    loss_pct:  Optional[float] = field(default=None)
    jitter_ms: Optional[float] = field(default=None)
    colo:      str             = field(default="")
    cf_valid:  bool            = field(default=False)

    _FIELDS = ("ip","port","mode","ping_ms","error","tcp_ms",
               "icmp_ms","dl_mbps","up_mbps","lat_ms","tested",
               "loss_pct","jitter_ms","colo","cf_valid")

    def to_dict(self):
        return {k: getattr(self, k) for k in self._FIELDS}

    @classmethod
    def from_dict(cls, d):
        kw = {k: d[k] for k in cls._FIELDS if k in d}
        for req, dflt in [("ip",""),("port",443),("mode","http"),
                           ("ping_ms",None),("error",None)]:
            kw.setdefault(req, dflt)
        return cls(**kw)


@dataclass
class ConfigProfile:
    name:        str
    uid:         str        = ""
    host:        str        = ""
    sni:         str        = ""
    path:        str        = "/"
    cfg_name:    str        = "Edge-Optimized"
    network:     str        = "ws"
    security:    str        = "tls"
    fp:          str        = "chrome"
    alpn:        str        = "http/1.1"
    allow_insecure: bool    = False
    grpc_service: str       = ""
    range_raw:   str        = ""
    range_name:  str        = "Custom"
    ports:       List[int]  = field(default_factory=lambda: [443])
    mode:        str        = "http"
    threads:     int        = 200
    timeout:     float      = 5.0
    top_n:       int        = 20
    results:     List[ProbeResult] = field(default_factory=list)
    scanned:     int        = 0
    scan_time:   str        = ""
    built_configs: List[str] = field(default_factory=list)
    scan_history: List[dict] = field(default_factory=list)
    favorites:   List[dict]  = field(default_factory=list)
    cf_workers:  List[dict]  = field(default_factory=list)

    @property
    def has_config(self) -> bool:
        return bool(self.uid.strip() and self.host.strip())

    def to_dict(self):
        return {
            "name": self.name, "uid": self.uid, "host": self.host,
            "sni": self.sni, "path": self.path, "cfg_name": self.cfg_name,
            "network": self.network, "security": self.security,
            "fp": self.fp, "alpn": self.alpn,
            "allow_insecure": self.allow_insecure,
            "grpc_service": self.grpc_service,
            "range_raw": self.range_raw, "range_name": self.range_name,
            "ports": self.ports, "mode": self.mode,
            "threads": self.threads, "timeout": self.timeout, "top_n": self.top_n,
            "results": [r.to_dict() for r in self.results],
            "scanned": self.scanned, "scan_time": self.scan_time,
            "built_configs": self.built_configs,
            "scan_history": self.scan_history,
            "favorites": self.favorites,
            "cf_workers": self.cf_workers,
        }

    @classmethod
    def from_dict(cls, d):
        p = cls(name=d.get("name","Profile"))
        for k in ("uid","host","sni","path","cfg_name","network","security",
                  "fp","alpn","allow_insecure","grpc_service",
                  "range_raw","range_name","ports","mode","threads","timeout",
                  "top_n","scanned","scan_time","built_configs",
                  "scan_history","favorites","cf_workers"):
            if k in d: setattr(p, k, d[k])
        p.results = [ProbeResult.from_dict(r) for r in d.get("results",[])]
        return p


# ============================================================
#  Module: persistence
# ============================================================


import json
import os
import sys
from typing import List, Tuple



def _profiles_path() -> str:
    base = (os.path.dirname(os.path.abspath(__file__))
            if not getattr(sys, "frozen", False)
            else os.path.dirname(sys.executable))
    return os.path.join(base, "vless_profiles.json")

def _theme_path() -> str:
    base = (os.path.dirname(os.path.abspath(__file__))
            if not getattr(sys, "frozen", False)
            else os.path.dirname(sys.executable))
    return os.path.join(base, "vless_theme.json")

def save_theme_pref(name: str) -> None:
    try:
        with open(_theme_path(), "w", encoding="utf-8") as f:
            json.dump({"theme": name}, f)
    except Exception:
        pass

def load_theme_pref() -> str:
    try:
        with open(_theme_path(), "r", encoding="utf-8") as f:
            t = json.load(f).get("theme", "light")
        return t if t in ("light", "dark") else "light"
    except Exception:
        return "light"

def save_profiles(profiles: List[ConfigProfile], idx: int) -> bool:
    try:
        data = {"active": idx, "profiles": [p.to_dict() for p in profiles]}
        path = _profiles_path()
        tmp  = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
        return True
    except Exception as e:
        try:
            print(f"[save_profiles] ERROR: {e}", file=sys.stderr)
        except Exception:
            pass
        return False

def load_profiles() -> Tuple[List[ConfigProfile], int]:
    try:
        with open(_profiles_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        profiles = []
        for d in data.get("profiles", []):
            p = ConfigProfile.from_dict(d)
            p.results      = []
            p.scanned      = 0
            p.scan_time    = ""
            p.built_configs= []
            profiles.append(p)
        idx = data.get("active", 0)
        if profiles:
            return profiles, max(0, min(idx, len(profiles)-1))
    except Exception:
        pass
    return [ConfigProfile(name="Profile 1")], 0


def load_profiles_with_data() -> Tuple[List[ConfigProfile], int]:
    try:
        with open(_profiles_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        profiles = [ConfigProfile.from_dict(d) for d in data.get("profiles", [])]
        idx = data.get("active", 0)
        if profiles:
            return profiles, max(0, min(idx, len(profiles)-1))
    except Exception:
        pass
    return [ConfigProfile(name="Profile 1")], 0


# ============================================================
#  Module: scanner
# ============================================================


import asyncio
import ipaddress
import socket
import ssl
import time
from typing import List, Optional, Tuple, Set



_CF_SNI_ROTATE = [
    "speed.cloudflare.com",
    "cloudflare.com",
    "www.cloudflare.com",
    "blog.cloudflare.com",
]


class Optimizer:
    def __init__(self, concurrency: int = 200, timeout: float = 5.0, tries: int = 4):
        self.sem     = asyncio.Semaphore(concurrency)
        self.timeout = timeout
        self.tries   = max(1, tries)
        self._ssl    = ssl.create_default_context()
        self._ssl.check_hostname = False
        self._ssl.verify_mode    = ssl.CERT_NONE

    @staticmethod
    def fix_range(raw: str) -> List[str]:
        s = raw.strip()
        if not s: return []
        if "," in s:
            out: List[str] = []
            seen: Set[str] = set()
            for part in s.split(","):
                for ip in Optimizer.fix_range(part.strip()):
                    if ip not in seen:
                        seen.add(ip); out.append(ip)
            return out[:65536]
        if any(c.isalpha() for c in s):
            try:
                return list({x[4][0] for x in
                    socket.getaddrinfo(s, None, socket.AF_INET)})[:65536]
            except Exception: return []
        if "-" in s:
            a, b = s.split("-", 1)
            try:
                si = int(ipaddress.ip_address(a.strip()))
                ei = int(ipaddress.ip_address(b.strip()))
                if si > ei: si, ei = ei, si
                if ei - si + 1 > 65536: ei = si + 65535
                return [str(ipaddress.ip_address(i)) for i in range(si, ei+1)]
            except Exception: return []
        try:
            net = ipaddress.ip_network(s, strict=False)
            h = list(net.hosts()) or [net.network_address]
            return [str(x) for x in h[:65536]]
        except ValueError: return []

    async def probe(self, ip, port, mode, sni, host, path) -> ProbeResult:
        async with self.sem:
            latencies: List[float] = []
            last_error: Optional[str] = None

            for attempt in range(self.tries):
                eff_sni = sni or host or _CF_SNI_ROTATE[attempt % len(_CF_SNI_ROTATE)]

                ok, tcp_ms = await self._tcp(ip, port)
                if not ok:
                    last_error = "tcp-fail"
                    continue

                if mode == "tcp":
                    latencies.append(tcp_ms)
                elif mode == "tls":
                    r = await self._tls_raw(ip, port, eff_sni)
                    if r is not None:
                        latencies.append(r)
                    else:
                        last_error = "tls-fail"
                else:
                    r = await self._http_raw(ip, port, eff_sni, host, path or "/")
                    if r is not None:
                        latencies.append(r)
                    else:
                        last_error = "http-fail"

            if not latencies:
                return ProbeResult(ip, port, mode, None, last_error or "all-fail")

            avg_ms    = sum(latencies) / len(latencies)
            jitter_ms = max(latencies) - min(latencies) if len(latencies) > 1 else 0.0
            loss_pct  = (self.tries - len(latencies)) / self.tries * 100.0

            colo, cf_valid = "", False
            if mode == "http":
                trace_sni = sni or host or "speed.cloudflare.com"
                colo, cf_valid = await self._cf_trace(ip, port, trace_sni)

            return ProbeResult(
                ip=ip, port=port, mode=mode,
                ping_ms=avg_ms, error=None,
                loss_pct=loss_pct, jitter_ms=jitter_ms,
                colo=colo, cf_valid=cf_valid,
            )

    async def _tcp(self, ip, port) -> Tuple[bool, float]:
        t0 = time.perf_counter()
        try:
            _, w = await asyncio.wait_for(asyncio.open_connection(ip, port),
                                          timeout=self.timeout)
            w.close()
            try: await asyncio.wait_for(w.wait_closed(), 1.0)
            except Exception: pass
            return True, (time.perf_counter()-t0)*1000
        except Exception: return False, 0.0

    async def _tls_raw(self, ip, port, sni) -> Optional[float]:
        t0 = time.perf_counter()
        kw = {"ssl": self._ssl}
        if sni: kw["server_hostname"] = sni
        try:
            _, w = await asyncio.wait_for(asyncio.open_connection(ip, port, **kw),
                                          timeout=self.timeout)
            w.close()
            try: await asyncio.wait_for(w.wait_closed(), 1.0)
            except Exception: pass
            return (time.perf_counter()-t0)*1000
        except Exception: return None

    async def _http_raw(self, ip, port, sni, host, path) -> Optional[float]:
        import base64 as _b64, os as _os

        async def _inner():
            ws_key   = _b64.b64encode(_os.urandom(16)).decode()
            kw       = {"ssl": self._ssl}
            if sni:  kw["server_hostname"] = sni
            req_host = host or sni or ip
            r, w = await asyncio.open_connection(ip, port, **kw)
            try:
                w.write((
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {req_host}\r\n"
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Key: {ws_key}\r\n"
                    "Sec-WebSocket-Version: 13\r\n"
                    "\r\n"
                ).encode())
                await w.drain()
                return await r.readline()
            finally:
                w.close()
                try: await asyncio.wait_for(w.wait_closed(), 0.5)
                except Exception: pass

        t0 = time.perf_counter()
        try:
            line  = await asyncio.wait_for(_inner(), timeout=self.timeout)
            parts = line.split()
            if len(parts) < 2 or parts[1] != b"101":
                return None
            return (time.perf_counter() - t0) * 1000
        except Exception:
            return None

    async def _cf_trace(self, ip, port, sni) -> Tuple[str, bool]:
        try:
            kw = {"ssl": self._ssl}
            if sni: kw["server_hostname"] = sni
            r, w = await asyncio.wait_for(
                asyncio.open_connection(ip, port, **kw), timeout=self.timeout)
            w.write((f"GET /cdn-cgi/trace HTTP/1.1\r\nHost: {sni or ip}\r\n"
                     "User-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n").encode())
            await asyncio.wait_for(w.drain(), timeout=self.timeout)
            raw = b""
            for _ in range(40):
                chunk = await asyncio.wait_for(r.read(512), timeout=self.timeout)
                if not chunk: break
                raw += chunk
                if b"\r\n\r\n" in raw and b"colo=" in raw: break
            w.close()
            try: await asyncio.wait_for(w.wait_closed(), 1.0)
            except Exception: pass
            body = raw.decode(errors="ignore")
            if "colo=" not in body: return "", False
            colo = ""
            for line in body.splitlines():
                if line.startswith("colo="):
                    colo = line.split("=",1)[1].strip()
                    break
            return colo, bool(colo)
        except Exception:
            return "", False


# ============================================================
#  Module: tun_manager
# ============================================================


import os
import platform
import subprocess
import sys
import time
import urllib.request
import zipfile
from typing import Optional, Tuple


class TunManager:
    WINTUN_URL = "https://www.wintun.net/builds/wintun-0.14.1.zip"
    TUN_NAME    = "VLESSEdgeTun"
    TUN_ADDR4   = "198.18.0.1"
    TUN_PREFIX4 = 16
    TUN_DNS     = "1.1.1.1"

    def __init__(self, tools_dir: str):
        self.tools_dir  = tools_dir
        self.dll_path   = os.path.join(tools_dir, "wintun.dll")
        self.enabled    = False
        self._server_ip = ""

    def is_supported(self) -> bool:
        return sys.platform == "win32"

    def is_dll_present(self) -> bool:
        return os.path.isfile(self.dll_path)

    def is_admin(self) -> bool:
        if sys.platform != "win32":
            return os.geteuid() == 0
        try:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def download_wintun(self, cb=None) -> Tuple[bool, str]:
        if sys.platform != "win32":
            return False, "wintun is Windows-only."
        try:
            os.makedirs(self.tools_dir, exist_ok=True)
            if cb: cb("Downloading wintun.zip…")
            req = urllib.request.Request(
                self.WINTUN_URL, headers={"User-Agent": "Mozilla/5.0"})
            zip_path = os.path.join(self.tools_dir, "wintun_dl.zip")
            with urllib.request.urlopen(req, timeout=60) as r:
                with open(zip_path, "wb") as f:
                    f.write(r.read())
            if cb: cb("Extracting wintun.dll…")
            machine = platform.machine().lower()
            if   "arm" in machine and "64" in machine: arch = "arm64"
            elif "arm" in machine:                      arch = "arm"
            elif "64"  in machine:                      arch = "amd64"
            else:                                       arch = "x86"
            with zipfile.ZipFile(zip_path) as z:
                names = z.namelist()
                target = next((n for n in names
                               if n.lower().endswith(f"{arch}/wintun.dll")), None)
                if not target:
                    target = next((n for n in names
                                   if n.lower().endswith("wintun.dll")), None)
                if not target:
                    return False, "wintun.dll not found inside zip."
                data = z.read(target)
                with open(self.dll_path, "wb") as f:
                    f.write(data)
            try: os.remove(zip_path)
            except Exception: pass
            if cb: cb(f"✔ wintun.dll saved → {self.dll_path}")
            return True, f"wintun.dll downloaded ({arch})"
        except Exception as e:
            return False, f"Download failed: {e}"

    def mark_enabled(self, server_ip: str = "") -> None:
        self.enabled    = True
        self._server_ip = server_ip

    def mark_disabled(self) -> None:
        self.enabled = False

    @staticmethod
    def _prefix_to_mask(prefix: int) -> str:
        n = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        return ".".join(str((n >> s) & 0xFF) for s in (24, 16, 8, 0))

    def _get_default_gateway(self) -> Optional[str]:
        kw = dict(creationflags=subprocess.CREATE_NO_WINDOW,
                  capture_output=True, text=True)
        try:
            r = subprocess.run(["route", "print", "0.0.0.0"], **kw)
            for line in r.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "0.0.0.0" and parts[1] == "0.0.0.0":
                    gw = parts[2]
                    if not gw.startswith("198.18."):
                        return gw
        except Exception:
            pass
        return None

    def _wait_for_adapter(self, name: str, timeout: float = 12.0) -> bool:
        kw       = dict(creationflags=subprocess.CREATE_NO_WINDOW,
                        capture_output=True, text=True)
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                r = subprocess.run(
                    ["netsh", "interface", "show", "interface"], **kw)
                if name in r.stdout:
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    def setup_tun_adapter(self, name: str, addr: str, prefix: int) -> bool:
        if sys.platform != "win32":
            return False
        mask = self._prefix_to_mask(prefix)
        kw   = dict(creationflags=subprocess.CREATE_NO_WINDOW,
                    capture_output=True, text=True)
        confirmed = False
        for attempt in range(5):
            subprocess.run(
                ["netsh", "interface", "ipv4", "set", "address",
                 f"name={name}", "source=static",
                 f"addr={addr}", f"mask={mask}", "gateway=none"],
                **kw)
            wait = 0.5 + attempt * 0.6
            time.sleep(wait)
            try:
                chk = subprocess.run(
                    ["netsh", "interface", "ipv4", "show", "addresses",
                     f"name={name}"],
                    **kw)
                if addr in chk.stdout:
                    confirmed = True
                    break
            except Exception:
                pass
        if not confirmed:
            return False
        subprocess.run(
            ["netsh", "interface", "ipv4", "set", "dnsservers",
             f"name={name}", "source=static", "addr=1.1.1.1", "validate=no"],
            **kw)
        return True

    def setup_routes(self, gw: str) -> bool:
        if sys.platform != "win32":
            return False
        kw_b = dict(creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        kw_t = dict(creationflags=subprocess.CREATE_NO_WINDOW,
                    capture_output=True, text=True)

        real_gw = self._get_default_gateway()

        if self._server_ip and real_gw:
            subprocess.run(
                ["route", "add", self._server_ip, "mask", "255.255.255.255",
                 real_gw, "metric", "1"],
                **kw_b)

        if real_gw:
            for _net, _mask in (
                ("10.0.0.0",    "255.0.0.0"),
                ("172.16.0.0",  "255.240.0.0"),
                ("192.168.0.0", "255.255.0.0"),
                ("169.254.0.0", "255.255.0.0"),
            ):
                subprocess.run(
                    ["route", "add", _net, "mask", _mask,
                     real_gw, "metric", "3"],
                    **kw_b)

        ok = 0
        for prefix in ("0.0.0.0/1", "128.0.0.0/1"):
            net, bits = prefix.split("/")
            r = subprocess.run(
                ["netsh", "interface", "ipv4", "add", "route",
                 f"prefix={prefix}", f"interface={self.TUN_NAME}",
                 f"nexthop={gw}", "metric=5", "store=active"],
                **kw_t)
            if r.returncode == 0 or "already exists" in (r.stdout + r.stderr).lower():
                ok += 1
            else:
                fb = subprocess.run(
                    ["route", "add", net, "mask", "128.0.0.0",
                     gw, "metric", "5"],
                    **kw_b)
                if fb.returncode == 0:
                    ok += 1
        return ok == 2

    def teardown_routes(self, gw: str) -> None:
        if sys.platform != "win32":
            return
        kw_b = dict(creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        kw_t = dict(creationflags=subprocess.CREATE_NO_WINDOW,
                    capture_output=True, text=True)
        for prefix in ("0.0.0.0/1", "128.0.0.0/1"):
            net = prefix.split("/")[0]
            subprocess.run(
                ["netsh", "interface", "ipv4", "delete", "route",
                 f"prefix={prefix}", f"interface={self.TUN_NAME}"],
                **kw_t)
            subprocess.run(
                ["route", "delete", net, "mask", "128.0.0.0", gw],
                **kw_b)
        if self._server_ip:
            subprocess.run(
                ["route", "delete", self._server_ip, "mask", "255.255.255.255"],
                **kw_b)
        for _net, _mask in (
            ("10.0.0.0",    "255.0.0.0"),
            ("172.16.0.0",  "255.240.0.0"),
            ("192.168.0.0", "255.255.0.0"),
            ("169.254.0.0", "255.255.0.0"),
        ):
            subprocess.run(
                ["route", "delete", _net, "mask", _mask],
                **kw_b)


# ============================================================
#  Module: xray_manager
# ============================================================


import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile


class XrayManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__))
                if not getattr(sys, "frozen", False)
                else os.path.dirname(sys.executable), "tools")
        self.base_dir  = base_dir
        self.xray_path = os.path.join(base_dir,
                         "xray.exe" if sys.platform == "win32" else "xray")
        self._proc:     Optional[subprocess.Popen] = None
        self._cfg_path: Optional[str] = None

    def is_installed(self) -> bool:
        if os.path.isfile(self.xray_path): return True
        p = shutil.which("xray.exe" if sys.platform == "win32" else "xray")
        if p: self.xray_path = p; return True
        return False

    @staticmethod
    def get_free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0)); return s.getsockname()[1]

    @staticmethod
    def _pick_asset(assets):
        plat    = sys.platform
        machine = platform.machine().lower()
        is_arm  = "arm" in machine or "aarch" in machine
        pk      = {"win32":"windows","linux":"linux","darwin":"macos"}.get(plat, plat)
        cands   = []
        for a in assets:
            nm = a.get("name","").lower()
            if pk not in nm: continue
            if is_arm:
                if "arm64" in nm or "aarch64" in nm: cands.append(a)
            else:
                if "64" in nm and "arm" not in nm: cands.append(a)
        if not cands:
            cands = [a for a in assets if pk in a.get("name","").lower()]
        return cands[0] if cands else None

    def download(self, cb=None) -> bool:
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            url = ext = None
            try:
                req = urllib.request.Request(
                    "https://api.github.com/repos/XTLS/Xray-core/releases/latest",
                    headers={"User-Agent":"Mozilla/5.0",
                             "Accept":"application/vnd.github+json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    data = json.loads(r.read())
                asset = self._pick_asset(data.get("assets",[]))
                if asset:
                    url = asset["browser_download_url"]
                    ext = ".zip" if url.lower().endswith(".zip") else ".tar.gz"
            except Exception as e:
                if cb: cb(f"API failed ({e}), using fallback…")
            if not url:
                plat   = "linux" if sys.platform.startswith("linux") else sys.platform
                is_arm = "arm" in platform.machine().lower()
                ak     = "arm64" if is_arm else "64"
                FB_MAP = {
                    ("win32","64"):    "Xray-windows-64.zip",
                    ("win32","arm64"): "Xray-windows-arm64-v8a.zip",
                    ("linux","64"):    "Xray-linux-64.zip",
                    ("linux","arm64"): "Xray-linux-arm64-v8a.zip",
                    ("darwin","64"):   "Xray-macos-64.zip",
                    ("darwin","arm64"):"Xray-macos-arm64-v8a.zip",
                }
                fn = FB_MAP.get((plat,ak)) or FB_MAP.get((plat,"64"))
                if not fn: raise RuntimeError("Unsupported platform")
                url = ("https://github.com/XTLS/Xray-core/releases/latest"
                       f"/download/{fn}")
                ext = ".zip"
            if cb: cb(f"Downloading {url.split('/')[-1]}…")
            dl = os.path.join(self.base_dir, f"xray_dl{ext}")
            req2 = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req2, timeout=120) as r:
                with open(dl,"wb") as f: f.write(r.read())
            if cb: cb("Extracting…")
            if ext == ".zip":
                with zipfile.ZipFile(dl) as z: z.extractall(self.base_dir)
            else:
                with tarfile.open(dl,"r:gz") as t: t.extractall(self.base_dir)
            try: os.remove(dl)
            except Exception: pass
            target = "xray.exe" if sys.platform == "win32" else "xray"
            for root_d,_,files in os.walk(self.base_dir):
                for f in files:
                    if f.lower() == target.lower():
                        src = os.path.join(root_d,f)
                        if os.path.abspath(src) != os.path.abspath(self.xray_path):
                            shutil.move(src, self.xray_path)
                        if not sys.platform.startswith("win"):
                            os.chmod(self.xray_path, 0o755)
                        return True
            raise RuntimeError("Binary not in archive")
        except Exception as e:
            if cb: cb(f"Error: {e}")
            return False

    @staticmethod
    def _stream_settings(p: "ConfigProfile", ip: str) -> dict:
        net = p.network or "ws"
        sec = p.security or "tls"
        host = p.host or ip
        sni  = p.sni or host
        path = p.path or "/"
        tls  = {"serverName": sni,
                "fingerprint": p.fp or "chrome",
                "allowInsecure": p.allow_insecure}
        alpn = [a.strip() for a in p.alpn.split(",") if a.strip()]
        if alpn: tls["alpn"] = alpn

        ss: dict = {"network": net, "security": sec}
        if sec == "tls": ss["tlsSettings"] = tls

        if net == "ws":
            ss["wsSettings"] = {"path": path, "host": host}
        elif net == "grpc":
            ss["grpcSettings"] = {"serviceName": p.grpc_service or "grpc"}
        elif net == "h2":
            ss["httpSettings"] = {"path": path, "host": [host]}
        return ss

    @staticmethod
    def build_test(ip, port, uid, host, sni, path, lport, profile=None):
        uid  = uid or "00000000-0000-0000-0000-000000000000"
        host = host or ip
        sni  = sni or host

        if profile:
            ss = XrayManager._stream_settings(profile, ip)
        else:
            ss = {"network":"ws","security":"tls",
                  "tlsSettings":{"serverName":sni,"fingerprint":"chrome",
                                 "allowInsecure":False},
                  "wsSettings":{"path":path,"host":host}}
        return {
            "log":{"loglevel":"warning"},
            "inbounds":[{"tag":"http","protocol":"http",
                         "listen":"127.0.0.1","port":lport,"settings":{}}],
            "outbounds":[{"tag":"proxy","protocol":"vless",
                "settings":{"vnext":[{"address":ip,"port":port,
                    "users":[{"id":uid,"encryption":"none"}]}]},
                "streamSettings": ss}],
        }

    @staticmethod
    def build_proxy(ip, port, uid, host, sni, path, socks=10808, http_p=10809,
                    profile=None, loglevel="warning", stats_port=None):
        uid  = uid or "00000000-0000-0000-0000-000000000000"
        host = host or ip
        sni  = sni or host

        if profile:
            ss = XrayManager._stream_settings(profile, ip)
        else:
            ss = {"network":"ws","security":"tls",
                  "tlsSettings":{"serverName":sni,"fingerprint":"chrome",
                                 "allowInsecure":False},
                  "wsSettings":{"path":path,"host":host}}

        inbounds = [
            {"tag":"socks","protocol":"socks","listen":"127.0.0.1",
             "port":socks,"settings":{"auth":"noauth","udp":True}},
            {"tag":"http","protocol":"http","listen":"127.0.0.1",
             "port":http_p,"settings":{}},
        ]
        routing_rules: list = []
        if stats_port:
            inbounds.append({
                "tag":"api-in","listen":"127.0.0.1","port":stats_port,
                "protocol":"dokodemo-door","settings":{"address":"127.0.0.1"},
            })
            routing_rules.append({
                "type":"field","inboundTag":["api-in"],"outboundTag":"api",
            })

        cfg: dict = {
            # access:"" → xray writes per-connection access log to stdout,
            # which the Connection Log tab reads (v2rayNG-style live log).
            "log": {"loglevel": loglevel, "access": ""},
            "inbounds": inbounds,
            "outbounds": [
                {"tag":"proxy","protocol":"vless",
                 "settings":{"vnext":[{"address":ip,"port":port,
                     "users":[{"id":uid,"encryption":"none"}]}]},
                 "streamSettings": ss},
                {"tag":"direct","protocol":"freedom","settings":{}},
                {"tag":"block","protocol":"blackhole","settings":{}},
            ],
            "routing": {"domainStrategy":"IPIfNonMatch","rules":routing_rules},
        }
        if stats_port:
            cfg["stats"]  = {}
            cfg["api"]    = {"tag":"api","services":["StatsService"]}
            cfg["policy"] = {"system":{
                "statsInboundUplink":True,"statsInboundDownlink":True,
                "statsOutboundUplink":True,"statsOutboundDownlink":True,
            }}
        return cfg

    @staticmethod
    def build_tun(ip, port, uid, host, sni, path, profile=None,
                  tun_name="VLESSEdgeTun", tun_addr="198.18.0.1",
                  tun_prefix=16, dns="1.1.1.1", loglevel="warning",
                  stats_port=None):
        uid  = uid  or "00000000-0000-0000-0000-000000000000"
        host = host or ip
        sni  = sni  or host

        if profile:
            ss = XrayManager._stream_settings(profile, ip)
        else:
            ss = {"network": "ws", "security": "tls",
                  "tlsSettings": {"serverName": sni, "fingerprint": "chrome",
                                  "allowInsecure": False},
                  "wsSettings":  {"path": path, "host": host}}

        PRIVATE_CIDRS = [
            "0.0.0.0/8", "10.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16",
            "172.16.0.0/12", "192.168.0.0/16", "224.0.0.0/4",
            "240.0.0.0/4", "255.255.255.255/32",
        ]

        _cfg = {
            # access:"" → xray writes per-connection access log to stdout,
            # which the Connection Log tab reads (v2rayNG-style live log).
            "log": {"loglevel": loglevel, "access": ""},
            "dns": {
                "hosts": {
                    "cloudflare-dns.com": ["1.1.1.1", "1.0.0.1"],
                    "dns.google":         ["8.8.8.8", "8.8.4.4"],
                },
                "servers": [
                    {"address": "https://cloudflare-dns.com/dns-query",
                     "queryStrategy": "UseIPv4"},
                    {"address": "https://dns.google/dns-query",
                     "queryStrategy": "UseIPv4"},
                ],
                "disableCache":    False,
                "disableFallback": False,
            },
            "inbounds": [
                {
                    "tag":      "tun-in",
                    "protocol": "tun",
                    "settings": {
                        "address": f"{tun_addr}/{tun_prefix}",
                        "mtu":     1400,
                        "name":    tun_name,
                    },
                    "sniffing": {
                        "enabled":             True,
                        "destOverride":        ["http", "tls", "quic"],
                        "routeOnly":           True,
                    },
                }
            ],
            "outbounds": [
                {
                    "tag":      "proxy",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [{
                            "address": ip,
                            "port":    port,
                            "users":   [{"id": uid, "encryption": "none"}],
                        }]
                    },
                    "streamSettings": ss,
                },
                {"tag": "direct",  "protocol": "freedom",   "settings": {}},
                {"tag": "block",   "protocol": "blackhole",  "settings": {}},
                {"tag": "dns-out", "protocol": "dns", "settings": {}},
            ],
            "policy": {
                "levels": {
                    "0": {
                        "connIdle":    30,
                        "uplinkOnly":  1,
                        "downlinkOnly": 2,
                    }
                }
            },
            "routing": {
                "domainStrategy": "IPIfNonMatch",
                "rules": [
                    {
                        "type":        "field",
                        "network":     "udp",
                        "port":        "67-68,123,137-139,547,1900,3702,5353,5355",
                        "outboundTag": "block",
                    },
                    {
                        "type":        "field",
                        "ip":          [ip],
                        "outboundTag": "direct",
                    },
                    {
                        "type":        "field",
                        "ip":          ["198.18.0.0/15",
                                        "198.18.255.255/32",
                                        "198.19.255.255/32"],
                        "outboundTag": "block",
                    },
                    {
                        "type":        "field",
                        "ip":          PRIVATE_CIDRS,
                        "outboundTag": "direct",
                    },
                    {
                        "type":        "field",
                        "port":        "53",
                        "outboundTag": "dns-out",
                    },
                    {
                        "type":        "field",
                        "network":     "udp",
                        "port":        "443",
                        "outboundTag": "block",
                    },
                    {
                        "type":        "field",
                        "network":     "tcp,udp",
                        "outboundTag": "proxy",
                    },
                ],
            },
        }
        if stats_port:
            _cfg["stats"] = {}
            _cfg["api"]   = {"tag": "api", "services": ["StatsService"]}
            _cfg["policy"]["system"] = {
                "statsInboundUplink":    True,
                "statsInboundDownlink":  True,
                "statsOutboundUplink":   True,
                "statsOutboundDownlink": True,
            }
            _cfg["inbounds"].append({
                "tag": "api-in", "listen": "127.0.0.1", "port": stats_port,
                "protocol": "dokodemo-door", "settings": {"address": "127.0.0.1"},
            })
            _cfg["routing"]["rules"].insert(0, {
                "type": "field", "inboundTag": ["api-in"], "outboundTag": "api",
            })
        return _cfg

    def start(self, cfg: dict) -> Optional[subprocess.Popen]:
        fd, cp = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd,"w") as f: json.dump(cfg,f)
        kw: dict = {}
        if sys.platform == "win32":
            kw["creationflags"] = subprocess.CREATE_NO_WINDOW
        self._proc = subprocess.Popen(
            [self.xray_path,"-c",cp],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kw)
        self._cfg_path = cp
        return self._proc

    def stop(self):
        proc = self._proc
        self._proc = None
        if proc:
            try: proc.terminate()
            except Exception: pass
            try: proc.wait(timeout=2)
            except Exception: pass
            try:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=2)
            except Exception: pass
            try:
                if proc.pid and proc.poll() is None:
                    if sys.platform == "win32":
                        subprocess.call(
                            ["taskkill","/F","/PID",str(proc.pid)],
                            creationflags=subprocess.CREATE_NO_WINDOW)
                    else:
                        os.kill(proc.pid, 9)
            except Exception: pass
        if self._cfg_path and os.path.isfile(self._cfg_path):
            try: os.remove(self._cfg_path)
            except Exception: pass
            self._cfg_path = None

    def query_stats(self, stats_port: int) -> Tuple[int, int]:
        kw: dict = {}
        if sys.platform == "win32":
            kw["creationflags"] = subprocess.CREATE_NO_WINDOW
        try:
            r = subprocess.run(
                [self.xray_path, "api", "statsquery",
                 f"--server=127.0.0.1:{stats_port}"],
                capture_output=True, text=True, timeout=5, **kw)
            data = json.loads(r.stdout or "{}")
            ul = dl = 0
            for stat in data.get("stat", []):
                name = stat.get("name", "")
                val  = int(stat.get("value") or 0)
                if   "uplink"   in name: ul += val
                elif "downlink" in name: dl += val
            return ul, dl
        except Exception:
            return 0, 0

    @staticmethod
    def latency(proxy_url) -> Tuple[Optional[float], Optional[str]]:
        try:
            h  = urllib.request.ProxyHandler({"http":proxy_url,"https":proxy_url})
            op = urllib.request.build_opener(h)
            req = urllib.request.Request("http://www.gstatic.com/generate_204",
                                         headers={"User-Agent":"Mozilla/5.0"})
            t0 = time.perf_counter()
            with op.open(req, timeout=10): pass
            return (time.perf_counter()-t0)*1000, None
        except Exception as e: return None, str(e)

    @staticmethod
    def latency_direct() -> Tuple[Optional[float], Optional[str]]:
        try:
            req = urllib.request.Request(
                "http://www.gstatic.com/generate_204",
                headers={"User-Agent": "Mozilla/5.0"})
            t0 = time.perf_counter()
            with urllib.request.urlopen(req, timeout=10): pass
            return (time.perf_counter() - t0) * 1000, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def dl_speed(proxy_url) -> Tuple[Optional[float], Optional[str]]:
        try:
            h  = urllib.request.ProxyHandler({"http":proxy_url,"https":proxy_url})
            op = urllib.request.build_opener(h)
            req = urllib.request.Request(DL_TEST_URL,
                                         headers={"User-Agent":"Mozilla/5.0"})
            t0 = time.perf_counter()
            with op.open(req, timeout=30) as r: data = r.read()
            el = time.perf_counter()-t0
            if el <= 0: return None,"zero-time"
            return (len(data)*8)/(el*1_000_000), None
        except Exception as e: return None, str(e)

    @staticmethod
    def up_speed(proxy_url, size_bytes: int = 1_000_000) -> Tuple[Optional[float], Optional[str]]:
        """Upload speed via the proxy — POST payload to Cloudflare's __up endpoint."""
        try:
            h  = urllib.request.ProxyHandler({"http":proxy_url,"https":proxy_url})
            op = urllib.request.build_opener(h)
            payload = b"x" * size_bytes
            req = urllib.request.Request(
                UL_TEST_URL, data=payload,
                headers={"User-Agent":"Mozilla/5.0",
                         "Content-Type":"application/octet-stream"})
            t0 = time.perf_counter()
            with op.open(req, timeout=30) as r: r.read()
            el = time.perf_counter()-t0
            if el <= 0: return None,"zero-time"
            return (size_bytes*8)/(el*1_000_000), None
        except Exception as e: return None, str(e)

    @staticmethod
    def icmp(ip) -> Tuple[Optional[float], Optional[str]]:
        import re
        try:
            cmd = (["ping","-n","1","-w","3000",ip]
                   if sys.platform=="win32"
                   else ["ping","-c","1","-W","3",ip])
            kw: dict = {}
            if sys.platform == "win32":
                kw["creationflags"] = subprocess.CREATE_NO_WINDOW
            res = subprocess.run(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=6, **kw)
            out = res.stdout.decode(errors="ignore")
            for pat in [r"time[=<](\d+\.?\d*)ms",
                        r"time[=<](\d+\.?\d*) ms",
                        r"Average = (\d+\.?\d*)ms"]:
                m = re.search(pat, out, re.IGNORECASE)
                if m: return float(m.group(1)), None
            return (0.0,None) if res.returncode==0 else (None,"no-reply")
        except subprocess.TimeoutExpired: return None,"timeout"
        except Exception as e: return None,str(e)


# ============================================================
#  Module: qr
# ============================================================


import sys
import tkinter as tk
from tkinter import messagebox
from typing import List



def _try_install_qr_lib():
    try:
        import subprocess as _sp
        _sp.run(
            [sys.executable, "-m", "pip", "install", "qrcode", "--quiet",
             "--disable-pip-version-check"],
            capture_output=True, timeout=45
        )
    except Exception:
        pass

_QR_LIB_INSTALL_ATTEMPTED = False

class _QR:
    _EXP = [0]*512; _LOG = [0]*256; _x = 1
    for _i in range(255):
        _EXP[_i] = _x; _LOG[_x] = _i
        _x <<= 1
        if _x & 0x100: _x ^= 0x11d
    for _i in range(255,512): _EXP[_i] = _EXP[_i-255]

    @classmethod
    def _mul(cls,a,b):
        return 0 if (a==0 or b==0) else cls._EXP[(cls._LOG[a]+cls._LOG[b])%255]

    @classmethod
    def _rs(cls, data: bytes, nsym: int) -> List[int]:
        gen = [1]
        for i in range(nsym):
            gen = [cls._mul(g,cls._EXP[i])^(gen[j+1] if j+1<len(gen) else 0)
                   for j,g in enumerate(gen)] + [cls._mul(gen[-1],cls._EXP[i])]
        rem = list(data)+[0]*nsym
        for i in range(len(data)):
            c = rem[i]
            if c:
                for j in range(1,len(gen)): rem[i+j] ^= cls._mul(gen[j],c)
        return rem[len(data):]

    @classmethod
    def _bch15_5(cls, val: int) -> int:
        v = val << 10
        for i in range(4, -1, -1):
            if v & (1 << (i + 10)):
                v ^= 0x537 << i
        return (val << 10) | v

    @classmethod
    def _write_format(cls, g, size: int, mask: int):
        fmt_data = (0b00 << 3) | mask
        fmt_word = cls._bch15_5(fmt_data) ^ 0b101010000010010
        pos1 = [(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,7),(8,8),
                (7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8)]
        pos2 = [(8,size-1),(8,size-2),(8,size-3),(8,size-4),(8,size-5),
                (8,size-6),(8,size-7),(size-8,8),(size-7,8),(size-6,8),
                (size-5,8),(size-4,8),(size-3,8),(size-2,8),(size-1,8)]
        for i,(r,c) in enumerate(pos1):
            g[r][c] = bool((fmt_word >> (14-i)) & 1)
        for i,(r,c) in enumerate(pos2):
            g[r][c] = bool((fmt_word >> (14-i)) & 1)

    _BLOCKS_M = {
         1: [(1,16)],          2: [(1,28)],          3: [(1,44)],
         4: [(2,32)],          5: [(2,43)],           6: [(4,27)],
         7: [(4,31)],          8: [(2,38),(2,39)],    9: [(3,36),(2,37)],
        10: [(4,43),(1,44)],  11: [(1,50),(4,51)],   12: [(6,46),(2,47)],
        13: [(8,44),(1,45)],  14: [(4,48),(2,49)],   15: [(5,47),(1,48)],
        16: [(7,45),(3,46)],  17: [(10,46),(1,47)],  18: [(9,43),(4,44)],
        19: [(3,44),(11,45)], 20: [(3,41),(13,42)],  21: [(17,42)],
        22: [(17,46)],        23: [(4,47),(14,48)],  24: [(6,45),(14,46)],
        25: [(8,47),(13,48)], 26: [(19,46),(4,47)],  27: [(22,45),(3,46)],
        28: [(3,45),(23,46)], 29: [(21,45),(7,46)],  30: [(19,45),(10,46)],
        31: [(2,45),(29,46)], 32: [(10,45),(23,46)], 33: [(14,45),(21,46)],
        34: [(14,46),(23,47)],35: [(12,45),(26,46)], 36: [(6,45),(34,46)],
        37: [(29,45),(14,46)],38: [(13,45),(32,46)], 39: [(40,45),(7,46)],
        40: [(18,45),(31,46)],
    }

    @classmethod
    def _interleave(cls, ver: int, data: bytes, ec_per_block: int) -> List[int]:
        block_spec = cls._BLOCKS_M.get(ver, [(1, len(data))])
        blocks = []
        offset = 0
        for count, dcw in block_spec:
            for _ in range(count):
                chunk = data[offset:offset+dcw]
                ec    = cls._rs(chunk, ec_per_block)
                blocks.append((list(chunk), ec))
                offset += dcw
        result = []
        max_dc = max(len(b[0]) for b in blocks)
        for i in range(max_dc):
            for dc, _ in blocks:
                if i < len(dc):
                    result.append(dc[i])
        for i in range(ec_per_block):
            for _, ec in blocks:
                result.append(ec[i])
        return result

    @classmethod
    def encode(cls, text: str) -> List[List[bool]]:
        global _QR_LIB_INSTALL_ATTEMPTED
        try:
            import segno
            qr = segno.make(text, error='m')
            matrix = qr.matrix
            return [[bool(c) for c in row] for row in matrix]
        except ImportError:
            pass
        try:
            import qrcode
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(text); qr.make(fit=True)
            matrix = qr.get_matrix()
            return [[bool(c) for c in row] for row in matrix]
        except ImportError:
            pass

        if not _QR_LIB_INSTALL_ATTEMPTED:
            _QR_LIB_INSTALL_ATTEMPTED = True
            _try_install_qr_lib()
            try:
                import qrcode
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
                qr.add_data(text); qr.make(fit=True)
                matrix = qr.get_matrix()
                return [[bool(c) for c in row] for row in matrix]
            except Exception:
                pass

        CAP_M = [
            (0,0),(16,10),(28,16),(44,26),(64,18),(86,24),
            (108,16),(124,18),(154,22),(182,22),(216,26),
            (254,30),(290,22),(334,22),(365,26),(415,24),
            (453,28),(507,28),(563,26),(627,26),(669,28),
            (714,28),(782,28),(860,28),(914,28),(1000,28),
            (1062,28),(1128,28),(1193,28),(1267,28),(1373,28),
            (1455,28),(1541,28),(1631,28),(1725,28),(1812,28),
            (1914,28),(1992,28),(2102,28),(2216,28),(2334,28),
        ]
        data = text.encode("utf-8")
        ver  = next((v for v in range(1, 41) if len(data) <= CAP_M[v][0]), None)
        if ver is None:
            raise ValueError(f"Text too long ({len(data)} bytes) for QR v40")

        ec_per_block = CAP_M[ver][1]
        data_cw      = CAP_M[ver][0]
        len_bits = 8 if ver <= 9 else 16
        bits    = "0100" + format(len(data), f"0{len_bits}b")
        for b in data: bits += format(b,"08b")
        bits += "0000"
        while len(bits) % 8: bits += "0"
        pad = [0xEC, 0x11]; pi = 0
        while len(bits) < data_cw * 8:
            bits += format(pad[pi % 2], "08b"); pi += 1
        db      = bytes(int(bits[k:k+8], 2) for k in range(0, len(bits), 8))
        all_cw  = cls._interleave(ver, db, ec_per_block)

        size   = ver*4+17
        g      = [[False]*size for _ in range(size)]
        res    = [[False]*size for _ in range(size)]

        def setpx(r, c, v):
            if 0 <= r < size and 0 <= c < size:
                g[r][c] = v; res[r][c] = True

        def rect(r, c, h, w, v):
            for dr in range(h):
                for dc in range(w): setpx(r+dr, c+dc, v)

        def finder(r, c):
            rect(r,c,7,7,True); rect(r+1,c+1,5,5,False); rect(r+2,c+2,3,3,True)

        finder(0,0); finder(0,size-7); finder(size-7,0)
        rect(7,0,1,8,False); rect(0,7,8,1,False)
        rect(7,size-8,1,8,False); rect(0,size-8,8,1,False)
        rect(size-8,0,1,8,False); rect(size-7,7,7,1,False)
        for i in range(8, size-8):
            g[6][i] = res[6][i] = (i % 2 == 0)
            g[i][6] = res[i][6] = (i % 2 == 0)
        setpx(size-8, 8, True)
        for i in range(9): res[8][i] = True
        for i in range(9): res[i][8] = True
        for i in range(size-8, size): res[8][i] = True
        for i in range(size-8, size): res[i][8] = True
        if ver >= 2:
            AP = {2:[6,18],3:[6,22],4:[6,26],5:[6,30],6:[6,34],
                  7:[6,22,38],8:[6,24,42],9:[6,26,46],10:[6,28,50]}
            pts = AP.get(ver, [])
            for ar in pts:
                for ac in pts:
                    if not res[ar][ac]:
                        rect(ar-2,ac-2,5,5,True); rect(ar-1,ac-1,3,3,False)
                        setpx(ar,ac,True)
        cls._write_format(g, size, mask=0)

        all_bits = "".join(format(cw, "08b") for cw in all_cw)
        bi = 0; col = size-1; up = True
        MASK = 0
        while col > 0:
            if col == 6: col -= 1
            rows = range(size-1, -1, -1) if up else range(size)
            for row in rows:
                for dc in range(2):
                    c = col - dc
                    if 0 <= c < size and not res[row][c]:
                        bit = (all_bits[bi] == "1") if bi < len(all_bits) else False
                        if (row + c) % 2 == 0: bit = not bit
                        g[row][c] = bit; bi += 1
            up = not up; col -= 2
        cls._write_format(g, size, mask=MASK)
        return g


def show_qr(parent, url: str, title: str = "QR Code"):
    try: grid = _QR.encode(url)
    except Exception as e:
        messagebox.showerror("QR", f"Cannot encode: {e}", parent=parent); return
    size  = len(grid)
    CELL  = max(4, min(9, 360//size))
    Q     = 4
    sz    = (size+Q*2)*CELL
    top   = tk.Toplevel(parent)
    top.title(title); top.resizable(False,False); top.configure(bg=CARD)
    cv = tk.Canvas(top, width=sz, height=sz, bg="white", highlightthickness=0)
    cv.pack(padx=10, pady=10)
    off = Q*CELL
    for r,row in enumerate(grid):
        for c,dark in enumerate(row):
            if dark:
                x0=off+c*CELL; y0=off+r*CELL
                cv.create_rectangle(x0,y0,x0+CELL,y0+CELL,fill="black",outline="")
    tk.Label(top, text=url[:64]+("…" if len(url)>64 else ""),
             font=FS, bg=CARD, fg=FG2, wraplength=sz).pack(padx=10,pady=(0,4))
    tk.Button(top, text="Copy URL", font=("Segoe UI", 10),
              bg="#00b4ab", fg="white",
              relief="flat", cursor="hand2", padx=12, pady=4,
              command=lambda: [parent.clipboard_clear(),
                               parent.clipboard_append(url)]).pack(side=tk.LEFT,padx=10,pady=(0,10))
    tk.Button(top, text="Close", font=("Segoe UI", 10),
              bg="#FA7567", fg="white",
              relief="flat", cursor="hand2", padx=12, pady=4,
              command=top.destroy).pack(side=tk.LEFT, pady=(0,10))


# ============================================================
#  Module: bpb_deploy
# ============================================================


import base64 as _b64
import json as _j
import re as _re3
import secrets as _sec
import urllib.error
import urllib.parse
import urllib.request
import uuid as _uuid_mod


_BPB_W = (
    'Ly8gQnVpbGQ6IDIwMjYtMDYtMDhUMDM6MTY6MjAuNzg2WgovLyBAdHMtbm9j'
    'aGVjawpsZXQgZT03MTMxMyx0PTI4NTQ1LHI9ODY0OTYsbj05MjYxNSxpPTQz'
    'ODYscz0xMzU5OSxvPTQ2MjEwLGE9MzQ3OTMsYz00NTAzMSx1PTkwODk4LGw9'
    'NTk4MzEsZD05MjA3Myx3PTI3NzI5LGg9ODMzNSxmPTk0NTc1LEE9Nzk3Myxw'
    'PTEyMzczLEU9NTQyNjgsQj0yMTM1MSxIPTM2MTA1LG09NTM2ODksZz0yMzAx'
    'LHk9NjMwNDQsVD03NjExNyx4PTg5MTU0LHY9MzU1NjksYj0zNDgxMSxSPTc2'
    'NTQzLE09Nzk1Mzgsaz00OTE1NSxTPTcxMjIxLEM9Njg3NixfPTg4OTQsTz03'
    'ODIyNyxQPTIwMjY2LEw9NTIyODksST02NjQ3MCxEPTg0MjM2LFU9ODg2ODMs'
    'Tj0zMjI0Nyx6PTUyOTg1LFg9Njk5NDIsRj01NzUwNCxqPTgxMTczLFc9ODQ5'
    'ODcsSj02ODQzLEs9Nzg2MixWPTg4NjQyLFk9ODAxNDAsWj00Njc3OSxHPTM4'
    'OSxRPTI5MjYwLHE9Mzg0MzAsJD0zNTg4NyxlZT0zNDQ2Nix0ZT01NzA4Myxy'
    'ZT00MjAyNSxuZT04Mjk4OCxpZT04MTQwMSxzZT0yMDA0NyxvZT01Mjc4NSxh'
    'ZT03MzI4OSxjZT0zNzY1MSx1ZT02ODExNCxsZT0xMzMzMixkZT02OTg1Mix3'
    'ZT02MzgwMixoZT05NDcxNSxmZT04NzA4NSxBZT02NTgyNyxwZT00OTkxNyxF'
    'ZT03NzQ2NixCZT04MDUzNyxIZT03NjA4MixtZT0zMzMzMixnZT0yMjY2LHll'
    'PTUwNzcxLFRlPTI3NDkxLHhlPTM3MTM3LHZlPTYwNTg0LGJlPTkwMjM4LFJl'
    'PTE4MzMyLE1lPTU0MDg5LGtlPTg0NjY2LFNlPTcxMTM3LENlPTIwMTQ0LF9l'
    'PTQ0NDQ1LE9lPTkzOTI0LFBlPTQ3NTE1LExlPTQzMDkxLEllPTI4MjksRGU9'
    'MTA0ODksVWU9MzQ4MTAsTmU9ODkxMzIsemU9NDg3NDksWGU9ODU0MDMsRmU9'
    'NjcyNDIsamU9MTg5MjgsV2U9MTM3NzIsSmU9NzcwMjIsS2U9NDEzMjIsVmU9'
    'OTAyNzUsWWU9MzI3ODMsWmU9MjQ3NjksR2U9MTI2NDEsUWU9NDg0MTEscWU9'
    'MjA1NTAsJGU9MjM2NDEsZXQ9Mzg0MjMsdHQ9OTUyNzgscnQ9ODUxMDEsbnQ9'
    'OTY3OTMsaXQ9MzA5MTMsc3Q9NDExOTEsb3Q9NzQyOTMsYXQ9NDQ0NzQsY3Q9'
    'NDk3NTksdXQ9OTkyMzksbHQ9NjUzNTMsZHQ9ODAxOTIsd3Q9NDUxODksaHQ9'
    'NDE1NTgsZnQ9OTQzNDQsQXQ9MzQyOSxwdD03ODIxMixFdD00MDAwNyxCdD01'
    'MTczNSxIdD03MTEzNCxtdD05OTQ5LGd0PTI5NDM0LHl0PTc4MDgsVHQ9MzEy'
    'NjQseHQ9NzU2NzQsdnQ9NDY5NDAsYnQ9NjE5NSxSdD01NDM2MSxNdD02ODU2'
    'OCxrdD00OTk2LFN0PTcxNzY0LEN0PTc4MjQ0LF90PTk2NzcwLE90PTQ1NzEw'
    'LFB0PTQxMDg5LEx0PTM2NjQzLEl0PTgyNTUyLER0PTkyNjcwLFV0PTQxODcy'
    'LE50PTYzNDE1LHp0PTQ5MTcyLFh0PTUwMDE2LEZ0PTc5ODg5LGp0PTUxMjQ2'
    'LFd0PTMyNTIzLEp0PTYwMzg4LEt0PTcwMTU0LFZ0PTEzNTIxLFl0PTczMzYz'
    'LFp0PTc5NDI5LEd0PTczODIsUXQ9NTY0ODkscXQ9MTM0MjUsJHQ9NDYxMDIs'
    'ZXI9MjA5NCx0cj00NTk5Nyxycj04NDk2MCxucj0yNzI2Myxpcj0xNzk0Mixz'
    'cj03NTU5LG9yPTQ2NDE4LGFyPTYwNjEwLGNyPTcyNzQ5LHVyPTE3MDgzLGxy'
    'PTYxNjAsZHI9OTU4NTYsd3I9MzM0MzUsaHI9MTk2OTIsZnI9NTU3NzAsQXI9'
    'NjMxMzEscHI9OTA2NDUsRXI9NzA5ODUsQnI9Njg5NjksSHI9MTQxNTEsbXI9'
    'NDI3NDMsZ3I9Nzk2MDQseXI9NDY1OCxUcj0zNDA0OCx4cj03NzcxNix2cj0z'
    'NzUxMCxicj0xMjMyOCxScj02NzU4MyxNcj02MDQ5Nixrcj00NDY0LFNyPTQz'
    'MTE0LENyPTMyNjQsX3I9NzYwMjMsT3I9NzM5NzIsUHI9Nzg0MjAsTHI9MzE3'
    'OTAsSXI9NTIxODcsRHI9MjM4NjYsVXI9MzUwMjIsTnI9MjEyMTAsenI9NDM1'
    'MixYcj02NTY5MSxGcj05MTE4OCxqcj00MDg5OSxXcj04NTAwMixKcj03NTI2'
    'OCxLcj04Mjk5NCxWcj05OTc4LFlyPTQ0MDMxLFpyPTIzMzE3LEdyPTQ4MDkw'
    'LFFyPTI0ODgwLHFyPTEwNTcxLCRyPTQ0NDg0LGVuPTY4MDMsdG49NTY2MjYs'
    'cm49ODE2Nyxubj01MDI3MCxzbj05ODE0MSxvbj01NTEyMyxhbj0yNzI4Nixj'
    'bj04MTk1OSx1bj01Nzc1Nyxsbj00MzE2OSxkbj0xNTEyNSx3bj04OTM5Mixo'
    'bj03NDg2NSxmbj02NTk5MCxBbj01MDk5MCxwbj05MDkyLEVuPTg4ODIyLEJu'
    'PTE3NzgzLEhuPTU2OTk3LG1uPTI0MTA5LGduPTc2MDg4LHluPTUxMjA2LFRu'
    'PTg0ODA3LHhuPTcwNjM1LHZuPTY4MzYzLGJuPTI5Mzk4LFJuPTM3ODUwLE1u'
    'PTM0NzQ4LGtuPTE5MTQxLFNuPTcwNzUxLENuPTczNzk5LF9uPTQ2ZTMsT249'
    'ODM1MTUsUG49OTc3ODQsTG49OTU2ODAsSW49MTQwNDcsRG49Njc1MTMsVW49'
    'MzgzMjYsTm49NjIxOTYsem49ODM2MDgsWG49NDY0NjMsRm49NDMyMSxqbj05'
    'OTU3NSxXbj0xNDA2NyxKbj00MDIyNCxLbj0yODQzNixWbj03MTAxNixZbj03'
    'NTAyNyxabj05OTg4MixHbj0yNTk0OSxRbj0zNDk1MSxxbj0xMTcyOCwkbj0y'
    'NzgyNyxlaT00MDgxMyx0aT02OTc2MyxyaT02OTk4OCxuaT0xNjE4OSxpaT0z'
    'MTM3NixzaT0xMzYzMCxvaT02MjcyNCxhaT00OTQ3NixjaT0zNzUxMix1aT00'
    'NjAzNCxsaT0yODk5NyxkaT0yOTI2Mix3aT03NjQ1OCxoaT03OTgzMyxmaT00'
    'NDI0NSxBaT01ODc0OSxwaT02NTA1NCxFaT05MjMzNSxCaT02ODc3NSxIaT03'
    'NjM5MCxtaT00Njc0MyxnaT00MDE4MSx5aT01MDE1NixUaT02OTYwLHhpPTQ1'
    'ZTMsdmk9MjcyNzMsYmk9MTE2NDYsUmk9Nzg4OTMsTWk9MjE2MDQsa2k9NDQw'
    'MTYsU2k9ODMyMjAsQ2k9OTQyNTAsX2k9NTUxNTksT2k9NjI1NzEsUGk9Njkz'
    'MTAsTGk9MjQ4MzAsSWk9MjU4OTMsRGk9NTY3ODksVWk9NDU3MixOaT04MDg5'
    'Nyx6aT0yMTMzOSxYaT05MDg4MixGaT04ODMxOSxqaT0xMjIxLFdpPTM2MDU5'
    'LEppPTYzMzI2LEtpPTEyNjIwLFZpPTYzNjk2LFlpPTE1OTY4LFppPTY1MjEw'
    'LEdpPTgzMTMwLFFpPTI3MSxxaT03ODM0MCwkaT02MTI2Myxlcz0zNTYwNix0'
    'cz00MTU4OSxycz03MjkzMCxucz00MzI1NCxpcz0zMzc2NztmdW5jdGlvbiBz'
    'cygpe3JldHVybiAyNzd9ZnVuY3Rpb24gb3MoKXtyZXR1cm4gNzg2fWZ1bmN0'
    'aW9uIGFzKCl7cmV0dXJuIDR9ZnVuY3Rpb24gY3MoKXtyZXR1cm4gNDM5fWZ1'
    'bmN0aW9uIHVzKCl7cmV0dXJuIDM3MX1mdW5jdGlvbiBscygpe3JldHVybiA4'
    'MH1mdW5jdGlvbiBkcygpe3JldHVybiA5NTd9ZnVuY3Rpb24gd3MoKXtyZXR1'
    'cm4gNjA2fWZ1bmN0aW9uIGhzKCl7cmV0dXJuIDkxOX1mdW5jdGlvbiBmcygp'
    'e3JldHVybiA1MTB9ZnVuY3Rpb24gQXMoKXtyZXR1cm4gMTgyfWZ1bmN0aW9u'
    'IHBzKCl7cmV0dXJuIDc0N31mdW5jdGlvbiBFcygpe3JldHVybiAyMDF9ZnVu'
    'Y3Rpb24gQnMoKXtyZXR1cm4gMjExfWZ1bmN0aW9uIEhzKCl7cmV0dXJuIDQ0'
    'Mn1mdW5jdGlvbiBtcygpe3JldHVybiAyMn1mdW5jdGlvbiBncygpe3JldHVy'
    'biAxNzF9ZnVuY3Rpb24geXMoKXtyZXR1cm4gMzkzfWZ1bmN0aW9uIFRzKCl7'
    'cmV0dXJuIDc4MX1mdW5jdGlvbiB4cygpe3JldHVybiA0ODF9ZnVuY3Rpb24g'
    'dnMoKXtyZXR1cm4gNzU0fWZ1bmN0aW9uIGJzKCl7cmV0dXJuIDE0MX1mdW5j'
    'dGlvbiBScygpe3JldHVybiA2NTl9ZnVuY3Rpb24gTXMoKXtyZXR1cm4gNDg0'
    'fWZ1bmN0aW9uIGtzKCl7cmV0dXJuIDIzN31mdW5jdGlvbiBTcygpe3JldHVy'
    'biA0NDl9ZnVuY3Rpb24gQ3MoKXtyZXR1cm4gNzAzfWZ1bmN0aW9uIF9zKCl7'
    'cmV0dXJuIDExMH1mdW5jdGlvbiBPcygpe3JldHVybiA0NTB9ZnVuY3Rpb24g'
    'UHMoKXtyZXR1cm4gMzYyfWZ1bmN0aW9uIExzKCl7cmV0dXJuIDg1M31mdW5j'
    'dGlvbiBJcygpe3JldHVybiA5OTZ9ZnVuY3Rpb24gRHMoKXtyZXR1cm4gNDI5'
    'fWZ1bmN0aW9uIFVzKCl7cmV0dXJuIDIxN31mdW5jdGlvbiBOcygpe3JldHVy'
    'biA2NjV9ZnVuY3Rpb24genMoKXtyZXR1cm4gOTkxfWZ1bmN0aW9uIFhzKCl7'
    'cmV0dXJuIDQ5OH1mdW5jdGlvbiBGcygpe3JldHVybiA1OTV9ZnVuY3Rpb24g'
    'anMoKXtyZXR1cm4gNDk5fWZ1bmN0aW9uIFdzKCl7cmV0dXJuIDcyMn1mdW5j'
    'dGlvbiBKcygpe3JldHVybiA0NjB9ZnVuY3Rpb24gS3MoKXtyZXR1cm4gNTg2'
    'fWZ1bmN0aW9uIFZzKCl7cmV0dXJuIDE2Nn1mdW5jdGlvbiBZcygpe3JldHVy'
    'biA0NTJ9ZnVuY3Rpb24gWnMoKXtyZXR1cm4gOTEyfWZ1bmN0aW9uIEdzKCl7'
    'cmV0dXJuIDQyOH1mdW5jdGlvbiBRcygpe3JldHVybiA1MTl9ZnVuY3Rpb24g'
    'cXMoKXtyZXR1cm4gOTEwfWZ1bmN0aW9uICRzKCl7cmV0dXJuIDk5Nn1mdW5j'
    'dGlvbiBlbygpe3JldHVybiA2OTV9ZnVuY3Rpb24gdG8oKXtyZXR1cm4gNDI1'
    'fWZ1bmN0aW9uIHJvKCl7cmV0dXJuIDc4fWZ1bmN0aW9uIG5vKCl7cmV0dXJu'
    'IDM1fWZ1bmN0aW9uIGlvKCl7cmV0dXJuIDcxMn1mdW5jdGlvbiBzbygpe3Jl'
    'dHVybiAyOTh9ZnVuY3Rpb24gb28oKXtyZXR1cm4gMTA0fWZ1bmN0aW9uIGFv'
    'KCl7cmV0dXJuIDI1OH1mdW5jdGlvbiBjbygpe3JldHVybiAyNDF9ZnVuY3Rp'
    'b24gdW8oKXtyZXR1cm4gNjI2fWZ1bmN0aW9uIGxvKCl7cmV0dXJuIDE1NX1m'
    'dW5jdGlvbiB3bygpe3JldHVybiA5NzF9ZnVuY3Rpb24gaG8oKXtyZXR1cm4g'
    'MjM4fWZ1bmN0aW9uIGZvKCl7cmV0dXJuIDczNn1mdW5jdGlvbiBBbygpe3Jl'
    'dHVybiAxMjh9ZnVuY3Rpb24gcG8oKXtyZXR1cm4gMzUxfWZ1bmN0aW9uIEVv'
    'KCl7cmV0dXJuIDk3Nn1mdW5jdGlvbiBCbygpe3JldHVybiA1Nzh9ZnVuY3Rp'
    'b24gSG8oKXtyZXR1cm4gMjA5fWZ1bmN0aW9uIG1vKCl7cmV0dXJuIDkxNX1m'
    'dW5jdGlvbiBnbygpe3JldHVybiA0OTd9ZnVuY3Rpb24geW8oKXtyZXR1cm4g'
    'OTAzfWZ1bmN0aW9uIFRvKCl7cmV0dXJuIDEwOX1mdW5jdGlvbiB4bygpe3Jl'
    'dHVybiA0OTJ9ZnVuY3Rpb24gdm8oKXtyZXR1cm4gNzc0fWZ1bmN0aW9uIGJv'
    'KCl7cmV0dXJuIDI4Nn1mdW5jdGlvbiBSbygpe3JldHVybiA5Njh9ZnVuY3Rp'
    'b24gTW8oKXtyZXR1cm4gMjR9ZnVuY3Rpb24ga28oKXtyZXR1cm4gNTMyfWZ1'
    'bmN0aW9uIFNvKCl7cmV0dXJuIDczNX1mdW5jdGlvbiBDbygpe3JldHVybiA5'
    'NjV9ZnVuY3Rpb24gX28oKXtyZXR1cm4gODE1fWZ1bmN0aW9uIE9vKCl7cmV0'
    'dXJuIDEyN31mdW5jdGlvbiBQbygpe3JldHVybiA4MX1mdW5jdGlvbiBMbygp'
    'e3JldHVybiAzNjF9ZnVuY3Rpb24gSW8oKXtyZXR1cm4gMTQ1fWZ1bmN0aW9u'
    'IERvKCl7cmV0dXJuIDMzMn1mdW5jdGlvbiBVbygpe3JldHVybiA5ODB9ZnVu'
    'Y3Rpb24gTm8oKXtyZXR1cm4gMTJ9ZnVuY3Rpb24gem8oKXtyZXR1cm4gMzAx'
    'fWZ1bmN0aW9uIFhvKCl7cmV0dXJuIDYxOX1mdW5jdGlvbiBGbygpe3JldHVy'
    'biA4NDh9ZnVuY3Rpb24gam8oKXtyZXR1cm4gNjk0fWZ1bmN0aW9uIFdvKCl7'
    'cmV0dXJuIDMwNn1mdW5jdGlvbiBKbygpe3JldHVybiAzMH1mdW5jdGlvbiBL'
    'bygpe3JldHVybiA0Mzl9ZnVuY3Rpb24gVm8oKXtyZXR1cm4gMzA2fWZ1bmN0'
    'aW9uIFlvKCl7cmV0dXJuIDcxMX1mdW5jdGlvbiBabygpe3JldHVybiAxNTJ9'
    'ZnVuY3Rpb24gR28oKXtyZXR1cm4gNjAzfWZ1bmN0aW9uIFFvKCl7cmV0dXJu'
    'IDg5OX1mdW5jdGlvbiBxbygpe3JldHVybiA1ODR9ZnVuY3Rpb24gJG8oKXty'
    'ZXR1cm4gNzY4fWZ1bmN0aW9uIGVhKCl7cmV0dXJuIDgwNX1mdW5jdGlvbiB0'
    'YSgpe3JldHVybiAzNDh9ZnVuY3Rpb24gcmEoKXtyZXR1cm4gNTE4fWZ1bmN0'
    'aW9uIG5hKCl7cmV0dXJuIDk3Nn1mdW5jdGlvbiBpYSgpe3JldHVybiA2MDB9'
    'ZnVuY3Rpb24gc2EoKXtyZXR1cm4gNDA5fWZ1bmN0aW9uIG9hKCl7cmV0dXJu'
    'IDQwOX1mdW5jdGlvbiBhYSgpe3JldHVybiAyOTV9ZnVuY3Rpb24gY2EoKXty'
    'ZXR1cm4gOTY5fWZ1bmN0aW9uIHVhKCl7cmV0dXJuIDYwNH1mdW5jdGlvbiBs'
    'YSgpe3JldHVybiA4NjB9ZnVuY3Rpb24gZGEoKXtyZXR1cm4gNTUxfWZ1bmN0'
    'aW9uIHdhKCl7cmV0dXJuIDUyNH1mdW5jdGlvbiBoYSgpe3JldHVybiA1MDZ9'
    'ZnVuY3Rpb24gZmEoKXtyZXR1cm4gNDg3fWZ1bmN0aW9uIEFhKCl7cmV0dXJu'
    'IDkxNH1mdW5jdGlvbiBwYSgpe3JldHVybiAxMzF9ZnVuY3Rpb24gRWEoKXty'
    'ZXR1cm4gNjF9ZnVuY3Rpb24gQmEoKXtyZXR1cm4gOTQ0fWZ1bmN0aW9uIEhh'
    'KCl7cmV0dXJuIDg2N31mdW5jdGlvbiBtYSgpe3JldHVybiA0MX1mdW5jdGlv'
    'biBnYSgpe3JldHVybiA2NDF9ZnVuY3Rpb24geWEoKXtyZXR1cm4gMjgwfWZ1'
    'bmN0aW9uIFRhKCl7cmV0dXJuIDkzM31mdW5jdGlvbiB4YSgpe3JldHVybiAy'
    'NDJ9ZnVuY3Rpb24gdmEoKXtyZXR1cm4gMzk3fWZ1bmN0aW9uIGJhKCl7cmV0'
    'dXJuIDc1M31mdW5jdGlvbiBSYSgpe3JldHVybiA5NzF9ZnVuY3Rpb24gTWEo'
    'KXtyZXR1cm4gNTk1fWZ1bmN0aW9uIGthKCl7cmV0dXJuIDk4M31mdW5jdGlv'
    'biBTYSgpe3JldHVybiAzNjN9ZnVuY3Rpb24gQ2EoKXtyZXR1cm4gOTI5fWZ1'
    'bmN0aW9uIF9hKCl7cmV0dXJuIDIxN31mdW5jdGlvbiBPYSgpe3JldHVybiA1'
    'MDR9ZnVuY3Rpb24gUGEoKXtyZXR1cm4gOTc2fWZ1bmN0aW9uIExhKCl7cmV0'
    'dXJuIDUyN31mdW5jdGlvbiBJYSgpe3JldHVybiA2NDN9ZnVuY3Rpb24gRGEo'
    'KXtyZXR1cm4gNjA0fWZ1bmN0aW9uIFVhKCl7cmV0dXJuIDMyMH1mdW5jdGlv'
    'biBOYSgpe3JldHVybiAxNzJ9ZnVuY3Rpb24gemEoKXtyZXR1cm4gNTc5fWZ1'
    'bmN0aW9uIFhhKCl7cmV0dXJuIDE5fWZ1bmN0aW9uIEZhKCl7cmV0dXJuIDQ5'
    'N31mdW5jdGlvbiBqYSgpe3JldHVybiAzMzF9ZnVuY3Rpb24gV2EoKXtyZXR1'
    'cm4gODI0fWZ1bmN0aW9uIEphKCl7cmV0dXJuIDIxfWZ1bmN0aW9uIEthKCl7'
    'cmV0dXJuIDU4NX1mdW5jdGlvbiBWYSgpe3JldHVybiA5Mn1mdW5jdGlvbiBZ'
    'YSgpe3JldHVybiAzNDd9ZnVuY3Rpb24gWmEoKXtyZXR1cm4gMTg0fWZ1bmN0'
    'aW9uIEdhKCl7cmV0dXJuIDY5Nn1mdW5jdGlvbiBRYSgpe3JldHVybiA0MjF9'
    'ZnVuY3Rpb24gcWEoKXtyZXR1cm4gNzg5fWZ1bmN0aW9uICRhKCl7cmV0dXJu'
    'IDg4N31mdW5jdGlvbiBlYygpe3JldHVybiA5MDF9ZnVuY3Rpb24gdGMoKXty'
    'ZXR1cm4gNzEyfWZ1bmN0aW9uIHJjKCl7cmV0dXJuIDY3OX1mdW5jdGlvbiBu'
    'Yygpe3JldHVybiA3MTN9ZnVuY3Rpb24gaWMoKXtyZXR1cm4gNDQzfWZ1bmN0'
    'aW9uIHNjKCl7cmV0dXJuIDgwOX1mdW5jdGlvbiBvYygpe3JldHVybiAxMDl9'
    'ZnVuY3Rpb24gYWMoKXtyZXR1cm4gMjcxfWZ1bmN0aW9uIGNjKCl7cmV0dXJu'
    'IDkyfWZ1bmN0aW9uIHVjKCl7cmV0dXJuIDIxMn1mdW5jdGlvbiBsYygpe3Jl'
    'dHVybiAxODd9ZnVuY3Rpb24gZGMoKXtyZXR1cm4gNzY4fWZ1bmN0aW9uIHdj'
    'KCl7cmV0dXJuIDQyN31mdW5jdGlvbiBoYygpe3JldHVybiA4NjV9ZnVuY3Rp'
    'b24gZmMoKXtyZXR1cm4gNTg4fWZ1bmN0aW9uIEFjKCl7cmV0dXJuIDQ3MH1m'
    'dW5jdGlvbiBwYygpe3JldHVybiA2NjB9ZnVuY3Rpb24gRWMoKXtyZXR1cm4g'
    'MTE3fWZ1bmN0aW9uIEJjKCl7cmV0dXJuIDg3OH1mdW5jdGlvbiBIYygpe3Jl'
    'dHVybiAzNzl9ZnVuY3Rpb24gbWMoKXtyZXR1cm4gNjE2fWZ1bmN0aW9uIGdj'
    'KCl7cmV0dXJuIDQ4M31mdW5jdGlvbiB5Yygpe3JldHVybiA4ODF9ZnVuY3Rp'
    'b24gVGMoKXtyZXR1cm4gNjUyfWZ1bmN0aW9uIHhjKCl7cmV0dXJuIDcyMn1m'
    'dW5jdGlvbiB2Yygpe3JldHVybiA3MTh9ZnVuY3Rpb24gYmMoKXtyZXR1cm4g'
    'Mzc1fWZ1bmN0aW9uIFJjKCl7cmV0dXJuIDQyNH1mdW5jdGlvbiBNYygpe3Jl'
    'dHVybiA5MDN9ZnVuY3Rpb24ga2MoKXtyZXR1cm4gNzczfWZ1bmN0aW9uIFNj'
    'KCl7cmV0dXJuIDE0NX1mdW5jdGlvbiBDYygpe3JldHVybiA0MzN9ZnVuY3Rp'
    'b24gX2MoKXtyZXR1cm4gNjI5fWZ1bmN0aW9uIE9jKCl7cmV0dXJuIDk1OX1m'
    'dW5jdGlvbiBQYygpe3JldHVybiA4fWZ1bmN0aW9uIExjKCl7cmV0dXJuIDIy'
    'Nn1mdW5jdGlvbiBJYygpe3JldHVybiA3NzR9ZnVuY3Rpb24gRGMoKXtyZXR1'
    'cm4gNTM3fWZ1bmN0aW9uIFVjKCl7cmV0dXJuIDgxOH1mdW5jdGlvbiBOYygp'
    'e3JldHVybiA1MjZ9ZnVuY3Rpb24gemMoKXtyZXR1cm4gMzk1fWZ1bmN0aW9u'
    'IFhjKCl7cmV0dXJuIDg4fWZ1bmN0aW9uIEZjKCl7cmV0dXJuIDQ5N31mdW5j'
    'dGlvbiBqYygpe3JldHVybiA1NzN9ZnVuY3Rpb24gV2MoKXtyZXR1cm4gNTE1'
    'fWZ1bmN0aW9uIEpjKCl7cmV0dXJuIDUxMX1mdW5jdGlvbiBLYygpe3JldHVy'
    'biA3Mjh9ZnVuY3Rpb24gVmMoKXtyZXR1cm4gNjgyfWZ1bmN0aW9uIFljKCl7'
    'cmV0dXJuIDE3Mn1mdW5jdGlvbiBaYygpe3JldHVybiA1M31mdW5jdGlvbiBH'
    'Yygpe3JldHVybiA4NzR9ZnVuY3Rpb24gUWMoKXtyZXR1cm4gOTQxfWZ1bmN0'
    'aW9uIHFjKCl7cmV0dXJuIDYwOH1mdW5jdGlvbiAkYygpe3JldHVybiA3NTV9'
    'ZnVuY3Rpb24gZXUoKXtyZXR1cm4gODU4fWZ1bmN0aW9uIHR1KCl7cmV0dXJu'
    'IDE0MX1mdW5jdGlvbiBydSgpe3JldHVybiA2NzN9ZnVuY3Rpb24gbnUoKXty'
    'ZXR1cm4gMjAwfWZ1bmN0aW9uIGl1KCl7cmV0dXJuIDQ0MH1mdW5jdGlvbiBz'
    'dSgpe3JldHVybiAzNzR9ZnVuY3Rpb24gb3UoKXtyZXR1cm4gNTkxfWZ1bmN0'
    'aW9uIGF1KCl7cmV0dXJuIDEwN31mdW5jdGlvbiBjdSgpe3JldHVybiAyODR9'
    'ZnVuY3Rpb24gdXUoKXtyZXR1cm4gOTY1fWZ1bmN0aW9uIGx1KCl7cmV0dXJu'
    'IDk1MH1mdW5jdGlvbiBkdSgpe3JldHVybiA5MDh9ZnVuY3Rpb24gd3UoKXty'
    'ZXR1cm4gNDQyfWZ1bmN0aW9uIGh1KCl7cmV0dXJuIDgxOH1mdW5jdGlvbiBm'
    'dSgpe3JldHVybiAxMzB9ZnVuY3Rpb24gQXUoKXtyZXR1cm4gMjQ1fWZ1bmN0'
    'aW9uIHB1KCl7cmV0dXJuIDc5MH1mdW5jdGlvbiBFdSgpe3JldHVybiA1NjB9'
    'ZnVuY3Rpb24gQnUoKXtyZXR1cm4gNjgyfWZ1bmN0aW9uIEh1KCl7cmV0dXJu'
    'IDQxN31mdW5jdGlvbiBtdSgpe3JldHVybiA4NTh9ZnVuY3Rpb24gZ3UoKXty'
    'ZXR1cm4gOTUyfWZ1bmN0aW9uIHl1KCl7cmV0dXJuIDgzNH1mdW5jdGlvbiBU'
    'dSgpe3JldHVybiA1MTN9ZnVuY3Rpb24geHUoKXtyZXR1cm4gMzU5fWZ1bmN0'
    'aW9uIHZ1KCl7cmV0dXJuIDIwOX1mdW5jdGlvbiBidSgpe3JldHVybiAxNDd9'
    'ZnVuY3Rpb24gUnUoKXtyZXR1cm4gOTQzfWZ1bmN0aW9uIE11KCl7cmV0dXJu'
    'IDc3NX1mdW5jdGlvbiBrdSgpe3JldHVybiAyNjJ9ZnVuY3Rpb24gU3UoKXty'
    'ZXR1cm4gODd9ZnVuY3Rpb24gQ3UoKXtyZXR1cm4gMTd9ZnVuY3Rpb24gX3Uo'
    'KXtyZXR1cm4gNjk5fWZ1bmN0aW9uIE91KCl7cmV0dXJuIDg4fWZ1bmN0aW9u'
    'IFB1KCl7cmV0dXJuIDQ4NX1mdW5jdGlvbiBMdSgpe3JldHVybiA2M31mdW5j'
    'dGlvbiBJdSgpe3JldHVybiAxMjF9ZnVuY3Rpb24gRHUoKXtyZXR1cm4gNDgx'
    'fWZ1bmN0aW9uIFV1KCl7cmV0dXJuIDc1fWZ1bmN0aW9uIE51KCl7cmV0dXJu'
    'IDg1MH1mdW5jdGlvbiB6dSgpe3JldHVybiA0ODF9ZnVuY3Rpb24gWHUoKXty'
    'ZXR1cm4gNjIzfWZ1bmN0aW9uIEZ1KCl7cmV0dXJuIDIxN31mdW5jdGlvbiBq'
    'dSgpe3JldHVybiA3NjV9ZnVuY3Rpb24gV3UoKXtyZXR1cm4gNTE0fWZ1bmN0'
    'aW9uIEp1KCl7cmV0dXJuIDU5OX1mdW5jdGlvbiBLdSgpe3JldHVybiAyNjF9'
    'ZnVuY3Rpb24gVnUoKXtyZXR1cm4gNjA5fWZ1bmN0aW9uIFl1KCl7cmV0dXJu'
    'IDY0MX1mdW5jdGlvbiBadSgpe3JldHVybiA4MDB9ZnVuY3Rpb24gR3UoKXty'
    'ZXR1cm4gNTE5fWZ1bmN0aW9uIFF1KCl7cmV0dXJuIDk1Nn1mdW5jdGlvbiBx'
    'dSgpe3JldHVybiA2MjZ9ZnVuY3Rpb24gJHUoKXtyZXR1cm4gMzQyfXZhciBl'
    'bD1PYmplY3QuY3JlYXRlLHRsPU9iamVjdC5kZWZpbmVQcm9wZXJ0eSxybD1P'
    'YmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9yLG5sPU9iamVjdC5nZXRP'
    'd25Qcm9wZXJ0eU5hbWVzLGlsPU9iamVjdC5nZXRQcm90b3R5cGVPZixzbD1P'
    'YmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LG9sPShlPT4idW5kZWZp'
    'bmVkIiE9dHlwZW9mIHJlcXVpcmU/cmVxdWlyZToidW5kZWZpbmVkIiE9dHlw'
    'ZW9mIFByb3h5P25ldyBQcm94eShlLHtnZXQ6KGUsdCk9PigidW5kZWZpbmVk'
    'IiE9dHlwZW9mIHJlcXVpcmU/cmVxdWlyZTplKVt0XX0pOmUpKGZ1bmN0aW9u'
    'KGUpe2lmKCJ1bmRlZmluZWQiIT10eXBlb2YgcmVxdWlyZSlyZXR1cm4gcmVx'
    'dWlyZS5hcHBseSh0aGlzLGFyZ3VtZW50cyk7dGhyb3cgRXJyb3IoJ0R5bmFt'
    'aWMgcmVxdWlyZSBvZiAiJytlKyciIGlzIG5vdCBzdXBwb3J0ZWQnKX0pLGFs'
    'LGNsPShlLHQscixuKT0+e2lmKHQmJiJvYmplY3QiPT10eXBlb2YgdHx8ImZ1'
    'bmN0aW9uIj09dHlwZW9mIHQpZm9yKGxldCBpIG9mIG5sKHQpKXNsLmNhbGwo'
    'ZSxpKXx8aT09PXJ8fHRsKGUsaSx7Z2V0OigpPT50W2ldLGVudW1lcmFibGU6'
    'IShuPXJsKHQsaSkpfHxuLmVudW1lcmFibGV9KTtyZXR1cm4gZX0sdWw9KGUs'
    'dCxyKT0+KHI9bnVsbCE9ZT9lbChpbChlKSk6e30sY2woIXQmJmUmJmUuX19l'
    'c01vZHVsZT9yOnRsKHIsImRlZmF1bHQiLHt2YWx1ZTplLGVudW1lcmFibGU6'
    'ITB9KSxlKSksbGw9KChlLHQpPT5mdW5jdGlvbiByKCl7cmV0dXJuIHR8fCgw'
    'LGVbbmwoZSlbMF1dKSgodD17ZXhwb3J0czp7fX0pLmV4cG9ydHMsdCksdC5l'
    'eHBvcnRzfSkoeyJub2RlX21vZHVsZXMvanN6aXAvZGlzdC9qc3ppcC5taW4u'
    'anMiKGUsdCl7IWZ1bmN0aW9uKHIpeyJvYmplY3QiPT10eXBlb2YgZSYmdm9p'
    'ZCAwIT09dD90LmV4cG9ydHM9cigpOiJmdW5jdGlvbiI9PXR5cGVvZiBkZWZp'
    'bmUmJmRlZmluZS5hbWQ/ZGVmaW5lKFtdLHIpOigidW5kZWZpbmVkIiE9dHlw'
    'ZW9mIHdpbmRvdz93aW5kb3c6InVuZGVmaW5lZCIhPXR5cGVvZiBnbG9iYWw/'
    'Z2xvYmFsOiJ1bmRlZmluZWQiIT10eXBlb2Ygc2VsZj9zZWxmOnRoaXMpLkpT'
    'WmlwPXIoKX0oZnVuY3Rpb24oKXtyZXR1cm4gZnVuY3Rpb24gZSh0LHIsbil7'
    'ZnVuY3Rpb24gaShvLGEpe2lmKCFyW29dKXtpZighdFtvXSl7dmFyIGM9ImZ1'
    'bmN0aW9uIj09dHlwZW9mIG9sJiZvbDtpZighYSYmYylyZXR1cm4gYyhvLCEw'
    'KTtpZihzKXJldHVybiBzKG8sITApO3ZhciB1PW5ldyBFcnJvcigiQ2Fubm90'
    'IGZpbmQgbW9kdWxlICciK28rIiciKTt0aHJvdyB1LmNvZGU9Ik1PRFVMRV9O'
    'T1RfRk9VTkQiLHV9dmFyIGw9cltvXT17ZXhwb3J0czp7fX07dFtvXVswXS5j'
    'YWxsKGwuZXhwb3J0cyxmdW5jdGlvbihlKXt2YXIgcjtyZXR1cm4gaSh0W29d'
    'WzFdW2VdfHxlKX0sbCxsLmV4cG9ydHMsZSx0LHIsbil9cmV0dXJuIHJbb10u'
    'ZXhwb3J0c31mb3IodmFyIHM9ImZ1bmN0aW9uIj09dHlwZW9mIG9sJiZvbCxv'
    'PTA7bzxuLmxlbmd0aDtvKyspaShuW29dKTtyZXR1cm4gaX0oezE6W2Z1bmN0'
    'aW9uKGUsdCxyKXt2YXIgbj1lKCIuL3V0aWxzIiksaT1lKCIuL3N1cHBvcnQi'
    'KSxzPSJBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWmFiY2RlZmdoaWprbG1u'
    'b3BxcnN0dXZ3eHl6MDEyMzQ1Njc4OSsvPSI7ci5lbmNvZGU9ZnVuY3Rpb24o'
    'ZSl7Zm9yKHZhciB0LHIsaSxvLGEsYyx1LGw9W10sZD0wLHc9ZS5sZW5ndGgs'
    'aD13LGY9InN0cmluZyIhPT1uLmdldFR5cGVPZihlKTtkPGUubGVuZ3RoOylo'
    'PXctZCxpPWY/KHQ9ZVtkKytdLHI9ZDx3P2VbZCsrXTowLGQ8dz9lW2QrK106'
    'MCk6KHQ9ZS5jaGFyQ29kZUF0KGQrKykscj1kPHc/ZS5jaGFyQ29kZUF0KGQr'
    'Kyk6MCxkPHc/ZS5jaGFyQ29kZUF0KGQrKyk6MCksbz10Pj4yLGE9KDMmdCk8'
    'PDR8cj4+NCxjPTE8aD8oMTUmcik8PDJ8aT4+Njo2NCx1PTI8aD82MyZpOjY0'
    'LGwucHVzaChzLmNoYXJBdChvKStzLmNoYXJBdChhKStzLmNoYXJBdChjKStz'
    'LmNoYXJBdCh1KSk7cmV0dXJuIGwuam9pbigiIil9LHIuZGVjb2RlPWZ1bmN0'
    'aW9uKGUpe3ZhciB0LHIsbixvLGEsYyx1PTAsbD0wLGQ9ImRhdGE6IjtpZihl'
    'LnN1YnN0cigwLDUpPT09ZCl0aHJvdyBuZXcgRXJyb3IoIkludmFsaWQgYmFz'
    'ZTY0IGlucHV0LCBpdCBsb29rcyBsaWtlIGEgZGF0YSB1cmwuIik7dmFyIHcs'
    'aD0zKihlPWUucmVwbGFjZSgvW15BLVphLXowLTkrLz1dL2csIiIpKS5sZW5n'
    'dGgvNDtpZihlLmNoYXJBdChlLmxlbmd0aC0xKT09PXMuY2hhckF0KDY0KSYm'
    'aC0tLGUuY2hhckF0KGUubGVuZ3RoLTIpPT09cy5jaGFyQXQoNjQpJiZoLS0s'
    'aCUxIT0wKXRocm93IG5ldyBFcnJvcigiSW52YWxpZCBiYXNlNjQgaW5wdXQs'
    'IGJhZCBjb250ZW50IGxlbmd0aC4iKTtmb3Iodz1pLnVpbnQ4YXJyYXk/bmV3'
    'IFVpbnQ4QXJyYXkoMHxoKTpuZXcgQXJyYXkoMHxoKTt1PGUubGVuZ3RoOyl0'
    'PXMuaW5kZXhPZihlLmNoYXJBdCh1KyspKTw8Mnwobz1zLmluZGV4T2YoZS5j'
    'aGFyQXQodSsrKSkpPj40LHI9KDE1Jm8pPDw0fChhPXMuaW5kZXhPZihlLmNo'
    'YXJBdCh1KyspKSk+PjIsbj0oMyZhKTw8NnwoYz1zLmluZGV4T2YoZS5jaGFy'
    'QXQodSsrKSkpLHdbbCsrXT10LDY0IT09YSYmKHdbbCsrXT1yKSw2NCE9PWMm'
    'Jih3W2wrK109bik7cmV0dXJuIHd9fSx7Ii4vc3VwcG9ydCI6MzAsIi4vdXRp'
    'bHMiOjMyfV0sMjpbZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoIi4vZXh0ZXJu'
    'YWwiKSxpPWUoIi4vc3RyZWFtL0RhdGFXb3JrZXIiKSxzPWUoIi4vc3RyZWFt'
    'L0NyYzMyUHJvYmUiKSxvPWUoIi4vc3RyZWFtL0RhdGFMZW5ndGhQcm9iZSIp'
    'O2Z1bmN0aW9uIGEoZSx0LHIsbixpKXt0aGlzLmNvbXByZXNzZWRTaXplPWUs'
    'dGhpcy51bmNvbXByZXNzZWRTaXplPXQsdGhpcy5jcmMzMj1yLHRoaXMuY29t'
    'cHJlc3Npb249bix0aGlzLmNvbXByZXNzZWRDb250ZW50PWl9YS5wcm90b3R5'
    'cGU9e2dldENvbnRlbnRXb3JrZXI6ZnVuY3Rpb24oKXt2YXIgZT1uZXcgaShu'
    'LlByb21pc2UucmVzb2x2ZSh0aGlzLmNvbXByZXNzZWRDb250ZW50KSkucGlw'
    'ZSh0aGlzLmNvbXByZXNzaW9uLnVuY29tcHJlc3NXb3JrZXIoKSkucGlwZShu'
    'ZXcgbygiZGF0YV9sZW5ndGgiKSksdD10aGlzO3JldHVybiBlLm9uKCJlbmQi'
    'LGZ1bmN0aW9uKCl7aWYodGhpcy5zdHJlYW1JbmZvLmRhdGFfbGVuZ3RoIT09'
    'dC51bmNvbXByZXNzZWRTaXplKXRocm93IG5ldyBFcnJvcigiQnVnIDogdW5j'
    'b21wcmVzc2VkIGRhdGEgc2l6ZSBtaXNtYXRjaCIpfSksZX0sZ2V0Q29tcHJl'
    'c3NlZFdvcmtlcjpmdW5jdGlvbigpe3JldHVybiBuZXcgaShuLlByb21pc2Uu'
    'cmVzb2x2ZSh0aGlzLmNvbXByZXNzZWRDb250ZW50KSkud2l0aFN0cmVhbUlu'
    'Zm8oImNvbXByZXNzZWRTaXplIix0aGlzLmNvbXByZXNzZWRTaXplKS53aXRo'
    'U3RyZWFtSW5mbygidW5jb21wcmVzc2VkU2l6ZSIsdGhpcy51bmNvbXByZXNz'
    'ZWRTaXplKS53aXRoU3RyZWFtSW5mbygiY3JjMzIiLHRoaXMuY3JjMzIpLndp'
    'dGhTdHJlYW1JbmZvKCJjb21wcmVzc2lvbiIsdGhpcy5jb21wcmVzc2lvbil9'
    'fSxhLmNyZWF0ZVdvcmtlckZyb209ZnVuY3Rpb24oZSx0LHIpe3JldHVybiBl'
    'LnBpcGUobmV3IHMpLnBpcGUobmV3IG8oInVuY29tcHJlc3NlZFNpemUiKSku'
    'cGlwZSh0LmNvbXByZXNzV29ya2VyKHIpKS5waXBlKG5ldyBvKCJjb21wcmVz'
    'c2VkU2l6ZSIpKS53aXRoU3RyZWFtSW5mbygiY29tcHJlc3Npb24iLHQpfSx0'
    'LmV4cG9ydHM9YX0seyIuL2V4dGVybmFsIjo2LCIuL3N0cmVhbS9DcmMzMlBy'
    'b2JlIjoyNSwiLi9zdHJlYW0vRGF0YUxlbmd0aFByb2JlIjoyNiwiLi9zdHJl'
    'YW0vRGF0YVdvcmtlciI6Mjd9XSwzOltmdW5jdGlvbihlLHQscil7dmFyIG49'
    'ZSgiLi9zdHJlYW0vR2VuZXJpY1dvcmtlciIpO3IuU1RPUkU9e21hZ2ljOiJc'
    'MFwwIixjb21wcmVzc1dvcmtlcjpmdW5jdGlvbigpe3JldHVybiBuZXcgbigi'
    'U1RPUkUgY29tcHJlc3Npb24iKX0sdW5jb21wcmVzc1dvcmtlcjpmdW5jdGlv'
    'bigpe3JldHVybiBuZXcgbigiU1RPUkUgZGVjb21wcmVzc2lvbiIpfX0sci5E'
    'RUZMQVRFPWUoIi4vZmxhdGUiKX0seyIuL2ZsYXRlIjo3LCIuL3N0cmVhbS9H'
    'ZW5lcmljV29ya2VyIjoyOH1dLDQ6W2Z1bmN0aW9uKGUsdCxyKXt2YXIgbj1l'
    'KCIuL3V0aWxzIiksaT1mdW5jdGlvbigpe2Zvcih2YXIgZSx0PVtdLHI9MDty'
    'PDI1NjtyKyspe2U9cjtmb3IodmFyIG49MDtuPDg7bisrKWU9MSZlPzM5ODgy'
    'OTIzODReZT4+PjE6ZT4+PjE7dFtyXT1lfXJldHVybiB0fSgpO3QuZXhwb3J0'
    'cz1mdW5jdGlvbihlLHQpe3JldHVybiB2b2lkIDAhPT1lJiZlLmxlbmd0aD8i'
    'c3RyaW5nIiE9PW4uZ2V0VHlwZU9mKGUpP2Z1bmN0aW9uKGUsdCxyLG4pe3Zh'
    'ciBzPWksbz0wK3I7ZV49LTE7Zm9yKHZhciBhPTA7YTxvO2ErKyllPWU+Pj44'
    'XnNbMjU1JihlXnRbYV0pXTtyZXR1cm4tMV5lfSgwfHQsZSxlLmxlbmd0aCww'
    'KTpmdW5jdGlvbihlLHQscixuKXt2YXIgcz1pLG89MCtyO2VePS0xO2Zvcih2'
    'YXIgYT0wO2E8bzthKyspZT1lPj4+OF5zWzI1NSYoZV50LmNoYXJDb2RlQXQo'
    'YSkpXTtyZXR1cm4tMV5lfSgwfHQsZSxlLmxlbmd0aCwwKTowfX0seyIuL3V0'
    'aWxzIjozMn1dLDU6W2Z1bmN0aW9uKGUsdCxyKXtyLmJhc2U2ND0hMSxyLmJp'
    'bmFyeT0hMSxyLmRpcj0hMSxyLmNyZWF0ZUZvbGRlcnM9ITAsci5kYXRlPW51'
    'bGwsci5jb21wcmVzc2lvbj1udWxsLHIuY29tcHJlc3Npb25PcHRpb25zPW51'
    'bGwsci5jb21tZW50PW51bGwsci51bml4UGVybWlzc2lvbnM9bnVsbCxyLmRv'
    'c1Blcm1pc3Npb25zPW51bGx9LHt9XSw2OltmdW5jdGlvbihlLHQscil7dmFy'
    'IG49bnVsbDtuPSJ1bmRlZmluZWQiIT10eXBlb2YgUHJvbWlzZT9Qcm9taXNl'
    'OmUoImxpZSIpLHQuZXhwb3J0cz17UHJvbWlzZTpufX0se2xpZTozN31dLDc6'
    'W2Z1bmN0aW9uKGUsdCxyKXt2YXIgbj0idW5kZWZpbmVkIiE9dHlwZW9mIFVp'
    'bnQ4QXJyYXkmJiJ1bmRlZmluZWQiIT10eXBlb2YgVWludDE2QXJyYXkmJiJ1'
    'bmRlZmluZWQiIT10eXBlb2YgVWludDMyQXJyYXksaT1lKCJwYWtvIikscz1l'
    'KCIuL3V0aWxzIiksbz1lKCIuL3N0cmVhbS9HZW5lcmljV29ya2VyIiksYT1u'
    'PyJ1aW50OGFycmF5IjoiYXJyYXkiO2Z1bmN0aW9uIGMoZSx0KXtvLmNhbGwo'
    'dGhpcywiRmxhdGVXb3JrZXIvIitlKSx0aGlzLl9wYWtvPW51bGwsdGhpcy5f'
    'cGFrb0FjdGlvbj1lLHRoaXMuX3Bha29PcHRpb25zPXQsdGhpcy5tZXRhPXt9'
    'fXIubWFnaWM9IlxiXDAiLHMuaW5oZXJpdHMoYyxvKSxjLnByb3RvdHlwZS5w'
    'cm9jZXNzQ2h1bms9ZnVuY3Rpb24oZSl7dGhpcy5tZXRhPWUubWV0YSxudWxs'
    'PT09dGhpcy5fcGFrbyYmdGhpcy5fY3JlYXRlUGFrbygpLHRoaXMuX3Bha28u'
    'cHVzaChzLnRyYW5zZm9ybVRvKGEsZS5kYXRhKSwhMSl9LGMucHJvdG90eXBl'
    'LmZsdXNoPWZ1bmN0aW9uKCl7by5wcm90b3R5cGUuZmx1c2guY2FsbCh0aGlz'
    'KSxudWxsPT09dGhpcy5fcGFrbyYmdGhpcy5fY3JlYXRlUGFrbygpLHRoaXMu'
    'X3Bha28ucHVzaChbXSwhMCl9LGMucHJvdG90eXBlLmNsZWFuVXA9ZnVuY3Rp'
    'b24oKXtvLnByb3RvdHlwZS5jbGVhblVwLmNhbGwodGhpcyksdGhpcy5fcGFr'
    'bz1udWxsfSxjLnByb3RvdHlwZS5fY3JlYXRlUGFrbz1mdW5jdGlvbigpe3Ro'
    'aXMuX3Bha289bmV3IGlbdGhpcy5fcGFrb0FjdGlvbl0oe3JhdzohMCxsZXZl'
    'bDp0aGlzLl9wYWtvT3B0aW9ucy5sZXZlbHx8LTF9KTt2YXIgZT10aGlzO3Ro'
    'aXMuX3Bha28ub25EYXRhPWZ1bmN0aW9uKHQpe2UucHVzaCh7ZGF0YTp0LG1l'
    'dGE6ZS5tZXRhfSl9fSxyLmNvbXByZXNzV29ya2VyPWZ1bmN0aW9uKGUpe3Jl'
    'dHVybiBuZXcgYygiRGVmbGF0ZSIsZSl9LHIudW5jb21wcmVzc1dvcmtlcj1m'
    'dW5jdGlvbigpe3JldHVybiBuZXcgYygiSW5mbGF0ZSIse30pfX0seyIuL3N0'
    'cmVhbS9HZW5lcmljV29ya2VyIjoyOCwiLi91dGlscyI6MzIscGFrbzozOH1d'
    'LDg6W2Z1bmN0aW9uKGUsdCxyKXtmdW5jdGlvbiBuKGUsdCl7dmFyIHIsbj0i'
    'Ijtmb3Iocj0wO3I8dDtyKyspbis9U3RyaW5nLmZyb21DaGFyQ29kZSgyNTUm'
    'ZSksZT4+Pj04O3JldHVybiBufWZ1bmN0aW9uIGkoZSx0LHIsaSxvLGwpe3Zh'
    'ciBkLHcsaD1lLmZpbGUsZj1lLmNvbXByZXNzaW9uLEE9bCE9PWEudXRmOGVu'
    'Y29kZSxwPXMudHJhbnNmb3JtVG8oInN0cmluZyIsbChoLm5hbWUpKSxFPXMu'
    'dHJhbnNmb3JtVG8oInN0cmluZyIsYS51dGY4ZW5jb2RlKGgubmFtZSkpLEI9'
    'aC5jb21tZW50LEg9cy50cmFuc2Zvcm1Ubygic3RyaW5nIixsKEIpKSxtPXMu'
    'dHJhbnNmb3JtVG8oInN0cmluZyIsYS51dGY4ZW5jb2RlKEIpKSxnPUUubGVu'
    'Z3RoIT09aC5uYW1lLmxlbmd0aCx5PW0ubGVuZ3RoIT09Qi5sZW5ndGgsVD0i'
    'Iix4PSIiLHY9IiIsYj1oLmRpcixSPWguZGF0ZSxNPXtjcmMzMjowLGNvbXBy'
    'ZXNzZWRTaXplOjAsdW5jb21wcmVzc2VkU2l6ZTowfTt0JiYhcnx8KE0uY3Jj'
    'MzI9ZS5jcmMzMixNLmNvbXByZXNzZWRTaXplPWUuY29tcHJlc3NlZFNpemUs'
    'TS51bmNvbXByZXNzZWRTaXplPWUudW5jb21wcmVzc2VkU2l6ZSk7dmFyIGs9'
    'MDt0JiYoa3w9OCksQXx8IWcmJiF5fHwoa3w9MjA0OCk7dmFyIFM9MCxDPTAs'
    'XyxPLFA7YiYmKFN8PTE2KSwiVU5JWCI9PT1vPyhDPTc5OCxTfD0oXz1oLnVu'
    'aXhQZXJtaXNzaW9ucyxPPWIsUD1fLF98fChQPU8/MTY4OTM6MzMyMDQpLCg2'
    'NTUzNSZQKTw8MTYpKTooQz0yMCxTfD1mdW5jdGlvbihlKXtyZXR1cm4gNjMm'
    'KGV8fDApfShoLmRvc1Blcm1pc3Npb25zKSksZD1SLmdldFVUQ0hvdXJzKCks'
    'ZDw8PTYsZHw9Ui5nZXRVVENNaW51dGVzKCksZDw8PTUsZHw9Ui5nZXRVVENT'
    'ZWNvbmRzKCkvMix3PVIuZ2V0VVRDRnVsbFllYXIoKS0xOTgwLHc8PD00LHd8'
    'PVIuZ2V0VVRDTW9udGgoKSsxLHc8PD01LHd8PVIuZ2V0VVRDRGF0ZSgpLGcm'
    'Jih4PW4oMSwxKStuKGMocCksNCkrRSxUKz0idXAiK24oeC5sZW5ndGgsMikr'
    'eCkseSYmKHY9bigxLDEpK24oYyhIKSw0KSttLFQrPSJ1YyIrbih2Lmxlbmd0'
    'aCwyKSt2KTt2YXIgTD0iIjtyZXR1cm4gTCs9IlxuXDAiLEwrPW4oaywyKSxM'
    'Kz1mLm1hZ2ljLEwrPW4oZCwyKSxMKz1uKHcsMiksTCs9bihNLmNyYzMyLDQp'
    'LEwrPW4oTS5jb21wcmVzc2VkU2l6ZSw0KSxMKz1uKE0udW5jb21wcmVzc2Vk'
    'U2l6ZSw0KSxMKz1uKHAubGVuZ3RoLDIpLEwrPW4oVC5sZW5ndGgsMikse2Zp'
    'bGVSZWNvcmQ6dS5MT0NBTF9GSUxFX0hFQURFUitMK3ArVCxkaXJSZWNvcmQ6'
    'dS5DRU5UUkFMX0ZJTEVfSEVBREVSK24oQywyKStMK24oSC5sZW5ndGgsMikr'
    'IlwwXDBcMFwwIituKFMsNCkrbihpLDQpK3ArVCtIfX12YXIgcz1lKCIuLi91'
    'dGlscyIpLG89ZSgiLi4vc3RyZWFtL0dlbmVyaWNXb3JrZXIiKSxhPWUoIi4u'
    'L3V0ZjgiKSxjPWUoIi4uL2NyYzMyIiksdT1lKCIuLi9zaWduYXR1cmUiKTtm'
    'dW5jdGlvbiBsKGUsdCxyLG4pe28uY2FsbCh0aGlzLCJaaXBGaWxlV29ya2Vy'
    'IiksdGhpcy5ieXRlc1dyaXR0ZW49MCx0aGlzLnppcENvbW1lbnQ9dCx0aGlz'
    'LnppcFBsYXRmb3JtPXIsdGhpcy5lbmNvZGVGaWxlTmFtZT1uLHRoaXMuc3Ry'
    'ZWFtRmlsZXM9ZSx0aGlzLmFjY3VtdWxhdGU9ITEsdGhpcy5jb250ZW50QnVm'
    'ZmVyPVtdLHRoaXMuZGlyUmVjb3Jkcz1bXSx0aGlzLmN1cnJlbnRTb3VyY2VP'
    'ZmZzZXQ9MCx0aGlzLmVudHJpZXNDb3VudD0wLHRoaXMuY3VycmVudEZpbGU9'
    'bnVsbCx0aGlzLl9zb3VyY2VzPVtdfXMuaW5oZXJpdHMobCxvKSxsLnByb3Rv'
    'dHlwZS5wdXNoPWZ1bmN0aW9uKGUpe3ZhciB0PWUubWV0YS5wZXJjZW50fHww'
    'LHI9dGhpcy5lbnRyaWVzQ291bnQsbj10aGlzLl9zb3VyY2VzLmxlbmd0aDt0'
    'aGlzLmFjY3VtdWxhdGU/dGhpcy5jb250ZW50QnVmZmVyLnB1c2goZSk6KHRo'
    'aXMuYnl0ZXNXcml0dGVuKz1lLmRhdGEubGVuZ3RoLG8ucHJvdG90eXBlLnB1'
    'c2guY2FsbCh0aGlzLHtkYXRhOmUuZGF0YSxtZXRhOntjdXJyZW50RmlsZTp0'
    'aGlzLmN1cnJlbnRGaWxlLHBlcmNlbnQ6cj8odCsxMDAqKHItbi0xKSkvcjox'
    'MDB9fSkpfSxsLnByb3RvdHlwZS5vcGVuZWRTb3VyY2U9ZnVuY3Rpb24oZSl7'
    'dGhpcy5jdXJyZW50U291cmNlT2Zmc2V0PXRoaXMuYnl0ZXNXcml0dGVuLHRo'
    'aXMuY3VycmVudEZpbGU9ZS5maWxlLm5hbWU7dmFyIHQ9dGhpcy5zdHJlYW1G'
    'aWxlcyYmIWUuZmlsZS5kaXI7aWYodCl7dmFyIHI9aShlLHQsITEsdGhpcy5j'
    'dXJyZW50U291cmNlT2Zmc2V0LHRoaXMuemlwUGxhdGZvcm0sdGhpcy5lbmNv'
    'ZGVGaWxlTmFtZSk7dGhpcy5wdXNoKHtkYXRhOnIuZmlsZVJlY29yZCxtZXRh'
    'OntwZXJjZW50OjB9fSl9ZWxzZSB0aGlzLmFjY3VtdWxhdGU9ITB9LGwucHJv'
    'dG90eXBlLmNsb3NlZFNvdXJjZT1mdW5jdGlvbihlKXt0aGlzLmFjY3VtdWxh'
    'dGU9ITE7dmFyIHQ9dGhpcy5zdHJlYW1GaWxlcyYmIWUuZmlsZS5kaXIscj1p'
    'KGUsdCwhMCx0aGlzLmN1cnJlbnRTb3VyY2VPZmZzZXQsdGhpcy56aXBQbGF0'
    'Zm9ybSx0aGlzLmVuY29kZUZpbGVOYW1lKSxzO2lmKHRoaXMuZGlyUmVjb3Jk'
    'cy5wdXNoKHIuZGlyUmVjb3JkKSx0KXRoaXMucHVzaCh7ZGF0YToocz1lLHUu'
    'REFUQV9ERVNDUklQVE9SK24ocy5jcmMzMiw0KStuKHMuY29tcHJlc3NlZFNp'
    'emUsNCkrbihzLnVuY29tcHJlc3NlZFNpemUsNCkpLG1ldGE6e3BlcmNlbnQ6'
    'MTAwfX0pO2Vsc2UgZm9yKHRoaXMucHVzaCh7ZGF0YTpyLmZpbGVSZWNvcmQs'
    'bWV0YTp7cGVyY2VudDowfX0pO3RoaXMuY29udGVudEJ1ZmZlci5sZW5ndGg7'
    'KXRoaXMucHVzaCh0aGlzLmNvbnRlbnRCdWZmZXIuc2hpZnQoKSk7dGhpcy5j'
    'dXJyZW50RmlsZT1udWxsfSxsLnByb3RvdHlwZS5mbHVzaD1mdW5jdGlvbigp'
    'e2Zvcih2YXIgZT10aGlzLmJ5dGVzV3JpdHRlbix0PTA7dDx0aGlzLmRpclJl'
    'Y29yZHMubGVuZ3RoO3QrKyl0aGlzLnB1c2goe2RhdGE6dGhpcy5kaXJSZWNv'
    'cmRzW3RdLG1ldGE6e3BlcmNlbnQ6MTAwfX0pO3ZhciByPXRoaXMuYnl0ZXNX'
    'cml0dGVuLWUsaT0obz10aGlzLmRpclJlY29yZHMubGVuZ3RoLGE9cixjPWUs'
    'bD10aGlzLnppcENvbW1lbnQsZD10aGlzLmVuY29kZUZpbGVOYW1lLHc9cy50'
    'cmFuc2Zvcm1Ubygic3RyaW5nIixkKGwpKSx1LkNFTlRSQUxfRElSRUNUT1JZ'
    'X0VORCsiXDBcMFwwXDAiK24obywyKStuKG8sMikrbihhLDQpK24oYyw0KStu'
    'KHcubGVuZ3RoLDIpK3cpLG8sYSxjLGwsZCx3O3RoaXMucHVzaCh7ZGF0YTpp'
    'LG1ldGE6e3BlcmNlbnQ6MTAwfX0pfSxsLnByb3RvdHlwZS5wcmVwYXJlTmV4'
    'dFNvdXJjZT1mdW5jdGlvbigpe3RoaXMucHJldmlvdXM9dGhpcy5fc291cmNl'
    'cy5zaGlmdCgpLHRoaXMub3BlbmVkU291cmNlKHRoaXMucHJldmlvdXMuc3Ry'
    'ZWFtSW5mbyksdGhpcy5pc1BhdXNlZD90aGlzLnByZXZpb3VzLnBhdXNlKCk6'
    'dGhpcy5wcmV2aW91cy5yZXN1bWUoKX0sbC5wcm90b3R5cGUucmVnaXN0ZXJQ'
    'cmV2aW91cz1mdW5jdGlvbihlKXt0aGlzLl9zb3VyY2VzLnB1c2goZSk7dmFy'
    'IHQ9dGhpcztyZXR1cm4gZS5vbigiZGF0YSIsZnVuY3Rpb24oZSl7dC5wcm9j'
    'ZXNzQ2h1bmsoZSl9KSxlLm9uKCJlbmQiLGZ1bmN0aW9uKCl7dC5jbG9zZWRT'
    'b3VyY2UodC5wcmV2aW91cy5zdHJlYW1JbmZvKSx0Ll9zb3VyY2VzLmxlbmd0'
    'aD90LnByZXBhcmVOZXh0U291cmNlKCk6dC5lbmQoKX0pLGUub24oImVycm9y'
    'IixmdW5jdGlvbihlKXt0LmVycm9yKGUpfSksdGhpc30sbC5wcm90b3R5cGUu'
    'cmVzdW1lPWZ1bmN0aW9uKCl7cmV0dXJuISFvLnByb3RvdHlwZS5yZXN1bWUu'
    'Y2FsbCh0aGlzKSYmKCF0aGlzLnByZXZpb3VzJiZ0aGlzLl9zb3VyY2VzLmxl'
    'bmd0aD8odGhpcy5wcmVwYXJlTmV4dFNvdXJjZSgpLCEwKTp0aGlzLnByZXZp'
    'b3VzfHx0aGlzLl9zb3VyY2VzLmxlbmd0aHx8dGhpcy5nZW5lcmF0ZWRFcnJv'
    'cj92b2lkIDA6KHRoaXMuZW5kKCksITApKX0sbC5wcm90b3R5cGUuZXJyb3I9'
    'ZnVuY3Rpb24oZSl7dmFyIHQ9dGhpcy5fc291cmNlcztpZighby5wcm90b3R5'
    'cGUuZXJyb3IuY2FsbCh0aGlzLGUpKXJldHVybiExO2Zvcih2YXIgcj0wO3I8'
    'dC5sZW5ndGg7cisrKXRyeXt0W3JdLmVycm9yKGUpfWNhdGNoKGUpe31yZXR1'
    'cm4hMH0sbC5wcm90b3R5cGUubG9jaz1mdW5jdGlvbigpe28ucHJvdG90eXBl'
    'LmxvY2suY2FsbCh0aGlzKTtmb3IodmFyIGU9dGhpcy5fc291cmNlcyx0PTA7'
    'dDxlLmxlbmd0aDt0KyspZVt0XS5sb2NrKCl9LHQuZXhwb3J0cz1sfSx7Ii4u'
    'L2NyYzMyIjo0LCIuLi9zaWduYXR1cmUiOjIzLCIuLi9zdHJlYW0vR2VuZXJp'
    'Y1dvcmtlciI6MjgsIi4uL3V0ZjgiOjMxLCIuLi91dGlscyI6MzJ9XSw5Oltm'
    'dW5jdGlvbihlLHQscil7dmFyIG49ZSgiLi4vY29tcHJlc3Npb25zIiksaT1l'
    'KCIuL1ppcEZpbGVXb3JrZXIiKTtyLmdlbmVyYXRlV29ya2VyPWZ1bmN0aW9u'
    'KGUsdCxyKXt2YXIgcz1uZXcgaSh0LnN0cmVhbUZpbGVzLHIsdC5wbGF0Zm9y'
    'bSx0LmVuY29kZUZpbGVOYW1lKSxvPTA7dHJ5e2UuZm9yRWFjaChmdW5jdGlv'
    'bihlLHIpe28rKzt2YXIgaT1mdW5jdGlvbihlLHQpe3ZhciByPWV8fHQsaT1u'
    'W3JdO2lmKCFpKXRocm93IG5ldyBFcnJvcihyKyIgaXMgbm90IGEgdmFsaWQg'
    'Y29tcHJlc3Npb24gbWV0aG9kICEiKTtyZXR1cm4gaX0oci5vcHRpb25zLmNv'
    'bXByZXNzaW9uLHQuY29tcHJlc3Npb24pLGE9ci5vcHRpb25zLmNvbXByZXNz'
    'aW9uT3B0aW9uc3x8dC5jb21wcmVzc2lvbk9wdGlvbnN8fHt9LGM9ci5kaXIs'
    'dT1yLmRhdGU7ci5fY29tcHJlc3NXb3JrZXIoaSxhKS53aXRoU3RyZWFtSW5m'
    'bygiZmlsZSIse25hbWU6ZSxkaXI6YyxkYXRlOnUsY29tbWVudDpyLmNvbW1l'
    'bnR8fCIiLHVuaXhQZXJtaXNzaW9uczpyLnVuaXhQZXJtaXNzaW9ucyxkb3NQ'
    'ZXJtaXNzaW9uczpyLmRvc1Blcm1pc3Npb25zfSkucGlwZShzKX0pLHMuZW50'
    'cmllc0NvdW50PW99Y2F0Y2goZSl7cy5lcnJvcihlKX1yZXR1cm4gc319LHsi'
    'Li4vY29tcHJlc3Npb25zIjozLCIuL1ppcEZpbGVXb3JrZXIiOjh9XSwxMDpb'
    'ZnVuY3Rpb24oZSx0LHIpe2Z1bmN0aW9uIG4oKXtpZighKHRoaXMgaW5zdGFu'
    'Y2VvZiBuKSlyZXR1cm4gbmV3IG47aWYoYXJndW1lbnRzLmxlbmd0aCl0aHJv'
    'dyBuZXcgRXJyb3IoIlRoZSBjb25zdHJ1Y3RvciB3aXRoIHBhcmFtZXRlcnMg'
    'aGFzIGJlZW4gcmVtb3ZlZCBpbiBKU1ppcCAzLjAsIHBsZWFzZSBjaGVjayB0'
    'aGUgdXBncmFkZSBndWlkZS4iKTt0aGlzLmZpbGVzPU9iamVjdC5jcmVhdGUo'
    'bnVsbCksdGhpcy5jb21tZW50PW51bGwsdGhpcy5yb290PSIiLHRoaXMuY2xv'
    'bmU9ZnVuY3Rpb24oKXt2YXIgZT1uZXcgbjtmb3IodmFyIHQgaW4gdGhpcyki'
    'ZnVuY3Rpb24iIT10eXBlb2YgdGhpc1t0XSYmKGVbdF09dGhpc1t0XSk7cmV0'
    'dXJuIGV9fShuLnByb3RvdHlwZT1lKCIuL29iamVjdCIpKS5sb2FkQXN5bmM9'
    'ZSgiLi9sb2FkIiksbi5zdXBwb3J0PWUoIi4vc3VwcG9ydCIpLG4uZGVmYXVs'
    'dHM9ZSgiLi9kZWZhdWx0cyIpLG4udmVyc2lvbj0iMy4xMC4xIixuLmxvYWRB'
    'c3luYz1mdW5jdGlvbihlLHQpe3JldHVybihuZXcgbikubG9hZEFzeW5jKGUs'
    'dCl9LG4uZXh0ZXJuYWw9ZSgiLi9leHRlcm5hbCIpLHQuZXhwb3J0cz1ufSx7'
    'Ii4vZGVmYXVsdHMiOjUsIi4vZXh0ZXJuYWwiOjYsIi4vbG9hZCI6MTEsIi4v'
    'b2JqZWN0IjoxNSwiLi9zdXBwb3J0IjozMH1dLDExOltmdW5jdGlvbihlLHQs'
    'cil7dmFyIG49ZSgiLi91dGlscyIpLGk9ZSgiLi9leHRlcm5hbCIpLHM9ZSgi'
    'Li91dGY4Iiksbz1lKCIuL3ppcEVudHJpZXMiKSxhPWUoIi4vc3RyZWFtL0Ny'
    'YzMyUHJvYmUiKSxjPWUoIi4vbm9kZWpzVXRpbHMiKTtmdW5jdGlvbiB1KGUp'
    'e3JldHVybiBuZXcgaS5Qcm9taXNlKGZ1bmN0aW9uKHQscil7dmFyIG49ZS5k'
    'ZWNvbXByZXNzZWQuZ2V0Q29udGVudFdvcmtlcigpLnBpcGUobmV3IGEpO24u'
    'b24oImVycm9yIixmdW5jdGlvbihlKXtyKGUpfSkub24oImVuZCIsZnVuY3Rp'
    'b24oKXtuLnN0cmVhbUluZm8uY3JjMzIhPT1lLmRlY29tcHJlc3NlZC5jcmMz'
    'Mj9yKG5ldyBFcnJvcigiQ29ycnVwdGVkIHppcCA6IENSQzMyIG1pc21hdGNo'
    'IikpOnQoKX0pLnJlc3VtZSgpfSl9dC5leHBvcnRzPWZ1bmN0aW9uKGUsdCl7'
    'dmFyIHI9dGhpcztyZXR1cm4gdD1uLmV4dGVuZCh0fHx7fSx7YmFzZTY0OiEx'
    'LGNoZWNrQ1JDMzI6ITEsb3B0aW1pemVkQmluYXJ5U3RyaW5nOiExLGNyZWF0'
    'ZUZvbGRlcnM6ITEsZGVjb2RlRmlsZU5hbWU6cy51dGY4ZGVjb2RlfSksYy5p'
    'c05vZGUmJmMuaXNTdHJlYW0oZSk/aS5Qcm9taXNlLnJlamVjdChuZXcgRXJy'
    'b3IoIkpTWmlwIGNhbid0IGFjY2VwdCBhIHN0cmVhbSB3aGVuIGxvYWRpbmcg'
    'YSB6aXAgZmlsZS4iKSk6bi5wcmVwYXJlQ29udGVudCgidGhlIGxvYWRlZCB6'
    'aXAgZmlsZSIsZSwhMCx0Lm9wdGltaXplZEJpbmFyeVN0cmluZyx0LmJhc2U2'
    'NCkudGhlbihmdW5jdGlvbihlKXt2YXIgcj1uZXcgbyh0KTtyZXR1cm4gci5s'
    'b2FkKGUpLHJ9KS50aGVuKGZ1bmN0aW9uKGUpe3ZhciByPVtpLlByb21pc2Uu'
    'cmVzb2x2ZShlKV0sbj1lLmZpbGVzO2lmKHQuY2hlY2tDUkMzMilmb3IodmFy'
    'IHM9MDtzPG4ubGVuZ3RoO3MrKylyLnB1c2godShuW3NdKSk7cmV0dXJuIGku'
    'UHJvbWlzZS5hbGwocil9KS50aGVuKGZ1bmN0aW9uKGUpe2Zvcih2YXIgaT1l'
    'LnNoaWZ0KCkscz1pLmZpbGVzLG89MDtvPHMubGVuZ3RoO28rKyl7dmFyIGE9'
    'c1tvXSxjPWEuZmlsZU5hbWVTdHIsdT1uLnJlc29sdmUoYS5maWxlTmFtZVN0'
    'cik7ci5maWxlKHUsYS5kZWNvbXByZXNzZWQse2JpbmFyeTohMCxvcHRpbWl6'
    'ZWRCaW5hcnlTdHJpbmc6ITAsZGF0ZTphLmRhdGUsZGlyOmEuZGlyLGNvbW1l'
    'bnQ6YS5maWxlQ29tbWVudFN0ci5sZW5ndGg/YS5maWxlQ29tbWVudFN0cjpu'
    'dWxsLHVuaXhQZXJtaXNzaW9uczphLnVuaXhQZXJtaXNzaW9ucyxkb3NQZXJt'
    'aXNzaW9uczphLmRvc1Blcm1pc3Npb25zLGNyZWF0ZUZvbGRlcnM6dC5jcmVh'
    'dGVGb2xkZXJzfSksYS5kaXJ8fChyLmZpbGUodSkudW5zYWZlT3JpZ2luYWxO'
    'YW1lPWMpfXJldHVybiBpLnppcENvbW1lbnQubGVuZ3RoJiYoci5jb21tZW50'
    'PWkuemlwQ29tbWVudCkscn0pfX0seyIuL2V4dGVybmFsIjo2LCIuL25vZGVq'
    'c1V0aWxzIjoxNCwiLi9zdHJlYW0vQ3JjMzJQcm9iZSI6MjUsIi4vdXRmOCI6'
    'MzEsIi4vdXRpbHMiOjMyLCIuL3ppcEVudHJpZXMiOjMzfV0sMTI6W2Z1bmN0'
    'aW9uKGUsdCxyKXt2YXIgbj1lKCIuLi91dGlscyIpLGk9ZSgiLi4vc3RyZWFt'
    'L0dlbmVyaWNXb3JrZXIiKTtmdW5jdGlvbiBzKGUsdCl7aS5jYWxsKHRoaXMs'
    'Ik5vZGVqcyBzdHJlYW0gaW5wdXQgYWRhcHRlciBmb3IgIitlKSx0aGlzLl91'
    'cHN0cmVhbUVuZGVkPSExLHRoaXMuX2JpbmRTdHJlYW0odCl9bi5pbmhlcml0'
    'cyhzLGkpLHMucHJvdG90eXBlLl9iaW5kU3RyZWFtPWZ1bmN0aW9uKGUpe3Zh'
    'ciB0PXRoaXM7KHRoaXMuX3N0cmVhbT1lKS5wYXVzZSgpLGUub24oImRhdGEi'
    'LGZ1bmN0aW9uKGUpe3QucHVzaCh7ZGF0YTplLG1ldGE6e3BlcmNlbnQ6MH19'
    'KX0pLm9uKCJlcnJvciIsZnVuY3Rpb24oZSl7dC5pc1BhdXNlZD90aGlzLmdl'
    'bmVyYXRlZEVycm9yPWU6dC5lcnJvcihlKX0pLm9uKCJlbmQiLGZ1bmN0aW9u'
    'KCl7dC5pc1BhdXNlZD90Ll91cHN0cmVhbUVuZGVkPSEwOnQuZW5kKCl9KX0s'
    'cy5wcm90b3R5cGUucGF1c2U9ZnVuY3Rpb24oKXtyZXR1cm4hIWkucHJvdG90'
    'eXBlLnBhdXNlLmNhbGwodGhpcykmJih0aGlzLl9zdHJlYW0ucGF1c2UoKSwh'
    'MCl9LHMucHJvdG90eXBlLnJlc3VtZT1mdW5jdGlvbigpe3JldHVybiEhaS5w'
    'cm90b3R5cGUucmVzdW1lLmNhbGwodGhpcykmJih0aGlzLl91cHN0cmVhbUVu'
    'ZGVkP3RoaXMuZW5kKCk6dGhpcy5fc3RyZWFtLnJlc3VtZSgpLCEwKX0sdC5l'
    'eHBvcnRzPXN9LHsiLi4vc3RyZWFtL0dlbmVyaWNXb3JrZXIiOjI4LCIuLi91'
    'dGlscyI6MzJ9XSwxMzpbZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoInJlYWRh'
    'YmxlLXN0cmVhbSIpLlJlYWRhYmxlO2Z1bmN0aW9uIGkoZSx0LHIpe24uY2Fs'
    'bCh0aGlzLHQpLHRoaXMuX2hlbHBlcj1lO3ZhciBpPXRoaXM7ZS5vbigiZGF0'
    'YSIsZnVuY3Rpb24oZSx0KXtpLnB1c2goZSl8fGkuX2hlbHBlci5wYXVzZSgp'
    'LHImJnIodCl9KS5vbigiZXJyb3IiLGZ1bmN0aW9uKGUpe2kuZW1pdCgiZXJy'
    'b3IiLGUpfSkub24oImVuZCIsZnVuY3Rpb24oKXtpLnB1c2gobnVsbCl9KX1l'
    'KCIuLi91dGlscyIpLmluaGVyaXRzKGksbiksaS5wcm90b3R5cGUuX3JlYWQ9'
    'ZnVuY3Rpb24oKXt0aGlzLl9oZWxwZXIucmVzdW1lKCl9LHQuZXhwb3J0cz1p'
    'fSx7Ii4uL3V0aWxzIjozMiwicmVhZGFibGUtc3RyZWFtIjoxNn1dLDE0Oltm'
    'dW5jdGlvbihlLHQscil7dC5leHBvcnRzPXtpc05vZGU6InVuZGVmaW5lZCIh'
    'PXR5cGVvZiBCdWZmZXIsbmV3QnVmZmVyRnJvbTpmdW5jdGlvbihlLHQpe2lm'
    'KEJ1ZmZlci5mcm9tJiZCdWZmZXIuZnJvbSE9PVVpbnQ4QXJyYXkuZnJvbSly'
    'ZXR1cm4gQnVmZmVyLmZyb20oZSx0KTtpZigibnVtYmVyIj09dHlwZW9mIGUp'
    'dGhyb3cgbmV3IEVycm9yKCdUaGUgImRhdGEiIGFyZ3VtZW50IG11c3Qgbm90'
    'IGJlIGEgbnVtYmVyJyk7cmV0dXJuIG5ldyBCdWZmZXIoZSx0KX0sYWxsb2NC'
    'dWZmZXI6ZnVuY3Rpb24oZSl7aWYoQnVmZmVyLmFsbG9jKXJldHVybiBCdWZm'
    'ZXIuYWxsb2MoZSk7dmFyIHQ9bmV3IEJ1ZmZlcihlKTtyZXR1cm4gdC5maWxs'
    'KDApLHR9LGlzQnVmZmVyOmZ1bmN0aW9uKGUpe3JldHVybiBCdWZmZXIuaXNC'
    'dWZmZXIoZSl9LGlzU3RyZWFtOmZ1bmN0aW9uKGUpe3JldHVybiBlJiYiZnVu'
    'Y3Rpb24iPT10eXBlb2YgZS5vbiYmImZ1bmN0aW9uIj09dHlwZW9mIGUucGF1'
    'c2UmJiJmdW5jdGlvbiI9PXR5cGVvZiBlLnJlc3VtZX19fSx7fV0sMTU6W2Z1'
    'bmN0aW9uKGUsdCxyKXtmdW5jdGlvbiBuKGUsdCxyKXt2YXIgbixpPXMuZ2V0'
    'VHlwZU9mKHQpLGE9cy5leHRlbmQocnx8e30sYyk7YS5kYXRlPWEuZGF0ZXx8'
    'bmV3IERhdGUsbnVsbCE9PWEuY29tcHJlc3Npb24mJihhLmNvbXByZXNzaW9u'
    'PWEuY29tcHJlc3Npb24udG9VcHBlckNhc2UoKSksInN0cmluZyI9PXR5cGVv'
    'ZiBhLnVuaXhQZXJtaXNzaW9ucyYmKGEudW5peFBlcm1pc3Npb25zPXBhcnNl'
    'SW50KGEudW5peFBlcm1pc3Npb25zLDgpKSxhLnVuaXhQZXJtaXNzaW9ucyYm'
    'MTYzODQmYS51bml4UGVybWlzc2lvbnMmJihhLmRpcj0hMCksYS5kb3NQZXJt'
    'aXNzaW9ucyYmMTYmYS5kb3NQZXJtaXNzaW9ucyYmKGEuZGlyPSEwKSxhLmRp'
    'ciYmKGU9QShlKSksYS5jcmVhdGVGb2xkZXJzJiYobj1mKGUpKSYmcC5jYWxs'
    'KHRoaXMsbiwhMCk7dmFyIGQ9InN0cmluZyI9PT1pJiYhMT09PWEuYmluYXJ5'
    'JiYhMT09PWEuYmFzZTY0O3ImJnZvaWQgMCE9PXIuYmluYXJ5fHwoYS5iaW5h'
    'cnk9IWQpLCh0IGluc3RhbmNlb2YgdSYmMD09PXQudW5jb21wcmVzc2VkU2l6'
    'ZXx8YS5kaXJ8fCF0fHwwPT09dC5sZW5ndGgpJiYoYS5iYXNlNjQ9ITEsYS5i'
    'aW5hcnk9ITAsdD0iIixhLmNvbXByZXNzaW9uPSJTVE9SRSIsaT0ic3RyaW5n'
    'Iik7dmFyIEU9bnVsbDtFPXQgaW5zdGFuY2VvZiB1fHx0IGluc3RhbmNlb2Yg'
    'bz90OncuaXNOb2RlJiZ3LmlzU3RyZWFtKHQpP25ldyBoKGUsdCk6cy5wcmVw'
    'YXJlQ29udGVudChlLHQsYS5iaW5hcnksYS5vcHRpbWl6ZWRCaW5hcnlTdHJp'
    'bmcsYS5iYXNlNjQpO3ZhciBCPW5ldyBsKGUsRSxhKTt0aGlzLmZpbGVzW2Vd'
    'PUJ9dmFyIGk9ZSgiLi91dGY4Iikscz1lKCIuL3V0aWxzIiksbz1lKCIuL3N0'
    'cmVhbS9HZW5lcmljV29ya2VyIiksYT1lKCIuL3N0cmVhbS9TdHJlYW1IZWxw'
    'ZXIiKSxjPWUoIi4vZGVmYXVsdHMiKSx1PWUoIi4vY29tcHJlc3NlZE9iamVj'
    'dCIpLGw9ZSgiLi96aXBPYmplY3QiKSxkPWUoIi4vZ2VuZXJhdGUiKSx3PWUo'
    'Ii4vbm9kZWpzVXRpbHMiKSxoPWUoIi4vbm9kZWpzL05vZGVqc1N0cmVhbUlu'
    'cHV0QWRhcHRlciIpLGY9ZnVuY3Rpb24oZSl7Ii8iPT09ZS5zbGljZSgtMSkm'
    'JihlPWUuc3Vic3RyaW5nKDAsZS5sZW5ndGgtMSkpO3ZhciB0PWUubGFzdElu'
    'ZGV4T2YoIi8iKTtyZXR1cm4gMDx0P2Uuc3Vic3RyaW5nKDAsdCk6IiJ9LEE9'
    'ZnVuY3Rpb24oZSl7cmV0dXJuIi8iIT09ZS5zbGljZSgtMSkmJihlKz0iLyIp'
    'LGV9LHA9ZnVuY3Rpb24oZSx0KXtyZXR1cm4gdD12b2lkIDAhPT10P3Q6Yy5j'
    'cmVhdGVGb2xkZXJzLGU9QShlKSx0aGlzLmZpbGVzW2VdfHxuLmNhbGwodGhp'
    'cyxlLG51bGwse2RpcjohMCxjcmVhdGVGb2xkZXJzOnR9KSx0aGlzLmZpbGVz'
    'W2VdfTtmdW5jdGlvbiBFKGUpe3JldHVybiJbb2JqZWN0IFJlZ0V4cF0iPT09'
    'T2JqZWN0LnByb3RvdHlwZS50b1N0cmluZy5jYWxsKGUpfXZhciBCPXtsb2Fk'
    'OmZ1bmN0aW9uKCl7dGhyb3cgbmV3IEVycm9yKCJUaGlzIG1ldGhvZCBoYXMg'
    'YmVlbiByZW1vdmVkIGluIEpTWmlwIDMuMCwgcGxlYXNlIGNoZWNrIHRoZSB1'
    'cGdyYWRlIGd1aWRlLiIpfSxmb3JFYWNoOmZ1bmN0aW9uKGUpe3ZhciB0LHIs'
    'bjtmb3IodCBpbiB0aGlzLmZpbGVzKW49dGhpcy5maWxlc1t0XSwocj10LnNs'
    'aWNlKHRoaXMucm9vdC5sZW5ndGgsdC5sZW5ndGgpKSYmdC5zbGljZSgwLHRo'
    'aXMucm9vdC5sZW5ndGgpPT09dGhpcy5yb290JiZlKHIsbil9LGZpbHRlcjpm'
    'dW5jdGlvbihlKXt2YXIgdD1bXTtyZXR1cm4gdGhpcy5mb3JFYWNoKGZ1bmN0'
    'aW9uKHIsbil7ZShyLG4pJiZ0LnB1c2gobil9KSx0fSxmaWxlOmZ1bmN0aW9u'
    'KGUsdCxyKXtpZigxIT09YXJndW1lbnRzLmxlbmd0aClyZXR1cm4gZT10aGlz'
    'LnJvb3QrZSxuLmNhbGwodGhpcyxlLHQsciksdGhpcztpZihFKGUpKXt2YXIg'
    'aT1lO3JldHVybiB0aGlzLmZpbHRlcihmdW5jdGlvbihlLHQpe3JldHVybiF0'
    'LmRpciYmaS50ZXN0KGUpfSl9dmFyIHM9dGhpcy5maWxlc1t0aGlzLnJvb3Qr'
    'ZV07cmV0dXJuIHMmJiFzLmRpcj9zOm51bGx9LGZvbGRlcjpmdW5jdGlvbihl'
    'KXtpZighZSlyZXR1cm4gdGhpcztpZihFKGUpKXJldHVybiB0aGlzLmZpbHRl'
    'cihmdW5jdGlvbih0LHIpe3JldHVybiByLmRpciYmZS50ZXN0KHQpfSk7dmFy'
    'IHQ9dGhpcy5yb290K2Uscj1wLmNhbGwodGhpcyx0KSxuPXRoaXMuY2xvbmUo'
    'KTtyZXR1cm4gbi5yb290PXIubmFtZSxufSxyZW1vdmU6ZnVuY3Rpb24oZSl7'
    'ZT10aGlzLnJvb3QrZTt2YXIgdD10aGlzLmZpbGVzW2VdO2lmKHR8fCgiLyIh'
    'PT1lLnNsaWNlKC0xKSYmKGUrPSIvIiksdD10aGlzLmZpbGVzW2VdKSx0JiYh'
    'dC5kaXIpZGVsZXRlIHRoaXMuZmlsZXNbZV07ZWxzZSBmb3IodmFyIHI9dGhp'
    'cy5maWx0ZXIoZnVuY3Rpb24odCxyKXtyZXR1cm4gci5uYW1lLnNsaWNlKDAs'
    'ZS5sZW5ndGgpPT09ZX0pLG49MDtuPHIubGVuZ3RoO24rKylkZWxldGUgdGhp'
    'cy5maWxlc1tyW25dLm5hbWVdO3JldHVybiB0aGlzfSxnZW5lcmF0ZTpmdW5j'
    'dGlvbigpe3Rocm93IG5ldyBFcnJvcigiVGhpcyBtZXRob2QgaGFzIGJlZW4g'
    'cmVtb3ZlZCBpbiBKU1ppcCAzLjAsIHBsZWFzZSBjaGVjayB0aGUgdXBncmFk'
    'ZSBndWlkZS4iKX0sZ2VuZXJhdGVJbnRlcm5hbFN0cmVhbTpmdW5jdGlvbihl'
    'KXt2YXIgdCxyPXt9O3RyeXtpZigocj1zLmV4dGVuZChlfHx7fSx7c3RyZWFt'
    'RmlsZXM6ITEsY29tcHJlc3Npb246IlNUT1JFIixjb21wcmVzc2lvbk9wdGlv'
    'bnM6bnVsbCx0eXBlOiIiLHBsYXRmb3JtOiJET1MiLGNvbW1lbnQ6bnVsbCxt'
    'aW1lVHlwZToiYXBwbGljYXRpb24vemlwIixlbmNvZGVGaWxlTmFtZTppLnV0'
    'ZjhlbmNvZGV9KSkudHlwZT1yLnR5cGUudG9Mb3dlckNhc2UoKSxyLmNvbXBy'
    'ZXNzaW9uPXIuY29tcHJlc3Npb24udG9VcHBlckNhc2UoKSwiYmluYXJ5c3Ry'
    'aW5nIj09PXIudHlwZSYmKHIudHlwZT0ic3RyaW5nIiksIXIudHlwZSl0aHJv'
    'dyBuZXcgRXJyb3IoIk5vIG91dHB1dCB0eXBlIHNwZWNpZmllZC4iKTtzLmNo'
    'ZWNrU3VwcG9ydChyLnR5cGUpLCJkYXJ3aW4iIT09ci5wbGF0Zm9ybSYmImZy'
    'ZWVic2QiIT09ci5wbGF0Zm9ybSYmImxpbnV4IiE9PXIucGxhdGZvcm0mJiJz'
    'dW5vcyIhPT1yLnBsYXRmb3JtfHwoci5wbGF0Zm9ybT0iVU5JWCIpLCJ3aW4z'
    'MiI9PT1yLnBsYXRmb3JtJiYoci5wbGF0Zm9ybT0iRE9TIik7dmFyIG49ci5j'
    'b21tZW50fHx0aGlzLmNvbW1lbnR8fCIiO3Q9ZC5nZW5lcmF0ZVdvcmtlcih0'
    'aGlzLHIsbil9Y2F0Y2goZSl7KHQ9bmV3IG8oImVycm9yIikpLmVycm9yKGUp'
    'fXJldHVybiBuZXcgYSh0LHIudHlwZXx8InN0cmluZyIsci5taW1lVHlwZSl9'
    'LGdlbmVyYXRlQXN5bmM6ZnVuY3Rpb24oZSx0KXtyZXR1cm4gdGhpcy5nZW5l'
    'cmF0ZUludGVybmFsU3RyZWFtKGUpLmFjY3VtdWxhdGUodCl9LGdlbmVyYXRl'
    'Tm9kZVN0cmVhbTpmdW5jdGlvbihlLHQpe3JldHVybihlPWV8fHt9KS50eXBl'
    'fHwoZS50eXBlPSJub2RlYnVmZmVyIiksdGhpcy5nZW5lcmF0ZUludGVybmFs'
    'U3RyZWFtKGUpLnRvTm9kZWpzU3RyZWFtKHQpfX07dC5leHBvcnRzPUJ9LHsi'
    'Li9jb21wcmVzc2VkT2JqZWN0IjoyLCIuL2RlZmF1bHRzIjo1LCIuL2dlbmVy'
    'YXRlIjo5LCIuL25vZGVqcy9Ob2RlanNTdHJlYW1JbnB1dEFkYXB0ZXIiOjEy'
    'LCIuL25vZGVqc1V0aWxzIjoxNCwiLi9zdHJlYW0vR2VuZXJpY1dvcmtlciI6'
    'MjgsIi4vc3RyZWFtL1N0cmVhbUhlbHBlciI6MjksIi4vdXRmOCI6MzEsIi4v'
    'dXRpbHMiOjMyLCIuL3ppcE9iamVjdCI6MzV9XSwxNjpbZnVuY3Rpb24oZSx0'
    'LHIpe3QuZXhwb3J0cz1lKCJzdHJlYW0iKX0se3N0cmVhbTp2b2lkIDB9XSwx'
    'NzpbZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoIi4vRGF0YVJlYWRlciIpO2Z1'
    'bmN0aW9uIGkoZSl7bi5jYWxsKHRoaXMsZSk7Zm9yKHZhciB0PTA7dDx0aGlz'
    'LmRhdGEubGVuZ3RoO3QrKyllW3RdPTI1NSZlW3RdfWUoIi4uL3V0aWxzIiku'
    'aW5oZXJpdHMoaSxuKSxpLnByb3RvdHlwZS5ieXRlQXQ9ZnVuY3Rpb24oZSl7'
    'cmV0dXJuIHRoaXMuZGF0YVt0aGlzLnplcm8rZV19LGkucHJvdG90eXBlLmxh'
    'c3RJbmRleE9mU2lnbmF0dXJlPWZ1bmN0aW9uKGUpe2Zvcih2YXIgdD1lLmNo'
    'YXJDb2RlQXQoMCkscj1lLmNoYXJDb2RlQXQoMSksbj1lLmNoYXJDb2RlQXQo'
    'MiksaT1lLmNoYXJDb2RlQXQoMykscz10aGlzLmxlbmd0aC00OzA8PXM7LS1z'
    'KWlmKHRoaXMuZGF0YVtzXT09PXQmJnRoaXMuZGF0YVtzKzFdPT09ciYmdGhp'
    'cy5kYXRhW3MrMl09PT1uJiZ0aGlzLmRhdGFbcyszXT09PWkpcmV0dXJuIHMt'
    'dGhpcy56ZXJvO3JldHVybi0xfSxpLnByb3RvdHlwZS5yZWFkQW5kQ2hlY2tT'
    'aWduYXR1cmU9ZnVuY3Rpb24oZSl7dmFyIHQ9ZS5jaGFyQ29kZUF0KDApLHI9'
    'ZS5jaGFyQ29kZUF0KDEpLG49ZS5jaGFyQ29kZUF0KDIpLGk9ZS5jaGFyQ29k'
    'ZUF0KDMpLHM9dGhpcy5yZWFkRGF0YSg0KTtyZXR1cm4gdD09PXNbMF0mJnI9'
    'PT1zWzFdJiZuPT09c1syXSYmaT09PXNbM119LGkucHJvdG90eXBlLnJlYWRE'
    'YXRhPWZ1bmN0aW9uKGUpe2lmKHRoaXMuY2hlY2tPZmZzZXQoZSksMD09PWUp'
    'cmV0dXJuW107dmFyIHQ9dGhpcy5kYXRhLnNsaWNlKHRoaXMuemVybyt0aGlz'
    'LmluZGV4LHRoaXMuemVybyt0aGlzLmluZGV4K2UpO3JldHVybiB0aGlzLmlu'
    'ZGV4Kz1lLHR9LHQuZXhwb3J0cz1pfSx7Ii4uL3V0aWxzIjozMiwiLi9EYXRh'
    'UmVhZGVyIjoxOH1dLDE4OltmdW5jdGlvbihlLHQscil7dmFyIG49ZSgiLi4v'
    'dXRpbHMiKTtmdW5jdGlvbiBpKGUpe3RoaXMuZGF0YT1lLHRoaXMubGVuZ3Ro'
    'PWUubGVuZ3RoLHRoaXMuaW5kZXg9MCx0aGlzLnplcm89MH1pLnByb3RvdHlw'
    'ZT17Y2hlY2tPZmZzZXQ6ZnVuY3Rpb24oZSl7dGhpcy5jaGVja0luZGV4KHRo'
    'aXMuaW5kZXgrZSl9LGNoZWNrSW5kZXg6ZnVuY3Rpb24oZSl7aWYodGhpcy5s'
    'ZW5ndGg8dGhpcy56ZXJvK2V8fGU8MCl0aHJvdyBuZXcgRXJyb3IoIkVuZCBv'
    'ZiBkYXRhIHJlYWNoZWQgKGRhdGEgbGVuZ3RoID0gIit0aGlzLmxlbmd0aCsi'
    'LCBhc2tlZCBpbmRleCA9ICIrZSsiKS4gQ29ycnVwdGVkIHppcCA/Iil9LHNl'
    'dEluZGV4OmZ1bmN0aW9uKGUpe3RoaXMuY2hlY2tJbmRleChlKSx0aGlzLmlu'
    'ZGV4PWV9LHNraXA6ZnVuY3Rpb24oZSl7dGhpcy5zZXRJbmRleCh0aGlzLmlu'
    'ZGV4K2UpfSxieXRlQXQ6ZnVuY3Rpb24oKXt9LHJlYWRJbnQ6ZnVuY3Rpb24o'
    'ZSl7dmFyIHQscj0wO2Zvcih0aGlzLmNoZWNrT2Zmc2V0KGUpLHQ9dGhpcy5p'
    'bmRleCtlLTE7dD49dGhpcy5pbmRleDt0LS0pcj0ocjw8OCkrdGhpcy5ieXRl'
    'QXQodCk7cmV0dXJuIHRoaXMuaW5kZXgrPWUscn0scmVhZFN0cmluZzpmdW5j'
    'dGlvbihlKXtyZXR1cm4gbi50cmFuc2Zvcm1Ubygic3RyaW5nIix0aGlzLnJl'
    'YWREYXRhKGUpKX0scmVhZERhdGE6ZnVuY3Rpb24oKXt9LGxhc3RJbmRleE9m'
    'U2lnbmF0dXJlOmZ1bmN0aW9uKCl7fSxyZWFkQW5kQ2hlY2tTaWduYXR1cmU6'
    'ZnVuY3Rpb24oKXt9LHJlYWREYXRlOmZ1bmN0aW9uKCl7dmFyIGU9dGhpcy5y'
    'ZWFkSW50KDQpO3JldHVybiBuZXcgRGF0ZShEYXRlLlVUQygxOTgwKyhlPj4y'
    'NSYxMjcpLChlPj4yMSYxNSktMSxlPj4xNiYzMSxlPj4xMSYzMSxlPj41JjYz'
    'LCgzMSZlKTw8MSkpfX0sdC5leHBvcnRzPWl9LHsiLi4vdXRpbHMiOjMyfV0s'
    'MTk6W2Z1bmN0aW9uKGUsdCxyKXt2YXIgbj1lKCIuL1VpbnQ4QXJyYXlSZWFk'
    'ZXIiKTtmdW5jdGlvbiBpKGUpe24uY2FsbCh0aGlzLGUpfWUoIi4uL3V0aWxz'
    'IikuaW5oZXJpdHMoaSxuKSxpLnByb3RvdHlwZS5yZWFkRGF0YT1mdW5jdGlv'
    'bihlKXt0aGlzLmNoZWNrT2Zmc2V0KGUpO3ZhciB0PXRoaXMuZGF0YS5zbGlj'
    'ZSh0aGlzLnplcm8rdGhpcy5pbmRleCx0aGlzLnplcm8rdGhpcy5pbmRleCtl'
    'KTtyZXR1cm4gdGhpcy5pbmRleCs9ZSx0fSx0LmV4cG9ydHM9aX0seyIuLi91'
    'dGlscyI6MzIsIi4vVWludDhBcnJheVJlYWRlciI6MjF9XSwyMDpbZnVuY3Rp'
    'b24oZSx0LHIpe3ZhciBuPWUoIi4vRGF0YVJlYWRlciIpO2Z1bmN0aW9uIGko'
    'ZSl7bi5jYWxsKHRoaXMsZSl9ZSgiLi4vdXRpbHMiKS5pbmhlcml0cyhpLG4p'
    'LGkucHJvdG90eXBlLmJ5dGVBdD1mdW5jdGlvbihlKXtyZXR1cm4gdGhpcy5k'
    'YXRhLmNoYXJDb2RlQXQodGhpcy56ZXJvK2UpfSxpLnByb3RvdHlwZS5sYXN0'
    'SW5kZXhPZlNpZ25hdHVyZT1mdW5jdGlvbihlKXtyZXR1cm4gdGhpcy5kYXRh'
    'Lmxhc3RJbmRleE9mKGUpLXRoaXMuemVyb30saS5wcm90b3R5cGUucmVhZEFu'
    'ZENoZWNrU2lnbmF0dXJlPWZ1bmN0aW9uKGUpe3JldHVybiBlPT09dGhpcy5y'
    'ZWFkRGF0YSg0KX0saS5wcm90b3R5cGUucmVhZERhdGE9ZnVuY3Rpb24oZSl7'
    'dGhpcy5jaGVja09mZnNldChlKTt2YXIgdD10aGlzLmRhdGEuc2xpY2UodGhp'
    'cy56ZXJvK3RoaXMuaW5kZXgsdGhpcy56ZXJvK3RoaXMuaW5kZXgrZSk7cmV0'
    'dXJuIHRoaXMuaW5kZXgrPWUsdH0sdC5leHBvcnRzPWl9LHsiLi4vdXRpbHMi'
    'OjMyLCIuL0RhdGFSZWFkZXIiOjE4fV0sMjE6W2Z1bmN0aW9uKGUsdCxyKXt2'
    'YXIgbj1lKCIuL0FycmF5UmVhZGVyIik7ZnVuY3Rpb24gaShlKXtuLmNhbGwo'
    'dGhpcyxlKX1lKCIuLi91dGlscyIpLmluaGVyaXRzKGksbiksaS5wcm90b3R5'
    'cGUucmVhZERhdGE9ZnVuY3Rpb24oZSl7aWYodGhpcy5jaGVja09mZnNldChl'
    'KSwwPT09ZSlyZXR1cm4gbmV3IFVpbnQ4QXJyYXkoMCk7dmFyIHQ9dGhpcy5k'
    'YXRhLnN1YmFycmF5KHRoaXMuemVybyt0aGlzLmluZGV4LHRoaXMuemVybyt0'
    'aGlzLmluZGV4K2UpO3JldHVybiB0aGlzLmluZGV4Kz1lLHR9LHQuZXhwb3J0'
    'cz1pfSx7Ii4uL3V0aWxzIjozMiwiLi9BcnJheVJlYWRlciI6MTd9XSwyMjpb'
    'ZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoIi4uL3V0aWxzIiksaT1lKCIuLi9z'
    'dXBwb3J0Iikscz1lKCIuL0FycmF5UmVhZGVyIiksbz1lKCIuL1N0cmluZ1Jl'
    'YWRlciIpLGE9ZSgiLi9Ob2RlQnVmZmVyUmVhZGVyIiksYz1lKCIuL1VpbnQ4'
    'QXJyYXlSZWFkZXIiKTt0LmV4cG9ydHM9ZnVuY3Rpb24oZSl7dmFyIHQ9bi5n'
    'ZXRUeXBlT2YoZSk7cmV0dXJuIG4uY2hlY2tTdXBwb3J0KHQpLCJzdHJpbmci'
    'IT09dHx8aS51aW50OGFycmF5PyJub2RlYnVmZmVyIj09PXQ/bmV3IGEoZSk6'
    'aS51aW50OGFycmF5P25ldyBjKG4udHJhbnNmb3JtVG8oInVpbnQ4YXJyYXki'
    'LGUpKTpuZXcgcyhuLnRyYW5zZm9ybVRvKCJhcnJheSIsZSkpOm5ldyBvKGUp'
    'fX0seyIuLi9zdXBwb3J0IjozMCwiLi4vdXRpbHMiOjMyLCIuL0FycmF5UmVh'
    'ZGVyIjoxNywiLi9Ob2RlQnVmZmVyUmVhZGVyIjoxOSwiLi9TdHJpbmdSZWFk'
    'ZXIiOjIwLCIuL1VpbnQ4QXJyYXlSZWFkZXIiOjIxfV0sMjM6W2Z1bmN0aW9u'
    'KGUsdCxyKXtyLkxPQ0FMX0ZJTEVfSEVBREVSPSJQSwMEIixyLkNFTlRSQUxf'
    'RklMRV9IRUFERVI9IlBLAQIiLHIuQ0VOVFJBTF9ESVJFQ1RPUllfRU5EPSJQ'
    'SwUGIixyLlpJUDY0X0NFTlRSQUxfRElSRUNUT1JZX0xPQ0FUT1I9IlBLBgci'
    'LHIuWklQNjRfQ0VOVFJBTF9ESVJFQ1RPUllfRU5EPSJQSwYGIixyLkRBVEFf'
    'REVTQ1JJUFRPUj0iUEsHXGIifSx7fV0sMjQ6W2Z1bmN0aW9uKGUsdCxyKXt2'
    'YXIgbj1lKCIuL0dlbmVyaWNXb3JrZXIiKSxpPWUoIi4uL3V0aWxzIik7ZnVu'
    'Y3Rpb24gcyhlKXtuLmNhbGwodGhpcywiQ29udmVydFdvcmtlciB0byAiK2Up'
    'LHRoaXMuZGVzdFR5cGU9ZX1pLmluaGVyaXRzKHMsbikscy5wcm90b3R5cGUu'
    'cHJvY2Vzc0NodW5rPWZ1bmN0aW9uKGUpe3RoaXMucHVzaCh7ZGF0YTppLnRy'
    'YW5zZm9ybVRvKHRoaXMuZGVzdFR5cGUsZS5kYXRhKSxtZXRhOmUubWV0YX0p'
    'fSx0LmV4cG9ydHM9c30seyIuLi91dGlscyI6MzIsIi4vR2VuZXJpY1dvcmtl'
    'ciI6Mjh9XSwyNTpbZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoIi4vR2VuZXJp'
    'Y1dvcmtlciIpLGk9ZSgiLi4vY3JjMzIiKTtmdW5jdGlvbiBzKCl7bi5jYWxs'
    'KHRoaXMsIkNyYzMyUHJvYmUiKSx0aGlzLndpdGhTdHJlYW1JbmZvKCJjcmMz'
    'MiIsMCl9ZSgiLi4vdXRpbHMiKS5pbmhlcml0cyhzLG4pLHMucHJvdG90eXBl'
    'LnByb2Nlc3NDaHVuaz1mdW5jdGlvbihlKXt0aGlzLnN0cmVhbUluZm8uY3Jj'
    'MzI9aShlLmRhdGEsdGhpcy5zdHJlYW1JbmZvLmNyYzMyfHwwKSx0aGlzLnB1'
    'c2goZSl9LHQuZXhwb3J0cz1zfSx7Ii4uL2NyYzMyIjo0LCIuLi91dGlscyI6'
    'MzIsIi4vR2VuZXJpY1dvcmtlciI6Mjh9XSwyNjpbZnVuY3Rpb24oZSx0LHIp'
    'e3ZhciBuPWUoIi4uL3V0aWxzIiksaT1lKCIuL0dlbmVyaWNXb3JrZXIiKTtm'
    'dW5jdGlvbiBzKGUpe2kuY2FsbCh0aGlzLCJEYXRhTGVuZ3RoUHJvYmUgZm9y'
    'ICIrZSksdGhpcy5wcm9wTmFtZT1lLHRoaXMud2l0aFN0cmVhbUluZm8oZSww'
    'KX1uLmluaGVyaXRzKHMsaSkscy5wcm90b3R5cGUucHJvY2Vzc0NodW5rPWZ1'
    'bmN0aW9uKGUpe2lmKGUpe3ZhciB0PXRoaXMuc3RyZWFtSW5mb1t0aGlzLnBy'
    'b3BOYW1lXXx8MDt0aGlzLnN0cmVhbUluZm9bdGhpcy5wcm9wTmFtZV09dCtl'
    'LmRhdGEubGVuZ3RofWkucHJvdG90eXBlLnByb2Nlc3NDaHVuay5jYWxsKHRo'
    'aXMsZSl9LHQuZXhwb3J0cz1zfSx7Ii4uL3V0aWxzIjozMiwiLi9HZW5lcmlj'
    'V29ya2VyIjoyOH1dLDI3OltmdW5jdGlvbihlLHQscil7dmFyIG49ZSgiLi4v'
    'dXRpbHMiKSxpPWUoIi4vR2VuZXJpY1dvcmtlciIpO2Z1bmN0aW9uIHMoZSl7'
    'aS5jYWxsKHRoaXMsIkRhdGFXb3JrZXIiKTt2YXIgdD10aGlzO3RoaXMuZGF0'
    'YUlzUmVhZHk9ITEsdGhpcy5pbmRleD0wLHRoaXMubWF4PTAsdGhpcy5kYXRh'
    'PW51bGwsdGhpcy50eXBlPSIiLHRoaXMuX3RpY2tTY2hlZHVsZWQ9ITEsZS50'
    'aGVuKGZ1bmN0aW9uKGUpe3QuZGF0YUlzUmVhZHk9ITAsdC5kYXRhPWUsdC5t'
    'YXg9ZSYmZS5sZW5ndGh8fDAsdC50eXBlPW4uZ2V0VHlwZU9mKGUpLHQuaXNQ'
    'YXVzZWR8fHQuX3RpY2tBbmRSZXBlYXQoKX0sZnVuY3Rpb24oZSl7dC5lcnJv'
    'cihlKX0pfW4uaW5oZXJpdHMocyxpKSxzLnByb3RvdHlwZS5jbGVhblVwPWZ1'
    'bmN0aW9uKCl7aS5wcm90b3R5cGUuY2xlYW5VcC5jYWxsKHRoaXMpLHRoaXMu'
    'ZGF0YT1udWxsfSxzLnByb3RvdHlwZS5yZXN1bWU9ZnVuY3Rpb24oKXtyZXR1'
    'cm4hIWkucHJvdG90eXBlLnJlc3VtZS5jYWxsKHRoaXMpJiYoIXRoaXMuX3Rp'
    'Y2tTY2hlZHVsZWQmJnRoaXMuZGF0YUlzUmVhZHkmJih0aGlzLl90aWNrU2No'
    'ZWR1bGVkPSEwLG4uZGVsYXkodGhpcy5fdGlja0FuZFJlcGVhdCxbXSx0aGlz'
    'KSksITApfSxzLnByb3RvdHlwZS5fdGlja0FuZFJlcGVhdD1mdW5jdGlvbigp'
    'e3RoaXMuX3RpY2tTY2hlZHVsZWQ9ITEsdGhpcy5pc1BhdXNlZHx8dGhpcy5p'
    'c0ZpbmlzaGVkfHwodGhpcy5fdGljaygpLHRoaXMuaXNGaW5pc2hlZHx8KG4u'
    'ZGVsYXkodGhpcy5fdGlja0FuZFJlcGVhdCxbXSx0aGlzKSx0aGlzLl90aWNr'
    'U2NoZWR1bGVkPSEwKSl9LHMucHJvdG90eXBlLl90aWNrPWZ1bmN0aW9uKCl7'
    'aWYodGhpcy5pc1BhdXNlZHx8dGhpcy5pc0ZpbmlzaGVkKXJldHVybiExO3Zh'
    'ciBlPW51bGwsdD1NYXRoLm1pbih0aGlzLm1heCx0aGlzLmluZGV4KzE2Mzg0'
    'KTtpZih0aGlzLmluZGV4Pj10aGlzLm1heClyZXR1cm4gdGhpcy5lbmQoKTtz'
    'd2l0Y2godGhpcy50eXBlKXtjYXNlInN0cmluZyI6ZT10aGlzLmRhdGEuc3Vi'
    'c3RyaW5nKHRoaXMuaW5kZXgsdCk7YnJlYWs7Y2FzZSJ1aW50OGFycmF5Ijpl'
    'PXRoaXMuZGF0YS5zdWJhcnJheSh0aGlzLmluZGV4LHQpO2JyZWFrO2Nhc2Ui'
    'YXJyYXkiOmNhc2Uibm9kZWJ1ZmZlciI6ZT10aGlzLmRhdGEuc2xpY2UodGhp'
    'cy5pbmRleCx0KX1yZXR1cm4gdGhpcy5pbmRleD10LHRoaXMucHVzaCh7ZGF0'
    'YTplLG1ldGE6e3BlcmNlbnQ6dGhpcy5tYXg/dGhpcy5pbmRleC90aGlzLm1h'
    'eCoxMDA6MH19KX0sdC5leHBvcnRzPXN9LHsiLi4vdXRpbHMiOjMyLCIuL0dl'
    'bmVyaWNXb3JrZXIiOjI4fV0sMjg6W2Z1bmN0aW9uKGUsdCxyKXtmdW5jdGlv'
    'biBuKGUpe3RoaXMubmFtZT1lfHwiZGVmYXVsdCIsdGhpcy5zdHJlYW1JbmZv'
    'PXt9LHRoaXMuZ2VuZXJhdGVkRXJyb3I9bnVsbCx0aGlzLmV4dHJhU3RyZWFt'
    'SW5mbz17fSx0aGlzLmlzUGF1c2VkPSEwLHRoaXMuaXNGaW5pc2hlZD0hMSx0'
    'aGlzLmlzTG9ja2VkPSExLHRoaXMuX2xpc3RlbmVycz17ZGF0YTpbXSxlbmQ6'
    'W10sZXJyb3I6W119LHRoaXMucHJldmlvdXM9bnVsbH1uLnByb3RvdHlwZT17'
    'cHVzaDpmdW5jdGlvbihlKXt0aGlzLmVtaXQoImRhdGEiLGUpfSxlbmQ6ZnVu'
    'Y3Rpb24oKXtpZih0aGlzLmlzRmluaXNoZWQpcmV0dXJuITE7dGhpcy5mbHVz'
    'aCgpO3RyeXt0aGlzLmVtaXQoImVuZCIpLHRoaXMuY2xlYW5VcCgpLHRoaXMu'
    'aXNGaW5pc2hlZD0hMH1jYXRjaChlKXt0aGlzLmVtaXQoImVycm9yIixlKX1y'
    'ZXR1cm4hMH0sZXJyb3I6ZnVuY3Rpb24oZSl7cmV0dXJuIXRoaXMuaXNGaW5p'
    'c2hlZCYmKHRoaXMuaXNQYXVzZWQ/dGhpcy5nZW5lcmF0ZWRFcnJvcj1lOih0'
    'aGlzLmlzRmluaXNoZWQ9ITAsdGhpcy5lbWl0KCJlcnJvciIsZSksdGhpcy5w'
    'cmV2aW91cyYmdGhpcy5wcmV2aW91cy5lcnJvcihlKSx0aGlzLmNsZWFuVXAo'
    'KSksITApfSxvbjpmdW5jdGlvbihlLHQpe3JldHVybiB0aGlzLl9saXN0ZW5l'
    'cnNbZV0ucHVzaCh0KSx0aGlzfSxjbGVhblVwOmZ1bmN0aW9uKCl7dGhpcy5z'
    'dHJlYW1JbmZvPXRoaXMuZ2VuZXJhdGVkRXJyb3I9dGhpcy5leHRyYVN0cmVh'
    'bUluZm89bnVsbCx0aGlzLl9saXN0ZW5lcnM9W119LGVtaXQ6ZnVuY3Rpb24o'
    'ZSx0KXtpZih0aGlzLl9saXN0ZW5lcnNbZV0pZm9yKHZhciByPTA7cjx0aGlz'
    'Ll9saXN0ZW5lcnNbZV0ubGVuZ3RoO3IrKyl0aGlzLl9saXN0ZW5lcnNbZV1b'
    'cl0uY2FsbCh0aGlzLHQpfSxwaXBlOmZ1bmN0aW9uKGUpe3JldHVybiBlLnJl'
    'Z2lzdGVyUHJldmlvdXModGhpcyl9LHJlZ2lzdGVyUHJldmlvdXM6ZnVuY3Rp'
    'b24oZSl7aWYodGhpcy5pc0xvY2tlZCl0aHJvdyBuZXcgRXJyb3IoIlRoZSBz'
    'dHJlYW0gJyIrdGhpcysiJyBoYXMgYWxyZWFkeSBiZWVuIHVzZWQuIik7dGhp'
    'cy5zdHJlYW1JbmZvPWUuc3RyZWFtSW5mbyx0aGlzLm1lcmdlU3RyZWFtSW5m'
    'bygpLHRoaXMucHJldmlvdXM9ZTt2YXIgdD10aGlzO3JldHVybiBlLm9uKCJk'
    'YXRhIixmdW5jdGlvbihlKXt0LnByb2Nlc3NDaHVuayhlKX0pLGUub24oImVu'
    'ZCIsZnVuY3Rpb24oKXt0LmVuZCgpfSksZS5vbigiZXJyb3IiLGZ1bmN0aW9u'
    'KGUpe3QuZXJyb3IoZSl9KSx0aGlzfSxwYXVzZTpmdW5jdGlvbigpe3JldHVy'
    'biF0aGlzLmlzUGF1c2VkJiYhdGhpcy5pc0ZpbmlzaGVkJiYodGhpcy5pc1Bh'
    'dXNlZD0hMCx0aGlzLnByZXZpb3VzJiZ0aGlzLnByZXZpb3VzLnBhdXNlKCks'
    'ITApfSxyZXN1bWU6ZnVuY3Rpb24oKXtpZighdGhpcy5pc1BhdXNlZHx8dGhp'
    'cy5pc0ZpbmlzaGVkKXJldHVybiExO3ZhciBlPXRoaXMuaXNQYXVzZWQ9ITE7'
    'cmV0dXJuIHRoaXMuZ2VuZXJhdGVkRXJyb3ImJih0aGlzLmVycm9yKHRoaXMu'
    'Z2VuZXJhdGVkRXJyb3IpLGU9ITApLHRoaXMucHJldmlvdXMmJnRoaXMucHJl'
    'dmlvdXMucmVzdW1lKCksIWV9LGZsdXNoOmZ1bmN0aW9uKCl7fSxwcm9jZXNz'
    'Q2h1bms6ZnVuY3Rpb24oZSl7dGhpcy5wdXNoKGUpfSx3aXRoU3RyZWFtSW5m'
    'bzpmdW5jdGlvbihlLHQpe3JldHVybiB0aGlzLmV4dHJhU3RyZWFtSW5mb1tl'
    'XT10LHRoaXMubWVyZ2VTdHJlYW1JbmZvKCksdGhpc30sbWVyZ2VTdHJlYW1J'
    'bmZvOmZ1bmN0aW9uKCl7Zm9yKHZhciBlIGluIHRoaXMuZXh0cmFTdHJlYW1J'
    'bmZvKU9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbCh0aGlz'
    'LmV4dHJhU3RyZWFtSW5mbyxlKSYmKHRoaXMuc3RyZWFtSW5mb1tlXT10aGlz'
    'LmV4dHJhU3RyZWFtSW5mb1tlXSl9LGxvY2s6ZnVuY3Rpb24oKXtpZih0aGlz'
    'LmlzTG9ja2VkKXRocm93IG5ldyBFcnJvcigiVGhlIHN0cmVhbSAnIit0aGlz'
    'KyInIGhhcyBhbHJlYWR5IGJlZW4gdXNlZC4iKTt0aGlzLmlzTG9ja2VkPSEw'
    'LHRoaXMucHJldmlvdXMmJnRoaXMucHJldmlvdXMubG9jaygpfSx0b1N0cmlu'
    'ZzpmdW5jdGlvbigpe3ZhciBlPSJXb3JrZXIgIit0aGlzLm5hbWU7cmV0dXJu'
    'IHRoaXMucHJldmlvdXM/dGhpcy5wcmV2aW91cysiIC0+ICIrZTplfX0sdC5l'
    'eHBvcnRzPW59LHt9XSwyOTpbZnVuY3Rpb24oZSx0LHIpe3ZhciBuPWUoIi4u'
    'L3V0aWxzIiksaT1lKCIuL0NvbnZlcnRXb3JrZXIiKSxzPWUoIi4vR2VuZXJp'
    'Y1dvcmtlciIpLG89ZSgiLi4vYmFzZTY0IiksYT1lKCIuLi9zdXBwb3J0Iiks'
    'Yz1lKCIuLi9leHRlcm5hbCIpLHU9bnVsbDtpZihhLm5vZGVzdHJlYW0pdHJ5'
    'e3U9ZSgiLi4vbm9kZWpzL05vZGVqc1N0cmVhbU91dHB1dEFkYXB0ZXIiKX1j'
    'YXRjaChlKXt9ZnVuY3Rpb24gbChlLHQpe3JldHVybiBuZXcgYy5Qcm9taXNl'
    'KGZ1bmN0aW9uKHIsaSl7dmFyIHM9W10sYT1lLl9pbnRlcm5hbFR5cGUsYz1l'
    'Ll9vdXRwdXRUeXBlLHU9ZS5fbWltZVR5cGU7ZS5vbigiZGF0YSIsZnVuY3Rp'
    'b24oZSxyKXtzLnB1c2goZSksdCYmdChyKX0pLm9uKCJlcnJvciIsZnVuY3Rp'
    'b24oZSl7cz1bXSxpKGUpfSkub24oImVuZCIsZnVuY3Rpb24oKXt0cnl7dmFy'
    'IGU9ZnVuY3Rpb24oZSx0LHIpe3N3aXRjaChlKXtjYXNlImJsb2IiOnJldHVy'
    'biBuLm5ld0Jsb2Iobi50cmFuc2Zvcm1UbygiYXJyYXlidWZmZXIiLHQpLHIp'
    'O2Nhc2UiYmFzZTY0IjpyZXR1cm4gby5lbmNvZGUodCk7ZGVmYXVsdDpyZXR1'
    'cm4gbi50cmFuc2Zvcm1UbyhlLHQpfX0oYyxmdW5jdGlvbihlLHQpe3ZhciBy'
    'LG49MCxpPW51bGwscz0wO2ZvcihyPTA7cjx0Lmxlbmd0aDtyKyspcys9dFty'
    'XS5sZW5ndGg7c3dpdGNoKGUpe2Nhc2Uic3RyaW5nIjpyZXR1cm4gdC5qb2lu'
    'KCIiKTtjYXNlImFycmF5IjpyZXR1cm4gQXJyYXkucHJvdG90eXBlLmNvbmNh'
    'dC5hcHBseShbXSx0KTtjYXNlInVpbnQ4YXJyYXkiOmZvcihpPW5ldyBVaW50'
    'OEFycmF5KHMpLHI9MDtyPHQubGVuZ3RoO3IrKylpLnNldCh0W3JdLG4pLG4r'
    'PXRbcl0ubGVuZ3RoO3JldHVybiBpO2Nhc2Uibm9kZWJ1ZmZlciI6cmV0dXJu'
    'IEJ1ZmZlci5jb25jYXQodCk7ZGVmYXVsdDp0aHJvdyBuZXcgRXJyb3IoImNv'
    'bmNhdCA6IHVuc3VwcG9ydGVkIHR5cGUgJyIrZSsiJyIpfX0oYSxzKSx1KTty'
    'KGUpfWNhdGNoKGUpe2koZSl9cz1bXX0pLnJlc3VtZSgpfSl9ZnVuY3Rpb24g'
    'ZChlLHQscil7dmFyIG89dDtzd2l0Y2godCl7Y2FzZSJibG9iIjpjYXNlImFy'
    'cmF5YnVmZmVyIjpvPSJ1aW50OGFycmF5IjticmVhaztjYXNlImJhc2U2NCI6'
    'bz0ic3RyaW5nIn10cnl7dGhpcy5faW50ZXJuYWxUeXBlPW8sdGhpcy5fb3V0'
    'cHV0VHlwZT10LHRoaXMuX21pbWVUeXBlPXIsbi5jaGVja1N1cHBvcnQobyks'
    'dGhpcy5fd29ya2VyPWUucGlwZShuZXcgaShvKSksZS5sb2NrKCl9Y2F0Y2go'
    'ZSl7dGhpcy5fd29ya2VyPW5ldyBzKCJlcnJvciIpLHRoaXMuX3dvcmtlci5l'
    'cnJvcihlKX19ZC5wcm90b3R5cGU9e2FjY3VtdWxhdGU6ZnVuY3Rpb24oZSl7'
    'cmV0dXJuIGwodGhpcyxlKX0sb246ZnVuY3Rpb24oZSx0KXt2YXIgcj10aGlz'
    'O3JldHVybiJkYXRhIj09PWU/dGhpcy5fd29ya2VyLm9uKGUsZnVuY3Rpb24o'
    'ZSl7dC5jYWxsKHIsZS5kYXRhLGUubWV0YSl9KTp0aGlzLl93b3JrZXIub24o'
    'ZSxmdW5jdGlvbigpe24uZGVsYXkodCxhcmd1bWVudHMscil9KSx0aGlzfSxy'
    'ZXN1bWU6ZnVuY3Rpb24oKXtyZXR1cm4gbi5kZWxheSh0aGlzLl93b3JrZXIu'
    'cmVzdW1lLFtdLHRoaXMuX3dvcmtlciksdGhpc30scGF1c2U6ZnVuY3Rpb24o'
    'KXtyZXR1cm4gdGhpcy5fd29ya2VyLnBhdXNlKCksdGhpc30sdG9Ob2RlanNT'
    'dHJlYW06ZnVuY3Rpb24oZSl7aWYobi5jaGVja1N1cHBvcnQoIm5vZGVzdHJl'
    'YW0iKSwibm9kZWJ1ZmZlciIhPT10aGlzLl9vdXRwdXRUeXBlKXRocm93IG5l'
    'dyBFcnJvcih0aGlzLl9vdXRwdXRUeXBlKyIgaXMgbm90IHN1cHBvcnRlZCBi'
    'eSB0aGlzIG1ldGhvZCIpO3JldHVybiBuZXcgdSh0aGlzLHtvYmplY3RNb2Rl'
    'OiJub2RlYnVmZmVyIiE9PXRoaXMuX291dHB1dFR5cGV9LGUpfX0sdC5leHBv'
    'cnRzPWR9LHsiLi4vYmFzZTY0IjoxLCIuLi9leHRlcm5hbCI6NiwiLi4vbm9k'
    'ZWpzL05vZGVqc1N0cmVhbU91dHB1dEFkYXB0ZXIiOjEzLCIuLi9zdXBwb3J0'
    'IjozMCwiLi4vdXRpbHMiOjMyLCIuL0NvbnZlcnRXb3JrZXIiOjI0LCIuL0dl'
    'bmVyaWNXb3JrZXIiOjI4fV0sMzA6W2Z1bmN0aW9uKGUsdCxyKXtpZihyLmJh'
    'c2U2ND0hMCxyLmFycmF5PSEwLHIuc3RyaW5nPSEwLHIuYXJyYXlidWZmZXI9'
    'InVuZGVmaW5lZCIhPXR5cGVvZiBBcnJheUJ1ZmZlciYmInVuZGVmaW5lZCIh'
    'PXR5cGVvZiBVaW50OEFycmF5LHIubm9kZWJ1ZmZlcj0idW5kZWZpbmVkIiE9'
    'dHlwZW9mIEJ1ZmZlcixyLnVpbnQ4YXJyYXk9InVuZGVmaW5lZCIhPXR5cGVv'
    'ZiBVaW50OEFycmF5LCJ1bmRlZmluZWQiPT10eXBlb2YgQXJyYXlCdWZmZXIp'
    'ci5ibG9iPSExO2Vsc2V7dmFyIG49bmV3IEFycmF5QnVmZmVyKDApO3RyeXty'
    'LmJsb2I9MD09PW5ldyBCbG9iKFtuXSx7dHlwZToiYXBwbGljYXRpb24vemlw'
    'In0pLnNpemV9Y2F0Y2goZSl7dHJ5e3ZhciBpPW5ldyhzZWxmLkJsb2JCdWls'
    'ZGVyfHxzZWxmLldlYktpdEJsb2JCdWlsZGVyfHxzZWxmLk1vekJsb2JCdWls'
    'ZGVyfHxzZWxmLk1TQmxvYkJ1aWxkZXIpO2kuYXBwZW5kKG4pLHIuYmxvYj0w'
    'PT09aS5nZXRCbG9iKCJhcHBsaWNhdGlvbi96aXAiKS5zaXplfWNhdGNoKGUp'
    'e3IuYmxvYj0hMX19fXRyeXtyLm5vZGVzdHJlYW09ISFlKCJyZWFkYWJsZS1z'
    'dHJlYW0iKS5SZWFkYWJsZX1jYXRjaChlKXtyLm5vZGVzdHJlYW09ITF9fSx7'
    'InJlYWRhYmxlLXN0cmVhbSI6MTZ9XSwzMTpbZnVuY3Rpb24oZSx0LHIpe2Zv'
    'cih2YXIgbj1lKCIuL3V0aWxzIiksaT1lKCIuL3N1cHBvcnQiKSxzPWUoIi4v'
    'bm9kZWpzVXRpbHMiKSxvPWUoIi4vc3RyZWFtL0dlbmVyaWNXb3JrZXIiKSxh'
    'PW5ldyBBcnJheSgyNTYpLGM9MDtjPDI1NjtjKyspYVtjXT0yNTI8PWM/Njoy'
    'NDg8PWM/NToyNDA8PWM/NDoyMjQ8PWM/MzoxOTI8PWM/MjoxO2Z1bmN0aW9u'
    'IHUoKXtvLmNhbGwodGhpcywidXRmLTggZGVjb2RlIiksdGhpcy5sZWZ0T3Zl'
    'cj1udWxsfWZ1bmN0aW9uIGwoKXtvLmNhbGwodGhpcywidXRmLTggZW5jb2Rl'
    'Iil9YVsyNTRdPWFbMjU0XT0xLHIudXRmOGVuY29kZT1mdW5jdGlvbihlKXty'
    'ZXR1cm4gaS5ub2RlYnVmZmVyP3MubmV3QnVmZmVyRnJvbShlLCJ1dGYtOCIp'
    'OmZ1bmN0aW9uKGUpe3ZhciB0LHIsbixzLG8sYT1lLmxlbmd0aCxjPTA7Zm9y'
    'KHM9MDtzPGE7cysrKTU1Mjk2PT0oNjQ1MTImKHI9ZS5jaGFyQ29kZUF0KHMp'
    'KSkmJnMrMTxhJiY1NjMyMD09KDY0NTEyJihuPWUuY2hhckNvZGVBdChzKzEp'
    'KSkmJihyPTY1NTM2KyhyLTU1Mjk2PDwxMCkrKG4tNTYzMjApLHMrKyksYys9'
    'cjwxMjg/MTpyPDIwNDg/MjpyPDY1NTM2PzM6NDtmb3IodD1pLnVpbnQ4YXJy'
    'YXk/bmV3IFVpbnQ4QXJyYXkoYyk6bmV3IEFycmF5KGMpLHM9bz0wO288Yztz'
    'KyspNTUyOTY9PSg2NDUxMiYocj1lLmNoYXJDb2RlQXQocykpKSYmcysxPGEm'
    'JjU2MzIwPT0oNjQ1MTImKG49ZS5jaGFyQ29kZUF0KHMrMSkpKSYmKHI9NjU1'
    'MzYrKHItNTUyOTY8PDEwKSsobi01NjMyMCkscysrKSxyPDEyOD90W28rK109'
    'cjoocjwyMDQ4P3RbbysrXT0xOTJ8cj4+PjY6KHI8NjU1MzY/dFtvKytdPTIy'
    'NHxyPj4+MTI6KHRbbysrXT0yNDB8cj4+PjE4LHRbbysrXT0xMjh8cj4+PjEy'
    'JjYzKSx0W28rK109MTI4fHI+Pj42JjYzKSx0W28rK109MTI4fDYzJnIpO3Jl'
    'dHVybiB0fShlKX0sci51dGY4ZGVjb2RlPWZ1bmN0aW9uKGUpe3JldHVybiBp'
    'Lm5vZGVidWZmZXI/bi50cmFuc2Zvcm1Ubygibm9kZWJ1ZmZlciIsZSkudG9T'
    'dHJpbmcoInV0Zi04Iik6ZnVuY3Rpb24oZSl7dmFyIHQscixpLHMsbz1lLmxl'
    'bmd0aCxjPW5ldyBBcnJheSgyKm8pO2Zvcih0PXI9MDt0PG87KWlmKChpPWVb'
    'dCsrXSk8MTI4KWNbcisrXT1pO2Vsc2UgaWYoNDwocz1hW2ldKSljW3IrK109'
    'NjU1MzMsdCs9cy0xO2Vsc2V7Zm9yKGkmPTI9PT1zPzMxOjM9PT1zPzE1Ojc7'
    'MTxzJiZ0PG87KWk9aTw8Nnw2MyZlW3QrK10scy0tOzE8cz9jW3IrK109NjU1'
    'MzM6aTw2NTUzNj9jW3IrK109aTooaS09NjU1MzYsY1tyKytdPTU1Mjk2fGk+'
    'PjEwJjEwMjMsY1tyKytdPTU2MzIwfDEwMjMmaSl9cmV0dXJuIGMubGVuZ3Ro'
    'IT09ciYmKGMuc3ViYXJyYXk/Yz1jLnN1YmFycmF5KDAscik6Yy5sZW5ndGg9'
    'ciksbi5hcHBseUZyb21DaGFyQ29kZShjKX0oZT1uLnRyYW5zZm9ybVRvKGku'
    'dWludDhhcnJheT8idWludDhhcnJheSI6ImFycmF5IixlKSl9LG4uaW5oZXJp'
    'dHModSxvKSx1LnByb3RvdHlwZS5wcm9jZXNzQ2h1bms9ZnVuY3Rpb24oZSl7'
    'dmFyIHQ9bi50cmFuc2Zvcm1UbyhpLnVpbnQ4YXJyYXk/InVpbnQ4YXJyYXki'
    'OiJhcnJheSIsZS5kYXRhKTtpZih0aGlzLmxlZnRPdmVyJiZ0aGlzLmxlZnRP'
    'dmVyLmxlbmd0aCl7aWYoaS51aW50OGFycmF5KXt2YXIgcz10Oyh0PW5ldyBV'
    'aW50OEFycmF5KHMubGVuZ3RoK3RoaXMubGVmdE92ZXIubGVuZ3RoKSkuc2V0'
    'KHRoaXMubGVmdE92ZXIsMCksdC5zZXQocyx0aGlzLmxlZnRPdmVyLmxlbmd0'
    'aCl9ZWxzZSB0PXRoaXMubGVmdE92ZXIuY29uY2F0KHQpO3RoaXMubGVmdE92'
    'ZXI9bnVsbH12YXIgbz1mdW5jdGlvbihlLHQpe3ZhciByO2ZvcigodD10fHxl'
    'Lmxlbmd0aCk+ZS5sZW5ndGgmJih0PWUubGVuZ3RoKSxyPXQtMTswPD1yJiYx'
    'Mjg9PSgxOTImZVtyXSk7KXItLTtyZXR1cm4gcjwwfHwwPT09cj90OnIrYVtl'
    'W3JdXT50P3I6dH0odCksYz10O28hPT10Lmxlbmd0aCYmKGkudWludDhhcnJh'
    'eT8oYz10LnN1YmFycmF5KDAsbyksdGhpcy5sZWZ0T3Zlcj10LnN1YmFycmF5'
    'KG8sdC5sZW5ndGgpKTooYz10LnNsaWNlKDAsbyksdGhpcy5sZWZ0T3Zlcj10'
    'LnNsaWNlKG8sdC5sZW5ndGgpKSksdGhpcy5wdXNoKHtkYXRhOnIudXRmOGRl'
    'Y29kZShjKSxtZXRhOmUubWV0YX0pfSx1LnByb3RvdHlwZS5mbHVzaD1mdW5j'
    'dGlvbigpe3RoaXMubGVmdE92ZXImJnRoaXMubGVmdE92ZXIubGVuZ3RoJiYo'
    'dGhpcy5wdXNoKHtkYXRhOnIudXRmOGRlY29kZSh0aGlzLmxlZnRPdmVyKSxt'
    'ZXRhOnt9fSksdGhpcy5sZWZ0T3Zlcj1udWxsKX0sci5VdGY4RGVjb2RlV29y'
    'a2VyPXUsbi5pbmhlcml0cyhsLG8pLGwucHJvdG90eXBlLnByb2Nlc3NDaHVu'
    'az1mdW5jdGlvbihlKXt0aGlzLnB1c2goe2RhdGE6ci51dGY4ZW5jb2RlKGUu'
    'ZGF0YSksbWV0YTplLm1ldGF9KX0sci5VdGY4RW5jb2RlV29ya2VyPWx9LHsi'
    'Li9ub2RlanNVdGlscyI6MTQsIi4vc3RyZWFtL0dlbmVyaWNXb3JrZXIiOjI4'
    'LCIuL3N1cHBvcnQiOjMwLCIuL3V0aWxzIjozMn1dLDMyOltmdW5jdGlvbihl'
    'LHQscil7dmFyIG49ZSgiLi9zdXBwb3J0IiksaT1lKCIuL2Jhc2U2NCIpLHM9'
    'ZSgiLi9ub2RlanNVdGlscyIpLG89ZSgiLi9leHRlcm5hbCIpO2Z1bmN0aW9u'
    'IGEoZSl7cmV0dXJuIGV9ZnVuY3Rpb24gYyhlLHQpe2Zvcih2YXIgcj0wO3I8'
    'ZS5sZW5ndGg7KytyKXRbcl09MjU1JmUuY2hhckNvZGVBdChyKTtyZXR1cm4g'
    'dH1lKCJzZXRpbW1lZGlhdGUiKSxyLm5ld0Jsb2I9ZnVuY3Rpb24oZSx0KXty'
    'LmNoZWNrU3VwcG9ydCgiYmxvYiIpO3RyeXtyZXR1cm4gbmV3IEJsb2IoW2Vd'
    'LHt0eXBlOnR9KX1jYXRjaChyKXt0cnl7dmFyIG49bmV3KHNlbGYuQmxvYkJ1'
    'aWxkZXJ8fHNlbGYuV2ViS2l0QmxvYkJ1aWxkZXJ8fHNlbGYuTW96QmxvYkJ1'
    'aWxkZXJ8fHNlbGYuTVNCbG9iQnVpbGRlcik7cmV0dXJuIG4uYXBwZW5kKGUp'
    'LG4uZ2V0QmxvYih0KX1jYXRjaChlKXt0aHJvdyBuZXcgRXJyb3IoIkJ1ZyA6'
    'IGNhbid0IGNvbnN0cnVjdCB0aGUgQmxvYi4iKX19fTt2YXIgdT17c3RyaW5n'
    'aWZ5QnlDaHVuazpmdW5jdGlvbihlLHQscil7dmFyIG49W10saT0wLHM9ZS5s'
    'ZW5ndGg7aWYoczw9cilyZXR1cm4gU3RyaW5nLmZyb21DaGFyQ29kZS5hcHBs'
    'eShudWxsLGUpO2Zvcig7aTxzOykiYXJyYXkiPT09dHx8Im5vZGVidWZmZXIi'
    'PT09dD9uLnB1c2goU3RyaW5nLmZyb21DaGFyQ29kZS5hcHBseShudWxsLGUu'
    'c2xpY2UoaSxNYXRoLm1pbihpK3IscykpKSk6bi5wdXNoKFN0cmluZy5mcm9t'
    'Q2hhckNvZGUuYXBwbHkobnVsbCxlLnN1YmFycmF5KGksTWF0aC5taW4oaSty'
    'LHMpKSkpLGkrPXI7cmV0dXJuIG4uam9pbigiIil9LHN0cmluZ2lmeUJ5Q2hh'
    'cjpmdW5jdGlvbihlKXtmb3IodmFyIHQ9IiIscj0wO3I8ZS5sZW5ndGg7cisr'
    'KXQrPVN0cmluZy5mcm9tQ2hhckNvZGUoZVtyXSk7cmV0dXJuIHR9LGFwcGx5'
    'Q2FuQmVVc2VkOnt1aW50OGFycmF5OmZ1bmN0aW9uKCl7dHJ5e3JldHVybiBu'
    'LnVpbnQ4YXJyYXkmJjE9PT1TdHJpbmcuZnJvbUNoYXJDb2RlLmFwcGx5KG51'
    'bGwsbmV3IFVpbnQ4QXJyYXkoMSkpLmxlbmd0aH1jYXRjaChlKXtyZXR1cm4h'
    'MX19KCksbm9kZWJ1ZmZlcjpmdW5jdGlvbigpe3RyeXtyZXR1cm4gbi5ub2Rl'
    'YnVmZmVyJiYxPT09U3RyaW5nLmZyb21DaGFyQ29kZS5hcHBseShudWxsLHMu'
    'YWxsb2NCdWZmZXIoMSkpLmxlbmd0aH1jYXRjaChlKXtyZXR1cm4hMX19KCl9'
    'fTtmdW5jdGlvbiBsKGUpe3ZhciB0PTY1NTM2LG49ci5nZXRUeXBlT2YoZSks'
    'aT0hMDtpZigidWludDhhcnJheSI9PT1uP2k9dS5hcHBseUNhbkJlVXNlZC51'
    'aW50OGFycmF5OiJub2RlYnVmZmVyIj09PW4mJihpPXUuYXBwbHlDYW5CZVVz'
    'ZWQubm9kZWJ1ZmZlciksaSlmb3IoOzE8dDspdHJ5e3JldHVybiB1LnN0cmlu'
    'Z2lmeUJ5Q2h1bmsoZSxuLHQpfWNhdGNoKGUpe3Q9TWF0aC5mbG9vcih0LzIp'
    'fXJldHVybiB1LnN0cmluZ2lmeUJ5Q2hhcihlKX1mdW5jdGlvbiBkKGUsdCl7'
    'Zm9yKHZhciByPTA7cjxlLmxlbmd0aDtyKyspdFtyXT1lW3JdO3JldHVybiB0'
    'fXIuYXBwbHlGcm9tQ2hhckNvZGU9bDt2YXIgdz17fTt3LnN0cmluZz17c3Ry'
    'aW5nOmEsYXJyYXk6ZnVuY3Rpb24oZSl7cmV0dXJuIGMoZSxuZXcgQXJyYXko'
    'ZS5sZW5ndGgpKX0sYXJyYXlidWZmZXI6ZnVuY3Rpb24oZSl7cmV0dXJuIHcu'
    'c3RyaW5nLnVpbnQ4YXJyYXkoZSkuYnVmZmVyfSx1aW50OGFycmF5OmZ1bmN0'
    'aW9uKGUpe3JldHVybiBjKGUsbmV3IFVpbnQ4QXJyYXkoZS5sZW5ndGgpKX0s'
    'bm9kZWJ1ZmZlcjpmdW5jdGlvbihlKXtyZXR1cm4gYyhlLHMuYWxsb2NCdWZm'
    'ZXIoZS5sZW5ndGgpKX19LHcuYXJyYXk9e3N0cmluZzpsLGFycmF5OmEsYXJy'
    'YXlidWZmZXI6ZnVuY3Rpb24oZSl7cmV0dXJuIG5ldyBVaW50OEFycmF5KGUp'
    'LmJ1ZmZlcn0sdWludDhhcnJheTpmdW5jdGlvbihlKXtyZXR1cm4gbmV3IFVp'
    'bnQ4QXJyYXkoZSl9LG5vZGVidWZmZXI6ZnVuY3Rpb24oZSl7cmV0dXJuIHMu'
    'bmV3QnVmZmVyRnJvbShlKX19LHcuYXJyYXlidWZmZXI9e3N0cmluZzpmdW5j'
    'dGlvbihlKXtyZXR1cm4gbChuZXcgVWludDhBcnJheShlKSl9LGFycmF5OmZ1'
    'bmN0aW9uKGUpe3JldHVybiBkKG5ldyBVaW50OEFycmF5KGUpLG5ldyBBcnJh'
    'eShlLmJ5dGVMZW5ndGgpKX0sYXJyYXlidWZmZXI6YSx1aW50OGFycmF5OmZ1'
    'bmN0aW9uKGUpe3JldHVybiBuZXcgVWludDhBcnJheShlKX0sbm9kZWJ1ZmZl'
    'cjpmdW5jdGlvbihlKXtyZXR1cm4gcy5uZXdCdWZmZXJGcm9tKG5ldyBVaW50'
    'OEFycmF5KGUpKX19LHcudWludDhhcnJheT17c3RyaW5nOmwsYXJyYXk6ZnVu'
    'Y3Rpb24oZSl7cmV0dXJuIGQoZSxuZXcgQXJyYXkoZS5sZW5ndGgpKX0sYXJy'
    'YXlidWZmZXI6ZnVuY3Rpb24oZSl7cmV0dXJuIGUuYnVmZmVyfSx1aW50OGFy'
    'cmF5OmEsbm9kZWJ1ZmZlcjpmdW5jdGlvbihlKXtyZXR1cm4gcy5uZXdCdWZm'
    'ZXJGcm9tKGUpfX0sdy5ub2RlYnVmZmVyPXtzdHJpbmc6bCxhcnJheTpmdW5j'
    'dGlvbihlKXtyZXR1cm4gZChlLG5ldyBBcnJheShlLmxlbmd0aCkpfSxhcnJh'
    'eWJ1ZmZlcjpmdW5jdGlvbihlKXtyZXR1cm4gdy5ub2RlYnVmZmVyLnVpbnQ4'
    'YXJyYXkoZSkuYnVmZmVyfSx1aW50OGFycmF5OmZ1bmN0aW9uKGUpe3JldHVy'
    'biBkKGUsbmV3IFVpbnQ4QXJyYXkoZS5sZW5ndGgpKX0sbm9kZWJ1ZmZlcjph'
    'fSxyLnRyYW5zZm9ybVRvPWZ1bmN0aW9uKGUsdCl7aWYodD10fHwiIiwhZSly'
    'ZXR1cm4gdDtyLmNoZWNrU3VwcG9ydChlKTt2YXIgbj1yLmdldFR5cGVPZih0'
    'KTtyZXR1cm4gd1tuXVtlXSh0KX0sci5yZXNvbHZlPWZ1bmN0aW9uKGUpe2Zv'
    'cih2YXIgdD1lLnNwbGl0KCIvIikscj1bXSxuPTA7bjx0Lmxlbmd0aDtuKysp'
    'e3ZhciBpPXRbbl07Ii4iPT09aXx8IiI9PT1pJiYwIT09biYmbiE9PXQubGVu'
    'Z3RoLTF8fCgiLi4iPT09aT9yLnBvcCgpOnIucHVzaChpKSl9cmV0dXJuIHIu'
    'am9pbigiLyIpfSxyLmdldFR5cGVPZj1mdW5jdGlvbihlKXtyZXR1cm4ic3Ry'
    'aW5nIj09dHlwZW9mIGU/InN0cmluZyI6IltvYmplY3QgQXJyYXldIj09PU9i'
    'amVjdC5wcm90b3R5cGUudG9TdHJpbmcuY2FsbChlKT8iYXJyYXkiOm4ubm9k'
    'ZWJ1ZmZlciYmcy5pc0J1ZmZlcihlKT8ibm9kZWJ1ZmZlciI6bi51aW50OGFy'
    'cmF5JiZlIGluc3RhbmNlb2YgVWludDhBcnJheT8idWludDhhcnJheSI6bi5h'
    'cnJheWJ1ZmZlciYmZSBpbnN0YW5jZW9mIEFycmF5QnVmZmVyPyJhcnJheWJ1'
    'ZmZlciI6dm9pZCAwfSxyLmNoZWNrU3VwcG9ydD1mdW5jdGlvbihlKXtpZigh'
    'bltlLnRvTG93ZXJDYXNlKCldKXRocm93IG5ldyBFcnJvcihlKyIgaXMgbm90'
    'IHN1cHBvcnRlZCBieSB0aGlzIHBsYXRmb3JtIil9LHIuTUFYX1ZBTFVFXzE2'
    'QklUUz02NTUzNSxyLk1BWF9WQUxVRV8zMkJJVFM9LTEsci5wcmV0dHk9ZnVu'
    'Y3Rpb24oZSl7dmFyIHQscixuPSIiO2ZvcihyPTA7cjwoZXx8IiIpLmxlbmd0'
    'aDtyKyspbis9IlxceCIrKCh0PWUuY2hhckNvZGVBdChyKSk8MTY/IjAiOiIi'
    'KSt0LnRvU3RyaW5nKDE2KS50b1VwcGVyQ2FzZSgpO3JldHVybiBufSxyLmRl'
    'bGF5PWZ1bmN0aW9uKGUsdCxyKXtzZXRJbW1lZGlhdGUoZnVuY3Rpb24oKXtl'
    'LmFwcGx5KHJ8fG51bGwsdHx8W10pfSl9LHIuaW5oZXJpdHM9ZnVuY3Rpb24o'
    'ZSx0KXtmdW5jdGlvbiByKCl7fXIucHJvdG90eXBlPXQucHJvdG90eXBlLGUu'
    'cHJvdG90eXBlPW5ldyByfSxyLmV4dGVuZD1mdW5jdGlvbigpe3ZhciBlLHQs'
    'cj17fTtmb3IoZT0wO2U8YXJndW1lbnRzLmxlbmd0aDtlKyspZm9yKHQgaW4g'
    'YXJndW1lbnRzW2VdKU9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHku'
    'Y2FsbChhcmd1bWVudHNbZV0sdCkmJnZvaWQgMD09PXJbdF0mJihyW3RdPWFy'
    'Z3VtZW50c1tlXVt0XSk7cmV0dXJuIHJ9LHIucHJlcGFyZUNvbnRlbnQ9ZnVu'
    'Y3Rpb24oZSx0LHMsYSx1KXtyZXR1cm4gby5Qcm9taXNlLnJlc29sdmUodCku'
    'dGhlbihmdW5jdGlvbihlKXtyZXR1cm4gbi5ibG9iJiYoZSBpbnN0YW5jZW9m'
    'IEJsb2J8fC0xIT09WyJbb2JqZWN0IEZpbGVdIiwiW29iamVjdCBCbG9iXSJd'
    'LmluZGV4T2YoT2JqZWN0LnByb3RvdHlwZS50b1N0cmluZy5jYWxsKGUpKSkm'
    'JiJ1bmRlZmluZWQiIT10eXBlb2YgRmlsZVJlYWRlcj9uZXcgby5Qcm9taXNl'
    'KGZ1bmN0aW9uKHQscil7dmFyIG49bmV3IEZpbGVSZWFkZXI7bi5vbmxvYWQ9'
    'ZnVuY3Rpb24oZSl7dChlLnRhcmdldC5yZXN1bHQpfSxuLm9uZXJyb3I9ZnVu'
    'Y3Rpb24oZSl7cihlLnRhcmdldC5lcnJvcil9LG4ucmVhZEFzQXJyYXlCdWZm'
    'ZXIoZSl9KTplfSkudGhlbihmdW5jdGlvbih0KXt2YXIgbD1yLmdldFR5cGVP'
    'Zih0KSxkO3JldHVybiBsPygiYXJyYXlidWZmZXIiPT09bD90PXIudHJhbnNm'
    'b3JtVG8oInVpbnQ4YXJyYXkiLHQpOiJzdHJpbmciPT09bCYmKHU/dD1pLmRl'
    'Y29kZSh0KTpzJiYhMCE9PWEmJih0PWMoZD10LG4udWludDhhcnJheT9uZXcg'
    'VWludDhBcnJheShkLmxlbmd0aCk6bmV3IEFycmF5KGQubGVuZ3RoKSkpKSx0'
    'KTpvLlByb21pc2UucmVqZWN0KG5ldyBFcnJvcigiQ2FuJ3QgcmVhZCB0aGUg'
    'ZGF0YSBvZiAnIitlKyInLiBJcyBpdCBpbiBhIHN1cHBvcnRlZCBKYXZhU2Ny'
    'aXB0IHR5cGUgKFN0cmluZywgQmxvYiwgQXJyYXlCdWZmZXIsIGV0YykgPyIp'
    'KX0pfX0seyIuL2Jhc2U2NCI6MSwiLi9leHRlcm5hbCI6NiwiLi9ub2RlanNV'
    'dGlscyI6MTQsIi4vc3VwcG9ydCI6MzAsc2V0aW1tZWRpYXRlOjU0fV0sMzM6'
    'W2Z1bmN0aW9uKGUsdCxyKXt2YXIgbj1lKCIuL3JlYWRlci9yZWFkZXJGb3Ii'
    'KSxpPWUoIi4vdXRpbHMiKSxzPWUoIi4vc2lnbmF0dXJlIiksbz1lKCIuL3pp'
    'cEVudHJ5IiksYT1lKCIuL3N1cHBvcnQiKTtmdW5jdGlvbiBjKGUpe3RoaXMu'
    'ZmlsZXM9W10sdGhpcy5sb2FkT3B0aW9ucz1lfWMucHJvdG90eXBlPXtjaGVj'
    'a1NpZ25hdHVyZTpmdW5jdGlvbihlKXtpZighdGhpcy5yZWFkZXIucmVhZEFu'
    'ZENoZWNrU2lnbmF0dXJlKGUpKXt0aGlzLnJlYWRlci5pbmRleC09NDt2YXIg'
    'dD10aGlzLnJlYWRlci5yZWFkU3RyaW5nKDQpO3Rocm93IG5ldyBFcnJvcigi'
    'Q29ycnVwdGVkIHppcCBvciBidWc6IHVuZXhwZWN0ZWQgc2lnbmF0dXJlICgi'
    'K2kucHJldHR5KHQpKyIsIGV4cGVjdGVkICIraS5wcmV0dHkoZSkrIikiKX19'
    'LGlzU2lnbmF0dXJlOmZ1bmN0aW9uKGUsdCl7dmFyIHI9dGhpcy5yZWFkZXIu'
    'aW5kZXg7dGhpcy5yZWFkZXIuc2V0SW5kZXgoZSk7dmFyIG49dGhpcy5yZWFk'
    'ZXIucmVhZFN0cmluZyg0KT09PXQ7cmV0dXJuIHRoaXMucmVhZGVyLnNldElu'
    'ZGV4KHIpLG59LHJlYWRCbG9ja0VuZE9mQ2VudHJhbDpmdW5jdGlvbigpe3Ro'
    'aXMuZGlza051bWJlcj10aGlzLnJlYWRlci5yZWFkSW50KDIpLHRoaXMuZGlz'
    'a1dpdGhDZW50cmFsRGlyU3RhcnQ9dGhpcy5yZWFkZXIucmVhZEludCgyKSx0'
    'aGlzLmNlbnRyYWxEaXJSZWNvcmRzT25UaGlzRGlzaz10aGlzLnJlYWRlci5y'
    'ZWFkSW50KDIpLHRoaXMuY2VudHJhbERpclJlY29yZHM9dGhpcy5yZWFkZXIu'
    'cmVhZEludCgyKSx0aGlzLmNlbnRyYWxEaXJTaXplPXRoaXMucmVhZGVyLnJl'
    'YWRJbnQoNCksdGhpcy5jZW50cmFsRGlyT2Zmc2V0PXRoaXMucmVhZGVyLnJl'
    'YWRJbnQoNCksdGhpcy56aXBDb21tZW50TGVuZ3RoPXRoaXMucmVhZGVyLnJl'
    'YWRJbnQoMik7dmFyIGU9dGhpcy5yZWFkZXIucmVhZERhdGEodGhpcy56aXBD'
    'b21tZW50TGVuZ3RoKSx0PWEudWludDhhcnJheT8idWludDhhcnJheSI6ImFy'
    'cmF5IixyPWkudHJhbnNmb3JtVG8odCxlKTt0aGlzLnppcENvbW1lbnQ9dGhp'
    'cy5sb2FkT3B0aW9ucy5kZWNvZGVGaWxlTmFtZShyKX0scmVhZEJsb2NrWmlw'
    'NjRFbmRPZkNlbnRyYWw6ZnVuY3Rpb24oKXt0aGlzLnppcDY0RW5kT2ZDZW50'
    'cmFsU2l6ZT10aGlzLnJlYWRlci5yZWFkSW50KDgpLHRoaXMucmVhZGVyLnNr'
    'aXAoNCksdGhpcy5kaXNrTnVtYmVyPXRoaXMucmVhZGVyLnJlYWRJbnQoNCks'
    'dGhpcy5kaXNrV2l0aENlbnRyYWxEaXJTdGFydD10aGlzLnJlYWRlci5yZWFk'
    'SW50KDQpLHRoaXMuY2VudHJhbERpclJlY29yZHNPblRoaXNEaXNrPXRoaXMu'
    'cmVhZGVyLnJlYWRJbnQoOCksdGhpcy5jZW50cmFsRGlyUmVjb3Jkcz10aGlz'
    'LnJlYWRlci5yZWFkSW50KDgpLHRoaXMuY2VudHJhbERpclNpemU9dGhpcy5y'
    'ZWFkZXIucmVhZEludCg4KSx0aGlzLmNlbnRyYWxEaXJPZmZzZXQ9dGhpcy5y'
    'ZWFkZXIucmVhZEludCg4KSx0aGlzLnppcDY0RXh0ZW5zaWJsZURhdGE9e307'
    'Zm9yKHZhciBlLHQscixuPXRoaXMuemlwNjRFbmRPZkNlbnRyYWxTaXplLTQ0'
    'OzA8bjspZT10aGlzLnJlYWRlci5yZWFkSW50KDIpLHQ9dGhpcy5yZWFkZXIu'
    'cmVhZEludCg0KSxyPXRoaXMucmVhZGVyLnJlYWREYXRhKHQpLHRoaXMuemlw'
    'NjRFeHRlbnNpYmxlRGF0YVtlXT17aWQ6ZSxsZW5ndGg6dCx2YWx1ZTpyfX0s'
    'cmVhZEJsb2NrWmlwNjRFbmRPZkNlbnRyYWxMb2NhdG9yOmZ1bmN0aW9uKCl7'
    'aWYodGhpcy5kaXNrV2l0aFppcDY0Q2VudHJhbERpclN0YXJ0PXRoaXMucmVh'
    'ZGVyLnJlYWRJbnQoNCksdGhpcy5yZWxhdGl2ZU9mZnNldEVuZE9mWmlwNjRD'
    'ZW50cmFsRGlyPXRoaXMucmVhZGVyLnJlYWRJbnQoOCksdGhpcy5kaXNrc0Nv'
    'dW50PXRoaXMucmVhZGVyLnJlYWRJbnQoNCksMTx0aGlzLmRpc2tzQ291bnQp'
    'dGhyb3cgbmV3IEVycm9yKCJNdWx0aS12b2x1bWVzIHppcCBhcmUgbm90IHN1'
    'cHBvcnRlZCIpfSxyZWFkTG9jYWxGaWxlczpmdW5jdGlvbigpe3ZhciBlLHQ7'
    'Zm9yKGU9MDtlPHRoaXMuZmlsZXMubGVuZ3RoO2UrKyl0PXRoaXMuZmlsZXNb'
    'ZV0sdGhpcy5yZWFkZXIuc2V0SW5kZXgodC5sb2NhbEhlYWRlck9mZnNldCks'
    'dGhpcy5jaGVja1NpZ25hdHVyZShzLkxPQ0FMX0ZJTEVfSEVBREVSKSx0LnJl'
    'YWRMb2NhbFBhcnQodGhpcy5yZWFkZXIpLHQuaGFuZGxlVVRGOCgpLHQucHJv'
    'Y2Vzc0F0dHJpYnV0ZXMoKX0scmVhZENlbnRyYWxEaXI6ZnVuY3Rpb24oKXt2'
    'YXIgZTtmb3IodGhpcy5yZWFkZXIuc2V0SW5kZXgodGhpcy5jZW50cmFsRGly'
    'T2Zmc2V0KTt0aGlzLnJlYWRlci5yZWFkQW5kQ2hlY2tTaWduYXR1cmUocy5D'
    'RU5UUkFMX0ZJTEVfSEVBREVSKTspKGU9bmV3IG8oe3ppcDY0OnRoaXMuemlw'
    'NjR9LHRoaXMubG9hZE9wdGlvbnMpKS5yZWFkQ2VudHJhbFBhcnQodGhpcy5y'
    'ZWFkZXIpLHRoaXMuZmlsZXMucHVzaChlKTtpZih0aGlzLmNlbnRyYWxEaXJS'
    'ZWNvcmRzIT09dGhpcy5maWxlcy5sZW5ndGgmJjAhPT10aGlzLmNlbnRyYWxE'
    'aXJSZWNvcmRzJiYwPT09dGhpcy5maWxlcy5sZW5ndGgpdGhyb3cgbmV3IEVy'
    'cm9yKCJDb3JydXB0ZWQgemlwIG9yIGJ1ZzogZXhwZWN0ZWQgIit0aGlzLmNl'
    'bnRyYWxEaXJSZWNvcmRzKyIgcmVjb3JkcyBpbiBjZW50cmFsIGRpciwgZ290'
    'ICIrdGhpcy5maWxlcy5sZW5ndGgpfSxyZWFkRW5kT2ZDZW50cmFsOmZ1bmN0'
    'aW9uKCl7dmFyIGU9dGhpcy5yZWFkZXIubGFzdEluZGV4T2ZTaWduYXR1cmUo'
    'cy5DRU5UUkFMX0RJUkVDVE9SWV9FTkQpO2lmKGU8MCl0aHJvdyB0aGlzLmlz'
    'U2lnbmF0dXJlKDAscy5MT0NBTF9GSUxFX0hFQURFUik/bmV3IEVycm9yKCJD'
    'b3JydXB0ZWQgemlwOiBjYW4ndCBmaW5kIGVuZCBvZiBjZW50cmFsIGRpcmVj'
    'dG9yeSIpOm5ldyBFcnJvcigiQ2FuJ3QgZmluZCBlbmQgb2YgY2VudHJhbCBk'
    'aXJlY3RvcnkgOiBpcyB0aGlzIGEgemlwIGZpbGUgPyBJZiBpdCBpcywgc2Vl'
    'IGh0dHBzOi8vc3R1ay5naXRodWIuaW8vanN6aXAvZG9jdW1lbnRhdGlvbi9o'
    'b3d0by9yZWFkX3ppcC5odG1sIik7dGhpcy5yZWFkZXIuc2V0SW5kZXgoZSk7'
    'dmFyIHQ9ZTtpZih0aGlzLmNoZWNrU2lnbmF0dXJlKHMuQ0VOVFJBTF9ESVJF'
    'Q1RPUllfRU5EKSx0aGlzLnJlYWRCbG9ja0VuZE9mQ2VudHJhbCgpLHRoaXMu'
    'ZGlza051bWJlcj09PWkuTUFYX1ZBTFVFXzE2QklUU3x8dGhpcy5kaXNrV2l0'
    'aENlbnRyYWxEaXJTdGFydD09PWkuTUFYX1ZBTFVFXzE2QklUU3x8dGhpcy5j'
    'ZW50cmFsRGlyUmVjb3Jkc09uVGhpc0Rpc2s9PT1pLk1BWF9WQUxVRV8xNkJJ'
    'VFN8fHRoaXMuY2VudHJhbERpclJlY29yZHM9PT1pLk1BWF9WQUxVRV8xNkJJ'
    'VFN8fHRoaXMuY2VudHJhbERpclNpemU9PT1pLk1BWF9WQUxVRV8zMkJJVFN8'
    'fHRoaXMuY2VudHJhbERpck9mZnNldD09PWkuTUFYX1ZBTFVFXzMyQklUUyl7'
    'aWYodGhpcy56aXA2ND0hMCwoZT10aGlzLnJlYWRlci5sYXN0SW5kZXhPZlNp'
    'Z25hdHVyZShzLlpJUDY0X0NFTlRSQUxfRElSRUNUT1JZX0xPQ0FUT1IpKTww'
    'KXRocm93IG5ldyBFcnJvcigiQ29ycnVwdGVkIHppcDogY2FuJ3QgZmluZCB0'
    'aGUgWklQNjQgZW5kIG9mIGNlbnRyYWwgZGlyZWN0b3J5IGxvY2F0b3IiKTtp'
    'Zih0aGlzLnJlYWRlci5zZXRJbmRleChlKSx0aGlzLmNoZWNrU2lnbmF0dXJl'
    'KHMuWklQNjRfQ0VOVFJBTF9ESVJFQ1RPUllfTE9DQVRPUiksdGhpcy5yZWFk'
    'QmxvY2taaXA2NEVuZE9mQ2VudHJhbExvY2F0b3IoKSwhdGhpcy5pc1NpZ25h'
    'dHVyZSh0aGlzLnJlbGF0aXZlT2Zmc2V0RW5kT2ZaaXA2NENlbnRyYWxEaXIs'
    'cy5aSVA2NF9DRU5UUkFMX0RJUkVDVE9SWV9FTkQpJiYodGhpcy5yZWxhdGl2'
    'ZU9mZnNldEVuZE9mWmlwNjRDZW50cmFsRGlyPXRoaXMucmVhZGVyLmxhc3RJ'
    'bmRleE9mU2lnbmF0dXJlKHMuWklQNjRfQ0VOVFJBTF9ESVJFQ1RPUllfRU5E'
    'KSx0aGlzLnJlbGF0aXZlT2Zmc2V0RW5kT2ZaaXA2NENlbnRyYWxEaXI8MCkp'
    'dGhyb3cgbmV3IEVycm9yKCJDb3JydXB0ZWQgemlwOiBjYW4ndCBmaW5kIHRo'
    'ZSBaSVA2NCBlbmQgb2YgY2VudHJhbCBkaXJlY3RvcnkiKTt0aGlzLnJlYWRl'
    'ci5zZXRJbmRleCh0aGlzLnJlbGF0aXZlT2Zmc2V0RW5kT2ZaaXA2NENlbnRy'
    'YWxEaXIpLHRoaXMuY2hlY2tTaWduYXR1cmUocy5aSVA2NF9DRU5UUkFMX0RJ'
    'UkVDVE9SWV9FTkQpLHRoaXMucmVhZEJsb2NrWmlwNjRFbmRPZkNlbnRyYWwo'
    'KX12YXIgcj10aGlzLmNlbnRyYWxEaXJPZmZzZXQrdGhpcy5jZW50cmFsRGly'
    'U2l6ZTt0aGlzLnppcDY0JiYocis9MjAscis9MTIrdGhpcy56aXA2NEVuZE9m'
    'Q2VudHJhbFNpemUpO3ZhciBuPXQtcjtpZigwPG4pdGhpcy5pc1NpZ25hdHVy'
    'ZSh0LHMuQ0VOVFJBTF9GSUxFX0hFQURFUil8fCh0aGlzLnJlYWRlci56ZXJv'
    'PW4pO2Vsc2UgaWYobjwwKXRocm93IG5ldyBFcnJvcigiQ29ycnVwdGVkIHpp'
    'cDogbWlzc2luZyAiK01hdGguYWJzKG4pKyIgYnl0ZXMuIil9LHByZXBhcmVS'
    'ZWFkZXI6ZnVuY3Rpb24oZSl7dGhpcy5yZWFkZXI9bihlKX0sbG9hZDpmdW5j'
    'dGlvbihlKXt0aGlzLnByZXBhcmVSZWFkZXIoZSksdGhpcy5yZWFkRW5kT2ZD'
    'ZW50cmFsKCksdGhpcy5yZWFkQ2VudHJhbERpcigpLHRoaXMucmVhZExvY2Fs'
    'RmlsZXMoKX19LHQuZXhwb3J0cz1jfSx7Ii4vcmVhZGVyL3JlYWRlckZvciI6'
    'MjIsIi4vc2lnbmF0dXJlIjoyMywiLi9zdXBwb3J0IjozMCwiLi91dGlscyI6'
    'MzIsIi4vemlwRW50cnkiOjM0fV0sMzQ6W2Z1bmN0aW9uKGUsdCxyKXt2YXIg'
    'bj1lKCIuL3JlYWRlci9yZWFkZXJGb3IiKSxpPWUoIi4vdXRpbHMiKSxzPWUo'
    'Ii4vY29tcHJlc3NlZE9iamVjdCIpLG89ZSgiLi9jcmMzMiIpLGE9ZSgiLi91'
    'dGY4IiksYz1lKCIuL2NvbXByZXNzaW9ucyIpLHU9ZSgiLi9zdXBwb3J0Iik7'
    'ZnVuY3Rpb24gbChlLHQpe3RoaXMub3B0aW9ucz1lLHRoaXMubG9hZE9wdGlv'
    'bnM9dH1sLnByb3RvdHlwZT17aXNFbmNyeXB0ZWQ6ZnVuY3Rpb24oKXtyZXR1'
    'cm4hKDEmfnRoaXMuYml0RmxhZyl9LHVzZVVURjg6ZnVuY3Rpb24oKXtyZXR1'
    'cm4hKDIwNDgmfnRoaXMuYml0RmxhZyl9LHJlYWRMb2NhbFBhcnQ6ZnVuY3Rp'
    'b24oZSl7dmFyIHQscjtpZihlLnNraXAoMjIpLHRoaXMuZmlsZU5hbWVMZW5n'
    'dGg9ZS5yZWFkSW50KDIpLHI9ZS5yZWFkSW50KDIpLHRoaXMuZmlsZU5hbWU9'
    'ZS5yZWFkRGF0YSh0aGlzLmZpbGVOYW1lTGVuZ3RoKSxlLnNraXAociksLTE9'
    'PT10aGlzLmNvbXByZXNzZWRTaXplfHwtMT09PXRoaXMudW5jb21wcmVzc2Vk'
    'U2l6ZSl0aHJvdyBuZXcgRXJyb3IoIkJ1ZyBvciBjb3JydXB0ZWQgemlwIDog'
    'ZGlkbid0IGdldCBlbm91Z2ggaW5mb3JtYXRpb24gZnJvbSB0aGUgY2VudHJh'
    'bCBkaXJlY3RvcnkgKGNvbXByZXNzZWRTaXplID09PSAtMSB8fCB1bmNvbXBy'
    'ZXNzZWRTaXplID09PSAtMSkiKTtpZihudWxsPT09KHQ9ZnVuY3Rpb24oZSl7'
    'Zm9yKHZhciB0IGluIGMpaWYoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9w'
    'ZXJ0eS5jYWxsKGMsdCkmJmNbdF0ubWFnaWM9PT1lKXJldHVybiBjW3RdO3Jl'
    'dHVybiBudWxsfSh0aGlzLmNvbXByZXNzaW9uTWV0aG9kKSkpdGhyb3cgbmV3'
    'IEVycm9yKCJDb3JydXB0ZWQgemlwIDogY29tcHJlc3Npb24gIitpLnByZXR0'
    'eSh0aGlzLmNvbXByZXNzaW9uTWV0aG9kKSsiIHVua25vd24gKGlubmVyIGZp'
    'bGUgOiAiK2kudHJhbnNmb3JtVG8oInN0cmluZyIsdGhpcy5maWxlTmFtZSkr'
    'IikiKTt0aGlzLmRlY29tcHJlc3NlZD1uZXcgcyh0aGlzLmNvbXByZXNzZWRT'
    'aXplLHRoaXMudW5jb21wcmVzc2VkU2l6ZSx0aGlzLmNyYzMyLHQsZS5yZWFk'
    'RGF0YSh0aGlzLmNvbXByZXNzZWRTaXplKSl9LHJlYWRDZW50cmFsUGFydDpm'
    'dW5jdGlvbihlKXt0aGlzLnZlcnNpb25NYWRlQnk9ZS5yZWFkSW50KDIpLGUu'
    'c2tpcCgyKSx0aGlzLmJpdEZsYWc9ZS5yZWFkSW50KDIpLHRoaXMuY29tcHJl'
    'c3Npb25NZXRob2Q9ZS5yZWFkU3RyaW5nKDIpLHRoaXMuZGF0ZT1lLnJlYWRE'
    'YXRlKCksdGhpcy5jcmMzMj1lLnJlYWRJbnQoNCksdGhpcy5jb21wcmVzc2Vk'
    'U2l6ZT1lLnJlYWRJbnQoNCksdGhpcy51bmNvbXByZXNzZWRTaXplPWUucmVh'
    'ZEludCg0KTt2YXIgdD1lLnJlYWRJbnQoMik7aWYodGhpcy5leHRyYUZpZWxk'
    'c0xlbmd0aD1lLnJlYWRJbnQoMiksdGhpcy5maWxlQ29tbWVudExlbmd0aD1l'
    'LnJlYWRJbnQoMiksdGhpcy5kaXNrTnVtYmVyU3RhcnQ9ZS5yZWFkSW50KDIp'
    'LHRoaXMuaW50ZXJuYWxGaWxlQXR0cmlidXRlcz1lLnJlYWRJbnQoMiksdGhp'
    'cy5leHRlcm5hbEZpbGVBdHRyaWJ1dGVzPWUucmVhZEludCg0KSx0aGlzLmxv'
    'Y2FsSGVhZGVyT2Zmc2V0PWUucmVhZEludCg0KSx0aGlzLmlzRW5jcnlwdGVk'
    'KCkpdGhyb3cgbmV3IEVycm9yKCJFbmNyeXB0ZWQgemlwIGFyZSBub3Qgc3Vw'
    'cG9ydGVkIik7ZS5za2lwKHQpLHRoaXMucmVhZEV4dHJhRmllbGRzKGUpLHRo'
    'aXMucGFyc2VaSVA2NEV4dHJhRmllbGQoZSksdGhpcy5maWxlQ29tbWVudD1l'
    'LnJlYWREYXRhKHRoaXMuZmlsZUNvbW1lbnRMZW5ndGgpfSxwcm9jZXNzQXR0'
    'cmlidXRlczpmdW5jdGlvbigpe3RoaXMudW5peFBlcm1pc3Npb25zPW51bGws'
    'dGhpcy5kb3NQZXJtaXNzaW9ucz1udWxsO3ZhciBlPXRoaXMudmVyc2lvbk1h'
    'ZGVCeT4+ODt0aGlzLmRpcj0hISgxNiZ0aGlzLmV4dGVybmFsRmlsZUF0dHJp'
    'YnV0ZXMpLDA9PWUmJih0aGlzLmRvc1Blcm1pc3Npb25zPTYzJnRoaXMuZXh0'
    'ZXJuYWxGaWxlQXR0cmlidXRlcyksMz09ZSYmKHRoaXMudW5peFBlcm1pc3Np'
    'b25zPXRoaXMuZXh0ZXJuYWxGaWxlQXR0cmlidXRlcz4+MTYmNjU1MzUpLHRo'
    'aXMuZGlyfHwiLyIhPT10aGlzLmZpbGVOYW1lU3RyLnNsaWNlKC0xKXx8KHRo'
    'aXMuZGlyPSEwKX0scGFyc2VaSVA2NEV4dHJhRmllbGQ6ZnVuY3Rpb24oKXtp'
    'Zih0aGlzLmV4dHJhRmllbGRzWzFdKXt2YXIgZT1uKHRoaXMuZXh0cmFGaWVs'
    'ZHNbMV0udmFsdWUpO3RoaXMudW5jb21wcmVzc2VkU2l6ZT09PWkuTUFYX1ZB'
    'TFVFXzMyQklUUyYmKHRoaXMudW5jb21wcmVzc2VkU2l6ZT1lLnJlYWRJbnQo'
    'OCkpLHRoaXMuY29tcHJlc3NlZFNpemU9PT1pLk1BWF9WQUxVRV8zMkJJVFMm'
    'Jih0aGlzLmNvbXByZXNzZWRTaXplPWUucmVhZEludCg4KSksdGhpcy5sb2Nh'
    'bEhlYWRlck9mZnNldD09PWkuTUFYX1ZBTFVFXzMyQklUUyYmKHRoaXMubG9j'
    'YWxIZWFkZXJPZmZzZXQ9ZS5yZWFkSW50KDgpKSx0aGlzLmRpc2tOdW1iZXJT'
    'dGFydD09PWkuTUFYX1ZBTFVFXzMyQklUUyYmKHRoaXMuZGlza051bWJlclN0'
    'YXJ0PWUucmVhZEludCg0KSl9fSxyZWFkRXh0cmFGaWVsZHM6ZnVuY3Rpb24o'
    'ZSl7dmFyIHQscixuLGk9ZS5pbmRleCt0aGlzLmV4dHJhRmllbGRzTGVuZ3Ro'
    'O2Zvcih0aGlzLmV4dHJhRmllbGRzfHwodGhpcy5leHRyYUZpZWxkcz17fSk7'
    'ZS5pbmRleCs0PGk7KXQ9ZS5yZWFkSW50KDIpLHI9ZS5yZWFkSW50KDIpLG49'
    'ZS5yZWFkRGF0YShyKSx0aGlzLmV4dHJhRmllbGRzW3RdPXtpZDp0LGxlbmd0'
    'aDpyLHZhbHVlOm59O2Uuc2V0SW5kZXgoaSl9LGhhbmRsZVVURjg6ZnVuY3Rp'
    'b24oKXt2YXIgZT11LnVpbnQ4YXJyYXk/InVpbnQ4YXJyYXkiOiJhcnJheSI7'
    'aWYodGhpcy51c2VVVEY4KCkpdGhpcy5maWxlTmFtZVN0cj1hLnV0ZjhkZWNv'
    'ZGUodGhpcy5maWxlTmFtZSksdGhpcy5maWxlQ29tbWVudFN0cj1hLnV0Zjhk'
    'ZWNvZGUodGhpcy5maWxlQ29tbWVudCk7ZWxzZXt2YXIgdD10aGlzLmZpbmRF'
    'eHRyYUZpZWxkVW5pY29kZVBhdGgoKTtpZihudWxsIT09dCl0aGlzLmZpbGVO'
    'YW1lU3RyPXQ7ZWxzZXt2YXIgcj1pLnRyYW5zZm9ybVRvKGUsdGhpcy5maWxl'
    'TmFtZSk7dGhpcy5maWxlTmFtZVN0cj10aGlzLmxvYWRPcHRpb25zLmRlY29k'
    'ZUZpbGVOYW1lKHIpfXZhciBuPXRoaXMuZmluZEV4dHJhRmllbGRVbmljb2Rl'
    'Q29tbWVudCgpO2lmKG51bGwhPT1uKXRoaXMuZmlsZUNvbW1lbnRTdHI9bjtl'
    'bHNle3ZhciBzPWkudHJhbnNmb3JtVG8oZSx0aGlzLmZpbGVDb21tZW50KTt0'
    'aGlzLmZpbGVDb21tZW50U3RyPXRoaXMubG9hZE9wdGlvbnMuZGVjb2RlRmls'
    'ZU5hbWUocyl9fX0sZmluZEV4dHJhRmllbGRVbmljb2RlUGF0aDpmdW5jdGlv'
    'bigpe3ZhciBlPXRoaXMuZXh0cmFGaWVsZHNbMjg3ODldO2lmKGUpe3ZhciB0'
    'PW4oZS52YWx1ZSk7cmV0dXJuIDEhPT10LnJlYWRJbnQoMSl8fG8odGhpcy5m'
    'aWxlTmFtZSkhPT10LnJlYWRJbnQoNCk/bnVsbDphLnV0ZjhkZWNvZGUodC5y'
    'ZWFkRGF0YShlLmxlbmd0aC01KSl9cmV0dXJuIG51bGx9LGZpbmRFeHRyYUZp'
    'ZWxkVW5pY29kZUNvbW1lbnQ6ZnVuY3Rpb24oKXt2YXIgZT10aGlzLmV4dHJh'
    'RmllbGRzWzI1NDYxXTtpZihlKXt2YXIgdD1uKGUudmFsdWUpO3JldHVybiAx'
    'IT09dC5yZWFkSW50KDEpfHxvKHRoaXMuZmlsZUNvbW1lbnQpIT09dC5yZWFk'
    'SW50KDQpP251bGw6YS51dGY4ZGVjb2RlKHQucmVhZERhdGEoZS5sZW5ndGgt'
    'NSkpfXJldHVybiBudWxsfX0sdC5leHBvcnRzPWx9LHsiLi9jb21wcmVzc2Vk'
    'T2JqZWN0IjoyLCIuL2NvbXByZXNzaW9ucyI6MywiLi9jcmMzMiI6NCwiLi9y'
    'ZWFkZXIvcmVhZGVyRm9yIjoyMiwiLi9zdXBwb3J0IjozMCwiLi91dGY4Ijoz'
    'MSwiLi91dGlscyI6MzJ9XSwzNTpbZnVuY3Rpb24oZSx0LHIpe2Z1bmN0aW9u'
    'IG4oZSx0LHIpe3RoaXMubmFtZT1lLHRoaXMuZGlyPXIuZGlyLHRoaXMuZGF0'
    'ZT1yLmRhdGUsdGhpcy5jb21tZW50PXIuY29tbWVudCx0aGlzLnVuaXhQZXJt'
    'aXNzaW9ucz1yLnVuaXhQZXJtaXNzaW9ucyx0aGlzLmRvc1Blcm1pc3Npb25z'
    'PXIuZG9zUGVybWlzc2lvbnMsdGhpcy5fZGF0YT10LHRoaXMuX2RhdGFCaW5h'
    'cnk9ci5iaW5hcnksdGhpcy5vcHRpb25zPXtjb21wcmVzc2lvbjpyLmNvbXBy'
    'ZXNzaW9uLGNvbXByZXNzaW9uT3B0aW9uczpyLmNvbXByZXNzaW9uT3B0aW9u'
    'c319dmFyIGk9ZSgiLi9zdHJlYW0vU3RyZWFtSGVscGVyIikscz1lKCIuL3N0'
    'cmVhbS9EYXRhV29ya2VyIiksbz1lKCIuL3V0ZjgiKSxhPWUoIi4vY29tcHJl'
    'c3NlZE9iamVjdCIpLGM9ZSgiLi9zdHJlYW0vR2VuZXJpY1dvcmtlciIpO24u'
    'cHJvdG90eXBlPXtpbnRlcm5hbFN0cmVhbTpmdW5jdGlvbihlKXt2YXIgdD1u'
    'dWxsLHI9InN0cmluZyI7dHJ5e2lmKCFlKXRocm93IG5ldyBFcnJvcigiTm8g'
    'b3V0cHV0IHR5cGUgc3BlY2lmaWVkLiIpO3ZhciBuPSJzdHJpbmciPT09KHI9'
    'ZS50b0xvd2VyQ2FzZSgpKXx8InRleHQiPT09cjsiYmluYXJ5c3RyaW5nIiE9'
    'PXImJiJ0ZXh0IiE9PXJ8fChyPSJzdHJpbmciKSx0PXRoaXMuX2RlY29tcHJl'
    'c3NXb3JrZXIoKTt2YXIgcz0hdGhpcy5fZGF0YUJpbmFyeTtzJiYhbiYmKHQ9'
    'dC5waXBlKG5ldyBvLlV0ZjhFbmNvZGVXb3JrZXIpKSwhcyYmbiYmKHQ9dC5w'
    'aXBlKG5ldyBvLlV0ZjhEZWNvZGVXb3JrZXIpKX1jYXRjaChlKXsodD1uZXcg'
    'YygiZXJyb3IiKSkuZXJyb3IoZSl9cmV0dXJuIG5ldyBpKHQsciwiIil9LGFz'
    'eW5jOmZ1bmN0aW9uKGUsdCl7cmV0dXJuIHRoaXMuaW50ZXJuYWxTdHJlYW0o'
    'ZSkuYWNjdW11bGF0ZSh0KX0sbm9kZVN0cmVhbTpmdW5jdGlvbihlLHQpe3Jl'
    'dHVybiB0aGlzLmludGVybmFsU3RyZWFtKGV8fCJub2RlYnVmZmVyIikudG9O'
    'b2RlanNTdHJlYW0odCl9LF9jb21wcmVzc1dvcmtlcjpmdW5jdGlvbihlLHQp'
    'e2lmKHRoaXMuX2RhdGEgaW5zdGFuY2VvZiBhJiZ0aGlzLl9kYXRhLmNvbXBy'
    'ZXNzaW9uLm1hZ2ljPT09ZS5tYWdpYylyZXR1cm4gdGhpcy5fZGF0YS5nZXRD'
    'b21wcmVzc2VkV29ya2VyKCk7dmFyIHI9dGhpcy5fZGVjb21wcmVzc1dvcmtl'
    'cigpO3JldHVybiB0aGlzLl9kYXRhQmluYXJ5fHwocj1yLnBpcGUobmV3IG8u'
    'VXRmOEVuY29kZVdvcmtlcikpLGEuY3JlYXRlV29ya2VyRnJvbShyLGUsdCl9'
    'LF9kZWNvbXByZXNzV29ya2VyOmZ1bmN0aW9uKCl7cmV0dXJuIHRoaXMuX2Rh'
    'dGEgaW5zdGFuY2VvZiBhP3RoaXMuX2RhdGEuZ2V0Q29udGVudFdvcmtlcigp'
    'OnRoaXMuX2RhdGEgaW5zdGFuY2VvZiBjP3RoaXMuX2RhdGE6bmV3IHModGhp'
    'cy5fZGF0YSl9fTtmb3IodmFyIHU9WyJhc1RleHQiLCJhc0JpbmFyeSIsImFz'
    'Tm9kZUJ1ZmZlciIsImFzVWludDhBcnJheSIsImFzQXJyYXlCdWZmZXIiXSxs'
    'PWZ1bmN0aW9uKCl7dGhyb3cgbmV3IEVycm9yKCJUaGlzIG1ldGhvZCBoYXMg'
    'YmVlbiByZW1vdmVkIGluIEpTWmlwIDMuMCwgcGxlYXNlIGNoZWNrIHRoZSB1'
    'cGdyYWRlIGd1aWRlLiIpfSxkPTA7ZDx1Lmxlbmd0aDtkKyspbi5wcm90b3R5'
    'cGVbdVtkXV09bDt0LmV4cG9ydHM9bn0seyIuL2NvbXByZXNzZWRPYmplY3Qi'
    'OjIsIi4vc3RyZWFtL0RhdGFXb3JrZXIiOjI3LCIuL3N0cmVhbS9HZW5lcmlj'
    'V29ya2VyIjoyOCwiLi9zdHJlYW0vU3RyZWFtSGVscGVyIjoyOSwiLi91dGY4'
    'IjozMX1dLDM2OltmdW5jdGlvbihlLHQscil7KGZ1bmN0aW9uKGUpe3ZhciBy'
    'LG4saT1lLk11dGF0aW9uT2JzZXJ2ZXJ8fGUuV2ViS2l0TXV0YXRpb25PYnNl'
    'cnZlcjtpZihpKXt2YXIgcz0wLG89bmV3IGkobCksYT1lLmRvY3VtZW50LmNy'
    'ZWF0ZVRleHROb2RlKCIiKTtvLm9ic2VydmUoYSx7Y2hhcmFjdGVyRGF0YToh'
    'MH0pLHI9ZnVuY3Rpb24oKXthLmRhdGE9cz0rK3MlMn19ZWxzZSBpZihlLnNl'
    'dEltbWVkaWF0ZXx8dm9pZCAwPT09ZS5NZXNzYWdlQ2hhbm5lbClyPSJkb2N1'
    'bWVudCJpbiBlJiYib25yZWFkeXN0YXRlY2hhbmdlImluIGUuZG9jdW1lbnQu'
    'Y3JlYXRlRWxlbWVudCgic2NyaXB0Iik/ZnVuY3Rpb24oKXt2YXIgdD1lLmRv'
    'Y3VtZW50LmNyZWF0ZUVsZW1lbnQoInNjcmlwdCIpO3Qub25yZWFkeXN0YXRl'
    'Y2hhbmdlPWZ1bmN0aW9uKCl7bCgpLHQub25yZWFkeXN0YXRlY2hhbmdlPW51'
    'bGwsdC5wYXJlbnROb2RlLnJlbW92ZUNoaWxkKHQpLHQ9bnVsbH0sZS5kb2N1'
    'bWVudC5kb2N1bWVudEVsZW1lbnQuYXBwZW5kQ2hpbGQodCl9OmZ1bmN0aW9u'
    'KCl7c2V0VGltZW91dChsLDApfTtlbHNle3ZhciBjPW5ldyBlLk1lc3NhZ2VD'
    'aGFubmVsO2MucG9ydDEub25tZXNzYWdlPWwscj1mdW5jdGlvbigpe2MucG9y'
    'dDIucG9zdE1lc3NhZ2UoMCl9fXZhciB1PVtdO2Z1bmN0aW9uIGwoKXt2YXIg'
    'ZSx0O249ITA7Zm9yKHZhciByPXUubGVuZ3RoO3I7KXtmb3IodD11LHU9W10s'
    'ZT0tMTsrK2U8cjspdFtlXSgpO3I9dS5sZW5ndGh9bj0hMX10LmV4cG9ydHM9'
    'ZnVuY3Rpb24oZSl7MSE9PXUucHVzaChlKXx8bnx8cigpfX0pLmNhbGwodGhp'
    'cywidW5kZWZpbmVkIiE9dHlwZW9mIGdsb2JhbD9nbG9iYWw6InVuZGVmaW5l'
    'ZCIhPXR5cGVvZiBzZWxmP3NlbGY6InVuZGVmaW5lZCIhPXR5cGVvZiB3aW5k'
    'b3c/d2luZG93Ont9KX0se31dLDM3OltmdW5jdGlvbihlLHQscil7dmFyIG49'
    'ZSgiaW1tZWRpYXRlIik7ZnVuY3Rpb24gaSgpe312YXIgcz17fSxvPVsiUkVK'
    'RUNURUQiXSxhPVsiRlVMRklMTEVEIl0sYz1bIlBFTkRJTkciXTtmdW5jdGlv'
    'biB1KGUpe2lmKCJmdW5jdGlvbiIhPXR5cGVvZiBlKXRocm93IG5ldyBUeXBl'
    'RXJyb3IoInJlc29sdmVyIG11c3QgYmUgYSBmdW5jdGlvbiIpO3RoaXMuc3Rh'
    'dGU9Yyx0aGlzLnF1ZXVlPVtdLHRoaXMub3V0Y29tZT12b2lkIDAsZSE9PWkm'
    'JmgodGhpcyxlKX1mdW5jdGlvbiBsKGUsdCxyKXt0aGlzLnByb21pc2U9ZSwi'
    'ZnVuY3Rpb24iPT10eXBlb2YgdCYmKHRoaXMub25GdWxmaWxsZWQ9dCx0aGlz'
    'LmNhbGxGdWxmaWxsZWQ9dGhpcy5vdGhlckNhbGxGdWxmaWxsZWQpLCJmdW5j'
    'dGlvbiI9PXR5cGVvZiByJiYodGhpcy5vblJlamVjdGVkPXIsdGhpcy5jYWxs'
    'UmVqZWN0ZWQ9dGhpcy5vdGhlckNhbGxSZWplY3RlZCl9ZnVuY3Rpb24gZChl'
    'LHQscil7bihmdW5jdGlvbigpe3ZhciBuO3RyeXtuPXQocil9Y2F0Y2godCl7'
    'cmV0dXJuIHMucmVqZWN0KGUsdCl9bj09PWU/cy5yZWplY3QoZSxuZXcgVHlw'
    'ZUVycm9yKCJDYW5ub3QgcmVzb2x2ZSBwcm9taXNlIHdpdGggaXRzZWxmIikp'
    'OnMucmVzb2x2ZShlLG4pfSl9ZnVuY3Rpb24gdyhlKXt2YXIgdD1lJiZlLnRo'
    'ZW47aWYoZSYmKCJvYmplY3QiPT10eXBlb2YgZXx8ImZ1bmN0aW9uIj09dHlw'
    'ZW9mIGUpJiYiZnVuY3Rpb24iPT10eXBlb2YgdClyZXR1cm4gZnVuY3Rpb24o'
    'KXt0LmFwcGx5KGUsYXJndW1lbnRzKX19ZnVuY3Rpb24gaChlLHQpe3ZhciBy'
    'PSExO2Z1bmN0aW9uIG4odCl7cnx8KHI9ITAscy5yZWplY3QoZSx0KSl9ZnVu'
    'Y3Rpb24gaSh0KXtyfHwocj0hMCxzLnJlc29sdmUoZSx0KSl9dmFyIG89Zihm'
    'dW5jdGlvbigpe3QoaSxuKX0pOyJlcnJvciI9PT1vLnN0YXR1cyYmbihvLnZh'
    'bHVlKX1mdW5jdGlvbiBmKGUsdCl7dmFyIHI9e307dHJ5e3IudmFsdWU9ZSh0'
    'KSxyLnN0YXR1cz0ic3VjY2VzcyJ9Y2F0Y2goZSl7ci5zdGF0dXM9ImVycm9y'
    'IixyLnZhbHVlPWV9cmV0dXJuIHJ9KHQuZXhwb3J0cz11KS5wcm90b3R5cGUu'
    'ZmluYWxseT1mdW5jdGlvbihlKXtpZigiZnVuY3Rpb24iIT10eXBlb2YgZSly'
    'ZXR1cm4gdGhpczt2YXIgdD10aGlzLmNvbnN0cnVjdG9yO3JldHVybiB0aGlz'
    'LnRoZW4oZnVuY3Rpb24ocil7cmV0dXJuIHQucmVzb2x2ZShlKCkpLnRoZW4o'
    'ZnVuY3Rpb24oKXtyZXR1cm4gcn0pfSxmdW5jdGlvbihyKXtyZXR1cm4gdC5y'
    'ZXNvbHZlKGUoKSkudGhlbihmdW5jdGlvbigpe3Rocm93IHJ9KX0pfSx1LnBy'
    'b3RvdHlwZS5jYXRjaD1mdW5jdGlvbihlKXtyZXR1cm4gdGhpcy50aGVuKG51'
    'bGwsZSl9LHUucHJvdG90eXBlLnRoZW49ZnVuY3Rpb24oZSx0KXtpZigiZnVu'
    'Y3Rpb24iIT10eXBlb2YgZSYmdGhpcy5zdGF0ZT09PWF8fCJmdW5jdGlvbiIh'
    'PXR5cGVvZiB0JiZ0aGlzLnN0YXRlPT09bylyZXR1cm4gdGhpczt2YXIgcj1u'
    'ZXcgdGhpcy5jb25zdHJ1Y3RvcihpKTtyZXR1cm4gdGhpcy5zdGF0ZSE9PWM/'
    'ZChyLHRoaXMuc3RhdGU9PT1hP2U6dCx0aGlzLm91dGNvbWUpOnRoaXMucXVl'
    'dWUucHVzaChuZXcgbChyLGUsdCkpLHJ9LGwucHJvdG90eXBlLmNhbGxGdWxm'
    'aWxsZWQ9ZnVuY3Rpb24oZSl7cy5yZXNvbHZlKHRoaXMucHJvbWlzZSxlKX0s'
    'bC5wcm90b3R5cGUub3RoZXJDYWxsRnVsZmlsbGVkPWZ1bmN0aW9uKGUpe2Qo'
    'dGhpcy5wcm9taXNlLHRoaXMub25GdWxmaWxsZWQsZSl9LGwucHJvdG90eXBl'
    'LmNhbGxSZWplY3RlZD1mdW5jdGlvbihlKXtzLnJlamVjdCh0aGlzLnByb21p'
    'c2UsZSl9LGwucHJvdG90eXBlLm90aGVyQ2FsbFJlamVjdGVkPWZ1bmN0aW9u'
    'KGUpe2QodGhpcy5wcm9taXNlLHRoaXMub25SZWplY3RlZCxlKX0scy5yZXNv'
    'bHZlPWZ1bmN0aW9uKGUsdCl7dmFyIHI9Zih3LHQpO2lmKCJlcnJvciI9PT1y'
    'LnN0YXR1cylyZXR1cm4gcy5yZWplY3QoZSxyLnZhbHVlKTt2YXIgbj1yLnZh'
    'bHVlO2lmKG4paChlLG4pO2Vsc2V7ZS5zdGF0ZT1hLGUub3V0Y29tZT10O2Zv'
    'cih2YXIgaT0tMSxvPWUucXVldWUubGVuZ3RoOysraTxvOyllLnF1ZXVlW2ld'
    'LmNhbGxGdWxmaWxsZWQodCl9cmV0dXJuIGV9LHMucmVqZWN0PWZ1bmN0aW9u'
    'KGUsdCl7ZS5zdGF0ZT1vLGUub3V0Y29tZT10O2Zvcih2YXIgcj0tMSxuPWUu'
    'cXVldWUubGVuZ3RoOysrcjxuOyllLnF1ZXVlW3JdLmNhbGxSZWplY3RlZCh0'
    'KTtyZXR1cm4gZX0sdS5yZXNvbHZlPWZ1bmN0aW9uKGUpe3JldHVybiBlIGlu'
    'c3RhbmNlb2YgdGhpcz9lOnMucmVzb2x2ZShuZXcgdGhpcyhpKSxlKX0sdS5y'
    'ZWplY3Q9ZnVuY3Rpb24oZSl7dmFyIHQ9bmV3IHRoaXMoaSk7cmV0dXJuIHMu'
    'cmVqZWN0KHQsZSl9LHUuYWxsPWZ1bmN0aW9uKGUpe3ZhciB0PXRoaXM7aWYo'
    'IltvYmplY3QgQXJyYXldIiE9PU9iamVjdC5wcm90b3R5cGUudG9TdHJpbmcu'
    'Y2FsbChlKSlyZXR1cm4gdGhpcy5yZWplY3QobmV3IFR5cGVFcnJvcigibXVz'
    'dCBiZSBhbiBhcnJheSIpKTt2YXIgcj1lLmxlbmd0aCxuPSExO2lmKCFyKXJl'
    'dHVybiB0aGlzLnJlc29sdmUoW10pO2Zvcih2YXIgbz1uZXcgQXJyYXkociks'
    'YT0wLGM9LTEsdT1uZXcgdGhpcyhpKTsrK2M8cjspbChlW2NdLGMpO3JldHVy'
    'biB1O2Z1bmN0aW9uIGwoZSxpKXt0LnJlc29sdmUoZSkudGhlbihmdW5jdGlv'
    'bihlKXtvW2ldPWUsKythIT09cnx8bnx8KG49ITAscy5yZXNvbHZlKHUsbykp'
    'fSxmdW5jdGlvbihlKXtufHwobj0hMCxzLnJlamVjdCh1LGUpKX0pfX0sdS5y'
    'YWNlPWZ1bmN0aW9uKGUpe3ZhciB0PXRoaXM7aWYoIltvYmplY3QgQXJyYXld'
    'IiE9PU9iamVjdC5wcm90b3R5cGUudG9TdHJpbmcuY2FsbChlKSlyZXR1cm4g'
    'dGhpcy5yZWplY3QobmV3IFR5cGVFcnJvcigibXVzdCBiZSBhbiBhcnJheSIp'
    'KTt2YXIgcj1lLmxlbmd0aCxuPSExO2lmKCFyKXJldHVybiB0aGlzLnJlc29s'
    'dmUoW10pO2Zvcih2YXIgbz0tMSxhPW5ldyB0aGlzKGkpLGM7KytvPHI7KWM9'
    'ZVtvXSx0LnJlc29sdmUoYykudGhlbihmdW5jdGlvbihlKXtufHwobj0hMCxz'
    'LnJlc29sdmUoYSxlKSl9LGZ1bmN0aW9uKGUpe258fChuPSEwLHMucmVqZWN0'
    'KGEsZSkpfSk7cmV0dXJuIGF9fSx7aW1tZWRpYXRlOjM2fV0sMzg6W2Z1bmN0'
    'aW9uKGUsdCxyKXt2YXIgbj17fTsoMCxlKCIuL2xpYi91dGlscy9jb21tb24i'
    'KS5hc3NpZ24pKG4sZSgiLi9saWIvZGVmbGF0ZSIpLGUoIi4vbGliL2luZmxh'
    'dGUiKSxlKCIuL2xpYi96bGliL2NvbnN0YW50cyIpKSx0LmV4cG9ydHM9bn0s'
    'eyIuL2xpYi9kZWZsYXRlIjozOSwiLi9saWIvaW5mbGF0ZSI6NDAsIi4vbGli'
    'L3V0aWxzL2NvbW1vbiI6NDEsIi4vbGliL3psaWIvY29uc3RhbnRzIjo0NH1d'
    'LDM5OltmdW5jdGlvbihlLHQscil7dmFyIG49ZSgiLi96bGliL2RlZmxhdGUi'
    'KSxpPWUoIi4vdXRpbHMvY29tbW9uIikscz1lKCIuL3V0aWxzL3N0cmluZ3Mi'
    'KSxvPWUoIi4vemxpYi9tZXNzYWdlcyIpLGE9ZSgiLi96bGliL3pzdHJlYW0i'
    'KSxjPU9iamVjdC5wcm90b3R5cGUudG9TdHJpbmcsdT0wLGw9LTEsZD0wLHc9'
    'ODtmdW5jdGlvbiBoKGUpe2lmKCEodGhpcyBpbnN0YW5jZW9mIGgpKXJldHVy'
    'biBuZXcgaChlKTt0aGlzLm9wdGlvbnM9aS5hc3NpZ24oe2xldmVsOmwsbWV0'
    'aG9kOjgsY2h1bmtTaXplOjE2Mzg0LHdpbmRvd0JpdHM6MTUsbWVtTGV2ZWw6'
    'OCxzdHJhdGVneTowLHRvOiIifSxlfHx7fSk7dmFyIHQ9dGhpcy5vcHRpb25z'
    'O3QucmF3JiYwPHQud2luZG93Qml0cz90LndpbmRvd0JpdHM9LXQud2luZG93'
    'Qml0czp0Lmd6aXAmJjA8dC53aW5kb3dCaXRzJiZ0LndpbmRvd0JpdHM8MTYm'
    'Jih0LndpbmRvd0JpdHMrPTE2KSx0aGlzLmVycj0wLHRoaXMubXNnPSIiLHRo'
    'aXMuZW5kZWQ9ITEsdGhpcy5jaHVua3M9W10sdGhpcy5zdHJtPW5ldyBhLHRo'
    'aXMuc3RybS5hdmFpbF9vdXQ9MDt2YXIgcj1uLmRlZmxhdGVJbml0Mih0aGlz'
    'LnN0cm0sdC5sZXZlbCx0Lm1ldGhvZCx0LndpbmRvd0JpdHMsdC5tZW1MZXZl'
    'bCx0LnN0cmF0ZWd5KTtpZigwIT09cil0aHJvdyBuZXcgRXJyb3Iob1tyXSk7'
    'aWYodC5oZWFkZXImJm4uZGVmbGF0ZVNldEhlYWRlcih0aGlzLnN0cm0sdC5o'
    'ZWFkZXIpLHQuZGljdGlvbmFyeSl7dmFyIHU7aWYodT0ic3RyaW5nIj09dHlw'
    'ZW9mIHQuZGljdGlvbmFyeT9zLnN0cmluZzJidWYodC5kaWN0aW9uYXJ5KToi'
    'W29iamVjdCBBcnJheUJ1ZmZlcl0iPT09Yy5jYWxsKHQuZGljdGlvbmFyeSk/'
    'bmV3IFVpbnQ4QXJyYXkodC5kaWN0aW9uYXJ5KTp0LmRpY3Rpb25hcnksMCE9'
    'PShyPW4uZGVmbGF0ZVNldERpY3Rpb25hcnkodGhpcy5zdHJtLHUpKSl0aHJv'
    'dyBuZXcgRXJyb3Iob1tyXSk7dGhpcy5fZGljdF9zZXQ9ITB9fWZ1bmN0aW9u'
    'IGYoZSx0KXt2YXIgcj1uZXcgaCh0KTtpZihyLnB1c2goZSwhMCksci5lcnIp'
    'dGhyb3cgci5tc2d8fG9bci5lcnJdO3JldHVybiByLnJlc3VsdH1oLnByb3Rv'
    'dHlwZS5wdXNoPWZ1bmN0aW9uKGUsdCl7dmFyIHIsbyxhPXRoaXMuc3RybSx1'
    'PXRoaXMub3B0aW9ucy5jaHVua1NpemU7aWYodGhpcy5lbmRlZClyZXR1cm4h'
    'MTtvPXQ9PT1+fnQ/dDohMD09PXQ/NDowLCJzdHJpbmciPT10eXBlb2YgZT9h'
    'LmlucHV0PXMuc3RyaW5nMmJ1ZihlKToiW29iamVjdCBBcnJheUJ1ZmZlcl0i'
    'PT09Yy5jYWxsKGUpP2EuaW5wdXQ9bmV3IFVpbnQ4QXJyYXkoZSk6YS5pbnB1'
    'dD1lLGEubmV4dF9pbj0wLGEuYXZhaWxfaW49YS5pbnB1dC5sZW5ndGg7ZG97'
    'aWYoMD09PWEuYXZhaWxfb3V0JiYoYS5vdXRwdXQ9bmV3IGkuQnVmOCh1KSxh'
    'Lm5leHRfb3V0PTAsYS5hdmFpbF9vdXQ9dSksMSE9PShyPW4uZGVmbGF0ZShh'
    'LG8pKSYmMCE9PXIpcmV0dXJuIHRoaXMub25FbmQociksISh0aGlzLmVuZGVk'
    'PSEwKTswIT09YS5hdmFpbF9vdXQmJigwIT09YS5hdmFpbF9pbnx8NCE9PW8m'
    'JjIhPT1vKXx8KCJzdHJpbmciPT09dGhpcy5vcHRpb25zLnRvP3RoaXMub25E'
    'YXRhKHMuYnVmMmJpbnN0cmluZyhpLnNocmlua0J1ZihhLm91dHB1dCxhLm5l'
    'eHRfb3V0KSkpOnRoaXMub25EYXRhKGkuc2hyaW5rQnVmKGEub3V0cHV0LGEu'
    'bmV4dF9vdXQpKSl9d2hpbGUoKDA8YS5hdmFpbF9pbnx8MD09PWEuYXZhaWxf'
    'b3V0KSYmMSE9PXIpO3JldHVybiA0PT09bz8ocj1uLmRlZmxhdGVFbmQodGhp'
    'cy5zdHJtKSx0aGlzLm9uRW5kKHIpLHRoaXMuZW5kZWQ9ITAsMD09PXIpOjIh'
    'PT1vfHwodGhpcy5vbkVuZCgwKSwhKGEuYXZhaWxfb3V0PTApKX0saC5wcm90'
    'b3R5cGUub25EYXRhPWZ1bmN0aW9uKGUpe3RoaXMuY2h1bmtzLnB1c2goZSl9'
    'LGgucHJvdG90eXBlLm9uRW5kPWZ1bmN0aW9uKGUpezA9PT1lJiYoInN0cmlu'
    'ZyI9PT10aGlzLm9wdGlvbnMudG8/dGhpcy5yZXN1bHQ9dGhpcy5jaHVua3Mu'
    'am9pbigiIik6dGhpcy5yZXN1bHQ9aS5mbGF0dGVuQ2h1bmtzKHRoaXMuY2h1'
    'bmtzKSksdGhpcy5jaHVua3M9W10sdGhpcy5lcnI9ZSx0aGlzLm1zZz10aGlz'
    'LnN0cm0ubXNnfSxyLkRlZmxhdGU9aCxyLmRlZmxhdGU9ZixyLmRlZmxhdGVS'
    'YXc9ZnVuY3Rpb24oZSx0KXtyZXR1cm4odD10fHx7fSkucmF3PSEwLGYoZSx0'
    'KX0sci5nemlwPWZ1bmN0aW9uKGUsdCl7cmV0dXJuKHQ9dHx8e30pLmd6aXA9'
    'ITAsZihlLHQpfX0seyIuL3V0aWxzL2NvbW1vbiI6NDEsIi4vdXRpbHMvc3Ry'
    'aW5ncyI6NDIsIi4vemxpYi9kZWZsYXRlIjo0NiwiLi96bGliL21lc3NhZ2Vz'
    'Ijo1MSwiLi96bGliL3pzdHJlYW0iOjUzfV0sNDA6W2Z1bmN0aW9uKGUsdCxy'
    'KXt2YXIgbj1lKCIuL3psaWIvaW5mbGF0ZSIpLGk9ZSgiLi91dGlscy9jb21t'
    'b24iKSxzPWUoIi4vdXRpbHMvc3RyaW5ncyIpLG89ZSgiLi96bGliL2NvbnN0'
    'YW50cyIpLGE9ZSgiLi96bGliL21lc3NhZ2VzIiksYz1lKCIuL3psaWIvenN0'
    'cmVhbSIpLHU9ZSgiLi96bGliL2d6aGVhZGVyIiksbD1PYmplY3QucHJvdG90'
    'eXBlLnRvU3RyaW5nO2Z1bmN0aW9uIGQoZSl7aWYoISh0aGlzIGluc3RhbmNl'
    'b2YgZCkpcmV0dXJuIG5ldyBkKGUpO3RoaXMub3B0aW9ucz1pLmFzc2lnbih7'
    'Y2h1bmtTaXplOjE2Mzg0LHdpbmRvd0JpdHM6MCx0bzoiIn0sZXx8e30pO3Zh'
    'ciB0PXRoaXMub3B0aW9uczt0LnJhdyYmMDw9dC53aW5kb3dCaXRzJiZ0Lndp'
    'bmRvd0JpdHM8MTYmJih0LndpbmRvd0JpdHM9LXQud2luZG93Qml0cywwPT09'
    'dC53aW5kb3dCaXRzJiYodC53aW5kb3dCaXRzPS0xNSkpLCEoMDw9dC53aW5k'
    'b3dCaXRzJiZ0LndpbmRvd0JpdHM8MTYpfHxlJiZlLndpbmRvd0JpdHN8fCh0'
    'LndpbmRvd0JpdHMrPTMyKSwxNTx0LndpbmRvd0JpdHMmJnQud2luZG93Qml0'
    'czw0OCYmISgxNSZ0LndpbmRvd0JpdHMpJiYodC53aW5kb3dCaXRzfD0xNSks'
    'dGhpcy5lcnI9MCx0aGlzLm1zZz0iIix0aGlzLmVuZGVkPSExLHRoaXMuY2h1'
    'bmtzPVtdLHRoaXMuc3RybT1uZXcgYyx0aGlzLnN0cm0uYXZhaWxfb3V0PTA7'
    'dmFyIHI9bi5pbmZsYXRlSW5pdDIodGhpcy5zdHJtLHQud2luZG93Qml0cyk7'
    'aWYociE9PW8uWl9PSyl0aHJvdyBuZXcgRXJyb3IoYVtyXSk7dGhpcy5oZWFk'
    'ZXI9bmV3IHUsbi5pbmZsYXRlR2V0SGVhZGVyKHRoaXMuc3RybSx0aGlzLmhl'
    'YWRlcil9ZnVuY3Rpb24gdyhlLHQpe3ZhciByPW5ldyBkKHQpO2lmKHIucHVz'
    'aChlLCEwKSxyLmVycil0aHJvdyByLm1zZ3x8YVtyLmVycl07cmV0dXJuIHIu'
    'cmVzdWx0fWQucHJvdG90eXBlLnB1c2g9ZnVuY3Rpb24oZSx0KXt2YXIgcixh'
    'LGMsdSxkLHcsaD10aGlzLnN0cm0sZj10aGlzLm9wdGlvbnMuY2h1bmtTaXpl'
    'LEE9dGhpcy5vcHRpb25zLmRpY3Rpb25hcnkscD0hMTtpZih0aGlzLmVuZGVk'
    'KXJldHVybiExO2E9dD09PX5+dD90OiEwPT09dD9vLlpfRklOSVNIOm8uWl9O'
    'T19GTFVTSCwic3RyaW5nIj09dHlwZW9mIGU/aC5pbnB1dD1zLmJpbnN0cmlu'
    'ZzJidWYoZSk6IltvYmplY3QgQXJyYXlCdWZmZXJdIj09PWwuY2FsbChlKT9o'
    'LmlucHV0PW5ldyBVaW50OEFycmF5KGUpOmguaW5wdXQ9ZSxoLm5leHRfaW49'
    'MCxoLmF2YWlsX2luPWguaW5wdXQubGVuZ3RoO2Rve2lmKDA9PT1oLmF2YWls'
    'X291dCYmKGgub3V0cHV0PW5ldyBpLkJ1ZjgoZiksaC5uZXh0X291dD0wLGgu'
    'YXZhaWxfb3V0PWYpLChyPW4uaW5mbGF0ZShoLG8uWl9OT19GTFVTSCkpPT09'
    'by5aX05FRURfRElDVCYmQSYmKHc9InN0cmluZyI9PXR5cGVvZiBBP3Muc3Ry'
    'aW5nMmJ1ZihBKToiW29iamVjdCBBcnJheUJ1ZmZlcl0iPT09bC5jYWxsKEEp'
    'P25ldyBVaW50OEFycmF5KEEpOkEscj1uLmluZmxhdGVTZXREaWN0aW9uYXJ5'
    'KHRoaXMuc3RybSx3KSkscj09PW8uWl9CVUZfRVJST1ImJiEwPT09cCYmKHI9'
    'by5aX09LLHA9ITEpLHIhPT1vLlpfU1RSRUFNX0VORCYmciE9PW8uWl9PSyly'
    'ZXR1cm4gdGhpcy5vbkVuZChyKSwhKHRoaXMuZW5kZWQ9ITApO2gubmV4dF9v'
    'dXQmJigwIT09aC5hdmFpbF9vdXQmJnIhPT1vLlpfU1RSRUFNX0VORCYmKDAh'
    'PT1oLmF2YWlsX2lufHxhIT09by5aX0ZJTklTSCYmYSE9PW8uWl9TWU5DX0ZM'
    'VVNIKXx8KCJzdHJpbmciPT09dGhpcy5vcHRpb25zLnRvPyhjPXMudXRmOGJv'
    'cmRlcihoLm91dHB1dCxoLm5leHRfb3V0KSx1PWgubmV4dF9vdXQtYyxkPXMu'
    'YnVmMnN0cmluZyhoLm91dHB1dCxjKSxoLm5leHRfb3V0PXUsaC5hdmFpbF9v'
    'dXQ9Zi11LHUmJmkuYXJyYXlTZXQoaC5vdXRwdXQsaC5vdXRwdXQsYyx1LDAp'
    'LHRoaXMub25EYXRhKGQpKTp0aGlzLm9uRGF0YShpLnNocmlua0J1ZihoLm91'
    'dHB1dCxoLm5leHRfb3V0KSkpKSwwPT09aC5hdmFpbF9pbiYmMD09PWguYXZh'
    'aWxfb3V0JiYocD0hMCl9d2hpbGUoKDA8aC5hdmFpbF9pbnx8MD09PWguYXZh'
    'aWxfb3V0KSYmciE9PW8uWl9TVFJFQU1fRU5EKTtyZXR1cm4gcj09PW8uWl9T'
    'VFJFQU1fRU5EJiYoYT1vLlpfRklOSVNIKSxhPT09by5aX0ZJTklTSD8ocj1u'
    'LmluZmxhdGVFbmQodGhpcy5zdHJtKSx0aGlzLm9uRW5kKHIpLHRoaXMuZW5k'
    'ZWQ9ITAscj09PW8uWl9PSyk6YSE9PW8uWl9TWU5DX0ZMVVNIfHwodGhpcy5v'
    'bkVuZChvLlpfT0spLCEoaC5hdmFpbF9vdXQ9MCkpfSxkLnByb3RvdHlwZS5v'
    'bkRhdGE9ZnVuY3Rpb24oZSl7dGhpcy5jaHVua3MucHVzaChlKX0sZC5wcm90'
    'b3R5cGUub25FbmQ9ZnVuY3Rpb24oZSl7ZT09PW8uWl9PSyYmKCJzdHJpbmci'
    'PT09dGhpcy5vcHRpb25zLnRvP3RoaXMucmVzdWx0PXRoaXMuY2h1bmtzLmpv'
    'aW4oIiIpOnRoaXMucmVzdWx0PWkuZmxhdHRlbkNodW5rcyh0aGlzLmNodW5r'
    'cykpLHRoaXMuY2h1bmtzPVtdLHRoaXMuZXJyPWUsdGhpcy5tc2c9dGhpcy5z'
    'dHJtLm1zZ30sci5JbmZsYXRlPWQsci5pbmZsYXRlPXcsci5pbmZsYXRlUmF3'
    'PWZ1bmN0aW9uKGUsdCl7cmV0dXJuKHQ9dHx8e30pLnJhdz0hMCx3KGUsdCl9'
    'LHIudW5nemlwPXd9LHsiLi91dGlscy9jb21tb24iOjQxLCIuL3V0aWxzL3N0'
    'cmluZ3MiOjQyLCIuL3psaWIvY29uc3RhbnRzIjo0NCwiLi96bGliL2d6aGVh'
    'ZGVyIjo0NywiLi96bGliL2luZmxhdGUiOjQ5LCIuL3psaWIvbWVzc2FnZXMi'
    'OjUxLCIuL3psaWIvenN0cmVhbSI6NTN9XSw0MTpbZnVuY3Rpb24oZSx0LHIp'
    'e3ZhciBuPSJ1bmRlZmluZWQiIT10eXBlb2YgVWludDhBcnJheSYmInVuZGVm'
    'aW5lZCIhPXR5cGVvZiBVaW50MTZBcnJheSYmInVuZGVmaW5lZCIhPXR5cGVv'
    'ZiBJbnQzMkFycmF5O3IuYXNzaWduPWZ1bmN0aW9uKGUpe2Zvcih2YXIgdD1B'
    'cnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChhcmd1bWVudHMsMSk7dC5sZW5n'
    'dGg7KXt2YXIgcj10LnNoaWZ0KCk7aWYocil7aWYoIm9iamVjdCIhPXR5cGVv'
    'ZiByKXRocm93IG5ldyBUeXBlRXJyb3IocisibXVzdCBiZSBub24tb2JqZWN0'
    'Iik7Zm9yKHZhciBuIGluIHIpci5oYXNPd25Qcm9wZXJ0eShuKSYmKGVbbl09'
    'cltuXSl9fXJldHVybiBlfSxyLnNocmlua0J1Zj1mdW5jdGlvbihlLHQpe3Jl'
    'dHVybiBlLmxlbmd0aD09PXQ/ZTplLnN1YmFycmF5P2Uuc3ViYXJyYXkoMCx0'
    'KTooZS5sZW5ndGg9dCxlKX07dmFyIGk9e2FycmF5U2V0OmZ1bmN0aW9uKGUs'
    'dCxyLG4saSl7aWYodC5zdWJhcnJheSYmZS5zdWJhcnJheSllLnNldCh0LnN1'
    'YmFycmF5KHIscituKSxpKTtlbHNlIGZvcih2YXIgcz0wO3M8bjtzKyspZVtp'
    'K3NdPXRbcitzXX0sZmxhdHRlbkNodW5rczpmdW5jdGlvbihlKXt2YXIgdCxy'
    'LG4saSxzLG87Zm9yKHQ9bj0wLHI9ZS5sZW5ndGg7dDxyO3QrKyluKz1lW3Rd'
    'Lmxlbmd0aDtmb3Iobz1uZXcgVWludDhBcnJheShuKSx0PWk9MCxyPWUubGVu'
    'Z3RoO3Q8cjt0Kyspcz1lW3RdLG8uc2V0KHMsaSksaSs9cy5sZW5ndGg7cmV0'
    'dXJuIG99fSxzPXthcnJheVNldDpmdW5jdGlvbihlLHQscixuLGkpe2Zvcih2'
    'YXIgcz0wO3M8bjtzKyspZVtpK3NdPXRbcitzXX0sZmxhdHRlbkNodW5rczpm'
    'dW5jdGlvbihlKXtyZXR1cm5bXS5jb25jYXQuYXBwbHkoW10sZSl9fTtyLnNl'
    'dFR5cGVkPWZ1bmN0aW9uKGUpe2U/KHIuQnVmOD1VaW50OEFycmF5LHIuQnVm'
    'MTY9VWludDE2QXJyYXksci5CdWYzMj1JbnQzMkFycmF5LHIuYXNzaWduKHIs'
    'aSkpOihyLkJ1Zjg9QXJyYXksci5CdWYxNj1BcnJheSxyLkJ1ZjMyPUFycmF5'
    'LHIuYXNzaWduKHIscykpfSxyLnNldFR5cGVkKG4pfSx7fV0sNDI6W2Z1bmN0'
    'aW9uKGUsdCxyKXt2YXIgbj1lKCIuL2NvbW1vbiIpLGk9ITAscz0hMDt0cnl7'
    'U3RyaW5nLmZyb21DaGFyQ29kZS5hcHBseShudWxsLFswXSl9Y2F0Y2goZSl7'
    'aT0hMX10cnl7U3RyaW5nLmZyb21DaGFyQ29kZS5hcHBseShudWxsLG5ldyBV'
    'aW50OEFycmF5KDEpKX1jYXRjaChlKXtzPSExfWZvcih2YXIgbz1uZXcgbi5C'
    'dWY4KDI1NiksYT0wO2E8MjU2O2ErKylvW2FdPTI1Mjw9YT82OjI0ODw9YT81'
    'OjI0MDw9YT80OjIyNDw9YT8zOjE5Mjw9YT8yOjE7ZnVuY3Rpb24gYyhlLHQp'
    'e2lmKHQ8NjU1MzcmJihlLnN1YmFycmF5JiZzfHwhZS5zdWJhcnJheSYmaSkp'
    'cmV0dXJuIFN0cmluZy5mcm9tQ2hhckNvZGUuYXBwbHkobnVsbCxuLnNocmlu'
    'a0J1ZihlLHQpKTtmb3IodmFyIHI9IiIsbz0wO288dDtvKyspcis9U3RyaW5n'
    'LmZyb21DaGFyQ29kZShlW29dKTtyZXR1cm4gcn1vWzI1NF09b1syNTRdPTEs'
    'ci5zdHJpbmcyYnVmPWZ1bmN0aW9uKGUpe3ZhciB0LHIsaSxzLG8sYT1lLmxl'
    'bmd0aCxjPTA7Zm9yKHM9MDtzPGE7cysrKTU1Mjk2PT0oNjQ1MTImKHI9ZS5j'
    'aGFyQ29kZUF0KHMpKSkmJnMrMTxhJiY1NjMyMD09KDY0NTEyJihpPWUuY2hh'
    'ckNvZGVBdChzKzEpKSkmJihyPTY1NTM2KyhyLTU1Mjk2PDwxMCkrKGktNTYz'
    'MjApLHMrKyksYys9cjwxMjg/MTpyPDIwNDg/MjpyPDY1NTM2PzM6NDtmb3Io'
    'dD1uZXcgbi5CdWY4KGMpLHM9bz0wO288YztzKyspNTUyOTY9PSg2NDUxMiYo'
    'cj1lLmNoYXJDb2RlQXQocykpKSYmcysxPGEmJjU2MzIwPT0oNjQ1MTImKGk9'
    'ZS5jaGFyQ29kZUF0KHMrMSkpKSYmKHI9NjU1MzYrKHItNTUyOTY8PDEwKSso'
    'aS01NjMyMCkscysrKSxyPDEyOD90W28rK109cjoocjwyMDQ4P3RbbysrXT0x'
    'OTJ8cj4+PjY6KHI8NjU1MzY/dFtvKytdPTIyNHxyPj4+MTI6KHRbbysrXT0y'
    'NDB8cj4+PjE4LHRbbysrXT0xMjh8cj4+PjEyJjYzKSx0W28rK109MTI4fHI+'
    'Pj42JjYzKSx0W28rK109MTI4fDYzJnIpO3JldHVybiB0fSxyLmJ1ZjJiaW5z'
    'dHJpbmc9ZnVuY3Rpb24oZSl7cmV0dXJuIGMoZSxlLmxlbmd0aCl9LHIuYmlu'
    'c3RyaW5nMmJ1Zj1mdW5jdGlvbihlKXtmb3IodmFyIHQ9bmV3IG4uQnVmOChl'
    'Lmxlbmd0aCkscj0wLGk9dC5sZW5ndGg7cjxpO3IrKyl0W3JdPWUuY2hhckNv'
    'ZGVBdChyKTtyZXR1cm4gdH0sci5idWYyc3RyaW5nPWZ1bmN0aW9uKGUsdCl7'
    'dmFyIHIsbixpLHMsYT10fHxlLmxlbmd0aCx1PW5ldyBBcnJheSgyKmEpO2Zv'
    'cihyPW49MDtyPGE7KWlmKChpPWVbcisrXSk8MTI4KXVbbisrXT1pO2Vsc2Ug'
    'aWYoNDwocz1vW2ldKSl1W24rK109NjU1MzMscis9cy0xO2Vsc2V7Zm9yKGkm'
    'PTI9PT1zPzMxOjM9PT1zPzE1Ojc7MTxzJiZyPGE7KWk9aTw8Nnw2MyZlW3Ir'
    'K10scy0tOzE8cz91W24rK109NjU1MzM6aTw2NTUzNj91W24rK109aTooaS09'
    'NjU1MzYsdVtuKytdPTU1Mjk2fGk+PjEwJjEwMjMsdVtuKytdPTU2MzIwfDEw'
    'MjMmaSl9cmV0dXJuIGModSxuKX0sci51dGY4Ym9yZGVyPWZ1bmN0aW9uKGUs'
    'dCl7dmFyIHI7Zm9yKCh0PXR8fGUubGVuZ3RoKT5lLmxlbmd0aCYmKHQ9ZS5s'
    'ZW5ndGgpLHI9dC0xOzA8PXImJjEyOD09KDE5MiZlW3JdKTspci0tO3JldHVy'
    'biByPDB8fDA9PT1yP3Q6citvW2Vbcl1dPnQ/cjp0fX0seyIuL2NvbW1vbiI6'
    'NDF9XSw0MzpbZnVuY3Rpb24oZSx0LHIpe3QuZXhwb3J0cz1mdW5jdGlvbihl'
    'LHQscixuKXtmb3IodmFyIGk9NjU1MzUmZSxzPWU+Pj4xNiY2NTUzNSxvPTA7'
    'MCE9PXI7KXtmb3Ioci09bz0yZTM8cj8yZTM6cjtzPXMrKGk9aSt0W24rK118'
    'MCl8MCwtLW87KTtpJT02NTUyMSxzJT02NTUyMX1yZXR1cm4gaXxzPDwxNn19'
    'LHt9XSw0NDpbZnVuY3Rpb24oZSx0LHIpe3QuZXhwb3J0cz17Wl9OT19GTFVT'
    'SDowLFpfUEFSVElBTF9GTFVTSDoxLFpfU1lOQ19GTFVTSDoyLFpfRlVMTF9G'
    'TFVTSDozLFpfRklOSVNIOjQsWl9CTE9DSzo1LFpfVFJFRVM6NixaX09LOjAs'
    'Wl9TVFJFQU1fRU5EOjEsWl9ORUVEX0RJQ1Q6MixaX0VSUk5POi0xLFpfU1RS'
    'RUFNX0VSUk9SOi0yLFpfREFUQV9FUlJPUjotMyxaX0JVRl9FUlJPUjotNSxa'
    'X05PX0NPTVBSRVNTSU9OOjAsWl9CRVNUX1NQRUVEOjEsWl9CRVNUX0NPTVBS'
    'RVNTSU9OOjksWl9ERUZBVUxUX0NPTVBSRVNTSU9OOi0xLFpfRklMVEVSRUQ6'
    'MSxaX0hVRkZNQU5fT05MWToyLFpfUkxFOjMsWl9GSVhFRDo0LFpfREVGQVVM'
    'VF9TVFJBVEVHWTowLFpfQklOQVJZOjAsWl9URVhUOjEsWl9VTktOT1dOOjIs'
    'Wl9ERUZMQVRFRDo4fX0se31dLDQ1OltmdW5jdGlvbihlLHQscil7dmFyIG49'
    'ZnVuY3Rpb24oKXtmb3IodmFyIGUsdD1bXSxyPTA7cjwyNTY7cisrKXtlPXI7'
    'Zm9yKHZhciBuPTA7bjw4O24rKyllPTEmZT8zOTg4MjkyMzg0XmU+Pj4xOmU+'
    'Pj4xO3Rbcl09ZX1yZXR1cm4gdH0oKTt0LmV4cG9ydHM9ZnVuY3Rpb24oZSx0'
    'LHIsaSl7dmFyIHM9bixvPWkrcjtlXj0tMTtmb3IodmFyIGE9aTthPG87YSsr'
    'KWU9ZT4+Pjhec1syNTUmKGVedFthXSldO3JldHVybi0xXmV9fSx7fV0sNDY6'
    'W2Z1bmN0aW9uKGUsdCxyKXt2YXIgbixpPWUoIi4uL3V0aWxzL2NvbW1vbiIp'
    'LHM9ZSgiLi90cmVlcyIpLG89ZSgiLi9hZGxlcjMyIiksYT1lKCIuL2NyYzMy'
    'IiksYz1lKCIuL21lc3NhZ2VzIiksdT0wLGw9NCxkPTAsdz0tMixoPS0xLGY9'
    'NCxBPTIscD04LEU9OSxCPTI4NixIPTMwLG09MTksZz01NzMseT0xNSxUPTMs'
    'eD0yNTgsdj0yNjIsYj00MixSPTExMyxNPTEsaz0yLFM9MyxDPTQ7ZnVuY3Rp'
    'b24gXyhlLHQpe3JldHVybiBlLm1zZz1jW3RdLHR9ZnVuY3Rpb24gTyhlKXty'
    'ZXR1cm4oZTw8MSktKDQ8ZT85OjApfWZ1bmN0aW9uIFAoZSl7Zm9yKHZhciB0'
    'PWUubGVuZ3RoOzA8PS0tdDspZVt0XT0wfWZ1bmN0aW9uIEwoZSl7dmFyIHQ9'
    'ZS5zdGF0ZSxyPXQucGVuZGluZztyPmUuYXZhaWxfb3V0JiYocj1lLmF2YWls'
    'X291dCksMCE9PXImJihpLmFycmF5U2V0KGUub3V0cHV0LHQucGVuZGluZ19i'
    'dWYsdC5wZW5kaW5nX291dCxyLGUubmV4dF9vdXQpLGUubmV4dF9vdXQrPXIs'
    'dC5wZW5kaW5nX291dCs9cixlLnRvdGFsX291dCs9cixlLmF2YWlsX291dC09'
    'cix0LnBlbmRpbmctPXIsMD09PXQucGVuZGluZyYmKHQucGVuZGluZ19vdXQ9'
    'MCkpfWZ1bmN0aW9uIEkoZSx0KXtzLl90cl9mbHVzaF9ibG9jayhlLDA8PWUu'
    'YmxvY2tfc3RhcnQ/ZS5ibG9ja19zdGFydDotMSxlLnN0cnN0YXJ0LWUuYmxv'
    'Y2tfc3RhcnQsdCksZS5ibG9ja19zdGFydD1lLnN0cnN0YXJ0LEwoZS5zdHJt'
    'KX1mdW5jdGlvbiBEKGUsdCl7ZS5wZW5kaW5nX2J1ZltlLnBlbmRpbmcrK109'
    'dH1mdW5jdGlvbiBVKGUsdCl7ZS5wZW5kaW5nX2J1ZltlLnBlbmRpbmcrK109'
    'dD4+PjgmMjU1LGUucGVuZGluZ19idWZbZS5wZW5kaW5nKytdPTI1NSZ0fWZ1'
    'bmN0aW9uIE4oZSx0KXt2YXIgcixuLGk9ZS5tYXhfY2hhaW5fbGVuZ3RoLHM9'
    'ZS5zdHJzdGFydCxvPWUucHJldl9sZW5ndGgsYT1lLm5pY2VfbWF0Y2gsYz1l'
    'LnN0cnN0YXJ0PmUud19zaXplLXY/ZS5zdHJzdGFydC0oZS53X3NpemUtdik6'
    'MCx1PWUud2luZG93LGw9ZS53X21hc2ssZD1lLnByZXYsdz1lLnN0cnN0YXJ0'
    'K3gsaD11W3Mrby0xXSxmPXVbcytvXTtlLnByZXZfbGVuZ3RoPj1lLmdvb2Rf'
    'bWF0Y2gmJihpPj49MiksYT5lLmxvb2thaGVhZCYmKGE9ZS5sb29rYWhlYWQp'
    'O2Rve2lmKHVbKHI9dCkrb109PT1mJiZ1W3Irby0xXT09PWgmJnVbcl09PT11'
    'W3NdJiZ1Wysrcl09PT11W3MrMV0pe3MrPTIscisrO2Rve313aGlsZSh1Wysr'
    'c109PT11Wysrcl0mJnVbKytzXT09PXVbKytyXSYmdVsrK3NdPT09dVsrK3Jd'
    'JiZ1Wysrc109PT11Wysrcl0mJnVbKytzXT09PXVbKytyXSYmdVsrK3NdPT09'
    'dVsrK3JdJiZ1Wysrc109PT11Wysrcl0mJnVbKytzXT09PXVbKytyXSYmczx3'
    'KTtpZihuPXgtKHctcykscz13LXgsbzxuKXtpZihlLm1hdGNoX3N0YXJ0PXQs'
    'YTw9KG89bikpYnJlYWs7aD11W3Mrby0xXSxmPXVbcytvXX19fXdoaWxlKCh0'
    'PWRbdCZsXSk+YyYmMCE9LS1pKTtyZXR1cm4gbzw9ZS5sb29rYWhlYWQ/bzpl'
    'Lmxvb2thaGVhZH1mdW5jdGlvbiB6KGUpe3ZhciB0LHIsbixzLGMsdSxsLGQs'
    'dyxoLGY9ZS53X3NpemU7ZG97aWYocz1lLndpbmRvd19zaXplLWUubG9va2Fo'
    'ZWFkLWUuc3Ryc3RhcnQsZS5zdHJzdGFydD49ZisoZi12KSl7Zm9yKGkuYXJy'
    'YXlTZXQoZS53aW5kb3csZS53aW5kb3csZixmLDApLGUubWF0Y2hfc3RhcnQt'
    'PWYsZS5zdHJzdGFydC09ZixlLmJsb2NrX3N0YXJ0LT1mLHQ9cj1lLmhhc2hf'
    'c2l6ZTtuPWUuaGVhZFstLXRdLGUuaGVhZFt0XT1mPD1uP24tZjowLC0tcjsp'
    'O2Zvcih0PXI9ZjtuPWUucHJldlstLXRdLGUucHJldlt0XT1mPD1uP24tZjow'
    'LC0tcjspO3MrPWZ9aWYoMD09PWUuc3RybS5hdmFpbF9pbilicmVhaztpZih1'
    'PWUuc3RybSxsPWUud2luZG93LGQ9ZS5zdHJzdGFydCtlLmxvb2thaGVhZCxo'
    'PXZvaWQgMCwodz1zKTwoaD11LmF2YWlsX2luKSYmKGg9dykscj0wPT09aD8w'
    'Oih1LmF2YWlsX2luLT1oLGkuYXJyYXlTZXQobCx1LmlucHV0LHUubmV4dF9p'
    'bixoLGQpLDE9PT11LnN0YXRlLndyYXA/dS5hZGxlcj1vKHUuYWRsZXIsbCxo'
    'LGQpOjI9PT11LnN0YXRlLndyYXAmJih1LmFkbGVyPWEodS5hZGxlcixsLGgs'
    'ZCkpLHUubmV4dF9pbis9aCx1LnRvdGFsX2luKz1oLGgpLGUubG9va2FoZWFk'
    'Kz1yLGUubG9va2FoZWFkK2UuaW5zZXJ0Pj0zKWZvcihjPWUuc3Ryc3RhcnQt'
    'ZS5pbnNlcnQsZS5pbnNfaD1lLndpbmRvd1tjXSxlLmluc19oPShlLmluc19o'
    'PDxlLmhhc2hfc2hpZnReZS53aW5kb3dbYysxXSkmZS5oYXNoX21hc2s7ZS5p'
    'bnNlcnQmJihlLmluc19oPShlLmluc19oPDxlLmhhc2hfc2hpZnReZS53aW5k'
    'b3dbYyszLTFdKSZlLmhhc2hfbWFzayxlLnByZXZbYyZlLndfbWFza109ZS5o'
    'ZWFkW2UuaW5zX2hdLGUuaGVhZFtlLmluc19oXT1jLGMrKyxlLmluc2VydC0t'
    'LCEoZS5sb29rYWhlYWQrZS5pbnNlcnQ8MykpOyk7fXdoaWxlKGUubG9va2Fo'
    'ZWFkPHYmJjAhPT1lLnN0cm0uYXZhaWxfaW4pfWZ1bmN0aW9uIFgoZSx0KXtm'
    'b3IodmFyIHIsbjs7KXtpZihlLmxvb2thaGVhZDx2KXtpZih6KGUpLGUubG9v'
    'a2FoZWFkPHYmJjA9PT10KXJldHVybiAxO2lmKDA9PT1lLmxvb2thaGVhZCli'
    'cmVha31pZihyPTAsZS5sb29rYWhlYWQ+PTMmJihlLmluc19oPShlLmluc19o'
    'PDxlLmhhc2hfc2hpZnReZS53aW5kb3dbZS5zdHJzdGFydCszLTFdKSZlLmhh'
    'c2hfbWFzayxyPWUucHJldltlLnN0cnN0YXJ0JmUud19tYXNrXT1lLmhlYWRb'
    'ZS5pbnNfaF0sZS5oZWFkW2UuaW5zX2hdPWUuc3Ryc3RhcnQpLDAhPT1yJiZl'
    'LnN0cnN0YXJ0LXI8PWUud19zaXplLXYmJihlLm1hdGNoX2xlbmd0aD1OKGUs'
    'cikpLGUubWF0Y2hfbGVuZ3RoPj0zKWlmKG49cy5fdHJfdGFsbHkoZSxlLnN0'
    'cnN0YXJ0LWUubWF0Y2hfc3RhcnQsZS5tYXRjaF9sZW5ndGgtMyksZS5sb29r'
    'YWhlYWQtPWUubWF0Y2hfbGVuZ3RoLGUubWF0Y2hfbGVuZ3RoPD1lLm1heF9s'
    'YXp5X21hdGNoJiZlLmxvb2thaGVhZD49Myl7Zm9yKGUubWF0Y2hfbGVuZ3Ro'
    'LS07ZS5zdHJzdGFydCsrLGUuaW5zX2g9KGUuaW5zX2g8PGUuaGFzaF9zaGlm'
    'dF5lLndpbmRvd1tlLnN0cnN0YXJ0KzMtMV0pJmUuaGFzaF9tYXNrLHI9ZS5w'
    'cmV2W2Uuc3Ryc3RhcnQmZS53X21hc2tdPWUuaGVhZFtlLmluc19oXSxlLmhl'
    'YWRbZS5pbnNfaF09ZS5zdHJzdGFydCwwIT0tLWUubWF0Y2hfbGVuZ3RoOyk7'
    'ZS5zdHJzdGFydCsrfWVsc2UgZS5zdHJzdGFydCs9ZS5tYXRjaF9sZW5ndGgs'
    'ZS5tYXRjaF9sZW5ndGg9MCxlLmluc19oPWUud2luZG93W2Uuc3Ryc3RhcnRd'
    'LGUuaW5zX2g9KGUuaW5zX2g8PGUuaGFzaF9zaGlmdF5lLndpbmRvd1tlLnN0'
    'cnN0YXJ0KzFdKSZlLmhhc2hfbWFzaztlbHNlIG49cy5fdHJfdGFsbHkoZSww'
    'LGUud2luZG93W2Uuc3Ryc3RhcnRdKSxlLmxvb2thaGVhZC0tLGUuc3Ryc3Rh'
    'cnQrKztpZihuJiYoSShlLCExKSwwPT09ZS5zdHJtLmF2YWlsX291dCkpcmV0'
    'dXJuIDF9cmV0dXJuIGUuaW5zZXJ0PWUuc3Ryc3RhcnQ8Mj9lLnN0cnN0YXJ0'
    'OjIsND09PXQ/KEkoZSwhMCksMD09PWUuc3RybS5hdmFpbF9vdXQ/Mzo0KTpl'
    'Lmxhc3RfbGl0JiYoSShlLCExKSwwPT09ZS5zdHJtLmF2YWlsX291dCk/MToy'
    'fWZ1bmN0aW9uIEYoZSx0KXtmb3IodmFyIHIsbixpOzspe2lmKGUubG9va2Fo'
    'ZWFkPHYpe2lmKHooZSksZS5sb29rYWhlYWQ8diYmMD09PXQpcmV0dXJuIDE7'
    'aWYoMD09PWUubG9va2FoZWFkKWJyZWFrfWlmKHI9MCxlLmxvb2thaGVhZD49'
    'MyYmKGUuaW5zX2g9KGUuaW5zX2g8PGUuaGFzaF9zaGlmdF5lLndpbmRvd1tl'
    'LnN0cnN0YXJ0KzMtMV0pJmUuaGFzaF9tYXNrLHI9ZS5wcmV2W2Uuc3Ryc3Rh'
    'cnQmZS53X21hc2tdPWUuaGVhZFtlLmluc19oXSxlLmhlYWRbZS5pbnNfaF09'
    'ZS5zdHJzdGFydCksZS5wcmV2X2xlbmd0aD1lLm1hdGNoX2xlbmd0aCxlLnBy'
    'ZXZfbWF0Y2g9ZS5tYXRjaF9zdGFydCxlLm1hdGNoX2xlbmd0aD0yLDAhPT1y'
    'JiZlLnByZXZfbGVuZ3RoPGUubWF4X2xhenlfbWF0Y2gmJmUuc3Ryc3RhcnQt'
    'cjw9ZS53X3NpemUtdiYmKGUubWF0Y2hfbGVuZ3RoPU4oZSxyKSxlLm1hdGNo'
    'X2xlbmd0aDw9NSYmKDE9PT1lLnN0cmF0ZWd5fHwzPT09ZS5tYXRjaF9sZW5n'
    'dGgmJjQwOTY8ZS5zdHJzdGFydC1lLm1hdGNoX3N0YXJ0KSYmKGUubWF0Y2hf'
    'bGVuZ3RoPTIpKSxlLnByZXZfbGVuZ3RoPj0zJiZlLm1hdGNoX2xlbmd0aDw9'
    'ZS5wcmV2X2xlbmd0aCl7Zm9yKGk9ZS5zdHJzdGFydCtlLmxvb2thaGVhZC0z'
    'LG49cy5fdHJfdGFsbHkoZSxlLnN0cnN0YXJ0LTEtZS5wcmV2X21hdGNoLGUu'
    'cHJldl9sZW5ndGgtMyksZS5sb29rYWhlYWQtPWUucHJldl9sZW5ndGgtMSxl'
    'LnByZXZfbGVuZ3RoLT0yOysrZS5zdHJzdGFydDw9aSYmKGUuaW5zX2g9KGUu'
    'aW5zX2g8PGUuaGFzaF9zaGlmdF5lLndpbmRvd1tlLnN0cnN0YXJ0KzMtMV0p'
    'JmUuaGFzaF9tYXNrLHI9ZS5wcmV2W2Uuc3Ryc3RhcnQmZS53X21hc2tdPWUu'
    'aGVhZFtlLmluc19oXSxlLmhlYWRbZS5pbnNfaF09ZS5zdHJzdGFydCksMCE9'
    'LS1lLnByZXZfbGVuZ3RoOyk7aWYoZS5tYXRjaF9hdmFpbGFibGU9MCxlLm1h'
    'dGNoX2xlbmd0aD0yLGUuc3Ryc3RhcnQrKyxuJiYoSShlLCExKSwwPT09ZS5z'
    'dHJtLmF2YWlsX291dCkpcmV0dXJuIDF9ZWxzZSBpZihlLm1hdGNoX2F2YWls'
    'YWJsZSl7aWYoKG49cy5fdHJfdGFsbHkoZSwwLGUud2luZG93W2Uuc3Ryc3Rh'
    'cnQtMV0pKSYmSShlLCExKSxlLnN0cnN0YXJ0KyssZS5sb29rYWhlYWQtLSww'
    'PT09ZS5zdHJtLmF2YWlsX291dClyZXR1cm4gMX1lbHNlIGUubWF0Y2hfYXZh'
    'aWxhYmxlPTEsZS5zdHJzdGFydCsrLGUubG9va2FoZWFkLS19cmV0dXJuIGUu'
    'bWF0Y2hfYXZhaWxhYmxlJiYobj1zLl90cl90YWxseShlLDAsZS53aW5kb3db'
    'ZS5zdHJzdGFydC0xXSksZS5tYXRjaF9hdmFpbGFibGU9MCksZS5pbnNlcnQ9'
    'ZS5zdHJzdGFydDwyP2Uuc3Ryc3RhcnQ6Miw0PT09dD8oSShlLCEwKSwwPT09'
    'ZS5zdHJtLmF2YWlsX291dD8zOjQpOmUubGFzdF9saXQmJihJKGUsITEpLDA9'
    'PT1lLnN0cm0uYXZhaWxfb3V0KT8xOjJ9ZnVuY3Rpb24gaihlLHQscixuLGkp'
    'e3RoaXMuZ29vZF9sZW5ndGg9ZSx0aGlzLm1heF9sYXp5PXQsdGhpcy5uaWNl'
    'X2xlbmd0aD1yLHRoaXMubWF4X2NoYWluPW4sdGhpcy5mdW5jPWl9ZnVuY3Rp'
    'b24gVygpe3RoaXMuc3RybT1udWxsLHRoaXMuc3RhdHVzPTAsdGhpcy5wZW5k'
    'aW5nX2J1Zj1udWxsLHRoaXMucGVuZGluZ19idWZfc2l6ZT0wLHRoaXMucGVu'
    'ZGluZ19vdXQ9MCx0aGlzLnBlbmRpbmc9MCx0aGlzLndyYXA9MCx0aGlzLmd6'
    'aGVhZD1udWxsLHRoaXMuZ3ppbmRleD0wLHRoaXMubWV0aG9kPTgsdGhpcy5s'
    'YXN0X2ZsdXNoPS0xLHRoaXMud19zaXplPTAsdGhpcy53X2JpdHM9MCx0aGlz'
    'LndfbWFzaz0wLHRoaXMud2luZG93PW51bGwsdGhpcy53aW5kb3dfc2l6ZT0w'
    'LHRoaXMucHJldj1udWxsLHRoaXMuaGVhZD1udWxsLHRoaXMuaW5zX2g9MCx0'
    'aGlzLmhhc2hfc2l6ZT0wLHRoaXMuaGFzaF9iaXRzPTAsdGhpcy5oYXNoX21h'
    'c2s9MCx0aGlzLmhhc2hfc2hpZnQ9MCx0aGlzLmJsb2NrX3N0YXJ0PTAsdGhp'
    'cy5tYXRjaF9sZW5ndGg9MCx0aGlzLnByZXZfbWF0Y2g9MCx0aGlzLm1hdGNo'
    'X2F2YWlsYWJsZT0wLHRoaXMuc3Ryc3RhcnQ9MCx0aGlzLm1hdGNoX3N0YXJ0'
    'PTAsdGhpcy5sb29rYWhlYWQ9MCx0aGlzLnByZXZfbGVuZ3RoPTAsdGhpcy5t'
    'YXhfY2hhaW5fbGVuZ3RoPTAsdGhpcy5tYXhfbGF6eV9tYXRjaD0wLHRoaXMu'
    'bGV2ZWw9MCx0aGlzLnN0cmF0ZWd5PTAsdGhpcy5nb29kX21hdGNoPTAsdGhp'
    'cy5uaWNlX21hdGNoPTAsdGhpcy5keW5fbHRyZWU9bmV3IGkuQnVmMTYoMipn'
    'KSx0aGlzLmR5bl9kdHJlZT1uZXcgaS5CdWYxNigxMjIpLHRoaXMuYmxfdHJl'
    'ZT1uZXcgaS5CdWYxNig3OCksUCh0aGlzLmR5bl9sdHJlZSksUCh0aGlzLmR5'
    'bl9kdHJlZSksUCh0aGlzLmJsX3RyZWUpLHRoaXMubF9kZXNjPW51bGwsdGhp'
    'cy5kX2Rlc2M9bnVsbCx0aGlzLmJsX2Rlc2M9bnVsbCx0aGlzLmJsX2NvdW50'
    'PW5ldyBpLkJ1ZjE2KDE2KSx0aGlzLmhlYXA9bmV3IGkuQnVmMTYoNTczKSxQ'
    'KHRoaXMuaGVhcCksdGhpcy5oZWFwX2xlbj0wLHRoaXMuaGVhcF9tYXg9MCx0'
    'aGlzLmRlcHRoPW5ldyBpLkJ1ZjE2KDU3MyksUCh0aGlzLmRlcHRoKSx0aGlz'
    'LmxfYnVmPTAsdGhpcy5saXRfYnVmc2l6ZT0wLHRoaXMubGFzdF9saXQ9MCx0'
    'aGlzLmRfYnVmPTAsdGhpcy5vcHRfbGVuPTAsdGhpcy5zdGF0aWNfbGVuPTAs'
    'dGhpcy5tYXRjaGVzPTAsdGhpcy5pbnNlcnQ9MCx0aGlzLmJpX2J1Zj0wLHRo'
    'aXMuYmlfdmFsaWQ9MH1mdW5jdGlvbiBKKGUpe3ZhciB0O3JldHVybiBlJiZl'
    'LnN0YXRlPyhlLnRvdGFsX2luPWUudG90YWxfb3V0PTAsZS5kYXRhX3R5cGU9'
    'MiwodD1lLnN0YXRlKS5wZW5kaW5nPTAsdC5wZW5kaW5nX291dD0wLHQud3Jh'
    'cDwwJiYodC53cmFwPS10LndyYXApLHQuc3RhdHVzPXQud3JhcD9iOlIsZS5h'
    'ZGxlcj0yPT09dC53cmFwPzA6MSx0Lmxhc3RfZmx1c2g9MCxzLl90cl9pbml0'
    'KHQpLDApOl8oZSx3KX1mdW5jdGlvbiBLKGUpe3ZhciB0PUooZSkscjtyZXR1'
    'cm4gMD09PXQmJigocj1lLnN0YXRlKS53aW5kb3dfc2l6ZT0yKnIud19zaXpl'
    'LFAoci5oZWFkKSxyLm1heF9sYXp5X21hdGNoPW5bci5sZXZlbF0ubWF4X2xh'
    'enksci5nb29kX21hdGNoPW5bci5sZXZlbF0uZ29vZF9sZW5ndGgsci5uaWNl'
    'X21hdGNoPW5bci5sZXZlbF0ubmljZV9sZW5ndGgsci5tYXhfY2hhaW5fbGVu'
    'Z3RoPW5bci5sZXZlbF0ubWF4X2NoYWluLHIuc3Ryc3RhcnQ9MCxyLmJsb2Nr'
    'X3N0YXJ0PTAsci5sb29rYWhlYWQ9MCxyLmluc2VydD0wLHIubWF0Y2hfbGVu'
    'Z3RoPXIucHJldl9sZW5ndGg9MixyLm1hdGNoX2F2YWlsYWJsZT0wLHIuaW5z'
    'X2g9MCksdH1mdW5jdGlvbiBWKGUsdCxyLG4scyxvKXtpZighZSlyZXR1cm4g'
    'dzt2YXIgYT0xO2lmKHQ9PT1oJiYodD02KSxuPDA/KGE9MCxuPS1uKToxNTxu'
    'JiYoYT0yLG4tPTE2KSxzPDF8fDk8c3x8OCE9PXJ8fG48OHx8MTU8bnx8dDww'
    'fHw5PHR8fG88MHx8NDxvKXJldHVybiBfKGUsdyk7OD09PW4mJihuPTkpO3Zh'
    'ciBjPW5ldyBXO3JldHVybihlLnN0YXRlPWMpLnN0cm09ZSxjLndyYXA9YSxj'
    'Lmd6aGVhZD1udWxsLGMud19iaXRzPW4sYy53X3NpemU9MTw8Yy53X2JpdHMs'
    'Yy53X21hc2s9Yy53X3NpemUtMSxjLmhhc2hfYml0cz1zKzcsYy5oYXNoX3Np'
    'emU9MTw8Yy5oYXNoX2JpdHMsYy5oYXNoX21hc2s9Yy5oYXNoX3NpemUtMSxj'
    'Lmhhc2hfc2hpZnQ9fn4oKGMuaGFzaF9iaXRzKzMtMSkvMyksYy53aW5kb3c9'
    'bmV3IGkuQnVmOCgyKmMud19zaXplKSxjLmhlYWQ9bmV3IGkuQnVmMTYoYy5o'
    'YXNoX3NpemUpLGMucHJldj1uZXcgaS5CdWYxNihjLndfc2l6ZSksYy5saXRf'
    'YnVmc2l6ZT0xPDxzKzYsYy5wZW5kaW5nX2J1Zl9zaXplPTQqYy5saXRfYnVm'
    'c2l6ZSxjLnBlbmRpbmdfYnVmPW5ldyBpLkJ1ZjgoYy5wZW5kaW5nX2J1Zl9z'
    'aXplKSxjLmRfYnVmPTEqYy5saXRfYnVmc2l6ZSxjLmxfYnVmPTMqYy5saXRf'
    'YnVmc2l6ZSxjLmxldmVsPXQsYy5zdHJhdGVneT1vLGMubWV0aG9kPXIsSyhl'
    'KX1uPVtuZXcgaigwLDAsMCwwLGZ1bmN0aW9uKGUsdCl7dmFyIHI9NjU1MzU7'
    'Zm9yKHI+ZS5wZW5kaW5nX2J1Zl9zaXplLTUmJihyPWUucGVuZGluZ19idWZf'
    'c2l6ZS01KTs7KXtpZihlLmxvb2thaGVhZDw9MSl7aWYoeihlKSwwPT09ZS5s'
    'b29rYWhlYWQmJjA9PT10KXJldHVybiAxO2lmKDA9PT1lLmxvb2thaGVhZCli'
    'cmVha31lLnN0cnN0YXJ0Kz1lLmxvb2thaGVhZCxlLmxvb2thaGVhZD0wO3Zh'
    'ciBuPWUuYmxvY2tfc3RhcnQrcjtpZigoMD09PWUuc3Ryc3RhcnR8fGUuc3Ry'
    'c3RhcnQ+PW4pJiYoZS5sb29rYWhlYWQ9ZS5zdHJzdGFydC1uLGUuc3Ryc3Rh'
    'cnQ9bixJKGUsITEpLDA9PT1lLnN0cm0uYXZhaWxfb3V0KSlyZXR1cm4gMTtp'
    'ZihlLnN0cnN0YXJ0LWUuYmxvY2tfc3RhcnQ+PWUud19zaXplLXYmJihJKGUs'
    'ITEpLDA9PT1lLnN0cm0uYXZhaWxfb3V0KSlyZXR1cm4gMX1yZXR1cm4gZS5p'
    'bnNlcnQ9MCw0PT09dD8oSShlLCEwKSwwPT09ZS5zdHJtLmF2YWlsX291dD8z'
    'OjQpOihlLnN0cnN0YXJ0PmUuYmxvY2tfc3RhcnQmJihJKGUsITEpLGUuc3Ry'
    'bS5hdmFpbF9vdXQpLDEpfSksbmV3IGooNCw0LDgsNCxYKSxuZXcgaig0LDUs'
    'MTYsOCxYKSxuZXcgaig0LDYsMzIsMzIsWCksbmV3IGooNCw0LDE2LDE2LEYp'
    'LG5ldyBqKDgsMTYsMzIsMzIsRiksbmV3IGooOCwxNiwxMjgsMTI4LEYpLG5l'
    'dyBqKDgsMzIsMTI4LDI1NixGKSxuZXcgaigzMiwxMjgsMjU4LDEwMjQsRiks'
    'bmV3IGooMzIsMjU4LDI1OCw0MDk2LEYpXSxyLmRlZmxhdGVJbml0PWZ1bmN0'
    'aW9uKGUsdCl7cmV0dXJuIFYoZSx0LDgsMTUsOCwwKX0sci5kZWZsYXRlSW5p'
    'dDI9VixyLmRlZmxhdGVSZXNldD1LLHIuZGVmbGF0ZVJlc2V0S2VlcD1KLHIu'
    'ZGVmbGF0ZVNldEhlYWRlcj1mdW5jdGlvbihlLHQpe3JldHVybiBlJiZlLnN0'
    'YXRlPzIhPT1lLnN0YXRlLndyYXA/dzooZS5zdGF0ZS5nemhlYWQ9dCwwKTp3'
    'fSxyLmRlZmxhdGU9ZnVuY3Rpb24oZSx0KXt2YXIgcixpLG8sYztpZighZXx8'
    'IWUuc3RhdGV8fDU8dHx8dDwwKXJldHVybiBlP18oZSx3KTp3O2lmKGk9ZS5z'
    'dGF0ZSwhZS5vdXRwdXR8fCFlLmlucHV0JiYwIT09ZS5hdmFpbF9pbnx8NjY2'
    'PT09aS5zdGF0dXMmJjQhPT10KXJldHVybiBfKGUsMD09PWUuYXZhaWxfb3V0'
    'Py01OncpO2lmKGkuc3RybT1lLHI9aS5sYXN0X2ZsdXNoLGkubGFzdF9mbHVz'
    'aD10LGkuc3RhdHVzPT09YilpZigyPT09aS53cmFwKWUuYWRsZXI9MCxEKGks'
    'MzEpLEQoaSwxMzkpLEQoaSw4KSxpLmd6aGVhZD8oRChpLChpLmd6aGVhZC50'
    'ZXh0PzE6MCkrKGkuZ3poZWFkLmhjcmM/MjowKSsoaS5nemhlYWQuZXh0cmE/'
    'NDowKSsoaS5nemhlYWQubmFtZT84OjApKyhpLmd6aGVhZC5jb21tZW50PzE2'
    'OjApKSxEKGksMjU1JmkuZ3poZWFkLnRpbWUpLEQoaSxpLmd6aGVhZC50aW1l'
    'Pj44JjI1NSksRChpLGkuZ3poZWFkLnRpbWU+PjE2JjI1NSksRChpLGkuZ3po'
    'ZWFkLnRpbWU+PjI0JjI1NSksRChpLDk9PT1pLmxldmVsPzI6Mjw9aS5zdHJh'
    'dGVneXx8aS5sZXZlbDwyPzQ6MCksRChpLDI1NSZpLmd6aGVhZC5vcyksaS5n'
    'emhlYWQuZXh0cmEmJmkuZ3poZWFkLmV4dHJhLmxlbmd0aCYmKEQoaSwyNTUm'
    'aS5nemhlYWQuZXh0cmEubGVuZ3RoKSxEKGksaS5nemhlYWQuZXh0cmEubGVu'
    'Z3RoPj44JjI1NSkpLGkuZ3poZWFkLmhjcmMmJihlLmFkbGVyPWEoZS5hZGxl'
    'cixpLnBlbmRpbmdfYnVmLGkucGVuZGluZywwKSksaS5nemluZGV4PTAsaS5z'
    'dGF0dXM9NjkpOihEKGksMCksRChpLDApLEQoaSwwKSxEKGksMCksRChpLDAp'
    'LEQoaSw5PT09aS5sZXZlbD8yOjI8PWkuc3RyYXRlZ3l8fGkubGV2ZWw8Mj80'
    'OjApLEQoaSwzKSxpLnN0YXR1cz1SKTtlbHNle3ZhciB1PTgrKGkud19iaXRz'
    'LTg8PDQpPDw4O3V8PSgyPD1pLnN0cmF0ZWd5fHxpLmxldmVsPDI/MDppLmxl'
    'dmVsPDY/MTo2PT09aS5sZXZlbD8yOjMpPDw2LDAhPT1pLnN0cnN0YXJ0JiYo'
    'dXw9MzIpLHUrPTMxLXUlMzEsaS5zdGF0dXM9UixVKGksdSksMCE9PWkuc3Ry'
    'c3RhcnQmJihVKGksZS5hZGxlcj4+PjE2KSxVKGksNjU1MzUmZS5hZGxlcikp'
    'LGUuYWRsZXI9MX1pZig2OT09PWkuc3RhdHVzKWlmKGkuZ3poZWFkLmV4dHJh'
    'KXtmb3Iobz1pLnBlbmRpbmc7aS5nemluZGV4PCg2NTUzNSZpLmd6aGVhZC5l'
    'eHRyYS5sZW5ndGgpJiYoaS5wZW5kaW5nIT09aS5wZW5kaW5nX2J1Zl9zaXpl'
    'fHwoaS5nemhlYWQuaGNyYyYmaS5wZW5kaW5nPm8mJihlLmFkbGVyPWEoZS5h'
    'ZGxlcixpLnBlbmRpbmdfYnVmLGkucGVuZGluZy1vLG8pKSxMKGUpLG89aS5w'
    'ZW5kaW5nLGkucGVuZGluZyE9PWkucGVuZGluZ19idWZfc2l6ZSkpOylEKGks'
    'MjU1JmkuZ3poZWFkLmV4dHJhW2kuZ3ppbmRleF0pLGkuZ3ppbmRleCsrO2ku'
    'Z3poZWFkLmhjcmMmJmkucGVuZGluZz5vJiYoZS5hZGxlcj1hKGUuYWRsZXIs'
    'aS5wZW5kaW5nX2J1ZixpLnBlbmRpbmctbyxvKSksaS5nemluZGV4PT09aS5n'
    'emhlYWQuZXh0cmEubGVuZ3RoJiYoaS5nemluZGV4PTAsaS5zdGF0dXM9NzMp'
    'fWVsc2UgaS5zdGF0dXM9NzM7aWYoNzM9PT1pLnN0YXR1cylpZihpLmd6aGVh'
    'ZC5uYW1lKXtvPWkucGVuZGluZztkb3tpZihpLnBlbmRpbmc9PT1pLnBlbmRp'
    'bmdfYnVmX3NpemUmJihpLmd6aGVhZC5oY3JjJiZpLnBlbmRpbmc+byYmKGUu'
    'YWRsZXI9YShlLmFkbGVyLGkucGVuZGluZ19idWYsaS5wZW5kaW5nLW8sbykp'
    'LEwoZSksbz1pLnBlbmRpbmcsaS5wZW5kaW5nPT09aS5wZW5kaW5nX2J1Zl9z'
    'aXplKSl7Yz0xO2JyZWFrfWM9aS5nemluZGV4PGkuZ3poZWFkLm5hbWUubGVu'
    'Z3RoPzI1NSZpLmd6aGVhZC5uYW1lLmNoYXJDb2RlQXQoaS5nemluZGV4Kysp'
    'OjAsRChpLGMpfXdoaWxlKDAhPT1jKTtpLmd6aGVhZC5oY3JjJiZpLnBlbmRp'
    'bmc+byYmKGUuYWRsZXI9YShlLmFkbGVyLGkucGVuZGluZ19idWYsaS5wZW5k'
    'aW5nLW8sbykpLDA9PT1jJiYoaS5nemluZGV4PTAsaS5zdGF0dXM9OTEpfWVs'
    'c2UgaS5zdGF0dXM9OTE7aWYoOTE9PT1pLnN0YXR1cylpZihpLmd6aGVhZC5j'
    'b21tZW50KXtvPWkucGVuZGluZztkb3tpZihpLnBlbmRpbmc9PT1pLnBlbmRp'
    'bmdfYnVmX3NpemUmJihpLmd6aGVhZC5oY3JjJiZpLnBlbmRpbmc+byYmKGUu'
    'YWRsZXI9YShlLmFkbGVyLGkucGVuZGluZ19idWYsaS5wZW5kaW5nLW8sbykp'
    'LEwoZSksbz1pLnBlbmRpbmcsaS5wZW5kaW5nPT09aS5wZW5kaW5nX2J1Zl9z'
    'aXplKSl7Yz0xO2JyZWFrfWM9aS5nemluZGV4PGkuZ3poZWFkLmNvbW1lbnQu'
    'bGVuZ3RoPzI1NSZpLmd6aGVhZC5jb21tZW50LmNoYXJDb2RlQXQoaS5nemlu'
    'ZGV4KyspOjAsRChpLGMpfXdoaWxlKDAhPT1jKTtpLmd6aGVhZC5oY3JjJiZp'
    'LnBlbmRpbmc+byYmKGUuYWRsZXI9YShlLmFkbGVyLGkucGVuZGluZ19idWYs'
    'aS5wZW5kaW5nLW8sbykpLDA9PT1jJiYoaS5zdGF0dXM9MTAzKX1lbHNlIGku'
    'c3RhdHVzPTEwMztpZigxMDM9PT1pLnN0YXR1cyYmKGkuZ3poZWFkLmhjcmM/'
    'KGkucGVuZGluZysyPmkucGVuZGluZ19idWZfc2l6ZSYmTChlKSxpLnBlbmRp'
    'bmcrMjw9aS5wZW5kaW5nX2J1Zl9zaXplJiYoRChpLDI1NSZlLmFkbGVyKSxE'
    'KGksZS5hZGxlcj4+OCYyNTUpLGUuYWRsZXI9MCxpLnN0YXR1cz1SKSk6aS5z'
    'dGF0dXM9UiksMCE9PWkucGVuZGluZyl7aWYoTChlKSwwPT09ZS5hdmFpbF9v'
    'dXQpcmV0dXJuIGkubGFzdF9mbHVzaD0tMSwwfWVsc2UgaWYoMD09PWUuYXZh'
    'aWxfaW4mJk8odCk8PU8ocikmJjQhPT10KXJldHVybiBfKGUsLTUpO2lmKDY2'
    'Nj09PWkuc3RhdHVzJiYwIT09ZS5hdmFpbF9pbilyZXR1cm4gXyhlLC01KTtp'
    'ZigwIT09ZS5hdmFpbF9pbnx8MCE9PWkubG9va2FoZWFkfHwwIT09dCYmNjY2'
    'IT09aS5zdGF0dXMpe3ZhciBsPTI9PT1pLnN0cmF0ZWd5P2Z1bmN0aW9uKGUs'
    'dCl7Zm9yKHZhciByOzspe2lmKDA9PT1lLmxvb2thaGVhZCYmKHooZSksMD09'
    'PWUubG9va2FoZWFkKSl7aWYoMD09PXQpcmV0dXJuIDE7YnJlYWt9aWYoZS5t'
    'YXRjaF9sZW5ndGg9MCxyPXMuX3RyX3RhbGx5KGUsMCxlLndpbmRvd1tlLnN0'
    'cnN0YXJ0XSksZS5sb29rYWhlYWQtLSxlLnN0cnN0YXJ0KyssciYmKEkoZSwh'
    'MSksMD09PWUuc3RybS5hdmFpbF9vdXQpKXJldHVybiAxfXJldHVybiBlLmlu'
    'c2VydD0wLDQ9PT10PyhJKGUsITApLDA9PT1lLnN0cm0uYXZhaWxfb3V0PzM6'
    'NCk6ZS5sYXN0X2xpdCYmKEkoZSwhMSksMD09PWUuc3RybS5hdmFpbF9vdXQp'
    'PzE6Mn0oaSx0KTozPT09aS5zdHJhdGVneT9mdW5jdGlvbihlLHQpe2Zvcih2'
    'YXIgcixuLGksbyxhPWUud2luZG93Ozspe2lmKGUubG9va2FoZWFkPD14KXtp'
    'Zih6KGUpLGUubG9va2FoZWFkPD14JiYwPT09dClyZXR1cm4gMTtpZigwPT09'
    'ZS5sb29rYWhlYWQpYnJlYWt9aWYoZS5tYXRjaF9sZW5ndGg9MCxlLmxvb2th'
    'aGVhZD49MyYmMDxlLnN0cnN0YXJ0JiYobj1hW2k9ZS5zdHJzdGFydC0xXSk9'
    'PT1hWysraV0mJm49PT1hWysraV0mJm49PT1hWysraV0pe289ZS5zdHJzdGFy'
    'dCt4O2Rve313aGlsZShuPT09YVsrK2ldJiZuPT09YVsrK2ldJiZuPT09YVsr'
    'K2ldJiZuPT09YVsrK2ldJiZuPT09YVsrK2ldJiZuPT09YVsrK2ldJiZuPT09'
    'YVsrK2ldJiZuPT09YVsrK2ldJiZpPG8pO2UubWF0Y2hfbGVuZ3RoPXgtKG8t'
    'aSksZS5tYXRjaF9sZW5ndGg+ZS5sb29rYWhlYWQmJihlLm1hdGNoX2xlbmd0'
    'aD1lLmxvb2thaGVhZCl9aWYoZS5tYXRjaF9sZW5ndGg+PTM/KHI9cy5fdHJf'
    'dGFsbHkoZSwxLGUubWF0Y2hfbGVuZ3RoLTMpLGUubG9va2FoZWFkLT1lLm1h'
    'dGNoX2xlbmd0aCxlLnN0cnN0YXJ0Kz1lLm1hdGNoX2xlbmd0aCxlLm1hdGNo'
    'X2xlbmd0aD0wKToocj1zLl90cl90YWxseShlLDAsZS53aW5kb3dbZS5zdHJz'
    'dGFydF0pLGUubG9va2FoZWFkLS0sZS5zdHJzdGFydCsrKSxyJiYoSShlLCEx'
    'KSwwPT09ZS5zdHJtLmF2YWlsX291dCkpcmV0dXJuIDF9cmV0dXJuIGUuaW5z'
    'ZXJ0PTAsND09PXQ/KEkoZSwhMCksMD09PWUuc3RybS5hdmFpbF9vdXQ/Mzo0'
    'KTplLmxhc3RfbGl0JiYoSShlLCExKSwwPT09ZS5zdHJtLmF2YWlsX291dCk/'
    'MToyfShpLHQpOm5baS5sZXZlbF0uZnVuYyhpLHQpO2lmKDMhPT1sJiY0IT09'
    'bHx8KGkuc3RhdHVzPTY2NiksMT09PWx8fDM9PT1sKXJldHVybiAwPT09ZS5h'
    'dmFpbF9vdXQmJihpLmxhc3RfZmx1c2g9LTEpLDA7aWYoMj09PWwmJigxPT09'
    'dD9zLl90cl9hbGlnbihpKTo1IT09dCYmKHMuX3RyX3N0b3JlZF9ibG9jayhp'
    'LDAsMCwhMSksMz09PXQmJihQKGkuaGVhZCksMD09PWkubG9va2FoZWFkJiYo'
    'aS5zdHJzdGFydD0wLGkuYmxvY2tfc3RhcnQ9MCxpLmluc2VydD0wKSkpLEwo'
    'ZSksMD09PWUuYXZhaWxfb3V0KSlyZXR1cm4gaS5sYXN0X2ZsdXNoPS0xLDB9'
    'cmV0dXJuIDQhPT10PzA6aS53cmFwPD0wPzE6KDI9PT1pLndyYXA/KEQoaSwy'
    'NTUmZS5hZGxlciksRChpLGUuYWRsZXI+PjgmMjU1KSxEKGksZS5hZGxlcj4+'
    'MTYmMjU1KSxEKGksZS5hZGxlcj4+MjQmMjU1KSxEKGksMjU1JmUudG90YWxf'
    'aW4pLEQoaSxlLnRvdGFsX2luPj44JjI1NSksRChpLGUudG90YWxfaW4+PjE2'
    'JjI1NSksRChpLGUudG90YWxfaW4+PjI0JjI1NSkpOihVKGksZS5hZGxlcj4+'
    'PjE2KSxVKGksNjU1MzUmZS5hZGxlcikpLEwoZSksMDxpLndyYXAmJihpLndy'
    'YXA9LWkud3JhcCksMCE9PWkucGVuZGluZz8wOjEpfSxyLmRlZmxhdGVFbmQ9'
    'ZnVuY3Rpb24oZSl7dmFyIHQ7cmV0dXJuIGUmJmUuc3RhdGU/KHQ9ZS5zdGF0'
    'ZS5zdGF0dXMpIT09YiYmNjkhPT10JiY3MyE9PXQmJjkxIT09dCYmMTAzIT09'
    'dCYmdCE9PVImJjY2NiE9PXQ/XyhlLHcpOihlLnN0YXRlPW51bGwsdD09PVI/'
    'XyhlLC0zKTowKTp3fSxyLmRlZmxhdGVTZXREaWN0aW9uYXJ5PWZ1bmN0aW9u'
    'KGUsdCl7dmFyIHIsbixzLGEsYyx1LGwsZCxoPXQubGVuZ3RoO2lmKCFlfHwh'
    'ZS5zdGF0ZSlyZXR1cm4gdztpZigyPT09KGE9KHI9ZS5zdGF0ZSkud3JhcCl8'
    'fDE9PT1hJiZyLnN0YXR1cyE9PWJ8fHIubG9va2FoZWFkKXJldHVybiB3O2Zv'
    'cigxPT09YSYmKGUuYWRsZXI9byhlLmFkbGVyLHQsaCwwKSksci53cmFwPTAs'
    'aD49ci53X3NpemUmJigwPT09YSYmKFAoci5oZWFkKSxyLnN0cnN0YXJ0PTAs'
    'ci5ibG9ja19zdGFydD0wLHIuaW5zZXJ0PTApLGQ9bmV3IGkuQnVmOChyLndf'
    'c2l6ZSksaS5hcnJheVNldChkLHQsaC1yLndfc2l6ZSxyLndfc2l6ZSwwKSx0'
    'PWQsaD1yLndfc2l6ZSksYz1lLmF2YWlsX2luLHU9ZS5uZXh0X2luLGw9ZS5p'
    'bnB1dCxlLmF2YWlsX2luPWgsZS5uZXh0X2luPTAsZS5pbnB1dD10LHoocik7'
    'ci5sb29rYWhlYWQ+PTM7KXtmb3Iobj1yLnN0cnN0YXJ0LHM9ci5sb29rYWhl'
    'YWQtMjtyLmluc19oPShyLmluc19oPDxyLmhhc2hfc2hpZnReci53aW5kb3db'
    'biszLTFdKSZyLmhhc2hfbWFzayxyLnByZXZbbiZyLndfbWFza109ci5oZWFk'
    'W3IuaW5zX2hdLHIuaGVhZFtyLmluc19oXT1uLG4rKywtLXM7KTtyLnN0cnN0'
    'YXJ0PW4sci5sb29rYWhlYWQ9Mix6KHIpfXJldHVybiByLnN0cnN0YXJ0Kz1y'
    'Lmxvb2thaGVhZCxyLmJsb2NrX3N0YXJ0PXIuc3Ryc3RhcnQsci5pbnNlcnQ9'
    'ci5sb29rYWhlYWQsci5sb29rYWhlYWQ9MCxyLm1hdGNoX2xlbmd0aD1yLnBy'
    'ZXZfbGVuZ3RoPTIsci5tYXRjaF9hdmFpbGFibGU9MCxlLm5leHRfaW49dSxl'
    'LmlucHV0PWwsZS5hdmFpbF9pbj1jLHIud3JhcD1hLDB9LHIuZGVmbGF0ZUlu'
    'Zm89InBha28gZGVmbGF0ZSAoZnJvbSBOb2RlY2EgcHJvamVjdCkifSx7Ii4u'
    'L3V0aWxzL2NvbW1vbiI6NDEsIi4vYWRsZXIzMiI6NDMsIi4vY3JjMzIiOjQ1'
    'LCIuL21lc3NhZ2VzIjo1MSwiLi90cmVlcyI6NTJ9XSw0NzpbZnVuY3Rpb24o'
    'ZSx0LHIpe3QuZXhwb3J0cz1mdW5jdGlvbigpe3RoaXMudGV4dD0wLHRoaXMu'
    'dGltZT0wLHRoaXMueGZsYWdzPTAsdGhpcy5vcz0wLHRoaXMuZXh0cmE9bnVs'
    'bCx0aGlzLmV4dHJhX2xlbj0wLHRoaXMubmFtZT0iIix0aGlzLmNvbW1lbnQ9'
    'IiIsdGhpcy5oY3JjPTAsdGhpcy5kb25lPSExfX0se31dLDQ4OltmdW5jdGlv'
    'bihlLHQscil7dC5leHBvcnRzPWZ1bmN0aW9uKGUsdCl7dmFyIHIsbixpLHMs'
    'byxhLGMsdSxsLGQsdyxoLGYsQSxwLEUsQixILG0sZyx5LFQseCx2LGI7cj1l'
    'LnN0YXRlLG49ZS5uZXh0X2luLHY9ZS5pbnB1dCxpPW4rKGUuYXZhaWxfaW4t'
    'NSkscz1lLm5leHRfb3V0LGI9ZS5vdXRwdXQsbz1zLSh0LWUuYXZhaWxfb3V0'
    'KSxhPXMrKGUuYXZhaWxfb3V0LTI1NyksYz1yLmRtYXgsdT1yLndzaXplLGw9'
    'ci53aGF2ZSxkPXIud25leHQsdz1yLndpbmRvdyxoPXIuaG9sZCxmPXIuYml0'
    'cyxBPXIubGVuY29kZSxwPXIuZGlzdGNvZGUsRT0oMTw8ci5sZW5iaXRzKS0x'
    'LEI9KDE8PHIuZGlzdGJpdHMpLTE7ZTpkb3tmPDE1JiYoaCs9dltuKytdPDxm'
    'LGYrPTgsaCs9dltuKytdPDxmLGYrPTgpLEg9QVtoJkVdO3Q6Zm9yKDs7KXtp'
    'ZihoPj4+PW09SD4+PjI0LGYtPW0sMD09KG09SD4+PjE2JjI1NSkpYltzKytd'
    'PTY1NTM1Jkg7ZWxzZXtpZighKDE2Jm0pKXtpZighKDY0Jm0pKXtIPUFbKDY1'
    'NTM1JkgpKyhoJigxPDxtKS0xKV07Y29udGludWUgdH1pZigzMiZtKXtyLm1v'
    'ZGU9MTI7YnJlYWsgZX1lLm1zZz0iaW52YWxpZCBsaXRlcmFsL2xlbmd0aCBj'
    'b2RlIixyLm1vZGU9MzA7YnJlYWsgZX1nPTY1NTM1JkgsKG0mPTE1KSYmKGY8'
    'bSYmKGgrPXZbbisrXTw8ZixmKz04KSxnKz1oJigxPDxtKS0xLGg+Pj49bSxm'
    'LT1tKSxmPDE1JiYoaCs9dltuKytdPDxmLGYrPTgsaCs9dltuKytdPDxmLGYr'
    'PTgpLEg9cFtoJkJdO3I6Zm9yKDs7KXtpZihoPj4+PW09SD4+PjI0LGYtPW0s'
    'ISgxNiYobT1IPj4+MTYmMjU1KSkpe2lmKCEoNjQmbSkpe0g9cFsoNjU1MzUm'
    'SCkrKGgmKDE8PG0pLTEpXTtjb250aW51ZSByfWUubXNnPSJpbnZhbGlkIGRp'
    'c3RhbmNlIGNvZGUiLHIubW9kZT0zMDticmVhayBlfWlmKHk9NjU1MzUmSCxm'
    'PChtJj0xNSkmJihoKz12W24rK108PGYsKGYrPTgpPG0mJihoKz12W24rK108'
    'PGYsZis9OCkpLGM8KHkrPWgmKDE8PG0pLTEpKXtlLm1zZz0iaW52YWxpZCBk'
    'aXN0YW5jZSB0b28gZmFyIGJhY2siLHIubW9kZT0zMDticmVhayBlfWlmKGg+'
    'Pj49bSxmLT1tLChtPXMtbyk8eSl7aWYobDwobT15LW0pJiZyLnNhbmUpe2Uu'
    'bXNnPSJpbnZhbGlkIGRpc3RhbmNlIHRvbyBmYXIgYmFjayIsci5tb2RlPTMw'
    'O2JyZWFrIGV9aWYoeD13LChUPTApPT09ZCl7aWYoVCs9dS1tLG08Zyl7Zm9y'
    'KGctPW07YltzKytdPXdbVCsrXSwtLW07KTtUPXMteSx4PWJ9fWVsc2UgaWYo'
    'ZDxtKXtpZihUKz11K2QtbSwobS09ZCk8Zyl7Zm9yKGctPW07YltzKytdPXdb'
    'VCsrXSwtLW07KTtpZihUPTAsZDxnKXtmb3IoZy09bT1kO2JbcysrXT13W1Qr'
    'K10sLS1tOyk7VD1zLXkseD1ifX19ZWxzZSBpZihUKz1kLW0sbTxnKXtmb3Io'
    'Zy09bTtiW3MrK109d1tUKytdLC0tbTspO1Q9cy15LHg9Yn1mb3IoOzI8Zzsp'
    'YltzKytdPXhbVCsrXSxiW3MrK109eFtUKytdLGJbcysrXT14W1QrK10sZy09'
    'MztnJiYoYltzKytdPXhbVCsrXSwxPGcmJihiW3MrK109eFtUKytdKSl9ZWxz'
    'ZXtmb3IoVD1zLXk7YltzKytdPWJbVCsrXSxiW3MrK109YltUKytdLGJbcysr'
    'XT1iW1QrK10sMjwoZy09Myk7KTtnJiYoYltzKytdPWJbVCsrXSwxPGcmJihi'
    'W3MrK109YltUKytdKSl9YnJlYWt9fWJyZWFrfX13aGlsZShuPGkmJnM8YSk7'
    'bi09Zz1mPj4zLGgmPSgxPDwoZi09Zzw8MykpLTEsZS5uZXh0X2luPW4sZS5u'
    'ZXh0X291dD1zLGUuYXZhaWxfaW49bjxpP2ktbis1OjUtKG4taSksZS5hdmFp'
    'bF9vdXQ9czxhP2EtcysyNTc6MjU3LShzLWEpLHIuaG9sZD1oLHIuYml0cz1m'
    'fX0se31dLDQ5OltmdW5jdGlvbihlLHQscil7dmFyIG49ZSgiLi4vdXRpbHMv'
    'Y29tbW9uIiksaT1lKCIuL2FkbGVyMzIiKSxzPWUoIi4vY3JjMzIiKSxvPWUo'
    'Ii4vaW5mZmFzdCIpLGE9ZSgiLi9pbmZ0cmVlcyIpLGM9MSx1PTIsbD0wLGQ9'
    'LTIsdz0xLGg9ODUyLGY9NTkyO2Z1bmN0aW9uIEEoZSl7cmV0dXJuKGU+Pj4y'
    'NCYyNTUpKyhlPj4+OCY2NTI4MCkrKCg2NTI4MCZlKTw8OCkrKCgyNTUmZSk8'
    'PDI0KX1mdW5jdGlvbiBwKCl7dGhpcy5tb2RlPTAsdGhpcy5sYXN0PSExLHRo'
    'aXMud3JhcD0wLHRoaXMuaGF2ZWRpY3Q9ITEsdGhpcy5mbGFncz0wLHRoaXMu'
    'ZG1heD0wLHRoaXMuY2hlY2s9MCx0aGlzLnRvdGFsPTAsdGhpcy5oZWFkPW51'
    'bGwsdGhpcy53Yml0cz0wLHRoaXMud3NpemU9MCx0aGlzLndoYXZlPTAsdGhp'
    'cy53bmV4dD0wLHRoaXMud2luZG93PW51bGwsdGhpcy5ob2xkPTAsdGhpcy5i'
    'aXRzPTAsdGhpcy5sZW5ndGg9MCx0aGlzLm9mZnNldD0wLHRoaXMuZXh0cmE9'
    'MCx0aGlzLmxlbmNvZGU9bnVsbCx0aGlzLmRpc3Rjb2RlPW51bGwsdGhpcy5s'
    'ZW5iaXRzPTAsdGhpcy5kaXN0Yml0cz0wLHRoaXMubmNvZGU9MCx0aGlzLm5s'
    'ZW49MCx0aGlzLm5kaXN0PTAsdGhpcy5oYXZlPTAsdGhpcy5uZXh0PW51bGws'
    'dGhpcy5sZW5zPW5ldyBuLkJ1ZjE2KDMyMCksdGhpcy53b3JrPW5ldyBuLkJ1'
    'ZjE2KDI4OCksdGhpcy5sZW5keW49bnVsbCx0aGlzLmRpc3RkeW49bnVsbCx0'
    'aGlzLnNhbmU9MCx0aGlzLmJhY2s9MCx0aGlzLndhcz0wfWZ1bmN0aW9uIEUo'
    'ZSl7dmFyIHQ7cmV0dXJuIGUmJmUuc3RhdGU/KHQ9ZS5zdGF0ZSxlLnRvdGFs'
    'X2luPWUudG90YWxfb3V0PXQudG90YWw9MCxlLm1zZz0iIix0LndyYXAmJihl'
    'LmFkbGVyPTEmdC53cmFwKSx0Lm1vZGU9MSx0Lmxhc3Q9MCx0LmhhdmVkaWN0'
    'PTAsdC5kbWF4PTMyNzY4LHQuaGVhZD1udWxsLHQuaG9sZD0wLHQuYml0cz0w'
    'LHQubGVuY29kZT10LmxlbmR5bj1uZXcgbi5CdWYzMihoKSx0LmRpc3Rjb2Rl'
    'PXQuZGlzdGR5bj1uZXcgbi5CdWYzMihmKSx0LnNhbmU9MSx0LmJhY2s9LTEs'
    'MCk6ZH1mdW5jdGlvbiBCKGUpe3ZhciB0O3JldHVybiBlJiZlLnN0YXRlPygo'
    'dD1lLnN0YXRlKS53c2l6ZT0wLHQud2hhdmU9MCx0LnduZXh0PTAsRShlKSk6'
    'ZH1mdW5jdGlvbiBIKGUsdCl7dmFyIHIsbjtyZXR1cm4gZSYmZS5zdGF0ZT8o'
    'bj1lLnN0YXRlLHQ8MD8ocj0wLHQ9LXQpOihyPTErKHQ+PjQpLHQ8NDgmJih0'
    'Jj0xNSkpLHQmJih0PDh8fDE1PHQpP2Q6KG51bGwhPT1uLndpbmRvdyYmbi53'
    'Yml0cyE9PXQmJihuLndpbmRvdz1udWxsKSxuLndyYXA9cixuLndiaXRzPXQs'
    'QihlKSkpOmR9ZnVuY3Rpb24gbShlLHQpe3ZhciByLG47cmV0dXJuIGU/KG49'
    'bmV3IHAsKGUuc3RhdGU9bikud2luZG93PW51bGwsMCE9PShyPUgoZSx0KSkm'
    'JihlLnN0YXRlPW51bGwpLHIpOmR9dmFyIGcseSxUPSEwO2Z1bmN0aW9uIHgo'
    'ZSl7aWYoVCl7dmFyIHQ7Zm9yKGc9bmV3IG4uQnVmMzIoNTEyKSx5PW5ldyBu'
    'LkJ1ZjMyKDMyKSx0PTA7dDwxNDQ7KWUubGVuc1t0KytdPTg7Zm9yKDt0PDI1'
    'NjspZS5sZW5zW3QrK109OTtmb3IoO3Q8MjgwOyllLmxlbnNbdCsrXT03O2Zv'
    'cig7dDwyODg7KWUubGVuc1t0KytdPTg7Zm9yKGEoMSxlLmxlbnMsMCwyODgs'
    'ZywwLGUud29yayx7Yml0czo5fSksdD0wO3Q8MzI7KWUubGVuc1t0KytdPTU7'
    'YSgyLGUubGVucywwLDMyLHksMCxlLndvcmsse2JpdHM6NX0pLFQ9ITF9ZS5s'
    'ZW5jb2RlPWcsZS5sZW5iaXRzPTksZS5kaXN0Y29kZT15LGUuZGlzdGJpdHM9'
    'NX1mdW5jdGlvbiB2KGUsdCxyLGkpe3ZhciBzLG89ZS5zdGF0ZTtyZXR1cm4g'
    'bnVsbD09PW8ud2luZG93JiYoby53c2l6ZT0xPDxvLndiaXRzLG8ud25leHQ9'
    'MCxvLndoYXZlPTAsby53aW5kb3c9bmV3IG4uQnVmOChvLndzaXplKSksaT49'
    'by53c2l6ZT8obi5hcnJheVNldChvLndpbmRvdyx0LHItby53c2l6ZSxvLndz'
    'aXplLDApLG8ud25leHQ9MCxvLndoYXZlPW8ud3NpemUpOihpPChzPW8ud3Np'
    'emUtby53bmV4dCkmJihzPWkpLG4uYXJyYXlTZXQoby53aW5kb3csdCxyLWks'
    'cyxvLnduZXh0KSwoaS09cyk/KG4uYXJyYXlTZXQoby53aW5kb3csdCxyLWks'
    'aSwwKSxvLnduZXh0PWksby53aGF2ZT1vLndzaXplKTooby53bmV4dCs9cyxv'
    'LnduZXh0PT09by53c2l6ZSYmKG8ud25leHQ9MCksby53aGF2ZTxvLndzaXpl'
    'JiYoby53aGF2ZSs9cykpKSwwfXIuaW5mbGF0ZVJlc2V0PUIsci5pbmZsYXRl'
    'UmVzZXQyPUgsci5pbmZsYXRlUmVzZXRLZWVwPUUsci5pbmZsYXRlSW5pdD1m'
    'dW5jdGlvbihlKXtyZXR1cm4gbShlLDE1KX0sci5pbmZsYXRlSW5pdDI9bSxy'
    'LmluZmxhdGU9ZnVuY3Rpb24oZSx0KXt2YXIgcixjLHUsbCx3LGgsZixwLEUs'
    'QixILG0sZyx5LFQsYixSLE0sayxTLEMsXyxPLFAsTD0wLEk9bmV3IG4uQnVm'
    'OCg0KSxEPVsxNiwxNywxOCwwLDgsNyw5LDYsMTAsNSwxMSw0LDEyLDMsMTMs'
    'MiwxNCwxLDE1XTtpZighZXx8IWUuc3RhdGV8fCFlLm91dHB1dHx8IWUuaW5w'
    'dXQmJjAhPT1lLmF2YWlsX2luKXJldHVybiBkOzEyPT09KHI9ZS5zdGF0ZSku'
    'bW9kZSYmKHIubW9kZT0xMyksdz1lLm5leHRfb3V0LHU9ZS5vdXRwdXQsZj1l'
    'LmF2YWlsX291dCxsPWUubmV4dF9pbixjPWUuaW5wdXQsaD1lLmF2YWlsX2lu'
    'LHA9ci5ob2xkLEU9ci5iaXRzLEI9aCxIPWYsXz0wO2U6Zm9yKDs7KXN3aXRj'
    'aChyLm1vZGUpe2Nhc2UgMTppZigwPT09ci53cmFwKXtyLm1vZGU9MTM7YnJl'
    'YWt9Zm9yKDtFPDE2Oyl7aWYoMD09PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytd'
    'PDxFLEUrPTh9aWYoMiZyLndyYXAmJjM1NjE1PT09cCl7SVtyLmNoZWNrPTBd'
    'PTI1NSZwLElbMV09cD4+PjgmMjU1LHIuY2hlY2s9cyhyLmNoZWNrLEksMiww'
    'KSxFPXA9MCxyLm1vZGU9MjticmVha31pZihyLmZsYWdzPTAsci5oZWFkJiYo'
    'ci5oZWFkLmRvbmU9ITEpLCEoMSZyLndyYXApfHwoKCgyNTUmcCk8PDgpKyhw'
    'Pj44KSklMzEpe2UubXNnPSJpbmNvcnJlY3QgaGVhZGVyIGNoZWNrIixyLm1v'
    'ZGU9MzA7YnJlYWt9aWYoOCE9KDE1JnApKXtlLm1zZz0idW5rbm93biBjb21w'
    'cmVzc2lvbiBtZXRob2QiLHIubW9kZT0zMDticmVha31pZihFLT00LEM9OCso'
    'MTUmKHA+Pj49NCkpLDA9PT1yLndiaXRzKXIud2JpdHM9QztlbHNlIGlmKEM+'
    'ci53Yml0cyl7ZS5tc2c9ImludmFsaWQgd2luZG93IHNpemUiLHIubW9kZT0z'
    'MDticmVha31yLmRtYXg9MTw8QyxlLmFkbGVyPXIuY2hlY2s9MSxyLm1vZGU9'
    'NTEyJnA/MTA6MTIsRT1wPTA7YnJlYWs7Y2FzZSAyOmZvcig7RTwxNjspe2lm'
    'KDA9PT1oKWJyZWFrIGU7aC0tLHArPWNbbCsrXTw8RSxFKz04fWlmKHIuZmxh'
    'Z3M9cCw4IT0oMjU1JnIuZmxhZ3MpKXtlLm1zZz0idW5rbm93biBjb21wcmVz'
    'c2lvbiBtZXRob2QiLHIubW9kZT0zMDticmVha31pZig1NzM0NCZyLmZsYWdz'
    'KXtlLm1zZz0idW5rbm93biBoZWFkZXIgZmxhZ3Mgc2V0IixyLm1vZGU9MzA7'
    'YnJlYWt9ci5oZWFkJiYoci5oZWFkLnRleHQ9cD4+OCYxKSw1MTImci5mbGFn'
    'cyYmKElbMF09MjU1JnAsSVsxXT1wPj4+OCYyNTUsci5jaGVjaz1zKHIuY2hl'
    'Y2ssSSwyLDApKSxFPXA9MCxyLm1vZGU9MztjYXNlIDM6Zm9yKDtFPDMyOyl7'
    'aWYoMD09PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytdPDxFLEUrPTh9ci5oZWFk'
    'JiYoci5oZWFkLnRpbWU9cCksNTEyJnIuZmxhZ3MmJihJWzBdPTI1NSZwLElb'
    'MV09cD4+PjgmMjU1LElbMl09cD4+PjE2JjI1NSxJWzNdPXA+Pj4yNCYyNTUs'
    'ci5jaGVjaz1zKHIuY2hlY2ssSSw0LDApKSxFPXA9MCxyLm1vZGU9NDtjYXNl'
    'IDQ6Zm9yKDtFPDE2Oyl7aWYoMD09PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytd'
    'PDxFLEUrPTh9ci5oZWFkJiYoci5oZWFkLnhmbGFncz0yNTUmcCxyLmhlYWQu'
    'b3M9cD4+OCksNTEyJnIuZmxhZ3MmJihJWzBdPTI1NSZwLElbMV09cD4+Pjgm'
    'MjU1LHIuY2hlY2s9cyhyLmNoZWNrLEksMiwwKSksRT1wPTAsci5tb2RlPTU7'
    'Y2FzZSA1OmlmKDEwMjQmci5mbGFncyl7Zm9yKDtFPDE2Oyl7aWYoMD09PWgp'
    'YnJlYWsgZTtoLS0scCs9Y1tsKytdPDxFLEUrPTh9ci5sZW5ndGg9cCxyLmhl'
    'YWQmJihyLmhlYWQuZXh0cmFfbGVuPXApLDUxMiZyLmZsYWdzJiYoSVswXT0y'
    'NTUmcCxJWzFdPXA+Pj44JjI1NSxyLmNoZWNrPXMoci5jaGVjayxJLDIsMCkp'
    'LEU9cD0wfWVsc2Ugci5oZWFkJiYoci5oZWFkLmV4dHJhPW51bGwpO3IubW9k'
    'ZT02O2Nhc2UgNjppZigxMDI0JnIuZmxhZ3MmJihoPChtPXIubGVuZ3RoKSYm'
    'KG09aCksbSYmKHIuaGVhZCYmKEM9ci5oZWFkLmV4dHJhX2xlbi1yLmxlbmd0'
    'aCxyLmhlYWQuZXh0cmF8fChyLmhlYWQuZXh0cmE9bmV3IEFycmF5KHIuaGVh'
    'ZC5leHRyYV9sZW4pKSxuLmFycmF5U2V0KHIuaGVhZC5leHRyYSxjLGwsbSxD'
    'KSksNTEyJnIuZmxhZ3MmJihyLmNoZWNrPXMoci5jaGVjayxjLG0sbCkpLGgt'
    'PW0sbCs9bSxyLmxlbmd0aC09bSksci5sZW5ndGgpKWJyZWFrIGU7ci5sZW5n'
    'dGg9MCxyLm1vZGU9NztjYXNlIDc6aWYoMjA0OCZyLmZsYWdzKXtpZigwPT09'
    'aClicmVhayBlO2ZvcihtPTA7Qz1jW2wrbSsrXSxyLmhlYWQmJkMmJnIubGVu'
    'Z3RoPDY1NTM2JiYoci5oZWFkLm5hbWUrPVN0cmluZy5mcm9tQ2hhckNvZGUo'
    'QykpLEMmJm08aDspO2lmKDUxMiZyLmZsYWdzJiYoci5jaGVjaz1zKHIuY2hl'
    'Y2ssYyxtLGwpKSxoLT1tLGwrPW0sQylicmVhayBlfWVsc2Ugci5oZWFkJiYo'
    'ci5oZWFkLm5hbWU9bnVsbCk7ci5sZW5ndGg9MCxyLm1vZGU9ODtjYXNlIDg6'
    'aWYoNDA5NiZyLmZsYWdzKXtpZigwPT09aClicmVhayBlO2ZvcihtPTA7Qz1j'
    'W2wrbSsrXSxyLmhlYWQmJkMmJnIubGVuZ3RoPDY1NTM2JiYoci5oZWFkLmNv'
    'bW1lbnQrPVN0cmluZy5mcm9tQ2hhckNvZGUoQykpLEMmJm08aDspO2lmKDUx'
    'MiZyLmZsYWdzJiYoci5jaGVjaz1zKHIuY2hlY2ssYyxtLGwpKSxoLT1tLGwr'
    'PW0sQylicmVhayBlfWVsc2Ugci5oZWFkJiYoci5oZWFkLmNvbW1lbnQ9bnVs'
    'bCk7ci5tb2RlPTk7Y2FzZSA5OmlmKDUxMiZyLmZsYWdzKXtmb3IoO0U8MTY7'
    'KXtpZigwPT09aClicmVhayBlO2gtLSxwKz1jW2wrK108PEUsRSs9OH1pZihw'
    'IT09KDY1NTM1JnIuY2hlY2spKXtlLm1zZz0iaGVhZGVyIGNyYyBtaXNtYXRj'
    'aCIsci5tb2RlPTMwO2JyZWFrfUU9cD0wfXIuaGVhZCYmKHIuaGVhZC5oY3Jj'
    'PXIuZmxhZ3M+PjkmMSxyLmhlYWQuZG9uZT0hMCksZS5hZGxlcj1yLmNoZWNr'
    'PTAsci5tb2RlPTEyO2JyZWFrO2Nhc2UgMTA6Zm9yKDtFPDMyOyl7aWYoMD09'
    'PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytdPDxFLEUrPTh9ZS5hZGxlcj1yLmNo'
    'ZWNrPUEocCksRT1wPTAsci5tb2RlPTExO2Nhc2UgMTE6aWYoMD09PXIuaGF2'
    'ZWRpY3QpcmV0dXJuIGUubmV4dF9vdXQ9dyxlLmF2YWlsX291dD1mLGUubmV4'
    'dF9pbj1sLGUuYXZhaWxfaW49aCxyLmhvbGQ9cCxyLmJpdHM9RSwyO2UuYWRs'
    'ZXI9ci5jaGVjaz0xLHIubW9kZT0xMjtjYXNlIDEyOmlmKDU9PT10fHw2PT09'
    'dClicmVhayBlO2Nhc2UgMTM6aWYoci5sYXN0KXtwPj4+PTcmRSxFLT03JkUs'
    'ci5tb2RlPTI3O2JyZWFrfWZvcig7RTwzOyl7aWYoMD09PWgpYnJlYWsgZTto'
    'LS0scCs9Y1tsKytdPDxFLEUrPTh9c3dpdGNoKHIubGFzdD0xJnAsRS09MSwz'
    'JihwPj4+PTEpKXtjYXNlIDA6ci5tb2RlPTE0O2JyZWFrO2Nhc2UgMTppZih4'
    'KHIpLHIubW9kZT0yMCw2IT09dClicmVhaztwPj4+PTIsRS09MjticmVhayBl'
    'O2Nhc2UgMjpyLm1vZGU9MTc7YnJlYWs7Y2FzZSAzOmUubXNnPSJpbnZhbGlk'
    'IGJsb2NrIHR5cGUiLHIubW9kZT0zMH1wPj4+PTIsRS09MjticmVhaztjYXNl'
    'IDE0OmZvcihwPj4+PTcmRSxFLT03JkU7RTwzMjspe2lmKDA9PT1oKWJyZWFr'
    'IGU7aC0tLHArPWNbbCsrXTw8RSxFKz04fWlmKCg2NTUzNSZwKSE9KHA+Pj4x'
    'Nl42NTUzNSkpe2UubXNnPSJpbnZhbGlkIHN0b3JlZCBibG9jayBsZW5ndGhz'
    'IixyLm1vZGU9MzA7YnJlYWt9aWYoci5sZW5ndGg9NjU1MzUmcCxFPXA9MCxy'
    'Lm1vZGU9MTUsNj09PXQpYnJlYWsgZTtjYXNlIDE1OnIubW9kZT0xNjtjYXNl'
    'IDE2OmlmKG09ci5sZW5ndGgpe2lmKGg8bSYmKG09aCksZjxtJiYobT1mKSww'
    'PT09bSlicmVhayBlO24uYXJyYXlTZXQodSxjLGwsbSx3KSxoLT1tLGwrPW0s'
    'Zi09bSx3Kz1tLHIubGVuZ3RoLT1tO2JyZWFrfXIubW9kZT0xMjticmVhaztj'
    'YXNlIDE3OmZvcig7RTwxNDspe2lmKDA9PT1oKWJyZWFrIGU7aC0tLHArPWNb'
    'bCsrXTw8RSxFKz04fWlmKHIubmxlbj0yNTcrKDMxJnApLHA+Pj49NSxFLT01'
    'LHIubmRpc3Q9MSsoMzEmcCkscD4+Pj01LEUtPTUsci5uY29kZT00KygxNSZw'
    'KSxwPj4+PTQsRS09NCwyODY8ci5ubGVufHwzMDxyLm5kaXN0KXtlLm1zZz0i'
    'dG9vIG1hbnkgbGVuZ3RoIG9yIGRpc3RhbmNlIHN5bWJvbHMiLHIubW9kZT0z'
    'MDticmVha31yLmhhdmU9MCxyLm1vZGU9MTg7Y2FzZSAxODpmb3IoO3IuaGF2'
    'ZTxyLm5jb2RlOyl7Zm9yKDtFPDM7KXtpZigwPT09aClicmVhayBlO2gtLSxw'
    'Kz1jW2wrK108PEUsRSs9OH1yLmxlbnNbRFtyLmhhdmUrK11dPTcmcCxwPj4+'
    'PTMsRS09M31mb3IoO3IuaGF2ZTwxOTspci5sZW5zW0Rbci5oYXZlKytdXT0w'
    'O2lmKHIubGVuY29kZT1yLmxlbmR5bixyLmxlbmJpdHM9NyxPPXtiaXRzOnIu'
    'bGVuYml0c30sXz1hKDAsci5sZW5zLDAsMTksci5sZW5jb2RlLDAsci53b3Jr'
    'LE8pLHIubGVuYml0cz1PLmJpdHMsXyl7ZS5tc2c9ImludmFsaWQgY29kZSBs'
    'ZW5ndGhzIHNldCIsci5tb2RlPTMwO2JyZWFrfXIuaGF2ZT0wLHIubW9kZT0x'
    'OTtjYXNlIDE5OmZvcig7ci5oYXZlPHIubmxlbityLm5kaXN0Oyl7Zm9yKDti'
    'PShMPXIubGVuY29kZVtwJigxPDxyLmxlbmJpdHMpLTFdKT4+PjE2JjI1NSxS'
    'PTY1NTM1JkwsISgoVD1MPj4+MjQpPD1FKTspe2lmKDA9PT1oKWJyZWFrIGU7'
    'aC0tLHArPWNbbCsrXTw8RSxFKz04fWlmKFI8MTYpcD4+Pj1ULEUtPVQsci5s'
    'ZW5zW3IuaGF2ZSsrXT1SO2Vsc2V7aWYoMTY9PT1SKXtmb3IoUD1UKzI7RTxQ'
    'Oyl7aWYoMD09PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytdPDxFLEUrPTh9aWYo'
    'cD4+Pj1ULEUtPVQsMD09PXIuaGF2ZSl7ZS5tc2c9ImludmFsaWQgYml0IGxl'
    'bmd0aCByZXBlYXQiLHIubW9kZT0zMDticmVha31DPXIubGVuc1tyLmhhdmUt'
    'MV0sbT0zKygzJnApLHA+Pj49MixFLT0yfWVsc2UgaWYoMTc9PT1SKXtmb3Io'
    'UD1UKzM7RTxQOyl7aWYoMD09PWgpYnJlYWsgZTtoLS0scCs9Y1tsKytdPDxF'
    'LEUrPTh9RS09VCxDPTAsbT0zKyg3JihwPj4+PVQpKSxwPj4+PTMsRS09M31l'
    'bHNle2ZvcihQPVQrNztFPFA7KXtpZigwPT09aClicmVhayBlO2gtLSxwKz1j'
    'W2wrK108PEUsRSs9OH1FLT1ULEM9MCxtPTExKygxMjcmKHA+Pj49VCkpLHA+'
    'Pj49NyxFLT03fWlmKHIuaGF2ZSttPnIubmxlbityLm5kaXN0KXtlLm1zZz0i'
    'aW52YWxpZCBiaXQgbGVuZ3RoIHJlcGVhdCIsci5tb2RlPTMwO2JyZWFrfWZv'
    'cig7bS0tOylyLmxlbnNbci5oYXZlKytdPUN9fWlmKDMwPT09ci5tb2RlKWJy'
    'ZWFrO2lmKDA9PT1yLmxlbnNbMjU2XSl7ZS5tc2c9ImludmFsaWQgY29kZSAt'
    'LSBtaXNzaW5nIGVuZC1vZi1ibG9jayIsci5tb2RlPTMwO2JyZWFrfWlmKHIu'
    'bGVuYml0cz05LE89e2JpdHM6ci5sZW5iaXRzfSxfPWEoMSxyLmxlbnMsMCxy'
    'Lm5sZW4sci5sZW5jb2RlLDAsci53b3JrLE8pLHIubGVuYml0cz1PLmJpdHMs'
    'Xyl7ZS5tc2c9ImludmFsaWQgbGl0ZXJhbC9sZW5ndGhzIHNldCIsci5tb2Rl'
    'PTMwO2JyZWFrfWlmKHIuZGlzdGJpdHM9NixyLmRpc3Rjb2RlPXIuZGlzdGR5'
    'bixPPXtiaXRzOnIuZGlzdGJpdHN9LF89YSgyLHIubGVucyxyLm5sZW4sci5u'
    'ZGlzdCxyLmRpc3Rjb2RlLDAsci53b3JrLE8pLHIuZGlzdGJpdHM9Ty5iaXRz'
    'LF8pe2UubXNnPSJpbnZhbGlkIGRpc3RhbmNlcyBzZXQiLHIubW9kZT0zMDti'
    'cmVha31pZihyLm1vZGU9MjAsNj09PXQpYnJlYWsgZTtjYXNlIDIwOnIubW9k'
    'ZT0yMTtjYXNlIDIxOmlmKDY8PWgmJjI1ODw9Zil7ZS5uZXh0X291dD13LGUu'
    'YXZhaWxfb3V0PWYsZS5uZXh0X2luPWwsZS5hdmFpbF9pbj1oLHIuaG9sZD1w'
    'LHIuYml0cz1FLG8oZSxIKSx3PWUubmV4dF9vdXQsdT1lLm91dHB1dCxmPWUu'
    'YXZhaWxfb3V0LGw9ZS5uZXh0X2luLGM9ZS5pbnB1dCxoPWUuYXZhaWxfaW4s'
    'cD1yLmhvbGQsRT1yLmJpdHMsMTI9PT1yLm1vZGUmJihyLmJhY2s9LTEpO2Jy'
    'ZWFrfWZvcihyLmJhY2s9MDtiPShMPXIubGVuY29kZVtwJigxPDxyLmxlbmJp'
    'dHMpLTFdKT4+PjE2JjI1NSxSPTY1NTM1JkwsISgoVD1MPj4+MjQpPD1FKTsp'
    'e2lmKDA9PT1oKWJyZWFrIGU7aC0tLHArPWNbbCsrXTw8RSxFKz04fWlmKGIm'
    'JiEoMjQwJmIpKXtmb3IoTT1ULGs9YixTPVI7Yj0oTD1yLmxlbmNvZGVbUyso'
    'KHAmKDE8PE0rayktMSk+Pk0pXSk+Pj4xNiYyNTUsUj02NTUzNSZMLCEoTSso'
    'VD1MPj4+MjQpPD1FKTspe2lmKDA9PT1oKWJyZWFrIGU7aC0tLHArPWNbbCsr'
    'XTw8RSxFKz04fXA+Pj49TSxFLT1NLHIuYmFjays9TX1pZihwPj4+PVQsRS09'
    'VCxyLmJhY2srPVQsci5sZW5ndGg9UiwwPT09Yil7ci5tb2RlPTI2O2JyZWFr'
    'fWlmKDMyJmIpe3IuYmFjaz0tMSxyLm1vZGU9MTI7YnJlYWt9aWYoNjQmYil7'
    'ZS5tc2c9ImludmFsaWQgbGl0ZXJhbC9sZW5ndGggY29kZSIsci5tb2RlPTMw'
    'O2JyZWFrfXIuZXh0cmE9MTUmYixyLm1vZGU9MjI7Y2FzZSAyMjppZihyLmV4'
    'dHJhKXtmb3IoUD1yLmV4dHJhO0U8UDspe2lmKDA9PT1oKWJyZWFrIGU7aC0t'
    'LHArPWNbbCsrXTw8RSxFKz04fXIubGVuZ3RoKz1wJigxPDxyLmV4dHJhKS0x'
    'LHA+Pj49ci5leHRyYSxFLT1yLmV4dHJhLHIuYmFjays9ci5leHRyYX1yLndh'
    'cz1yLmxlbmd0aCxyLm1vZGU9MjM7Y2FzZSAyMzpmb3IoO2I9KEw9ci5kaXN0'
    'Y29kZVtwJigxPDxyLmRpc3RiaXRzKS0xXSk+Pj4xNiYyNTUsUj02NTUzNSZM'
    'LCEoKFQ9TD4+PjI0KTw9RSk7KXtpZigwPT09aClicmVhayBlO2gtLSxwKz1j'
    'W2wrK108PEUsRSs9OH1pZighKDI0MCZiKSl7Zm9yKE09VCxrPWIsUz1SO2I9'
    'KEw9ci5kaXN0Y29kZVtTKygocCYoMTw8TStrKS0xKT4+TSldKT4+PjE2JjI1'
    'NSxSPTY1NTM1JkwsIShNKyhUPUw+Pj4yNCk8PUUpOyl7aWYoMD09PWgpYnJl'
    'YWsgZTtoLS0scCs9Y1tsKytdPDxFLEUrPTh9cD4+Pj1NLEUtPU0sci5iYWNr'
    'Kz1NfWlmKHA+Pj49VCxFLT1ULHIuYmFjays9VCw2NCZiKXtlLm1zZz0iaW52'
    'YWxpZCBkaXN0YW5jZSBjb2RlIixyLm1vZGU9MzA7YnJlYWt9ci5vZmZzZXQ9'
    'UixyLmV4dHJhPTE1JmIsci5tb2RlPTI0O2Nhc2UgMjQ6aWYoci5leHRyYSl7'
    'Zm9yKFA9ci5leHRyYTtFPFA7KXtpZigwPT09aClicmVhayBlO2gtLSxwKz1j'
    'W2wrK108PEUsRSs9OH1yLm9mZnNldCs9cCYoMTw8ci5leHRyYSktMSxwPj4+'
    'PXIuZXh0cmEsRS09ci5leHRyYSxyLmJhY2srPXIuZXh0cmF9aWYoci5vZmZz'
    'ZXQ+ci5kbWF4KXtlLm1zZz0iaW52YWxpZCBkaXN0YW5jZSB0b28gZmFyIGJh'
    'Y2siLHIubW9kZT0zMDticmVha31yLm1vZGU9MjU7Y2FzZSAyNTppZigwPT09'
    'ZilicmVhayBlO2lmKG09SC1mLHIub2Zmc2V0Pm0pe2lmKChtPXIub2Zmc2V0'
    'LW0pPnIud2hhdmUmJnIuc2FuZSl7ZS5tc2c9ImludmFsaWQgZGlzdGFuY2Ug'
    'dG9vIGZhciBiYWNrIixyLm1vZGU9MzA7YnJlYWt9Zz1tPnIud25leHQ/KG0t'
    'PXIud25leHQsci53c2l6ZS1tKTpyLnduZXh0LW0sbT5yLmxlbmd0aCYmKG09'
    'ci5sZW5ndGgpLHk9ci53aW5kb3d9ZWxzZSB5PXUsZz13LXIub2Zmc2V0LG09'
    'ci5sZW5ndGg7Zm9yKGY8bSYmKG09ZiksZi09bSxyLmxlbmd0aC09bTt1W3cr'
    'K109eVtnKytdLC0tbTspOzA9PT1yLmxlbmd0aCYmKHIubW9kZT0yMSk7YnJl'
    'YWs7Y2FzZSAyNjppZigwPT09ZilicmVhayBlO3VbdysrXT1yLmxlbmd0aCxm'
    'LS0sci5tb2RlPTIxO2JyZWFrO2Nhc2UgMjc6aWYoci53cmFwKXtmb3IoO0U8'
    'MzI7KXtpZigwPT09aClicmVhayBlO2gtLSxwfD1jW2wrK108PEUsRSs9OH1p'
    'ZihILT1mLGUudG90YWxfb3V0Kz1ILHIudG90YWwrPUgsSCYmKGUuYWRsZXI9'
    'ci5jaGVjaz1yLmZsYWdzP3Moci5jaGVjayx1LEgsdy1IKTppKHIuY2hlY2ss'
    'dSxILHctSCkpLEg9Ziwoci5mbGFncz9wOkEocCkpIT09ci5jaGVjayl7ZS5t'
    'c2c9ImluY29ycmVjdCBkYXRhIGNoZWNrIixyLm1vZGU9MzA7YnJlYWt9RT1w'
    'PTB9ci5tb2RlPTI4O2Nhc2UgMjg6aWYoci53cmFwJiZyLmZsYWdzKXtmb3Io'
    'O0U8MzI7KXtpZigwPT09aClicmVhayBlO2gtLSxwKz1jW2wrK108PEUsRSs9'
    'OH1pZihwIT09KDQyOTQ5NjcyOTUmci50b3RhbCkpe2UubXNnPSJpbmNvcnJl'
    'Y3QgbGVuZ3RoIGNoZWNrIixyLm1vZGU9MzA7YnJlYWt9RT1wPTB9ci5tb2Rl'
    'PTI5O2Nhc2UgMjk6Xz0xO2JyZWFrIGU7Y2FzZSAzMDpfPS0zO2JyZWFrIGU7'
    'Y2FzZSAzMTpyZXR1cm4tNDtjYXNlIDMyOmRlZmF1bHQ6cmV0dXJuIGR9cmV0'
    'dXJuIGUubmV4dF9vdXQ9dyxlLmF2YWlsX291dD1mLGUubmV4dF9pbj1sLGUu'
    'YXZhaWxfaW49aCxyLmhvbGQ9cCxyLmJpdHM9RSwoci53c2l6ZXx8SCE9PWUu'
    'YXZhaWxfb3V0JiZyLm1vZGU8MzAmJihyLm1vZGU8Mjd8fDQhPT10KSkmJnYo'
    'ZSxlLm91dHB1dCxlLm5leHRfb3V0LEgtZS5hdmFpbF9vdXQpPyhyLm1vZGU9'
    'MzEsLTQpOihCLT1lLmF2YWlsX2luLEgtPWUuYXZhaWxfb3V0LGUudG90YWxf'
    'aW4rPUIsZS50b3RhbF9vdXQrPUgsci50b3RhbCs9SCxyLndyYXAmJkgmJihl'
    'LmFkbGVyPXIuY2hlY2s9ci5mbGFncz9zKHIuY2hlY2ssdSxILGUubmV4dF9v'
    'dXQtSCk6aShyLmNoZWNrLHUsSCxlLm5leHRfb3V0LUgpKSxlLmRhdGFfdHlw'
    'ZT1yLmJpdHMrKHIubGFzdD82NDowKSsoMTI9PT1yLm1vZGU/MTI4OjApKygy'
    'MD09PXIubW9kZXx8MTU9PT1yLm1vZGU/MjU2OjApLCgwPT1CJiYwPT09SHx8'
    'ND09PXQpJiYwPT09XyYmKF89LTUpLF8pfSxyLmluZmxhdGVFbmQ9ZnVuY3Rp'
    'b24oZSl7aWYoIWV8fCFlLnN0YXRlKXJldHVybiBkO3ZhciB0PWUuc3RhdGU7'
    'cmV0dXJuIHQud2luZG93JiYodC53aW5kb3c9bnVsbCksZS5zdGF0ZT1udWxs'
    'LDB9LHIuaW5mbGF0ZUdldEhlYWRlcj1mdW5jdGlvbihlLHQpe3ZhciByO3Jl'
    'dHVybiBlJiZlLnN0YXRlJiYyJihyPWUuc3RhdGUpLndyYXA/KChyLmhlYWQ9'
    'dCkuZG9uZT0hMSwwKTpkfSxyLmluZmxhdGVTZXREaWN0aW9uYXJ5PWZ1bmN0'
    'aW9uKGUsdCl7dmFyIHIsbj10Lmxlbmd0aDtyZXR1cm4gZSYmZS5zdGF0ZT8w'
    'IT09KHI9ZS5zdGF0ZSkud3JhcCYmMTEhPT1yLm1vZGU/ZDoxMT09PXIubW9k'
    'ZSYmaSgxLHQsbiwwKSE9PXIuY2hlY2s/LTM6dihlLHQsbixuKT8oci5tb2Rl'
    'PTMxLC00KTooci5oYXZlZGljdD0xLDApOmR9LHIuaW5mbGF0ZUluZm89InBh'
    'a28gaW5mbGF0ZSAoZnJvbSBOb2RlY2EgcHJvamVjdCkifSx7Ii4uL3V0aWxz'
    'L2NvbW1vbiI6NDEsIi4vYWRsZXIzMiI6NDMsIi4vY3JjMzIiOjQ1LCIuL2lu'
    'ZmZhc3QiOjQ4LCIuL2luZnRyZWVzIjo1MH1dLDUwOltmdW5jdGlvbihlLHQs'
    'cil7dmFyIG49ZSgiLi4vdXRpbHMvY29tbW9uIiksaT1bMyw0LDUsNiw3LDgs'
    'OSwxMCwxMSwxMywxNSwxNywxOSwyMywyNywzMSwzNSw0Myw1MSw1OSw2Nyw4'
    'Myw5OSwxMTUsMTMxLDE2MywxOTUsMjI3LDI1OCwwLDBdLHM9WzE2LDE2LDE2'
    'LDE2LDE2LDE2LDE2LDE2LDE3LDE3LDE3LDE3LDE4LDE4LDE4LDE4LDE5LDE5'
    'LDE5LDE5LDIwLDIwLDIwLDIwLDIxLDIxLDIxLDIxLDE2LDcyLDc4XSxvPVsx'
    'LDIsMyw0LDUsNyw5LDEzLDE3LDI1LDMzLDQ5LDY1LDk3LDEyOSwxOTMsMjU3'
    'LDM4NSw1MTMsNzY5LDEwMjUsMTUzNywyMDQ5LDMwNzMsNDA5Nyw2MTQ1LDgx'
    'OTMsMTIyODksMTYzODUsMjQ1NzcsMCwwXSxhPVsxNiwxNiwxNiwxNiwxNywx'
    'NywxOCwxOCwxOSwxOSwyMCwyMCwyMSwyMSwyMiwyMiwyMywyMywyNCwyNCwy'
    'NSwyNSwyNiwyNiwyNywyNywyOCwyOCwyOSwyOSw2NCw2NF07dC5leHBvcnRz'
    'PWZ1bmN0aW9uKGUsdCxyLGMsdSxsLGQsdyl7dmFyIGgsZixBLHAsRSxCLEgs'
    'bSxnLHk9dy5iaXRzLFQ9MCx4PTAsdj0wLGI9MCxSPTAsTT0wLGs9MCxTPTAs'
    'Qz0wLF89MCxPPW51bGwsUD0wLEw9bmV3IG4uQnVmMTYoMTYpLEk9bmV3IG4u'
    'QnVmMTYoMTYpLEQ9bnVsbCxVPTA7Zm9yKFQ9MDtUPD0xNTtUKyspTFtUXT0w'
    'O2Zvcih4PTA7eDxjO3grKylMW3Rbcit4XV0rKztmb3IoUj15LGI9MTU7MTw9'
    'YiYmMD09PUxbYl07Yi0tKTtpZihiPFImJihSPWIpLDA9PT1iKXJldHVybiB1'
    'W2wrK109MjA5NzE1MjAsdVtsKytdPTIwOTcxNTIwLHcuYml0cz0xLDA7Zm9y'
    'KHY9MTt2PGImJjA9PT1MW3ZdO3YrKyk7Zm9yKFI8diYmKFI9diksVD1TPTE7'
    'VDw9MTU7VCsrKWlmKFM8PD0xLChTLT1MW1RdKTwwKXJldHVybi0xO2lmKDA8'
    'UyYmKDA9PT1lfHwxIT09YikpcmV0dXJuLTE7Zm9yKElbMV09MCxUPTE7VDwx'
    'NTtUKyspSVtUKzFdPUlbVF0rTFtUXTtmb3IoeD0wO3g8Yzt4KyspMCE9PXRb'
    'cit4XSYmKGRbSVt0W3IreF1dKytdPXgpO2lmKEI9MD09PWU/KE89RD1kLDE5'
    'KToxPT09ZT8oTz1pLFAtPTI1NyxEPXMsVS09MjU3LDI1Nik6KE89byxEPWEs'
    'LTEpLFQ9dixFPWwsaz14PV89MCxBPS0xLHA9KEM9MTw8KE09UikpLTEsMT09'
    'PWUmJjg1MjxDfHwyPT09ZSYmNTkyPEMpcmV0dXJuIDE7Zm9yKDs7KXtmb3Io'
    'SD1ULWssZz1kW3hdPEI/KG09MCxkW3hdKTpkW3hdPkI/KG09RFtVK2RbeF1d'
    'LE9bUCtkW3hdXSk6KG09OTYsMCksaD0xPDxULWssdj1mPTE8PE07dVtFKyhf'
    'Pj5rKSsoZi09aCldPUg8PDI0fG08PDE2fGcsMCE9PWY7KTtmb3IoaD0xPDxU'
    'LTE7XyZoOyloPj49MTtpZigwIT09aD8oXyY9aC0xLF8rPWgpOl89MCx4Kyss'
    'MD09LS1MW1RdKXtpZihUPT09YilicmVhaztUPXRbcitkW3hdXX1pZihSPFQm'
    'JihfJnApIT09QSl7Zm9yKDA9PT1rJiYoaz1SKSxFKz12LFM9MTw8KE09VC1r'
    'KTtNK2s8YiYmISgoUy09TFtNK2tdKTw9MCk7KU0rKyxTPDw9MTtpZihDKz0x'
    'PDxNLDE9PT1lJiY4NTI8Q3x8Mj09PWUmJjU5MjxDKXJldHVybiAxO3VbQT1f'
    'JnBdPVI8PDI0fE08PDE2fEUtbH19cmV0dXJuIDAhPT1fJiYodVtFK19dPVQt'
    'azw8MjR8NjQ8PDE2KSx3LmJpdHM9UiwwfX0seyIuLi91dGlscy9jb21tb24i'
    'OjQxfV0sNTE6W2Z1bmN0aW9uKGUsdCxyKXt0LmV4cG9ydHM9ezI6Im5lZWQg'
    'ZGljdGlvbmFyeSIsMToic3RyZWFtIGVuZCIsMDoiIiwiLTEiOiJmaWxlIGVy'
    'cm9yIiwiLTIiOiJzdHJlYW0gZXJyb3IiLCItMyI6ImRhdGEgZXJyb3IiLCIt'
    'NCI6Imluc3VmZmljaWVudCBtZW1vcnkiLCItNSI6ImJ1ZmZlciBlcnJvciIs'
    'Ii02IjoiaW5jb21wYXRpYmxlIHZlcnNpb24ifX0se31dLDUyOltmdW5jdGlv'
    'bihlLHQscil7dmFyIG49ZSgiLi4vdXRpbHMvY29tbW9uIiksaT0wLHM9MTtm'
    'dW5jdGlvbiBvKGUpe2Zvcih2YXIgdD1lLmxlbmd0aDswPD0tLXQ7KWVbdF09'
    'MH12YXIgYT0wLGM9MjksdT0yNTYsbD0yODYsZD0zMCx3PTE5LGg9NTczLGY9'
    'MTUsQT0xNixwPTcsRT0yNTYsQj0xNixIPTE3LG09MTgsZz1bMCwwLDAsMCww'
    'LDAsMCwwLDEsMSwxLDEsMiwyLDIsMiwzLDMsMywzLDQsNCw0LDQsNSw1LDUs'
    'NSwwXSx5PVswLDAsMCwwLDEsMSwyLDIsMywzLDQsNCw1LDUsNiw2LDcsNyw4'
    'LDgsOSw5LDEwLDEwLDExLDExLDEyLDEyLDEzLDEzXSxUPVswLDAsMCwwLDAs'
    'MCwwLDAsMCwwLDAsMCwwLDAsMCwwLDIsMyw3XSx4PVsxNiwxNywxOCwwLDgs'
    'Nyw5LDYsMTAsNSwxMSw0LDEyLDMsMTMsMiwxNCwxLDE1XSx2PW5ldyBBcnJh'
    'eSg1NzYpO28odik7dmFyIGI9bmV3IEFycmF5KDYwKTtvKGIpO3ZhciBSPW5l'
    'dyBBcnJheSg1MTIpO28oUik7dmFyIE09bmV3IEFycmF5KDI1Nik7byhNKTt2'
    'YXIgaz1uZXcgQXJyYXkoYyk7byhrKTt2YXIgUyxDLF8sTz1uZXcgQXJyYXko'
    'ZCk7ZnVuY3Rpb24gUChlLHQscixuLGkpe3RoaXMuc3RhdGljX3RyZWU9ZSx0'
    'aGlzLmV4dHJhX2JpdHM9dCx0aGlzLmV4dHJhX2Jhc2U9cix0aGlzLmVsZW1z'
    'PW4sdGhpcy5tYXhfbGVuZ3RoPWksdGhpcy5oYXNfc3RyZWU9ZSYmZS5sZW5n'
    'dGh9ZnVuY3Rpb24gTChlLHQpe3RoaXMuZHluX3RyZWU9ZSx0aGlzLm1heF9j'
    'b2RlPTAsdGhpcy5zdGF0X2Rlc2M9dH1mdW5jdGlvbiBJKGUpe3JldHVybiBl'
    'PDI1Nj9SW2VdOlJbMjU2KyhlPj4+NyldfWZ1bmN0aW9uIEQoZSx0KXtlLnBl'
    'bmRpbmdfYnVmW2UucGVuZGluZysrXT0yNTUmdCxlLnBlbmRpbmdfYnVmW2Uu'
    'cGVuZGluZysrXT10Pj4+OCYyNTV9ZnVuY3Rpb24gVShlLHQscil7ZS5iaV92'
    'YWxpZD5BLXI/KGUuYmlfYnVmfD10PDxlLmJpX3ZhbGlkJjY1NTM1LEQoZSxl'
    'LmJpX2J1ZiksZS5iaV9idWY9dD4+QS1lLmJpX3ZhbGlkLGUuYmlfdmFsaWQr'
    'PXItQSk6KGUuYmlfYnVmfD10PDxlLmJpX3ZhbGlkJjY1NTM1LGUuYmlfdmFs'
    'aWQrPXIpfWZ1bmN0aW9uIE4oZSx0LHIpe1UoZSxyWzIqdF0sclsyKnQrMV0p'
    'fWZ1bmN0aW9uIHooZSx0KXtmb3IodmFyIHI9MDtyfD0xJmUsZT4+Pj0xLHI8'
    'PD0xLDA8LS10Oyk7cmV0dXJuIHI+Pj4xfWZ1bmN0aW9uIFgoZSx0LHIpe3Zh'
    'ciBuLGkscz1uZXcgQXJyYXkoMTYpLG89MDtmb3Iobj0xO248PWY7bisrKXNb'
    'bl09bz1vK3Jbbi0xXTw8MTtmb3IoaT0wO2k8PXQ7aSsrKXt2YXIgYT1lWzIq'
    'aSsxXTswIT09YSYmKGVbMippXT16KHNbYV0rKyxhKSl9fWZ1bmN0aW9uIEYo'
    'ZSl7dmFyIHQ7Zm9yKHQ9MDt0PGw7dCsrKWUuZHluX2x0cmVlWzIqdF09MDtm'
    'b3IodD0wO3Q8ZDt0KyspZS5keW5fZHRyZWVbMip0XT0wO2Zvcih0PTA7dDx3'
    'O3QrKyllLmJsX3RyZWVbMip0XT0wO2UuZHluX2x0cmVlWzUxMl09MSxlLm9w'
    'dF9sZW49ZS5zdGF0aWNfbGVuPTAsZS5sYXN0X2xpdD1lLm1hdGNoZXM9MH1m'
    'dW5jdGlvbiBqKGUpezg8ZS5iaV92YWxpZD9EKGUsZS5iaV9idWYpOjA8ZS5i'
    'aV92YWxpZCYmKGUucGVuZGluZ19idWZbZS5wZW5kaW5nKytdPWUuYmlfYnVm'
    'KSxlLmJpX2J1Zj0wLGUuYmlfdmFsaWQ9MH1mdW5jdGlvbiBXKGUsdCxyLG4p'
    'e3ZhciBpPTIqdCxzPTIqcjtyZXR1cm4gZVtpXTxlW3NdfHxlW2ldPT09ZVtz'
    'XSYmblt0XTw9bltyXX1mdW5jdGlvbiBKKGUsdCxyKXtmb3IodmFyIG49ZS5o'
    'ZWFwW3JdLGk9cjw8MTtpPD1lLmhlYXBfbGVuJiYoaTxlLmhlYXBfbGVuJiZX'
    'KHQsZS5oZWFwW2krMV0sZS5oZWFwW2ldLGUuZGVwdGgpJiZpKyssIVcodCxu'
    'LGUuaGVhcFtpXSxlLmRlcHRoKSk7KWUuaGVhcFtyXT1lLmhlYXBbaV0scj1p'
    'LGk8PD0xO2UuaGVhcFtyXT1ufWZ1bmN0aW9uIEsoZSx0LHIpe3ZhciBuLGks'
    'cyxvLGE9MDtpZigwIT09ZS5sYXN0X2xpdClmb3IoO249ZS5wZW5kaW5nX2J1'
    'ZltlLmRfYnVmKzIqYV08PDh8ZS5wZW5kaW5nX2J1ZltlLmRfYnVmKzIqYSsx'
    'XSxpPWUucGVuZGluZ19idWZbZS5sX2J1ZithXSxhKyssMD09PW4/TihlLGks'
    'dCk6KE4oZSwocz1NW2ldKSt1KzEsdCksMCE9PShvPWdbc10pJiZVKGUsaS09'
    'a1tzXSxvKSxOKGUscz1JKC0tbiksciksMCE9PShvPXlbc10pJiZVKGUsbi09'
    'T1tzXSxvKSksYTxlLmxhc3RfbGl0Oyk7TihlLEUsdCl9ZnVuY3Rpb24gVihl'
    'LHQpe3ZhciByLG4saSxzPXQuZHluX3RyZWUsbz10LnN0YXRfZGVzYy5zdGF0'
    'aWNfdHJlZSxhPXQuc3RhdF9kZXNjLmhhc19zdHJlZSxjPXQuc3RhdF9kZXNj'
    'LmVsZW1zLHU9LTE7Zm9yKGUuaGVhcF9sZW49MCxlLmhlYXBfbWF4PWgscj0w'
    'O3I8YztyKyspMCE9PXNbMipyXT8oZS5oZWFwWysrZS5oZWFwX2xlbl09dT1y'
    'LGUuZGVwdGhbcl09MCk6c1syKnIrMV09MDtmb3IoO2UuaGVhcF9sZW48Mjsp'
    'c1syKihpPWUuaGVhcFsrK2UuaGVhcF9sZW5dPXU8Mj8rK3U6MCldPTEsZS5k'
    'ZXB0aFtpXT0wLGUub3B0X2xlbi0tLGEmJihlLnN0YXRpY19sZW4tPW9bMipp'
    'KzFdKTtmb3IodC5tYXhfY29kZT11LHI9ZS5oZWFwX2xlbj4+MTsxPD1yO3It'
    'LSlKKGUscyxyKTtmb3IoaT1jO3I9ZS5oZWFwWzFdLGUuaGVhcFsxXT1lLmhl'
    'YXBbZS5oZWFwX2xlbi0tXSxKKGUscywxKSxuPWUuaGVhcFsxXSxlLmhlYXBb'
    'LS1lLmhlYXBfbWF4XT1yLGUuaGVhcFstLWUuaGVhcF9tYXhdPW4sc1syKmld'
    'PXNbMipyXStzWzIqbl0sZS5kZXB0aFtpXT0oZS5kZXB0aFtyXT49ZS5kZXB0'
    'aFtuXT9lLmRlcHRoW3JdOmUuZGVwdGhbbl0pKzEsc1syKnIrMV09c1syKm4r'
    'MV09aSxlLmhlYXBbMV09aSsrLEooZSxzLDEpLDI8PWUuaGVhcF9sZW47KTtl'
    'LmhlYXBbLS1lLmhlYXBfbWF4XT1lLmhlYXBbMV0sZnVuY3Rpb24oZSx0KXt2'
    'YXIgcixuLGkscyxvLGEsYz10LmR5bl90cmVlLHU9dC5tYXhfY29kZSxsPXQu'
    'c3RhdF9kZXNjLnN0YXRpY190cmVlLGQ9dC5zdGF0X2Rlc2MuaGFzX3N0cmVl'
    'LHc9dC5zdGF0X2Rlc2MuZXh0cmFfYml0cyxBPXQuc3RhdF9kZXNjLmV4dHJh'
    'X2Jhc2UscD10LnN0YXRfZGVzYy5tYXhfbGVuZ3RoLEU9MDtmb3Iocz0wO3M8'
    'PWY7cysrKWUuYmxfY291bnRbc109MDtmb3IoY1syKmUuaGVhcFtlLmhlYXBf'
    'bWF4XSsxXT0wLHI9ZS5oZWFwX21heCsxO3I8aDtyKyspcDwocz1jWzIqY1sy'
    'KihuPWUuaGVhcFtyXSkrMV0rMV0rMSkmJihzPXAsRSsrKSxjWzIqbisxXT1z'
    'LHU8bnx8KGUuYmxfY291bnRbc10rKyxvPTAsQTw9biYmKG89d1tuLUFdKSxh'
    'PWNbMipuXSxlLm9wdF9sZW4rPWEqKHMrbyksZCYmKGUuc3RhdGljX2xlbis9'
    'YSoobFsyKm4rMV0rbykpKTtpZigwIT09RSl7ZG97Zm9yKHM9cC0xOzA9PT1l'
    'LmJsX2NvdW50W3NdOylzLS07ZS5ibF9jb3VudFtzXS0tLGUuYmxfY291bnRb'
    'cysxXSs9MixlLmJsX2NvdW50W3BdLS0sRS09Mn13aGlsZSgwPEUpO2Zvcihz'
    'PXA7MCE9PXM7cy0tKWZvcihuPWUuYmxfY291bnRbc107MCE9PW47KXU8KGk9'
    'ZS5oZWFwWy0tcl0pfHwoY1syKmkrMV0hPT1zJiYoZS5vcHRfbGVuKz0ocy1j'
    'WzIqaSsxXSkqY1syKmldLGNbMippKzFdPXMpLG4tLSl9fShlLHQpLFgocyx1'
    'LGUuYmxfY291bnQpfWZ1bmN0aW9uIFkoZSx0LHIpe3ZhciBuLGkscz0tMSxv'
    'PXRbMV0sYT0wLGM9Nyx1PTQ7Zm9yKDA9PT1vJiYoYz0xMzgsdT0zKSx0WzIq'
    'KHIrMSkrMV09NjU1MzUsbj0wO248PXI7bisrKWk9byxvPXRbMioobisxKSsx'
    'XSwrK2E8YyYmaT09PW98fChhPHU/ZS5ibF90cmVlWzIqaV0rPWE6MCE9PWk/'
    'KGkhPT1zJiZlLmJsX3RyZWVbMippXSsrLGUuYmxfdHJlZVszMl0rKyk6YTw9'
    'MTA/ZS5ibF90cmVlWzM0XSsrOmUuYmxfdHJlZVszNl0rKyxzPWksdT0oYT0w'
    'KT09PW8/KGM9MTM4LDMpOmk9PT1vPyhjPTYsMyk6KGM9Nyw0KSl9ZnVuY3Rp'
    'b24gWihlLHQscil7dmFyIG4saSxzPS0xLG89dFsxXSxhPTAsYz03LHU9NDtm'
    'b3IoMD09PW8mJihjPTEzOCx1PTMpLG49MDtuPD1yO24rKylpZihpPW8sbz10'
    'WzIqKG4rMSkrMV0sISgrK2E8YyYmaT09PW8pKXtpZihhPHUpZm9yKDtOKGUs'
    'aSxlLmJsX3RyZWUpLDAhPS0tYTspO2Vsc2UgMCE9PWk/KGkhPT1zJiYoTihl'
    'LGksZS5ibF90cmVlKSxhLS0pLE4oZSxCLGUuYmxfdHJlZSksVShlLGEtMywy'
    'KSk6YTw9MTA/KE4oZSxILGUuYmxfdHJlZSksVShlLGEtMywzKSk6KE4oZSxt'
    'LGUuYmxfdHJlZSksVShlLGEtMTEsNykpO3M9aSx1PShhPTApPT09bz8oYz0x'
    'MzgsMyk6aT09PW8/KGM9NiwzKTooYz03LDQpfX1vKE8pO3ZhciBHPSExO2Z1'
    'bmN0aW9uIFEoZSx0LHIsaSl7dmFyIHMsbyxhLGM7VShlLDArKGk/MTowKSwz'
    'KSxvPXQsYT1yLGM9ITAsaihzPWUpLEQocyxhKSxEKHMsfmEpLG4uYXJyYXlT'
    'ZXQocy5wZW5kaW5nX2J1ZixzLndpbmRvdyxvLGEscy5wZW5kaW5nKSxzLnBl'
    'bmRpbmcrPWF9ci5fdHJfaW5pdD1mdW5jdGlvbihlKXtHfHwoZnVuY3Rpb24o'
    'KXt2YXIgZSx0LHIsbixpLHM9bmV3IEFycmF5KDE2KTtmb3Iobj1yPTA7bjwy'
    'ODtuKyspZm9yKGtbbl09cixlPTA7ZTwxPDxnW25dO2UrKylNW3IrK109bjtm'
    'b3IoTVtyLTFdPW4sbj1pPTA7bjwxNjtuKyspZm9yKE9bbl09aSxlPTA7ZTwx'
    'PDx5W25dO2UrKylSW2krK109bjtmb3IoaT4+PTc7bjxkO24rKylmb3IoT1tu'
    'XT1pPDw3LGU9MDtlPDE8PHlbbl0tNztlKyspUlsyNTYraSsrXT1uO2Zvcih0'
    'PTA7dDw9Zjt0Kyspc1t0XT0wO2ZvcihlPTA7ZTw9MTQzOyl2WzIqZSsxXT04'
    'LGUrKyxzWzhdKys7Zm9yKDtlPD0yNTU7KXZbMiplKzFdPTksZSsrLHNbOV0r'
    'Kztmb3IoO2U8PTI3OTspdlsyKmUrMV09NyxlKyssc1s3XSsrO2Zvcig7ZTw9'
    'Mjg3Oyl2WzIqZSsxXT04LGUrKyxzWzhdKys7Zm9yKFgodiwyODcscyksZT0w'
    'O2U8ZDtlKyspYlsyKmUrMV09NSxiWzIqZV09eihlLDUpO1M9bmV3IFAodixn'
    'LDI1NyxsLGYpLEM9bmV3IFAoYix5LDAsZCxmKSxfPW5ldyBQKG5ldyBBcnJh'
    'eSgwKSxULDAsdyw3KX0oKSxHPSEwKSxlLmxfZGVzYz1uZXcgTChlLmR5bl9s'
    'dHJlZSxTKSxlLmRfZGVzYz1uZXcgTChlLmR5bl9kdHJlZSxDKSxlLmJsX2Rl'
    'c2M9bmV3IEwoZS5ibF90cmVlLF8pLGUuYmlfYnVmPTAsZS5iaV92YWxpZD0w'
    'LEYoZSl9LHIuX3RyX3N0b3JlZF9ibG9jaz1RLHIuX3RyX2ZsdXNoX2Jsb2Nr'
    'PWZ1bmN0aW9uKGUsdCxyLG4pe3ZhciBpLHMsbz0wOzA8ZS5sZXZlbD8oMj09'
    'PWUuc3RybS5kYXRhX3R5cGUmJihlLnN0cm0uZGF0YV90eXBlPWZ1bmN0aW9u'
    'KGUpe3ZhciB0LHI9NDA5MzYyNDQ0Nztmb3IodD0wO3Q8PTMxO3QrKyxyPj4+'
    'PTEpaWYoMSZyJiYwIT09ZS5keW5fbHRyZWVbMip0XSlyZXR1cm4gMDtpZigw'
    'IT09ZS5keW5fbHRyZWVbMThdfHwwIT09ZS5keW5fbHRyZWVbMjBdfHwwIT09'
    'ZS5keW5fbHRyZWVbMjZdKXJldHVybiAxO2Zvcih0PTMyO3Q8dTt0KyspaWYo'
    'MCE9PWUuZHluX2x0cmVlWzIqdF0pcmV0dXJuIDE7cmV0dXJuIDB9KGUpKSxW'
    'KGUsZS5sX2Rlc2MpLFYoZSxlLmRfZGVzYyksbz1mdW5jdGlvbihlKXt2YXIg'
    'dDtmb3IoWShlLGUuZHluX2x0cmVlLGUubF9kZXNjLm1heF9jb2RlKSxZKGUs'
    'ZS5keW5fZHRyZWUsZS5kX2Rlc2MubWF4X2NvZGUpLFYoZSxlLmJsX2Rlc2Mp'
    'LHQ9MTg7Mzw9dCYmMD09PWUuYmxfdHJlZVsyKnhbdF0rMV07dC0tKTtyZXR1'
    'cm4gZS5vcHRfbGVuKz0zKih0KzEpKzUrNSs0LHR9KGUpLGk9ZS5vcHRfbGVu'
    'KzMrNz4+PjMsKHM9ZS5zdGF0aWNfbGVuKzMrNz4+PjMpPD1pJiYoaT1zKSk6'
    'aT1zPXIrNSxyKzQ8PWkmJi0xIT09dD9RKGUsdCxyLG4pOjQ9PT1lLnN0cmF0'
    'ZWd5fHxzPT09aT8oVShlLDIrKG4/MTowKSwzKSxLKGUsdixiKSk6KFUoZSw0'
    'KyhuPzE6MCksMyksZnVuY3Rpb24oZSx0LHIsbil7dmFyIGk7Zm9yKFUoZSx0'
    'LTI1Nyw1KSxVKGUsci0xLDUpLFUoZSxuLTQsNCksaT0wO2k8bjtpKyspVShl'
    'LGUuYmxfdHJlZVsyKnhbaV0rMV0sMyk7WihlLGUuZHluX2x0cmVlLHQtMSks'
    'WihlLGUuZHluX2R0cmVlLHItMSl9KGUsZS5sX2Rlc2MubWF4X2NvZGUrMSxl'
    'LmRfZGVzYy5tYXhfY29kZSsxLG8rMSksSyhlLGUuZHluX2x0cmVlLGUuZHlu'
    'X2R0cmVlKSksRihlKSxuJiZqKGUpfSxyLl90cl90YWxseT1mdW5jdGlvbihl'
    'LHQscil7cmV0dXJuIGUucGVuZGluZ19idWZbZS5kX2J1ZisyKmUubGFzdF9s'
    'aXRdPXQ+Pj44JjI1NSxlLnBlbmRpbmdfYnVmW2UuZF9idWYrMiplLmxhc3Rf'
    'bGl0KzFdPTI1NSZ0LGUucGVuZGluZ19idWZbZS5sX2J1ZitlLmxhc3RfbGl0'
    'XT0yNTUmcixlLmxhc3RfbGl0KyssMD09PXQ/ZS5keW5fbHRyZWVbMipyXSsr'
    'OihlLm1hdGNoZXMrKyx0LS0sZS5keW5fbHRyZWVbMiooTVtyXSt1KzEpXSsr'
    'LGUuZHluX2R0cmVlWzIqSSh0KV0rKyksZS5sYXN0X2xpdD09PWUubGl0X2J1'
    'ZnNpemUtMX0sci5fdHJfYWxpZ249ZnVuY3Rpb24oZSl7dmFyIHQ7VShlLDIs'
    'MyksTihlLEUsdiksMTY9PT0odD1lKS5iaV92YWxpZD8oRCh0LHQuYmlfYnVm'
    'KSx0LmJpX2J1Zj0wLHQuYmlfdmFsaWQ9MCk6ODw9dC5iaV92YWxpZCYmKHQu'
    'cGVuZGluZ19idWZbdC5wZW5kaW5nKytdPTI1NSZ0LmJpX2J1Zix0LmJpX2J1'
    'Zj4+PTgsdC5iaV92YWxpZC09OCl9fSx7Ii4uL3V0aWxzL2NvbW1vbiI6NDF9'
    'XSw1MzpbZnVuY3Rpb24oZSx0LHIpe3QuZXhwb3J0cz1mdW5jdGlvbigpe3Ro'
    'aXMuaW5wdXQ9bnVsbCx0aGlzLm5leHRfaW49MCx0aGlzLmF2YWlsX2luPTAs'
    'dGhpcy50b3RhbF9pbj0wLHRoaXMub3V0cHV0PW51bGwsdGhpcy5uZXh0X291'
    'dD0wLHRoaXMuYXZhaWxfb3V0PTAsdGhpcy50b3RhbF9vdXQ9MCx0aGlzLm1z'
    'Zz0iIix0aGlzLnN0YXRlPW51bGwsdGhpcy5kYXRhX3R5cGU9Mix0aGlzLmFk'
    'bGVyPTB9fSx7fV0sNTQ6W2Z1bmN0aW9uKGUsdCxyKXsoZnVuY3Rpb24oZSl7'
    'IWZ1bmN0aW9uKGUsdCl7aWYoIWUuc2V0SW1tZWRpYXRlKXt2YXIgcixuLGks'
    'cyxvPTEsYT17fSxjPSExLHU9ZS5kb2N1bWVudCxsPU9iamVjdC5nZXRQcm90'
    'b3R5cGVPZiYmT2JqZWN0LmdldFByb3RvdHlwZU9mKGUpO2w9bCYmbC5zZXRU'
    'aW1lb3V0P2w6ZSxyPSJbb2JqZWN0IHByb2Nlc3NdIj09PXt9LnRvU3RyaW5n'
    'LmNhbGwoZS5wcm9jZXNzKT9mdW5jdGlvbihlKXtwcm9jZXNzLm5leHRUaWNr'
    'KGZ1bmN0aW9uKCl7dyhlKX0pfTpmdW5jdGlvbigpe2lmKGUucG9zdE1lc3Nh'
    'Z2UmJiFlLmltcG9ydFNjcmlwdHMpe3ZhciB0PSEwLHI9ZS5vbm1lc3NhZ2U7'
    'cmV0dXJuIGUub25tZXNzYWdlPWZ1bmN0aW9uKCl7dD0hMX0sZS5wb3N0TWVz'
    'c2FnZSgiIiwiKiIpLGUub25tZXNzYWdlPXIsdH19KCk/KHM9InNldEltbWVk'
    'aWF0ZSQiK01hdGgucmFuZG9tKCkrIiQiLGUuYWRkRXZlbnRMaXN0ZW5lcj9l'
    'LmFkZEV2ZW50TGlzdGVuZXIoIm1lc3NhZ2UiLGgsITEpOmUuYXR0YWNoRXZl'
    'bnQoIm9ubWVzc2FnZSIsaCksZnVuY3Rpb24odCl7ZS5wb3N0TWVzc2FnZShz'
    'K3QsIioiKX0pOmUuTWVzc2FnZUNoYW5uZWw/KChpPW5ldyBNZXNzYWdlQ2hh'
    'bm5lbCkucG9ydDEub25tZXNzYWdlPWZ1bmN0aW9uKGUpe3coZS5kYXRhKX0s'
    'ZnVuY3Rpb24oZSl7aS5wb3J0Mi5wb3N0TWVzc2FnZShlKX0pOnUmJiJvbnJl'
    'YWR5c3RhdGVjaGFuZ2UiaW4gdS5jcmVhdGVFbGVtZW50KCJzY3JpcHQiKT8o'
    'bj11LmRvY3VtZW50RWxlbWVudCxmdW5jdGlvbihlKXt2YXIgdD11LmNyZWF0'
    'ZUVsZW1lbnQoInNjcmlwdCIpO3Qub25yZWFkeXN0YXRlY2hhbmdlPWZ1bmN0'
    'aW9uKCl7dyhlKSx0Lm9ucmVhZHlzdGF0ZWNoYW5nZT1udWxsLG4ucmVtb3Zl'
    'Q2hpbGQodCksdD1udWxsfSxuLmFwcGVuZENoaWxkKHQpfSk6ZnVuY3Rpb24o'
    'ZSl7c2V0VGltZW91dCh3LDAsZSl9LGwuc2V0SW1tZWRpYXRlPWZ1bmN0aW9u'
    'KGUpeyJmdW5jdGlvbiIhPXR5cGVvZiBlJiYoZT1uZXcgRnVuY3Rpb24oIiIr'
    'ZSkpO2Zvcih2YXIgdD1uZXcgQXJyYXkoYXJndW1lbnRzLmxlbmd0aC0xKSxu'
    'PTA7bjx0Lmxlbmd0aDtuKyspdFtuXT1hcmd1bWVudHNbbisxXTt2YXIgaT17'
    'Y2FsbGJhY2s6ZSxhcmdzOnR9O3JldHVybiBhW29dPWkscihvKSxvKyt9LGwu'
    'Y2xlYXJJbW1lZGlhdGU9ZH1mdW5jdGlvbiBkKGUpe2RlbGV0ZSBhW2VdfWZ1'
    'bmN0aW9uIHcoZSl7aWYoYylzZXRUaW1lb3V0KHcsMCxlKTtlbHNle3ZhciBy'
    'PWFbZV07aWYocil7Yz0hMDt0cnl7IWZ1bmN0aW9uKGUpe3ZhciByPWUuY2Fs'
    'bGJhY2ssbj1lLmFyZ3M7c3dpdGNoKG4ubGVuZ3RoKXtjYXNlIDA6cigpO2Jy'
    'ZWFrO2Nhc2UgMTpyKG5bMF0pO2JyZWFrO2Nhc2UgMjpyKG5bMF0sblsxXSk7'
    'YnJlYWs7Y2FzZSAzOnIoblswXSxuWzFdLG5bMl0pO2JyZWFrO2RlZmF1bHQ6'
    'ci5hcHBseSh0LG4pfX0ocil9ZmluYWxseXtkKGUpLGM9ITF9fX19ZnVuY3Rp'
    'b24gaCh0KXt0LnNvdXJjZT09PWUmJiJzdHJpbmciPT10eXBlb2YgdC5kYXRh'
    'JiYwPT09dC5kYXRhLmluZGV4T2YocykmJncoK3QuZGF0YS5zbGljZShzLmxl'
    'bmd0aCkpfX0oInVuZGVmaW5lZCI9PXR5cGVvZiBzZWxmP3ZvaWQgMD09PWU/'
    'dGhpczplOnNlbGYpfSkuY2FsbCh0aGlzLCJ1bmRlZmluZWQiIT10eXBlb2Yg'
    'Z2xvYmFsP2dsb2JhbDoidW5kZWZpbmVkIiE9dHlwZW9mIHNlbGY/c2VsZjoi'
    'dW5kZWZpbmVkIiE9dHlwZW9mIHdpbmRvdz93aW5kb3c6e30pfSx7fV19LHt9'
    'LFsxMF0pKDEwKX0pfX0pLGRsPVt7cHJpdmF0ZUtleToic0JtUVZIRXl3R0FL'
    'UThSYXR6by9mNU9VQ2E3TVNvelpwejFKSzJQU1ZYRT0iLHB1YmxpY0tleToi'
    'Ym1YT0MrRjFGeEVNRjlkeWlLMkg1LzFTVXR6SDBKdVZvNTFoMndQZmd5bz0i'
    'LHdhcnBJUHY2OiIyNjA2OjQ3MDA6MTEwOjhkZDg6ZGU1Zjo5YTg5OmJmYWM6'
    'NzQ5Yy8xMjgiLHJlc2VydmVkOiI1OW5LIn0se3ByaXZhdGVLZXk6Ik9QaUQ0'
    'ZGVQcTg2NTJESUNrbkpzVEpTNFVIMEZvV1kxZmZPWnpaaElzVXM9IixwdWJs'
    'aWNLZXk6ImJtWE9DK0YxRnhFTUY5ZHlpSzJINS8xU1V0ekgwSnVWbzUxaDJ3'
    'UGZneW89Iix3YXJwSVB2NjoiMjYwNjo0NzAwOjExMDo4OTEyOjEyMjU6NzBj'
    'ODoxYWQ3OjZjZTAvMTI4IixyZXNlcnZlZDoiRy9uaCJ9XTthc3luYyBmdW5j'
    'dGlvbiB3bChlKXtjb25zdCB0PVtdO3RyeXtjb25zdCByPVthd2FpdCBmbCgp'
    'LGF3YWl0IGZsKCldO2Zvcihjb25zdFtlLG5db2Ygci5lbnRyaWVzKCkpe2Nv'
    'bnN0e2NvbmZpZzpyfT1hd2FpdCBobChuKTt0LnB1c2goe3ByaXZhdGVLZXk6'
    'bi5wcml2YXRlS2V5LHdhcnBJUHY2OmAke3IuaW50ZXJmYWNlLmFkZHJlc3Nl'
    'cy52Nn0vMTI4YCxyZXNlcnZlZDpyLmNsaWVudF9pZCxwdWJsaWNLZXk6ci5w'
    'ZWVyc1swXS5wdWJsaWNfa2V5fSksMD09PWUmJmF3YWl0IG5ldyBQcm9taXNl'
    'KGU9PnNldFRpbWVvdXQoZSwxZTMpKX1yZXR1cm4gYXdhaXQgZS5rdi5wdXQo'
    'IndhcnBBY2NvdW50cyIsSlNPTi5zdHJpbmdpZnkodCkpLHR9Y2F0Y2goZSl7'
    'cmV0dXJuIGNvbnNvbGUuZXJyb3IoIkZhaWxlZCB0byBmZXRjaCBuZXcgV0FS'
    'UCBhY2NvdW50czoiLGUgaW5zdGFuY2VvZiBFcnJvcj9lLm1lc3NhZ2U6U3Ry'
    'aW5nKGUpKSxkbH19YXN5bmMgZnVuY3Rpb24gaGwoZSl7Y29uc3QgdD1hd2Fp'
    'dCBmZXRjaCgiaHR0cHM6Ly9hcGkuY2xvdWRmbGFyZWNsaWVudC5jb20vdjBh'
    'NDAwNS9yZWciLHttZXRob2Q6IlBPU1QiLGhlYWRlcnM6eyJVc2VyLUFnZW50'
    'IjoiaW5zb21uaWEvOC42LjEiLCJDb250ZW50LVR5cGUiOiJhcHBsaWNhdGlv'
    'bi9qc29uIn0sYm9keTpKU09OLnN0cmluZ2lmeSh7aW5zdGFsbF9pZDoiIixm'
    'Y21fdG9rZW46IiIsdG9zOihuZXcgRGF0ZSkudG9JU09TdHJpbmcoKSx0eXBl'
    'OiJBbmRyb2lkIixtb2RlbDoiUEMiLGxvY2FsZToiZW5fVVMiLHdhcnBfZW5h'
    'YmxlZDohMCxrZXk6ZS5wdWJsaWNLZXl9KX0pO2lmKCF0Lm9rKXRocm93IG5l'
    'dyBFcnJvcihgQVBJIHJldHVybmVkIHN0YXR1cyAke3Quc3RhdHVzfTogJHth'
    'd2FpdCB0LnRleHQoKX1gKTtyZXR1cm4gdC5qc29uKCl9YXN5bmMgZnVuY3Rp'
    'b24gZmwoKXtjb25zdCBlPWF3YWl0IGNyeXB0by5zdWJ0bGUuZ2VuZXJhdGVL'
    'ZXkoe25hbWU6IlgyNTUxOSIsbmFtZWRDdXJ2ZToiWDI1NTE5In0sITAsWyJk'
    'ZXJpdmVCaXRzIl0pLHQ9YXdhaXQgY3J5cHRvLnN1YnRsZS5leHBvcnRLZXko'
    'InBrY3M4IixlLnByaXZhdGVLZXkpLHI9bmV3IFVpbnQ4QXJyYXkodCkuc2xp'
    'Y2UoLTMyKSxuPXZvaWQgMCxpPWU9PmJ0b2EoU3RyaW5nLmZyb21DaGFyQ29k'
    'ZSguLi5lKSk7cmV0dXJue3B1YmxpY0tleTppKG5ldyBVaW50OEFycmF5KGF3'
    'YWl0IGNyeXB0by5zdWJ0bGUuZXhwb3J0S2V5KCJyYXciLGUucHVibGljS2V5'
    'KSkpLHByaXZhdGVLZXk6aShyKX19ZnVuY3Rpb24gQWwoZSl7Y29uc3QgdD0o'
    'bmV3IFRleHRFbmNvZGVyKS5lbmNvZGUoZSkscj1BcnJheS5mcm9tKHQsZT0+'
    'U3RyaW5nLmZyb21DaGFyQ29kZShlKSkuam9pbigiIik7cmV0dXJuIGJ0b2Eo'
    'cil9ZnVuY3Rpb24gcGwoZSl7cmV0dXJuKG5ldyBUZXh0RGVjb2RlcikuZGVj'
    'b2RlKFVpbnQ4QXJyYXkuZnJvbShhdG9iKGUpLGU9PmUuY2hhckNvZGVBdCgw'
    'KSkpfWZ1bmN0aW9uIEVsKGUpe2NvbnN0IHQ9dm9pZCAwO3JldHVybi9eWzAt'
    'OWEtZl17OH0tWzAtOWEtZl17NH0tWzRdWzAtOWEtZl17M30tWzg5YWJdWzAt'
    'OWEtZl17M30tWzAtOWEtZl17MTJ9JC9pLnRlc3QoZSl9ZnVuY3Rpb24gQmwo'
    'ZSx0LHIsbixpKXtjb25zdCBzPXsiQ29udGVudC1UeXBlIjoiYXBwbGljYXRp'
    'b24vanNvbiIsLi4uaX0sbz17c3VjY2VzczplLHN0YXR1czp0LG1lc3NhZ2U6'
    'cj8/bnVsbCxib2R5Om4/P251bGx9O3JldHVybiBuZXcgUmVzcG9uc2UoSlNP'
    'Ti5zdHJpbmdpZnkobykse3N0YXR1czp0LGhlYWRlcnM6c30pfWZ1bmN0aW9u'
    'IEhsKGUpe3JldHVybiBlIGluc3RhbmNlb2YgRXJyb3I/ZS5tZXNzYWdlOlN0'
    'cmluZyhlKX1mdW5jdGlvbiBtbChlKXtpZighZSlyZXR1cm4hMTtjb25zdCB0'
    'PXZvaWQgMDtyZXR1cm4vXig/IS0pKD86W0EtWmEtejAtOS1dezEsNjN9Likr'
    'W0EtWmEtel17Mix9JC8udGVzdChlKX1hc3luYyBmdW5jdGlvbiBnbChlLHQ9'
    'ITEpe2NvbnN0IHI9YGh0dHBzOi8vY2xvdWRmbGFyZS1kbnMuY29tL2Rucy1x'
    'dWVyeT9uYW1lPSR7ZW5jb2RlVVJJQ29tcG9uZW50KGUpfWAsbj17aXB2NDpg'
    'JHtyfSZ0eXBlPUFgLGlwdjY6YCR7cn0mdHlwZT1BQUFBYH07dHJ5e2NvbnN0'
    'IGU9YXdhaXQgeWwobi5pcHY0LDEpLHI9dm9pZCAwO3JldHVybntpcHY0OmUs'
    'aXB2Njp0P1tdOmF3YWl0IHlsKG4uaXB2NiwyOCl9fWNhdGNoKHQpe3Rocm93'
    'IG5ldyBFcnJvcihgRXJyb3IgcmVzb2x2aW5nIEROUyBmb3IgJHtlfTogJHtI'
    'bCh0KX1gKX19YXN5bmMgZnVuY3Rpb24geWwoZSx0KXt0cnl7Y29uc3Qgcj1h'
    'd2FpdCBmZXRjaChlLHtoZWFkZXJzOnthY2NlcHQ6ImFwcGxpY2F0aW9uL2Ru'
    'cy1qc29uIn19KSxuPWF3YWl0IHIuanNvbigpO3JldHVybiBuLkFuc3dlcj9u'
    'LkFuc3dlci5maWx0ZXIoZT0+ZS50eXBlPT09dCkubWFwKGU9PmUuZGF0YSk6'
    'W119Y2F0Y2godCl7dGhyb3cgbmV3IEVycm9yKGBGYWlsZWQgdG8gZmV0Y2gg'
    'RE5TIHJlY29yZHMgZnJvbSAke2V9OiAke0hsKHQpfWApfX1mdW5jdGlvbiBU'
    'bCgpe2NvbnN0e3NldHRpbmdzOntWTENvbmZpZ3M6ZSxUUkNvbmZpZ3M6dH0s'
    'ZGljdDp7X1ZMXzpyLF9UUl86bn19PWdsb2JhbFRoaXM7cmV0dXJuW10uY29u'
    'Y2F0SWYoZSxyKS5jb25jYXRJZih0LG4pfWFzeW5jIGZ1bmN0aW9uIHhsKGUp'
    'e2NvbnN0e2h0dHBDb25maWc6e2hvc3ROYW1lOnR9LHNldHRpbmdzOntlbmFi'
    'bGVJUHY2OnIsY3VzdG9tQ2RuQWRkcnM6bixjbGVhbklQczppfX09Z2xvYmFs'
    'VGhpcyx7aXB2NDpzLGlwdjY6b309YXdhaXQgZ2wodCwhciksYT12b2lkIDA7'
    'cmV0dXJuW3QsInd3dy5zcGVlZHRlc3QubmV0IiwuLi5zLC4uLm8ubWFwKGU9'
    'PmBbJHtlfV1gKSwuLi5pXS5jb25jYXRJZighZSxuKX1mdW5jdGlvbiB2bChl'
    'LHQscixuLGkscyl7Y29uc3R7c2V0dGluZ3M6e2NsZWFuSVBzOm8sY3VzdG9t'
    'Q2RuQWRkcnM6YSx1cHN0cmVhbVBhcmFtczp7dXBzdHJlYW1TZXJ2ZXI6Y319'
    'LGRpY3Q6e19WTF86dSxfVkxfQ0FQXzpsLF9UUl9DQVBfOmR9fT1nbG9iYWxU'
    'aGlzLHc9dm9pZCAwLGg9YS5pbmNsdWRlcyhyKT8iIEMiOmk/IiBGIjoiIixm'
    'PXM/IvCflJcgIjoiIixBPW49PT11P2w6ZDtsZXQgcDtyZXR1cm4gcD1vLmlu'
    'Y2x1ZGVzKHIpPyJDbGVhbiBJUCI6bWwocik/IkRvbWFpbiI6U2wocik/IklQ'
    'djQiOkNsKHIpPyJJUHY2IjoiIixyPT09Yz9g8J+SpiAke2V9IC0gJHtmfSR7'
    'QX0ke2h9IC0gVXBzdHJlYW0gUHJveHlgOmDwn5KmICR7ZX0gLSAke2Z9JHtB'
    'fSR7aH0gLSAke3B9IDogJHt0fWB9ZnVuY3Rpb24gYmwoZSl7bGV0IHQ9IiI7'
    'Zm9yKGxldCByPTA7cjxlLmxlbmd0aDtyKyspdCs9TWF0aC5yYW5kb20oKTwu'
    'NT9lW3JdLnRvVXBwZXJDYXNlKCk6ZVtyXTtyZXR1cm4gdH1mdW5jdGlvbiBS'
    'bChlLHQpe2xldCByPSIiO2NvbnN0IG49IkFCQ0RFRkdISUpLTE1OT1BRUlNU'
    'VVZXWFlaYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXowMTIzNDU2Nzg5Iixp'
    'PU1hdGguZmxvb3IoTWF0aC5yYW5kb20oKSoodC1lKzEpKStlO2ZvcihsZXQg'
    'ZT0wO2U8aTtlKyspcis9bi5jaGFyQXQoTWF0aC5mbG9vcig2MipNYXRoLnJh'
    'bmRvbSgpKSk7cmV0dXJuIHJ9ZnVuY3Rpb24gTWwoZSl7Y29uc3R7c2V0dGlu'
    'Z3M6e3Byb3h5SVBNb2RlOnQscHJveHlJUHM6cixwcmVmaXhlczpufSxkaWN0'
    'OntfVkxfOml9fT1nbG9iYWxUaGlzLHM9e2p1bms6UmwoOCwxNikscHJvdG9j'
    'b2w6ZT09PWk/InZsIjoidHIiLG1vZGU6dCxwYW5lbElQczoicHJveHlpcCI9'
    'PT10P3I6bn07cmV0dXJuYC8ke2J0b2EoSlNPTi5zdHJpbmdpZnkocykpfWB9'
    'ZnVuY3Rpb24ga2woZSl7Y29uc3QgdD1hdG9iKGUpLHI9dm9pZCAwLG49dm9p'
    'ZCAwO3JldHVybiBBcnJheS5mcm9tKHQpLm1hcChlPT5lLmNoYXJDb2RlQXQo'
    'MCkudG9TdHJpbmcoMTYpLnBhZFN0YXJ0KDIsIjAiKSkuam9pbigiIikubWF0'
    'Y2goLy57Mn0vZykubWFwKGU9PnBhcnNlSW50KGUsMTYpKX1mdW5jdGlvbiBT'
    'bChlKXtjb25zdCB0PXZvaWQgMDtyZXR1cm4vXig/OjI1WzAtNV18MlswLTRd'
    'WzAtOV18WzAxXT9bMC05XVswLTldPylcLig/OjI1WzAtNV18MlswLTRdWzAt'
    'OV18WzAxXT9bMC05XVswLTldPylcLig/OjI1WzAtNV18MlswLTRdWzAtOV18'
    'WzAxXT9bMC05XVswLTldPylcLig/OjI1WzAtNV18MlswLTRdWzAtOV18WzAx'
    'XT9bMC05XVswLTldPykoPzpcLyhbMC05XXxbMS0yXVswLTldfDNbMC0yXSkp'
    'PyQvLnRlc3QoZSl9ZnVuY3Rpb24gQ2woZSl7Y29uc3QgdD12b2lkIDA7cmV0'
    'dXJuL15cWyg/Oig/OlthLWZBLUYwLTldezEsNH06KXs3fVthLWZBLUYwLTld'
    'ezEsNH18KD86W2EtZkEtRjAtOV17MSw0fTopezEsN306fDo6KD86W2EtZkEt'
    'RjAtOV17MSw0fTopezAsN318KD86W2EtZkEtRjAtOV17MSw0fTopezEsNn06'
    'W2EtZkEtRjAtOV17MSw0fXwoPzpbYS1mQS1GMC05XXsxLDR9Oil7MSw1fSg/'
    'OjpbYS1mQS1GMC05XXsxLDR9KXsxLDJ9fCg/OlthLWZBLUYwLTldezEsNH06'
    'KXsxLDR9KD86OlthLWZBLUYwLTldezEsNH0pezEsM318KD86W2EtZkEtRjAt'
    'OV17MSw0fTopezEsM30oPzo6W2EtZkEtRjAtOV17MSw0fSl7MSw0fXwoPzpb'
    'YS1mQS1GMC05XXsxLDR9Oil7MSwyfSg/OjpbYS1mQS1GMC05XXsxLDR9KXsx'
    'LDV9fFthLWZBLUYwLTldezEsNH06KD86OlthLWZBLUYwLTldezEsNH0pezEs'
    'Nn0pXF0oPzpcLygxWzAtMV1bMC05XXwxMlswLThdfFswLTldP1swLTldKSk/'
    'JC8udGVzdChlKX1mdW5jdGlvbiBfbChlKXt0cnl7Y29uc3QgdD12b2lkIDAs'
    'cj1uZXcgVVJMKGUpLmhvc3RuYW1lLG49dm9pZCAwO3JldHVybntob3N0OnIs'
    'aXNIb3N0RG9tYWluOm1sKHIpfX1jYXRjaHtyZXR1cm57aG9zdDoiIixpc0hv'
    'c3REb21haW46ITF9fX1mdW5jdGlvbiBPbChlKXtjb25zdHtodHRwQ29uZmln'
    'Ontob3N0TmFtZTp0fSxzZXR0aW5nczp7Y3VzdG9tQ2RuQWRkcnM6cixjdXN0'
    'b21DZG5Ib3N0Om4sY3VzdG9tQ2RuU25pOml9fT1nbG9iYWxUaGlzLHM9ci5p'
    'bmNsdWRlcyhlKSxvPXZvaWQgMCxhPXZvaWQgMDtyZXR1cm57aG9zdDpzP246'
    'dCxzbmk6cz9pOmJsKHQpLGFsbG93SW5zZWN1cmU6c319ZnVuY3Rpb24gUGwo'
    'ZSx0KXtjb25zdCByPS9eKD86XFsoPzxpcHY2Pi4rPylcXXwoPzxob3N0Plte'
    'Ol0rKSkoOig/PHBvcnQ+XGQrKSk/JC8sbj1lLm1hdGNoKHIpO2lmKCFufHwh'
    'bi5ncm91cHMpcmV0dXJue2hvc3Q6IiIscG9ydDowfTtjb25zdHtpcHY2Omks'
    'aG9zdDpzLHBvcnQ6b309bi5ncm91cHM7bGV0IGE9aT8/cz8/IiI7dCYmaSYm'
    'KGE9YFske2l9XWApO2NvbnN0IGM9dm9pZCAwO3JldHVybntob3N0OmEscG9y'
    'dDpvP051bWJlcihvKTowfX1mdW5jdGlvbiBMbChlKXtjb25zdHtkZWZhdWx0'
    'SHR0cHNQb3J0czp0fT1nbG9iYWxUaGlzLmh0dHBDb25maWc7cmV0dXJuIHQu'
    'aW5jbHVkZXMoZSl9dmFyIElsPWU9PiJkaXJlY3QiPT09ZSxEbD1lPT4iYmxv'
    'Y2siPT09ZTtmdW5jdGlvbiBVbChlKXtjb25zdHtjdXN0b21CeXBhc3NSdWxl'
    'czp0LGN1c3RvbUJ5cGFzc1NhbmN0aW9uUnVsZXM6cixjdXN0b21CbG9ja1J1'
    'bGVzOm59PWdsb2JhbFRoaXMuc2V0dGluZ3M7cmV0dXJue2J5cGFzczp7Z2Vv'
    'c2l0ZXM6ZS5maWx0ZXIoZT0+SWwoZS50eXBlKSkubWFwKGU9PmUuZ2Vvc2l0'
    'ZSksZ2VvaXBzOmUuZmlsdGVyKGU9PklsKGUudHlwZSkmJmUuZ2VvaXApLm1h'
    'cChlPT5lLmdlb2lwKSxkb21haW5zOlsuLi50LmZpbHRlcihtbCksLi4uci5m'
    'aWx0ZXIobWwpXSxpcHM6dC5maWx0ZXIoZT0+IW1sKGUpKX0sYmxvY2s6e2dl'
    'b3NpdGVzOmUuZmlsdGVyKGU9PkRsKGUudHlwZSkpLm1hcChlPT5lLmdlb3Np'
    'dGUpLGdlb2lwczplLmZpbHRlcihlPT5EbChlLnR5cGUpJiZlLmdlb2lwKS5t'
    'YXAoZT0+ZS5nZW9pcCksZG9tYWluczpuLmZpbHRlcihtbCksaXBzOm4uZmls'
    'dGVyKGU9PiFtbChlKSl9fX1mdW5jdGlvbiBObChlKXtjb25zdHtsb2NhbERO'
    'Uzp0LGFudGlTYW5jdGlvbkROUzpyLGN1c3RvbUJ5cGFzc1J1bGVzOm4sY3Vz'
    'dG9tQnlwYXNzU2FuY3Rpb25SdWxlczppLGN1c3RvbUJsb2NrUnVsZXM6c309'
    'Z2xvYmFsVGhpcy5zZXR0aW5ncztyZXR1cm57YnlwYXNzOntsb2NhbEROUzp7'
    'Z2Vvc2l0ZUdlb2lwczplLmZpbHRlcigoe3R5cGU6ZSxnZW9pcDpyLGRuczpu'
    'fSk9PklsKGUpJiZyJiZuPT09dCkubWFwKCh7Z2Vvc2l0ZTplLGdlb2lwOnR9'
    'KT0+KHtnZW9zaXRlOmUsZ2VvaXA6dH0pKSxnZW9zaXRlczplLmZpbHRlcigo'
    'e3R5cGU6ZSxnZW9pcDpyLGRuczpufSk9PklsKGUpJiYhciYmbj09PXQpLm1h'
    'cChlPT5lLmdlb3NpdGUpLGRvbWFpbnM6bi5maWx0ZXIobWwpfSxhbnRpU2Fu'
    'Y3Rpb25ETlM6e2dlb3NpdGVzOmUuZmlsdGVyKGU9PklsKGUudHlwZSkmJmUu'
    'ZG5zPT09cikubWFwKGU9PmUuZ2Vvc2l0ZSksZG9tYWluczppLmZpbHRlciht'
    'bCl9fSxibG9jazp7Z2Vvc2l0ZXM6ZS5maWx0ZXIoZT0+RGwoZS50eXBlKSku'
    'bWFwKGU9PmUuZ2Vvc2l0ZSksZG9tYWluczpzLmZpbHRlcihtbCl9fX1mdW5j'
    'dGlvbiB6bChlLHQpe2lmKGUmJnQpcmV0dXJuIGU9PT10P1N0cmluZyhlKTpg'
    'JHtlfS0ke3R9YH1hc3luYyBmdW5jdGlvbiBYbChlLHQpe2NvbnN0e2h0dHBD'
    'b25maWc6e3BhbmVsVmVyc2lvbjpyfSxzZXR0aW5nczpufT1nbG9iYWxUaGlz'
    'O2xldCBpLHM7dHJ5e3JldHVybiBpPWF3YWl0IHQua3YuZ2V0KCJwcm94eVNl'
    'dHRpbmdzIix7dHlwZToianNvbiJ9KSxzPWF3YWl0IHQua3YuZ2V0KCJ3YXJw'
    'QWNjb3VudHMiLHt0eXBlOiJqc29uIn0pLGl8fChhd2FpdCB0Lmt2LnB1dCgi'
    'cHJveHlTZXR0aW5ncyIsSlNPTi5zdHJpbmdpZnkobikpLGk9biksc3x8KHM9'
    'YXdhaXQgd2wodCkpLHIhPT1pLnBhbmVsVmVyc2lvbiYmKGk9YXdhaXQgRmwo'
    'ZSx0KSkse3NldHRpbmdzOmksd2FycEFjY291bnRzOnN9fWNhdGNoKGUpe3Ro'
    'cm93IGNvbnNvbGUubG9nKGUpLG5ldyBFcnJvcihgQW4gZXJyb3Igb2NjdXJy'
    'ZWQgd2hpbGUgZ2V0dGluZyBLVjogJHtIbChlKX1gKX19YXN5bmMgZnVuY3Rp'
    'b24gRmwoZSx0KXtjb25zdHtzZXR0aW5nczpyLGh0dHBDb25maWc6e3BhbmVs'
    'VmVyc2lvbjpufX09Z2xvYmFsVGhpcyxpPSJQVVQiPT09ZS5tZXRob2Q/YXdh'
    'aXQgZS5qc29uKCk6bnVsbDtsZXQgczt0cnl7cz1hd2FpdCB0Lmt2LmdldCgi'
    'cHJveHlTZXR0aW5ncyIse3R5cGU6Impzb24ifSl9Y2F0Y2goZSl7dGhyb3cg'
    'Y29uc29sZS5sb2coZSksbmV3IEVycm9yKGBBbiBlcnJvciBvY2N1cnJlZCB3'
    'aGlsZSBnZXR0aW5nIGN1cnJlbnQgS1Ygc2V0dGluZ3M6ICR7SGwoZSl9YCl9'
    'Y29uc3Qgbz1hc3luYyhlLHQpPT57Y29uc3Qgbj1pPy5bZV0/P3M/LltlXT8/'
    'cltlXTtyZXR1cm4gdD9hd2FpdCB0KG4pOm59LGE9W1sicmVtb3RlRE5TIl0s'
    'WyJyZW1vdGVEbnNIb3N0IiwicmVtb3RlRE5TIixqbF0sWyJsb2NhbEROUyJd'
    'LFsiYW50aVNhbmN0aW9uRE5TIl0sWyJlbmFibGVJUHY2Il0sWyJmYWtlRE5T'
    'Il0sWyJsb2dMZXZlbCJdLFsiYWxsb3dMQU5Db25uZWN0aW9uIl0sWyJwcm94'
    'eUlQTW9kZSJdLFsicHJveHlJUHMiXSxbInByZWZpeGVzIl0sWyJ1cHN0cmVh'
    'bVByb3h5Il0sWyJ1cHN0cmVhbVBhcmFtcyIsInVwc3RyZWFtUHJveHkiLEps'
    'XSxbIm91dFByb3h5Il0sWyJvdXRQcm94eVBhcmFtcyIsIm91dFByb3h5IixX'
    'bF0sWyJjbGVhbklQcyJdLFsiY3VzdG9tQ2RuQWRkcnMiXSxbImN1c3RvbUNk'
    'bkhvc3QiXSxbImN1c3RvbUNkblNuaSJdLFsiYmVzdFZMVFJJbnRlcnZhbCJd'
    'LFsiVkxDb25maWdzIl0sWyJUUkNvbmZpZ3MiXSxbInBvcnRzIl0sWyJmaW5n'
    'ZXJwcmludCJdLFsiZW5hYmxlVEZPIl0sWyJmcmFnbWVudE1vZGUiXSxbImZy'
    'YWdtZW50TGVuZ3RoTWluIl0sWyJmcmFnbWVudExlbmd0aE1heCJdLFsiZnJh'
    'Z21lbnRJbnRlcnZhbE1pbiJdLFsiZnJhZ21lbnRJbnRlcnZhbE1heCJdLFsi'
    'ZnJhZ21lbnRNYXhTcGxpdE1pbiJdLFsiZnJhZ21lbnRNYXhTcGxpdE1heCJd'
    'LFsiZnJhZ21lbnRQYWNrZXRzIl0sWyJlbmFibGVFQ0giXSxbImVjaFNlcnZl'
    'ck5hbWUiXSxbImJ5cGFzc0lyYW4iXSxbImJ5cGFzc0NoaW5hIl0sWyJieXBh'
    'c3NSdXNzaWEiXSxbImJ5cGFzc09wZW5BaSJdLFsiYnlwYXNzR29vZ2xlQWki'
    'XSxbImJ5cGFzc01pY3Jvc29mdCJdLFsiYnlwYXNzT3JhY2xlIl0sWyJieXBh'
    'c3NEb2NrZXIiXSxbImJ5cGFzc0Fkb2JlIl0sWyJieXBhc3NFcGljR2FtZXMi'
    'XSxbImJ5cGFzc0ludGVsIl0sWyJieXBhc3NBbWQiXSxbImJ5cGFzc052aWRp'
    'YSJdLFsiYnlwYXNzQXN1cyJdLFsiYnlwYXNzSHAiXSxbImJ5cGFzc0xlbm92'
    'byJdLFsiYmxvY2tBZHMiXSxbImJsb2NrUG9ybiJdLFsiYmxvY2tVRFA0NDMi'
    'XSxbImJsb2NrTWFsd2FyZSJdLFsiYmxvY2tQaGlzaGluZyJdLFsiYmxvY2tD'
    'cnlwdG9taW5lcnMiXSxbImN1c3RvbUJ5cGFzc1J1bGVzIl0sWyJjdXN0b21C'
    'bG9ja1J1bGVzIl0sWyJjdXN0b21CeXBhc3NTYW5jdGlvblJ1bGVzIl0sWyJ3'
    'YXJwUmVtb3RlRE5TIl0sWyJ3YXJwRW5kcG9pbnRzIl0sWyJiZXN0V2FycElu'
    'dGVydmFsIl0sWyJ4cmF5VWRwTm9pc2VzIl0sWyJrbm9ja2VyTm9pc2VNb2Rl'
    'Il0sWyJub2lzZUNvdW50TWluIl0sWyJub2lzZUNvdW50TWF4Il0sWyJub2lz'
    'ZVNpemVNaW4iXSxbIm5vaXNlU2l6ZU1heCJdLFsibm9pc2VEZWxheU1pbiJd'
    'LFsibm9pc2VEZWxheU1heCJdLFsiYW1uZXppYU5vaXNlQ291bnQiXSxbImFt'
    'bmV6aWFOb2lzZVNpemVNaW4iXSxbImFtbmV6aWFOb2lzZVNpemVNYXgiXSxb'
    'ImN1c3RvbVN1YnMiXSxbImN1c3RvbUNvbmZpZ3MiXV0sYz1hd2FpdCBQcm9t'
    'aXNlLmFsbChhLm1hcChhc3luYyhbZSx0LHJdKT0+W2UsYXdhaXQgbyh0Pz9l'
    'LHIpXSkpLHU9ey4uLk9iamVjdC5mcm9tRW50cmllcyhjKSxwYW5lbFZlcnNp'
    'b246bn07dHJ5e3JldHVybiBhd2FpdCB0Lmt2LnB1dCgicHJveHlTZXR0aW5n'
    'cyIsSlNPTi5zdHJpbmdpZnkodSkpLHV9Y2F0Y2goZSl7dGhyb3cgY29uc29s'
    'ZS5sb2coZSksbmV3IEVycm9yKGBBbiBlcnJvciBvY2N1cnJlZCB3aGlsZSB1'
    'cGRhdGluZyBLVjogJHtIbChlKX1gKX19YXN5bmMgZnVuY3Rpb24gamwoZSl7'
    'Y29uc3R7aG9zdDp0LGlzSG9zdERvbWFpbjpyfT1fbChlKSxuPXtob3N0OnQs'
    'aXNEb21haW46cixpcHY0OltdLGlwdjY6W119O2lmKHIpe2NvbnN0e2lwdjQ6'
    'ZSxpcHY2OnJ9PWF3YWl0IGdsKHQpO24uaXB2ND1lLG4uaXB2Nj1yfXJldHVy'
    'biBufWZ1bmN0aW9uIFdsKGUpe2lmKCFlKXJldHVybnt9O2NvbnN0e19TU186'
    'dCxfVFJfOnIsX1ZMXzpuLF9WTV86aX09Z2xvYmFsVGhpcy5kaWN0O2xldCBz'
    'PW5ldyBVUkwoZSk7Y29uc3Qgbz1zLnByb3RvY29sLnNsaWNlKDAsLTEpLGE9'
    'InNzIj09PW8/dDpvLnJlcGxhY2UoInNvY2tzNSIsInNvY2tzIik7aWYoYT09'
    'PWkpe2NvbnN0IGU9SlNPTi5wYXJzZShwbChzLmhvc3QpKTtyZXR1cm57cHJv'
    'dG9jb2w6YSx1dWlkOmUuaWQsc2VydmVyOmUuYWRkLHBvcnQ6K2UucG9ydCxh'
    'aWQ6K2UuYWlkLHR5cGU6ZS5uZXQsaGVhZGVyVHlwZTplLnR5cGUsc2Vydmlj'
    'ZU5hbWU6ZS5wYXRoLGF1dGhvcml0eTplLmF1dGhvcml0eSxwYXRoOmUucGF0'
    'aHx8dm9pZCAwLGhvc3Q6ZS5ob3N0fHx2b2lkIDAsc2VjdXJpdHk6ZS50bHMs'
    'c25pOmUuc25pLGZwOmUuZnAsYWxwbjplLmFscG58fHZvaWQgMH19Y29uc3Qg'
    'Yz17cHJvdG9jb2w6YSxzZXJ2ZXI6cy5ob3N0bmFtZSxwb3J0OitzLnBvcnR9'
    'LHU9KGUsdCk9PntpZihlKWZvcihjb25zdFtlLHRdb2Ygcy5zZWFyY2hQYXJh'
    'bXMpY1tlXT10fHx2b2lkIDA7cmV0dXJuey4uLmMsLi4udH19O3N3aXRjaChh'
    'KXtjYXNlIG46cmV0dXJuIHUoITAse3V1aWQ6cy51c2VybmFtZX0pO2Nhc2Ug'
    'cjpyZXR1cm4gdSghMCx7cGFzc3dvcmQ6cy51c2VybmFtZX0pO2Nhc2UgdDpj'
    'b25zdCBlPXBsKHMudXNlcm5hbWUpLFtpLC4uLm9dPWUuc3BsaXQoIjoiKTty'
    'ZXR1cm4gdSghMCx7bWV0aG9kOmkscGFzc3dvcmQ6by5qb2luKCI6Iil9KTtj'
    'YXNlInNvY2tzIjpjYXNlImh0dHAiOmxldCBhLGM7dHJ5e2NvbnN0IGU9cGwo'
    'cy51c2VybmFtZSk7ZS5pbmNsdWRlcygiOiIpJiYoW2EsY109ZS5zcGxpdCgi'
    'OiIpKX1jYXRjaChlKXthPXMudXNlcm5hbWUsYz1zLnBhc3N3b3JkfXJldHVy'
    'biB1KCExLHt1c2VyOmF8fHZvaWQgMCxwYXNzOmN8fHZvaWQgMH0pO2RlZmF1'
    'bHQ6cmV0dXJue319fWZ1bmN0aW9uIEpsKGUpe2xldCB0LHI7cmV0dXJuIGUm'
    'Jih7aG9zdDp0LHBvcnQ6cn09UGwoZSwhMCkpLHt1cHN0cmVhbVNlcnZlcjp0'
    'LHVwc3RyZWFtUG9ydDpyfX1hc3luYyBmdW5jdGlvbiBLbChlLHQpe2NvbnN0'
    'IHI9YXdhaXQgWGwoZSx0KTtnbG9iYWxUaGlzLnNldHRpbmdzPXIuc2V0dGlu'
    'Z3N9ZnVuY3Rpb24gVmwoZSx0KXtjb25zdHtwYXRobmFtZTpyfT1uZXcgVVJM'
    'KGUudXJsKSx7VVVJRDpuLFRSX1BBU1M6aSxGQUxMQkFDSzpzLERPSF9VUkw6'
    'b309dDtnbG9iYWxUaGlzLmdsb2JhbENvbmZpZz17dXNlcklEOm4sVHJQYXNz'
    'OmkscGF0aE5hbWU6ZGVjb2RlVVJJQ29tcG9uZW50KHIpLGZhbGxiYWNrRG9t'
    'YWluOnN8fCJ3d3cuaGNhcHRjaGEuY29tIixkb2hVUkw6b3x8Imh0dHBzOi8v'
    'Y2xvdWRmbGFyZS1kbnMuY29tL2Rucy1xdWVyeSJ9fWZ1bmN0aW9uIFlsKGUp'
    'e2NvbnN0e19wdWJsaWNfcHJveHlfaXBfOnR9PWdsb2JhbFRoaXMuZGljdDtn'
    'bG9iYWxUaGlzLndzQ29uZmlnPXtlbnZQcm94eUlQczplLlBST1hZX0lQLGVu'
    'dlByZWZpeGVzOmUuUFJFRklYLGRlZmF1bHRQcm94eUlQczpbdF0sZGVmYXVs'
    'dFByZWZpeGVzOlsiWzJhMDI6ODk4OjE0Njo2NDo6XSIsIlsyNjAyOmZjNTk6'
    'YjA6NjQ6Ol0iLCJbMjYwMjpmYzU5OjExOjY0OjpdIl19fWZ1bmN0aW9uIFps'
    'KGUsdCl7Y29uc3R7X1ZMX0NBUF86cixfVFJfQ0FQXzpuLF93ZWJzaXRlXzpp'
    'fT1nbG9iYWxUaGlzLmRpY3Qse1VVSUQ6cyxUUl9QQVNTOm8sU1VCX1BBVEg6'
    'YSxrdjpjfT10LHtwYXRobmFtZTp1LG9yaWdpbjpsLHNlYXJjaFBhcmFtczpk'
    'LGhvc3RuYW1lOnd9PW5ldyBVUkwoZS51cmwpO2lmKCFbIi9zZWNyZXRzIiwi'
    'L2Zhdmljb24uaWNvIl0uaW5jbHVkZXMoZGVjb2RlVVJJQ29tcG9uZW50KHUp'
    'KSl7aWYoIXN8fCFvKXRocm93IG5ldyBFcnJvcihgUGxlYXNlIHNldCAke3J9'
    'IFVVSUQgYW5kICR7bn0gcGFzc3dvcmQgZmlyc3QuIFZpc2l0IDxhIGhyZWY9'
    'IiR7bH0vc2VjcmV0cyIgdGFyZ2V0PSJfYmxhbmsiPmhlcmU8L2E+IHRvIGdl'
    'bmVyYXRlIHRoZW0uYCx7Y2F1c2U6ImluaXQifSk7aWYoIUVsKHMpKXRocm93'
    'IG5ldyBFcnJvcihgSW52YWxpZCBVVUlEOiAke3N9YCx7Y2F1c2U6ImluaXQi'
    'fSk7aWYoIm9iamVjdCIhPXR5cGVvZiBjKXRocm93IG5ldyBFcnJvcihgS1Yg'
    'RGF0YXNldCBpcyBub3QgcHJvcGVybHkgc2V0ISBQbGVhc2UgcmVmZXIgdG8g'
    'PGEgaHJlZj0iJHtpfSIgdGFyZ2V0PSJfYmxhbmsiPnR1dG9yaWFsczwvYT4u'
    'YCx7Y2F1c2U6ImluaXQifSl9Z2xvYmFsVGhpcy5odHRwQ29uZmlnPXtwYW5l'
    'bFZlcnNpb246IjQuMi4yIixkZWZhdWx0SHR0cFBvcnRzOls4MCw4MDgwLDIw'
    'NTIsMjA4MiwyMDg2LDIwOTUsODg4MF0sZGVmYXVsdEh0dHBzUG9ydHM6WzQ0'
    'Myw4NDQzLDIwNTMsMjA4MywyMDg3LDIwOTZdLGhvc3ROYW1lOncsY2xpZW50'
    'OmRlY29kZVVSSUNvbXBvbmVudChkLmdldCgiYXBwIik/PyIiKSx1cmxPcmln'
    'aW46bCxzdWJQYXRoOmF8fHN9fUFycmF5LnByb3RvdHlwZS5jb25jYXRJZj1m'
    'dW5jdGlvbihlLHQpe3JldHVybiBlP0FycmF5LmlzQXJyYXkodCk/Wy4uLnRo'
    'aXMsLi4udF06Wy4uLnRoaXMsdF06dGhpc30sT2JqZWN0LnByb3RvdHlwZS5v'
    'bWl0RW1wdHk9ZnVuY3Rpb24oKXtpZigwIT09T2JqZWN0LmtleXModGhpcyku'
    'bGVuZ3RoKXJldHVybiB0aGlzfSxnbG9iYWxUaGlzLmRpY3Q9e19WTF86YXRv'
    'YigiZG14bGMzTT0iKSxfVkxfQ0FQXzphdG9iKCJWa3hGVTFNPSIpLF9WTV86'
    'YXRvYigiZG0xbGMzTT0iKSxfVFJfOmF0b2IoImRISnZhbUZ1IiksX1RSX0NB'
    'UF86YXRvYigiVkhKdmFtRnUiKSxfU1NfOmF0b2IoImMyaGhaRzkzYzI5amEz'
    'TT0iKSxfVjJfOmF0b2IoImRqSnlZWGs9IiksX3Byb2plY3RfOmF0b2IoIlFs'
    'QkMiKSxfd2Vic2l0ZV86YXRvYigiYUhSMGNITTZMeTlpYVdFdGNHRnBiaTFp'
    'WVdOb1pTNW5hWFJvZFdJdWFXOHZRbEJDTFZkdmNtdGxjaTFRWVc1bGJDOD0i'
    'KSxfcHVibGljX3Byb3h5X2lwXzphdG9iKCJZbkJpTG5sdmRYTmxaaTVwYzJW'
    'bllYSnZMbU52YlE9PSIpfSxnbG9iYWxUaGlzLnNldHRpbmdzPXtsb2NhbERO'
    'UzoiOC44LjguOCIsYW50aVNhbmN0aW9uRE5TOiIxNzguMjIuMTIyLjEwMCIs'
    'ZmFrZUROUzohMSxlbmFibGVJUHY2OiEwLGFsbG93TEFOQ29ubmVjdGlvbjoh'
    'MSxsb2dMZXZlbDoid2FybmluZyIscmVtb3RlRE5TOiJodHRwczovLzguOC44'
    'LjgvZG5zLXF1ZXJ5IixyZW1vdGVEbnNIb3N0Ontob3N0OiI4LjguOC44Iixp'
    'c0RvbWFpbjohMSxpcHY0OltdLGlwdjY6W119LHByb3h5SVBNb2RlOiJwcm94'
    'eWlwIixwcm94eUlQczpbXSxwcmVmaXhlczpbXSx1cHN0cmVhbVByb3h5OiIi'
    'LHVwc3RyZWFtUGFyYW1zOnt1cHN0cmVhbVNlcnZlcjp2b2lkIDAsdXBzdHJl'
    'YW1Qb3J0OnZvaWQgMH0sb3V0UHJveHk6IiIsb3V0UHJveHlQYXJhbXM6e30s'
    'Y2xlYW5JUHM6W10sY3VzdG9tQ2RuQWRkcnM6W10sY3VzdG9tQ2RuSG9zdDoi'
    'IixjdXN0b21DZG5Tbmk6IiIsYmVzdFZMVFJJbnRlcnZhbDozMCxWTENvbmZp'
    'Z3M6ITAsVFJDb25maWdzOiEwLHBvcnRzOls0NDNdLGZpbmdlcnByaW50OiJj'
    'aHJvbWUiLGVuYWJsZVRGTzohMSxmcmFnbWVudE1vZGU6ImN1c3RvbSIsZnJh'
    'Z21lbnRMZW5ndGhNaW46MTAwLGZyYWdtZW50TGVuZ3RoTWF4OjIwMCxmcmFn'
    'bWVudEludGVydmFsTWluOjEsZnJhZ21lbnRJbnRlcnZhbE1heDoxLGZyYWdt'
    'ZW50TWF4U3BsaXRNaW46dm9pZCAwLGZyYWdtZW50TWF4U3BsaXRNYXg6dm9p'
    'ZCAwLGZyYWdtZW50UGFja2V0czoidGxzaGVsbG8iLGVuYWJsZUVDSDohMSxl'
    'Y2hTZXJ2ZXJOYW1lOiIiLGJ5cGFzc0lyYW46ITEsYnlwYXNzQ2hpbmE6ITEs'
    'YnlwYXNzUnVzc2lhOiExLGJ5cGFzc09wZW5BaTohMSxieXBhc3NHb29nbGVB'
    'aTohMSxieXBhc3NNaWNyb3NvZnQ6ITEsYnlwYXNzT3JhY2xlOiExLGJ5cGFz'
    'c0RvY2tlcjohMSxieXBhc3NBZG9iZTohMSxieXBhc3NFcGljR2FtZXM6ITEs'
    'YnlwYXNzSW50ZWw6ITEsYnlwYXNzQW1kOiExLGJ5cGFzc052aWRpYTohMSxi'
    'eXBhc3NBc3VzOiExLGJ5cGFzc0hwOiExLGJ5cGFzc0xlbm92bzohMSxibG9j'
    'a0FkczohMSxibG9ja1Bvcm46ITEsYmxvY2tVRFA0NDM6ITEsYmxvY2tNYWx3'
    'YXJlOiExLGJsb2NrUGhpc2hpbmc6ITEsYmxvY2tDcnlwdG9taW5lcnM6ITEs'
    'Y3VzdG9tQnlwYXNzUnVsZXM6W10sY3VzdG9tQmxvY2tSdWxlczpbXSxjdXN0'
    'b21CeXBhc3NTYW5jdGlvblJ1bGVzOltdLHdhcnBSZW1vdGVETlM6IjEuMS4x'
    'LjEiLHdhcnBFbmRwb2ludHM6WyJlbmdhZ2UuY2xvdWRmbGFyZWNsaWVudC5j'
    'b206MjQwOCJdLGJlc3RXYXJwSW50ZXJ2YWw6MzAseHJheVVkcE5vaXNlczpb'
    'e3R5cGU6InJhbmQiLHBhY2tldDoiNTAtMTAwIixkZWxheToiMS0xIixjb3Vu'
    'dDo1fV0sa25vY2tlck5vaXNlTW9kZToicXVpYyIsbm9pc2VDb3VudE1pbjox'
    'MCxub2lzZUNvdW50TWF4OjE1LG5vaXNlU2l6ZU1pbjo1LG5vaXNlU2l6ZU1h'
    'eDoxMCxub2lzZURlbGF5TWluOjEsbm9pc2VEZWxheU1heDoxLGFtbmV6aWFO'
    'b2lzZUNvdW50OjUsYW1uZXppYU5vaXNlU2l6ZU1pbjo1MCxhbW5lemlhTm9p'
    'c2VTaXplTWF4OjEwMCxjdXN0b21TdWJzOltdLGN1c3RvbUNvbmZpZ3M6W10s'
    'cGFuZWxWZXJzaW9uOiI0LjIuMiJ9O3ZhciBHbD1uZXcgVGV4dEVuY29kZXIs'
    'UWw9bmV3IFRleHREZWNvZGVyLHFsPTIqKjMyO2Z1bmN0aW9uICRsKC4uLmUp'
    'e2NvbnN0IHQ9ZS5yZWR1Y2UoKGUse2xlbmd0aDp0fSk9PmUrdCwwKSxyPW5l'
    'dyBVaW50OEFycmF5KHQpO2xldCBuPTA7Zm9yKGNvbnN0IHQgb2YgZSlyLnNl'
    'dCh0LG4pLG4rPXQubGVuZ3RoO3JldHVybiByfWZ1bmN0aW9uIGVkKGUpe2Nv'
    'bnN0IHQ9bmV3IFVpbnQ4QXJyYXkoZS5sZW5ndGgpO2ZvcihsZXQgcj0wO3I8'
    'ZS5sZW5ndGg7cisrKXtjb25zdCBuPWUuY2hhckNvZGVBdChyKTtpZihuPjEy'
    'Nyl0aHJvdyBuZXcgVHlwZUVycm9yKCJub24tQVNDSUkgc3RyaW5nIGVuY291'
    'bnRlcmVkIGluIGVuY29kZSgpIik7dFtyXT1ufXJldHVybiB0fWZ1bmN0aW9u'
    'IHRkKGUpe2lmKFVpbnQ4QXJyYXkucHJvdG90eXBlLnRvQmFzZTY0KXJldHVy'
    'biBlLnRvQmFzZTY0KCk7Y29uc3QgdD0zMjc2OCxyPVtdO2ZvcihsZXQgbj0w'
    'O248ZS5sZW5ndGg7bis9dClyLnB1c2goU3RyaW5nLmZyb21DaGFyQ29kZS5h'
    'cHBseShudWxsLGUuc3ViYXJyYXkobixuK3QpKSk7cmV0dXJuIGJ0b2Eoci5q'
    'b2luKCIiKSl9ZnVuY3Rpb24gcmQoZSl7aWYoVWludDhBcnJheS5mcm9tQmFz'
    'ZTY0KXJldHVybiBVaW50OEFycmF5LmZyb21CYXNlNjQoZSk7Y29uc3QgdD1h'
    'dG9iKGUpLHI9bmV3IFVpbnQ4QXJyYXkodC5sZW5ndGgpO2ZvcihsZXQgZT0w'
    'O2U8dC5sZW5ndGg7ZSsrKXJbZV09dC5jaGFyQ29kZUF0KGUpO3JldHVybiBy'
    'fWZ1bmN0aW9uIG5kKGUpe2lmKFVpbnQ4QXJyYXkuZnJvbUJhc2U2NClyZXR1'
    'cm4gVWludDhBcnJheS5mcm9tQmFzZTY0KCJzdHJpbmciPT10eXBlb2YgZT9l'
    'OlFsLmRlY29kZShlKSx7YWxwaGFiZXQ6ImJhc2U2NHVybCJ9KTtsZXQgdD1l'
    'O3QgaW5zdGFuY2VvZiBVaW50OEFycmF5JiYodD1RbC5kZWNvZGUodCkpLHQ9'
    'dC5yZXBsYWNlKC8tL2csIisiKS5yZXBsYWNlKC9fL2csIi8iKTt0cnl7cmV0'
    'dXJuIHJkKHQpfWNhdGNoe3Rocm93IG5ldyBUeXBlRXJyb3IoIlRoZSBpbnB1'
    'dCB0byBiZSBkZWNvZGVkIGlzIG5vdCBjb3JyZWN0bHkgZW5jb2RlZC4iKX19'
    'ZnVuY3Rpb24gaWQoZSl7bGV0IHQ9ZTtyZXR1cm4ic3RyaW5nIj09dHlwZW9m'
    'IHQmJih0PUdsLmVuY29kZSh0KSksVWludDhBcnJheS5wcm90b3R5cGUudG9C'
    'YXNlNjQ/dC50b0Jhc2U2NCh7YWxwaGFiZXQ6ImJhc2U2NHVybCIsb21pdFBh'
    'ZGRpbmc6ITB9KTp0ZCh0KS5yZXBsYWNlKC89L2csIiIpLnJlcGxhY2UoL1wr'
    'L2csIi0iKS5yZXBsYWNlKC9cLy9nLCJfIil9dmFyIHNkPShlLHQ9ImFsZ29y'
    'aXRobS5uYW1lIik9Pm5ldyBUeXBlRXJyb3IoYENyeXB0b0tleSBkb2VzIG5v'
    'dCBzdXBwb3J0IHRoaXMgb3BlcmF0aW9uLCBpdHMgJHt0fSBtdXN0IGJlICR7'
    'ZX1gKSxvZD0oZSx0KT0+ZS5uYW1lPT09dDtmdW5jdGlvbiBhZChlKXtyZXR1'
    'cm4gcGFyc2VJbnQoZS5uYW1lLnNsaWNlKDQpLDEwKX1mdW5jdGlvbiBjZChl'
    'LHQpe2NvbnN0IHI9dm9pZCAwO2lmKGFkKGUuaGFzaCkhPT10KXRocm93IHNk'
    'KGBTSEEtJHt0fWAsImFsZ29yaXRobS5oYXNoIil9ZnVuY3Rpb24gdWQoZSl7'
    'c3dpdGNoKGUpe2Nhc2UiRVMyNTYiOnJldHVybiJQLTI1NiI7Y2FzZSJFUzM4'
    'NCI6cmV0dXJuIlAtMzg0IjtjYXNlIkVTNTEyIjpyZXR1cm4iUC01MjEiO2Rl'
    'ZmF1bHQ6dGhyb3cgbmV3IEVycm9yKCJ1bnJlYWNoYWJsZSIpfX1mdW5jdGlv'
    'biBsZChlLHQpe2lmKHQmJiFlLnVzYWdlcy5pbmNsdWRlcyh0KSl0aHJvdyBu'
    'ZXcgVHlwZUVycm9yKGBDcnlwdG9LZXkgZG9lcyBub3Qgc3VwcG9ydCB0aGlz'
    'IG9wZXJhdGlvbiwgaXRzIHVzYWdlcyBtdXN0IGluY2x1ZGUgJHt0fS5gKX1m'
    'dW5jdGlvbiBkZChlLHQscil7c3dpdGNoKHQpe2Nhc2UiSFMyNTYiOmNhc2Ui'
    'SFMzODQiOmNhc2UiSFM1MTIiOmlmKCFvZChlLmFsZ29yaXRobSwiSE1BQyIp'
    'KXRocm93IHNkKCJITUFDIik7Y2QoZS5hbGdvcml0aG0scGFyc2VJbnQodC5z'
    'bGljZSgyKSwxMCkpO2JyZWFrO2Nhc2UiUlMyNTYiOmNhc2UiUlMzODQiOmNh'
    'c2UiUlM1MTIiOmlmKCFvZChlLmFsZ29yaXRobSwiUlNBU1NBLVBLQ1MxLXYx'
    'XzUiKSl0aHJvdyBzZCgiUlNBU1NBLVBLQ1MxLXYxXzUiKTtjZChlLmFsZ29y'
    'aXRobSxwYXJzZUludCh0LnNsaWNlKDIpLDEwKSk7YnJlYWs7Y2FzZSJQUzI1'
    'NiI6Y2FzZSJQUzM4NCI6Y2FzZSJQUzUxMiI6aWYoIW9kKGUuYWxnb3JpdGht'
    'LCJSU0EtUFNTIikpdGhyb3cgc2QoIlJTQS1QU1MiKTtjZChlLmFsZ29yaXRo'
    'bSxwYXJzZUludCh0LnNsaWNlKDIpLDEwKSk7YnJlYWs7Y2FzZSJFZDI1NTE5'
    'IjpjYXNlIkVkRFNBIjppZighb2QoZS5hbGdvcml0aG0sIkVkMjU1MTkiKSl0'
    'aHJvdyBzZCgiRWQyNTUxOSIpO2JyZWFrO2Nhc2UiTUwtRFNBLTQ0IjpjYXNl'
    'Ik1MLURTQS02NSI6Y2FzZSJNTC1EU0EtODciOmlmKCFvZChlLmFsZ29yaXRo'
    'bSx0KSl0aHJvdyBzZCh0KTticmVhaztjYXNlIkVTMjU2IjpjYXNlIkVTMzg0'
    'IjpjYXNlIkVTNTEyIjp7aWYoIW9kKGUuYWxnb3JpdGhtLCJFQ0RTQSIpKXRo'
    'cm93IHNkKCJFQ0RTQSIpO2NvbnN0IHI9dWQodCksbj12b2lkIDA7aWYoZS5h'
    'bGdvcml0aG0ubmFtZWRDdXJ2ZSE9PXIpdGhyb3cgc2QociwiYWxnb3JpdGht'
    'Lm5hbWVkQ3VydmUiKTticmVha31kZWZhdWx0OnRocm93IG5ldyBUeXBlRXJy'
    'b3IoIkNyeXB0b0tleSBkb2VzIG5vdCBzdXBwb3J0IHRoaXMgb3BlcmF0aW9u'
    'Iil9bGQoZSxyKX1mdW5jdGlvbiB3ZChlLHQsLi4ucil7aWYoKHI9ci5maWx0'
    'ZXIoQm9vbGVhbikpLmxlbmd0aD4yKXtjb25zdCB0PXIucG9wKCk7ZSs9YG9u'
    'ZSBvZiB0eXBlICR7ci5qb2luKCIsICIpfSwgb3IgJHt0fS5gfWVsc2UgMj09'
    'PXIubGVuZ3RoP2UrPWBvbmUgb2YgdHlwZSAke3JbMF19IG9yICR7clsxXX0u'
    'YDplKz1gb2YgdHlwZSAke3JbMF19LmA7cmV0dXJuIG51bGw9PXQ/ZSs9YCBS'
    'ZWNlaXZlZCAke3R9YDoiZnVuY3Rpb24iPT10eXBlb2YgdCYmdC5uYW1lP2Ur'
    'PWAgUmVjZWl2ZWQgZnVuY3Rpb24gJHt0Lm5hbWV9YDoib2JqZWN0Ij09dHlw'
    'ZW9mIHQmJm51bGwhPXQmJnQuY29uc3RydWN0b3I/Lm5hbWUmJihlKz1gIFJl'
    'Y2VpdmVkIGFuIGluc3RhbmNlIG9mICR7dC5jb25zdHJ1Y3Rvci5uYW1lfWAp'
    'LGV9dmFyIGhkPShlLC4uLnQpPT53ZCgiS2V5IG11c3QgYmUgIixlLC4uLnQp'
    'LGZkPShlLHQsLi4ucik9PndkKGBLZXkgZm9yIHRoZSAke2V9IGFsZ29yaXRo'
    'bSBtdXN0IGJlIGAsdCwuLi5yKSxBZD1jbGFzcyBleHRlbmRzIEVycm9ye3N0'
    'YXRpYyBjb2RlPSJFUlJfSk9TRV9HRU5FUklDIjtjb2RlPSJFUlJfSk9TRV9H'
    'RU5FUklDIjtjb25zdHJ1Y3RvcihlLHQpe3N1cGVyKGUsdCksdGhpcy5uYW1l'
    'PXRoaXMuY29uc3RydWN0b3IubmFtZSxFcnJvci5jYXB0dXJlU3RhY2tUcmFj'
    'ZT8uKHRoaXMsdGhpcy5jb25zdHJ1Y3Rvcil9fSxwZD1jbGFzcyBleHRlbmRz'
    'IEFke3N0YXRpYyBjb2RlPSJFUlJfSldUX0NMQUlNX1ZBTElEQVRJT05fRkFJ'
    'TEVEIjtjb2RlPSJFUlJfSldUX0NMQUlNX1ZBTElEQVRJT05fRkFJTEVEIjtj'
    'bGFpbTtyZWFzb247cGF5bG9hZDtjb25zdHJ1Y3RvcihlLHQscj0idW5zcGVj'
    'aWZpZWQiLG49InVuc3BlY2lmaWVkIil7c3VwZXIoZSx7Y2F1c2U6e2NsYWlt'
    'OnIscmVhc29uOm4scGF5bG9hZDp0fX0pLHRoaXMuY2xhaW09cix0aGlzLnJl'
    'YXNvbj1uLHRoaXMucGF5bG9hZD10fX0sRWQ9Y2xhc3MgZXh0ZW5kcyBBZHtz'
    'dGF0aWMgY29kZT0iRVJSX0pXVF9FWFBJUkVEIjtjb2RlPSJFUlJfSldUX0VY'
    'UElSRUQiO2NsYWltO3JlYXNvbjtwYXlsb2FkO2NvbnN0cnVjdG9yKGUsdCxy'
    'PSJ1bnNwZWNpZmllZCIsbj0idW5zcGVjaWZpZWQiKXtzdXBlcihlLHtjYXVz'
    'ZTp7Y2xhaW06cixyZWFzb246bixwYXlsb2FkOnR9fSksdGhpcy5jbGFpbT1y'
    'LHRoaXMucmVhc29uPW4sdGhpcy5wYXlsb2FkPXR9fSxCZD1jbGFzcyBleHRl'
    'bmRzIEFke3N0YXRpYyBjb2RlPSJFUlJfSk9TRV9BTEdfTk9UX0FMTE9XRUQi'
    'O2NvZGU9IkVSUl9KT1NFX0FMR19OT1RfQUxMT1dFRCJ9LEhkPWNsYXNzIGV4'
    'dGVuZHMgQWR7c3RhdGljIGNvZGU9IkVSUl9KT1NFX05PVF9TVVBQT1JURUQi'
    'O2NvZGU9IkVSUl9KT1NFX05PVF9TVVBQT1JURUQifSxtZD1jbGFzcyBleHRl'
    'bmRzIEFke3N0YXRpYyBjb2RlPSJFUlJfSldTX0lOVkFMSUQiO2NvZGU9IkVS'
    'Ul9KV1NfSU5WQUxJRCJ9LGdkPWNsYXNzIGV4dGVuZHMgQWR7c3RhdGljIGNv'
    'ZGU9IkVSUl9KV1RfSU5WQUxJRCI7Y29kZT0iRVJSX0pXVF9JTlZBTElEIn0s'
    'eWQ9Y2xhc3MgZXh0ZW5kcyBBZHtzdGF0aWMgY29kZT0iRVJSX0pXU19TSUdO'
    'QVRVUkVfVkVSSUZJQ0FUSU9OX0ZBSUxFRCI7Y29kZT0iRVJSX0pXU19TSUdO'
    'QVRVUkVfVkVSSUZJQ0FUSU9OX0ZBSUxFRCI7Y29uc3RydWN0b3IoZT0ic2ln'
    'bmF0dXJlIHZlcmlmaWNhdGlvbiBmYWlsZWQiLHQpe3N1cGVyKGUsdCl9fSxU'
    'ZD1lPT57aWYoIkNyeXB0b0tleSI9PT1lPy5bU3ltYm9sLnRvU3RyaW5nVGFn'
    'XSlyZXR1cm4hMDt0cnl7cmV0dXJuIGUgaW5zdGFuY2VvZiBDcnlwdG9LZXl9'
    'Y2F0Y2h7cmV0dXJuITF9fSx4ZD1lPT4iS2V5T2JqZWN0Ij09PWU/LltTeW1i'
    'b2wudG9TdHJpbmdUYWddLHZkPWU9PlRkKGUpfHx4ZChlKTtmdW5jdGlvbiBi'
    'ZChlLHQpe2lmKGUpdGhyb3cgbmV3IFR5cGVFcnJvcihgJHt0fSBjYW4gb25s'
    'eSBiZSBjYWxsZWQgb25jZWApfWZ1bmN0aW9uIFJkKGUsdCxyKXt0cnl7cmV0'
    'dXJuIG5kKGUpfWNhdGNoe3Rocm93IG5ldyByKGBGYWlsZWQgdG8gYmFzZTY0'
    'dXJsIGRlY29kZSB0aGUgJHt0fWApfX12YXIgTWQ9ZT0+Im9iamVjdCI9PXR5'
    'cGVvZiBlJiZudWxsIT09ZTtmdW5jdGlvbiBrZChlKXtpZighTWQoZSl8fCJb'
    'b2JqZWN0IE9iamVjdF0iIT09T2JqZWN0LnByb3RvdHlwZS50b1N0cmluZy5j'
    'YWxsKGUpKXJldHVybiExO2lmKG51bGw9PT1PYmplY3QuZ2V0UHJvdG90eXBl'
    'T2YoZSkpcmV0dXJuITA7bGV0IHQ9ZTtmb3IoO251bGwhPT1PYmplY3QuZ2V0'
    'UHJvdG90eXBlT2YodCk7KXQ9T2JqZWN0LmdldFByb3RvdHlwZU9mKHQpO3Jl'
    'dHVybiBPYmplY3QuZ2V0UHJvdG90eXBlT2YoZSk9PT10fWZ1bmN0aW9uIFNk'
    'KC4uLmUpe2NvbnN0IHQ9ZS5maWx0ZXIoQm9vbGVhbik7aWYoMD09PXQubGVu'
    'Z3RofHwxPT09dC5sZW5ndGgpcmV0dXJuITA7bGV0IHI7Zm9yKGNvbnN0IGUg'
    'b2YgdCl7Y29uc3QgdD1PYmplY3Qua2V5cyhlKTtpZihyJiYwIT09ci5zaXpl'
    'KWZvcihjb25zdCBlIG9mIHQpe2lmKHIuaGFzKGUpKXJldHVybiExO3IuYWRk'
    'KGUpfWVsc2Ugcj1uZXcgU2V0KHQpfXJldHVybiEwfXZhciBDZD1lPT5rZChl'
    'KSYmInN0cmluZyI9PXR5cGVvZiBlLmt0eSxfZD1lPT4ib2N0IiE9PWUua3R5'
    'JiYoIkFLUCI9PT1lLmt0eSYmInN0cmluZyI9PXR5cGVvZiBlLnByaXZ8fCJz'
    'dHJpbmciPT10eXBlb2YgZS5kKSxPZD1lPT4ib2N0IiE9PWUua3R5JiZ2b2lk'
    'IDA9PT1lLmQmJnZvaWQgMD09PWUucHJpdixQZD1lPT4ib2N0Ij09PWUua3R5'
    'JiYic3RyaW5nIj09dHlwZW9mIGUuaztmdW5jdGlvbiBMZChlLHQpe2lmKGUu'
    'c3RhcnRzV2l0aCgiUlMiKXx8ZS5zdGFydHNXaXRoKCJQUyIpKXtjb25zdHtt'
    'b2R1bHVzTGVuZ3RoOnJ9PXQuYWxnb3JpdGhtO2lmKCJudW1iZXIiIT10eXBl'
    'b2Ygcnx8cjwyMDQ4KXRocm93IG5ldyBUeXBlRXJyb3IoYCR7ZX0gcmVxdWly'
    'ZXMga2V5IG1vZHVsdXNMZW5ndGggdG8gYmUgMjA0OCBiaXRzIG9yIGxhcmdl'
    'cmApfX1mdW5jdGlvbiBJZChlLHQpe2NvbnN0IHI9YFNIQS0ke2Uuc2xpY2Uo'
    'LTMpfWA7c3dpdGNoKGUpe2Nhc2UiSFMyNTYiOmNhc2UiSFMzODQiOmNhc2Ui'
    'SFM1MTIiOnJldHVybntoYXNoOnIsbmFtZToiSE1BQyJ9O2Nhc2UiUFMyNTYi'
    'OmNhc2UiUFMzODQiOmNhc2UiUFM1MTIiOnJldHVybntoYXNoOnIsbmFtZToi'
    'UlNBLVBTUyIsc2FsdExlbmd0aDpwYXJzZUludChlLnNsaWNlKC0zKSwxMCk+'
    'PjN9O2Nhc2UiUlMyNTYiOmNhc2UiUlMzODQiOmNhc2UiUlM1MTIiOnJldHVy'
    'bntoYXNoOnIsbmFtZToiUlNBU1NBLVBLQ1MxLXYxXzUifTtjYXNlIkVTMjU2'
    'IjpjYXNlIkVTMzg0IjpjYXNlIkVTNTEyIjpyZXR1cm57aGFzaDpyLG5hbWU6'
    'IkVDRFNBIixuYW1lZEN1cnZlOnQubmFtZWRDdXJ2ZX07Y2FzZSJFZDI1NTE5'
    'IjpjYXNlIkVkRFNBIjpyZXR1cm57bmFtZToiRWQyNTUxOSJ9O2Nhc2UiTUwt'
    'RFNBLTQ0IjpjYXNlIk1MLURTQS02NSI6Y2FzZSJNTC1EU0EtODciOnJldHVy'
    'bntuYW1lOmV9O2RlZmF1bHQ6dGhyb3cgbmV3IEhkKGBhbGcgJHtlfSBpcyBu'
    'b3Qgc3VwcG9ydGVkIGVpdGhlciBieSBKT1NFIG9yIHlvdXIgamF2YXNjcmlw'
    'dCBydW50aW1lYCl9fWFzeW5jIGZ1bmN0aW9uIERkKGUsdCxyKXtpZih0IGlu'
    'c3RhbmNlb2YgVWludDhBcnJheSl7aWYoIWUuc3RhcnRzV2l0aCgiSFMiKSl0'
    'aHJvdyBuZXcgVHlwZUVycm9yKGhkKHQsIkNyeXB0b0tleSIsIktleU9iamVj'
    'dCIsIkpTT04gV2ViIEtleSIpKTtyZXR1cm4gY3J5cHRvLnN1YnRsZS5pbXBv'
    'cnRLZXkoInJhdyIsdCx7aGFzaDpgU0hBLSR7ZS5zbGljZSgtMyl9YCxuYW1l'
    'OiJITUFDIn0sITEsW3JdKX1yZXR1cm4gZGQodCxlLHIpLHR9YXN5bmMgZnVu'
    'Y3Rpb24gVWQoZSx0LHIpe2NvbnN0IG49YXdhaXQgRGQoZSx0LCJzaWduIik7'
    'TGQoZSxuKTtjb25zdCBpPWF3YWl0IGNyeXB0by5zdWJ0bGUuc2lnbihJZChl'
    'LG4uYWxnb3JpdGhtKSxuLHIpO3JldHVybiBuZXcgVWludDhBcnJheShpKX1h'
    'c3luYyBmdW5jdGlvbiBOZChlLHQscixuKXtjb25zdCBpPWF3YWl0IERkKGUs'
    'dCwidmVyaWZ5Iik7TGQoZSxpKTtjb25zdCBzPUlkKGUsaS5hbGdvcml0aG0p'
    'O3RyeXtyZXR1cm4gYXdhaXQgY3J5cHRvLnN1YnRsZS52ZXJpZnkocyxpLHIs'
    'bil9Y2F0Y2h7cmV0dXJuITF9fXZhciB6ZD0nSW52YWxpZCBvciB1bnN1cHBv'
    'cnRlZCBKV0sgImFsZyIgKEFsZ29yaXRobSkgUGFyYW1ldGVyIHZhbHVlJztm'
    'dW5jdGlvbiBYZChlKXtsZXQgdCxyO3N3aXRjaChlLmt0eSl7Y2FzZSJBS1Ai'
    'OnN3aXRjaChlLmFsZyl7Y2FzZSJNTC1EU0EtNDQiOmNhc2UiTUwtRFNBLTY1'
    'IjpjYXNlIk1MLURTQS04NyI6dD17bmFtZTplLmFsZ30scj1lLnByaXY/WyJz'
    'aWduIl06WyJ2ZXJpZnkiXTticmVhaztkZWZhdWx0OnRocm93IG5ldyBIZCh6'
    'ZCl9YnJlYWs7Y2FzZSJSU0EiOnN3aXRjaChlLmFsZyl7Y2FzZSJQUzI1NiI6'
    'Y2FzZSJQUzM4NCI6Y2FzZSJQUzUxMiI6dD17bmFtZToiUlNBLVBTUyIsaGFz'
    'aDpgU0hBLSR7ZS5hbGcuc2xpY2UoLTMpfWB9LHI9ZS5kP1sic2lnbiJdOlsi'
    'dmVyaWZ5Il07YnJlYWs7Y2FzZSJSUzI1NiI6Y2FzZSJSUzM4NCI6Y2FzZSJS'
    'UzUxMiI6dD17bmFtZToiUlNBU1NBLVBLQ1MxLXYxXzUiLGhhc2g6YFNIQS0k'
    'e2UuYWxnLnNsaWNlKC0zKX1gfSxyPWUuZD9bInNpZ24iXTpbInZlcmlmeSJd'
    'O2JyZWFrO2Nhc2UiUlNBLU9BRVAiOmNhc2UiUlNBLU9BRVAtMjU2IjpjYXNl'
    'IlJTQS1PQUVQLTM4NCI6Y2FzZSJSU0EtT0FFUC01MTIiOnQ9e25hbWU6IlJT'
    'QS1PQUVQIixoYXNoOmBTSEEtJHtwYXJzZUludChlLmFsZy5zbGljZSgtMyks'
    'MTApfHwxfWB9LHI9ZS5kP1siZGVjcnlwdCIsInVud3JhcEtleSJdOlsiZW5j'
    'cnlwdCIsIndyYXBLZXkiXTticmVhaztkZWZhdWx0OnRocm93IG5ldyBIZCh6'
    'ZCl9YnJlYWs7Y2FzZSJFQyI6c3dpdGNoKGUuYWxnKXtjYXNlIkVTMjU2Ijpj'
    'YXNlIkVTMzg0IjpjYXNlIkVTNTEyIjp0PXtuYW1lOiJFQ0RTQSIsbmFtZWRD'
    'dXJ2ZTp7RVMyNTY6IlAtMjU2IixFUzM4NDoiUC0zODQiLEVTNTEyOiJQLTUy'
    'MSJ9W2UuYWxnXX0scj1lLmQ/WyJzaWduIl06WyJ2ZXJpZnkiXTticmVhaztj'
    'YXNlIkVDREgtRVMiOmNhc2UiRUNESC1FUytBMTI4S1ciOmNhc2UiRUNESC1F'
    'UytBMTkyS1ciOmNhc2UiRUNESC1FUytBMjU2S1ciOnQ9e25hbWU6IkVDREgi'
    'LG5hbWVkQ3VydmU6ZS5jcnZ9LHI9ZS5kP1siZGVyaXZlQml0cyJdOltdO2Jy'
    'ZWFrO2RlZmF1bHQ6dGhyb3cgbmV3IEhkKHpkKX1icmVhaztjYXNlIk9LUCI6'
    'c3dpdGNoKGUuYWxnKXtjYXNlIkVkMjU1MTkiOmNhc2UiRWREU0EiOnQ9e25h'
    'bWU6IkVkMjU1MTkifSxyPWUuZD9bInNpZ24iXTpbInZlcmlmeSJdO2JyZWFr'
    'O2Nhc2UiRUNESC1FUyI6Y2FzZSJFQ0RILUVTK0ExMjhLVyI6Y2FzZSJFQ0RI'
    'LUVTK0ExOTJLVyI6Y2FzZSJFQ0RILUVTK0EyNTZLVyI6dD17bmFtZTplLmNy'
    'dn0scj1lLmQ/WyJkZXJpdmVCaXRzIl06W107YnJlYWs7ZGVmYXVsdDp0aHJv'
    'dyBuZXcgSGQoemQpfWJyZWFrO2RlZmF1bHQ6dGhyb3cgbmV3IEhkKCdJbnZh'
    'bGlkIG9yIHVuc3VwcG9ydGVkIEpXSyAia3R5IiAoS2V5IFR5cGUpIFBhcmFt'
    'ZXRlciB2YWx1ZScpfXJldHVybnthbGdvcml0aG06dCxrZXlVc2FnZXM6cn19'
    'YXN5bmMgZnVuY3Rpb24gRmQoZSl7aWYoIWUuYWxnKXRocm93IG5ldyBUeXBl'
    'RXJyb3IoJyJhbGciIGFyZ3VtZW50IGlzIHJlcXVpcmVkIHdoZW4gImp3ay5h'
    'bGciIGlzIG5vdCBwcmVzZW50Jyk7Y29uc3R7YWxnb3JpdGhtOnQsa2V5VXNh'
    'Z2VzOnJ9PVhkKGUpLG49ey4uLmV9O3JldHVybiJBS1AiIT09bi5rdHkmJmRl'
    'bGV0ZSBuLmFsZyxkZWxldGUgbi51c2UsY3J5cHRvLnN1YnRsZS5pbXBvcnRL'
    'ZXkoImp3ayIsbix0LGUuZXh0Pz8oIWUuZCYmIWUucHJpdiksZS5rZXlfb3Bz'
    'Pz9yKX12YXIgamQ9ImdpdmVuIEtleU9iamVjdCBpbnN0YW5jZSBjYW5ub3Qg'
    'YmUgdXNlZCBmb3IgdGhpcyBhbGdvcml0aG0iLFdkLEpkPWFzeW5jKGUsdCxy'
    'LG49ITEpPT57V2R8fD1uZXcgV2Vha01hcDtsZXQgaT1XZC5nZXQoZSk7aWYo'
    'aT8uW3JdKXJldHVybiBpW3JdO2NvbnN0IHM9YXdhaXQgRmQoey4uLnQsYWxn'
    'OnJ9KTtyZXR1cm4gbiYmT2JqZWN0LmZyZWV6ZShlKSxpP2lbcl09czpXZC5z'
    'ZXQoZSx7W3JdOnN9KSxzfSxLZD0oZSx0KT0+e1dkfHw9bmV3IFdlYWtNYXA7'
    'bGV0IHI9V2QuZ2V0KGUpO2lmKHI/Llt0XSlyZXR1cm4gclt0XTtjb25zdCBu'
    'PSJwdWJsaWMiPT09ZS50eXBlLGk9ISFuO2xldCBzO2lmKCJ4MjU1MTkiPT09'
    'ZS5hc3ltbWV0cmljS2V5VHlwZSl7c3dpdGNoKHQpe2Nhc2UiRUNESC1FUyI6'
    'Y2FzZSJFQ0RILUVTK0ExMjhLVyI6Y2FzZSJFQ0RILUVTK0ExOTJLVyI6Y2Fz'
    'ZSJFQ0RILUVTK0EyNTZLVyI6YnJlYWs7ZGVmYXVsdDp0aHJvdyBuZXcgVHlw'
    'ZUVycm9yKGpkKX1zPWUudG9DcnlwdG9LZXkoZS5hc3ltbWV0cmljS2V5VHlw'
    'ZSxpLG4/W106WyJkZXJpdmVCaXRzIl0pfWlmKCJlZDI1NTE5Ij09PWUuYXN5'
    'bW1ldHJpY0tleVR5cGUpe2lmKCJFZERTQSIhPT10JiYiRWQyNTUxOSIhPT10'
    'KXRocm93IG5ldyBUeXBlRXJyb3IoamQpO3M9ZS50b0NyeXB0b0tleShlLmFz'
    'eW1tZXRyaWNLZXlUeXBlLGksW24/InZlcmlmeSI6InNpZ24iXSl9c3dpdGNo'
    'KGUuYXN5bW1ldHJpY0tleVR5cGUpe2Nhc2UibWwtZHNhLTQ0IjpjYXNlIm1s'
    'LWRzYS02NSI6Y2FzZSJtbC1kc2EtODciOmlmKHQhPT1lLmFzeW1tZXRyaWNL'
    'ZXlUeXBlLnRvVXBwZXJDYXNlKCkpdGhyb3cgbmV3IFR5cGVFcnJvcihqZCk7'
    'cz1lLnRvQ3J5cHRvS2V5KGUuYXN5bW1ldHJpY0tleVR5cGUsaSxbbj8idmVy'
    'aWZ5Ijoic2lnbiJdKX1pZigicnNhIj09PWUuYXN5bW1ldHJpY0tleVR5cGUp'
    'e2xldCByO3N3aXRjaCh0KXtjYXNlIlJTQS1PQUVQIjpyPSJTSEEtMSI7YnJl'
    'YWs7Y2FzZSJSUzI1NiI6Y2FzZSJQUzI1NiI6Y2FzZSJSU0EtT0FFUC0yNTYi'
    'OnI9IlNIQS0yNTYiO2JyZWFrO2Nhc2UiUlMzODQiOmNhc2UiUFMzODQiOmNh'
    'c2UiUlNBLU9BRVAtMzg0IjpyPSJTSEEtMzg0IjticmVhaztjYXNlIlJTNTEy'
    'IjpjYXNlIlBTNTEyIjpjYXNlIlJTQS1PQUVQLTUxMiI6cj0iU0hBLTUxMiI7'
    'YnJlYWs7ZGVmYXVsdDp0aHJvdyBuZXcgVHlwZUVycm9yKGpkKX1pZih0LnN0'
    'YXJ0c1dpdGgoIlJTQS1PQUVQIikpcmV0dXJuIGUudG9DcnlwdG9LZXkoe25h'
    'bWU6IlJTQS1PQUVQIixoYXNoOnJ9LGksbj9bImVuY3J5cHQiXTpbImRlY3J5'
    'cHQiXSk7cz1lLnRvQ3J5cHRvS2V5KHtuYW1lOnQuc3RhcnRzV2l0aCgiUFMi'
    'KT8iUlNBLVBTUyI6IlJTQVNTQS1QS0NTMS12MV81IixoYXNoOnJ9LGksW24/'
    'InZlcmlmeSI6InNpZ24iXSl9aWYoImVjIj09PWUuYXN5bW1ldHJpY0tleVR5'
    'cGUpe2NvbnN0IHI9dm9pZCAwLG89bmV3IE1hcChbWyJwcmltZTI1NnYxIiwi'
    'UC0yNTYiXSxbInNlY3AzODRyMSIsIlAtMzg0Il0sWyJzZWNwNTIxcjEiLCJQ'
    'LTUyMSJdXSkuZ2V0KGUuYXN5bW1ldHJpY0tleURldGFpbHM/Lm5hbWVkQ3Vy'
    'dmUpO2lmKCFvKXRocm93IG5ldyBUeXBlRXJyb3IoamQpO2NvbnN0IGE9e0VT'
    'MjU2OiJQLTI1NiIsRVMzODQ6IlAtMzg0IixFUzUxMjoiUC01MjEifTthW3Rd'
    'JiZvPT09YVt0XSYmKHM9ZS50b0NyeXB0b0tleSh7bmFtZToiRUNEU0EiLG5h'
    'bWVkQ3VydmU6b30saSxbbj8idmVyaWZ5Ijoic2lnbiJdKSksdC5zdGFydHNX'
    'aXRoKCJFQ0RILUVTIikmJihzPWUudG9DcnlwdG9LZXkoe25hbWU6IkVDREgi'
    'LG5hbWVkQ3VydmU6b30saSxuP1tdOlsiZGVyaXZlQml0cyJdKSl9aWYoIXMp'
    'dGhyb3cgbmV3IFR5cGVFcnJvcihqZCk7cmV0dXJuIHI/clt0XT1zOldkLnNl'
    'dChlLHtbdF06c30pLHN9O2FzeW5jIGZ1bmN0aW9uIFZkKGUsdCl7aWYoZSBp'
    'bnN0YW5jZW9mIFVpbnQ4QXJyYXkpcmV0dXJuIGU7aWYoVGQoZSkpcmV0dXJu'
    'IGU7aWYoeGQoZSkpe2lmKCJzZWNyZXQiPT09ZS50eXBlKXJldHVybiBlLmV4'
    'cG9ydCgpO2lmKCJ0b0NyeXB0b0tleSJpbiBlJiYiZnVuY3Rpb24iPT10eXBl'
    'b2YgZS50b0NyeXB0b0tleSl0cnl7cmV0dXJuIEtkKGUsdCl9Y2F0Y2goZSl7'
    'aWYoZSBpbnN0YW5jZW9mIFR5cGVFcnJvcil0aHJvdyBlfWxldCByPWUuZXhw'
    'b3J0KHtmb3JtYXQ6Imp3ayJ9KTtyZXR1cm4gSmQoZSxyLHQpfWlmKENkKGUp'
    'KXJldHVybiBlLms/bmQoZS5rKTpKZChlLGUsdCwhMCk7dGhyb3cgbmV3IEVy'
    'cm9yKCJ1bnJlYWNoYWJsZSIpfWZ1bmN0aW9uIFlkKGUsdCxyLG4saSl7aWYo'
    'dm9pZCAwIT09aS5jcml0JiZ2b2lkIDA9PT1uPy5jcml0KXRocm93IG5ldyBl'
    'KCciY3JpdCIgKENyaXRpY2FsKSBIZWFkZXIgUGFyYW1ldGVyIE1VU1QgYmUg'
    'aW50ZWdyaXR5IHByb3RlY3RlZCcpO2lmKCFufHx2b2lkIDA9PT1uLmNyaXQp'
    'cmV0dXJuIG5ldyBTZXQ7aWYoIUFycmF5LmlzQXJyYXkobi5jcml0KXx8MD09'
    'PW4uY3JpdC5sZW5ndGh8fG4uY3JpdC5zb21lKGU9PiJzdHJpbmciIT10eXBl'
    'b2YgZXx8MD09PWUubGVuZ3RoKSl0aHJvdyBuZXcgZSgnImNyaXQiIChDcml0'
    'aWNhbCkgSGVhZGVyIFBhcmFtZXRlciBNVVNUIGJlIGFuIGFycmF5IG9mIG5v'
    'bi1lbXB0eSBzdHJpbmdzIHdoZW4gcHJlc2VudCcpO2xldCBzO3M9dm9pZCAw'
    'IT09cj9uZXcgTWFwKFsuLi5PYmplY3QuZW50cmllcyhyKSwuLi50LmVudHJp'
    'ZXMoKV0pOnQ7Zm9yKGNvbnN0IHQgb2Ygbi5jcml0KXtpZighcy5oYXModCkp'
    'dGhyb3cgbmV3IEhkKGBFeHRlbnNpb24gSGVhZGVyIFBhcmFtZXRlciAiJHt0'
    'fSIgaXMgbm90IHJlY29nbml6ZWRgKTtpZih2b2lkIDA9PT1pW3RdKXRocm93'
    'IG5ldyBlKGBFeHRlbnNpb24gSGVhZGVyIFBhcmFtZXRlciAiJHt0fSIgaXMg'
    'bWlzc2luZ2ApO2lmKHMuZ2V0KHQpJiZ2b2lkIDA9PT1uW3RdKXRocm93IG5l'
    'dyBlKGBFeHRlbnNpb24gSGVhZGVyIFBhcmFtZXRlciAiJHt0fSIgTVVTVCBi'
    'ZSBpbnRlZ3JpdHkgcHJvdGVjdGVkYCl9cmV0dXJuIG5ldyBTZXQobi5jcml0'
    'KX1mdW5jdGlvbiBaZChlLHQpe2lmKHZvaWQgMCE9PXQmJighQXJyYXkuaXNB'
    'cnJheSh0KXx8dC5zb21lKGU9PiJzdHJpbmciIT10eXBlb2YgZSkpKXRocm93'
    'IG5ldyBUeXBlRXJyb3IoYCIke2V9IiBvcHRpb24gbXVzdCBiZSBhbiBhcnJh'
    'eSBvZiBzdHJpbmdzYCk7aWYodClyZXR1cm4gbmV3IFNldCh0KX12YXIgR2Q9'
    'ZT0+ZT8uW1N5bWJvbC50b1N0cmluZ1RhZ10sUWQ9KGUsdCxyKT0+e2lmKHZv'
    'aWQgMCE9PXQudXNlKXtsZXQgZTtzd2l0Y2gocil7Y2FzZSJzaWduIjpjYXNl'
    'InZlcmlmeSI6ZT0ic2lnIjticmVhaztjYXNlImVuY3J5cHQiOmNhc2UiZGVj'
    'cnlwdCI6ZT0iZW5jIjticmVha31pZih0LnVzZSE9PWUpdGhyb3cgbmV3IFR5'
    'cGVFcnJvcihgSW52YWxpZCBrZXkgZm9yIHRoaXMgb3BlcmF0aW9uLCBpdHMg'
    'InVzZSIgbXVzdCBiZSAiJHtlfSIgd2hlbiBwcmVzZW50YCl9aWYodm9pZCAw'
    'IT09dC5hbGcmJnQuYWxnIT09ZSl0aHJvdyBuZXcgVHlwZUVycm9yKGBJbnZh'
    'bGlkIGtleSBmb3IgdGhpcyBvcGVyYXRpb24sIGl0cyAiYWxnIiBtdXN0IGJl'
    'ICIke2V9IiB3aGVuIHByZXNlbnRgKTtpZihBcnJheS5pc0FycmF5KHQua2V5'
    'X29wcykpe2xldCBuO3N3aXRjaCghMCl7Y2FzZSJzaWduIj09PXJ8fCJ2ZXJp'
    'ZnkiPT09cjpjYXNlImRpciI9PT1lOmNhc2UgZS5pbmNsdWRlcygiQ0JDLUhT'
    'Iik6bj1yO2JyZWFrO2Nhc2UgZS5zdGFydHNXaXRoKCJQQkVTMiIpOm49ImRl'
    'cml2ZUJpdHMiO2JyZWFrO2Nhc2UvXkFcZHszfSg/OkdDTSk/KD86S1cpPyQv'
    'LnRlc3QoZSk6bj0hZS5pbmNsdWRlcygiR0NNIikmJmUuZW5kc1dpdGgoIktX'
    'Iik/ImVuY3J5cHQiPT09cj8id3JhcEtleSI6InVud3JhcEtleSI6cjticmVh'
    'aztjYXNlImVuY3J5cHQiPT09ciYmZS5zdGFydHNXaXRoKCJSU0EiKTpuPSJ3'
    'cmFwS2V5IjticmVhaztjYXNlImRlY3J5cHQiPT09cjpuPWUuc3RhcnRzV2l0'
    'aCgiUlNBIik/InVud3JhcEtleSI6ImRlcml2ZUJpdHMiO2JyZWFrfWlmKG4m'
    'JiExPT09dC5rZXlfb3BzPy5pbmNsdWRlcz8uKG4pKXRocm93IG5ldyBUeXBl'
    'RXJyb3IoYEludmFsaWQga2V5IGZvciB0aGlzIG9wZXJhdGlvbiwgaXRzICJr'
    'ZXlfb3BzIiBtdXN0IGluY2x1ZGUgIiR7bn0iIHdoZW4gcHJlc2VudGApfXJl'
    'dHVybiEwfSxxZD0oZSx0LHIpPT57aWYoISh0IGluc3RhbmNlb2YgVWludDhB'
    'cnJheSkpe2lmKENkKHQpKXtpZihQZCh0KSYmUWQoZSx0LHIpKXJldHVybjt0'
    'aHJvdyBuZXcgVHlwZUVycm9yKCdKU09OIFdlYiBLZXkgZm9yIHN5bW1ldHJp'
    'YyBhbGdvcml0aG1zIG11c3QgaGF2ZSBKV0sgImt0eSIgKEtleSBUeXBlKSBl'
    'cXVhbCB0byAib2N0IiBhbmQgdGhlIEpXSyAiayIgKEtleSBWYWx1ZSkgcHJl'
    'c2VudCcpfWlmKCF2ZCh0KSl0aHJvdyBuZXcgVHlwZUVycm9yKGZkKGUsdCwi'
    'Q3J5cHRvS2V5IiwiS2V5T2JqZWN0IiwiSlNPTiBXZWIgS2V5IiwiVWludDhB'
    'cnJheSIpKTtpZigic2VjcmV0IiE9PXQudHlwZSl0aHJvdyBuZXcgVHlwZUVy'
    'cm9yKGAke0dkKHQpfSBpbnN0YW5jZXMgZm9yIHN5bW1ldHJpYyBhbGdvcml0'
    'aG1zIG11c3QgYmUgb2YgdHlwZSAic2VjcmV0ImApfX0sJGQ9KGUsdCxyKT0+'
    'e2lmKENkKHQpKXN3aXRjaChyKXtjYXNlImRlY3J5cHQiOmNhc2Uic2lnbiI6'
    'aWYoX2QodCkmJlFkKGUsdCxyKSlyZXR1cm47dGhyb3cgbmV3IFR5cGVFcnJv'
    'cigiSlNPTiBXZWIgS2V5IGZvciB0aGlzIG9wZXJhdGlvbiBtdXN0IGJlIGEg'
    'cHJpdmF0ZSBKV0siKTtjYXNlImVuY3J5cHQiOmNhc2UidmVyaWZ5IjppZihP'
    'ZCh0KSYmUWQoZSx0LHIpKXJldHVybjt0aHJvdyBuZXcgVHlwZUVycm9yKCJK'
    'U09OIFdlYiBLZXkgZm9yIHRoaXMgb3BlcmF0aW9uIG11c3QgYmUgYSBwdWJs'
    'aWMgSldLIil9aWYoIXZkKHQpKXRocm93IG5ldyBUeXBlRXJyb3IoZmQoZSx0'
    'LCJDcnlwdG9LZXkiLCJLZXlPYmplY3QiLCJKU09OIFdlYiBLZXkiKSk7aWYo'
    'InNlY3JldCI9PT10LnR5cGUpdGhyb3cgbmV3IFR5cGVFcnJvcihgJHtHZCh0'
    'KX0gaW5zdGFuY2VzIGZvciBhc3ltbWV0cmljIGFsZ29yaXRobXMgbXVzdCBu'
    'b3QgYmUgb2YgdHlwZSAic2VjcmV0ImApO2lmKCJwdWJsaWMiPT09dC50eXBl'
    'KXN3aXRjaChyKXtjYXNlInNpZ24iOnRocm93IG5ldyBUeXBlRXJyb3IoYCR7'
    'R2QodCl9IGluc3RhbmNlcyBmb3IgYXN5bW1ldHJpYyBhbGdvcml0aG0gc2ln'
    'bmluZyBtdXN0IGJlIG9mIHR5cGUgInByaXZhdGUiYCk7Y2FzZSJkZWNyeXB0'
    'Ijp0aHJvdyBuZXcgVHlwZUVycm9yKGAke0dkKHQpfSBpbnN0YW5jZXMgZm9y'
    'IGFzeW1tZXRyaWMgYWxnb3JpdGhtIGRlY3J5cHRpb24gbXVzdCBiZSBvZiB0'
    'eXBlICJwcml2YXRlImApfWlmKCJwcml2YXRlIj09PXQudHlwZSlzd2l0Y2go'
    'cil7Y2FzZSJ2ZXJpZnkiOnRocm93IG5ldyBUeXBlRXJyb3IoYCR7R2QodCl9'
    'IGluc3RhbmNlcyBmb3IgYXN5bW1ldHJpYyBhbGdvcml0aG0gdmVyaWZ5aW5n'
    'IG11c3QgYmUgb2YgdHlwZSAicHVibGljImApO2Nhc2UiZW5jcnlwdCI6dGhy'
    'b3cgbmV3IFR5cGVFcnJvcihgJHtHZCh0KX0gaW5zdGFuY2VzIGZvciBhc3lt'
    'bWV0cmljIGFsZ29yaXRobSBlbmNyeXB0aW9uIG11c3QgYmUgb2YgdHlwZSAi'
    'cHVibGljImApfX07ZnVuY3Rpb24gZXcoZSx0LHIpe3N3aXRjaChlLnN1YnN0'
    'cmluZygwLDIpKXtjYXNlIkExIjpjYXNlIkEyIjpjYXNlImRpIjpjYXNlIkhT'
    'IjpjYXNlIlBCIjpxZChlLHQscik7YnJlYWs7ZGVmYXVsdDokZChlLHQscil9'
    'fWFzeW5jIGZ1bmN0aW9uIHR3KGUsdCxyKXtpZigha2QoZSkpdGhyb3cgbmV3'
    'IG1kKCJGbGF0dGVuZWQgSldTIG11c3QgYmUgYW4gb2JqZWN0Iik7aWYodm9p'
    'ZCAwPT09ZS5wcm90ZWN0ZWQmJnZvaWQgMD09PWUuaGVhZGVyKXRocm93IG5l'
    'dyBtZCgnRmxhdHRlbmVkIEpXUyBtdXN0IGhhdmUgZWl0aGVyIG9mIHRoZSAi'
    'cHJvdGVjdGVkIiBvciAiaGVhZGVyIiBtZW1iZXJzJyk7aWYodm9pZCAwIT09'
    'ZS5wcm90ZWN0ZWQmJiJzdHJpbmciIT10eXBlb2YgZS5wcm90ZWN0ZWQpdGhy'
    'b3cgbmV3IG1kKCJKV1MgUHJvdGVjdGVkIEhlYWRlciBpbmNvcnJlY3QgdHlw'
    'ZSIpO2lmKHZvaWQgMD09PWUucGF5bG9hZCl0aHJvdyBuZXcgbWQoIkpXUyBQ'
    'YXlsb2FkIG1pc3NpbmciKTtpZigic3RyaW5nIiE9dHlwZW9mIGUuc2lnbmF0'
    'dXJlKXRocm93IG5ldyBtZCgiSldTIFNpZ25hdHVyZSBtaXNzaW5nIG9yIGlu'
    'Y29ycmVjdCB0eXBlIik7aWYodm9pZCAwIT09ZS5oZWFkZXImJiFrZChlLmhl'
    'YWRlcikpdGhyb3cgbmV3IG1kKCJKV1MgVW5wcm90ZWN0ZWQgSGVhZGVyIGlu'
    'Y29ycmVjdCB0eXBlIik7bGV0IG49e307aWYoZS5wcm90ZWN0ZWQpdHJ5e2Nv'
    'bnN0IHQ9bmQoZS5wcm90ZWN0ZWQpO249SlNPTi5wYXJzZShRbC5kZWNvZGUo'
    'dCkpfWNhdGNoe3Rocm93IG5ldyBtZCgiSldTIFByb3RlY3RlZCBIZWFkZXIg'
    'aXMgaW52YWxpZCIpfWlmKCFTZChuLGUuaGVhZGVyKSl0aHJvdyBuZXcgbWQo'
    'IkpXUyBQcm90ZWN0ZWQgYW5kIEpXUyBVbnByb3RlY3RlZCBIZWFkZXIgUGFy'
    'YW1ldGVyIG5hbWVzIG11c3QgYmUgZGlzam9pbnQiKTtjb25zdCBpPXsuLi5u'
    'LC4uLmUuaGVhZGVyfSxzPXZvaWQgMDtsZXQgbz0hMDtpZihZZChtZCxuZXcg'
    'TWFwKFtbImI2NCIsITBdXSkscj8uY3JpdCxuLGkpLmhhcygiYjY0IikmJihv'
    'PW4uYjY0LCJib29sZWFuIiE9dHlwZW9mIG8pKXRocm93IG5ldyBtZCgnVGhl'
    'ICJiNjQiIChiYXNlNjR1cmwtZW5jb2RlIHBheWxvYWQpIEhlYWRlciBQYXJh'
    'bWV0ZXIgbXVzdCBiZSBhIGJvb2xlYW4nKTtjb25zdHthbGc6YX09aTtpZigi'
    'c3RyaW5nIiE9dHlwZW9mIGF8fCFhKXRocm93IG5ldyBtZCgnSldTICJhbGci'
    'IChBbGdvcml0aG0pIEhlYWRlciBQYXJhbWV0ZXIgbWlzc2luZyBvciBpbnZh'
    'bGlkJyk7Y29uc3QgYz1yJiZaZCgiYWxnb3JpdGhtcyIsci5hbGdvcml0aG1z'
    'KTtpZihjJiYhYy5oYXMoYSkpdGhyb3cgbmV3IEJkKCciYWxnIiAoQWxnb3Jp'
    'dGhtKSBIZWFkZXIgUGFyYW1ldGVyIHZhbHVlIG5vdCBhbGxvd2VkJyk7aWYo'
    'byl7aWYoInN0cmluZyIhPXR5cGVvZiBlLnBheWxvYWQpdGhyb3cgbmV3IG1k'
    'KCJKV1MgUGF5bG9hZCBtdXN0IGJlIGEgc3RyaW5nIil9ZWxzZSBpZigic3Ry'
    'aW5nIiE9dHlwZW9mIGUucGF5bG9hZCYmIShlLnBheWxvYWQgaW5zdGFuY2Vv'
    'ZiBVaW50OEFycmF5KSl0aHJvdyBuZXcgbWQoIkpXUyBQYXlsb2FkIG11c3Qg'
    'YmUgYSBzdHJpbmcgb3IgYW4gVWludDhBcnJheSBpbnN0YW5jZSIpO2xldCB1'
    'PSExOyJmdW5jdGlvbiI9PXR5cGVvZiB0JiYodD1hd2FpdCB0KG4sZSksdT0h'
    'MCksZXcoYSx0LCJ2ZXJpZnkiKTtjb25zdCBsPSRsKHZvaWQgMCE9PWUucHJv'
    'dGVjdGVkP2VkKGUucHJvdGVjdGVkKTpuZXcgVWludDhBcnJheSxlZCgiLiIp'
    'LCJzdHJpbmciPT10eXBlb2YgZS5wYXlsb2FkP28/ZWQoZS5wYXlsb2FkKTpH'
    'bC5lbmNvZGUoZS5wYXlsb2FkKTplLnBheWxvYWQpLGQ9UmQoZS5zaWduYXR1'
    'cmUsInNpZ25hdHVyZSIsbWQpLHc9YXdhaXQgVmQodCxhKSxoPXZvaWQgMDtp'
    'ZighYXdhaXQgTmQoYSx3LGQsbCkpdGhyb3cgbmV3IHlkO2xldCBmO2Y9bz9S'
    'ZChlLnBheWxvYWQsInBheWxvYWQiLG1kKToic3RyaW5nIj09dHlwZW9mIGUu'
    'cGF5bG9hZD9HbC5lbmNvZGUoZS5wYXlsb2FkKTplLnBheWxvYWQ7Y29uc3Qg'
    'QT17cGF5bG9hZDpmfTtyZXR1cm4gdm9pZCAwIT09ZS5wcm90ZWN0ZWQmJihB'
    'LnByb3RlY3RlZEhlYWRlcj1uKSx2b2lkIDAhPT1lLmhlYWRlciYmKEEudW5w'
    'cm90ZWN0ZWRIZWFkZXI9ZS5oZWFkZXIpLHU/ey4uLkEsa2V5Ond9OkF9YXN5'
    'bmMgZnVuY3Rpb24gcncoZSx0LHIpe2lmKGUgaW5zdGFuY2VvZiBVaW50OEFy'
    'cmF5JiYoZT1RbC5kZWNvZGUoZSkpLCJzdHJpbmciIT10eXBlb2YgZSl0aHJv'
    'dyBuZXcgbWQoIkNvbXBhY3QgSldTIG11c3QgYmUgYSBzdHJpbmcgb3IgVWlu'
    'dDhBcnJheSIpO2NvbnN0ezA6biwxOmksMjpzLGxlbmd0aDpvfT1lLnNwbGl0'
    'KCIuIik7aWYoMyE9PW8pdGhyb3cgbmV3IG1kKCJJbnZhbGlkIENvbXBhY3Qg'
    'SldTIik7Y29uc3QgYT1hd2FpdCB0dyh7cGF5bG9hZDppLHByb3RlY3RlZDpu'
    'LHNpZ25hdHVyZTpzfSx0LHIpLGM9e3BheWxvYWQ6YS5wYXlsb2FkLHByb3Rl'
    'Y3RlZEhlYWRlcjphLnByb3RlY3RlZEhlYWRlcn07cmV0dXJuImZ1bmN0aW9u'
    'Ij09dHlwZW9mIHQ/ey4uLmMsa2V5OmEua2V5fTpjfXZhciBudz1lPT5NYXRo'
    'LmZsb29yKGUuZ2V0VGltZSgpLzFlMyksaXc9NjAsc3c9MzYwMCxvdz04NjQw'
    'MCxhdz03Km93LGN3PTMxNTU3NjAwLHV3PS9eKFwrfFwtKT8gPyhcZCt8XGQr'
    'XC5cZCspID8oc2Vjb25kcz98c2Vjcz98c3xtaW51dGVzP3xtaW5zP3xtfGhv'
    'dXJzP3xocnM/fGh8ZGF5cz98ZHx3ZWVrcz98d3x5ZWFycz98eXJzP3x5KSg/'
    'OiAoYWdvfGZyb20gbm93KSk/JC9pO2Z1bmN0aW9uIGx3KGUpe2NvbnN0IHQ9'
    'dXcuZXhlYyhlKTtpZighdHx8dFs0XSYmdFsxXSl0aHJvdyBuZXcgVHlwZUVy'
    'cm9yKCJJbnZhbGlkIHRpbWUgcGVyaW9kIGZvcm1hdCIpO2NvbnN0IHI9cGFy'
    'c2VGbG9hdCh0WzJdKSxuPXZvaWQgMDtsZXQgaTtzd2l0Y2godFszXS50b0xv'
    'd2VyQ2FzZSgpKXtjYXNlInNlYyI6Y2FzZSJzZWNzIjpjYXNlInNlY29uZCI6'
    'Y2FzZSJzZWNvbmRzIjpjYXNlInMiOmk9TWF0aC5yb3VuZChyKTticmVhaztj'
    'YXNlIm1pbnV0ZSI6Y2FzZSJtaW51dGVzIjpjYXNlIm1pbiI6Y2FzZSJtaW5z'
    'IjpjYXNlIm0iOmk9TWF0aC5yb3VuZChyKml3KTticmVhaztjYXNlImhvdXIi'
    'OmNhc2UiaG91cnMiOmNhc2UiaHIiOmNhc2UiaHJzIjpjYXNlImgiOmk9TWF0'
    'aC5yb3VuZChyKnN3KTticmVhaztjYXNlImRheSI6Y2FzZSJkYXlzIjpjYXNl'
    'ImQiOmk9TWF0aC5yb3VuZChyKm93KTticmVhaztjYXNlIndlZWsiOmNhc2Ui'
    'd2Vla3MiOmNhc2UidyI6aT1NYXRoLnJvdW5kKHIqYXcpO2JyZWFrO2RlZmF1'
    'bHQ6aT1NYXRoLnJvdW5kKHIqY3cpO2JyZWFrfXJldHVybiItIj09PXRbMV18'
    'fCJhZ28iPT09dFs0XT8taTppfWZ1bmN0aW9uIGR3KGUsdCl7aWYoIU51bWJl'
    'ci5pc0Zpbml0ZSh0KSl0aHJvdyBuZXcgVHlwZUVycm9yKGBJbnZhbGlkICR7'
    'ZX0gaW5wdXRgKTtyZXR1cm4gdH12YXIgd3c9ZT0+ZS5pbmNsdWRlcygiLyIp'
    'P2UudG9Mb3dlckNhc2UoKTpgYXBwbGljYXRpb24vJHtlLnRvTG93ZXJDYXNl'
    'KCl9YCxodz0oZSx0KT0+InN0cmluZyI9PXR5cGVvZiBlP3QuaW5jbHVkZXMo'
    'ZSk6ISFBcnJheS5pc0FycmF5KGUpJiZ0LnNvbWUoU2V0LnByb3RvdHlwZS5o'
    'YXMuYmluZChuZXcgU2V0KGUpKSk7ZnVuY3Rpb24gZncoZSx0LHI9e30pe2xl'
    'dCBuO3RyeXtuPUpTT04ucGFyc2UoUWwuZGVjb2RlKHQpKX1jYXRjaHt9aWYo'
    'IWtkKG4pKXRocm93IG5ldyBnZCgiSldUIENsYWltcyBTZXQgbXVzdCBiZSBh'
    'IHRvcC1sZXZlbCBKU09OIG9iamVjdCIpO2NvbnN0e3R5cDppfT1yO2lmKGkm'
    'Jigic3RyaW5nIiE9dHlwZW9mIGUudHlwfHx3dyhlLnR5cCkhPT13dyhpKSkp'
    'dGhyb3cgbmV3IHBkKCd1bmV4cGVjdGVkICJ0eXAiIEpXVCBoZWFkZXIgdmFs'
    'dWUnLG4sInR5cCIsImNoZWNrX2ZhaWxlZCIpO2NvbnN0e3JlcXVpcmVkQ2xh'
    'aW1zOnM9W10saXNzdWVyOm8sc3ViamVjdDphLGF1ZGllbmNlOmMsbWF4VG9r'
    'ZW5BZ2U6dX09cixsPVsuLi5zXTt2b2lkIDAhPT11JiZsLnB1c2goImlhdCIp'
    'LHZvaWQgMCE9PWMmJmwucHVzaCgiYXVkIiksdm9pZCAwIT09YSYmbC5wdXNo'
    'KCJzdWIiKSx2b2lkIDAhPT1vJiZsLnB1c2goImlzcyIpO2Zvcihjb25zdCBl'
    'IG9mIG5ldyBTZXQobC5yZXZlcnNlKCkpKWlmKCEoZSBpbiBuKSl0aHJvdyBu'
    'ZXcgcGQoYG1pc3NpbmcgcmVxdWlyZWQgIiR7ZX0iIGNsYWltYCxuLGUsIm1p'
    'c3NpbmciKTtpZihvJiYhKEFycmF5LmlzQXJyYXkobyk/bzpbb10pLmluY2x1'
    'ZGVzKG4uaXNzKSl0aHJvdyBuZXcgcGQoJ3VuZXhwZWN0ZWQgImlzcyIgY2xh'
    'aW0gdmFsdWUnLG4sImlzcyIsImNoZWNrX2ZhaWxlZCIpO2lmKGEmJm4uc3Vi'
    'IT09YSl0aHJvdyBuZXcgcGQoJ3VuZXhwZWN0ZWQgInN1YiIgY2xhaW0gdmFs'
    'dWUnLG4sInN1YiIsImNoZWNrX2ZhaWxlZCIpO2lmKGMmJiFodyhuLmF1ZCwi'
    'c3RyaW5nIj09dHlwZW9mIGM/W2NdOmMpKXRocm93IG5ldyBwZCgndW5leHBl'
    'Y3RlZCAiYXVkIiBjbGFpbSB2YWx1ZScsbiwiYXVkIiwiY2hlY2tfZmFpbGVk'
    'Iik7bGV0IGQ7c3dpdGNoKHR5cGVvZiByLmNsb2NrVG9sZXJhbmNlKXtjYXNl'
    'InN0cmluZyI6ZD1sdyhyLmNsb2NrVG9sZXJhbmNlKTticmVhaztjYXNlIm51'
    'bWJlciI6ZD1yLmNsb2NrVG9sZXJhbmNlO2JyZWFrO2Nhc2UidW5kZWZpbmVk'
    'IjpkPTA7YnJlYWs7ZGVmYXVsdDp0aHJvdyBuZXcgVHlwZUVycm9yKCJJbnZh'
    'bGlkIGNsb2NrVG9sZXJhbmNlIG9wdGlvbiB0eXBlIil9Y29uc3R7Y3VycmVu'
    'dERhdGU6d309cixoPW53KHd8fG5ldyBEYXRlKTtpZigodm9pZCAwIT09bi5p'
    'YXR8fHUpJiYibnVtYmVyIiE9dHlwZW9mIG4uaWF0KXRocm93IG5ldyBwZCgn'
    'ImlhdCIgY2xhaW0gbXVzdCBiZSBhIG51bWJlcicsbiwiaWF0IiwiaW52YWxp'
    'ZCIpO2lmKHZvaWQgMCE9PW4ubmJmKXtpZigibnVtYmVyIiE9dHlwZW9mIG4u'
    'bmJmKXRocm93IG5ldyBwZCgnIm5iZiIgY2xhaW0gbXVzdCBiZSBhIG51bWJl'
    'cicsbiwibmJmIiwiaW52YWxpZCIpO2lmKG4ubmJmPmgrZCl0aHJvdyBuZXcg'
    'cGQoJyJuYmYiIGNsYWltIHRpbWVzdGFtcCBjaGVjayBmYWlsZWQnLG4sIm5i'
    'ZiIsImNoZWNrX2ZhaWxlZCIpfWlmKHZvaWQgMCE9PW4uZXhwKXtpZigibnVt'
    'YmVyIiE9dHlwZW9mIG4uZXhwKXRocm93IG5ldyBwZCgnImV4cCIgY2xhaW0g'
    'bXVzdCBiZSBhIG51bWJlcicsbiwiZXhwIiwiaW52YWxpZCIpO2lmKG4uZXhw'
    'PD1oLWQpdGhyb3cgbmV3IEVkKCciZXhwIiBjbGFpbSB0aW1lc3RhbXAgY2hl'
    'Y2sgZmFpbGVkJyxuLCJleHAiLCJjaGVja19mYWlsZWQiKX1pZih1KXtjb25z'
    'dCBlPWgtbi5pYXQsdD12b2lkIDA7aWYoZS1kPigibnVtYmVyIj09dHlwZW9m'
    'IHU/dTpsdyh1KSkpdGhyb3cgbmV3IEVkKCciaWF0IiBjbGFpbSB0aW1lc3Rh'
    'bXAgY2hlY2sgZmFpbGVkICh0b28gZmFyIGluIHRoZSBwYXN0KScsbiwiaWF0'
    'IiwiY2hlY2tfZmFpbGVkIik7aWYoZTwwLWQpdGhyb3cgbmV3IHBkKCciaWF0'
    'IiBjbGFpbSB0aW1lc3RhbXAgY2hlY2sgZmFpbGVkIChpdCBzaG91bGQgYmUg'
    'aW4gdGhlIHBhc3QpJyxuLCJpYXQiLCJjaGVja19mYWlsZWQiKX1yZXR1cm4g'
    'bn12YXIgQXc9Y2xhc3N7I2U7Y29uc3RydWN0b3IoZSl7aWYoIWtkKGUpKXRo'
    'cm93IG5ldyBUeXBlRXJyb3IoIkpXVCBDbGFpbXMgU2V0IE1VU1QgYmUgYW4g'
    'b2JqZWN0Iik7dGhpcy4jZT1zdHJ1Y3R1cmVkQ2xvbmUoZSl9ZGF0YSgpe3Jl'
    'dHVybiBHbC5lbmNvZGUoSlNPTi5zdHJpbmdpZnkodGhpcy4jZSkpfWdldCBp'
    'c3MoKXtyZXR1cm4gdGhpcy4jZS5pc3N9c2V0IGlzcyhlKXt0aGlzLiNlLmlz'
    'cz1lfWdldCBzdWIoKXtyZXR1cm4gdGhpcy4jZS5zdWJ9c2V0IHN1YihlKXt0'
    'aGlzLiNlLnN1Yj1lfWdldCBhdWQoKXtyZXR1cm4gdGhpcy4jZS5hdWR9c2V0'
    'IGF1ZChlKXt0aGlzLiNlLmF1ZD1lfXNldCBqdGkoZSl7dGhpcy4jZS5qdGk9'
    'ZX1zZXQgbmJmKGUpeyJudW1iZXIiPT10eXBlb2YgZT90aGlzLiNlLm5iZj1k'
    'dygic2V0Tm90QmVmb3JlIixlKTplIGluc3RhbmNlb2YgRGF0ZT90aGlzLiNl'
    'Lm5iZj1kdygic2V0Tm90QmVmb3JlIixudyhlKSk6dGhpcy4jZS5uYmY9bnco'
    'bmV3IERhdGUpK2x3KGUpfXNldCBleHAoZSl7Im51bWJlciI9PXR5cGVvZiBl'
    'P3RoaXMuI2UuZXhwPWR3KCJzZXRFeHBpcmF0aW9uVGltZSIsZSk6ZSBpbnN0'
    'YW5jZW9mIERhdGU/dGhpcy4jZS5leHA9ZHcoInNldEV4cGlyYXRpb25UaW1l'
    'IixudyhlKSk6dGhpcy4jZS5leHA9bncobmV3IERhdGUpK2x3KGUpfXNldCBp'
    'YXQoZSl7dm9pZCAwPT09ZT90aGlzLiNlLmlhdD1udyhuZXcgRGF0ZSk6ZSBp'
    'bnN0YW5jZW9mIERhdGU/dGhpcy4jZS5pYXQ9ZHcoInNldElzc3VlZEF0Iixu'
    'dyhlKSk6dGhpcy4jZS5pYXQ9ZHcoInNldElzc3VlZEF0Iiwic3RyaW5nIj09'
    'dHlwZW9mIGU/bncobmV3IERhdGUpK2x3KGUpOmUpfX07YXN5bmMgZnVuY3Rp'
    'b24gcHcoZSx0LHIpe2NvbnN0IG49YXdhaXQgcncoZSx0LHIpO2lmKG4ucHJv'
    'dGVjdGVkSGVhZGVyLmNyaXQ/LmluY2x1ZGVzKCJiNjQiKSYmITE9PT1uLnBy'
    'b3RlY3RlZEhlYWRlci5iNjQpdGhyb3cgbmV3IGdkKCJKV1RzIE1VU1QgTk9U'
    'IHVzZSB1bmVuY29kZWQgcGF5bG9hZCIpO2NvbnN0IGk9dm9pZCAwLHM9e3Bh'
    'eWxvYWQ6Zncobi5wcm90ZWN0ZWRIZWFkZXIsbi5wYXlsb2FkLHIpLHByb3Rl'
    'Y3RlZEhlYWRlcjpuLnByb3RlY3RlZEhlYWRlcn07cmV0dXJuImZ1bmN0aW9u'
    'Ij09dHlwZW9mIHQ/ey4uLnMsa2V5Om4ua2V5fTpzfXZhciBFdz1jbGFzc3sj'
    'ZTsjdDsjcjtjb25zdHJ1Y3RvcihlKXtpZighKGUgaW5zdGFuY2VvZiBVaW50'
    'OEFycmF5KSl0aHJvdyBuZXcgVHlwZUVycm9yKCJwYXlsb2FkIG11c3QgYmUg'
    'YW4gaW5zdGFuY2Ugb2YgVWludDhBcnJheSIpO3RoaXMuI2U9ZX1zZXRQcm90'
    'ZWN0ZWRIZWFkZXIoZSl7cmV0dXJuIGJkKHRoaXMuI3QsInNldFByb3RlY3Rl'
    'ZEhlYWRlciIpLHRoaXMuI3Q9ZSx0aGlzfXNldFVucHJvdGVjdGVkSGVhZGVy'
    'KGUpe3JldHVybiBiZCh0aGlzLiNyLCJzZXRVbnByb3RlY3RlZEhlYWRlciIp'
    'LHRoaXMuI3I9ZSx0aGlzfWFzeW5jIHNpZ24oZSx0KXtpZighdGhpcy4jdCYm'
    'IXRoaXMuI3IpdGhyb3cgbmV3IG1kKCJlaXRoZXIgc2V0UHJvdGVjdGVkSGVh'
    'ZGVyIG9yIHNldFVucHJvdGVjdGVkSGVhZGVyIG11c3QgYmUgY2FsbGVkIGJl'
    'Zm9yZSAjc2lnbigpIik7aWYoIVNkKHRoaXMuI3QsdGhpcy4jcikpdGhyb3cg'
    'bmV3IG1kKCJKV1MgUHJvdGVjdGVkIGFuZCBKV1MgVW5wcm90ZWN0ZWQgSGVh'
    'ZGVyIFBhcmFtZXRlciBuYW1lcyBtdXN0IGJlIGRpc2pvaW50Iik7Y29uc3Qg'
    'cj17Li4udGhpcy4jdCwuLi50aGlzLiNyfSxuPXZvaWQgMDtsZXQgaT0hMDtp'
    'ZihZZChtZCxuZXcgTWFwKFtbImI2NCIsITBdXSksdD8uY3JpdCx0aGlzLiN0'
    'LHIpLmhhcygiYjY0IikmJihpPXRoaXMuI3QuYjY0LCJib29sZWFuIiE9dHlw'
    'ZW9mIGkpKXRocm93IG5ldyBtZCgnVGhlICJiNjQiIChiYXNlNjR1cmwtZW5j'
    'b2RlIHBheWxvYWQpIEhlYWRlciBQYXJhbWV0ZXIgbXVzdCBiZSBhIGJvb2xl'
    'YW4nKTtjb25zdHthbGc6c309cjtpZigic3RyaW5nIiE9dHlwZW9mIHN8fCFz'
    'KXRocm93IG5ldyBtZCgnSldTICJhbGciIChBbGdvcml0aG0pIEhlYWRlciBQ'
    'YXJhbWV0ZXIgbWlzc2luZyBvciBpbnZhbGlkJyk7bGV0IG8sYSxjLHU7ZXco'
    'cyxlLCJzaWduIiksaT8obz1pZCh0aGlzLiNlKSxhPWVkKG8pKTooYT10aGlz'
    'LiNlLG89IiIpLHRoaXMuI3Q/KGM9aWQoSlNPTi5zdHJpbmdpZnkodGhpcy4j'
    'dCkpLHU9ZWQoYykpOihjPSIiLHU9bmV3IFVpbnQ4QXJyYXkpO2NvbnN0IGw9'
    'JGwodSxlZCgiLiIpLGEpLGQ9YXdhaXQgVmQoZSxzKSx3PXZvaWQgMCxoPXtz'
    'aWduYXR1cmU6aWQoYXdhaXQgVWQocyxkLGwpKSxwYXlsb2FkOm99O3JldHVy'
    'biB0aGlzLiNyJiYoaC5oZWFkZXI9dGhpcy4jciksdGhpcy4jdCYmKGgucHJv'
    'dGVjdGVkPWMpLGh9fSxCdz1jbGFzc3sjbjtjb25zdHJ1Y3RvcihlKXt0aGlz'
    'LiNuPW5ldyBFdyhlKX1zZXRQcm90ZWN0ZWRIZWFkZXIoZSl7cmV0dXJuIHRo'
    'aXMuI24uc2V0UHJvdGVjdGVkSGVhZGVyKGUpLHRoaXN9YXN5bmMgc2lnbihl'
    'LHQpe2NvbnN0IHI9YXdhaXQgdGhpcy4jbi5zaWduKGUsdCk7aWYodm9pZCAw'
    'PT09ci5wYXlsb2FkKXRocm93IG5ldyBUeXBlRXJyb3IoInVzZSB0aGUgZmxh'
    'dHRlbmVkIG1vZHVsZSBmb3IgY3JlYXRpbmcgSldTIHdpdGggYjY0OiBmYWxz'
    'ZSIpO3JldHVybmAke3IucHJvdGVjdGVkfS4ke3IucGF5bG9hZH0uJHtyLnNp'
    'Z25hdHVyZX1gfX0sSHc9Y2xhc3N7I3Q7I2k7Y29uc3RydWN0b3IoZT17fSl7'
    'dGhpcy4jaT1uZXcgQXcoZSl9c2V0SXNzdWVyKGUpe3JldHVybiB0aGlzLiNp'
    'Lmlzcz1lLHRoaXN9c2V0U3ViamVjdChlKXtyZXR1cm4gdGhpcy4jaS5zdWI9'
    'ZSx0aGlzfXNldEF1ZGllbmNlKGUpe3JldHVybiB0aGlzLiNpLmF1ZD1lLHRo'
    'aXN9c2V0SnRpKGUpe3JldHVybiB0aGlzLiNpLmp0aT1lLHRoaXN9c2V0Tm90'
    'QmVmb3JlKGUpe3JldHVybiB0aGlzLiNpLm5iZj1lLHRoaXN9c2V0RXhwaXJh'
    'dGlvblRpbWUoZSl7cmV0dXJuIHRoaXMuI2kuZXhwPWUsdGhpc31zZXRJc3N1'
    'ZWRBdChlKXtyZXR1cm4gdGhpcy4jaS5pYXQ9ZSx0aGlzfXNldFByb3RlY3Rl'
    'ZEhlYWRlcihlKXtyZXR1cm4gdGhpcy4jdD1lLHRoaXN9YXN5bmMgc2lnbihl'
    'LHQpe2NvbnN0IHI9bmV3IEJ3KHRoaXMuI2kuZGF0YSgpKTtpZihyLnNldFBy'
    'b3RlY3RlZEhlYWRlcih0aGlzLiN0KSxBcnJheS5pc0FycmF5KHRoaXMuI3Q/'
    'LmNyaXQpJiZ0aGlzLiN0LmNyaXQuaW5jbHVkZXMoImI2NCIpJiYhMT09PXRo'
    'aXMuI3QuYjY0KXRocm93IG5ldyBnZCgiSldUcyBNVVNUIE5PVCB1c2UgdW5l'
    'bmNvZGVkIHBheWxvYWQiKTtyZXR1cm4gci5zaWduKGUsdCl9fTthc3luYyBm'
    'dW5jdGlvbiBtdyhlLHQpe2lmKCJQT1NUIiE9PWUubWV0aG9kKXJldHVybiBC'
    'bCghMSw0MDUsIk1ldGhvZCBub3QgYWxsb3dlZC4iKTtjb25zdCByPXZvaWQg'
    'MCxuPXZvaWQgMDtpZihhd2FpdCBlLnRleHQoKSE9PWF3YWl0IHQua3YuZ2V0'
    'KCJwd2QiKSlyZXR1cm4gQmwoITEsNDAxLCJXcm9uZyBwYXNzd29yZC4iKTts'
    'ZXQgaT1hd2FpdCB0Lmt2LmdldCgic2VjcmV0S2V5Iik7aXx8KGk9Z3coKSxh'
    'd2FpdCB0Lmt2LnB1dCgic2VjcmV0S2V5IixpKSk7Y29uc3Qgcz0obmV3IFRl'
    'eHRFbmNvZGVyKS5lbmNvZGUoaSkse3VzZXJJRDpvfT1nbG9iYWxUaGlzLmds'
    'b2JhbENvbmZpZyxhPXZvaWQgMDtyZXR1cm4gQmwoITAsMjAwLCJTdWNjZXNz'
    'ZnVsbHkgZ2VuZXJhdGVkIEF1dGggdG9rZW4iLG51bGwseyJTZXQtQ29va2ll'
    'Ijpgand0VG9rZW49JHthd2FpdCBuZXcgSHcoe3VzZXJJRDpvfSkuc2V0UHJv'
    'dGVjdGVkSGVhZGVyKHthbGc6IkhTMjU2In0pLnNldElzc3VlZEF0KCkuc2V0'
    'RXhwaXJhdGlvblRpbWUoIjI0aCIpLnNpZ24ocyl9OyBIdHRwT25seTsgU2Vj'
    'dXJlOyBNYXgtQWdlPTYwNDgwMDsgUGF0aD0vOyBTYW1lU2l0ZT1TdHJpY3Rg'
    'LCJDb250ZW50LVR5cGUiOiJ0ZXh0L3BsYWluIn0pfWZ1bmN0aW9uIGd3KCl7'
    'Y29uc3QgZT1uZXcgVWludDhBcnJheSgzMik7cmV0dXJuIGNyeXB0by5nZXRS'
    'YW5kb21WYWx1ZXMoZSksQXJyYXkuZnJvbShlLGU9PmUudG9TdHJpbmcoMTYp'
    'LnBhZFN0YXJ0KDIsIjAiKSkuam9pbigiIil9YXN5bmMgZnVuY3Rpb24geXco'
    'ZSx0KXt0cnl7Y29uc3Qgcj1hd2FpdCB0Lmt2LmdldCgic2VjcmV0S2V5Iik7'
    'aWYobnVsbD09PXIpcmV0dXJuIGNvbnNvbGUubG9nKCJTZWNyZXQga2V5IG5v'
    'dCBmb3VuZCBpbiBLVi4iKSwhMTtjb25zdCBuPShuZXcgVGV4dEVuY29kZXIp'
    'LmVuY29kZShyKSxpPWUuaGVhZGVycy5nZXQoIkNvb2tpZSIpPy5tYXRjaCgv'
    'KF58O1xzKilqd3RUb2tlbj0oW147XSopLykscz1pP2lbMl06bnVsbDtpZigh'
    'cylyZXR1cm4gY29uc29sZS5sb2coIlVuYXV0aG9yaXplZDogVG9rZW4gbm90'
    'IGF2YWlsYWJsZSEiKSwhMTtjb25zdHtwYXlsb2FkOm99PWF3YWl0IHB3KHMs'
    'bik7cmV0dXJuIGNvbnNvbGUubG9nKGBTdWNjZXNzZnVsbHkgYXV0aGVudGlj'
    'YXRlZCwgVXNlciBJRDogJHtvLnVzZXJJRH1gKSwhMH1jYXRjaChlKXtyZXR1'
    'cm4gY29uc29sZS5sb2coZSksITF9fWFzeW5jIGZ1bmN0aW9uIFR3KGUsdCl7'
    'bGV0IHI9YXdhaXQgeXcoZSx0KTtjb25zdCBuPWF3YWl0IHQua3YuZ2V0KCJw'
    'd2QiKTtpZihuJiYhcilyZXR1cm4gQmwoITEsNDAxLCJVbmF1dGhvcml6ZWQu'
    'Iik7Y29uc3QgaT1hd2FpdCBlLnRleHQoKTtyZXR1cm4gaT09PW4/QmwoITEs'
    'NDAwLCJQbGVhc2UgZW50ZXIgYSBuZXcgUGFzc3dvcmQuIik6KGF3YWl0IHQu'
    'a3YucHV0KCJwd2QiLGkpLEJsKCEwLDIwMCwiU3VjY2Vzc2Z1bGx5IGxvZ2dl'
    'ZCBpbiEiLG51bGwseyJTZXQtQ29va2llIjoiand0VG9rZW49OyBQYXRoPS87'
    'IFNlY3VyZTsgU2FtZVNpdGU9Tm9uZTsgRXhwaXJlcz1UaHUsIDAxIEphbiAx'
    'OTcwIDAwOjAwOjAwIEdNVCIsIkNvbnRlbnQtVHlwZSI6InRleHQvcGxhaW4i'
    'fSkpfWZ1bmN0aW9uIHh3KCl7Y29uc3R7bG9jYWxETlM6ZSxhbnRpU2FuY3Rp'
    'b25ETlM6dCxibG9ja01hbHdhcmU6cixibG9ja1BoaXNoaW5nOm4sYmxvY2tD'
    'cnlwdG9taW5lcnM6aSxibG9ja0FkczpzLGJsb2NrUG9ybjpvLGJ5cGFzc0ly'
    'YW46YSxieXBhc3NDaGluYTpjLGJ5cGFzc1J1c3NpYTp1LGJ5cGFzc09wZW5B'
    'aTpsLGJ5cGFzc0dvb2dsZUFpOmQsYnlwYXNzTWljcm9zb2Z0OncsYnlwYXNz'
    'T3JhY2xlOmgsYnlwYXNzRG9ja2VyOmYsYnlwYXNzQWRvYmU6QSxieXBhc3NF'
    'cGljR2FtZXM6cCxieXBhc3NJbnRlbDpFLGJ5cGFzc0FtZDpCLGJ5cGFzc052'
    'aWRpYTpILGJ5cGFzc0FzdXM6bSxieXBhc3NIcDpnLGJ5cGFzc0xlbm92bzp5'
    'fT1nbG9iYWxUaGlzLnNldHRpbmdzO3JldHVyblt7cnVsZTpyLHR5cGU6ImJs'
    'b2NrIixmb3JtYXQ6InRleHQiLGdlb3NpdGU6Im1hbHdhcmUiLGdlb3NpdGVV'
    'Ukw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9DaG9jb2xh'
    'dGU0VS9JcmFuLWNsYXNoLXJ1bGVzL3JlbGVhc2UvbWFsd2FyZS50eHQiLGdl'
    'b2lwOiJtYWx3YXJlLWNpZHIiLGdlb2lwVVJMOiJodHRwczovL3Jhdy5naXRo'
    'dWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJhbi1jbGFzaC1ydWxl'
    'cy9yZWxlYXNlL21hbHdhcmUtaXAudHh0In0se3J1bGU6bix0eXBlOiJibG9j'
    'ayIsZm9ybWF0OiJ0ZXh0IixnZW9zaXRlOiJwaGlzaGluZyIsZ2Vvc2l0ZVVS'
    'TDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0'
    'ZTRVL0lyYW4tY2xhc2gtcnVsZXMvcmVsZWFzZS9waGlzaGluZy50eHQiLGdl'
    'b2lwOiJwaGlzaGluZy1jaWRyIixnZW9pcFVSTDoiaHR0cHM6Ly9yYXcuZ2l0'
    'aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRVL0lyYW4tY2xhc2gtcnVs'
    'ZXMvcmVsZWFzZS9waGlzaGluZy1pcC50eHQifSx7cnVsZTppLHR5cGU6ImJs'
    'b2NrIixmb3JtYXQ6InRleHQiLGdlb3NpdGU6ImNyeXB0b21pbmVycyIsZ2Vv'
    'c2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0No'
    'b2NvbGF0ZTRVL0lyYW4tY2xhc2gtcnVsZXMvcmVsZWFzZS9jcnlwdG9taW5l'
    'cnMudHh0In0se3J1bGU6cyx0eXBlOiJibG9jayIsZm9ybWF0OiJ0ZXh0Iixn'
    'ZW9zaXRlOiJjYXRlZ29yeS1hZHMtYWxsIixnZW9zaXRlVVJMOiJodHRwczov'
    'L3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJhbi1j'
    'bGFzaC1ydWxlcy9yZWxlYXNlL2NhdGVnb3J5LWFkcy1hbGwudHh0In0se3J1'
    'bGU6byx0eXBlOiJibG9jayIsZm9ybWF0OiJ0ZXh0IixnZW9zaXRlOiJuc2Z3'
    'IixnZW9zaXRlVVJMOiJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5j'
    'b20vQ2hvY29sYXRlNFUvSXJhbi1jbGFzaC1ydWxlcy9yZWxlYXNlL25zZncu'
    'dHh0In0se3J1bGU6YSx0eXBlOiJkaXJlY3QiLGRuczplLGZvcm1hdDoidGV4'
    'dCIsZ2Vvc2l0ZToiaXIiLGdlb2lwOiJpci1jaWRyIixnZW9zaXRlVVJMOiJo'
    'dHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUv'
    'SXJhbi1jbGFzaC1ydWxlcy9yZWxlYXNlL2lyLnR4dCIsZ2VvaXBVUkw6Imh0'
    'dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9DaG9jb2xhdGU0VS9J'
    'cmFuLWNsYXNoLXJ1bGVzL3JlbGVhc2UvaXJjaWRyLnR4dCJ9LHtydWxlOmMs'
    'dHlwZToiZGlyZWN0IixkbnM6ZSxmb3JtYXQ6InlhbWwiLGdlb3NpdGU6ImNu'
    'IixnZW9pcDoiY24tY2lkciIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0'
    'aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRhLXJ1bGVzLWRhdC9t'
    'ZXRhL2dlby9nZW9zaXRlL2NuLnlhbWwiLGdlb2lwVVJMOiJodHRwczovL3Jh'
    'dy5naXRodWJ1c2VyY29udGVudC5jb20vTWV0YUN1YmVYL21ldGEtcnVsZXMt'
    'ZGF0L21ldGEvZ2VvL2dlb2lwL2NuLnlhbWwifSx7cnVsZTp1LHR5cGU6ImRp'
    'cmVjdCIsZG5zOmUsZm9ybWF0OiJ5YW1sIixnZW9zaXRlOiJydSIsZ2VvaXA6'
    'InJ1LWNpZHIiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJj'
    'b250ZW50LmNvbS9NZXRhQ3ViZVgvbWV0YS1ydWxlcy1kYXQvbWV0YS9nZW8v'
    'Z2Vvc2l0ZS9jYXRlZ29yeS1ydS55YW1sIixnZW9pcFVSTDoiaHR0cHM6Ly9y'
    'YXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRhLXJ1bGVz'
    'LWRhdC9tZXRhL2dlby9nZW9pcC9ydS55YW1sIn0se3J1bGU6bCx0eXBlOiJk'
    'aXJlY3QiLGRuczp0LGZvcm1hdDoieWFtbCIsZ2Vvc2l0ZToib3BlbmFpIixn'
    'ZW9zaXRlVVJMOiJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20v'
    'TWV0YUN1YmVYL21ldGEtcnVsZXMtZGF0L21ldGEvZ2VvL2dlb3NpdGUvb3Bl'
    'bmFpLnlhbWwifSx7cnVsZTpkLHR5cGU6ImRpcmVjdCIsZG5zOnQsZm9ybWF0'
    'OiJ5YW1sIixnZW9zaXRlOiJnb29nbGVhaSIsZ2Vvc2l0ZVVSTDoiaHR0cHM6'
    'Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRhLXJ1'
    'bGVzLWRhdC9tZXRhL2dlby9nZW9zaXRlL2dvb2dsZS1kZWVwbWluZC55YW1s'
    'In0se3J1bGU6dyx0eXBlOiJkaXJlY3QiLGRuczp0LGZvcm1hdDoieWFtbCIs'
    'Z2Vvc2l0ZToibWljcm9zb2Z0IixnZW9zaXRlVVJMOiJodHRwczovL3Jhdy5n'
    'aXRodWJ1c2VyY29udGVudC5jb20vTWV0YUN1YmVYL21ldGEtcnVsZXMtZGF0'
    'L21ldGEvZ2VvL2dlb3NpdGUvbWljcm9zb2Z0LnlhbWwifSx7cnVsZTpoLHR5'
    'cGU6ImRpcmVjdCIsZG5zOnQsZm9ybWF0OiJ5YW1sIixnZW9zaXRlOiJvcmFj'
    'bGUiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50'
    'LmNvbS9NZXRhQ3ViZVgvbWV0YS1ydWxlcy1kYXQvbWV0YS9nZW8vZ2Vvc2l0'
    'ZS9vcmFjbGUueWFtbCJ9LHtydWxlOmYsdHlwZToiZGlyZWN0IixkbnM6dCxm'
    'b3JtYXQ6InlhbWwiLGdlb3NpdGU6ImRvY2tlciIsZ2Vvc2l0ZVVSTDoiaHR0'
    'cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRh'
    'LXJ1bGVzLWRhdC9tZXRhL2dlby9nZW9zaXRlL2RvY2tlci55YW1sIn0se3J1'
    'bGU6QSx0eXBlOiJkaXJlY3QiLGRuczp0LGZvcm1hdDoieWFtbCIsZ2Vvc2l0'
    'ZToiYWRvYmUiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJj'
    'b250ZW50LmNvbS9NZXRhQ3ViZVgvbWV0YS1ydWxlcy1kYXQvbWV0YS9nZW8v'
    'Z2Vvc2l0ZS9hZG9iZS55YW1sIn0se3J1bGU6cCx0eXBlOiJkaXJlY3QiLGRu'
    'czp0LGZvcm1hdDoieWFtbCIsZ2Vvc2l0ZToiZXBpY2dhbWVzIixnZW9zaXRl'
    'VVJMOiJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vTWV0YUN1'
    'YmVYL21ldGEtcnVsZXMtZGF0L21ldGEvZ2VvL2dlb3NpdGUvZXBpY2dhbWVz'
    'LnlhbWwifSx7cnVsZTpFLHR5cGU6ImRpcmVjdCIsZG5zOnQsZm9ybWF0OiJ5'
    'YW1sIixnZW9zaXRlOiJpbnRlbCIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcu'
    'Z2l0aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRhLXJ1bGVzLWRh'
    'dC9tZXRhL2dlby9nZW9zaXRlL2ludGVsLnlhbWwifSx7cnVsZTpCLHR5cGU6'
    'ImRpcmVjdCIsZG5zOnQsZm9ybWF0OiJ5YW1sIixnZW9zaXRlOiJhbWQiLGdl'
    'b3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9N'
    'ZXRhQ3ViZVgvbWV0YS1ydWxlcy1kYXQvbWV0YS9nZW8vZ2Vvc2l0ZS9hbWQu'
    'eWFtbCJ9LHtydWxlOkgsdHlwZToiZGlyZWN0IixkbnM6dCxmb3JtYXQ6Inlh'
    'bWwiLGdlb3NpdGU6Im52aWRpYSIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcu'
    'Z2l0aHVidXNlcmNvbnRlbnQuY29tL01ldGFDdWJlWC9tZXRhLXJ1bGVzLWRh'
    'dC9tZXRhL2dlby9nZW9zaXRlL252aWRpYS55YW1sIn0se3J1bGU6bSx0eXBl'
    'OiJkaXJlY3QiLGRuczp0LGZvcm1hdDoieWFtbCIsZ2Vvc2l0ZToiYXN1cyIs'
    'Z2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29t'
    'L01ldGFDdWJlWC9tZXRhLXJ1bGVzLWRhdC9tZXRhL2dlby9nZW9zaXRlL2Fz'
    'dXMueWFtbCJ9LHtydWxlOmcsdHlwZToiZGlyZWN0IixkbnM6dCxmb3JtYXQ6'
    'InlhbWwiLGdlb3NpdGU6ImhwIixnZW9zaXRlVVJMOiJodHRwczovL3Jhdy5n'
    'aXRodWJ1c2VyY29udGVudC5jb20vTWV0YUN1YmVYL21ldGEtcnVsZXMtZGF0'
    'L21ldGEvZ2VvL2dlb3NpdGUvaHAueWFtbCJ9LHtydWxlOnksdHlwZToiZGly'
    'ZWN0IixkbnM6dCxmb3JtYXQ6InlhbWwiLGdlb3NpdGU6Imxlbm92byIsZ2Vv'
    'c2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL01l'
    'dGFDdWJlWC9tZXRhLXJ1bGVzLWRhdC9tZXRhL2dlby9nZW9zaXRlL2xlbm92'
    'by55YW1sIn1dLmZpbHRlcigoe3J1bGU6ZX0pPT5lKX1hc3luYyBmdW5jdGlv'
    'biB2dyhlLHQscil7Y29uc3R7bG9jYWxETlM6bixyZW1vdGVETlM6aSx3YXJw'
    'UmVtb3RlRE5TOnMsYW50aVNhbmN0aW9uRE5TOm8sb3V0UHJveHlQYXJhbXM6'
    'YSxyZW1vdGVEbnNIb3N0OmMsZW5hYmxlSVB2Njp1LGZha2VETlM6bCxhbGxv'
    'd0xBTkNvbm5lY3Rpb246ZH09Z2xvYmFsVGhpcy5zZXR0aW5ncyx3PSJsb2Nh'
    'bGhvc3QiPT09bj8ic3lzdGVtIjpgJHtufSNESVJFQ1RgLGg9dm9pZCAwLGY9'
    'dm9pZCAwLEE9YCR7dD9zOml9IyR7dD9g8J+SpiBXYXJwICR7cj8iUHJvICI6'
    'IiJ9LSBCZXN0IFBpbmcg8J+agGA6ZT8i8J+SpiBCZXN0IFBpbmcg8J+agCI6'
    'IuKchSBTZWxlY3RvciJ9YCxwPXt9LEU9e307aWYoZSYmIXQpe2NvbnN0e3Nl'
    'cnZlcjplfT1hO21sKGUpJiYoRVtlXT1BKX1pZihjLmlzRG9tYWluJiYhdCl7'
    'Y29uc3R7aXB2NDplLGlwdjY6dCxob3N0OnJ9PWM7cFtyXT1lLmNvbmNhdElm'
    'KHUsdCl9Y29uc3QgQj12b2lkIDAsSD1ObCh4dygpKSxtPXZvaWQgMDtbLi4u'
    'SC5ibG9jay5nZW9zaXRlcy5tYXAoZT0+YHJ1bGUtc2V0OiR7ZX1gKSwuLi5I'
    'LmJsb2NrLmRvbWFpbnMubWFwKGU9PmArLiR7ZX1gKV0uZm9yRWFjaChlPT5w'
    'W2VdPSJyY29kZTovL3JlZnVzZWQiKTtjb25zdCBnPVsuLi5ILmJ5cGFzcy5h'
    'bnRpU2FuY3Rpb25ETlMuZ2Vvc2l0ZXMubWFwKGU9PmBydWxlLXNldDoke2V9'
    'YCksLi4uSC5ieXBhc3MuYW50aVNhbmN0aW9uRE5TLmRvbWFpbnMubWFwKGU9'
    'PmArLiR7ZX1gKV0seT1bLi4uSC5ieXBhc3MubG9jYWxETlMuZ2Vvc2l0ZUdl'
    'b2lwcy5tYXAoKHtnZW9zaXRlOmV9KT0+YHJ1bGUtc2V0OiR7ZX1gKSwuLi5I'
    'LmJ5cGFzcy5sb2NhbEROUy5nZW9zaXRlcy5tYXAoZT0+YHJ1bGUtc2V0OiR7'
    'ZX1gKSwuLi5ILmJ5cGFzcy5sb2NhbEROUy5kb21haW5zLm1hcChlPT5gKy4k'
    'e2V9YCldO2lmKGcubGVuZ3RoKXtnLmZvckVhY2goZT0+RVtlXT1gJHtvfSNE'
    'SVJFQ1RgKTtjb25zdHtob3N0OmUsaXNIb3N0RG9tYWluOnR9PV9sKG8pO3Qm'
    'JnkucHVzaChlKX15LmZvckVhY2goZT0+RVtlXT13KTtjb25zdCBUPXZvaWQg'
    'MDtsZXQgeD0icmVkaXItaG9zdCIsdj17fTtsJiYoeD0iZmFrZS1pcCIsdj17'
    'ImZha2UtaXAtcmFuZ2UiOiIxOTguMTguMC4xLzE2IiwiZmFrZS1pcC1maWx0'
    'ZXItbW9kZSI6ImJsYWNrbGlzdCIsImZha2UtaXAtZmlsdGVyIjpbIisubGFu'
    'IiwiKy5sb2NhbCJdfSk7Y29uc3QgYj12b2lkIDA7cmV0dXJue2VuYWJsZToh'
    'MCwicmVzcGVjdC1ydWxlcyI6ITAsInVzZS1zeXN0ZW0taG9zdHMiOiExLGxp'
    'c3RlbjooZD8iMC4wLjAuMCI6IjEyNy4wLjAuMSIpKyI6MTA1MyIsaXB2Njp1'
    'LGhvc3RzOnAub21pdEVtcHR5KCksbmFtZXNlcnZlcjpbQV0sInByb3h5LXNl'
    'cnZlci1uYW1lc2VydmVyIjpbd10sImRpcmVjdC1uYW1lc2VydmVyIjpbd10s'
    'ImRpcmVjdC1uYW1lc2VydmVyLWZvbGxvdy1wb2xpY3kiOiEwLCJuYW1lc2Vy'
    'dmVyLXBvbGljeSI6RS5vbWl0RW1wdHkoKSwiZW5oYW5jZWQtbW9kZSI6eCwu'
    'Li52fX1mdW5jdGlvbiBidyhlKXtjb25zdHtibG9ja1VEUDQ0Mzp0fT1nbG9i'
    'YWxUaGlzLnNldHRpbmdzLHI9dm9pZCAwLG49VWwoeHcoKSksaT1bIkdFT0lQ'
    'LGxhbixESVJFQ1Qsbm8tcmVzb2x2ZSJdO3JldHVybiBlP3QmJmkucHVzaCgi'
    'QU5ELCgoTkVUV09SSyx1ZHApLChEU1QtUE9SVCw0NDMpKSxSRUpFQ1QiKTpp'
    'LnB1c2goIk5FVFdPUkssdWRwLFJFSkVDVCIpLFsuLi5pLC4uLm4uYmxvY2su'
    'Z2Vvc2l0ZXMubWFwKGU9PmBSVUxFLVNFVCwke2V9LFJFSkVDVGApLC4uLm4u'
    'YmxvY2suZG9tYWlucy5tYXAoZT0+YERPTUFJTi1TVUZGSVgsJHtlfSxSRUpF'
    'Q1RgKSwuLi5uLmJsb2NrLmdlb2lwcy5tYXAoZT0+YFJVTEUtU0VULCR7ZX0s'
    'UkVKRUNUYCksLi4ubi5ibG9jay5pcHMubWFwKGU9Pmt3KGUsIlJFSkVDVCIp'
    'KSwuLi5uLmJ5cGFzcy5nZW9zaXRlcy5tYXAoZT0+YFJVTEUtU0VULCR7ZX0s'
    'RElSRUNUYCksLi4ubi5ieXBhc3MuZG9tYWlucy5tYXAoZT0+YERPTUFJTi1T'
    'VUZGSVgsJHtlfSxESVJFQ1RgKSwuLi5uLmJ5cGFzcy5nZW9pcHMubWFwKGU9'
    'PmBSVUxFLVNFVCwke2V9LERJUkVDVGApLC4uLm4uYnlwYXNzLmlwcy5tYXAo'
    'ZT0+a3coZSwiRElSRUNUIikpLCJNQVRDSCzinIUgU2VsZWN0b3IiXX1mdW5j'
    'dGlvbiBSdygpe2NvbnN0IGU9dm9pZCAwO3JldHVybiB4dygpLnJlZHVjZSgo'
    'ZSx0KT0+KE13KGUsdCksZSkse30pLm9taXRFbXB0eSgpfWZ1bmN0aW9uIE13'
    'KGUsdCl7Y29uc3R7Z2Vvc2l0ZTpyLGdlb2lwOm4sZ2Vvc2l0ZVVSTDppLGdl'
    'b2lwVVJMOnMsZm9ybWF0Om99PXQsYT0idGV4dCI9PT1vPyJ0eHQiOm8sYz0o'
    'dCxyLG4pPT57ZVt0XT17dHlwZToiaHR0cCIsZm9ybWF0Om8sYmVoYXZpb3I6'
    'cixwYXRoOmAuL3J1bGVzZXQvJHt0fS4ke2F9YCxpbnRlcnZhbDo4NjQwMCx1'
    'cmw6bn19O3ImJmkmJmMociwiZG9tYWluIixpKSxuJiZzJiZjKG4sImlwY2lk'
    'ciIscyl9ZnVuY3Rpb24ga3coZSx0KXtjb25zdCByPShlPUNsKGUpP2UucmVw'
    'bGFjZSgvXFt8XF0vZywiIik6ZSkuaW5jbHVkZXMoIi8iKT8iIjpTbChlKT8i'
    'LzMyIjoiLzEyOCI7cmV0dXJuYElQLUNJRFIsJHtlfSR7cn0sJHt0fWB9ZnVu'
    'Y3Rpb24gU3coZSx0LHIsbixpLHMsbyxhLGMpe3JldHVybntuYW1lOmUsdHlw'
    'ZTp0LHNlcnZlcjpyLnJlcGxhY2UoL1xbfFxdL2csIiIpLHBvcnQ6biwiaXAt'
    'dmVyc2lvbiI6aT8iaXB2NC1wcmVmZXIiOiJpcHY0Iix0Zm86cyx1ZHA6ITEs'
    'Li4uYywuLi5vLC4uLmF9fWZ1bmN0aW9uIEN3KGUsdCxyLG4pe2NvbnN0e2Rp'
    'Y3Q6e19WTF86aSxfVFJfOnN9LGdsb2JhbENvbmZpZzp7dXNlcklEOm8sVHJQ'
    'YXNzOmF9LHNldHRpbmdzOntmaW5nZXJwcmludDpjLGVuYWJsZVRGTzp1LGVu'
    'YWJsZUlQdjY6bCxlbmFibGVFQ0g6ZCxlY2hTZXJ2ZXJOYW1lOncsdXBzdHJl'
    'YW1QYXJhbXM6e3Vwc3RyZWFtU2VydmVyOmh9fX09Z2xvYmFsVGhpcyxmPUxs'
    'KG4pfHxyPT09aDtpZihlPT09cyYmIWYpcmV0dXJuIG51bGw7Y29uc3R7aG9z'
    'dDpBLHNuaTpwLGFsbG93SW5zZWN1cmU6RX09T2wociksQj1mP0x3KGUsInRs'
    'cyIsRSxwLGQsd3x8dm9pZCAwLCJodHRwLzEuMSIsYyk6e30sSD1Jdygid3Mi'
    'LHZvaWQgMCxNbChlKSxBLHZvaWQgMCwyNTYwKTtyZXR1cm4gU3codCxlLHIs'
    'bixsLHUsQixILGU9PT1pP3t1dWlkOm8sInBhY2tldC1lbmNvZGluZyI6IiJ9'
    'OntwYXNzd29yZDphfSl9ZnVuY3Rpb24gX3coZSx0LHIsbixpKXtjb25zdHth'
    'bW5lemlhTm9pc2VDb3VudDpzLGFtbmV6aWFOb2lzZVNpemVNaW46byxhbW5l'
    'emlhTm9pc2VTaXplTWF4OmEsZW5hYmxlSVB2NjpjfT1nbG9iYWxUaGlzLnNl'
    'dHRpbmdzLHtob3N0OnUscG9ydDpsfT1QbChyLCExKSxkPWM/ImlwdjQtcHJl'
    'ZmVyIjoiaXB2NCIse3dhcnBJUHY2OncscmVzZXJ2ZWQ6aCxwdWJsaWNLZXk6'
    'Zixwcml2YXRlS2V5OkF9PWU7cmV0dXJue25hbWU6dCx0eXBlOiJ3aXJlZ3Vh'
    'cmQiLGlwOiIxNzIuMTYuMC4yLzMyIixpcHY2OncsImlwLXZlcnNpb24iOmQs'
    'InByaXZhdGUta2V5IjpBLHNlcnZlcjpuPyIxNjIuMTU5LjE5Mi4xIjp1LHBv'
    'cnQ6bj8yNDA4OmwsInB1YmxpYy1rZXkiOmYsImFsbG93ZWQtaXBzIjpbIjAu'
    'MC4wLjAvMCIsIjo6LzAiXSxyZXNlcnZlZDpoLHVkcDohMCxtdHU6MTI4MCwi'
    'ZGlhbGVyLXByb3h5IjpufHx2b2lkIDAsImFtbmV6aWEtd2ctb3B0aW9uIjpp'
    'P3tqYzpzLGptaW46byxqbWF4OmF9OnZvaWQgMH19ZnVuY3Rpb24gT3coKXtj'
    'b25zdHtkaWN0OntfU1NfOmUsX1ZMXzp0LF9UUl86cixfVk1fOm59LHNldHRp'
    'bmdzOntvdXRQcm94eTppLG91dFByb3h5UGFyYW1zOntwcm90b2NvbDpzLHNl'
    'cnZlcjpvLHBvcnQ6YSx1c2VyOmMscGFzczp1LHBhc3N3b3JkOmwsbWV0aG9k'
    'OmQsdXVpZDp3LGZsb3c6aCxzZWN1cml0eTpmLHR5cGU6QSxzbmk6cCxmcDpF'
    'LGhvc3Q6QixwYXRoOkgsYWxwbjptLHBiazpnLHNpZDp5LGhlYWRlclR5cGU6'
    'VCxzZXJ2aWNlTmFtZTp4LGFpZDp2fX19PWdsb2JhbFRoaXMse3NlYXJjaFBh'
    'cmFtczpifT1uZXcgVVJMKGkpLFI9Yi5nZXQoImVkIiksTT1SPytSOnZvaWQg'
    'MCxrPUx3KHMsZiwhMSxwfHxvLCExLHZvaWQgMCxtLEUsZyx5KSxTPUl3KEEs'
    'VCxILEIseCxNKTtzd2l0Y2gocyl7Y2FzZSJodHRwIjpyZXR1cm4gU3coIiIs'
    'Imh0dHAiLG8sYSwhMSwhMSx7fSx7fSx7dXNlcm5hbWU6YyxwYXNzd29yZDp1'
    'fSk7Y2FzZSJzb2NrcyI6cmV0dXJuIFN3KCIiLCJzb2NrczUiLG8sYSwhMSwh'
    'MSx7fSx7fSx7dXNlcm5hbWU6YyxwYXNzd29yZDp1fSk7Y2FzZSBlOnJldHVy'
    'biBTdygiIiwic3MiLG8sYSwhMSwhMSx7fSx7fSx7Y2lwaGVyOmQscGFzc3dv'
    'cmQ6bH0pO2Nhc2UgdDpyZXR1cm4gU3coIiIsdCxvLGEsITEsITEsayxTLHt1'
    'dWlkOncsZmxvdzpofSk7Y2FzZSBuOnJldHVybiBTdygiIixuLG8sYSwhMSwh'
    'MSxrLFMse3V1aWQ6dyxjaXBoZXI6ImF1dG8iLGFsdGVySWQ6dn0pO2Nhc2Ug'
    'cjppZigibm9uZSI9PT1mKXJldHVybjtyZXR1cm4gU3coIiIscixvLGEsITEs'
    'ITEsayxTLHtwYXNzd29yZDpsfSk7ZGVmYXVsdDpyZXR1cm59fWZ1bmN0aW9u'
    'IFB3KGUsdCxyKXtjb25zdHtiZXN0V2FycEludGVydmFsOm4sYmVzdFZMVFJJ'
    'bnRlcnZhbDppfT1nbG9iYWxUaGlzLnNldHRpbmdzO3JldHVybntuYW1lOmUs'
    'dHlwZToidXJsLXRlc3QiLHByb3hpZXM6dCx1cmw6Imh0dHBzOi8vd3d3Lmdz'
    'dGF0aWMuY29tL2dlbmVyYXRlXzIwNCIsaW50ZXJ2YWw6cj9uOmksdG9sZXJh'
    'bmNlOjUwfX1mdW5jdGlvbiBMdyhlLHQscixuLGkscyxvLGEsYyx1KXtpZigh'
    'WyJ0bHMiLCJyZWFsaXR5Il0uaW5jbHVkZXModCkpcmV0dXJue307Y29uc3R7'
    'X1RSXzpsfT1nbG9iYWxUaGlzLmRpY3QsZD17dGxzOiEwLFtlPT09bD8ic25p'
    'Ijoic2VydmVybmFtZSJdOm4sImNsaWVudC1maW5nZXJwcmludCI6InJhbmRv'
    'bWl6ZWQiPT09YT8icmFuZG9tIjphLCJza2lwLWNlcnQtdmVyaWZ5IjpyfTty'
    'ZXR1cm4idGxzIj09PXQ/ey4uLmQsYWxwbjpvPy5zcGxpdCgiLCIpLCJlY2gt'
    'b3B0cyI6aT97ZW5hYmxlOiEwLCJxdWVyeS1zZXJ2ZXItbmFtZSI6c306dm9p'
    'ZCAwfToicmVhbGl0eSI9PT10JiZjJiZ1P3suLi5kLCJyZWFsaXR5LW9wdHMi'
    'OnsicHVibGljLWtleSI6Yywic2hvcnQtaWQiOnV9fTp7fX1mdW5jdGlvbiBJ'
    'dyhlLHQscj0iLyIsbixpLHMpe3N3aXRjaChyPXI/LnNwbGl0KCI/IilbMF0s'
    'ZSl7Y2FzZSJ0Y3AiOnJldHVybiJodHRwIj09PXQ/e25ldHdvcms6Imh0dHAi'
    'LCJodHRwLW9wdHMiOnttZXRob2Q6IkdFVCIscGF0aDpyLnNwbGl0KCIsIiks'
    'aGVhZGVyczp7SG9zdDpuPy5zcGxpdCgiLCIpLENvbm5lY3Rpb246WyJrZWVw'
    'LWFsaXZlIl0sIkNvbnRlbnQtVHlwZSI6WyJhcHBsaWNhdGlvbi9vY3RldC1z'
    'dHJlYW0iXX19fTp7bmV0d29yazoidGNwIn07Y2FzZSJ3cyI6cmV0dXJue25l'
    'dHdvcms6IndzIiwid3Mtb3B0cyI6e3BhdGg6ciwibWF4LWVhcmx5LWRhdGEi'
    'OnMsImVhcmx5LWRhdGEtaGVhZGVyLW5hbWUiOnM/IlNlYy1XZWJTb2NrZXQt'
    'UHJvdG9jb2wiOnZvaWQgMCxoZWFkZXJzOntIb3N0Om59fX07Y2FzZSJodHRw'
    'dXBncmFkZSI6Y29uc3R7X1YyXzplfT1nbG9iYWxUaGlzLmRpY3Q7cmV0dXJu'
    'e25ldHdvcms6IndzIiwid3Mtb3B0cyI6e1tgJHtlfS1odHRwLXVwZ3JhZGVg'
    'XTohMCxbYCR7ZX0taHR0cC11cGdyYWRlLWZhc3Qtb3BlbmBdOiEwLHBhdGg6'
    'cixoZWFkZXJzOntIb3N0Om59fX07Y2FzZSJncnBjIjpyZXR1cm57bmV0d29y'
    'azoiZ3JwYyIsImdycGMtb3B0cyI6eyJncnBjLXNlcnZpY2UtbmFtZSI6aX19'
    'O2RlZmF1bHQ6cmV0dXJue319fXZhciBEdz17ZW5hYmxlOiEwLHN0YWNrOiJt'
    'aXhlZCIsImF1dG8tcm91dGUiOiEwLCJzdHJpY3Qtcm91dGUiOiEwLCJhdXRv'
    'LWRldGVjdC1pbnRlcmZhY2UiOiEwLCJkbnMtaGlqYWNrIjpbImFueTo1MyIs'
    'InRjcDovL2FueTo1MyJdLG10dTo5ZTN9LFV3PXtlbmFibGU6ITAsImZvcmNl'
    'LWRucy1tYXBwaW5nIjohMCwicGFyc2UtcHVyZS1pcCI6ITAsIm92ZXJyaWRl'
    'LWRlc3RpbmF0aW9uIjohMCxzbmlmZjp7SFRUUDp7cG9ydHM6WzgwLDgwODAs'
    'ODg4MCwyMDUyLDIwODIsMjA4NiwyMDk1XX0sVExTOntwb3J0czpbNDQzLDg0'
    'NDMsMjA1MywyMDgzLDIwODcsMjA5Nl19fX07YXN5bmMgZnVuY3Rpb24gTnco'
    'ZSx0LHIsbixpLHMsbyl7Y29uc3R7bG9nTGV2ZWw6YSxhbGxvd0xBTkNvbm5l'
    'Y3Rpb246Y309Z2xvYmFsVGhpcy5zZXR0aW5ncyx1PXM/e306eyJkaXNhYmxl'
    'LWtlZXAtYWxpdmUiOiExLCJrZWVwLWFsaXZlLWlkbGUiOjEwLCJrZWVwLWFs'
    'aXZlLWludGVydmFsIjoxNSwidGNwLWNvbmN1cnJlbnQiOiEwfSxsPXsibWl4'
    'ZWQtcG9ydCI6Nzg5MCxpcHY2OiEwLCJhbGxvdy1sYW4iOmMsInVuaWZpZWQt'
    'ZGVsYXkiOiExLCJsb2ctbGV2ZWwiOmEucmVwbGFjZSgibm9uZSIsInNpbGVu'
    'dCIpLG1vZGU6InJ1bGUiLC4uLnUsImdlby1hdXRvLXVwZGF0ZSI6ITAsImdl'
    'by11cGRhdGUtaW50ZXJ2YWwiOjE2OCwiZXh0ZXJuYWwtY29udHJvbGxlciI6'
    'IjEyNy4wLjAuMTo5MDkwIiwiZXh0ZXJuYWwtY29udHJvbGxlci1jb3JzIjp7'
    'ImFsbG93LW9yaWdpbnMiOlsiKiJdLCJhbGxvdy1wcml2YXRlLW5ldHdvcmsi'
    'OiEwfSwiZXh0ZXJuYWwtdWkiOiJ1aSIsImV4dGVybmFsLXVpLXVybCI6Imh0'
    'dHBzOi8vZ2l0aHViLmNvbS9NZXRhQ3ViZVgvbWV0YWN1YmV4ZC9hcmNoaXZl'
    'L3JlZnMvaGVhZHMvZ2gtcGFnZXMuemlwIixwcm9maWxlOnsic3RvcmUtc2Vs'
    'ZWN0ZWQiOiEwLCJzdG9yZS1mYWtlLWlwIjohMH0sZG5zOmF3YWl0IHZ3KGks'
    'cyxvKSx0dW46RHcsc25pZmZlcjpVdyxwcm94aWVzOmUsInByb3h5LWdyb3Vw'
    'cyI6W3tuYW1lOiLinIUgU2VsZWN0b3IiLHR5cGU6InNlbGVjdCIscHJveGll'
    'czp0fV0sInJ1bGUtcHJvdmlkZXJzIjpSdygpLHJ1bGVzOmJ3KHMpLG50cDp7'
    'ZW5hYmxlOiEwLHNlcnZlcjoidGltZS5jbG91ZGZsYXJlLmNvbSIscG9ydDox'
    'MjMsaW50ZXJ2YWw6MzB9fSxkPXZvaWQgMCx3PVB3KHM/YPCfkqYgV2FycCAk'
    'e28/IlBybyAiOiIifS0gQmVzdCBQaW5nIPCfmoBgOiLwn5KmIEJlc3QgUGlu'
    'ZyDwn5qAIixyLHMpO3JldHVybiBsWyJwcm94eS1ncm91cHMiXS5wdXNoKHcp'
    'LHMmJmxbInByb3h5LWdyb3VwcyJdLnB1c2goUHcoYPCfkqYgV29XICR7bz8i'
    'UHJvICI6IiJ9LSBCZXN0IFBpbmcg8J+agGAsbixzKSksaSYmbFsicHJveHkt'
    'Z3JvdXBzIl0ucHVzaChQdygi8J+SpiDwn5SXIEJlc3QgUGluZyDwn5qAIixu'
    'LHMpKSxsfWFzeW5jIGZ1bmN0aW9uIHp3KCl7Y29uc3R7b3V0UHJveHk6ZSxw'
    'b3J0czp0LHVwc3RyZWFtUGFyYW1zOnt1cHN0cmVhbVNlcnZlcjpyLHVwc3Ry'
    'ZWFtUG9ydDpufX09Z2xvYmFsVGhpcy5zZXR0aW5ncyxpPWU/T3coKTp2b2lk'
    'IDAscz0hIWksbz1hd2FpdCB4bCghMSksYT1UbCgpO3ImJm4mJih0LnVuc2hp'
    'ZnQobiksby51bnNoaWZ0KHIpKTtjb25zdCBjPVtdLHU9W10sbD1bXSxkPVsi'
    '8J+SpiBCZXN0IFBpbmcg8J+agCJdLmNvbmNhdElmKHMsIvCfkqYg8J+UlyBC'
    'ZXN0IFBpbmcg8J+agCIpO2Zvcihjb25zdCBlIG9mIGEpe2xldCBhPTE7Zm9y'
    'KGNvbnN0IHcgb2YgdClmb3IoY29uc3QgdCBvZiBvKXtpZih3PT09biE9KHQ9'
    'PT1yKSljb250aW51ZTtjb25zdCBvPXZsKGEsdyx0LGUsITEsITEpLGg9Q3co'
    'ZSxvLHQsdyk7aWYoaCl7aWYoYy5wdXNoKG8pLGQucHVzaChvKSxsLnB1c2go'
    'aCkscyl7Y29uc3Qgcj12bChhLHcsdCxlLCExLCEwKTtsZXQgbj1zdHJ1Y3R1'
    'cmVkQ2xvbmUoaSk7bi5uYW1lPXIsblsiZGlhbGVyLXByb3h5Il09byxsLnB1'
    'c2gobiksdS5wdXNoKHIpLGQucHVzaChyKX1hKyt9fX1jb25zdCB3PWF3YWl0'
    'IE53KGwsZCxjLHUscywhMSwhMSk7cmV0dXJuIG5ldyBSZXNwb25zZShKU09O'
    'LnN0cmluZ2lmeSh3LG51bGwsNCkse3N0YXR1czoyMDAsaGVhZGVyczp7IkNv'
    'bnRlbnQtVHlwZSI6InRleHQvcGxhaW47Y2hhcnNldD11dGYtOCIsIkNhY2hl'
    'LUNvbnRyb2wiOiJuby1zdG9yZSIsIkNETi1DYWNoZS1Db250cm9sIjoibm8t'
    'c3RvcmUifX0pfWFzeW5jIGZ1bmN0aW9uIFh3KGUsdCxyKXtjb25zdHt3YXJw'
    'RW5kcG9pbnRzOm59PWdsb2JhbFRoaXMuc2V0dGluZ3Mse3dhcnBBY2NvdW50'
    'czppfT1hd2FpdCBYbChlLHQpLHM9W10sbz1bXSxhPVtdLGM9cj8iUHJvICI6'
    'IiIsdT1bYPCfkqYgV2FycCAke2N9LSBCZXN0IFBpbmcg8J+agGAsYPCfkqYg'
    'V29XICR7Y30tIEJlc3QgUGluZyDwn5qAYF07bi5mb3JFYWNoKChlLHQpPT57'
    'Y29uc3Qgbj1g8J+SpiAke3QrMX0gLSBXYXJwICR7Y33wn4eu8J+Ht2A7cy5w'
    'dXNoKG4pO2NvbnN0IGw9YPCfkqYgJHt0KzF9IC0gV29XICR7Y33wn4yNYDtv'
    'LnB1c2gobCksdS5wdXNoKG4sbCk7Y29uc3QgZD1fdyhpWzBdLG4sZSwiIixy'
    'KSx3PV93KGlbMV0sbCxlLG4sITEpO2EucHVzaChkLHcpfSk7Y29uc3QgbD1h'
    'd2FpdCBOdyhhLHUscyxvLCExLCEwLHIpO3JldHVybiBuZXcgUmVzcG9uc2Uo'
    'SlNPTi5zdHJpbmdpZnkobCxudWxsLDQpLHtzdGF0dXM6MjAwLGhlYWRlcnM6'
    'eyJDb250ZW50LVR5cGUiOiJ0ZXh0L3BsYWluO2NoYXJzZXQ9dXRmLTgiLCJD'
    'YWNoZS1Db250cm9sIjoibm8tc3RvcmUiLCJDRE4tQ2FjaGUtQ29udHJvbCI6'
    'Im5vLXN0b3JlIn19KX1mdW5jdGlvbiBGdygpe2NvbnN0e2xvY2FsRE5TOmUs'
    'YW50aVNhbmN0aW9uRE5TOnQsYmxvY2tNYWx3YXJlOnIsYmxvY2tQaGlzaGlu'
    'ZzpuLGJsb2NrQ3J5cHRvbWluZXJzOmksYmxvY2tBZHM6cyxibG9ja1Bvcm46'
    'byxieXBhc3NJcmFuOmEsYnlwYXNzQ2hpbmE6YyxieXBhc3NSdXNzaWE6dSxi'
    'eXBhc3NPcGVuQWk6bCxieXBhc3NHb29nbGVBaTpkLGJ5cGFzc01pY3Jvc29m'
    'dDp3LGJ5cGFzc09yYWNsZTpoLGJ5cGFzc0RvY2tlcjpmLGJ5cGFzc0Fkb2Jl'
    'OkEsYnlwYXNzRXBpY0dhbWVzOnAsYnlwYXNzSW50ZWw6RSxieXBhc3NBbWQ6'
    'QixieXBhc3NOdmlkaWE6SCxieXBhc3NBc3VzOm0sYnlwYXNzSHA6ZyxieXBh'
    'c3NMZW5vdm86eX09Z2xvYmFsVGhpcy5zZXR0aW5ncztyZXR1cm5be3J1bGU6'
    'cix0eXBlOiJibG9jayIsZ2Vvc2l0ZToiZ2Vvc2l0ZS1tYWx3YXJlIixnZW9p'
    'cDoiZ2VvaXAtbWFsd2FyZSIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0'
    'aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRVL0lyYW4tc2luZy1ib3gt'
    'cnVsZXMvcnVsZS1zZXQvZ2Vvc2l0ZS1tYWx3YXJlLnNycyIsZ2VvaXBVUkw6'
    'Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9DaG9jb2xhdGU0'
    'VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0L2dlb2lwLW1hbHdhcmUu'
    'c3JzIn0se3J1bGU6bix0eXBlOiJibG9jayIsZ2Vvc2l0ZToiZ2Vvc2l0ZS1w'
    'aGlzaGluZyIsZ2VvaXA6Imdlb2lwLXBoaXNoaW5nIixnZW9zaXRlVVJMOiJo'
    'dHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUv'
    'SXJhbi1zaW5nLWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRlLXBoaXNoaW5n'
    'LnNycyIsZ2VvaXBVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50'
    'LmNvbS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0'
    'L2dlb2lwLXBoaXNoaW5nLnNycyJ9LHtydWxlOmksdHlwZToiYmxvY2siLGdl'
    'b3NpdGU6Imdlb3NpdGUtY3J5cHRvbWluZXJzIixnZW9zaXRlVVJMOiJodHRw'
    'czovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJh'
    'bi1zaW5nLWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRlLWNyeXB0b21pbmVy'
    'cy5zcnMifSx7cnVsZTpzLHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9zaXRl'
    'LWNhdGVnb3J5LWFkcy1hbGwiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3Lmdp'
    'dGh1YnVzZXJjb250ZW50LmNvbS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94'
    'LXJ1bGVzL3J1bGUtc2V0L2dlb3NpdGUtY2F0ZWdvcnktYWRzLWFsbC5zcnMi'
    'fSx7cnVsZTpvLHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9zaXRlLW5zZnci'
    'LGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNv'
    'bS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0L2dl'
    'b3NpdGUtbnNmdy5zcnMifSx7cnVsZTphLHR5cGU6ImRpcmVjdCIsZG5zOmUs'
    'Z2Vvc2l0ZToiZ2Vvc2l0ZS1pciIsZ2VvaXA6Imdlb2lwLWlyIixnZW9zaXRl'
    'VVJMOiJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29s'
    'YXRlNFUvSXJhbi1zaW5nLWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRlLWly'
    'LnNycyIsZ2VvaXBVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50'
    'LmNvbS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0'
    'L2dlb2lwLWlyLnNycyJ9LHtydWxlOmMsdHlwZToiZGlyZWN0IixkbnM6ZSxn'
    'ZW9zaXRlOiJnZW9zaXRlLWNuIixnZW9pcDoiZ2VvaXAtY24iLGdlb3NpdGVV'
    'Ukw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9DaG9jb2xh'
    'dGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0L2dlb3NpdGUtY24u'
    'c3JzIixnZW9pcFVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQu'
    'Y29tL0Nob2NvbGF0ZTRVL0lyYW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQv'
    'Z2VvaXAtY24uc3JzIn0se3J1bGU6dSx0eXBlOiJkaXJlY3QiLGRuczplLGdl'
    'b3NpdGU6Imdlb3NpdGUtY2F0ZWdvcnktcnUiLGdlb2lwOiJnZW9pcC1ydSIs'
    'Z2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29t'
    'L0Nob2NvbGF0ZTRVL0lyYW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vv'
    'c2l0ZS1jYXRlZ29yeS1ydS5zcnMiLGdlb2lwVVJMOiJodHRwczovL3Jhdy5n'
    'aXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJhbi1zaW5nLWJv'
    'eC1ydWxlcy9ydWxlLXNldC9nZW9pcC1ydS5zcnMifSx7cnVsZTpsLHR5cGU6'
    'ImRpcmVjdCIsZG5zOnQsZ2Vvc2l0ZToiZ2Vvc2l0ZS1vcGVuYWkiLGdlb3Np'
    'dGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9DaG9j'
    'b2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0L2dlb3NpdGUt'
    'b3BlbmFpLnNycyJ9LHtydWxlOmQsdHlwZToiZGlyZWN0IixkbnM6dCxnZW9z'
    'aXRlOiJnZW9zaXRlLWdvb2dsZS1kZWVwbWluZCIsZ2Vvc2l0ZVVSTDoiaHR0'
    'cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRVL0ly'
    'YW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vvc2l0ZS1nb29nbGUtZGVl'
    'cG1pbmQuc3JzIn0se3J1bGU6dyx0eXBlOiJkaXJlY3QiLGRuczp0LGdlb3Np'
    'dGU6Imdlb3NpdGUtbWljcm9zb2Z0IixnZW9zaXRlVVJMOiJodHRwczovL3Jh'
    'dy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJhbi1zaW5n'
    'LWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRlLW1pY3Jvc29mdC5zcnMifSx7'
    'cnVsZTpoLHR5cGU6ImRpcmVjdCIsZG5zOnQsZ2Vvc2l0ZToiZ2Vvc2l0ZS1v'
    'cmFjbGUiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250'
    'ZW50LmNvbS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUt'
    'c2V0L2dlb3NpdGUtb3JhY2xlLnNycyJ9LHtydWxlOmYsdHlwZToiZGlyZWN0'
    'IixkbnM6dCxnZW9zaXRlOiJnZW9zaXRlLWRvY2tlciIsZ2Vvc2l0ZVVSTDoi'
    'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRV'
    'L0lyYW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vvc2l0ZS1kb2NrZXIu'
    'c3JzIn0se3J1bGU6QSx0eXBlOiJkaXJlY3QiLGRuczp0LGdlb3NpdGU6Imdl'
    'b3NpdGUtYWRvYmUiLGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVz'
    'ZXJjb250ZW50LmNvbS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVz'
    'L3J1bGUtc2V0L2dlb3NpdGUtYWRvYmUuc3JzIn0se3J1bGU6cCx0eXBlOiJk'
    'aXJlY3QiLGRuczp0LGdlb3NpdGU6Imdlb3NpdGUtZXBpY2dhbWVzIixnZW9z'
    'aXRlVVJMOiJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hv'
    'Y29sYXRlNFUvSXJhbi1zaW5nLWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRl'
    'LWVwaWNnYW1lcy5zcnMifSx7cnVsZTpFLHR5cGU6ImRpcmVjdCIsZG5zOnQs'
    'Z2Vvc2l0ZToiZ2Vvc2l0ZS1pbnRlbCIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9y'
    'YXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRVL0lyYW4tc2lu'
    'Zy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vvc2l0ZS1pbnRlbC5zcnMifSx7cnVs'
    'ZTpCLHR5cGU6ImRpcmVjdCIsZG5zOnQsZ2Vvc2l0ZToiZ2Vvc2l0ZS1hbWQi'
    'LGdlb3NpdGVVUkw6Imh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNv'
    'bS9DaG9jb2xhdGU0VS9JcmFuLXNpbmctYm94LXJ1bGVzL3J1bGUtc2V0L2dl'
    'b3NpdGUtYW1kLnNycyJ9LHtydWxlOkgsdHlwZToiZGlyZWN0IixkbnM6dCxn'
    'ZW9zaXRlOiJnZW9zaXRlLW52aWRpYSIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9y'
    'YXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Nob2NvbGF0ZTRVL0lyYW4tc2lu'
    'Zy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vvc2l0ZS1udmlkaWEuc3JzIn0se3J1'
    'bGU6bSx0eXBlOiJkaXJlY3QiLGRuczp0LGdlb3NpdGU6Imdlb3NpdGUtYXN1'
    'cyIsZ2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQu'
    'Y29tL0Nob2NvbGF0ZTRVL0lyYW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQv'
    'Z2Vvc2l0ZS1hc3VzLnNycyJ9LHtydWxlOmcsdHlwZToiZGlyZWN0IixkbnM6'
    'dCxnZW9zaXRlOiJnZW9zaXRlLWhwIixnZW9zaXRlVVJMOiJodHRwczovL3Jh'
    'dy5naXRodWJ1c2VyY29udGVudC5jb20vQ2hvY29sYXRlNFUvSXJhbi1zaW5n'
    'LWJveC1ydWxlcy9ydWxlLXNldC9nZW9zaXRlLWhwLnNycyJ9LHtydWxlOnks'
    'dHlwZToiZGlyZWN0IixkbnM6dCxnZW9zaXRlOiJnZW9zaXRlLWxlbm92byIs'
    'Z2Vvc2l0ZVVSTDoiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29t'
    'L0Nob2NvbGF0ZTRVL0lyYW4tc2luZy1ib3gtcnVsZXMvcnVsZS1zZXQvZ2Vv'
    'c2l0ZS1sZW5vdm8uc3JzIn1dLmZpbHRlcigoe3J1bGU6ZX0pPT5lKX1hc3lu'
    'YyBmdW5jdGlvbiBqdyhlLHQpe2NvbnN0e2xvY2FsRE5TOnIscmVtb3RlRE5T'
    'Om4sd2FycFJlbW90ZUROUzppLGFudGlTYW5jdGlvbkROUzpzLG91dFByb3h5'
    'UGFyYW1zOm8scmVtb3RlRG5zSG9zdDphLGVuYWJsZUlQdjY6YyxmYWtlRE5T'
    'OnUsZW5hYmxlRUNIOmwsZWNoU2VydmVyTmFtZTpkfT1nbG9iYWxUaGlzLnNl'
    'dHRpbmdzLHc9dm9pZCAwLGg9bmV3IFVSTChuKS5wcm90b2NvbC5yZXBsYWNl'
    'KCI6IiwiIiksZj1be3R5cGU6ZT8idWRwIjpoLHNlcnZlcjplP2k6YS5ob3N0'
    'LGRldG91cjplPyLwn5KmIFdhcnAgLSBCZXN0IFBpbmcg8J+agCI6dD8i8J+S'
    'piBCZXN0IFBpbmcg8J+agCI6IuKchSBTZWxlY3RvciIsdGFnOiJkbnMtcmVt'
    'b3RlIn1dOyJsb2NhbGhvc3QiPT09cj9XdyhmLCJsb2NhbCIsImRucy1kaXJl'
    'Y3QiLHZvaWQgMCx2b2lkIDAsdm9pZCAwKTpXdyhmLCJ1ZHAiLCJkbnMtZGly'
    'ZWN0IixyLHZvaWQgMCx2b2lkIDApO2NvbnN0IEE9W3tjbGFzaF9tb2RlOiJE'
    'aXJlY3QiLHNlcnZlcjoiZG5zLWRpcmVjdCJ9LHtjbGFzaF9tb2RlOiJHbG9i'
    'YWwiLHNlcnZlcjoiZG5zLXJlbW90ZSJ9XTtpZihsKXtjb25zdHtob3N0TmFt'
    'ZTplfT1nbG9iYWxUaGlzLmh0dHBDb25maWc7SncoQSwiZG5zLWRpcmVjdCIs'
    'dm9pZCAwLHZvaWQgMCx2b2lkIDAsW2R8fGVdLFsiSFRUUFMiXSl9aWYodCYm'
    'IWUpe2NvbnN0e3NlcnZlcjplfT1vO21sKGUpJiZBLnB1c2goe2RvbWFpbjpl'
    'LHNlcnZlcjoiZG5zLXJlbW90ZSJ9KX1pZihhLmlzRG9tYWluJiYhZSl7Y29u'
    'c3R7aXB2NDplLGlwdjY6dCxob3N0OnJ9PWEsbj12b2lkIDA7V3coZiwiaG9z'
    'dHMiLCJob3N0cyIsdm9pZCAwLHZvaWQgMCx2b2lkIDAscixlLmNvbmNhdElm'
    'KGMsdCkpLEEudW5zaGlmdCh7aXBfYWNjZXB0X2FueTohMCxzZXJ2ZXI6Imhv'
    'c3RzIn0pfWNvbnN0IHA9dm9pZCAwLEU9TmwoRncoKSksQj12b2lkIDA7Wy4u'
    'LkUuYmxvY2suZ2Vvc2l0ZXMsLi4uRS5ibG9jay5kb21haW5zXS5sZW5ndGgm'
    'Jkp3KEEsInJlamVjdCIsdm9pZCAwLEUuYmxvY2suZ2Vvc2l0ZXMsdm9pZCAw'
    'LEUuYmxvY2suZG9tYWlucyksRS5ieXBhc3MubG9jYWxETlMuZ2Vvc2l0ZUdl'
    'b2lwcy5mb3JFYWNoKCh7Z2Vvc2l0ZTplLGdlb2lwOnR9KT0+e0p3KEEsImRu'
    'cy1kaXJlY3QiLHZvaWQgMCxbZV0sdCx2b2lkIDApfSk7Y29uc3QgSD12b2lk'
    'IDA7Wy4uLkUuYnlwYXNzLmxvY2FsRE5TLmdlb3NpdGVzLC4uLkUuYnlwYXNz'
    'LmxvY2FsRE5TLmRvbWFpbnNdLmxlbmd0aCYmSncoQSwiZG5zLWRpcmVjdCIs'
    'dm9pZCAwLEUuYnlwYXNzLmxvY2FsRE5TLmdlb3NpdGVzLHZvaWQgMCxFLmJ5'
    'cGFzcy5sb2NhbEROUy5kb21haW5zKTtjb25zdCBtPXZvaWQgMDtpZihbLi4u'
    'RS5ieXBhc3MuYW50aVNhbmN0aW9uRE5TLmdlb3NpdGVzLC4uLkUuYnlwYXNz'
    'LmFudGlTYW5jdGlvbkROUy5kb21haW5zXS5sZW5ndGgpe2NvbnN0IGU9X2wo'
    'cyk7SncoQSwiZG5zLWFudGktc2FuY3Rpb24iLHZvaWQgMCxFLmJ5cGFzcy5h'
    'bnRpU2FuY3Rpb25ETlMuZ2Vvc2l0ZXMsdm9pZCAwLEUuYnlwYXNzLmFudGlT'
    'YW5jdGlvbkROUy5kb21haW5zKSxlLmlzSG9zdERvbWFpbj9XdyhmLCJodHRw'
    'cyIsImRucy1hbnRpLXNhbmN0aW9uIixlLmhvc3Qsdm9pZCAwLCJkbnMtZGly'
    'ZWN0Iik6V3coZiwidWRwIiwiZG5zLWFudGktc2FuY3Rpb24iLHMsdm9pZCAw'
    'LHZvaWQgMCl9cmV0dXJuIHUmJihXdyhmLCJmYWtlaXAiLCJkbnMtZmFrZSIs'
    'dm9pZCAwLHZvaWQgMCx2b2lkIDAsdm9pZCAwLHZvaWQgMCwiMTk4LjE4LjAu'
    'MC8xNSIsYz8iZmMwMDo6LzE4Ijp2b2lkIDApLEp3KEEsImRucy1mYWtlIiwi'
    'dHVuLWluIix2b2lkIDAsdm9pZCAwLHZvaWQgMCxbIkEiLCJBQUFBIl0pKSx7'
    'c2VydmVyczpmLHJ1bGVzOkEsc3RyYXRlZ3k6Yz8icHJlZmVyX2lwdjQiOiJp'
    'cHY0X29ubHkiLGluZGVwZW5kZW50X2NhY2hlOiEwfX1mdW5jdGlvbiBXdyhl'
    'LHQscixuLGkscyxvLGEsYyx1KXtlLnB1c2goe3R5cGU6dCxzZXJ2ZXI6bixk'
    'ZXRvdXI6aSxkb21haW5fcmVzb2x2ZXI6cz97c2VydmVyOnMsc3RyYXRlZ3k6'
    'ImlwdjRfb25seSJ9OnZvaWQgMCxwcmVkZWZpbmVkOm8/e1tvXTphfTp2b2lk'
    'IDAsaW5ldDRfcmFuZ2U6YyxpbmV0Nl9yYW5nZTp1LHRhZzpyfSl9ZnVuY3Rp'
    'b24gSncoZSx0LHIsbixpLHMsbyl7Y29uc3QgYT1uJiZpO2UucHVzaCh7aW5i'
    'b3VuZDpyLHR5cGU6YT8ibG9naWNhbCI6dm9pZCAwLG1vZGU6YT8iYW5kIjp2'
    'b2lkIDAscnVsZXM6YT9be3J1bGVfc2V0Om59LHtydWxlX3NldDppfV06dm9p'
    'ZCAwLHJ1bGVfc2V0Om4/Lmxlbmd0aCYmIWk/bjp2b2lkIDAsZG9tYWluX3N1'
    'ZmZpeDpzPy5vbWl0RW1wdHkoKSxxdWVyeV90eXBlOm8sYWN0aW9uOiJyZWpl'
    'Y3QiPT09dD8icmVqZWN0Ijoicm91dGUiLHNlcnZlcjoicmVqZWN0Ij09PXQ/'
    'dm9pZCAwOnR9KX1mdW5jdGlvbiBLdyhlKXtjb25zdHtibG9ja1VEUDQ0Mzp0'
    'LGVuYWJsZUlQdjY6cn09Z2xvYmFsVGhpcy5zZXR0aW5ncyxuPVt7aXBfY2lk'
    'cjoiMTcyLjE5LjAuMiIsYWN0aW9uOiJoaWphY2stZG5zIn0se2NsYXNoX21v'
    'ZGU6IkRpcmVjdCIsb3V0Ym91bmQ6ImRpcmVjdCJ9LHtjbGFzaF9tb2RlOiJH'
    'bG9iYWwiLG91dGJvdW5kOiLinIUgU2VsZWN0b3IifSx7YWN0aW9uOiJzbmlm'
    'ZiJ9LHtwcm90b2NvbDoiZG5zIixhY3Rpb246ImhpamFjay1kbnMifSx7aXBf'
    'aXNfcHJpdmF0ZTohMCxvdXRib3VuZDoiZGlyZWN0In1dO2U/dCYmVncobiwi'
    'cmVqZWN0Iix2b2lkIDAsdm9pZCAwLHZvaWQgMCx2b2lkIDAsInVkcCIsInF1'
    'aWMiLDQ0Myk6VncobiwicmVqZWN0Iix2b2lkIDAsdm9pZCAwLHZvaWQgMCx2'
    'b2lkIDAsInVkcCIpO2NvbnN0IGk9RncoKSxzPVVsKGkpLG89dm9pZCAwO1su'
    'Li5zLmJsb2NrLmdlb3NpdGVzLC4uLnMuYmxvY2suZG9tYWluc10ubGVuZ3Ro'
    'JiZWdyhuLCJyZWplY3QiLHMuYmxvY2suZG9tYWlucyx2b2lkIDAscy5ibG9j'
    'ay5nZW9zaXRlcyk7Y29uc3QgYT12b2lkIDA7Wy4uLnMuYmxvY2suZ2VvaXBz'
    'LC4uLnMuYmxvY2suaXBzXS5sZW5ndGgmJlZ3KG4sInJlamVjdCIsdm9pZCAw'
    'LHMuYmxvY2suaXBzLHZvaWQgMCxzLmJsb2NrLmdlb2lwcyk7Y29uc3QgYz12'
    'b2lkIDA7Wy4uLnMuYnlwYXNzLmdlb3NpdGVzLC4uLnMuYnlwYXNzLmRvbWFp'
    'bnNdLmxlbmd0aCYmVncobiwiZGlyZWN0IixzLmJ5cGFzcy5kb21haW5zLHZv'
    'aWQgMCxzLmJ5cGFzcy5nZW9zaXRlcyk7Y29uc3QgdT12b2lkIDA7Wy4uLnMu'
    'YnlwYXNzLmdlb2lwcywuLi5zLmJ5cGFzcy5pcHNdLmxlbmd0aCYmVncobiwi'
    'ZGlyZWN0Iix2b2lkIDAscy5ieXBhc3MuaXBzLHZvaWQgMCxzLmJ5cGFzcy5n'
    'ZW9pcHMpO2NvbnN0IGw9cj8icHJlZmVyX2lwdjQiOiJpcHY0X29ubHkiLGQ9'
    'dm9pZCAwO3JldHVybntydWxlczpuLHJ1bGVfc2V0OmkucmVkdWNlKChlLHQp'
    'PT4oWXcoZSx0KSxlKSxbXSkub21pdEVtcHR5KCksYXV0b19kZXRlY3RfaW50'
    'ZXJmYWNlOiEwLGRlZmF1bHRfZG9tYWluX3Jlc29sdmVyOntzZXJ2ZXI6ImRu'
    'cy1kaXJlY3QiLHN0cmF0ZWd5OmwscmV3cml0ZV90dGw6NjB9LGZpbmFsOiLi'
    'nIUgU2VsZWN0b3IifX1mdW5jdGlvbiBWdyhlLHQscixuLGkscyxvLGEsYyl7'
    'ZS5wdXNoKHtydWxlX3NldDppfHxzLGRvbWFpbl9zdWZmaXg6cj8ubGVuZ3Ro'
    'P3I6dm9pZCAwLGlwX2NpZHI6bj8ubGVuZ3RoP246dm9pZCAwLG5ldHdvcms6'
    'byxwcm90b2NvbDphLHBvcnQ6YyxhY3Rpb246InJlamVjdCI9PT10PyJyZWpl'
    'Y3QiOiJyb3V0ZSIsb3V0Ym91bmQ6ImRpcmVjdCI9PT10PyJkaXJlY3QiOnZv'
    'aWQgMH0pfWZ1bmN0aW9uIFl3KGUsdCl7Y29uc3R7Z2Vvc2l0ZTpyLGdlb3Np'
    'dGVVUkw6bixnZW9pcDppLGdlb2lwVVJMOnN9PXQsbz0odCxyKT0+ZS5wdXNo'
    'KHt0eXBlOiJyZW1vdGUiLHRhZzp0LGZvcm1hdDoiYmluYXJ5Iix1cmw6cixk'
    'b3dubG9hZF9kZXRvdXI6ImRpcmVjdCJ9KTtyJiZuJiZvKHIsbiksaSYmcyYm'
    'byhpLHMpfWZ1bmN0aW9uIFp3KGUsdCxyLG4saSxzLG8sYSl7cmV0dXJue3Rh'
    'ZzplLHR5cGU6dCxzZXJ2ZXI6cixzZXJ2ZXJfcG9ydDpuLHRjcF9mYXN0X29w'
    'ZW46aSwuLi5zLHRsczpvLHRyYW5zcG9ydDphfX1mdW5jdGlvbiBHdyhlLHQs'
    'cixuLGkpe2NvbnN0e2RpY3Q6e19WTF86c30sZ2xvYmFsQ29uZmlnOnt1c2Vy'
    'SUQ6byxUclBhc3M6YX0sc2V0dGluZ3M6e2ZpbmdlcnByaW50OmMsZW5hYmxl'
    'VEZPOnUsZW5hYmxlRUNIOmwsZWNoU2VydmVyTmFtZTpkLHVwc3RyZWFtUGFy'
    'YW1zOnt1cHN0cmVhbVNlcnZlcjp3fX19PWdsb2JhbFRoaXMse2hvc3Q6aCxz'
    'bmk6ZixhbGxvd0luc2VjdXJlOkF9PU9sKHIpLHA9dGgoIndzIiwibm9uZSIs'
    'TWwoZSksaCx2b2lkIDAsMjU2MCksRT1MbChuKXx8cj09PXc/ZWgoInRscyIs'
    'aSxBLGYsbCYmIWksZHx8dm9pZCAwLCJodHRwLzEuMSIsYyk6dm9pZCAwO3Jl'
    'dHVybiBadyh0LGUscixuLHUsZT09PXM/e3V1aWQ6byxwYWNrZXRfZW5jb2Rp'
    'bmc6IiIsbmV0d29yazoidGNwIn06e3Bhc3N3b3JkOmEsbmV0d29yazoidGNw'
    'In0sRSxwKX1mdW5jdGlvbiBRdyhlLHQscixuKXtjb25zdHtob3N0OmkscG9y'
    'dDpzfT1QbChyLCExKSx7d2FycElQdjY6byxyZXNlcnZlZDphLHB1YmxpY0tl'
    'eTpjLHByaXZhdGVLZXk6dX09ZTtyZXR1cm57dGFnOnQsZGV0b3VyOm58fHZv'
    'aWQgMCx0eXBlOiJ3aXJlZ3VhcmQiLGFkZHJlc3M6WyIxNzIuMTYuMC4yLzMy'
    'IixvXSxtdHU6MTI4MCxwZWVyczpbe2FkZHJlc3M6bj8iMTYyLjE1OS4xOTIu'
    'MSI6aSxwb3J0Om4/MjQwODpzLHB1YmxpY19rZXk6YyxyZXNlcnZlZDprbChh'
    'KSxhbGxvd2VkX2lwczpbIjAuMC4wLjAvMCIsIjo6LzAiXSxwZXJzaXN0ZW50'
    'X2tlZXBhbGl2ZV9pbnRlcnZhbDo1fV0scHJpdmF0ZV9rZXk6dX19ZnVuY3Rp'
    'b24gcXcoKXtjb25zdHtkaWN0OntfVkxfOmUsX1RSXzp0LF9TU186cixfVk1f'
    'Om59LHNldHRpbmdzOntvdXRQcm94eTppLG91dFByb3h5UGFyYW1zOntwcm90'
    'b2NvbDpzLHNlcnZlcjpvLHBvcnQ6YSx1c2VyOmMscGFzczp1LHBhc3N3b3Jk'
    'OmwsbWV0aG9kOmQsdXVpZDp3LGZsb3c6aCxzZWN1cml0eTpmLHR5cGU6QSxz'
    'bmk6cCxmcDpFLGhvc3Q6QixwYXRoOkgsYWxwbjptLHBiazpnLHNpZDp5LGhl'
    'YWRlclR5cGU6VCxzZXJ2aWNlTmFtZTp4LGFpZDp2fX19PWdsb2JhbFRoaXMs'
    'e3NlYXJjaFBhcmFtczpifT1uZXcgVVJMKGkpLFI9Yi5nZXQoImVkIiksTT1S'
    'PytSOnZvaWQgMCxrPWVoKGYsITEsITEscHx8bywhMSx2b2lkIDAsbSxFLGcs'
    'eSksUz10aChBLFQsSCxCLHgsTSk7c3dpdGNoKHMpe2Nhc2UiaHR0cCI6cmV0'
    'dXJuIFp3KCIiLHMsbyxhLCExLHt1c2VybmFtZTpjLHBhc3N3b3JkOnV9KTtj'
    'YXNlInNvY2tzIjpyZXR1cm4gWncoIiIscyxvLGEsITEse3VzZXJuYW1lOmMs'
    'cGFzc3dvcmQ6dSx2ZXJzaW9uOiI1IixuZXR3b3JrOiJ0Y3AifSk7Y2FzZSBy'
    'OnJldHVybiBadygiIixzLG8sYSwhMSx7bWV0aG9kOmQscGFzc3dvcmQ6bCxu'
    'ZXR3b3JrOiJ0Y3AifSk7Y2FzZSBlOnJldHVybiBadygiIixzLG8sYSwhMSx7'
    'dXVpZDp3LGZsb3c6aCxuZXR3b3JrOiJ0Y3AifSxrLFMpO2Nhc2UgbjpyZXR1'
    'cm4gWncoIiIscyxvLGEsITEse3V1aWQ6dyxzZWN1cml0eToiYXV0byIsYWx0'
    'ZXJfaWQ6dixuZXR3b3JrOiJ0Y3AifSxrLFMpO2Nhc2UgdDpyZXR1cm4gWnco'
    'IiIscyxvLGEsITEse3Bhc3N3b3JkOmwsbmV0d29yazoidGNwIn0sayxTKTtk'
    'ZWZhdWx0OnJldHVybn19ZnVuY3Rpb24gJHcoZSx0LHIpe2NvbnN0e2Jlc3RX'
    'YXJwSW50ZXJ2YWw6bixiZXN0VkxUUkludGVydmFsOml9PWdsb2JhbFRoaXMu'
    'c2V0dGluZ3M7cmV0dXJue3R5cGU6InVybHRlc3QiLHRhZzplLG91dGJvdW5k'
    'czp0LHVybDoiaHR0cHM6Ly93d3cuZ3N0YXRpYy5jb20vZ2VuZXJhdGVfMjA0'
    'IixpbnRlcnJ1cHRfZXhpc3RfY29ubmVjdGlvbnM6ITEsaW50ZXJ2YWw6cj9g'
    'JHtufXNgOmAke2l9c2B9fWZ1bmN0aW9uIGVoKGUsdCxyLG4saSxzLG8sYSxj'
    'LHUpe2lmKCFbInRscyIsInJlYWxpdHkiXS5pbmNsdWRlcyhlKSlyZXR1cm47'
    'Y29uc3QgbD1vPy5zcGxpdCgiLCIpLmZpbHRlcihlPT4iaDIiIT09ZSksZD17'
    'ZW5hYmxlZDohMCxzZXJ2ZXJfbmFtZTpuLHJlY29yZF9mcmFnbWVudDp0LGlu'
    'c2VjdXJlOnIsYWxwbjpsLHV0bHM6e2VuYWJsZWQ6ISFhLGZpbmdlcnByaW50'
    'OmF9LGVjaDppP3tlbmFibGVkOiEwLHF1ZXJ5X3NlcnZlcl9uYW1lOnN9OnZv'
    'aWQgMH07cmV0dXJuInRscyI9PT1lP2Q6InJlYWxpdHkiPT09ZSYmYyYmdT97'
    'Li4uZCxyZWFsaXR5OntlbmFibGVkOiEwLHB1YmxpY19rZXk6YyxzaG9ydF9p'
    'ZDp1fX06dm9pZCAwfWZ1bmN0aW9uIHRoKGUsdCxyPSIvIixuLGkscyl7c3dp'
    'dGNoKHI9cj8uc3BsaXQoIj8iKVswXSxlKXtjYXNlInRjcCI6cmV0dXJuImh0'
    'dHAiPT09dD97dHlwZToiaHR0cCIsaG9zdDpuPy5zcGxpdCgiLCIpLHBhdGg6'
    'cixtZXRob2Q6IkdFVCIsaGVhZGVyczp7Q29ubmVjdGlvbjpbImtlZXAtYWxp'
    'dmUiXSwiQ29udGVudC1UeXBlIjpbImFwcGxpY2F0aW9uL29jdGV0LXN0cmVh'
    'bSJdfX06dm9pZCAwO2Nhc2Uid3MiOnJldHVybnt0eXBlOiJ3cyIscGF0aDpy'
    'Py5zcGxpdCgiP2VkPSIpWzBdLG1heF9lYXJseV9kYXRhOnMsZWFybHlfZGF0'
    'YV9oZWFkZXJfbmFtZTpzPyJTZWMtV2ViU29ja2V0LVByb3RvY29sIjp2b2lk'
    'IDAsaGVhZGVyczp7SG9zdDpufX07Y2FzZSJodHRwdXBncmFkZSI6cmV0dXJu'
    'e3R5cGU6Imh0dHB1cGdyYWRlIixob3N0Om4scGF0aDpyPy5zcGxpdCgiP2Vk'
    'PSIpWzBdfTtjYXNlImdycGMiOnJldHVybnt0eXBlOiJncnBjIixzZXJ2aWNl'
    'X25hbWU6aX07ZGVmYXVsdDpyZXR1cm59fXZhciByaD17dHlwZToidHVuIix0'
    'YWc6InR1bi1pbiIsYWRkcmVzczpbIjE3Mi4xOS4wLjEvMjgiXSxtdHU6OWUz'
    'LGF1dG9fcm91dGU6ITAsc3RyaWN0X3JvdXRlOiEwLHN0YWNrOiJtaXhlZCJ9'
    'O2Z1bmN0aW9uIG5oKCl7Y29uc3R7YWxsb3dMQU5Db25uZWN0aW9uOmV9PWds'
    'b2JhbFRoaXMuc2V0dGluZ3M7cmV0dXJue3R5cGU6Im1peGVkIix0YWc6Im1p'
    'eGVkLWluIixsaXN0ZW46ZT8iMC4wLjAuMCI6IjEyNy4wLjAuMSIsbGlzdGVu'
    'X3BvcnQ6MjA4MH19YXN5bmMgZnVuY3Rpb24gaWgoZSx0LHIsbixpLHMsbyl7'
    'Y29uc3R7bG9nTGV2ZWw6YX09Z2xvYmFsVGhpcy5zZXR0aW5ncyxjPXtsb2c6'
    'e2Rpc2FibGVkOiJub25lIj09PWEsbGV2ZWw6Im5vbmUiPT09YT92b2lkIDA6'
    'Indhcm5pbmciPT09YT8id2FybiI6YSx0aW1lc3RhbXA6ITB9LGRuczphd2Fp'
    'dCBqdyhzLG8pLGluYm91bmRzOltyaCxuaCgpXSxvdXRib3VuZHM6Wy4uLmUs'
    'e3R5cGU6InNlbGVjdG9yIix0YWc6IuKchSBTZWxlY3RvciIsb3V0Ym91bmRz'
    'OnIsaW50ZXJydXB0X2V4aXN0X2Nvbm5lY3Rpb25zOiExfSx7dHlwZToiZGly'
    'ZWN0Iix0YWc6ImRpcmVjdCJ9XSxlbmRwb2ludHM6dC5vbWl0RW1wdHkoKSxy'
    'b3V0ZTpLdyhzKSxudHA6e2VuYWJsZWQ6ITAsc2VydmVyOiJ0aW1lLmNsb3Vk'
    'ZmxhcmUuY29tIixzZXJ2ZXJfcG9ydDoxMjMsZG9tYWluX3Jlc29sdmVyOiJk'
    'bnMtZGlyZWN0IixpbnRlcnZhbDoiMzBtIix3cml0ZV90b19zeXN0ZW06ITF9'
    'LGV4cGVyaW1lbnRhbDp7Y2FjaGVfZmlsZTp7ZW5hYmxlZDohMCxzdG9yZV9m'
    'YWtlaXA6ITB9LGNsYXNoX2FwaTp7ZXh0ZXJuYWxfY29udHJvbGxlcjoiMTI3'
    'LjAuMC4xOjkwOTAiLGV4dGVybmFsX3VpOiJ1aSIsZGVmYXVsdF9tb2RlOiJS'
    'dWxlIixleHRlcm5hbF91aV9kb3dubG9hZF91cmw6Imh0dHBzOi8vZ2l0aHVi'
    'LmNvbS9NZXRhQ3ViZVgvbWV0YWN1YmV4ZC9hcmNoaXZlL3JlZnMvaGVhZHMv'
    'Z2gtcGFnZXMuemlwIixleHRlcm5hbF91aV9kb3dubG9hZF9kZXRvdXI6ImRp'
    'cmVjdCJ9fX0sdT12b2lkIDAsbD0kdyhzPyLwn5KmIFdhcnAgLSBCZXN0IFBp'
    'bmcg8J+agCI6IvCfkqYgQmVzdCBQaW5nIPCfmoAiLG4scyk7cmV0dXJuIGMu'
    'b3V0Ym91bmRzLnB1c2gobCkscyYmYy5vdXRib3VuZHMucHVzaCgkdygi8J+S'
    'piBXb1cgLSBCZXN0IFBpbmcg8J+agCIsaSxzKSksbyYmYy5vdXRib3VuZHMu'
    'cHVzaCgkdygi8J+SpiDwn5SXIEJlc3QgUGluZyDwn5qAIixpLHMpKSxjfWFz'
    'eW5jIGZ1bmN0aW9uIHNoKGUpe2NvbnN0e291dFByb3h5OnQscG9ydHM6cix1'
    'cHN0cmVhbVBhcmFtczp7dXBzdHJlYW1TZXJ2ZXI6bix1cHN0cmVhbVBvcnQ6'
    'aX19PWdsb2JhbFRoaXMuc2V0dGluZ3Mscz10P3F3KCk6dm9pZCAwLG89ISFz'
    'LGE9VGwoKSxjPWF3YWl0IHhsKGUpLHU9ci5maWx0ZXIodD0+IWV8fExsKHQp'
    'KTtuJiZpJiYhZSYmKHUudW5zaGlmdChpKSxjLnVuc2hpZnQobikpO2NvbnN0'
    'IGw9W10sZD1bXSx3PVtdLGg9WyLwn5KmIEJlc3QgUGluZyDwn5qAIl0uY29u'
    'Y2F0SWYobywi8J+SpiDwn5SXIEJlc3QgUGluZyDwn5qAIik7Zm9yKGNvbnN0'
    'IHQgb2YgYSl7bGV0IHI9MTtmb3IoY29uc3QgYSBvZiB1KWZvcihjb25zdCB1'
    'IG9mIGMpe2lmKGE9PT1pIT0odT09PW4pKWNvbnRpbnVlO2NvbnN0IGM9dmwo'
    'cixhLHUsdCxlLCExKSxmPUd3KHQsYyx1LGEsZSk7aWYody5wdXNoKGYpLGwu'
    'cHVzaChjKSxoLnB1c2goYyksbyl7Y29uc3Qgbj12bChyLGEsdSx0LGUsITAp'
    'LGk9c3RydWN0dXJlZENsb25lKHMpO2kudGFnPW4saS5kZXRvdXI9Yyx3LnB1'
    'c2goaSksZC5wdXNoKG4pLGgucHVzaChuKX1yKyt9fWNvbnN0IGY9YXdhaXQg'
    'aWgodyxbXSxoLGwsZCwhMSxvKTtyZXR1cm4gbmV3IFJlc3BvbnNlKEpTT04u'
    'c3RyaW5naWZ5KGYsbnVsbCw0KSx7c3RhdHVzOjIwMCxoZWFkZXJzOnsiQ29u'
    'dGVudC1UeXBlIjoidGV4dC9wbGFpbjtjaGFyc2V0PXV0Zi04IiwiQ2FjaGUt'
    'Q29udHJvbCI6Im5vLXN0b3JlIiwiQ0ROLUNhY2hlLUNvbnRyb2wiOiJuby1z'
    'dG9yZSJ9fSl9YXN5bmMgZnVuY3Rpb24gb2goZSx0KXtjb25zdHt3YXJwRW5k'
    'cG9pbnRzOnJ9PWdsb2JhbFRoaXMuc2V0dGluZ3Mse3dhcnBBY2NvdW50czpu'
    'fT1hd2FpdCBYbChlLHQpLGk9W10scz1bXSxvPVtdLGE9WyLwn5KmIFdhcnAg'
    'LSBCZXN0IFBpbmcg8J+agCIsIvCfkqYgV29XIC0gQmVzdCBQaW5nIPCfmoAi'
    'XTtyLmZvckVhY2goKGUsdCk9Pntjb25zdCByPWDwn5KmICR7dCsxfSAtIFdh'
    'cnAg8J+HrvCfh7dgO2kucHVzaChyKTtjb25zdCBjPWDwn5KmICR7dCsxfSAt'
    'IFdvVyDwn4yNYDtzLnB1c2goYyksYS5wdXNoKHIsYyk7Y29uc3QgdT1Rdyhu'
    'WzBdLHIsZSksbD1RdyhuWzFdLGMsZSxyKTtvLnB1c2godSxsKX0pO2NvbnN0'
    'IGM9YXdhaXQgaWgoW10sbyxhLGkscywhMCwhMSk7cmV0dXJuIG5ldyBSZXNw'
    'b25zZShKU09OLnN0cmluZ2lmeShjLG51bGwsNCkse3N0YXR1czoyMDAsaGVh'
    'ZGVyczp7IkNvbnRlbnQtVHlwZSI6InRleHQvcGxhaW47Y2hhcnNldD11dGYt'
    'OCIsIkNhY2hlLUNvbnRyb2wiOiJuby1zdG9yZSIsIkNETi1DYWNoZS1Db250'
    'cm9sIjoibm8tc3RvcmUifX0pfWZ1bmN0aW9uIGFoKCl7Y29uc3R7bG9jYWxE'
    'TlM6ZSxhbnRpU2FuY3Rpb25ETlM6dCxibG9ja01hbHdhcmU6cixibG9ja1Bo'
    'aXNoaW5nOm4sYmxvY2tDcnlwdG9taW5lcnM6aSxibG9ja0FkczpzLGJsb2Nr'
    'UG9ybjpvLGJ5cGFzc0lyYW46YSxieXBhc3NDaGluYTpjLGJ5cGFzc1J1c3Np'
    'YTp1LGJ5cGFzc09wZW5BaTpsLGJ5cGFzc0dvb2dsZUFpOmQsYnlwYXNzTWlj'
    'cm9zb2Z0OncsYnlwYXNzT3JhY2xlOmgsYnlwYXNzRG9ja2VyOmYsYnlwYXNz'
    'QWRvYmU6QSxieXBhc3NFcGljR2FtZXM6cCxieXBhc3NJbnRlbDpFLGJ5cGFz'
    'c0FtZDpCLGJ5cGFzc052aWRpYTpILGJ5cGFzc0FzdXM6bSxieXBhc3NIcDpn'
    'LGJ5cGFzc0xlbm92bzp5fT1nbG9iYWxUaGlzLnNldHRpbmdzO3JldHVyblt7'
    'cnVsZTpzLHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9zaXRlOmNhdGVnb3J5'
    'LWFkcy1hbGwifSx7cnVsZTpzLHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9z'
    'aXRlOmNhdGVnb3J5LWFkcy1pciJ9LHtydWxlOm8sdHlwZToiYmxvY2siLGdl'
    'b3NpdGU6Imdlb3NpdGU6Y2F0ZWdvcnktcG9ybiJ9LHtydWxlOnIsdHlwZToi'
    'YmxvY2siLGdlb3NpdGU6Imdlb3NpdGU6bWFsd2FyZSIsZ2VvaXA6Imdlb2lw'
    'Om1hbHdhcmUifSx7cnVsZTpuLHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9z'
    'aXRlOnBoaXNoaW5nIixnZW9pcDoiZ2VvaXA6cGhpc2hpbmcifSx7cnVsZTpp'
    'LHR5cGU6ImJsb2NrIixnZW9zaXRlOiJnZW9zaXRlOmNyeXB0b21pbmVycyJ9'
    'LHtydWxlOmEsdHlwZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRlOmNhdGVn'
    'b3J5LWlyIixnZW9pcDoiZ2VvaXA6aXIiLGRuczplfSx7cnVsZTpjLHR5cGU6'
    'ImRpcmVjdCIsZ2Vvc2l0ZToiZ2Vvc2l0ZTpjbiIsZ2VvaXA6Imdlb2lwOmNu'
    'IixkbnM6ZX0se3J1bGU6dSx0eXBlOiJkaXJlY3QiLGdlb3NpdGU6Imdlb3Np'
    'dGU6Y2F0ZWdvcnktcnUiLGdlb2lwOiJnZW9pcDpydSIsZG5zOmV9LHtydWxl'
    'OmwsdHlwZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRlOm9wZW5haSIsZG5z'
    'OnR9LHtydWxlOmQsdHlwZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRlOmdv'
    'b2dsZS1kZWVwbWluZCIsZG5zOnR9LHtydWxlOncsdHlwZToiZGlyZWN0Iixn'
    'ZW9zaXRlOiJnZW9zaXRlOm1pY3Jvc29mdCIsZG5zOnR9LHtydWxlOmgsdHlw'
    'ZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRlOm9yYWNsZSIsZG5zOnR9LHty'
    'dWxlOmYsdHlwZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRlOmRvY2tlciIs'
    'ZG5zOnR9LHtydWxlOkEsdHlwZToiZGlyZWN0IixnZW9zaXRlOiJnZW9zaXRl'
    'OmFkb2JlIixkbnM6dH0se3J1bGU6cCx0eXBlOiJkaXJlY3QiLGdlb3NpdGU6'
    'Imdlb3NpdGU6ZXBpY2dhbWVzIixkbnM6dH0se3J1bGU6RSx0eXBlOiJkaXJl'
    'Y3QiLGdlb3NpdGU6Imdlb3NpdGU6aW50ZWwiLGRuczp0fSx7cnVsZTpCLHR5'
    'cGU6ImRpcmVjdCIsZ2Vvc2l0ZToiZ2Vvc2l0ZTphbWQiLGRuczp0fSx7cnVs'
    'ZTpILHR5cGU6ImRpcmVjdCIsZ2Vvc2l0ZToiZ2Vvc2l0ZTpudmlkaWEiLGRu'
    'czp0fSx7cnVsZTptLHR5cGU6ImRpcmVjdCIsZ2Vvc2l0ZToiZ2Vvc2l0ZTph'
    'c3VzIixkbnM6dH0se3J1bGU6Zyx0eXBlOiJkaXJlY3QiLGdlb3NpdGU6Imdl'
    'b3NpdGU6aHAiLGRuczp0fSx7cnVsZTp5LHR5cGU6ImRpcmVjdCIsZ2Vvc2l0'
    'ZToiZ2Vvc2l0ZTpsZW5vdm8iLGRuczp0fV0uZmlsdGVyKCh7cnVsZTplfSk9'
    'PmUpfWFzeW5jIGZ1bmN0aW9uIGNoKGUsdCxyLG4saSxzKXtjb25zdHtsb2Nh'
    'bEROUzpvLHJlbW90ZUROUzphLHdhcnBSZW1vdGVETlM6YyxhbnRpU2FuY3Rp'
    'b25ETlM6dSxyZW1vdGVEbnNIb3N0OmwsZW5hYmxlSVB2NjpkLGZha2VETlM6'
    'd309Z2xvYmFsVGhpcy5zZXR0aW5ncyxoPXt9LGY9W10sQT1bXTtpZihsLmlz'
    'RG9tYWluJiYhdCYmIXIpe2NvbnN0e2lwdjQ6ZSxpcHY2OnQsaG9zdDpyfT1s'
    'O2hbcl09ZS5jb25jYXRJZihkLHQpfWlmKG4pe2NvbnN0e2lwdjQ6ZSxpcHY2'
    'OnR9PWF3YWl0IGdsKG4sZCk7aFtuXT1bLi4uZSwuLi50XX1sZXQgcD0hMCxF'
    'PXI/YzphO3QmJihFPWBodHRwczovLyR7aX0vZG5zLXF1ZXJ5YCxpJiZzJiYo'
    'aFtpXT1zKSxwPSExKTtjb25zdCBCPXVoKEUsdm9pZCAwLHZvaWQgMCx2b2lk'
    'IDAsdm9pZCAwLCJyZW1vdGUtZG5zIik7Zi5wdXNoKEIpO2NvbnN0IEg9dm9p'
    'ZCAwLG09TmwoYWgoKSksZz12b2lkIDA7Wy4uLm0uYmxvY2suZ2Vvc2l0ZXMs'
    'Li4ubS5ibG9jay5kb21haW5zLm1hcChlPT5gZG9tYWluOiR7ZX1gKV0uZm9y'
    'RWFjaChlPT5oW2VdPSIjMyIpLG0uYnlwYXNzLmxvY2FsRE5TLmdlb3NpdGVH'
    'ZW9pcHMuZm9yRWFjaCgoe2dlb3NpdGU6ZSxnZW9pcDp0fSk9Pntjb25zdCBy'
    'PXVoKG8sW2VdLFt0XSxwKTtmLnB1c2gociksQS5wdXNoKGUpfSk7Y29uc3Qg'
    'eT1bLi4ubS5ieXBhc3MuYW50aVNhbmN0aW9uRE5TLmdlb3NpdGVzLC4uLm0u'
    'YnlwYXNzLmFudGlTYW5jdGlvbkROUy5kb21haW5zLm1hcChlPT5gZG9tYWlu'
    'OiR7ZX1gKV0sVD1bLi4ubS5ieXBhc3MubG9jYWxETlMuZ2Vvc2l0ZXMsLi4u'
    'bS5ieXBhc3MubG9jYWxETlMuZG9tYWlucy5tYXAoZT0+YGRvbWFpbjoke2V9'
    'YCksLi4uZS5maWx0ZXIobWwpLm1hcChlPT5gZnVsbDoke2V9YCldO2lmKHku'
    'bGVuZ3RoKXtjb25zdCBlPXVoKHUseSx2b2lkIDAscCwhMCk7Zi5wdXNoKGUp'
    'O2NvbnN0e2hvc3Q6dCxpc0hvc3REb21haW46cn09X2wodSk7ciYmVC5wdXNo'
    'KGBmdWxsOiR7dH1gKX1pZihzPy5maWx0ZXIobWwpLmZvckVhY2goZT0+VC5w'
    'dXNoKGBmdWxsOiR7ZX1gKSksVC5sZW5ndGgpe2NvbnN0IGU9dWgobyxULHZv'
    'aWQgMCxwKTtmLnB1c2goZSksQS5wdXNoKC4uLlQpfWlmKHcpe2NvbnN0IGU9'
    'QS5sZW5ndGg/dWgoImZha2VkbnMiLEEsdm9pZCAwLCExLHZvaWQgMCk6ImZh'
    'a2VkbnMiO2YudW5zaGlmdChlKX1yZXR1cm57aG9zdHM6aC5vbWl0RW1wdHko'
    'KSxzZXJ2ZXJzOmYscXVlcnlTdHJhdGVneTpyJiYhZD8iVXNlSVB2NCI6IlVz'
    'ZUlQIix0YWc6ImRucyJ9fWZ1bmN0aW9uIHVoKGUsdCxyLG4saSxzKXtyZXR1'
    'cm57YWRkcmVzczplLGRvbWFpbnM6dCxleHBlY3RJUHM6cixza2lwRmFsbGJh'
    'Y2s6bixmaW5hbFF1ZXJ5OmksdGFnOnN9fWZ1bmN0aW9uIGxoKGUsdCxyLG4p'
    'e2NvbnN0e2Jsb2NrVURQNDQzOml9PWdsb2JhbFRoaXMuc2V0dGluZ3Mscz1b'
    'e2luYm91bmRUYWc6WyJtaXhlZC1pbiJdLHBvcnQ6NTMsb3V0Ym91bmRUYWc6'
    'ImRucy1vdXQiLHR5cGU6ImZpZWxkIn0se2luYm91bmRUYWc6WyJkbnMtaW4i'
    'XSxvdXRib3VuZFRhZzoiZG5zLW91dCIsdHlwZToiZmllbGQifV0sbz12b2lk'
    'IDAsYT10P2U/ImFsbC1jaGFpbnMiOiJhbGwtcHJveGllcyI6ZT8iY2hhaW4i'
    'OnI/ImRpcmVjdCI6InByb3h5IixjPXZvaWQgMDtkaChzLFsicmVtb3RlLWRu'
    'cyJdLHZvaWQgMCx2b2lkIDAsdm9pZCAwLHZvaWQgMCx2b2lkIDAsdD8iYWxs'
    'LXByb3hpZXMiOiJwcm94eSIsdCksZGgocyxbImRucyJdLHZvaWQgMCx2b2lk'
    'IDAsdm9pZCAwLHZvaWQgMCx2b2lkIDAsImRpcmVjdCIsITEpLGRoKHMsdm9p'
    'ZCAwLFsiZ2Vvc2l0ZTpwcml2YXRlIl0sdm9pZCAwLHZvaWQgMCx2b2lkIDAs'
    'dm9pZCAwLCJkaXJlY3QiLCExKSxkaChzLHZvaWQgMCx2b2lkIDAsWyJnZW9p'
    'cDpwcml2YXRlIl0sdm9pZCAwLHZvaWQgMCx2b2lkIDAsImRpcmVjdCIsITEp'
    'LG58fHI/aSYmZGgocyx2b2lkIDAsdm9pZCAwLHZvaWQgMCw0NDMsInVkcCIs'
    'dm9pZCAwLCJibG9jayIsITEpOmRoKHMsdm9pZCAwLHZvaWQgMCx2b2lkIDAs'
    'dm9pZCAwLCJ1ZHAiLHZvaWQgMCwiYmxvY2siLCExKTtjb25zdCB1PXZvaWQg'
    'MCxsPVVsKGFoKCkpLGQ9Wy4uLmwuYmxvY2suZ2Vvc2l0ZXMsLi4ubC5ibG9j'
    'ay5kb21haW5zLm1hcChlPT5gZG9tYWluOiR7ZX1gKV07ZC5sZW5ndGgmJmRo'
    'KHMsdm9pZCAwLGQsdm9pZCAwLHZvaWQgMCx2b2lkIDAsdm9pZCAwLCJibG9j'
    'ayIpO2NvbnN0IHc9Wy4uLmwuYmxvY2suZ2VvaXBzLC4uLmwuYmxvY2suaXBz'
    'XTt3Lmxlbmd0aCYmZGgocyx2b2lkIDAsdm9pZCAwLHcsdm9pZCAwLHZvaWQg'
    'MCx2b2lkIDAsImJsb2NrIik7Y29uc3QgaD1bLi4ubC5ieXBhc3MuZ2Vvc2l0'
    'ZXMsLi4ubC5ieXBhc3MuZG9tYWlucy5tYXAoZT0+YGRvbWFpbjoke2V9YCld'
    'O2gubGVuZ3RoJiZkaChzLHZvaWQgMCxoLHZvaWQgMCx2b2lkIDAsdm9pZCAw'
    'LHZvaWQgMCwiZGlyZWN0Iik7Y29uc3QgZj1bLi4ubC5ieXBhc3MuZ2VvaXBz'
    'LC4uLmwuYnlwYXNzLmlwc107Zi5sZW5ndGgmJmRoKHMsdm9pZCAwLHZvaWQg'
    'MCxmLHZvaWQgMCx2b2lkIDAsdm9pZCAwLCJkaXJlY3QiKSxyJiYoZGgocyx2'
    'b2lkIDAsdm9pZCAwLHZvaWQgMCx2b2lkIDAsInRjcCIsWyJ0bHMiXSwicHJv'
    'eHkiLCExKSxkaChzLHZvaWQgMCx2b2lkIDAsdm9pZCAwLHZvaWQgMCwidGNw'
    'IixbImh0dHAiXSwiaHR0cC1mcmFnbWVudCIsITEpLGRoKHMsdm9pZCAwLHZv'
    'aWQgMCx2b2lkIDAsdm9pZCAwLCJ1ZHAiLFsicXVpYyJdLCJ1ZHAtbm9pc2Ui'
    'LCExKSxkaChzLHZvaWQgMCx2b2lkIDAsdm9pZCAwLCI0NDMsMjA1MywyMDgz'
    'LDIwODcsMjA5Niw4NDQzIiwidWRwIix2b2lkIDAsInVkcC1ub2lzZSIsITEp'
    'KTtjb25zdCBBPXZvaWQgMDtyZXR1cm4gZGgocyx2b2lkIDAsdm9pZCAwLHZv'
    'aWQgMCx2b2lkIDAsbnx8cj8idGNwLHVkcCI6InRjcCIsdm9pZCAwLGEsdCks'
    'c312YXIgZGg9KGUsdCxyLG4saSxzLG8sYSxjKT0+ZS5wdXNoKHtpbmJvdW5k'
    'VGFnOnQsZG9tYWluOnIsaXA6bixwb3J0OmksbmV0d29yazpzLHByb3RvY29s'
    'Om8sYmFsYW5jZXJUYWc6Yz9hOnZvaWQgMCxvdXRib3VuZFRhZzpjP3ZvaWQg'
    'MDphLHR5cGU6ImZpZWxkIn0pO2Z1bmN0aW9uIHdoKGUsdCxyKXtjb25zdCBu'
    'PXZvaWQgMDtyZXR1cm57bGlzdGVuOmU/IjAuMC4wLjAiOiIxMjcuMC4wLjEi'
    'LHBvcnQ6MTA4MDgscHJvdG9jb2w6Im1peGVkIixzZXR0aW5nczp7YXV0aDoi'
    'bm9hdXRoIix1ZHA6ITB9LHNuaWZmaW5nOntkZXN0T3ZlcnJpZGU6WyJodHRw'
    'IiwidGxzIl0uY29uY2F0SWYodCwicXVpYyIpLmNvbmNhdElmKHIsImZha2Vk'
    'bnMiKSxlbmFibGVkOiEwLHJvdXRlT25seTohMH0sdGFnOiJtaXhlZC1pbiJ9'
    'fWZ1bmN0aW9uIGhoKGUpe3JldHVybntsaXN0ZW46ZT8iMC4wLjAuMCI6IjEy'
    'Ny4wLjAuMSIscG9ydDoxMDg1Myxwcm90b2NvbDoiZG9rb2RlbW8tZG9vciIs'
    'c2V0dGluZ3M6e2FkZHJlc3M6IjEuMS4xLjEiLG5ldHdvcms6InRjcCx1ZHAi'
    'LHBvcnQ6NTN9LHRhZzoiZG5zLWluIn19ZnVuY3Rpb24gZmgoZSx0LHIsbixp'
    'KXtyZXR1cm57cHJvdG9jb2w6ZSxtdXg6cj97ZW5hYmxlZDohMCxjb25jdXJy'
    'ZW5jeTo4LHh1ZHBDb25jdXJyZW5jeToxNix4dWRwUHJveHlVRFA0NDM6InJl'
    'amVjdCJ9OnZvaWQgMCxzZXR0aW5nczpuLHN0cmVhbVNldHRpbmdzOmksdGFn'
    'OnR9fWZ1bmN0aW9uIEFoKGUsdCxyLG4saSxzKXtjb25zdHtmcmFnbWVudFBh'
    'Y2tldHM6byxmcmFnbWVudExlbmd0aE1pbjphLGZyYWdtZW50TGVuZ3RoTWF4'
    'OmMsZnJhZ21lbnRJbnRlcnZhbE1pbjp1LGZyYWdtZW50SW50ZXJ2YWxNYXg6'
    'bCxmcmFnbWVudE1heFNwbGl0TWluOmQsZnJhZ21lbnRNYXhTcGxpdE1heDp3'
    'LGVuYWJsZVRGTzpoLHhyYXlVZHBOb2lzZXM6ZixlbmFibGVJUHY2OkF9PWds'
    'b2JhbFRoaXMuc2V0dGluZ3M7bGV0IHA9e30sRTtyZXR1cm4gZSYmKHA9e2Zy'
    'YWdtZW50OntwYWNrZXRzOnN8fG8sbGVuZ3RoOm58fHpsKGEsYyksaW50ZXJ2'
    'YWw6aXx8emwodSxsKSxtYXhTcGxpdDp6bChkLHcpfX0sRT17c29ja29wdDpt'
    'aCghMCxoLCJVc2VJUCIpfSksdCYmKHA9ey4uLnAsbm9pc2VzOlRoKGYpLGRv'
    'bWFpblN0cmF0ZWd5OmU/dm9pZCAwOkE/IlVzZUlQdjR2NiI6IlVzZUlQdjQi'
    'fSkse3Byb3RvY29sOiJmcmVlZG9tIixzZXR0aW5nczpwLHN0cmVhbVNldHRp'
    'bmdzOkUsdGFnOnJ9fWZ1bmN0aW9uIHBoKGUsdCxyLG4saSxzLG8pe2NvbnN0'
    'e3NldHRpbmdzOntmaW5nZXJwcmludDphLGVuYWJsZVRGTzpjLGVuYWJsZUVD'
    'SDp1LGVjaFNlcnZlck5hbWU6bCxmcmFnbWVudFBhY2tldHM6ZCxmcmFnbWVu'
    'dExlbmd0aE1pbjp3LGZyYWdtZW50TGVuZ3RoTWF4OmgsZnJhZ21lbnRJbnRl'
    'cnZhbE1pbjpmLGZyYWdtZW50SW50ZXJ2YWxNYXg6QSxmcmFnbWVudE1heFNw'
    'bGl0TWluOnAsZnJhZ21lbnRNYXhTcGxpdE1heDpFLHVwc3RyZWFtUGFyYW1z'
    'Ont1cHN0cmVhbVNlcnZlcjpCfX0sZ2xvYmFsQ29uZmlnOnt1c2VySUQ6SCxU'
    'clBhc3M6bX0sZGljdDp7X1ZMXzpnfX09Z2xvYmFsVGhpcyx5PUxsKG4pfHxy'
    'PT09Qix7aG9zdDpULHNuaTp4fT1PbChyKSx2PXk/Z2goeCxhLCJodHRwLzEu'
    'MSIsdSYmIWksbHx8dm9pZCAwKTp2b2lkIDAsYj17bmV0d29yazoid3MiLC4u'
    'LkhoKCJ3cyIsIm5vbmUiLGAke01sKHQpfT9lZD0yNTYwYCxUKSxzZWN1cml0'
    'eTp5PyJ0bHMiOiJub25lIix0bHNTZXR0aW5nczp2LHNvY2tvcHQ6bWgoITAs'
    'YywiVXNlSVAiKSxmaW5hbG1hc2s6aT97dGNwOlt7dHlwZToiZnJhZ21lbnQi'
    'LHNldHRpbmdzOntwYWNrZXRzOmQsbGVuZ3RoOnM/P3psKHcsaCksZGVsYXk6'
    'bz8/emwoZixBKSxtYXhTcGxpdDp6bChwLEUpfX1dfTp2b2lkIDB9O3JldHVy'
    'biBmaCh0LGUsITEsdD09PWc/e3ZuZXh0Olt7YWRkcmVzczpyLHBvcnQ6bix1'
    'c2Vyczpbe2lkOkgsZW5jcnlwdGlvbjoibm9uZSJ9XX1dfTp7c2VydmVyczpb'
    'e2FkZHJlc3M6cixwb3J0Om4scGFzc3dvcmQ6bX1dfSxiKX1mdW5jdGlvbiBF'
    'aChlLHQscixuLGkpe2NvbnN0e3hyYXlVZHBOb2lzZXM6c309Z2xvYmFsVGhp'
    'cy5zZXR0aW5ncyx7d2FycElQdjY6byxyZXNlcnZlZDphLHB1YmxpY0tleTpj'
    'LHByaXZhdGVLZXk6dX09ZTtsZXQgbD17YWRkcmVzczpbIjE3Mi4xNi4wLjIv'
    'MzIiLG9dLG10dToxMjgwLHBlZXJzOlt7ZW5kcG9pbnQ6cj8iMTYyLjE1OS4x'
    'OTIuMToyNDA4Ijp0LHB1YmxpY0tleTpjLGtlZXBBbGl2ZTo1fV0scmVzZXJ2'
    'ZWQ6a2woYSksc2VjcmV0S2V5OnV9O2NvbnN0IGQ9e307aWYocilkLnNvY2tv'
    'cHQ9bWgoITEsITEsdm9pZCAwLCJwcm94eSIpO2Vsc2UgaWYobilpZihpKXtj'
    'b25zdHtrbm9ja2VyTm9pc2VNb2RlOmUsbm9pc2VDb3VudE1pbjp0LG5vaXNl'
    'Q291bnRNYXg6cixub2lzZVNpemVNaW46bixub2lzZVNpemVNYXg6aSxub2lz'
    'ZURlbGF5TWluOnMsbm9pc2VEZWxheU1heDpvfT1nbG9iYWxUaGlzLnNldHRp'
    'bmdzO2w9ey4uLmwsd25vaXNlOmUsd25vaXNlY291bnQ6emwodCxyKSx3cGF5'
    'bG9hZHNpemU6emwobixpKSx3bm9pc2VkZWxheTp6bChzLG8pfX1lbHNlIGQu'
    'ZmluYWxtYXNrPXt1ZHA6W3t0eXBlOiJub2lzZSIsc2V0dGluZ3M6e3Jlc2V0'
    'OiIzMC02MCIsbm9pc2U6VGgocyl9fV19O3JldHVybntwcm90b2NvbDoid2ly'
    'ZWd1YXJkIixzZXR0aW5nczpsLHN0cmVhbVNldHRpbmdzOmQub21pdEVtcHR5'
    'KCksdGFnOnI/ImNoYWluIjoicHJveHkifX1mdW5jdGlvbiBCaCgpe2NvbnN0'
    'e2RpY3Q6e19WTF86ZSxfVFJfOnQsX1NTXzpyLF9WTV86bn0sc2V0dGluZ3M6'
    'e291dFByb3h5UGFyYW1zOntwcm90b2NvbDppLHNlcnZlcjpzLHBvcnQ6byx1'
    'c2VyOmEscGFzczpjLHBhc3N3b3JkOnUsbWV0aG9kOmwsdXVpZDpkLGZsb3c6'
    'dyxzZWN1cml0eTpoLHR5cGU6Zixzbmk6QSxmcDpwLGhvc3Q6RSxwYXRoOkIs'
    'YWxwbjpILHBiazptLHNpZDpnLHNweDp5LGhlYWRlclR5cGU6VCxzZXJ2aWNl'
    'TmFtZTp4LG1vZGU6dixhdXRob3JpdHk6Yn19fT1nbG9iYWxUaGlzLFI9e25l'
    'dHdvcms6Znx8InJhdyIsLi4uSGgoZixULEIsRSx4LHYsYiksc2VjdXJpdHk6'
    'aCx0bHNTZXR0aW5nczoidGxzIj09PWg/Z2goQXx8cyxwLEgsITEsdm9pZCAw'
    'KTp2b2lkIDAscmVhbGl0eVNldHRpbmdzOiJyZWFsaXR5Ij09PWg/eWgoQSxw'
    'LG0sZyx5KTp2b2lkIDAsc29ja29wdDptaCghMSwhMSwiVXNlSVB2NCIsInBy'
    'b3h5Iil9LE09ISgicmVhbGl0eSI9PT1ofHwiZ3JwYyI9PT1mKTtzd2l0Y2go'
    'aSl7Y2FzZSJodHRwIjpjYXNlInNvY2tzIjpyZXR1cm4gZmgoaSwiY2hhaW4i'
    'LE0se3NlcnZlcnM6W3thZGRyZXNzOnMscG9ydDpvLHVzZXJzOlt7dXNlcjph'
    'LHBhc3M6Y31dfV19LFIpO2Nhc2UgcjpyZXR1cm4gZmgoaSwiY2hhaW4iLE0s'
    'e3NlcnZlcnM6W3thZGRyZXNzOnMscG9ydDpvLG1ldGhvZDpsLHBhc3N3b3Jk'
    'OnV9XX0sUik7Y2FzZSBlOnJldHVybiBmaChpLCJjaGFpbiIsTSx7dm5leHQ6'
    'W3thZGRyZXNzOnMscG9ydDpvLHVzZXJzOlt7aWQ6ZCxmbG93OncsZW5jcnlw'
    'dGlvbjoibm9uZSJ9XX1dfSxSKTtjYXNlIG46cmV0dXJuIGZoKGksImNoYWlu'
    'IixNLHt2bmV4dDpbe2FkZHJlc3M6cyxwb3J0Om8sdXNlcnM6W3tpZDpkLHNl'
    'Y3VyaXR5OiJhdXRvIn1dfV19LFIpO2Nhc2UgdDpyZXR1cm4gZmgoaSwiY2hh'
    'aW4iLE0se3NlcnZlcnM6W3thZGRyZXNzOnMscG9ydDpvLHBhc3N3b3JkOnV9'
    'XX0sUik7ZGVmYXVsdDpyZXR1cm59fWZ1bmN0aW9uIEhoKGUsdCxyPSIvIixu'
    'LGkscyxvKXtzd2l0Y2goZSl7Y2FzZSJ0Y3AiOmNhc2UicmF3IjpyZXR1cm57'
    'cmF3U2V0dGluZ3M6e2hlYWRlcjoiaHR0cCI9PT10P3t0eXBlOiJodHRwIixy'
    'ZXF1ZXN0OntoZWFkZXJzOntIb3N0Om4/LnNwbGl0KCIsIiksIkFjY2VwdC1F'
    'bmNvZGluZyI6WyJnemlwLCBkZWZsYXRlIl0sQ29ubmVjdGlvbjpbImtlZXAt'
    'YWxpdmUiXSxQcmFnbWE6Im5vLWNhY2hlIn0scGF0aDpyLnNwbGl0KCIsIiks'
    'bWV0aG9kOiJHRVQiLHZlcnNpb246IjEuMSJ9fTp7dHlwZToibm9uZSJ9fX07'
    'Y2FzZSJ3cyI6cmV0dXJue3dzU2V0dGluZ3M6e2hvc3Q6bixwYXRoOnJ9fTtj'
    'YXNlImh0dHB1cGdyYWRlIjpyZXR1cm57aHR0cHVwZ3JhZGVTZXR0aW5nczp7'
    'aG9zdDpuLHBhdGg6cn19O2Nhc2UiZ3JwYyI6cmV0dXJue2dycGNTZXR0aW5n'
    'czp7YXV0aG9yaXR5Om8sbXVsdGlNb2RlOiJtdWx0aSI9PT1zLHNlcnZpY2VO'
    'YW1lOml9fTtkZWZhdWx0OnJldHVybnt9fX1mdW5jdGlvbiBtaChlLHQscixu'
    'KXtyZXR1cm57ZG9tYWluU3RyYXRlZ3k6cixkaWFsZXJQcm94eTpuLHRjcEZh'
    'c3RPcGVuOnR8fHZvaWQgMCxoYXBweUV5ZWJhbGxzOmU/e3RyeURlbGF5TXM6'
    'MjUwLHByaW9yaXRpemVJUHY2OiExLGludGVybGVhdmU6MixtYXhDb25jdXJy'
    'ZW50VHJ5OjR9OnZvaWQgMH19ZnVuY3Rpb24gZ2goZSx0LHIsbixpKXtjb25z'
    'dHtsb2NhbEROUzpzfT1nbG9iYWxUaGlzLnNldHRpbmdzLG89ImxvY2FsaG9z'
    'dCI9PT1zPyI4LjguOC44IjpzO3JldHVybntzZXJ2ZXJOYW1lOmUsZmluZ2Vy'
    'cHJpbnQ6dCxhbHBuOnI/LnNwbGl0KCIsIiksZWNoQ29uZmlnTGlzdDpuP2k/'
    'YCR7aX0rdWRwOi8vJHtvfWA6YHVkcDovLyR7b31gOnZvaWQgMH19ZnVuY3Rp'
    'b24geWgoZSx0LHIsbixpKXtyZXR1cm57c2VydmVyTmFtZTplLGZpbmdlcnBy'
    'aW50OnQscHVibGljS2V5OnIsc2hvcnRJZDpuLHNwaWRlclg6aSxzaG93OiEx'
    'LGFsbG93SW5zZWN1cmU6ITF9fWZ1bmN0aW9uIFRoKGUpe3JldHVybiBlLmZs'
    'YXRNYXAoKHt0eXBlOmUscGFja2V0OnQsZGVsYXk6cixjb3VudDpufSk9Pntj'
    'b25zdCBpPSJyYW5kIj09PWU/e3JhbmQ6dCxyYW5kUmFuZ2U6IjAtMjU1Iixk'
    'ZWxheTpyfTp7dHlwZTplLHBhY2tldDoiYXJyYXkiPT09ZT90LnNwbGl0KCIs'
    'IikubWFwKE51bWJlcik6dCxkZWxheTpyfTtyZXR1cm4gQXJyYXkuZnJvbSh7'
    'bGVuZ3RoOm59LCgpPT5pKX0pfWZ1bmN0aW9uIHhoKGUsdCxyKXtyZXR1cm57'
    'dGFnOmUsc2VsZWN0b3I6W3RdLHN0cmF0ZWd5Ont0eXBlOiJsZWFzdFBpbmci'
    'fSxmYWxsYmFja1RhZzpyPyJwcm94eS0yIjp2b2lkIDB9fWFzeW5jIGZ1bmN0'
    'aW9uIHZoKGUsdCxyLG4saSxzLG8sYSxjLHUsbCl7Y29uc3R7ZmFrZUROUzpk'
    'LGJlc3RXYXJwSW50ZXJ2YWw6dyxiZXN0VkxUUkludGVydmFsOmgsbG9nTGV2'
    'ZWw6ZixhbGxvd0xBTkNvbm5lY3Rpb246QX09Z2xvYmFsVGhpcy5zZXR0aW5n'
    'cztsZXQgcCxFO3ImJihwPVt4aCgiYWxsLXByb3hpZXMiLCJwcm94eSIsaSld'
    'LmNvbmNhdElmKG4seGgoImFsbC1jaGFpbnMiLCJjaGFpbiIsITEpKSxFPXtz'
    'dWJqZWN0U2VsZWN0b3I6bj9bImNoYWluIiwicHJveHkiXTpbInByb3h5Il0s'
    'cHJvYmVVcmw6Imh0dHBzOi8vd3d3LmdzdGF0aWMuY29tL2dlbmVyYXRlXzIw'
    'NCIscHJvYmVJbnRlcnZhbDpgJHtzP3c6aH1zYCxlbmFibGVDb25jdXJyZW5j'
    'eTohMH0pO2NvbnN0IEI9dm9pZCAwO3JldHVybntyZW1hcmtzOmUsdmVyc2lv'
    'bjp7bWluOiIyNi4yLjYifSxsb2c6e2xvZ2xldmVsOmZ9LGRuczphd2FpdCBj'
    'aChhLG8scyxjLHUsbCksaW5ib3VuZHM6W3doKEEsbyxkKSxoaChBKV0sb3V0'
    'Ym91bmRzOlsuLi50LHtwcm90b2NvbDoiZG5zIixzZXR0aW5nczp7cnVsZXM6'
    'W3thY3Rpb246ImhpamFjayJ9XX0sdGFnOiJkbnMtb3V0In0se3Byb3RvY29s'
    'OiJmcmVlZG9tIixzZXR0aW5nczp7ZG9tYWluU3RyYXRlZ3k6IlVzZUlQIn0s'
    'dGFnOiJkaXJlY3QifSx7cHJvdG9jb2w6ImJsYWNraG9sZSIsc2V0dGluZ3M6'
    'e3Jlc3BvbnNlOnt0eXBlOiJodHRwIn19LHRhZzoiYmxvY2sifV0scm91dGlu'
    'Zzp7ZG9tYWluU3RyYXRlZ3k6IklQSWZOb25NYXRjaCIscnVsZXM6bGgobixy'
    'LG8scyksYmFsYW5jZXJzOnB9LG9ic2VydmF0b3J5OkUscG9saWN5OntsZXZl'
    'bHM6ezA6e2Nvbm5JZGxlOjMwMCxoYW5kc2hha2U6NCx1cGxpbmtPbmx5OjEs'
    'ZG93bmxpbmtPbmx5OjF9fSxzeXN0ZW06e3N0YXRzT3V0Ym91bmRVcGxpbms6'
    'ITAsc3RhdHNPdXRib3VuZERvd25saW5rOiEwfX0sc3RhdHM6e319fWFzeW5j'
    'IGZ1bmN0aW9uIGJoKGUsdCxyLG4saSl7Y29uc3Qgcz0hIW4ubGVuZ3RoLG89'
    'dm9pZCAwLGE9dm9pZCAwLGM9YPCfkqYgJHtzPyLwn5SXICI6IiJ9QmVzdCBQ'
    'aW5nJHtpPyIgRiI6IiJ9IPCfmoBgLHU9Wy4uLm4sLi4ucl0sbD1hd2FpdCB2'
    'aChjLHUsITAscywhMCwhMSwhMSx0KTtzJiZhd2FpdCBiaChlLHQscixbXSxp'
    'KSxlLnB1c2gobCl9YXN5bmMgZnVuY3Rpb24gUmgoZSx0KXtjb25zdHtodHRw'
    'Q29uZmlnOntob3N0TmFtZTpyfSxzZXR0aW5nczp7ZnJhZ21lbnRJbnRlcnZh'
    'bE1pbjpuLGZyYWdtZW50SW50ZXJ2YWxNYXg6aX0sZGljdDp7X1ZMXzpzfX09'
    'Z2xvYmFsVGhpcyxvPSEhdCxhPVtdLGM9dm9pZCAwO1siMS01IiwiMS0xMCIs'
    'IjEwLTIwIiwiMjAtMzAiLCIzMC00MCIsIjQwLTUwIiwiNTAtNjAiLCI2MC03'
    'MCIsIjcwLTgwIiwiODAtOTAiLCI5MC0xMDAiLCIxMC0zMCIsIjIwLTQwIiwi'
    'MzAtNTAiLCI0MC02MCIsIjUwLTcwIiwiNjAtODAiLCI3MC05MCIsIjgwLTEw'
    'MCIsIjEwMC0yMDAiXS5mb3JFYWNoKChlLGMpPT57aWYobyl7Y29uc3QgZT1D'
    'aCh0LGBjaGFpbi0ke2MrMX1gLGBwcm94eS0ke2MrMX1gKTthLnB1c2goZSl9'
    'Y29uc3QgdT1waChgcHJveHktJHtjKzF9YCxzLHIsNDQzLCEwLGUsYCR7bn0t'
    'JHtpfWApO2EucHVzaCh1KX0pO2NvbnN0IHU9bz8i8J+UlyAiOiIiLGw9YXdh'
    'aXQgdmgoYPCfkqYgJHt1fUJlc3QgRnJhZ21lbnQg8J+YjmAsYSwhMCxvLCEx'
    'LCExLCExLFtdLHIpO3QmJmF3YWl0IFJoKGUpLGUucHVzaChsKX1hc3luYyBm'
    'dW5jdGlvbiBNaChlKXtjb25zdCB0PUFoKCEwLCExLCJwcm94eSIpLHI9QWgo'
    'ITEsITAsInVkcC1ub2lzZSIpLG49dm9pZCAwLGk9W3QsQWgoITAsITEsImh0'
    'dHAtZnJhZ21lbnQiLHZvaWQgMCx2b2lkIDAsIjEtMSIpLHJdLHM9YXdhaXQg'
    'dmgoIvCfkqYgMSAtIFdvcmtlcmxlc3Mg4q2QIixpLCExLCExLCExLCExLCEw'
    'LFtdLHZvaWQgMCwiY2xvdWRmbGFyZS1kbnMuY29tIixbImNsb3VkZmxhcmUu'
    'Y29tIl0pLG89YXdhaXQgdmgoIvCfkqYgMiAtIFdvcmtlcmxlc3Mg4q2QIixp'
    'LCExLCExLCExLCExLCEwLFtdLHZvaWQgMCwiZG5zLmdvb2dsZSIsWyI4Ljgu'
    'OC44IiwiOC44LjQuNCJdKTtlLnB1c2gocyxvKX1hc3luYyBmdW5jdGlvbiBr'
    'aChlKXtjb25zdHtvdXRQcm94eTp0LHBvcnRzOnIsdXBzdHJlYW1QYXJhbXM6'
    'e3Vwc3RyZWFtU2VydmVyOm4sdXBzdHJlYW1Qb3J0Oml9fT1nbG9iYWxUaGlz'
    'LnNldHRpbmdzLHM9dD9CaCgpOnZvaWQgMCxvPWF3YWl0IHhsKGUpLGE9ci5m'
    'aWx0ZXIodD0+IWV8fExsKHQpKSxjPVRsKCk7biYmaSYmIWUmJihhLnVuc2hp'
    'ZnQoaSksby51bnNoaWZ0KG4pKTtjb25zdCB1PVtdLGw9W10sZD1bXTtsZXQg'
    'dz0xO2Zvcihjb25zdCB0IG9mIGMpe2xldCByPTE7Zm9yKGNvbnN0IGMgb2Yg'
    'YSlmb3IoY29uc3QgYSBvZiBvKXtpZihjPT09aSE9KGE9PT1uKSljb250aW51'
    'ZTtjb25zdCBvPXBoKCJwcm94eSIsdCxhLGMsZSksaD1DaChvLGBwcm94eS0k'
    'e3d9YCk7bC5wdXNoKGgpO2NvbnN0IGY9dmwocixjLGEsdCxlLCExKSxBPWF3'
    'YWl0IHZoKGYsW29dLCExLCExLCExLCExLCExLFthXSk7aWYodS5wdXNoKEEp'
    'LHMpe2NvbnN0IG49dmwocixjLGEsdCxlLCEwKSxpPWF3YWl0IHZoKG4sW3Ms'
    'b10sITEsITAsITEsITEsITEsW2FdKTt1LnB1c2goaSk7Y29uc3QgbD1DaChz'
    'LGBjaGFpbi0ke3d9YCxgcHJveHktJHt3fWApO2QucHVzaChsKX1yKyssdysr'
    'fX1yZXR1cm4gYXdhaXQgYmgodSxvLGwsZCxlKSxlJiYoYXdhaXQgUmgodSxz'
    'KSxhd2FpdCBNaCh1KSksbmV3IFJlc3BvbnNlKEpTT04uc3RyaW5naWZ5KHUs'
    'bnVsbCw0KSx7c3RhdHVzOjIwMCxoZWFkZXJzOnsiQ29udGVudC1UeXBlIjoi'
    'dGV4dC9wbGFpbjtjaGFyc2V0PXV0Zi04IiwiQ2FjaGUtQ29udHJvbCI6Im5v'
    'LXN0b3JlIiwiQ0ROLUNhY2hlLUNvbnRyb2wiOiJuby1zdG9yZSJ9fSl9YXN5'
    'bmMgZnVuY3Rpb24gU2goZSx0LHIsbil7Y29uc3R7d2FycEVuZHBvaW50czpp'
    'fT1nbG9iYWxUaGlzLnNldHRpbmdzLHt3YXJwQWNjb3VudHM6c309YXdhaXQg'
    'WGwoZSx0KSxvPXI/IiBQcm8gIjoiICIsYT1bXSxjPVtdLHU9W10sbD1bXTtm'
    'b3IoY29uc3RbZSx0XW9mIGkuZW50cmllcygpKXtjb25zdHtob3N0Oml9PVBs'
    'KHQpO21sKGkpJiZsLnB1c2goaSk7Y29uc3QgZD1FaChzWzBdLHQsITEscixu'
    'KSx3PUVoKHNbMV0sdCwhMCxyLG4pLGg9YXdhaXQgdmgoYPCfkqYgJHtlKzF9'
    'IC0gV2FycCR7b33wn4eu8J+Ht2AsW2RdLCExLCExLCExLCEwLCExLFtpXSks'
    'Zj1hd2FpdCB2aChg8J+SpiAke2UrMX0gLSBXb1cke2998J+MjWAsW3csZF0s'
    'ITEsITAsITEsITAsITEsW2ldKTthLnB1c2goaCxmKTtjb25zdCBBPUNoKGQs'
    'YHByb3h5LSR7ZSsxfWApO2MucHVzaChBKTtjb25zdCBwPUNoKHcsYGNoYWlu'
    'LSR7ZSsxfWAsYHByb3h5LSR7ZSsxfWApO3UucHVzaChwKX1jb25zdCBkPWF3'
    'YWl0IHZoKGDwn5KmIFdhcnAke299LSBCZXN0IFBpbmcg8J+agGAsWy4uLmNd'
    'LCEwLCExLCExLCEwLCExLGwpLHc9YXdhaXQgdmgoYPCfkqYgV29XJHtvfS0g'
    'QmVzdCBQaW5nIPCfmoBgLFsuLi51LC4uLmNdLCEwLCEwLCExLCEwLCExLGwp'
    'O3JldHVybiBhLnB1c2goZCx3KSxuZXcgUmVzcG9uc2UoSlNPTi5zdHJpbmdp'
    'ZnkoYSxudWxsLDQpLHtzdGF0dXM6MjAwLGhlYWRlcnM6eyJDb250ZW50LVR5'
    'cGUiOiJ0ZXh0L3BsYWluO2NoYXJzZXQ9dXRmLTgiLCJDYWNoZS1Db250cm9s'
    'Ijoibm8tc3RvcmUiLCJDRE4tQ2FjaGUtQ29udHJvbCI6Im5vLXN0b3JlIn19'
    'KX1mdW5jdGlvbiBDaChlLHQscil7Y29uc3Qgbj1zdHJ1Y3R1cmVkQ2xvbmUo'
    'ZSk7cmV0dXJuIG4udGFnPXQsciYmbi5zdHJlYW1TZXR0aW5ncz8uc29ja29w'
    'dCYmKG4uc3RyZWFtU2V0dGluZ3Muc29ja29wdC5kaWFsZXJQcm94eT1yKSxu'
    'fWltcG9ydHtjb25uZWN0IGFzIF9ofWZyb20iY2xvdWRmbGFyZTpzb2NrZXRz'
    'Ijt2YXIgT2g9MSxQaD0yO2FzeW5jIGZ1bmN0aW9uIExoKGUsdCxyLG4saSxz'
    'LG8pe2FzeW5jIGZ1bmN0aW9uIGEodCxyKXtjb25zdCBpPV9oKHtob3N0bmFt'
    'ZTp0LHBvcnQ6cn0pO2UudmFsdWU9aSxvKGBjb25uZWN0ZWQgdG8gJHt0fTok'
    'e3J9YCk7Y29uc3Qgcz1pLndyaXRhYmxlLmdldFdyaXRlcigpO3JldHVybiBh'
    'd2FpdCBzLndyaXRlKG4pLHMucmVsZWFzZUxvY2soKSxpfWFzeW5jIGZ1bmN0'
    'aW9uIGMoKXtjb25zdHtwcm94eU1vZGU6ZSxwYW5lbElQczpuLGVudlByb3h5'
    'SVBzOmMsZGVmYXVsdFByb3h5SVBzOnUsZW52UHJlZml4ZXM6bCxkZWZhdWx0'
    'UHJlZml4ZXM6ZH09Z2xvYmFsVGhpcy53c0NvbmZpZyx3PWU9PmVbTWF0aC5m'
    'bG9vcihNYXRoLnJhbmRvbSgpKmUubGVuZ3RoKV0saD1lPT5lP2Uuc3BsaXQo'
    'IiwiKS5tYXAoZT0+ZS50cmltKCkpLmZpbHRlcihCb29sZWFuKTp2b2lkIDA7'
    'aWYoInByb3h5aXAiPT09ZSl7byhgZGlyZWN0IGNvbm5lY3Rpb24gZmFpbGVk'
    'LCB0cnlpbmcgdG8gdXNlIFByb3h5IElQIGZvciAke3R9YCk7Y29uc3QgZT12'
    'b2lkIDAsaT13KG4/Lmxlbmd0aD9uOmgoYyk/P3UpLHtob3N0OnMscG9ydDph'
    'fT1QbChpLCEwKTt0PXN8fHQscj1hfHxyfWVsc2UgaWYoInByZWZpeCI9PT1l'
    'KXtvKGBkaXJlY3QgY29ubmVjdGlvbiBmYWlsZWQsIHRyeWluZyB0byBnZW5l'
    'cmF0ZSBkeW5hbWljIHByZWZpeCBmb3IgJHt0fWApO2NvbnN0IGU9dm9pZCAw'
    'LHI9dyhuPy5sZW5ndGg/bjpoKGwpPz9kKSxzPWF3YWl0IFhoKHQscik7cz90'
    'PXM6aS5jbG9zZSgxMDExLCJSZXRyeSBjb25uZWN0aW9uIGZhaWxlZDogSW52'
    'YWxpZCBQcmVmaXgiKX10cnl7Y29uc3QgZT1hd2FpdCBhKHQscik7ZS5jbG9z'
    'ZWQuY2F0Y2goZT0+Y29uc29sZS5sb2coInJldHJ5IFRDUCBzb2NrZXQgY2xv'
    'c2VkIGVycm9yIixlKSkuZmluYWxseSgoKT0+emgoaSkpLEloKGUsaSxzLG51'
    'bGwsbyl9Y2F0Y2goZSl7Y29uc29sZS5lcnJvcigiUmV0cnkgY29ubmVjdGlv'
    'biBmYWlsZWQ6IixlKSxpLmNsb3NlKDEwMTEsYFJldHJ5IGNvbm5lY3Rpb24g'
    'ZmFpbGVkOiAke0hsKGUpfWApfX10cnl7Y29uc3QgZT12b2lkIDA7SWgoYXdh'
    'aXQgYSh0LHIpLGkscyxjLG8pfWNhdGNoKGUpe2NvbnNvbGUuZXJyb3IoYENv'
    'bm5lY3Rpb24gZmFpbGVkOiAke2V9YCksaS5jbG9zZSgxMDExLGBDb25uZWN0'
    'aW9uIGZhaWxlZDogJHtIbChlKX1gKX19YXN5bmMgZnVuY3Rpb24gSWgoZSx0'
    'LHIsbixpKXtsZXQgcz1yLG89ITE7Y29uc3QgYT1uZXcgV3JpdGFibGVTdHJl'
    'YW0oe3N0YXJ0KCl7fSxhc3luYyB3cml0ZShlLHIpe289ITAsMSE9PXQucmVh'
    'ZHlTdGF0ZSYmci5lcnJvcigid2ViU29ja2V0LnJlYWR5U3RhdGUgaXMgbm90'
    'IG9wZW4sIG1heWJlIGNsb3NlIikscz8odC5zZW5kKGF3YWl0IG5ldyBCbG9i'
    'KFtzLGVdKS5hcnJheUJ1ZmZlcigpKSxzPW51bGwpOnQuc2VuZChlKX0sY2xv'
    'c2UoKXtpKGByZW1vdGVDb25uZWN0aW9uLnJlYWRhYmxlIGlzIGNsb3NlIHdp'
    'dGggaGFzSW5jb21pbmdEYXRhIGlzICR7b31gKX0sYWJvcnQodCl7Y29uc29s'
    'ZS5lcnJvcigicmVtb3RlQ29ubmVjdGlvbi5yZWFkYWJsZSBhYm9ydCIsdCks'
    'TmgoZSl9fSk7dHJ5e2F3YWl0IGUucmVhZGFibGUucGlwZVRvKGEpfWNhdGNo'
    'KHIpe2NvbnNvbGUuZXJyb3IoIlZMUmVtb3RlU29ja2V0VG9XUyBoYXMgZXhj'
    'ZXB0aW9uLiIsciksTmgoZSksemgodCl9ITE9PT1vJiZuJiYoaSgicmV0cnki'
    'KSxuKCkpfWZ1bmN0aW9uIERoKGUsdCxyKXtsZXQgbj0hMTtjb25zdCBpPXZv'
    'aWQgMDtyZXR1cm4gbmV3IFJlYWRhYmxlU3RyZWFtKHtzdGFydChpKXtlLmFk'
    'ZEV2ZW50TGlzdGVuZXIoIm1lc3NhZ2UiLGU9PntufHxpLmVucXVldWUoZS5k'
    'YXRhKX0pLGUuYWRkRXZlbnRMaXN0ZW5lcigiY2xvc2UiLCgpPT57emgoZSks'
    'bnx8aS5jbG9zZSgpfSksZS5hZGRFdmVudExpc3RlbmVyKCJlcnJvciIsZT0+'
    'e3IoIndlYlNvY2tldFNlcnZlciBoYXMgZXJyb3IiKSxpLmVycm9yKGUpfSk7'
    'Y29uc3R7ZWFybHlEYXRhOnMsZXJyb3I6b309VWgodCk7bz9pLmVycm9yKG8p'
    'OnMmJmkuZW5xdWV1ZShzKX0scHVsbChlKXt9LGNhbmNlbCh0KXtufHwocihg'
    'UmVhZGFibGVTdHJlYW0gd2FzIGNhbmNlbGVkLCBkdWUgdG8gJHt0fWApLG49'
    'ITAsemgoZSkpfX0pfWZ1bmN0aW9uIFVoKGUpe2lmKCFlKXJldHVybntlYXJs'
    'eURhdGE6bnVsbCxlcnJvcjpudWxsfTt0cnl7ZT1lLnJlcGxhY2UoLy0vZywi'
    'KyIpLnJlcGxhY2UoL18vZywiLyIpO2NvbnN0IHQ9YXRvYihlKSxyPXZvaWQg'
    'MDtyZXR1cm57ZWFybHlEYXRhOlVpbnQ4QXJyYXkuZnJvbSh0LGU9PmUuY2hh'
    'ckNvZGVBdCgwKSkuYnVmZmVyLGVycm9yOm51bGx9fWNhdGNoKGUpe3JldHVy'
    'bntlYXJseURhdGE6bnVsbCxlcnJvcjplfX19ZnVuY3Rpb24gTmgoZSl7aWYo'
    'ZSl0cnl7ZS5jbG9zZSgpfWNhdGNoKGUpe2NvbnNvbGUuZXJyb3IoIkZhaWxl'
    'ZCB0byBjbG9zZSBUQ1Agc29ja2V0OiIsZSl9fWZ1bmN0aW9uIHpoKGUpe3Ry'
    'eXsxIT09ZS5yZWFkeVN0YXRlJiYyIT09ZS5yZWFkeVN0YXRlfHxlLmNsb3Nl'
    'KCl9Y2F0Y2goZSl7Y29uc29sZS5lcnJvcigic2FmZUNsb3NlV2ViU29ja2V0'
    'IGVycm9yIixlKX19YXN5bmMgZnVuY3Rpb24gWGgoZSx0KXtsZXQgcj1lO2lm'
    'KCFTbChlKSl7Y29uc3R7aXB2NDp0fT1hd2FpdCBnbChlLCEwKTtpZighdC5s'
    'ZW5ndGgpdGhyb3cgbmV3IEVycm9yKCJVbmFibGUgdG8gZmluZCBJUHY0IGlu'
    'IEROUyByZWNvcmRzIik7cj10WzBdfXJldHVybiBGaChyLHQpfWZ1bmN0aW9u'
    'IEZoKGUsdCl7Y29uc3Qgcj1lLnNwbGl0KCIuIik7aWYoNCE9PXIubGVuZ3Ro'
    'KXRocm93IG5ldyBFcnJvcigiSW52YWxpZCBJUHY0IGFkZHJlc3MiKTtjb25z'
    'dCBuPXIubWFwKGU9Pntjb25zdCB0PXBhcnNlSW50KGUsMTApO2lmKHQ8MHx8'
    'dD4yNTUpdGhyb3cgbmV3IEVycm9yKCJJbnZhbGlkIElQdjQgYWRkcmVzcyIp'
    'O3JldHVybiB0LnRvU3RyaW5nKDE2KS5wYWRTdGFydCgyLCIwIil9KSxpPXQu'
    'bWF0Y2goL15cWyhbMC05QS1GYS1mOl0rKVxdJC8pO2lmKGkpcmV0dXJuYFsk'
    'e2lbMV19JHtuWzBdfSR7blsxXX06JHtuWzJdfSR7blszXX1dYH1hc3luYyBm'
    'dW5jdGlvbiBqaChlKXtjb25zdCB0PW5ldyBXZWJTb2NrZXRQYWlyLFtyLG5d'
    'PU9iamVjdC52YWx1ZXModCk7bi5hY2NlcHQoKSxuLmJpbmFyeVR5cGU9ImFy'
    'cmF5YnVmZmVyIjtsZXQgaT0iIixzPSIiO2NvbnN0IG89KGUsdCk9Pntjb25z'
    'b2xlLmxvZyhgWyR7aX06JHtzfV0gJHtlfWAsdHx8IiIpfSxhPWUuaGVhZGVy'
    'cy5nZXQoInNlYy13ZWJzb2NrZXQtcHJvdG9jb2wiKXx8IiIsYz1EaChuLGEs'
    'byk7bGV0IHU9e3ZhbHVlOm51bGx9LGw9bnVsbCxkPSExO2NvbnN0IHc9bmV3'
    'IFdyaXRhYmxlU3RyZWFtKHthc3luYyB3cml0ZShlKXtpZihkJiZsKXJldHVy'
    'biBsKGUpO2lmKHUudmFsdWUpe2NvbnN0IHQ9dS52YWx1ZS53cml0YWJsZS5n'
    'ZXRXcml0ZXIoKTtyZXR1cm4gYXdhaXQgdC53cml0ZShlKSx2b2lkIHQucmVs'
    'ZWFzZUxvY2soKX1jb25zdHt1c2VySUQ6dH09Z2xvYmFsVGhpcy5nbG9iYWxD'
    'b25maWcse2hhc0Vycm9yOnIsbWVzc2FnZTphLHBvcnRSZW1vdGU6Yz00NDMs'
    'YWRkcmVzc1JlbW90ZTp3PSIiLHJhd0RhdGFJbmRleDpoLFZMVmVyc2lvbjpm'
    'PW5ldyBVaW50OEFycmF5KFswLDBdKSxpc1VEUDpBfT1XaChlLHQpO2lmKGk9'
    'dyxzPWAke2N9LS0ke01hdGgucmFuZG9tKCl9ICR7QT8idWRwICI6InRjcCAi'
    'fSBgLHIpdGhyb3cgbmV3IEVycm9yKGEpO2NvbnN0IHA9bmV3IFVpbnQ4QXJy'
    'YXkoW2ZbMF0sMF0pLEU9ZS5zbGljZShoKTtpZihBKXtpZig1Mz09PWMpe2Q9'
    'ITA7Y29uc3R7d3JpdGU6ZX09YXdhaXQgVmgobixwLG8pO3JldHVybiBsPWUs'
    'dm9pZCBhd2FpdCBsKEUpfXRocm93IG5ldyBFcnJvcigiVURQIHByb3h5IG9u'
    'bHkgZW5hYmxlIGZvciBETlMgd2hpY2ggaXMgcG9ydCA1MyIpfWF3YWl0IExo'
    'KHUsdyxjLEUsbixwLG8pfSxjbG9zZSgpe05oKHUudmFsdWUpfSxhYm9ydChl'
    'KXtvKCJyZWFkYWJsZVdlYlNvY2tldFN0cmVhbSBpcyBhYm9ydCIsSlNPTi5z'
    'dHJpbmdpZnkoZSkpfX0pO3JldHVybiBjLnBpcGVUbyh3KS5jYXRjaChlPT57'
    'bygicmVhZGFibGVXZWJTb2NrZXRTdHJlYW0gcGlwZVRvIGVycm9yIixlKSxO'
    'aCh1LnZhbHVlKX0pLG5ldyBSZXNwb25zZShudWxsLHtzdGF0dXM6MTAxLHdl'
    'YlNvY2tldDpyfSl9ZnVuY3Rpb24gV2goZSx0KXtpZihlLmJ5dGVMZW5ndGg8'
    'MjQpcmV0dXJue2hhc0Vycm9yOiEwLG1lc3NhZ2U6ImludmFsaWQgZGF0YSJ9'
    'O2NvbnN0IHI9bmV3IFVpbnQ4QXJyYXkoZS5zbGljZSgwLDEpKSxuPXZvaWQg'
    'MCxpPXZvaWQgMCxzPXZvaWQgMDtpZighKEtoKG5ldyBVaW50OEFycmF5KGUu'
    'c2xpY2UoMSwxNykpKT09PXQpKXJldHVybntoYXNFcnJvcjohMCxtZXNzYWdl'
    'OiJpbnZhbGlkIHVzZXIifTtjb25zdCBvPW5ldyBVaW50OEFycmF5KGUuc2xp'
    'Y2UoMTcsMTgpKVswXSxhPW5ldyBVaW50OEFycmF5KGUuc2xpY2UoMTgrbywx'
    'OCtvKzEpKVswXTtsZXQgYz0hMTtpZigxPT09YSk7ZWxzZXtpZigyIT09YSly'
    'ZXR1cm57aGFzRXJyb3I6ITAsbWVzc2FnZTpgY29tbWFuZCAke2F9IGlzIG5v'
    'dCBzdXBwb3J0ZWQsIGNvbW1hbmQgMDEtdGNwLDAyLXVkcCwwMy1tdXhgfTtj'
    'PSEwfWNvbnN0IHU9MTgrbysxLGw9ZS5zbGljZSh1LHUrMiksZD1uZXcgRGF0'
    'YVZpZXcobCkuZ2V0VWludDE2KDApO2xldCB3PXUrMjtjb25zdCBoPXZvaWQg'
    'MCxmPW5ldyBVaW50OEFycmF5KGUuc2xpY2Uodyx3KzEpKVswXTtsZXQgQT0w'
    'LHA9dysxLEU9IiI7c3dpdGNoKGYpe2Nhc2UgMTpBPTQsRT1uZXcgVWludDhB'
    'cnJheShlLnNsaWNlKHAscCtBKSkuam9pbigiLiIpO2JyZWFrO2Nhc2UgMjpB'
    'PW5ldyBVaW50OEFycmF5KGUuc2xpY2UocCxwKzEpKVswXSxwKz0xLEU9KG5l'
    'dyBUZXh0RGVjb2RlcikuZGVjb2RlKGUuc2xpY2UocCxwK0EpKTticmVhaztj'
    'YXNlIDM6e0E9MTY7Y29uc3QgdD1uZXcgRGF0YVZpZXcoZS5zbGljZShwLHAr'
    'QSkpLHI9W107Zm9yKGxldCBlPTA7ZTw4O2UrKylyLnB1c2godC5nZXRVaW50'
    'MTYoMiplKS50b1N0cmluZygxNikpO0U9ci5qb2luKCI6Iik7YnJlYWt9ZGVm'
    'YXVsdDpyZXR1cm57aGFzRXJyb3I6ITAsbWVzc2FnZTpgaW52YWxpZCBhZGRy'
    'ZXNzVHlwZSBpcyAke2Z9YH19cmV0dXJuIEU/e2hhc0Vycm9yOiExLGFkZHJl'
    'c3NSZW1vdGU6RSxhZGRyZXNzVHlwZTpmLHBvcnRSZW1vdGU6ZCxyYXdEYXRh'
    'SW5kZXg6cCtBLFZMVmVyc2lvbjpyLGlzVURQOmN9OntoYXNFcnJvcjohMCxt'
    'ZXNzYWdlOmBhZGRyZXNzVmFsdWUgaXMgZW1wdHksIGFkZHJlc3NUeXBlIGlz'
    'ICR7Zn1gfX1mdW5jdGlvbiBKaChlLHQ9MCl7Y29uc3Qgcj1bXTtmb3IobGV0'
    'IGU9MDtlPDI1NjsrK2Upci5wdXNoKChlKzI1NikudG9TdHJpbmcoMTYpLnNs'
    'aWNlKDEpKTtyZXR1cm4ocltlW3QrMF1dK3JbZVt0KzFdXStyW2VbdCsyXV0r'
    'cltlW3QrM11dKyItIityW2VbdCs0XV0rcltlW3QrNV1dKyItIityW2VbdCs2'
    'XV0rcltlW3QrN11dKyItIityW2VbdCs4XV0rcltlW3QrOV1dKyItIityW2Vb'
    'dCsxMF1dK3JbZVt0KzExXV0rcltlW3QrMTJdXStyW2VbdCsxM11dK3JbZVt0'
    'KzE0XV0rcltlW3QrMTVdXSkudG9Mb3dlckNhc2UoKX1mdW5jdGlvbiBLaChl'
    'LHQ9MCl7Y29uc3Qgcj1KaChlLHQpO2lmKCFFbChyKSl0aHJvdyBUeXBlRXJy'
    'b3IoIlN0cmluZ2lmaWVkIFVVSUQgaXMgaW52YWxpZCIpO3JldHVybiByfWFz'
    'eW5jIGZ1bmN0aW9uIFZoKGUsdCxyKXtsZXQgbj0hMTtjb25zdCBpPW5ldyBU'
    'cmFuc2Zvcm1TdHJlYW0oe3N0YXJ0KGUpe30sdHJhbnNmb3JtKGUsdCl7Zm9y'
    'KGxldCByPTA7cjxlLmJ5dGVMZW5ndGg7KXtjb25zdCBuPWUuc2xpY2Uocixy'
    'KzIpLGk9bmV3IERhdGFWaWV3KG4pLmdldFVpbnQxNigwKSxzPW5ldyBVaW50'
    'OEFycmF5KGUuc2xpY2UocisyLHIrMitpKSk7cj1yKzIraSx0LmVucXVldWUo'
    'cyl9fSxmbHVzaChlKXt9fSk7aS5yZWFkYWJsZS5waXBlVG8obmV3IFdyaXRh'
    'YmxlU3RyZWFtKHthc3luYyB3cml0ZShpKXtjb25zdCBzPWF3YWl0IGZldGNo'
    'KCJodHRwczovL2Nsb3VkZmxhcmUtZG5zLmNvbS9kbnMtcXVlcnkiLHttZXRo'
    'b2Q6IlBPU1QiLGhlYWRlcnM6eyJjb250ZW50LXR5cGUiOiJhcHBsaWNhdGlv'
    'bi9kbnMtbWVzc2FnZSJ9LGJvZHk6aX0pLG89YXdhaXQgcy5hcnJheUJ1ZmZl'
    'cigpLGE9by5ieXRlTGVuZ3RoLGM9bmV3IFVpbnQ4QXJyYXkoW2E+PjgmMjU1'
    'LDI1NSZhXSk7MT09PWUucmVhZHlTdGF0ZSYmKHIoYGRvaCBzdWNjZXNzIGFu'
    'ZCBkbnMgbWVzc2FnZSBsZW5ndGggaXMgJHthfWApLG4/ZS5zZW5kKGF3YWl0'
    'IG5ldyBCbG9iKFtjLG9dKS5hcnJheUJ1ZmZlcigpKTooZS5zZW5kKGF3YWl0'
    'IG5ldyBCbG9iKFt0LGMsb10pLmFycmF5QnVmZmVyKCkpLG49ITApKX19KSku'
    'Y2F0Y2goZT0+e3IoImRucyB1ZHAgaGFzIGVycm9yIitlKX0pO2NvbnN0IHM9'
    'aS53cml0YWJsZS5nZXRXcml0ZXIoKTtyZXR1cm57YXN5bmMgd3JpdGUoZSl7'
    'YXdhaXQgcy53cml0ZShlKX19fWFzeW5jIGZ1bmN0aW9uIFloKGUpe2NvbnN0'
    'IHQ9bmV3IFdlYlNvY2tldFBhaXIsW3Isbl09T2JqZWN0LnZhbHVlcyh0KTtu'
    'LmFjY2VwdCgpLG4uYmluYXJ5VHlwZT0iYXJyYXlidWZmZXIiO2xldCBpPSIi'
    'LHM9IiI7Y29uc3Qgbz0oZSx0KT0+e2NvbnNvbGUubG9nKGBbJHtpfToke3N9'
    'XSAke2V9YCx0fHwiIil9LGE9ZS5oZWFkZXJzLmdldCgic2VjLXdlYnNvY2tl'
    'dC1wcm90b2NvbCIpfHwiIixjPURoKG4sYSxvKTtsZXQgdT17dmFsdWU6bnVs'
    'bH0sbD1udWxsO2NvbnN0IGQ9bmV3IFdyaXRhYmxlU3RyZWFtKHthc3luYyB3'
    'cml0ZShlLHQpe2lmKG51bGwpcmV0dXJuIGwoZSk7aWYodS52YWx1ZSl7Y29u'
    'c3QgdD11LnZhbHVlLndyaXRhYmxlLmdldFdyaXRlcigpO3JldHVybiBhd2Fp'
    'dCB0LndyaXRlKGUpLHZvaWQgdC5yZWxlYXNlTG9jaygpfWNvbnN0e2hhc0Vy'
    'cm9yOnIsbWVzc2FnZTphLHBvcnRSZW1vdGU6Yz00NDMsYWRkcmVzc1JlbW90'
    'ZTpkPSIiLHJhd0NsaWVudERhdGE6d309WmgoZSk7aWYoaT1kLHM9YCR7Y30t'
    'LSR7TWF0aC5yYW5kb20oKX0gdGNwYCxyKXRocm93IG5ldyBFcnJvcihhKTth'
    'd2FpdCBMaCh1LGQsYyx3LG4sbnVsbCxvKX0sY2xvc2UoKXtOaCh1LnZhbHVl'
    'KX0sYWJvcnQoZSl7bygicmVhZGFibGVXZWJTb2NrZXRTdHJlYW0gaXMgYWJv'
    'cnRlZCIsSlNPTi5zdHJpbmdpZnkoZSkpfX0pO3JldHVybiBjLnBpcGVUbyhk'
    'KS5jYXRjaChlPT57bygicmVhZGFibGVXZWJTb2NrZXRTdHJlYW0gcGlwZVRv'
    'IGVycm9yIixlKSxOaCh1LnZhbHVlKX0pLG5ldyBSZXNwb25zZShudWxsLHtz'
    'dGF0dXM6MTAxLHdlYlNvY2tldDpyfSl9ZnVuY3Rpb24gWmgoZSl7aWYoZS5i'
    'eXRlTGVuZ3RoPDU2KXJldHVybntoYXNFcnJvcjohMCxtZXNzYWdlOiJpbnZh'
    'bGlkIGRhdGEifTtsZXQgdD01Njtjb25zdCByPW5ldyBVaW50OEFycmF5KGUu'
    'c2xpY2UodCw1NykpWzBdLG49bmV3IFVpbnQ4QXJyYXkoZS5zbGljZSg1Nyw1'
    'OCkpWzBdO2lmKDEzIT09cnx8MTAhPT1uKXJldHVybntoYXNFcnJvcjohMCxt'
    'ZXNzYWdlOiJpbnZhbGlkIGhlYWRlciBmb3JtYXQgKG1pc3NpbmcgQ1IgTEYp'
    'In07Y29uc3QgaT0obmV3IFRleHREZWNvZGVyKS5kZWNvZGUoZS5zbGljZSgw'
    'LHQpKSx7VHJQYXNzOnN9PWdsb2JhbFRoaXMuZ2xvYmFsQ29uZmlnO2lmKGkh'
    'PT1HaChzKSlyZXR1cm57aGFzRXJyb3I6ITAsbWVzc2FnZToiaW52YWxpZCBw'
    'YXNzd29yZCJ9O2NvbnN0IG89ZS5zbGljZSg1OCk7aWYoby5ieXRlTGVuZ3Ro'
    'PDYpcmV0dXJue2hhc0Vycm9yOiEwLG1lc3NhZ2U6ImludmFsaWQgU09DS1M1'
    'IHJlcXVlc3QgZGF0YSJ9O2NvbnN0IGE9bmV3IERhdGFWaWV3KG8pLGM9dm9p'
    'ZCAwO2lmKDEhPT1hLmdldFVpbnQ4KDApKXJldHVybntoYXNFcnJvcjohMCxt'
    'ZXNzYWdlOiJ1bnN1cHBvcnRlZCBjb21tYW5kLCBvbmx5IFRDUCAoQ09OTkVD'
    'VCkgaXMgYWxsb3dlZCJ9O2NvbnN0IHU9YS5nZXRVaW50OCgxKTtsZXQgbD0w'
    'LGQ9Mix3PSIiO3N3aXRjaCh1KXtjYXNlIDE6bD00LHc9bmV3IFVpbnQ4QXJy'
    'YXkoby5zbGljZShkLGQrbCkpLmpvaW4oIi4iKTticmVhaztjYXNlIDM6bD1u'
    'ZXcgVWludDhBcnJheShvLnNsaWNlKGQsZCsxKSlbMF0sZCs9MSx3PShuZXcg'
    'VGV4dERlY29kZXIpLmRlY29kZShvLnNsaWNlKGQsZCtsKSk7YnJlYWs7Y2Fz'
    'ZSA0OntsPTE2O2NvbnN0IGU9bmV3IERhdGFWaWV3KG8uc2xpY2UoZCxkK2wp'
    'KSx0PVtdO2ZvcihsZXQgcj0wO3I8ODtyKyspdC5wdXNoKGUuZ2V0VWludDE2'
    'KDIqcikudG9TdHJpbmcoMTYpKTt3PXQuam9pbigiOiIpO2JyZWFrfWRlZmF1'
    'bHQ6cmV0dXJue2hhc0Vycm9yOiEwLG1lc3NhZ2U6YGludmFsaWQgYWRkcmVz'
    'c1R5cGUgaXMgJHt1fWB9fWlmKCF3KXJldHVybntoYXNFcnJvcjohMCxtZXNz'
    'YWdlOmBhZGRyZXNzIGlzIGVtcHR5LCBhZGRyZXNzVHlwZSBpcyAke3V9YH07'
    'Y29uc3QgaD1kK2wsZj1vLnNsaWNlKGgsaCsyKSxBPXZvaWQgMDtyZXR1cm57'
    'aGFzRXJyb3I6ITEsYWRkcmVzc1JlbW90ZTp3LHBvcnRSZW1vdGU6bmV3IERh'
    'dGFWaWV3KGYpLmdldFVpbnQxNigwKSxyYXdDbGllbnREYXRhOm8uc2xpY2Uo'
    'aCs0KX19ZnVuY3Rpb24gR2goZSl7Y29uc3QgdD0oZSx0KT0+ZT4+PnR8ZTw8'
    'MzItdCxyPVszMjM4MzcxMDMyLDkxNDE1MDY2Myw4MTI3MDI5OTksNDE0NDkx'
    'MjY5Nyw0MjkwNzc1ODU3LDE3NTA2MDMwMjUsMTY5NDA3NjgzOSwzMjA0MDc1'
    'NDI4XSxuPVsxMTE2MzUyNDA4LDE4OTk0NDc0NDEsMzA0OTMyMzQ3MSwzOTIx'
    'MDA5NTczLDk2MTk4NzE2MywxNTA4OTcwOTkzLDI0NTM2MzU3NDgsMjg3MDc2'
    'MzIyMSwzNjI0MzgxMDgwLDMxMDU5ODQwMSw2MDcyMjUyNzgsMTQyNjg4MTk4'
    'NywxOTI1MDc4Mzg4LDIxNjIwNzgyMDYsMjYxNDg4ODEwMywzMjQ4MjIyNTgw'
    'LDM4MzUzOTA0MDEsNDAyMjIyNDc3NCwyNjQzNDcwNzgsNjA0ODA3NjI4LDc3'
    'MDI1NTk4MywxMjQ5MTUwMTIyLDE1NTUwODE2OTIsMTk5NjA2NDk4NiwyNTU0'
    'MjIwODgyLDI4MjE4MzQzNDksMjk1Mjk5NjgwOCwzMjEwMzEzNjcxLDMzMzY1'
    'NzE4OTEsMzU4NDUyODcxMSwxMTM5MjY5OTMsMzM4MjQxODk1LDY2NjMwNzIw'
    'NSw3NzM1Mjk5MTIsMTI5NDc1NzM3MiwxMzk2MTgyMjkxLDE2OTUxODM3MDAs'
    'MTk4NjY2MTA1MSwyMTc3MDI2MzUwLDI0NTY5NTYwMzcsMjczMDQ4NTkyMSwy'
    'ODIwMzAyNDExLDMyNTk3MzA4MDAsMzM0NTc2NDc3MSwzNTE2MDY1ODE3LDM2'
    'MDAzNTI4MDQsNDA5NDU3MTkwOSwyNzU0MjMzNDQsNDMwMjI3NzM0LDUwNjk0'
    'ODYxNiw2NTkwNjA1NTYsODgzOTk3ODc3LDk1ODEzOTU3MSwxMzIyODIyMjE4'
    'LDE1MzcwMDIwNjMsMTc0Nzg3Mzc3OSwxOTU1NTYyMjIyLDIwMjQxMDQ4MTUs'
    'MjIyNzczMDQ1MiwyMzYxODUyNDI0LDI0Mjg0MzY0NzQsMjc1NjczNDE4Nywz'
    'MjA0MDMxNDc5LDMzMjkzMjUyOThdLGk9dm9pZCAwLHM9KGU9Pntjb25zdCB0'
    'PVtdO2ZvcihsZXQgcj0wO3I8ZS5sZW5ndGg7cisrKXtsZXQgbj1lLmNoYXJD'
    'b2RlQXQocik7bjwxMjg/dC5wdXNoKG4pOm48MjA0OD90LnB1c2goMTkyfG4+'
    'PjYsMTI4fDYzJm4pOm48NTUyOTZ8fG4+PTU3MzQ0P3QucHVzaCgyMjR8bj4+'
    'MTIsMTI4fG4+PjYmNjMsMTI4fDYzJm4pOihyKyssbj02NTUzNisoKDEwMjMm'
    'bik8PDEwfDEwMjMmZS5jaGFyQ29kZUF0KHIpKSx0LnB1c2goMjQwfG4+PjE4'
    'LDEyOHxuPj4xMiY2MywxMjh8bj4+NiY2MywxMjh8NjMmbikpfXJldHVybiB0'
    'fSkoZSksbz04KnMubGVuZ3RoO2ZvcihzLnB1c2goMTI4KTtzLmxlbmd0aCU2'
    'NCE9NTY7KXMucHVzaCgwKTtjb25zdCBhPU1hdGguZmxvb3Ioby80Mjk0OTY3'
    'Mjk2KSxjPTQyOTQ5NjcyOTUmbztmb3IobGV0IGU9MztlPj0wO2UtLSlzLnB1'
    'c2goYT4+OCplJjI1NSk7Zm9yKGxldCBlPTM7ZT49MDtlLS0pcy5wdXNoKGM+'
    'PjgqZSYyNTUpO2ZvcihsZXQgZT0wO2U8cy5sZW5ndGg7ZSs9NjQpe2NvbnN0'
    'IGk9bmV3IEFycmF5KDY0KS5maWxsKDApO2ZvcihsZXQgdD0wO3Q8MTY7dCsr'
    'KWlbdF09c1tlKzQqdF08PDI0fHNbZSs0KnQrMV08PDE2fHNbZSs0KnQrMl08'
    'PDh8c1tlKzQqdCszXTtmb3IobGV0IGU9MTY7ZTw2NDtlKyspe2NvbnN0IHI9'
    'dChpW2UtMTVdLDcpXnQoaVtlLTE1XSwxOCleaVtlLTE1XT4+PjMsbj10KGlb'
    'ZS0yXSwxNyledChpW2UtMl0sMTkpXmlbZS0yXT4+PjEwO2lbZV09aVtlLTE2'
    'XStyK2lbZS03XStufDB9bGV0W28sYSxjLHUsbCxkLHcsaF09cjtmb3IobGV0'
    'IGU9MDtlPDY0O2UrKyl7Y29uc3Qgcj12b2lkIDAscz12b2lkIDAsZj1oKyh0'
    'KGwsNiledChsLDExKV50KGwsMjUpKSsobCZkXn5sJncpK25bZV0raVtlXXww'
    'LEE9dm9pZCAwLHA9byZhXm8mY15hJmMsRT12b2lkIDA7aD13LHc9ZCxkPWws'
    'bD11K2Z8MCx1PWMsYz1hLGE9byxvPWYrKCh0KG8sMiledChvLDEzKV50KG8s'
    'MjIpKStwfDApfDB9clswXT1yWzBdK298MCxyWzFdPXJbMV0rYXwwLHJbMl09'
    'clsyXStjfDAsclszXT1yWzNdK3V8MCxyWzRdPXJbNF0rbHwwLHJbNV09cls1'
    'XStkfDAscls2XT1yWzZdK3d8MCxyWzddPXJbN10raHwwfXJldHVybiByLnNs'
    'aWNlKDAsNykubWFwKGU9PigiMDAwMDAwMDAiKyhlPj4+MCkudG9TdHJpbmco'
    'MTYpKS5zbGljZSgtOCkpLmpvaW4oIiIpfXZhciBRaD11bChsbCgpLDEpO2Fz'
    'eW5jIGZ1bmN0aW9uIHFoKGUpe2NvbnN0e3BhdGhOYW1lOnR9PWdsb2JhbFRo'
    'aXMuZ2xvYmFsQ29uZmlnLHI9dC5yZXBsYWNlKCIvIiwiIik7dHJ5e2NvbnN0'
    'e3Byb3RvY29sOnQsbW9kZTpuLHBhbmVsSVBzOml9PUpTT04ucGFyc2UoYXRv'
    'YihyKSk7c3dpdGNoKGdsb2JhbFRoaXMud3NDb25maWc9ey4uLmdsb2JhbFRo'
    'aXMud3NDb25maWcsd3NQcm90b2NvbDp0LHByb3h5TW9kZTpuLHBhbmVsSVBz'
    'Oml9LHQpe2Nhc2UidmwiOnJldHVybiBhd2FpdCBqaChlKTtjYXNlInRyIjpy'
    'ZXR1cm4gYXdhaXQgWWgoZSk7ZGVmYXVsdDpyZXR1cm4gYXdhaXQgbGYoZSl9'
    'fWNhdGNoKGUpe3JldHVybiBuZXcgUmVzcG9uc2UoIkZhaWxlZCB0byBwYXJz'
    'ZSBXZWJTb2NrZXQgcGF0aCBjb25maWciLHtzdGF0dXM6NDAwfSl9fWFzeW5j'
    'IGZ1bmN0aW9uICRoKGUsdCl7Y29uc3R7cGF0aE5hbWU6cn09Z2xvYmFsVGhp'
    'cy5nbG9iYWxDb25maWc7c3dpdGNoKHIpe2Nhc2UiL3BhbmVsIjpyZXR1cm4g'
    'YXdhaXQgQWYoZSx0KTtjYXNlIi9wYW5lbC9zZXR0aW5ncyI6cmV0dXJuIGF3'
    'YWl0IHVmKGUsdCk7Y2FzZSIvcGFuZWwvdXBkYXRlLXNldHRpbmdzIjpyZXR1'
    'cm4gYXdhaXQgYWYoZSx0KTtjYXNlIi9wYW5lbC9yZXNldC1zZXR0aW5ncyI6'
    'cmV0dXJuIGF3YWl0IGNmKGUsdCk7Y2FzZSIvcGFuZWwvcmVzZXQtcGFzc3dv'
    'cmQiOnJldHVybiBhd2FpdCBUdyhlLHQpO2Nhc2UiL3BhbmVsL215LWlwIjpy'
    'ZXR1cm4gYXdhaXQgZGYoZSk7Y2FzZSIvcGFuZWwvdXBkYXRlLXdhcnAiOnJl'
    'dHVybiBhd2FpdCBCZihlLHQpO2Nhc2UiL3BhbmVsL2dldC13YXJwLWNvbmZp'
    'Z3MiOnJldHVybiBhd2FpdCB3ZihlLHQpO2RlZmF1bHQ6cmV0dXJuIGF3YWl0'
    'IGxmKGUpfX1hc3luYyBmdW5jdGlvbiBlZihlLHQpe2NvbnN0IHI9dm9pZCAw'
    'O2lmKCFhd2FpdCB5dyhlLHQpKXtjb25zdHt1cmxPcmlnaW46ZX09Z2xvYmFs'
    'VGhpcy5odHRwQ29uZmlnO3JldHVybiBSZXNwb25zZS5yZWRpcmVjdChgJHtl'
    'fS9sb2dpbmAsMzAyKX1jb25zdHtwYXRoTmFtZTpufT1nbG9iYWxUaGlzLmds'
    'b2JhbENvbmZpZztzd2l0Y2gobil7Y2FzZSIvcHJveHktaXAiOnJldHVybiBh'
    'd2FpdCByZigpO2Nhc2UiL3Byb3h5LWlwL2dldCI6cmV0dXJuIGF3YWl0IGhm'
    'KCk7ZGVmYXVsdDpyZXR1cm4gYXdhaXQgbGYoZSl9fWFzeW5jIGZ1bmN0aW9u'
    'IHRmKGUpe2NvbnN0IHQ9dm9pZCAwLHI9KGF3YWl0IEhmKCJINHNJQUFBQUFB'
    'QUFBNFZVMFc3VE1CVDlGVytJZFpYcXBNMDJ0Q1dPSlFZRklXM2F0STRIbmlv'
    'M3ZrbE1IVHV5M2JTbDZoL3dDL3djWDRLY1pHeGpJSlRFaXMrTjd6MzMrTVRr'
    'NFAzTnUvc3Z0MU5VdWtwUzRrY2ttU3BTVUpTVXdEZ2xGVGlHc3BJWkN5Nzlm'
    'UDhCbi9lWVloV2tqWUIxclkxRG1WWU9sRXNQMTRLN011WFFpQXh3T3hrSkpa'
    'eGdFdHVNU1Vnbmg1UTQ0U1RReTl0TGRNc1VTTlNjQmxFUWtiRERpUlJxaVF6'
    'SVZHUmFvZEpBbm9ZNWEvd3NFSm1teExxdEJCb2JyZDBPNDB4TGJlS0ZaTmt5'
    'd2RqVEJ0T0RyOFlYYjA0dThnVGpCY3VXaGRFcnhSOUNlZDdpMmp6NW5IUCtt'
    'TUtXak90MUhOVWI1Si9UZW9OTXNXREg0eEhxN3lBNkcrNFhtbTlIWHJwZENh'
    'SW9YVHdaajE4bmJldmRhOFZNSVZROFRyaXd0V1RiT0pld1NiNnVyQlA1RnZm'
    'S3hSa29CeVpoVWhRS0N3ZVZmWUJ5clJ6T1dTWGtOclpiNjZEQ0s1RjBqQnRt'
    'am5zRmhzbUxIcnZvbi9Bd2NiQnh1SzNVMTJpYkNEZ3pTMXhwRHI5RlhaZkN3'
    'UXRSVDA0dnp0OWYvbFhVU2VTdi8yc1luWjJOME9QUUtWbE9kazk1UHkzYWMr'
    'N1RQWXQzMkhEUC9yMTQ3MjJqZGcwWUp6SW0rOVlyd2JtRXBOKzFFd1BWbm9T'
    'ZHRVall1ZC9MUWdrWERSSThCV08wYWZlTENRV0drbkpDaWFnS2xFbG1iV2RX'
    'YTdKblhrVk11dlRRTy8xS0YvcVFva2ZURTFzejVmUFdmb29iTUZiNERKNUEy'
    'dTY1RmQ4Z3RoV1RFZ3g5K0VmOEtzOXYwdktpcEl6b3p4L2YwVXhYNEVxaENy'
    'UUc1ZERhYUZVY2tMQ01LS2twV2RENWZIcDNkM00zdjU3T1ptOC9UdWR6RWk0'
    'b0NXdEt3alpOTjlyTWlOcFJxVE1tWjA0YlZrQlFnUHZrb0RvZWVIdGNhdzZE'
    'SVVyVEZBMUFzWVVFUGtCSFI0anJiRldCY2tGcnBGYVFLMkZkd0RqdkZyYStH'
    'Z3dURXZZMVNOaUpHN1puenk5YUNXYzVpd1FBQUE9PSIsITApKS5yZXBsYWNl'
    'KCJfX0VSUk9SX01FU1NBR0VfXyIsSGwoZSkpO3JldHVybiBuZXcgUmVzcG9u'
    'c2Uocix7c3RhdHVzOjIwMCxoZWFkZXJzOnsiQ29udGVudC1UeXBlIjoidGV4'
    'dC9odG1sOyBjaGFyc2V0PXV0Zi04In19KX1hc3luYyBmdW5jdGlvbiByZigp'
    'e2NvbnN0IGU9YXdhaXQgSGYoIkg0c0lBQUFBQUFBQUE0MVgyM0xjTmhKOTM2'
    'OUFhSmRGcmtuTXhaSXZuQ0dUV0xhenJwSnJWYkgyWVd1OUZXR0FKb2tJQkxo'
    'QXo4MFRQdVl2OG5YN0pWc2dPYU9SWlRrN2xLaEJvN3ZST04xOUFNMi9lL1Az'
    'ODZ0L1hyNGxGZFlxbi9zM1VVeVhHZWg4WGdFVCtid0daSVJYekRyQTdCOVg3'
    'NUtYZzB5ekdyS1ZoSFZqTEJKdU5JTEdMRmhMZ1ZVbVlDVTVKTjBnbGxxaVpD'
    'cHhuQ25JSmtFK1I0a0s4dGVYcjhrbDA2REk2cFJPNlhRKzZ1VnpKZlVOc2FB'
    'eXlZMG1sWVVpR3hWczVVZFVjbk9rNEhDcndGVUEyS3NGRldMajB0R29NQm9k'
    'TFkwcEZiQkdPc3BOUGVMT1RiOHZXQzNWTnZ2QUVLeGs2dW5IYmIwd3lqMzky'
    'U3kxQUpHYXhuMk8xMldGOGJ2M0Z4ZnhUei8vK09hSDZaalMwNWZ4WkR5bTlN'
    'VjRISThwbmNUSjJaalM2WGo4eE1mMWk0ZkRaUU1NdjNEVGJKOEk2UnJGdHRs'
    'Q0dYNFQ1UE11MkR5MXh1QXVTYmhSeHFZTHhmak5MRWs4MkdBSDRhUHhxK2ZQ'
    'WGhXekpGa3dmbE5hSDlsK3FpaThITmxDUWNJNHloVWNacWIrOFViR0h2a1NR'
    'bmpaRXRIb2UvNkhaVjNGaEZtbjAyWkQvTzlwc3lHMlhMQndISlBoaDA3UG9u'
    'Wmh4SGJua1UxNkVOT3JOZFRtVjBuT3pWS2ozWkozaXBVdWRsdUhVQ2RMT2Jz'
    'WC9vclo4UDZ1b3RueDdDQkMyR0RDbEN4MXlrRWoyUGF2Y1pxeUFzSEdhYnFB'
    'd2xqWUxjd21jZkt6MUdVNjdIcGhObDJjVkRCN2s5Ukd3QUhyZFNVUjdtSDk3'
    'UFRWeXpldnY0cjFaT3FmQitDZW52bm5IdHpQenZ4ekQvSERLbitDK1BUc0xD'
    'YTNyeDczYXJJN0J1ZzQvZ0dud2QyZCtWNFd0YjVsOUc0RkZpVm5hb0MwbGtJ'
    'b21GVWd5d3JUWnhicXR0dmtybXZadEpDWURMVThxNWt0cFU0VUZKaXlKWnE5'
    'd0hhbW5hU0hJSjAwRytLTWtvSU1lVDVDSnByZGpoUnJIS1FPR21ZWnduN0NO'
    'WXo3Ukk3M0FzdUVYTHAwY3Rwczltc3VES0twMCttNDJjek1DbXloekRxdHBC'
    'Q2dXeFF4VnJ1anN2RVI5L0NzTFd0U2JmeWZXY09FOE10TXZJOUQwWFJ1dnhs'
    'L2l5SXRwSFdZOEVxcWJxMEh5dnQrdFVTenJtdldQZG92eHVNdm5PM3VGenVL'
    'VkdQVlQ0ZlRhRGVRU1ZvbzJNdzZ6VVFpMUc3UW41V3NTWjgzbTViV0E3RWxy'
    'aWUyeFBiRWRxZUVqb3N6bXZHbGRjYW1qWkdkcXk3V0ZiT1NvVFE2Y1lBb2Rl'
    'blNFMCtJSjJRY24zaDZQQ0duNDNGODR2bXhrM25lUENIVDAzWSs2b2x1UHVw'
    'UEVOK04rYnlhNUhOWmw0UXI1bHhQN003eU83eE9tTUlzOEtmQ2hTbE5rSlBi'
    'QTJMdUdxYUpGRm5qaDhrS3JKUGVnMThvNitKMThqT2tybVpLZ2MzMzU0bTM4'
    'bkZNOG5tWEZPK2hCTk5uS0o5akh5QmEvelYvTkI5aDFYMjd0R2F6SmU4dkQ0'
    'S0IzMjdIRW04SDd6OE9paVB2YUxSMzJtKzc4eTBJTjhySGtwM2xGNGI1OHFP'
    'VXprY29Ea2E5OW1nSXpIRXJHeVM0YlNDcmpWZ3FJQUlLc0ZuM3ptWGRuYms3'
    'MGhpMUxhUlNRM3llZnQ5NlFuYWtKWVUxTlRtY2gxeG82bTYyRGVNM1ZNQnF4'
    'SHVMcEZDc1REb1NUL2JPZ3RsZnlQQjUwSDhZemVhalBzcDl0RGx6VzgxSnNk'
    'VGNsdzFSaG9tZndMeGh5TUpveDQxMlNEQVRoaTlyMEVqL3N3UzcvUWdLT0Jv'
    'YkJvOE9hU0VkRmtFMFE3c2R6RXpHMWt3aUtRQjVGUWFqeHVjbmtjMm9CQXlp'
    'ZU9lV25JTnpLY1RlTk5WeERjNnhFbExiRHBhRy91cU1EcU9aTE1MdklNTEtt'
    'alhSc0NadnJUVTJ2SDduUFV0ZGtuM3FIU21ZVkNBSVEvSjRaK2pTcXBZazVQ'
    'SE90dGU5RjAwVjZCS3J5QUl1clNZckkwV0lWR29OOW05WEh5Nnk0TXZrbjV5'
    'ZDVPOTZyMmhJQ1hpNzJtMHQrSTBmT3dsaVRRdGozekplaGFHSkljcnlBUlY5'
    'Q3lhM3dCRGVLdkNqTUVBYlJMSE5EQjJ5Zkc0RWZQOFJyYTg3WHhaK2ZPbWJQ'
    'YVNVL290U2VrZnozN1JtVFloWlBwbStPSDArZllyVVgvLzh6SThZanFQaytW'
    'a1VwVUV3MDBkaFhuL1M1Q3VmT1lyODhRNmVUdHB1Z3c4cmZYMm1tKzA2djJl'
    'TjRDRnVDNGpSWEVsK2t3WCs1blZsenBWc0ZvWlpFWjc0N01tbVBZbUNiNnpp'
    'UDhkM3QyL0UwNVBLd3dyOWVyLzlGaVJCKzhDR3Y0MkZyN0hPeTVDVDN0V2ZH'
    'aG5LSmY3L3l0STEzOVM5anBHeXBnRXR6cnNqU0VkdDFITG1HOUJFdStNU3Zm'
    'NWFuWGQ5bFhiYkdKcXh2YTN4NjloWHNGRkFvV3MvRTdYdGdUZStUQ0JHTzgx'
    'V3NtUm9MT1Y3TVYxYmlYQUZHd3d4b2xpQkRzTW95NWtDaTJIdzN6OStKK2Vt'
    'a1gybkhZelNUL3FURHA1aUZORitKNWpsZHlNSmJ2dlR4NUVHTVVaUkc0RDJ6'
    'Q1NDTE11VTRVeDlSR05aQ2JRRWZJOVFoNEcvYkg0d0FvTG95Wk5EVjNiWDBL'
    'NXlMNlJEeW9Ub0ZidGJhUkRGZHhqeWlFOUh3MkhRL1ZQMlB4WEZkRk9rRFFB'
    'QSIsITEpO3JldHVybiBuZXcgUmVzcG9uc2UoZSx7aGVhZGVyczp7IkNvbnRl'
    'bnQtVHlwZSI6InRleHQvaHRtbDsgY2hhcnNldD11dGYtOCJ9fSl9YXN5bmMg'
    'ZnVuY3Rpb24gbmYoZSx0KXtjb25zdHtwYXRoTmFtZTpyfT1nbG9iYWxUaGlz'
    'Lmdsb2JhbENvbmZpZztyZXR1cm4iL2xvZ2luIj09PXI/YXdhaXQgcGYoZSx0'
    'KToiL2xvZ2luL2F1dGhlbnRpY2F0ZSI9PT1yP2F3YWl0IG13KGUsdCk6YXdh'
    'aXQgbGYoZSl9ZnVuY3Rpb24gc2YoKXtyZXR1cm4gQmwoITAsMjAwLCJTdWNj'
    'ZXNzZnVsbHkgbG9nZ2VkIG91dCEiLG51bGwseyJTZXQtQ29va2llIjoiand0'
    'VG9rZW49OyBTZWN1cmU7IFNhbWVTaXRlPU5vbmU7IEV4cGlyZXM9VGh1LCAw'
    'MSBKYW4gMTk3MCAwMDowMDowMCBHTVQiLCJDb250ZW50LVR5cGUiOiJ0ZXh0'
    'L3BsYWluIn0pfWFzeW5jIGZ1bmN0aW9uIG9mKGUsdCl7YXdhaXQgS2woZSx0'
    'KTtjb25zdHtnbG9iYWxDb25maWc6e3BhdGhOYW1lOnJ9LGh0dHBDb25maWc6'
    'e2NsaWVudDpuLHN1YlBhdGg6aX19PWdsb2JhbFRoaXM7c3dpdGNoKHIpe2Nh'
    'c2VgL3N1Yi9ub3JtYWwvJHtpfWA6c3dpdGNoKG4pe2Nhc2UieHJheSI6cmV0'
    'dXJuIGF3YWl0IGtoKCExKTtjYXNlInNpbmctYm94IjpyZXR1cm4gYXdhaXQg'
    'c2goITEpO2Nhc2UiY2xhc2giOnJldHVybiBhd2FpdCB6dygpO2RlZmF1bHQ6'
    'YnJlYWt9Y2FzZWAvc3ViL3Jhdy8ke2l9YDpzd2l0Y2gobil7Y2FzZSJ4cmF5'
    'IjpjYXNlInNpbmctYm94IjpyZXR1cm4gYXdhaXQgVGYoKTtkZWZhdWx0OmJy'
    'ZWFrfWNhc2VgL3N1Yi9mcmFnbWVudC8ke2l9YDpzd2l0Y2gobil7Y2FzZSJ4'
    'cmF5IjpyZXR1cm4gYXdhaXQga2goITApO2Nhc2Uic2luZy1ib3giOnJldHVy'
    'biBhd2FpdCBzaCghMCk7ZGVmYXVsdDpicmVha31jYXNlYC9zdWIvd2FycC8k'
    'e2l9YDpzd2l0Y2gobil7Y2FzZSJ4cmF5IjpyZXR1cm4gYXdhaXQgU2goZSx0'
    'LCExLCExKTtjYXNlInNpbmctYm94IjpyZXR1cm4gYXdhaXQgb2goZSx0KTtj'
    'YXNlImNsYXNoIjpyZXR1cm4gYXdhaXQgWHcoZSx0LCExKTtkZWZhdWx0OmJy'
    'ZWFrfWNhc2VgL3N1Yi93YXJwLXByby8ke2l9YDpzd2l0Y2gobil7Y2FzZSJ4'
    'cmF5IjpyZXR1cm4gYXdhaXQgU2goZSx0LCEwLCExKTtjYXNlInhyYXkta25v'
    'Y2tlciI6cmV0dXJuIGF3YWl0IFNoKGUsdCwhMCwhMCk7Y2FzZSJjbGFzaCI6'
    'cmV0dXJuIGF3YWl0IFh3KGUsdCwhMCk7ZGVmYXVsdDpicmVha31kZWZhdWx0'
    'OnJldHVybiBhd2FpdCBsZihlKX19YXN5bmMgZnVuY3Rpb24gYWYoZSx0KXtp'
    'ZigiUFVUIiE9PWUubWV0aG9kKXJldHVybiBCbCghMSw0MDUsIk1ldGhvZCBu'
    'b3QgYWxsb3dlZC4iKTtjb25zdCByPXZvaWQgMDtpZighYXdhaXQgeXcoZSx0'
    'KSlyZXR1cm4gQmwoITEsNDAxLCJVbmF1dGhvcml6ZWQgb3IgZXhwaXJlZCBz'
    'ZXNzaW9uLiIpO3RyeXtjb25zdCByPXZvaWQgMDtyZXR1cm4gQmwoITAsMjAw'
    'LCIiLGF3YWl0IEZsKGUsdCkpfWNhdGNoKGUpe3JldHVybiBjb25zb2xlLmxv'
    'ZyhlKSxCbCghMSw1MDAsYEVycm9yIG9jY3VycmVkIHdoaWxlIHVwZGF0aW5n'
    'IHNldHRpbmdzOiAke0hsKGUpfWApfX1hc3luYyBmdW5jdGlvbiBjZihlLHQp'
    'e2lmKCJQT1NUIiE9PWUubWV0aG9kKXJldHVybiBCbCghMSw0MDUsIk1ldGhv'
    'ZCBub3QgYWxsb3dlZCEiKTtjb25zdCByPXZvaWQgMDtpZighYXdhaXQgeXco'
    'ZSx0KSlyZXR1cm4gQmwoITEsNDAxLCJVbmF1dGhvcml6ZWQgb3IgZXhwaXJl'
    'ZCBzZXNzaW9uLiIpO3RyeXtjb25zdHtzZXR0aW5nczplfT1nbG9iYWxUaGlz'
    'O3JldHVybiBhd2FpdCB0Lmt2LnB1dCgicHJveHlTZXR0aW5ncyIsSlNPTi5z'
    'dHJpbmdpZnkoZSkpLEJsKCEwLDIwMCwiIixlKX1jYXRjaChlKXtyZXR1cm4g'
    'Y29uc29sZS5sb2coZSksQmwoITEsNTAwLGBFcnJvciBvY2N1cnJlZCB3aGls'
    'ZSByZXNldHRpbmcgc2V0dGluZ3M6ICR7SGwoZSl9YCl9fWFzeW5jIGZ1bmN0'
    'aW9uIHVmKGUsdCl7Y29uc3Qgcj1Cb29sZWFuKGF3YWl0IHQua3YuZ2V0KCJw'
    'd2QiKSksbj12b2lkIDA7aWYoIWF3YWl0IHl3KGUsdCkpcmV0dXJuIEJsKCEx'
    'LDQwMSwiVW5hdXRob3JpemVkIG9yIGV4cGlyZWQgc2Vzc2lvbi4iLHtpc1Bh'
    'c3NTZXQ6cn0pO3RyeXtjb25zdCBuPWF3YWl0IFhsKGUsdCkse3N1YlBhdGg6'
    'aX09Z2xvYmFsVGhpcy5odHRwQ29uZmlnLHM9dm9pZCAwO3JldHVybiBCbCgh'
    'MCwyMDAsdm9pZCAwLHtwcm94eVNldHRpbmdzOm4uc2V0dGluZ3MsaXNQYXNz'
    'U2V0OnIsc3ViUGF0aDppfSl9Y2F0Y2goZSl7cmV0dXJuIGNvbnNvbGUubG9n'
    'KGUpLEJsKCExLDUwMCxgRXJyb3Igb2NjdXJyZWQgd2hpbGUgZmV0Y2hpbmcg'
    'c2V0dGluZ3M6ICR7SGwoZSl9YCl9fWFzeW5jIGZ1bmN0aW9uIGxmKGUpe2Nv'
    'bnN0e2ZhbGxiYWNrRG9tYWluOnR9PWdsb2JhbFRoaXMuZ2xvYmFsQ29uZmln'
    'LHt1cmw6cixtZXRob2Q6bixoZWFkZXJzOmksYm9keTpzfT1lLG89bmV3IFVS'
    'TChyKTtvLmhvc3RuYW1lPXQsby5wcm90b2NvbD0iaHR0cHM6Ijtjb25zdCBh'
    'PW5ldyBSZXF1ZXN0KG8udG9TdHJpbmcoKSx7bWV0aG9kOm4saGVhZGVyczpp'
    'LGJvZHk6cyxyZWRpcmVjdDoibWFudWFsIn0pO3JldHVybiBhd2FpdCBmZXRj'
    'aChhKX1hc3luYyBmdW5jdGlvbiBkZihlKXtjb25zdCB0PWF3YWl0IGUudGV4'
    'dCgpO3RyeXtjb25zdCBlPWF3YWl0IGZldGNoKGBodHRwOi8vaXAtYXBpLmNv'
    'bS9qc29uLyR7dH0/bm9jYWNoZT0ke0RhdGUubm93KCl9YCkscj12b2lkIDA7'
    'cmV0dXJuIEJsKCEwLDIwMCwiIixhd2FpdCBlLmpzb24oKSl9Y2F0Y2goZSl7'
    'cmV0dXJuIGNvbnNvbGUuZXJyb3IoIkVycm9yIGZldGNoaW5nIElQIGFkZHJl'
    'c3M6IixlKSxCbCghMSw1MDAsYEVycm9yIGZldGNoaW5nIElQIGFkZHJlc3M6'
    'ICR7SGwoZSl9YCl9fWFzeW5jIGZ1bmN0aW9uIHdmKGUsdCl7Y29uc3R7aHR0'
    'cENvbmZpZzp7Y2xpZW50OnJ9LGRpY3Q6e19wcm9qZWN0XzpufX09Z2xvYmFs'
    'VGhpcyxpPSJhbW5lemlhIj09PXIscz12b2lkIDA7aWYoIWF3YWl0IHl3KGUs'
    'dCkpcmV0dXJuIG5ldyBSZXNwb25zZSgiVW5hdXRob3JpemVkIG9yIGV4cGly'
    'ZWQgc2Vzc2lvbi4iLHtzdGF0dXM6NDAxfSk7dHJ5e2NvbnN0e3dhcnBBY2Nv'
    'dW50czpyLHNldHRpbmdzOnN9PWF3YWl0IFhsKGUsdCkse3dhcnBJUHY2Om8s'
    'cHVibGljS2V5OmEscHJpdmF0ZUtleTpjfT1yWzBdLHt3YXJwRW5kcG9pbnRz'
    'OnUsd2FycFJlbW90ZUROUzpsLGFtbmV6aWFOb2lzZUNvdW50OmQsYW1uZXpp'
    'YU5vaXNlU2l6ZU1pbjp3LGFtbmV6aWFOb2lzZVNpemVNYXg6aH09cyxmPW5l'
    'dyBRaC5kZWZhdWx0LEE9ZT0+ZS5zcGxpdCgiXG4iKS5tYXAoZT0+ZS50cmlt'
    'KCkpLmpvaW4oIlxuIik7dT8uZm9yRWFjaCgoZSx0KT0+e2NvbnN0IHI9YFtJ'
    'bnRlcmZhY2VdXG4gICAgICAgICAgICAgICAgUHJpdmF0ZUtleSA9ICR7Y31c'
    'biAgICAgICAgICAgICAgICBBZGRyZXNzID0gMTcyLjE2LjAuMi8zMiwgJHtv'
    'fVxuICAgICAgICAgICAgICAgIEROUyA9ICR7bH1cbiAgICAgICAgICAgICAg'
    'ICBNVFUgPSAxMjgwXG4gICAgICAgICAgICAgICAgJHtpP2BKYyA9ICR7ZH1c'
    'biAgICAgICAgICAgICAgICAgICAgSm1pbiA9ICR7d31cbiAgICAgICAgICAg'
    'ICAgICAgICAgSm1heCA9ICR7aH1cbiAgICAgICAgICAgICAgICAgICAgUzEg'
    'PSAwXG4gICAgICAgICAgICAgICAgICAgIFMyID0gMFxuICAgICAgICAgICAg'
    'ICAgICAgICBIMSA9IDBcbiAgICAgICAgICAgICAgICAgICAgSDIgPSAwXG4g'
    'ICAgICAgICAgICAgICAgICAgIEgzID0gMFxuICAgICAgICAgICAgICAgICAg'
    'ICBINCA9IDBgOiIifVxuICAgICAgICAgICAgICAgIFtQZWVyXVxuICAgICAg'
    'ICAgICAgICAgIFB1YmxpY0tleSA9ICR7YX1cbiAgICAgICAgICAgICAgICBB'
    'bGxvd2VkSVBzID0gMC4wLjAuMC8wLCA6Oi8wXG4gICAgICAgICAgICAgICAg'
    'RW5kcG9pbnQgPSAke2V9XG4gICAgICAgICAgICAgICAgUGVyc2lzdGVudEtl'
    'ZXBhbGl2ZSA9IDI1YDtmLmZpbGUoYCR7bn0tV2FycC0ke3QrMX0uY29uZmAs'
    'QShyKSl9KTtjb25zdCBwPWF3YWl0IGYuZ2VuZXJhdGVBc3luYyh7dHlwZToi'
    'YmxvYiJ9KSxFPWF3YWl0IHAuYXJyYXlCdWZmZXIoKTtyZXR1cm4gbmV3IFJl'
    'c3BvbnNlKEUse2hlYWRlcnM6eyJDb250ZW50LVR5cGUiOiJhcHBsaWNhdGlv'
    'bi96aXAiLCJDb250ZW50LURpc3Bvc2l0aW9uIjpgYXR0YWNobWVudDsgZmls'
    'ZW5hbWU9IiR7bn0tV2FycC0ke2k/IlByby0iOiIifWNvbmZpZ3MuemlwImB9'
    'fSl9Y2F0Y2goZSl7cmV0dXJuIEJsKCExLDUwMCxgRXJyb3IgZ2VuZXJhdGlu'
    'ZyBaSVAgZmlsZTogJHtIbChlKX1gKX19YXN5bmMgZnVuY3Rpb24gaGYoKXtj'
    'b25zdCBlPWF3YWl0IGdsKGdsb2JhbFRoaXMuZGljdC5fcHVibGljX3Byb3h5'
    'X2lwXywhMCksdD12b2lkIDA7cmV0dXJuIEJsKCEwLDIwMCx2b2lkIDAsYXdh'
    'aXQgeWYoZS5pcHY0KSl9YXN5bmMgZnVuY3Rpb24gZmYoKXtjb25zdCBlPSJB'
    'QUFCQUFFQVFFQUFBQUVBSUFBb1FnQUFGZ0FBQUNnQUFBQkFBQUFBZ0FBQUFB'
    'RUFJQUFBQUFBQUFFQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FTR3RFQlNzL0tGc1JHUkN5QXdRQzV3QUFBUG9CQWdIdER4WU92eVUy'
    'SW5GRVpEOFFUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FPVlExTGdjTEI5VUFBQUQvQVFF'
    'QS95a2pHUDlBTnliL01Db2Qvd1VFQS84QUFBRC9BZ1FDNnlvL0oxZE1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FPVlUyS3dJREF1NEFBQUQvV2swMS85VzNmLy8xMDVMLzlkT1MvL1hUa3Yv'
    'anhJZi9lbWxJL3dZRkEvOEFBQUQvSmpnalpreHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFcHRSUUUyVURN'
    'M0lqTWdlaFFkRXFzTkZBekhCd3NIenc0VkRjVVdJUldtSlRjamNUcFZOaWxN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FTR3BEQmdjS0J0Y0FBQUQvbFlCWS8v'
    'WFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9UU2tmK3hqRTcvRFFv'
    'Ri93QUJBUGc2VlRZc1RIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBUzI1R0FDMURLbFFIQ3dmWEFBQUEvd0FBQVA4QUFBRC9BQUFBL3dB'
    'QUFQOEFBQUQvQUFBQS93QUFBUDhBQUFEL0RCSUx3elZQTWpoTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUNvL0oxc0FBQUQvVlVrei8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1'
    'TC85ZE9TLy9YVGt2L3h6SWovNUxKaC81dDVRdjhBQUFEL0Vob1JyVXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBUGxzNUlBNFZEYndBQUFEL0JB'
    'TUMvMGsrSy8rVmdGbi95Njk1LytyS2kvLzAwcEgvNk1pSy84YXFkditKZGxI'
    'L055OGgvd0FBQVA4QUFBRDlGeUlWbWtWbFFBMU1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3QVJHUkMwQUFBQS84R21j'
    'Ly8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvNnI5MC8r'
    'U3lZZi9qc1dEL01pWVYvd0FBQVBsQ1lqNFNUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBTmxBeU5RSUVBdW9BQUFEL1MwQXMvOU8yZnYvMTA1TC85ZE9TLy9YVGt2'
    'LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YrL3BISC9MeWtjL3dB'
    'QUFQOEpEUWpTUUY4OEdVeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qklha01GQUFFQTlSNGFFdi8wMHBILzlkT1MvL1hUa3YvMTA1TC85'
    'ZE9TLy9YVGt2LzEwNUwvOHMySy8rU3lZZi9rc21ILzVMSmgvM3BmTS84QUFB'
    'RC9Ma1FyVUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBTzFnM0pRSURBdTBDQVFIL2lYWlIv'
    'L1RTa2YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlk'
    'T1MvL1hUa3YvMTA1TC85ZE9TLys3Tmp2OWJUamIvQUFBQS93a05DTTlHWjBF'
    'S1RIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBT0ZRMEx3QUFBUDli'
    'VGpiLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOU5LUi8raTZi'
    'di9rc21ILzVMSmgvK1N5WWYrWGRrRC9BQUFBL3lvK0oyMU1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'UldaQkRBY0xCdGdBQUFEL2xIOVkvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEw'
    'NUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2'
    'LzEwNUwvOU5LUi8xNVBNLzhBQUFEL0V4d1JwMHR1UmdCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFDMUVLbFlBQUFEL2lYWlIvL1hUa3YvMTA1TC85ZE9T'
    'Ly9YVGt2LzEwNUwvOWRPUy8rM0Zmdi9rc21ILzVMSmgvK1N5WWYva3NtSC9r'
    'WEU5L3dBQUFQOHFQaWRtVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFCc3BHWXdBQUFEL1pWYzgvL1hU'
    'a3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1Mv'
    'L1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi9sdW5IL01T'
    'WVUvd0FBQVA4c1FTbFVUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0FqTkNC'
    'M0FBQUEvNjZXWi8vMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vREtoZi9r'
    'c21MLzVMSmgvK1N5WWYva3NtSC81TEpoLzJST0t2OEFBQUQvTkU0eFBFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFSmhQUk1BQVFEMkV4QUwvK2ZIaXYvMTA1TC85ZE9TLy9YVGt2LzEwNUwv'
    'OWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEw'
    'NUwvOWRPUy8vWFRrdi8xMDVMLzZieHcvN1dOVFA4QUFBRC9DQXdIMGt0dVJn'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQUhTb2Jqd0FBQVAvSnJYZi85ZE9TLy9Y'
    'VGt2LzEwNUwvOWRPUy8vSE1pUC9rczJQLzVMSmgvK1N5WWYva3NtSC81TEpo'
    'LzkydFh2OFdFUW4vQWdNQzYwbHJSQVJNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0FsTnlOdUFBQUEvNFJ5VHYv'
    'MTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hU'
    'a3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1Mv'
    'K2U0YXYva3NtSC9RelFjL3dBQUFQODJVREkyVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBQlloRmFFQUFBRC8zYjZELy9YVGt2LzEwNUwvOWRPUy8vTE5pZi9sdFdY'
    'LzVMSmgvK1N5WWYva3NtSC81TEpoLytPeFlQOWlUQ24vQUFBQS94NHRISVJN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQURoWU91d1FEQXYva3hJZi85ZE9TLy9YVGt2LzEwNUwvOWRP'
    'Uy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwv'
    'OWRPUy8vWFRrdi8xMDVMLzlkT1MvL1RSa1Ava3NtTC81TEpoLzZKK1JQOEFB'
    'QUQvSGl3Y2hreHdSd0JNY0VjQVRIQkhBRXh3UndBU0d4R3hBQUFBLys3Tmp2'
    'LzEwNUwvOWRPUy8vRExodi9sdEdYLzVMSmgvK1N5WWYva3NtSC81TEpoLzlX'
    'bVd2OWJSeWIvQUFBQS93Z01COWRGWmtFTFRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBQUlEQXVjcUpC'
    'bi85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3Yv'
    'MTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hU'
    'a3Yvd3lvWC81TEpoLytTeVlmL2RyRjMvQlFNQy93NFdEcjVNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FEeFlPdmdZR0EvLzEwNUwvOWRPUy8rL0lndi9rc21MLzVM'
    'SmgvK1N5WWYvZ3IxLy9yb2hLLzE5S0tQOExDUVQvQUFBQS93VUlCZDg4V1Rn'
    'a1RIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXB0UlFBQUFBRDhRVGdtLy9YVGt2LzEwNUwvOWRPUy8v'
    'WFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRP'
    'Uy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC82cjkxLytTeVlmL2tzbUgv'
    'NUxKaC95TWNELzhFQmdUaVRIQkhBRXh3UndCTWNFY0FUSEJIQUFzUUNzb1BE'
    'UW4veks5NS83Q1VZZitQYnozL2RGc3gvMVpESlA4eEpoVC9DQWNEL3dBQUFQ'
    'OEFBQUQvQWdNQzdCNHNISVJGWlVBTlRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCSmJFUUFB'
    'QUFBL0VNNUovLzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1'
    'TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3Yv'
    'MTA1TC85TktRLytXMFpQL2tzbUgvNUxKaC8rU3lZZjgxS1JiL0FBQUE4a3h3'
    'UndCTWNFY0FUSEJIQUV4d1J3QUhDd2ZZQUFBQS93QUFBUDhBQUFEL0FBQUEv'
    'd0FBQVA4QUFBRC9BQUVBOHdzUkM4Y2NLaHFRTVVndVNVZHBRd1pNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUFBQkFPMHlLeDcvOWRPUy8vWFRr'
    'di8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8v'
    'WFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLysvSWd2L2tzbUgvNUxK'
    'aC8rU3lZZi9rc21IL01pY1Yvd0FBQU85TWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'SGl3Y2doQVhEcm9aSlJlZUlEQWVnaWs4Sm1RelREQkVQbHc2SUVsc1JBRk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3QUpEZ25SRlJJTS8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85'
    'ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1'
    'TC85ZE9TLy9YVGt2L291MjcvNUxKaC8rU3lZZi9rc21ILzVMSmgveG9VQ3Y4'
    'SEN3ZllUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBRkI0VHB3QUFBUC9j'
    'dllMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRr'
    'di8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2L3l6WXIvNUxKaC8r'
    'U3lZZi9rc21ILzVMSmgvOHlmVnY4QUFBRC9GQjBTcTB4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFDUTFJWFVBQUFEL280eGgvL1hUa3YvMTA1TC85ZE9T'
    'Ly9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85'
    'ZE9TLy9YVGt2LzEwNUwvNnI1MC8rU3lZZi9rc21ILzVMSmgvK1N5WWYrQVpE'
    'Yi9BQUFBL3lZNUkydE1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0EwVGpF'
    'N0FBQUEvMkZVT3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8x'
    'MDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOHM2TC8rU3lZ'
    'di9rc21ILzVMSmgvK1N5WWYvWnFWei9HUk1LL3dBQkFQaEJYendZVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVNHcERCUUVDQWZBWEV3My84dEdRLy9Y'
    'VGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9T'
    'Ly9YVGt2LzEwNUwvOWRPUy8rbThjUC9rc21ILzVMSmgvK1N5WWYva3NtSC9Y'
    'RWNuL3dBQUFQOGFKeG1PVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQURoVE5DNGZMaDJGRGhVTndBVUlCZUFBQUFEcEJ3c0gyUkliRWJN'
    'bE5pSjBQMTQ3RzB4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndBU0hCR3VBQUFBLzhDbGN2LzEwNUwvOWRPUy8vWFRrdi8xMDVM'
    'LzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vRExodi9r'
    'c21ILzVMSmgvK1N5WWYva3NtSC9rWEU5L3dBQUFQOEZDQVhlUldWQURVeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FSV1ZBRGhRZEVxVUFBQUQvQUFBQS93'
    'QUFBUDhQRFFuL0doWVAvd2dIQmY4QUFBRC9BQUFBL3dBQUFQa2FKaGlRUldW'
    'QURFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FLVDBtWUFBQUFQ'
    'OXlZa1QvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9Y'
    'VGt2LzEwNUwvOWRPUy8vVFNrZi9udVd6LzVMSmgvK1N5WWYva3NtSC9tWGhC'
    'L3dZRUF2OENBd0x0T1ZVMkxFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FP'
    'MWczSmdnTUI5Y0FBQUQvS0NJWC81YUJXZi9kdm9ULzlkT1MvL1hUa3YvejBa'
    'RC96YkY2LzROeFR2OGJGeEQvQUFBQS93Y0xCOWs2VlRZc1RIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUVKaVBSQUFBUUQzSGhvUi8vUFJrZi8xMDVMLzlk'
    'T1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi91eDRE'
    'LzVMSmgvK1N5WWYvanNXRC9lbDh6L3dFQkFQOENBd0x3TmxBeU9FeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FObEF5TlFJREF1NEJBQUQvZVdoSS8vSFFr'
    'UC8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvNjhxTS8z'
    'SmlRLzhDQVFIL0FnTUM4VGRSTXpaTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBRXh3UnFRQUFBUCs3b1cvLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2'
    'LzEwNUwvOWRPUy8vWFRrdi8wMFkvLzViVm0vK1N5WWYvZ3IxLy9YVWduL3dB'
    'QUFQOENCQUx1TkU0eE9FeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FQMTA2'
    'SFFNRUEra0FBQUQvaTNkUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85'
    'ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVML2szNVgvd0FBQVA4RUJ3'
    'VGhSV1ZBREV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFERkpMa1FBQUFEL1kxVTYv'
    'L1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzZy'
    'OTEvK1N5WWYvQWxsSC9NQ1VVL3dBQUFQOEpEUWpSUEZrNEpVeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FSbWhDQ1FzUUNzb0FBQUQvZ25CTi8vWFRrdi8x'
    'MDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRr'
    'di8xMDVMLzlkT1MvL1hUa3Y5dFhrSC9BQUFBL3g0c0hJaE1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JLYlVVQUJ3c0gyUTBMQi8vb3lJci85ZE9TLy9YVGt2LzEw'
    'NUwvOWRPUy8vWFRrdi8xMDVMLzhNbUUvK0t4WVArRFpqZi9DUWNEL3dBQUFQ'
    'OFZIeE9nUm1oQkNreHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FTMjVHQUJN'
    'ZEVxZ0FBQUQvYUZrKy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9T'
    'Ly9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC83'
    'ODZPL3lJZUZQOEJBZ0gwUW1JK0VVeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBQ0l5'
    'SDNrQUFBRC9qbnBVLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlOR1Ev'
    'OGFkV3Y4MktoYi9BQUFBL3dJREF2QXBQU2RaVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUNnN0pXSUFBQUQvTGljYi8rL09qdi8xMDVM'
    'LzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8x'
    'MDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2K0dkRkQvQUFBQS95YzZK'
    'V1pNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndBL1hUc2JBQUFBK2lZZ0Z2L3owWkgv'
    'OWRPUy8vWFRrdi8xMDVMLzhNNk8vNEp0U1A4SkJ3VC9BQUFBL3c4V0RyczlX'
    'amtnVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUQ5ZE94'
    'b0NBd0x1Q0FjRS84cXVlUC8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9Y'
    'VGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9T'
    'Ly9YVGt2LzEwNUwvenJGNi93QUFBUDhUSFJLcVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUJNY0Vxd0FBQUQvc0pocC8vWFRrdi8xMDVML3FwSmwveU1l'
    'RmY4QUFBRC9CUWNFNHlvL0tGaExia1lBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV0dVJnQVJHUkN5QUFBQS81Ui9XUC8xMDVMLzlk'
    'T1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVM'
    'LzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vUFJrZjhI'
    'QmdUL0NBd0gxVXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3QXdSeTFKQUFB'
    'QS8xSkhNZi9XdUgvL1NEMHEvd0FBQVA4QUFBRC9GaUVWblVWbFFBNU1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3QXJR'
    'Q2hYQUFBQS8wSTRKLy8wMHBILzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2'
    'LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9Y'
    'VGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVML0ZCRU0vd0VDQWVKTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBU0d0REF3UUhCT0FHQlFQL0Nna0cvd0FBQVA4'
    'TEVBckpOVTR4T2t4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3QkNZajRVQXdRQzZRY0dCUC9Qc252LzlkT1Mv'
    'L1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlk'
    'T1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVM'
    'LzlOS1Ivd2dIQmY4SURBZldUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0FpTXlCekFBQUEvd1VIQk9NcVBpZGNTbTFGQWt4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'RmlFVm5nQUFBUDk3YWtuLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEw'
    'NUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2'
    'LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvOUswZlA4QUFBRC9FaHdScmt4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVIybENCaXRBS1Y5RlpV'
    'QU9USEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBTlU4eE9BQUFBUDRoSEJQLzdjeU4vL1hU'
    'a3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1Mv'
    'L1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlk'
    'T1MvL1hUa3YrTWVWUC9BQUFBL3lZNEkydE1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBU1d4'
    'RUFnb1BDYzBBQUFEL3FKQmovL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwv'
    'OWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YvMTA1TC85ZE9TLy9YVGt2LzEw'
    'NUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hUa3YveTBKRC9LU01ZL3dBQkFQ'
    'ZEFYendWVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFWm5RUTBBQVFEMEFBQUEvd2dIQlA5'
    'bFZqei8xYmQrLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlkT1MvL1hU'
    'a3YvMTA1TC85ZE9TLy9YVGt2LzEwNUwvOWRPUy8vWFRrdi8xMDVMLzlOS1Iv'
    'L0hNaVAvdHczdi9mMmMrL3dBQUFQOFlJeGFaVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVBsczZIUjh0SElVREJBUG9BQUFBL3dNREF2OUlQaXYvcDQ5'
    'aC8rekdnZi93eVlULzhNcUUvL0RKaFAvd3lZUC83OGlDLys3SGdQL3R4WDMv'
    'N01ONi8rdkFkZi9wdkhELzU3aHEvK1N6WXYva3NtSC9vbjVFL3dRREFmOENC'
    'QUxyUVdBOEdFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FTR3BEQlN4QktWVU5GQXpDQUFBQS93QUFBUDhWRVFuL1pFNHEvN0tMUy8v'
    'anNXRC81TEpoLytTeVlmL2tzbUgvNUxKaC8rU3lZZi9rc21ILzVMSmgvK1N5'
    'WWYvaHNGLy9nR1EyL3dZRUF2OEFBUUQ0TVVrdVEweHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFE'
    'bFVOU3daSlJlWEFBRUE5QUFBQVA4QUFBRC9IQllNLzJOTkt2K2hma1QvMXFk'
    'Yi8rU3lZZi9rc21ILzVMSmgvK0d2WC8ramYwWC9MeVFUL3dBQUFQOENBd0x3'
    'TVVndVEweHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRVJrUHc4cVB5'
    'aGVFaHNSc0FBQkFQVUFBQUQvQUFBQS93QUFBUDhXRVFuL0tCOFIveVllRVA4'
    'S0NBVC9BQUFBL3dBQUFQOFBGdzYxUEZrNEpVeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3QkZaa0VLTWtvdlJD'
    'RXhIMzhUSEJHd0NRMEkwZ01GQStRRkJ3VGlDeEVMeUIwckc0ODRValF3VEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FU'
    'SEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNF'
    'Y0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndC'
    'TWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3'
    'UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhB'
    'RXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRI'
    'QkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0Vj'
    'QVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdSd0JN'
    'Y0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFFeHdS'
    'd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhCSEFF'
    'eHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNBVEhC'
    'SEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1jRWNB'
    'VEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3Qk1j'
    'RWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4d1J3'
    'Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJIQUV4'
    'd1J3Qk1jRWNBVEhCSEFFeHdSd0JNY0VjQVRIQkhBRXh3UndCTWNFY0FUSEJI'
    'QUV4d1J3Qk1jRWNBLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8v'
    'Ly8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8v'
    'Ly8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8v'
    'L2dELy8vLy8vLy84QUgvLy8vLy8vL2dBUC8vLytBSC84QUFmLy8vd0FIL3dB'
    'Qi8vLzhBQUgvQUFELy8vZ0FBUDRBQVAvLzhBQUFmZ0FBLy8vZ0FBQitBQUQv'
    'LytBQUFENEFBUC8vd0FBQVBnQUEvLy9BQUFBZUFBSC8vOEFBQUI0QUFmLy93'
    'QUFBSGdBRC8vL0FBQUFlQUFmLy84QUFBQjRBSC8vL3dBQUFIZ0gvLy8vQUFB'
    'QWYvLy8vLzhBQUFCLy8vLy8vd0FBQUgvLy8vLy9BQUFBZi8vLy8vOEFBQUQr'
    'QVAvLy80QUFBUGdBUC8vL2dBQUI4QUFmLy8rQUFBUGdBQS8vLzhBQUI4QUFC'
    'Ly8vd0FBUGdBQUgvLy9nQUIrQUFBUC8vK0FBZndBQUEvLy80QUQrQUFBRC8v'
    'L3dBLzRBQUFQLy8vQUgvQUFBQS8vLzhCLzRBQUFELy8vNFAvZ0FBQVAvLy9q'
    'LzhBQUFBLy8vLy8vZ0FBQUQvLy8vLytBQUFBZi8vLy8vOEFBQUIvLy8vLy84'
    'QUFBUC8vLy8vLytBQUIvLy8vLy8vK0FBUC8vLy8vLy8vQUQvLy8vLy8vLy8v'
    'Ly8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8v'
    'Ly8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8v'
    'Ly8vLy8vLy8vLy8vLy8vLy8vLzg9Iix0PVVpbnQ4QXJyYXkuZnJvbShhdG9i'
    'KGUpLGU9PmUuY2hhckNvZGVBdCgwKSk7cmV0dXJuIG5ldyBSZXNwb25zZSh0'
    'LHtoZWFkZXJzOnsiQ29udGVudC1UeXBlIjoiaW1hZ2UveC1pY29uIiwiQ2Fj'
    'aGUtQ29udHJvbCI6InB1YmxpYywgbWF4LWFnZT04NjQwMCJ9fSl9YXN5bmMg'
    'ZnVuY3Rpb24gQWYoZSx0KXtjb25zdCByPXZvaWQgMDtpZihhd2FpdCB0Lmt2'
    'LmdldCgicHdkIikpe2NvbnN0IHI9dm9pZCAwO2lmKCFhd2FpdCB5dyhlLHQp'
    'KXtjb25zdHt1cmxPcmlnaW46ZX09Z2xvYmFsVGhpcy5odHRwQ29uZmlnO3Jl'
    'dHVybiBSZXNwb25zZS5yZWRpcmVjdChgJHtlfS9sb2dpbmAsMzAyKX19Y29u'
    'c3Qgbj1hd2FpdCBIZigiSDRzSUFBQUFBQUFBQSsxOWEzTWJTWkxZZC8rS1l1'
    'OHNoVjUxTndDSzFHZ0FOcmdVSlkxNEoybTRKRFY3ZHhSM1ZFUVhnSllhWFpp'
    'dUFoOERJdUkrMkE1L3VQUGF1M3RoZS9kOFl6dkM1MWY0b3lNYzRYOHpmOER6'
    'RXh4WmorN3FGd2crWnFRTjczQUVvS3Vyc3JLeXNySXlzNnF5TmxlZWZMRnor'
    'SmQ3VDlHSWo2UGVKbnlpQ01kRG44Uzl6UkhCUVc5elREaEcvUkZPR09IKzY4'
    'Tm43aU9WRnVNeDhVOURjamFoQ1VkOUduTVNjOTg2Q3dNKzhnTnlHdmFKS3g2'
    'Y01BNTVpQ09YOVhGRS9MYlYyK1FoajBqdjhkNWp0SWRqRXFIVGRXL05XOXRz'
    'eXZUTktJemZvNFJFZnRpbk1Sb2xaT0EzQi9nVW5yeXdUNDBNakY5RWhJMEk0'
    'VExiaVBNSjZ6U2IvU0IreDd4K1JLZkJJTUlKOGZwMDNNVHY4SGt6Q2s5WWMw'
    'Qmo3dUl6d3VpWU5OZTlUNzFXczgveXlkNDRqTDArWXdzcXMzUnRVSTU1UTBx'
    'SEVjR1RrSW5hK295dGJRM3dPSXd1L0plWWt5VEUwZjJEaS9FSmpkajlmVHFO'
    'QXhKMDZJUjk0NXdOUjl4NXR2dmloZlA1L3ZhVG42KzFQRy85a2ROdXRUenYw'
    'MWJMYVhsZTIzRTNXcDYzMW1xdEFoRytBdG96SHdmQlYvMHc2VWZFd1ZOT0V4'
    'S1RNNmMvSXYzM09sbjF5bGQ5T3Jsd0FoSVJUcHdnWms1QXorS0k0c0FaaFBH'
    'UUpKTWtqTGtUeGdQcXZDY1hYNTJTaElkOUhEbDBRdUt2d3ZncmdQdDE4bFdm'
    'QnNSaGhQTXdIaktIalhCQ0hFNlNjUmpqeU9IVG1EaW5KQWtISVFtYzA1Q0ZK'
    'MkVVOGd2ajUxZDBNRmdOUWphSjhJVi9FdEgrZTZ1M0tZamE2eVNVOHBucjlt'
    'bEVrODVKaFB2dnU2NDdTY0l4VGk1VTZrOWFuejE4OE5tZzY3cU05R2tjR0c4'
    'ZXJILzJLRGpwdWk3d0xFbEtCVTV3Ly8wd0FacnJWNE1CcEE5b01xNTYrUm44'
    'ZFYyWDQ1T0l1TGpQdzFPU3ZseURQNmdyY1RrNTV5a09KL0FIbGRIRXdDRUlB'
    'a2liY2s3akVsNWhQSm55TWdKbm81Q1RyRFZzaEFONjFsbWJuQ1A0dHo0NVI4'
    'bndCRGRhRGxML2Uyc2JkaGVvRjNNY3hpVFJPQ1E0Q0tlc3MvWm9jaTVxaXdW'
    'ZTFabmE2eUlUaWNpWXhMejRzaVZlWm1Vbk9BakNlS2hCWnkrR2VOSlpLK1kr'
    'b2VlNkZhM2FOclR0Q2h4MVBRcTc0bXVvRFY3TlQyaHdNUlBqVnc2NXp1RVpH'
    'ZE4zSWRxaDA1Z25GK2haaElGcEx4Z25ZM2NhZGt0RVA4VkpvOHdwZHRkOHE1'
    'SkV0K01vSE1hZFBvazVTZVkvY3pvZFBPQWtjVHFkRXpLZ0NabUpOb2ZmQVBL'
    'S2xpZFU0dWtGT0hudmptbEFVbzdYUFY3RjhjL3FPUDdKNHhMSHA4bGxwbTZ2'
    'd1Y4OTA2ZnZxNWgrYlFQK3lrei9aQVArU2t6L1lBUCtTbnlmWWxmRDkwWTFp'
    'emwvYldQRFFkbEhGZi9YTVZ5cGFOdWVqOW96czVkTmtxck9WckJ5NzJXYVBZ'
    'Y3BLWjVwb2FuNFlod0dRVVM2SXhJT1I3enpJQ0hqdVplaU4xTkNzRE9JeUhr'
    'WFB0d2dURWlmaHpUdTlHazBIY2RkU2RCT2UzS09HSTNDQUNuK05PaHNkL09E'
    'VlBObzVmaTJ1M29vRmJPcGRJQjJubTlvRlQzdHVjY2twc2hvRUl6RFlwa2hu'
    'dGhHbzN1NjNHeU1rMkVZZDFwenJ6Q2NsNkZMVmxPRkxGaTJEVGVuN2tJWldx'
    'UnhqVEN6NTU0WWcxbTd4L2hjNmtxZHoxby83V3I2SUpqVkRVR2xvRmFPWDF1'
    'VmNrOG81M1RjZWRDYW5BdmlEOExoTTVxTWx5QnQyckhYNjRaQ0J5amtxOTZo'
    'bHRId2hFWXoyZVIycS9YVDdoSlZpb0hsaHB5TW1SSzczWGRUeHNQQmhhdjBu'
    'QTZiNEQ1eFR3Zy9JMFRpMkJaME1HdEZRWGhhYm1HbjNjMndLUlNJOEFtSlpp'
    'cVhJZnNqTXVCbUtTSFZqdmpGaFBqeGRIeENrbVBIU0lLQ3VZUnBFaDA3akVT'
    'a3p4MTRpUk9DVFpLVVpwbVV1OFJzSElVeGNaVjhhWHNiTjJmcHlobS9jdDZy'
    'bVRPcnBibmQ1UW1PV1NpNjBNUUNlUThZSXBpUmVkcHFjK0lPNHhGSlF0NWwv'
    'WVJHMFFsT0o1Vit2NDhFeUFsT1NHeG1rRVRqb3pEdUpvU0YzNUJPVEdOUzFR'
    'SVlhSXBtZlJ6MUd4dlJDTjFIUUUrN292czZBOXFmc2xJbmxwT2hLMVdxN0ZE'
    'MW9Cc29IMmU1U1ZMaVZaalk3UzZkY3VqWlRxc0tuNFRnd0tWeGRGSEdxZktW'
    'd0N0N2s2S1RKcWw1YjVqZ2k3cmVyUlkzaFNGaTFEbkJqSjNSSkRpZWxSbFlk'
    'dFJHNjZkNVZ2NGpaTjJybTMralBzK0R4UTcyd1Bvc1NZV0E5R21DQlhyQTZY'
    'UHNzVDZPNVV3aVpnRVFUUjFReldYSmFjd0l6NUhGVk16c3VYenlFbkpLRWti'
    'TTZxN0ZGRjB4anMvaytIcllhdFhYMkswZ1MwNzNMVS9ST1phWmU1T0VjdHFu'
    'RVpzVlpvdUVuc2tKNUN6Qmt3NThxTXhDU1FHYTVJUi94YXhTQWJBNDBTaTFY'
    'd0pXRTRSSmFqRlppSjl6Y0NTNFkzdytLMDB6VnlJQ0NJTnhvMEZJUHB1WkU1'
    'Vit3eVk0cmhwd1lGZTRZbHJzVEJJeTk4Qlp3MXhoZkNNK2tpVUVvV0lLWCtY'
    'K0J0RlFLQlowQm1IQ3VOc2ZoVkZRVWFuZ0FpR0dJNXdNQlpueXhTT2NsdFlr'
    'R0NaaDBJVVBsNVB4Sk1KY21CN1RjY3c2N1VHQ2pIOXpMNWxHaEluZWJEOHNk'
    'bWRGM3hrRUwvSkZVUy93RWpvRjc0WUF2bEVGdTlOTzFiT3FIc3NVdVVISU5i'
    'Zk1OVmpGS05VcWhHSWNZd1N0dDFvR0xiUFJiL1JYdmdrZW5reWlpMW0rbFZV'
    'a3Vjb1VRSzJ1SGl6Vm5HOHl1Qkllb201WHU0Y3lKVis5bm9DakwzdWRsZGNE'
    'WFU3WjA0VFJwRE9ob1RGZkdLVE1pRytveFMyVWx6UjVRVEwzeHNyNzVqTHBm'
    'WE1UNlgycnNkbDBuNGV4VUxFRTEyWTYrY2JrSElsUDJUV25PQW1GSUU2YjFy'
    'a0hycng3cU9YY0E4ZmVQYlRlYWpuM3dMTW4wc0RqZHcrdHJjOHhxa2RzMFd3'
    'eER3akhZY1E2TWVVTk9aVG93SVc1eDU2bGpnWmhBeXljVCtkc09nWXF6VXlP'
    'K3hSa2RyNExpc3hhNGtBRnA5TVo0K1E5U1dZR3gzb2JDUmwzRnpaR2x4YVRw'
    'U3Q4aFJHWlpSUGlhTTBaUGNpcjYyV0JrelBlVFFlRlhjZSs1YUU3SDYxblBE'
    'dlNFNm1nWVdzcEJRV0dJdVU1YzVhZWttUVEwVFAzdkNOTU9iTVpPbnZCRkNs'
    'TW9CcUwxdVJjV29OTHR5ZG4vVUJGS0RTNjVzRkQ0d1YyMGw5UzNhaHplUmxx'
    'Qi9CcEFuM1VyWnYyRkVnNS9EVTUxWWpQeHU1UGhOZXBYU2M0RlJBdm9rTTY1'
    'Yk1GZ3o1bkJYZGFDNlRLM0J1R2ZEUTlxZk03TEdGbkdpUUdHVm1ZVnFTVTF6'
    'Q0YvSmg3aWc0M3JFbk5ZZXVnTFp0enVwcTFUUzhwRXE1U1l4UStuSlQ1S2lJ'
    'Y1dCV0FpSEtaRWk0SWRtMWRXL2pUYTNURmdsNVhrQy9wVU8vbWZIWWdaZ1hY'
    'S3k4eC9IbHJPY1VjUjFHcWoydnZSeUphS0VhS3FRbER3bHo0TmZQODZISTZ5'
    'ZVZXa2xNbHBiYWlPUU5kUWRrY0dZc0VVWHA0bmdLNjgxbzVESVZHVno5RFpG'
    'Z0lEM3pLOXZVNnZnVE9BOUJ6cmdDdTNiV0RrODgyV2luckZsdHFDdm8yQ0hy'
    'SnBFQTJQWDROdTBpc1M1M1E4K1BaOVV3eFhiMFhoQXhhRUpUTGcyZkE1RU5G'
    'MzVqQ05CSFJNeEtZdkNWNlJ0SGVKYWNrNWt3YVVhcWl6Z2pFZGtVdGE1ODlh'
    'cDE4bG1mVFI4Q21Hd1UyZmFEWUZGU3pqdmdGK3V4Zk50dzFjRE9ZbmF6ZEJH'
    'YVNySDdCQUZvQTIwdGQxMHF5NVlGbUpjVlNiS01OenU5U21abWVPZkxhYjUw'
    'SlZLcXlPRi9YRkZUZFd0RnE2TVMwTitRNnhLeXkwZTNKdVozdmp3ZVRjL1Jw'
    'cVR2eU5MOEs0dHlUS3lDMTgvamN3MEhneGpSa3BEZ2pMVEg5ZExWZFJVZzg5'
    'K1NpN0cyQi9lVFJTYXZWYXBVd1IrSTVaODlmdzlYU3AxR0VKNHgwR0puZ0JQ'
    'TjBYdERUUnVzbUx2SzhwQlZMaFpxK25WRVlCRUNWVWpQRTh0NHlMdXhTeWNX'
    'TENnazlxeXBUYWVQbXpLN3FNakVmeVJLTk5idktMNkVWaGdwTlozemhocE15'
    'cDRua1A5WnVWTWdIanY1VjRYQ29jQVF1WjcrazBNMmVNbXFxbVdiS3E1dDV0'
    'OVdubGNNb2NNcHBvMlhXU1dyMHVlWFdpVXpYUlNxVXIwV2pja1BLeXg4VnRs'
    'QUZlOWROaTdWVW5YdGpHdUJNRDFienJsTGVCdUU1Q2JyZnVHRWNDS2VLVU5O'
    'YVhkREhXbWF6OVFJSC9FNzVxN0F1cGpBeFpmNjZybDRUZmxaMkpaVHR5T3M1'
    'TzVWNEZzaVlYSXpXOU1kTkhOdXFqK3YzUzRqMnRlMk1sUGlFMFdqS2lTQWUr'
    'TllGTGVGSHhSVFhjRGRhUDRYZFJEOU5LU1FuOEdXWXVkTGhaWW9CYVc5K25i'
    'aGlJOWRNNW1ja0d1UmNnK1pJNjBlVTVUS0tta2tjVkJsM2c0aGkzaEU2ZnJl'
    'Z0FGY0RWdnFWZXNqcEdLMVdxOUtYWGpRV2Y2SWQraytUaE9yU0NRa3FXeTRJ'
    'K292OUQ4Znpna0poUEZTNi82eFF0eW10UmUyU1M2dlpQcmYvUlJwNHRTWWlj'
    'SnRzd1VPQU9OSldRczRTWFFQRHRLQy81RGdkdVB6UlFwdXZpQ29ZZ0U3SzV2'
    'QlVvc0VpM1RlL0d3ZVZ5TGVRTXFXYVVKaFQyOHVtekJYVkxkVFNFekpJQ0J1'
    'NVEwTGRpUFlGdzk1QVljd0FTWVdqM2w1VWJzWmwxWGx2R2t5VUdsczFNdlFv'
    'RW5QL2hDUVpaeVlrd2pCdGxQTlVMcXM1QzdPSnRWQlRVVktDV1RrR2hQOGsy'
    'MzdDNlhBWUVWY0RuTldMMUVTTnlNbDVqZmtGQXJYSTIxTUdTcFpjRHpZV3BI'
    'K0NQNE0vbzcza2F0R2kvS1JtYnlqL2RPMGNmb3FqcVduRm1GMGRpZm5hZEpS'
    'ZXRZcHlQY2ZqSStoek91VmcwbWNZbFB0RmFNTkxUOFIxcTdXTFczYkRTYmhF'
    'd0NYOTlmbDF6c0xvKy9tWUJDRkdzUFNPV0I5TVFJVGpBRFZnR1UvTFQ5aU1N'
    'TXR2bEttd1dwWUE5ZW5EUjNsUXhjMUdZZ3VFeUlWK2hyelA3R1dBdGxzZ3ho'
    'ZEJGUURuODgybTNOcTcyWlFieVVINDlUWkg3ZDVtT0I2aWZvUVprL3U3V2RM'
    'UGJlOUdPT0srQlp2RFg5QWh0WG9vMnllK0NYNHJGQWErWEUyQzFXcllpQ1lx'
    'OHJPSmhvMXhGSkdrcDdlVlF5bkFvOTNiQk9lWHJOdktOd0NsdjZ6ZTVtaXRK'
    'NnVTV2V2NnZhZlhmRlFWNkNCOUJnaGlTZ29EUDl1RnBlQVpDVFJtMDVOeHlQ'
    'M3BKTUNjYUFBTjRaaXllNXRLQ3ZjMmxRRG9iWTRlOUhib2VFeGp0SW56bTk1'
    'UFF1eE9NQWdPM0I4UjVlWDJRdHA4dlBmWS9TV0YxUmxYMExFcEVaaEt0YWZa'
    'RitDYWlNTnFMZmUvT29sdy9CNEpGYzUvVHFMSmNyU0E3ZU1wcVRHUSswRnZz'
    'NW1pblJGZTdUSXprMHhtNzIwSy96a2EwTVNIaVM1Njh1cWc5LzIzdi83OS8v'
    'M2Z2MFl2SUFFOWVYV3cyUlM1QkpEZXBoQU1LSjBCZ09pNnFEeW5rRDRsNU90'
    'cG1KQ2d0OWtVSmVYbjFaamdtSWNIT0JhWVM0VCs1dGRvTytZaDBxbExZVlVB'
    'STVFckp0NFV4d0YrVHlSdS8rVS9vV2Y0UFNtakpHY2p3RVJsbGhqb2twdDBJ'
    'cG9pSkovUGt5bnBQWTJGMTNXektWOFZzZ3h3eEVqdmlYTE5acG1hc3FMcnRv'
    'Q0l5bmIzVGgvMnZ2LzJkMzlBOEt1dUFWbGUyUWFqN0lkdWh2QTZ2OWgrdFVQ'
    'aldESDdkMy80SGRxR1pKQXpLcEdoUVVMSDZNWDJxN28ybGdFcGppbFg4S0hi'
    'SE5IaEMzSktvdDczMy81TE5WU0hTS1RVTlU2WDBDTlVsYzlqQ1hwVEJaSzVQ'
    'R2M0aWNONDJQdWwvSzdKSlpTc25yRGlhbktBQk92dENqRlcrVDRnSjlOaDd3'
    'bDhYa0V1L2FtRnQ5YWxKUWtyWmZxWEw1NGVIQ0FYSFNiMEhiNDcyWDRhRWNa'
    'Y0xvQitqQkkrSVdQS1NTcFI5OFhqVXFJMExTbjVKM3U4cWZpY1RoaFBDQjd2'
    'SmZUOG92Zjl0Ny8vNytpMVNrS0hPM3RJcEYrSlZnNktSQzBQK0pwWTBTbVg1'
    'Yjc3KzM4QncycG5oTU40U1Z4MFdZbEdDdW1hR1BRamd1UGRQZGI3N3UvL0s5'
    'cUJCN1M3eDFBVFBhRmpITVlNZUZYMXU5eUVtT2RjeGFwd0pDN1B4TTJkOUhp'
    'ZUs4QzZ1M3Z1Z1FJaGVUTjl5dkV0bk1XellncW4wMGlDWXBxUUFVa1NvYmd0'
    'dzhiR3FiWWNONXZFMUR0bDgvVFVsSkQwVEo4U2VzYjhkbSt6cVV0ZGw4SmZ2'
    'dGdSZzViMXZ2djl2NE5PM3RPYkcvTllHY3BydXYwUkZaekhscGxONU1xeGhs'
    'NkdoZWFrMWNyMlpJL1pISUpvM0IvaGVFajhFWTZEaUdqRWRrU2kxbEpSWlZ1'
    'RVJFc2JVS1RGWXRRTzkzT29aWSszUVMyRjBwTkN0b0JiK2ZQcW51TVJjOFht'
    'UnRCWGZvTU9YeHlnUFhnczkxc1laSmwxSjRxTmpCVWRXSTFKR0lqWjBPWHBS'
    'SkxidmlpTklOUHphQ0lhMDlqTklmdGJCRW1MRWM0VnVoblNWMmlzMmZIVDN2'
    'ZmYvdXQvanA1bENiV0thNVpGS2E4R2tQeUUzUjhsZEV4NjhxdE9EUW9UTXFE'
    'blBmVmRrNHZoQVU3Q252eXFVeDhvNjRXVTFiekZjWkRRTU9pcDd6b2xKUmlT'
    'SG56VXZIL3dzTlY3OExCVjgvYnJyM3RmZjEzekxzRnhRTWM5K2JVd1QvZ05D'
    'WHJaejF0cmhpZUU4UzlmSE83dmdnZmtGSU9HK0x0L2loNFR4cEZPcXAzSjVN'
    'RUg2UFlpRk5uM3BkUnhHUHZ0RmhyamMvK3oxczNNajhOblgvUysrL1YvRTNQ'
    'K004dzQrbUpDNHNWV3lPR3pMMHdqQkNEOFdQcDRkcjZ1U2dFYnJTODNKOExw'
    'YmUzRWVMcnpmTE1KQlpjbDJOT2Q1NkQxLzA5WmNoR2RudTQ4TitrRUJUKzAz'
    'VUw2b3dPU25KTGtGUjRUYVRvRGxqSU5RZUtWYWxZT2hHcGZEdW9TRTh6ZGQ2'
    'UFUvSGIzbHUzTENlVGYzWHRKQTVMYWNQQlExNk5HZnRsbUUwQyt5OFNiY05M'
    'TFVLcnMyVWxDQnVGNTc5WDI0Y1AxVy9lcndnYm11dC8rYlVxTXE5WFdwaWdv'
    'OWhBSUZkUktpMW9maXhxcW01WWoreDJvb1pMK1JKRk1kQVBhVTJrM1Z2Skw5'
    'dWxKUkUrYTBBUE5nUFpaVTFTamEvSEdnU2E3ckY2ajlCSFJYdEZEMFY0OVhV'
    'SDdIMnZNNzB3WnAyTzA4K1RWc3FPK0wwcnNCUEYyRUNUUTg3LzVhd1EvQ1dP'
    'RUxXVVQ1UUFveXlpZmRtdkdUT0U5cDR4TEhPSFhsWUk1VjY2QW1nQjFVendP'
    'NGxDaWNmQnFkM2tzRHVLd2dBVEFxV1dVR2lkUzNtMzBGd20rUU04U1BJUzky'
    'WGZtTlJvb2dCK2p4MGpqdHZSRVpSWlFGb09aVWpBam54bnZHbmJSb0JBZDE1'
    'UERyR1lXaStoWjd3VTlxM2tMNjJ2VGNlK2wrS3JKTXdxSG85N3pjRGlxTTBi'
    'Z21DYnBIWWl2VzArVW1oZ3ZTRHprbzVkaERPTC9YeUg1YU5KVWQ3WThjVmlq'
    'cHBlZzVTbWVKUXRGUGZQVnlhVzlucXNsMlZMUThYa2xkSHd1OVArTlZ1dm1T'
    'eWtLb3JZckpGbis3aDhxTFpackVjYUFtRWZlZkNHSkE0MTQwTG9walZKNFJT'
    'cVpMNm9ydWlHeFh1THpnMGtVY2lEV2QzLzRyUmlYK0J5SnRCdlR5d0JhR0x6'
    'R0MyakcyalhwazVZdjBzZDhJUUhma0I1N3VQK2VDRy9MYi84UnFZZXJoSlRL'
    'bHNkSUF5cllTaEVia1NpaVBmMmpSbHkwM1hhdjdiWnIzNjcxMnU1YTdkc0h2'
    'YmI3b1BidFJxL3RidHhzTVNRL2p6MDk1eVNKY1lUMjhSblN6cjY3bXM2SUF1'
    'N0taUFl4VG10eWFqbVluZ2p2M0w5QjhLdWZoSUt3MTFERW9KaXBaSWhucVlB'
    'aDJDL2wwOEhnOXBxWTlsYi93OStoZ3pBZVJrUjMyVFUwUnRPL20wOWFGdDJs'
    'R091WE9KbWd6OEZNd05HZE1kUVpUaVlmSXhNQlh2djVGYlZrK1JXMVhHblpN'
    'Zm1rbTA0UUFPVnBISWhOVUhJWktYMjZuVjJKazhuSHZXS1VhM2xHMGl4Sjhi'
    'cEIyWnNPVFhDRkFrRnU3Mlkxb1dSdTFsenFyZHlzYWdmcVl4NzN2dnQzL3dm'
    'VUJERkl0L3Q5aU5WWGtDRnFhNjFBVS8xV0N4SHFTUVV0c1VDUmo4TCtlN1dU'
    'Q2tBcWdkS3dlNjlGV3JwOURQckFsZm11NnZzMHNtYmE4N0xlbTRxaXZmMHY3'
    'bFFNdVpPRWZraFJkUGRPakpkNHhQQ3J6OUVyMkV5OHJCL2pmVXo3NzBraXlp'
    'akw4Ti8rcisvKyttKy8vL1kzLzZQQ09xeVFma1VJa3ZOTHFjbzk5U3lNSU93'
    'UHVnY0xiZmNjZE8vcmFkaUhiN2x3Y3M5Qk5FRTR2a0RQbi80Rllqd1IwVC9D'
    'OXdUZEk2UWwvMnUzSG1HTThUM3J4bkpWYkxjV0FTNmxmU0p0WVpGd2JYMDdC'
    'MHUyUFo5MEk0UE5BS0hWN0h4U0FlcE5DSEFRZmtPVTJmcHJCQTgzYTdzQ1l5'
    'Q3BVMjdlY2dFaDEzQ2RjZ2Z0ZmtJaWZKRWFwdUxwWmkzWGdBdzAwNlNidDEy'
    'Q3lEVStUVnJVK2gvTlZ4cGhOa0l1Mmg3SDVKc1FYMC9jWUZub1Zjckw5YU92'
    'aHZJbENHcG5YeW41ZHB4aXdydjlRS21BVmtiN1ZzT21CRWd6VU5XTDY3QVJi'
    'TTNTSjFUTVhkLzEzRlU4Mkg0ek5qdGRTL0RGcTgrUnEzNlpmRmFyMjZUbnkx'
    'T2xCZ2ZCNjJBaXlqWmdrZFJlRHBNc1JIaU4rcEx1OUFnWlljVmhkVzBOWjEv'
    'RnVkb1hlMFR1U3MxUjBiTmNzZlBrSTlGMWJyWWlTeGpoa2pqTENwcVRDemds'
    'Skp2ZSsvN2JiLzhiZWl4U1VDS2hWT3phTVl0Y3RXa25RMEFSdVhaSGxvUzZt'
    'MkExNG8xblkra2VsVkNISEQzNHFOMEp0bHpOTzZNd3htYlZNbUZoM1NKTFQz'
    'emVzdmI5S1dOaHJucVZzckIrbWFjbnYrNWd0NWtJSlpUeHduOUdqMFZFdlFX'
    'c2tCVzRRMDRBb051Qk1tZlRwenBLcVBlOTdZQjVOKzhGZ0xKSGs5aW9WRHd1'
    'cWhVeTlPRGpkdFcrZnJLM3Z2N0FxRmdsTEtwYVp1bjk0dlh1enUwcWY0bWpN'
    'NXdRbzNhZFVyOFRjajlrN3krRWxLbmFCV2tDNmFudlcvYkxLR1FqRVB0RzMr'
    'aWtXMkdwb2ZUMGo5dmh1Wk5jVERnZEE4T2J6SnRMdmhXK0pxU2UrWERsMkYr'
    'Zzd0NWlIOEMxWmhycGczMnNCRmR4dXNsdG5WbmV5MnVBTXoyOVp2SWQ3UTRR'
    'b25DL0tCcHZpbllLTElkMWxyclVmbzg3Njg3MGlObE5WQWVtQ3Q5RWg4aVh2'
    'V3RsQXZaVmJvZm1wS3BTRms2cU1rOXZaNFQ1NTN1SHQ1elhQeGQzOXVTUlNO'
    'TVdvcUZ6OWVRUHRMMWJIT1hYeGVWbDJFOG9vd051SXBNbExzUW16ZFpMZjkw'
    'U215OFMzSTlJcm5Oa3l1TE9FWGw2OHV1V0dEd1JuamNUQTVXeUVBT1pweWUv'
    'Ym9uQmRrQlBjaVNRQ1F2ckYxbDY0dk9XdFQrZGhQM1A0YUluRTRNc2NTRVdh'
    'YlllL0VMaTV5M1JBZDkvbE5QOVJjSmk1Uit5OU1UbmJidGlIT1E2WWh4YzBR'
    'M2pvTGY5OHNrdGEzMTFHZ1o1dFYrbExLeGI1dW5Kcjl1Mm0wMXovUytlRjdl'
    'Y1RWa1BQbTVaOC9PSldlL3p5ZUphbjA5NnovZHVXZU1MRXROVGF0YXFVaGJX'
    'TFBQMDVOY2RHRm1taHFJbjNySStkRU5OS0Fld3JCSGxYMTlqVTZuaGw1RVR1'
    'SWpHclNmcy9LVUM4TWJLTzU5a0RJSzAzT09xZFRZZGZ4UGxBMzFiUUxTeEVk'
    'S2d0eTJxWGtySk1TK3JLenFvVUwxN0xCOUxYQy9KN0F2dmluaUhzbmNVQldT'
    'QXB4SFBGZ2lGR3lhTnRHRDNOa041bmxUR3hUbmhhY3NIR0Eyd3ExN0F6N1Z6'
    'QzBIQWIxZEd1Sk1zdWRrTWI0SDEwM054ZjJJZTdReFhJbDdua2MxaEorNDRk'
    'UFdGZmo4UWtydmpoVWlHNDZXUW5FNnVSREhuRlI2RUVaRW52aUt5SzVKeHYw'
    'OG0zUGNDekN2T3UyVVdtNnlwRkV5anVIUUxuRnNXREhjU0dHUWtyR3FsdnVl'
    'MzhnQ01TdS9wSzVxTWI3VkpaY3J3a0RSakFlWkg4NU1XUWdYMk5tV3dWZWkz'
    'YVJTNUVodTk4MG9HQ3V4dGNzZ1g2RjF3UzZDamI1Wk1Wdy9FbDNLdXAzanFu'
    'cndOVExYOGZLY3dKWjQvQUVoM2IvK0xPd1Y3d0JNU01od0hlYWhONkN6NHB3'
    'V0hsQXRQNU9oRHY5aEhjRGxvSmhFczJETHppLzNHUGRuOXNEQitudUFMK0g2'
    'VnBpaCtONGZIUFh2SkxUbnFPdEw2U1VNaXVFTW5GNGdaRmFEWCt5OE1OTm4w'
    'NVBYK2l3Vm9Mb3RQMzdocDlTcWtubWhoTFFlRmdVNFFWV0d6TEE1NkVpZ3Y5'
    'WEN4c1NpNXMzSEhSTkE2T0MxNzV4eU5HaHE0ZmVjc3FDRmZ6WVlPRW90c0g1'
    'b1pLeEQrd0F5Wll2VHhNYVZjMEg5Sk9MNVR0cFJndnlUSmtOd3AzR2VSZ0h6'
    'SDB2dXVJZXBCT1E1SGRFenZma2dDVXFNL2dtbWhpT2NISG9ZU25Uc2NnMDJs'
    'bUMyMXpIOEg1ODJrcXZxam56TmJvS3dtZU9peTZjbWZOTlQvenpSVXpZT204'
    'dmZNU0V1Wi9XTVFTQXVSL1NBeXFZVFJ4NmNZL0ZGcHF5WTlUZlh2YXBiOG9E'
    'cnJsV2gvY09iOElUVFhLMlpOVlVQMVZqbDhoaHBuSVIvUktVOWRhdmF0WjlR'
    'RW4zMEVrK21mbkQ1L1hGT3FDTUNmd0pJcC96SG02bHRDM2NPTS9SSkgwUjFK'
    'M0FTZm1kUHB2bnlFOGZreHpQZ1YyTjJGS0wzN1dYWTBaZUdkZHZNcjhwN2U5'
    'YXdOTUJOOGNhY3duNGRCRUE3dUZ1YWY0MFJzZDd0TEJqZW41WStUeVlzWTNq'
    'R2pYOHZHRllmMWJqc2IvNmpuaE91blkzRk84STluTXY0QkpzNjdOaHFCb3Fa'
    'WS9xVjZGbHp6TVl5b1NnUS9pQTZldytSUHh1R2RzSjBwS090Wjc0TWFoTFdv'
    'ZmxBbS9OUHl4WitXTCs1dUdLYUxBaCt0K005aitFR0gzcDB2V2R6UnVQdGxt'
    'SkRoRkNkTHFnYjU1akwwVFRpeFFNY0tJaFZ0NGpIUDc2dlM5TkF0TWdOVGlG'
    'aTJTeDdsdk90Rm5EdUlScEVwdVQ5cUZJb3JGTjFKUXYrazdONjFzZ3RVTGVx'
    'VEVGWFgvUDNSU0w1YVpEK1lBTXhoOVBISndCL08vVm4yVmQ0Wkc3b3FOc3Nm'
    'RlR0V0l2MVJzR1dLMmNmSG5uOVNqZitvVkdQTlZUbmw4Nk1mbldWc1AvaXcv'
    'RmhWWmhVeTUwN1o4WmVmbzhOcEhKTWxWM1hxMVhDRjNBMjA4V3ZFVmJtRk12'
    'NURIRGNJNHZRS1VvalRDTmRJbytlSGgzc0g2clJCV2xuaFNsdnpWZkcyWGxV'
    'ejBKU09jbmw2K1M1YUFzR015MkdNSE5LZEtKeWNVSndFallEMnA3QkM3dzBK'
    'ZnhvUitQbjRZamRvM0F2bzZKN3R3Y21uSFRtOGJLdDZvRlVlN2xwRVZIVkNT'
    'cHdDZ3FYRWwzQnB1MjRBL003RlE0SUVmZWx4cnEzaVRubDVLeGhsWkY5RFM1'
    'dWFUMjdZdlZVZWpnbnJhc1QxN2JENkZtaDViMVgrVXRnVVI4aVFIbU1acmZW'
    'a1pxUmZGYnY1R2lGRFkzS21vZlJla1RNRFpDazJWUEhpN2R4eFB2MVNMUDlu'
    'TUZYMEx5T2hFQkJLZDFndDZ4UXU2Ylo2cHlFTFQ4SW81QmRmMGNGZ01SL1VI'
    'dktESVorTTA1YnZ5T2M3YVgwQnRqcmxWMGo4RWFpUUMvQ2tDNHI3TDRzdGts'
    'ZGpxZ0w2THZ2QWw0ZXBOTXFwSkZXSEJTVU1KZmRLL0pqS1EvT01WUTZqcjVQ'
    'U3dQdkZmdTNRcXg2T3hjd3laRmNtdWNRWUJHWEZHTEc1OGZtTC9kTEF6QzZa'
    'L2pvQlhlTVFaaHdGNGV2RUZSTlFyelQxWmZsTkNicm8vR2xGZUxFbHBmM0F2'
    'Q1JONHZ4UzNmU3pWaGxVekRqZE9DVFVoY3VRaFZJazY2bDhwYWswSUx3LzJ0'
    'MkRXMUVyenZYbGprWWlEV2dNMStkY2RRYXhSQTlSeXZEbGhCTldlQ1B2RWVj'
    'amNVZHJNaGFJYmpiNVNLUmxsMGtxTnhSTFgzM0JSMmxFWUpYYTFNRGtyZVJL'
    'THdJU1NuMURNTTlBVkd1a3BJK21NaVdpOUNVWGhaSjltWm9ybmsvTHdRaDVD'
    'VURJQzZXekJMUG83a0VKYVZiQW1rM3llb2xzYzFFL0tRcE95dlBjV1h4bnBr'
    'Z2ZvWm03d0NneWc2WE9lT3FRejFFWXZ3Y01WWEh4ZU1OcmhmSyt4OTdub3FC'
    'MEl4YWtHbGdxMld4dFNyR1U2WE5aR25aUnVpMTN0dms5dWZqcWxDUTg3T09v'
    'M2lySWo5S0lEbUU3b0tLT2ZGQWFMMXluVEtmR0tXYjVPbFVLQ2dTZjBET1N1'
    'SFF3V081RWNJNExNbndDbkx5SHFMZUhZdmJSM1I5UkxPTHhGVlhxWE9iMFhQ'
    'V1lCbVMzbngwbmwvaXRuY01uRHQ1TkdVZFEwaDBMZy9JS05LVkJKOGsycHNF'
    'MEluQzhteVMrK096Smc4aG9oaVkwdWhpRVVhUUc1N01JRDUrTzZidVFvYm04'
    'ZE52U0xOWVBZbys5djVqZy9uc3ZJS2ROTlVqZFFZU0hMb0V5cmdabWRmOEpV'
    'di9Wd20vWU1JOElMRk5zV2RMM2plcmVNYStmQ2l2QjIvZ2RQbTlHNFFscnlp'
    'bmtIV3UydlpiWFVvL2VPSXk5ZDJBNjVBSDNMSG1OWG1ENXZyemgvb0RUQkE4'
    'SktOTzduSXdibHU0VHkxNWRUVlZ0R1ArZTZJMFhJZU1lRGdLWlVYYUIzZTNU'
    'bUhGNXJMOU9QYmV5OC82VzdSekpheDlVQnViRTA3RTRyNTBtaExrbkhjNGdU'
    'ZENoSUhUQ3NYOWtTWkNXWTRteVIwYVkwR09kMklrcGJ4eWxSOFdQYmN1eE5P'
    'eDhRVjNCc1hYc2pmR2tRZndlTk0vN2VrcVNpd05SRTAyMm82aEJiTnRSOFFL'
    'ZVE0K0p1MUg5by9YMUI4NGorRmhyYmNESEkvSHhxYlBXK3V6aHNWbEE1WC9V'
    'Y2g2MTRPUFJveGFVV1lQczR1TWhsTms0N2c2bUtxUlRHSWM4eEp3SUtkWWc5'
    'a3hRZjVaZW85dmhUbnB2YlNkMnhGV3NIZXlBeDA0SEJHVWRPdmRKOTR1VGQ2'
    'VFBQY3hZT0l3Ync0aWU0T2h3RkRKbmh2czhQRTB2eUdVZGZqOTJaTnBoSkp2'
    'WXdkNGdqRGhKZ0RRbEFuaGgzSSttQVVRK3MyMVJkUmFmdGtPOVNGeTdNN2Vk'
    'Q1oxTUk2TXRUa0xpZ0NRQ2hnaWUxY0NDL0s5RVA5cjZ2VzZIekVKdFI5TUUy'
    'S3RoT3prZFpKNVNybGpickpaWkF6cXljcmFrLy9hVDJWa1lCL1RNbzBrNERP'
    'TjVNNGlaSzlpaCtja3NJRERzWHUvdjd0RHhoTVlrNWdZNVBUWTkyY044Wk0v'
    'Zk9ubSs5d1kwZVlyN293YjNlOXhURjdvZWNTOE1qdTBTaitjemk3Y2t5TExu'
    'UnN3Q3dKZVhsbVdYUnBSWlFESVVpbjNJNytEYUlSM2JEdlhKVVh5ODViMmpZ'
    'ZHl3M2lSdllzdDJtRWhVbmR6Rm5vaTc0STFJT0J4eDM0THcrSmJEVmxjYjJC'
    'UHhTcGp0WUlVaW5SdTlsZTlUaFJSWlRzQjBEZXBMT0JHOGVJSTVCdE1TNlFk'
    'Z09Ta1N0N013SmczYklTRGpuc0pFQ1FJUDdvQm9TT2xnbGJOWDU1YW1VRlgy'
    'YnRxQ2tqREpoSkdkZGdqeGU3TUY2R2h5TmV3WkY3eFdRZXp5aTdlZnFOejlo'
    'RWJSYzVFNG41eS9uZHR6MjZtNjFpenJsaEZtbW5wU3l3bU16aUYrVHdrVm1E'
    'T2Z4andKUVFaNFJQMnliWWN2T1VYRStZN2l0b045MHFqdlY4R01qZGp1Sm9S'
    'UGt4ajkyY0VYcnp3WlJ6OGNYRFN3dmVMN2hUUnFOS3VDQzY1bU9TUDJEWXdw'
    'djRvMlhlTHBRRGorQ25lSU1ZOUtFNzFoNmZlV3M4SU5sQXBLWmIyMHlqdW1M'
    'RnYxdFlwMDRsc2kxS1RsNUtkem1RY2NmNE9JbnZtV1ZLR3NyUHFpTytybTlV'
    'T29sYXVxTDFZTWR2YlZIYUJjQXRaQ3RpcGEyUmIwU1NXSzNJc3cwNFYzUm1F'
    'VWVIQWJ6bWx1QUJTMTFqS1dCWFVwN1daRFk4b3BYNnlrZkRsa0sxWFZPaGwv'
    'MkhQTUx1SStTbkVCdFczeVJEcUtZVUxqeVlWQ2gvdjRESWNjaWFtd1lUVkZK'
    'SjZtTkxTZDJaandFUTA2MXQ0WEI0ZVdBL2gyeU54MlptemE3eE1HYWdQam1F'
    'OUJieGdUQnBzMk9sUm1ZM01GbUh2dkdJeVNiamhvck1RMkh5WDBETUdRRlE2'
    'anhsc0pBSDB5dzNQa29rOW1kUDQySFp0czNzZUFsbEplYUVRODRWRnFXTThB'
    'WFFnRHU3dUhSRkxIY29pbmNMaThKUGE4U0lMY1hIODF4MVQ1TGl3N0w0b2JW'
    'aWg0cEtEeERyRExKbUdjNnJ2Y2J4RGZjaTJIaTg5WWZHTHhTY1VuczlQSk5J'
    'R0VGZCtQdHc2RStCSHljWWNHWkE5dTlXbDRubmZrZVY2Y0twdnR0VS9YSDY3'
    'ZEoxNS9oQlBJdDgwYkxkdDl1R0hiSGN0eVFyOUJIRzc3dmJwMmtyejJ3cnRo'
    'ZzIxWndrRmhkU3pnQVdJN09rMVpNRmJIMHI4Y21DRG02Sk5aTW45cjVBdTV5'
    'QVJmRHM3U1F5YUFzb25sVUh2ZXpaZ3d6ak9oTm1uQ3llbTZOeVQwSFlOTlFx'
    'ZnRaamdSekxRVjB6N1k2cjUxL3dubXhJdnBXY04yWmlLdFk4WFVaWEN6ampW'
    'WFBPZlI5MW1IeTRwaTBlcUczUzJ4bzJBc2xIUHNBSThOY0FnUnl1QllIVW81'
    'TnZia3p6bkNYRHhPazBneU1abS90ZWRTM3c0bkhUeFBxNVZqd1prcEFuYW9v'
    'MzVCMzNXWUF6VHJKRTdJSnAxUWw4b05YbXgzZVFNNzFHRk80b1IyYnA1UU1p'
    'aGp3RnNNbitVNkoremplSVMvQ1NmQzJ2emgrNlhzaTd0VjV5QmNxUGZPT3Na'
    'WmFmMXdmV1BNTVJXTGpkclNROXduVzlZV25rejBGUmRXeDdLNnlqclJNczBU'
    'YmpFdDk0ZUV1K2FaRHVzK254dVRDTngxeDhuQjlPUjFFb0ZnY1dJSDY5cW8w'
    'TU5ncGJtcWhsU2tVMitDK1Vpc1hMeHRzdWxKRS9xaitjbXNiQWJOM3pwOGRa'
    'VjZqT0NrUDlyRENSNHpEeFpJWXFsUldRNjNuWGgxdFVHOUVXWWovKzMzMy83'
    'bUg5SGp2Y2ZRMnlDTzhOWmJ2U3NiK0ZWNGNGeDVheDJzZzRObHZ6Vk5JditU'
    'R1JVNHp0OTIxSSsweVdvNTMyaHFmcEd4aGlTbCtWY3V3WU1vVGdkVnVhaHRT'
    'RVNTRzNReDZDMHlnZWdSQWtPSXdCQ3FuMUZKZmdpUWJBaHdtR1ExODRDMjIr'
    'Q09VcXVGaUZyQW51a0MrYks4S2NEbm1nNjRQbzdvU2VPSUhEc3o4S04waEVY'
    'VG5FUTRqSzI1YlJxVC9ZUmdUdFNjMWJDd1pYZXhaTnJYK3kvVVcybExBSWxq'
    'TUJKMXpUNHZLSk9TZTRUQzFzQ1FVL2dYRzNZaG14eXJPcHVoK3hkQ0pxWjlk'
    'WXFqRUs1OHkxNDV2R2hFRUNlZVJwR3pYcUQ3Q2FmQ2FMSEE3NnhQYTBNWVFz'
    'czBjY2MxRmRlcUwybGtRNkdnU0t2WnNvUkVFaTB1TW1neHJxRWhRendwYWNH'
    'TlE5aFI2eGc0ajl2bCtZRnJHWXA5ek9tSk5Qc0ZFU1k0WVFRRXBMd1lMNnZG'
    'TVZ3eTB0bENGOGhGS2VVNVZlUkl6N2FiUEdneW9ObzVwQWFsUTNXYjJESjJR'
    'bklkTzhFSks0YXpFenZVTU9Lcm9ZZzF3SUlMQ1R1czJqTHJSb1NqcUhab0JP'
    'RXBXQXh5MG5rRkVsWlZZam1SQWpqQlFSREdROTlhbTV4bnFTZTQvMzRvVmhk'
    'MmFFUVQzL3JKUVB4bk9UQlNmN0VQVTJBamNtYUFaQ2QwenNLQWp6cHJHdzhk'
    'NlNVUVAvdFE4Z2xPM25lc244aGI2Q3laOWtKa3lVRDJhWktRUG45QlRrblVr'
    'YkM5SFNQTmV6NjNuU1EzVkNOaktCUWxNTEZuTVQ0Tmg1alRCSmhiSm50blNj'
    'akpJZkFqYUxnakVqY2F0dC9ERVVsNHcvcnU3LzhaMnFHVFVISlRXcWp6Sm40'
    'VFcvZUpiWHVLQi8xZUxROENIc0I0WlZsZmNVdmtESVMxV3FodldOLzkvai9B'
    'ZlY3YkNVRVhkSXJZTkNGYmxtM0xDYko3NWRBMnJwaTBEUDR5ck9YK05HSFFq'
    'VEFzTFdlQmZYS1ZHU2hyRVJwQnlSanNKeVFnTVhoV1dNZFNibHpyS3R1d3lp'
    'aGMxQUlkWVhleEt1V2tkcVhzNExlYXdyR2NwQkR0OTZjSkNSeTBGeEhNQ09M'
    'SkJjSkRITVlyYitMdi92QTdaWFU2VjFtbEJ2dUlyWHg2aTVna1U0QlV5eUU2'
    'NmNYS2dpbFUzQmtLR2w0T3lsWHpxWFMzYVYrNzlCc0JjS1ZZcFhKYWVYeTNU'
    'QjlZd1U5Ly96N29wNTBGT1Z6WGFmbStYNTlocTBHOFNTTFdDSi9JVGhMdTBE'
    'd08va294eGRFMC9NUHYwRFpIMEIwY1FZUmREUml4RVoxR0FUb2hTUHJBU2JC'
    'aTJjN2l0clR0emlrTkE5U3lTK1NpQ2M5SXBYbGRMaE0wVXVSQUhVMDExQ1VJ'
    'cVJjM3ZNbVVqV0QycnFhbXpsWW1Zd29nV3hzaEs3N1A3V3FxcDltbHIveXVh'
    'WC80NGdESkdYVTUycGViWDk4QjV1VTJRZzRXc1NvS3h6LzhUdDVuaDZZTXJz'
    'MVJLRUVBN3M4SlJkdU1nZEhIS2RvWlFmZGpUdFpmSXh3SHFicUpzTWppSUFv'
    'Mi9CbGNkYWRIMkJtTjczRjRpc0h6RE5MK3UzLy9XK0M4UGlGQkpvSVJOS1dF'
    'cDcvU0xvL0d2UE43Q2JYTXlHL1pVaTl6dUYvaEM2OTNZSnRPOHRnL1NtRytF'
    'THp4TW93dHA1aUd6NDAwZmRWeVBtZWFpcyt0WXdmN3M0aWVkWTdhTFZobGJE'
    'bHRwMzNzakVrUVRzZWRvNDJXMHhacEc4Zk9LQnlPSUp1ekJvbk9XdXZZWVhC'
    'dE11a2N0WjBObVVmR29lL0UybWZGajhpeFBlL0c2ZEpGZ3p0eDVnS2p0ZVRq'
    'ZHBjcVhSWWZrZU9qK05peEpIQndtWkV0c0JYNU51ZEplRExsQkh4NE9LQnhk'
    'QUdydDhtVVdIYUhxc21qS3BOdExpb1ZJcmxYVHVEUU9lZ01ydXVWMSsvaEtD'
    'b0VNazk1N0taenZSRTZmckduOFdvMUlEK3pDNHl6VVB1Vm50NkNBVFBMMGFT'
    'ejBwcmIxVXFBSXplZ3NjN01VaXF0ZTNneElWWkhySU9FMGl2UUZHYm1mSzYw'
    'TXhDQVNpZlErbHFxU0hDdFNNU3BJb0VsaG5RT2JITkhPZ1JmWUVuSFVndkFv'
    'QVVVRFJiSFVBdjI4bmNFU0w3SWJncklhd2h2NHUrLy9jMS8xRHFKdWpUOGdr'
    'NlQzQUVENWdGbjFtcWtZdUVGZEltMDBrbzl3bUR0a2hIRzdWbmxmTUk0bmV3'
    'bGRJS0hXSzRjZHJYQlY3WjNsWGRmOHZWS3U2dmRhL3p5TW5icVIzUitaZXhx'
    'THU1cUMwN0pnVlFlV04vOXpSL1FDNHJCdXZFOHI4anVTcEd0NHZmWE5leU9m'
    'eVR1SnBxN2VjcmRzV2JyOVZiYjkzME9hK0NLeDZUa09TQ01LWWNFYlBWZDBU'
    'd1UwV0VZUzgzV3MyeW54dFVuY2dISGt3VWN6eVhIeDJXT3h6bU8xeXdnTHU4'
    'SWkwcnduYkQ0YTFuc0NnYjNCbUdNbytoQ0dIcXpwUVNDWmg1bVNuN2hySGdh'
    'amIrRVY4eFFzQmNzb1Fnd1d4NmJSQ0Z2V0xDNVFjOTF4T05KT0c0STlJU205'
    'NWpTaU9EWXZydzhPalpkcTF4WGVhMGFKWEREVWNUazlURVprT2F2R2x1K04y'
    'czdheHNQNXAvWWphMU9ZNnR6aE4xdnR0Mi9hcm1mSGVlZTNPTlp5M25Zbmh2'
    'djdTMzdqV2ZmVnluSHN6WG40WVA1SjAyUEV3YTJ0Vm4xN3Q3cGVyNWlxR3R0'
    'NDZqbGJoeGZyaDIxM1BYak44SGxVYXQ5dlBVbWVCTUl5TE1IOHlzeTFWZTJz'
    'L3RrL3dlb3NMSFZlZE1FdWtEN0w0L2E3dHF4L1BuZ3FPV3VIZHYyVmkxS0Qw'
    'MTAzaHlsMUI1c3U4OEF4S3p0ck04Nzl1elRlVEh4c2pwajIvbDAzcWw5OTNC'
    'ZVNxL051d0hOTHIyQ04ydjFoZFpyQ3oyb0wvU2d0dEFDOU5acUMyM01MMHNs'
    'NnZJK25GL1d2dnQwYnI4NXJ1KzVhbWI2VTk5OUpIMTMyZW1rQTdNTm8vYlI4'
    'V1ZiREZvMVRPRlQvcTRab0VLd1A2ZU1nKzJhOTNDUHhjd0RmYjQ1b296MzNo'
    'eDVQOXQ2YzN4NTlLdk84WDJvdHRQWTJnUUx1ZmNtdUMvQXA5NEN2aldESWgz'
    'dWdRZDF3ang0RXBzcHN5UjQycnFmZSt6QVlzQmNmaHFNK0NVb1ZvQWp1Ry96'
    'aXlZRjlQVzhVcWw0U1pTd1JJUE8vVmhoMjFpaGw1Y3JEZHA3dUxIeFlPUHlr'
    'bTYyYlh0MXRiSFM0S3VyS3hSK0tqR0c3Y3RMSmRIbFR6V3ZZTnRVSmJVZXVD'
    'OFcxWjY4T21qWU0vQlJrM1RuZ3pteFdZbk9wbHlQSkYweTVJYXpUQkhXY0Zi'
    'c3hxSWlPSUdZdXZBSTJLc0lRMmxRZFZiYWMxbnV5T0w5U2NkeTFEbzFtSDZn'
    'dlIwYk8wMjlpZklkMlZzclIxYmJFMytXWTRtZDBlb1gvSzJsYVd0cDJvTTBE'
    'WDZ0UFd3OTdLeC8ybXJKajA2NzNXNVhKYmRhbGNudDlscDE3c3JrZHJ1eXls'
    'WUxrck45MzI0UU0xaU50eHlMa2Y0MENmbUZWL2wyZ01kaFZQT094c1F6L2tH'
    'akE4clRmM2x5QXJNSkQ5cmxaY1BvTldPdEhvNk9oZ3pGVkJqSjlJd0VzQWtj'
    'bllsakZtQWw1N1JFT0VvbDlsOU1waWRSMkJlbEdVbE93UjBVaGU4SmtoZWpP'
    'bWc3RU9GMVFOK1hQaWl6K2h5ZkhPN3NPZWdKZlk1b2dwN1FRdzFPbFNzenRM'
    'NHU3MGxzcnJibG1CbkhQRXl6Q1pZR3p1ZUNzWG5LMk1ST3lTTTVmTVo5b2xo'
    'MVphVTQ0RGxnazFMeHJjbjdjTit3UUY3Y0R1aTlpWlVwSU5keXExc0I3bVU1'
    'S0N0YkFHNzlmV05JWmxncFRhNGFFK0cwZnZMcW9OQnRjR2dCZ2ZVUkl5aU9j'
    'QkFraERIVWVQMWtEN0xiMGhtaXNTYTFXTCtBTFc4TDBJN1Urd3pqUm9ieTZx'
    'cDhEMFFYVHFHYVJvaE0xMmdGVFpBQmVObW15TnV5cGZjemE4MlJWYnFyMnRL'
    'T3JPd21hT3ZZRzBTWXY4U1RSdDRrc1EybjhVcE9FVjVkWGNucE11STVOUWhn'
    'VGJwZzNGaTFWMFJhaFZveUtKbWJYRHVqS3lUMTdoNXpOSzhDN1hiM1VBSk8r'
    'T0pZbDZPVDRQNUlYc1VwU0MvczBTaU1pYWNXNUxReDlUWkhjcjJaUExac09m'
    'cFh1RUlwTDRmUzJTTWRPdGZHZ0MrSFFaa0JYazRqSGs0aW9rZDRnUTNBRXR6'
    'ZHkzcC9KNGkzZ3lESkpSekVvZmtJa0pabGpZSTJrZmJkQ2xsSXFKS28rYUY2'
    'ckV5dnZZU2VYK3p1bVdRcXN1eEVaU2x5NkEwYks4QkJrMy9VZHI3YVBueTR2'
    'cGVRUVhoT0ZqZFdaaWsyVnBtYVM3WlIxSVlrclBwbXl2ZjVkcUlwN0tCQ1I4'
    'ZTNiVEJNR2svallBSzdXQmMxK016TWQwVVh3NnJia2hRZ0N1UnRtL0V5akYv'
    'aTgveEJCdEdFWFRqSmszUGlPTzBXU055ajVSZG8wc3MzWktKMTdCeGRZOUhH'
    'S0srVGN4QmU0dk1EOEUvbElhU3BlUWd2OFRrUzZRSkVuSjdKa29XTloxRk1u'
    'TEZDSWlITGZ4QitRNHpzNHRISURjOVo1aWNrd2hkR2J2bHNaQmNKSXIvYXkv'
    'Z3FYMGNwVlpSVkVWdVFXZVZ4ZDBDVGh1aS9JN0V0NkpnT0VKZExrNDNZN3NG'
    'R0pUdG5nN3pWV3dRNjZHVVloK1BwR1BWeERNcnNDVUVuNFhBSVc0VkhPQWFx'
    'd2R1VnQ0WTlzdEtxVUF0R09JeUZxTlAyVWw3RG9WTXUzbHBxbDUrMjdscXBX'
    'ZFU4QmRkbjUwM3pUZE83bnhtN1R1dzNHMkQ0WERMYWY4L2s1OGJsYVVRWXUr'
    'UUpmWWZqUzhac1VlN29WMi9ZejQvdi94eStPOGYzTy9COWZEOEZKV29HcXpD'
    'MjZ3MHl1Y0ZGZTNrUE9JNERuQWpkZm93NVF6Z2hZazhOdW84YUFoV1lWaVJP'
    'OEFzUXRUdk5KaXowZGtBRCtibFV5enRndGw1WjZnUXo4bkM5VkVTMEZZQk93'
    'OEI4NlhtZWZEK1c3MlZ4a1NRSjAyazJkZGlLcW5KR29jSnJZVU9rQ3g2WjRn'
    'LzJ3RXlibWgzcVFEUEJEaEJISTV6RXgvbWRyVVBDRzZuRkpyYVVWV1dBelpL'
    'U0xYZ21oTXhOZHJEekRndWJ3N2E3ekNkd05DK0JUWHdSYzBLZmVESGg4M0RR'
    'T0xJa29jVFNxR2krNVZpU05xWnhSMjI1OU1tV1pnTDVCQ1RRUy9kcW54eDYv'
    'WHIzQ1hTZ1B1eXVDQmNPR3NucTZzb1IyT2xpK0F0ek15RVlJcENZdUNUMjBr'
    'aDgrZUxwd1lHRHZueXBWUGREMFVTa3FRdkRGOGJ1NFlzREIrM0xtaURiS3pC'
    'M1U2eFdoQ3NCY01GbmxtT2RBWGJEWk5KWHZvWHBaSmpnZ0pnWWhyZkdrQ2M0'
    'WnVOUXJ1NG9MSGwvNHFBejVpQ29YSThBVlh2TzlWRXBhclRlV0dkTjVSVkxt'
    'TEdxWDRNYUN2S2wyb0pJRmRmTUptdkU2WXhzQ1V0TWZYTXdTOUtYcTZ0a2Ra'
    'WGJtWlYyVCt4T2lTSmtTZFF0TkFoSkZEQmpid3JZYUJENUtVRUJpUWlYTVd3'
    'SWVBeFc3dFhNMjM4dUl4Q0tlYUNPRXUrTlBISi9SbW9STjMvVkFMNjgvSG9h'
    'OWk4VEhBZDBMQnlPMis0ejdBNk83eHRyRlBtRzZNNFhreHBDY0tpcnd0dWht'
    'QjVaQUIrK1pSVVdOQkhMTnFBUk9aZUtxRmZYeHIvUXA2ZXo3YnRIYXVmcnNV'
    'OGM1Z3VmOXRHMisxZlkvYWJsZm5hL2VUeGJuOXMvS3lXdXpYMy9NcC8wWU82'
    'RDExTzRPQkovcFoxNlA3TTlIUEtjRVVnTHRic0tIL0ZqdTZjZUtEeFVqSTdE'
    'RVVGak5hbEtJZ1V3MDVzN2tjWTRpa2dDdENCZlQzRUV5K2xqTmRGYXRpUDI2'
    'aVQrU3N2dXNyTlE3N2ZEakZoU1dGc2RKcnNtQmd6eTJpRlUvbGprVW5WRHJB'
    'YkNVMWVWSXIwRUpLbS9JcllHUTIwbkNjSHZ1NkltNkM2ck0ydis2azF3MzMw'
    'VHBCTnlUWlg3b25melZXYnR4ZEpTbHA2dWx0dHVRY3ZiTGZkQks2dGJkaTV4'
    'OExFUGRlaUZSMWV0TzZwVDhGM1N3OGJTY1lIYWk3RzRndW9HQ2VhQ0JDTnli'
    'blhFV3FOYU9GTkRZN1kydDMvMmlXME9saXVvODV5Y0wreU5kQ0JvVWJxYjRq'
    'M0Nwd1RCTmdZa2hZdllGd2EwZ3NQUUFhSUQxSEkvY3hCMkIrTE50dnZNcStw'
    'T25DVDR3dXFZbEhVczI0TnRUUmRnTkloK3prYjg2dXA5MHZOYjhMWHByMjFz'
    'VkxSSjRHdUtzRDRkanpGaVpJSVRzWE5VeHA5ZzZJVHdNMEppMUhMWE5qWUtk'
    'SjdiemtwU0h2WlAreU01dGRUSk5kSWZIUWlGQmF3bVEwQ1RnbnVvalBiVG5l'
    'ZElGa1ZRTnNla2dTaTNVdWRBZlQxaFBDRjRyTFhjU3N5bVpxWVNabFhXWHJW'
    'MXB5dVR4cnpCRjJvR0phRndKKy91ZFdEdEpQTnRpTWRhRi9BMVRsdmtEcVR6'
    'VXVRQTJLVTNEU2FwZ0paSGQzTkplNExYQzRtR1ZWUk9GZ2FPbWF6c3IzU1hI'
    'V0NwSW85SWRhWml0Y2FwZEhnN1pWZXNZeHJ5K1pRS0g1ZFQ5dWM0TmE0UHA4'
    'WkQ0QlJOYnFlR3Rad3FxOHFwMEgrY2FtWEFxWmcvNHlJQTVjSjFLZ2Jkc1JJ'
    'TWVtTkhlUTlVeGU1T2JtN2lQTkpuQnFQamRLVU9ZUzhYaU1Xbm9sL1ZMTnVR'
    'aDZhSUkwVmtoeDF4Q0JZVDRZdk8yMDlteVJFL25ydWZ6RUw0Zml2UE1YWWll'
    'TERoek5ORVJwTHhQSzhZWHNiSnA4bE52c2VHRDRiRFNUdFllNlR5ZEhMRHRo'
    'ZkVINEdJRlBnSUxKQmpYNWNNQTRnY1VSUGRCQXFJUlJSZkZldktmWnRxRHhR'
    'SFlRanJWaEV6MDlxMms5WXlyNHR2QXFBdHVibkw4bjJnSGgwZ1ZRem1TQVZB'
    'ZmV2RjFibGRpamhVMmJwVTR5bVdyZzJmUXRMdHJsemFhTEVQK2xJWFB2ejRC'
    'bHVKYkFkbk1reEg4S3JjMktkM3hzbE14bGE0ejU4V2ozVXdQQ2F1akdOajNY'
    'WXYyOUs3elJidVdsdXdUZXlGakdwMjFmYkhRdVRUS2hLbGJwYWxJMWs0Y1gx'
    'ZUkwU3BaUzhJazJNVklubGE5cUtOazdtd215S1lUcXkyUklhREJsdnhmUlVy'
    'Uit2Y05IZkV6TktWTUJSUW9WNkpMUkJXNXNsSS9DYVlBTWRLeldIZ2tHaUs3'
    'UlZaU3VUckV3azkvNUdZWThDVUQxZFhJN3VtV3VWdVRlUGRqU0ZJbTNZUVlQ'
    'Tk1RaDlQUW80akZCSE9TZUtJTktrbE9VSjVBeVZFNTMrRUlQb0I3bk94UWt6'
    'am9TY2FVclhqT1Exeld0enhYTHVyMHp5WXFrSmIvQWlESkUrM3pFMGR6OTlX'
    'SGxNeUIxQnVQN0lpdEF3elZOaWRpYjcvOWwvLzdWWDdSSy9hZTR6U0NMWEw3'
    'TXZrTjR2NWtodS9oY2hmeEZhVGhpVmlhMWhkbU5weU1iZ3lENDJsdHh3RTVO'
    'U3l0NG9UWU9mb3VHNE9WSEliRzhjVVNBWVgyMXVXT2ljaUR0a0RRZ3dRU2dD'
    'aEJXSFBNT3k1WWY0OUZjSlFiRnF4N2ptSmZ5OE5iRjAreUNRQ00xcjN0SndL'
    'L2JkdlltVDhaNGFyVHVnVTFGaXJsODhpc2hsaGhpMDlpMXN5cXJBNCtQYkpq'
    'TTJSMmw4dEptTGhCUmZSUHFyQXljREdVRklIT1M2Z0pZSkF2bDFNanEzNHZo'
    'OTIrSDAvbkJ2SHNvdlNqMGZNRlhxTVpYdGhISlBrK2VITEYzNE1BUU5xQTM4'
    'RHE3blZCWGw5VGNDZlVLb2NyV2dRa1hQemtEWU9BcTJ1eWVPLzJuREFQdC9h'
    'TXM3ejVNUGNPZFNQTHkvVktYamhTZEJhbmJVQjVuL0xVcHFkMVhZM0xFZHNt'
    'RCtrTWphTFZPMDI1ZzY3NGxBd013OEZpM1lieDVjZDVvV0IvM1lhVEZ4aGVM'
    'dWZ6UEQ5TmdTaE0waGtzSmpKWHNWWXcwVSsyeHl0OStUcWl3UzYyUnl0RjdP'
    'WUVVc3QrV0JwK05MREovR3E1T0ZsWWx4YlBRbEdCVXN0Y3FVT25TcitNNW9w'
    'MkxXNjJTb01lcW0xVlhIaUV4cFZZaTZIeVBmZi90di85ZDFmLyszMzMvN21m'
    'NkNYNGdLS3FxR2pnVmNrU3lvSWhWb08zYktwV1ZOS2xLUVRiZlhDS0ZjK00v'
    'VEpUUC8wZlo5NjBEVmJsajRUQ0JKdTNwT09zODJtQkxCOEZZTEZvUUx4b3hh'
    'OGRFOWRIenpqaVlBTzM3WEFwZlZ5ZmVEZzVRTGc4RjBML0RrNXZ6NWs2WE1D'
    'MlBKWExmVHRSTnd5dlJEK1psT1dxV0tpWnBtTEt0TnV3c20vL1Vjay9SZzNZ'
    'Mkp6T2dMdHg2cmdaK1VuMFdTRDBDMVNXczRyTWZzaFcvc3ZmdzhxbVpEaHQy'
    'K3ZWRzJyV2l6ZE9tYURoZFNmVytESjlhMjJsVVg4LzVFSjhIZi9JSmZsRjdj'
    'K0ZjNWg3STd4ZVowd1dwSWFxVXVzZm1RWmxCSVRwK0VkUDJvZEwwYzNwS2VX'
    'SG5KUjViUnhJN3p4K1EzeGJpK0o5ekw5cmRRd2h4V0QyWG01eWRhdUNsWUtH'
    'cW5RUndnbld0bXh5NUJVaU9WS0VDcmVxWTZYa2tGWm9JS0JCd3lneWVCUHpI'
    'Ykk2bXBWT05aYUpldisvWElZcTB4WnF3aDJJMkpMTXQ2d3ZLSzJWSXdCZU8r'
    'b1Zrb2QzOHNXcFRSZ2FaVG5WNmgwNU4yY1YwaHNKQWhqL2toSS9NWkx6RWRl'
    'bjRSUjQ4SFBTSE05MjRmWlR5NG1uQUxSNUpTcEZtYTU3WWpRUW1ZWVFSVWlF'
    'S0lJY3R2MldCVDJTYVBsRUh0dU54NnVWeXhwYWNTMEptcm1FQ3MrMThPY05O'
    'ZVd3UnZzTjM1c3VMMjB0N0g5MElZSU5nY2NKN3l4NWxndHk5Wjd0cXpGelFG'
    'dG9CcFphL3Z4enBPbnp6NS92dnRuZi83aTVhc3Y5bjZ4ZjNENCtzdGYvc1Zm'
    'L2hVKzZRZGtNQnlGNzk1SDQ1aE92azRZbjU2ZW5WOTgwMnF2UFZqZmVQanBv'
    'ODhzRlgvV2FHOFdTVUk4QzlJM2Fsb0xRWUhGZ2ZpZlBsdzd6dG9pRzJERzBz'
    'cU5PQlZKb1owUEZaSG5lRE9XZ2JuZytwZDBxbmN2U2FEaTJMb2NZaXN5WkdY'
    'TklYZVZuWStJekY1M3VIMTF0YkhVTU5JUlV5c0RLOWUyeTNWTHZvQjhsTzlG'
    'NGJwVFNaTFpOU0lvVm5FUjJ6VGxWdG9PRnp4Vmo1T3ZOeC9POHk2bjlMaXg4'
    'Z0hKUUVIWDlRMUpweE11blFsZXdWN0l3TUZ6UUhqRkdsVlJ1SXV1c094dUlW'
    'cXdVeDNpZG40ZGo2MDhjNlRDOW5Xb0k1Ymgwa0FCc04ycFd3N3Y1NU80RkF1'
    'OUZBNk1MVG9YRE10clNEUnpLZGVUZGdrcHY0b3BCSmFJQjdiQXdWc1pOMWpk'
    'R2lJWEthcWRYbkY5RkdGNzdsUjNwSWorN1JYdmJMbzZDcmlhdVkwbzRKcGhS'
    'SHh2OElDSGRNb1VNZ2ZoU1JUR1F3aFltOWJoK3pBN1hreElWMzc1ZkV0cTZa'
    'MHNqNHdnbmdzb3UyVmw5MGxaSFN0L3VSUTQ5dXk1ZWJGRlUxMGhNK0xqcVBm'
    'L0FJaHlYdUpHRWdFQSIsITEpO3JldHVybiBuZXcgUmVzcG9uc2Uobix7aGVh'
    'ZGVyczp7IkNvbnRlbnQtVHlwZSI6InRleHQvaHRtbDsgY2hhcnNldD11dGYt'
    'OCJ9fSl9YXN5bmMgZnVuY3Rpb24gcGYoZSx0KXtjb25zdCByPXZvaWQgMDtp'
    'Zihhd2FpdCB5dyhlLHQpKXtjb25zdHt1cmxPcmlnaW46ZX09Z2xvYmFsVGhp'
    'cy5odHRwQ29uZmlnO3JldHVybiBSZXNwb25zZS5yZWRpcmVjdChgJHtlfS9w'
    'YW5lbGAsMzAyKX1jb25zdCBuPWF3YWl0IEhmKCJINHNJQUFBQUFBQUFBNTFZ'
    'L1c3Y05oSi9GVWFwNHhVcWFiVzczdGpXVjlyRXlTRkFpZ1pOaWtOeEtGcXVO'
    'SkpZVTZTTzVINTFxMmZvLy8zckh1T2U1MTdnWHVGQVV2dmxYU2ZCZ2JZc2tq'
    'T2NqOS9NY09Ua3lkMzNyejcrOVA0MXFsVkRzMFEvRWNXc1NvRmxTUTI0eUpJ'
    'R0ZFWjVqWVVFbGY3NDhZMS8wNjh4M0VDNklMQnN1VkFvNTB3QlU2bXpKSVdx'
    'MHdJV0pBZmZURHpDaUNLWStqTEhGTktSa3lXS0tBclp5L2N2MFh2TWdLTEZW'
    'VEFPeHNuUXJpZVVzSHNrZ0tZazV3elZBc3AwV09LRm5nVWs1ejJCV1hkcXBW'
    'b1pEWWNsWjBvR0ZlY1ZCZHdTR2VTOEdlWlNqbCtVdUNGMG5YNkhGUWlDNmRj'
    'ZjFzMk1VL24xRDN6T0NpZ2kzc3JmdldWVksrL04yM2Z2dkwvOThPM2ROK013'
    'Q0s1dXZGRVlCc0YxR0hwaEVJdzhmeG9Hd1RnTW4ybEZmdEgyeTVUeWlqQnZR'
    'U1NaRVVyVSt1RDFGMTZXendvaVc0clg2WXp5L040eFJrbTFwaUJyQUpVbDVq'
    'MkxCT2RxNC9zNXAxeEVNNHJ6KzlqM1cwRWFMTmI5NnRQdzl2bmt0b3g5WCtN'
    'QzRtUjVodlA3U21pYnRsdGxxZGRMTHBwem03ZDZ4TDVQOFl5Q3IyQ2x0bHVU'
    'eVVTTEdlL21NejIwQ0M0T0pCZEZFZnMrWWUxY25aNi9ySW1DdmJLeXhnVmZS'
    'dU4yaGZUdlZidENvcHJoUWVpaC9pY1lUOTF1eG91MXA2TndVd09wYWhXTnd2'
    'QWlickNvQ0l0Q3M3M1JRUHNXMDBpdXBZTEduNVA0UklFRkZvTlRwN2h4eXlW'
    'UmhMTklBTVdLTENEbUN4QWw1Y3VvSmtVQkxEYXV3SlJVTE1xQktSQkdibEJn'
    'Y2U4M3ZJQWRVRnNiendIMTVnU295ZFh0emQzTHMwQ054bm84anRWdS94U3J1'
    'emQ2SE1GMU45WGpCSzdKVkkvSEVYczZudXJ4ZWN6RzA2bUg5ZytMWEtBTEFD'
    'WU14R2JuWVR5VG5NNFZ4SXEzMFRTOGlDbVV5cndvZ1puVXhrYm1qV0lGQTM4'
    'YVh1Z1V1M0JqVXphaTIvQ2lxMGViUXpnUFBlcGFvSG90ai9idG10dnBZc0Uy'
    'Q3hDSzVKajJtRGFrS0NqRWZZQk5CRFJkUFQ2VzBydlM3UUlEeU42MHZkTjYw'
    'ck9BdWJIMWZEUnFWMGh5U2dyVVIrTUJJRnNpWCtDQ3pHVTB2bWxYOFl5dnRn'
    'YUZEeE5GajJEa3hpMHVDc0txYUJ5MnE3akNyWDNwNjB4VVVsakYrdUVYUkVC'
    'dWNNZzVuVGVzQzB5dE1pcHZQazl1anI1cFZ3YytFSndlTS80Mmw0cVVhNzh2'
    'L3BGc2NRNytETlFTZ01YRzNUNVIwTWcra2N5Wm8rZnRxcU40QnRTbTh0SUNj'
    'UjJHOFNFSUQwUGQ3WUlXUzdua292Q1hBcmN0aUdObGJOQ1lnbkdTNDZlOHlH'
    'VEJQOVM2aFhTNzk3UDNTVEt0eTgrYlF6RVdDVjhZQTY0MERDZTFZMSs4QXNX'
    'cmlvSy9GZkdKUEJGOTdkTUhubWJLVHdPYkpmbGNTQzZpbGhNamFDNTE1QU9G'
    'WEVXTU0raTkrUlRmNnRHZHRmZkV1bTF3R2RuL1J4UWJ2ay9DK0ZpbFBsK1Yz'
    'QzZvQ1ZOOWVnb29lbi82TTY0VWI0eThialpYaXJPTkNhNlRYSGdZb3owc1o0'
    'THpGTmxvTkc1WHNZbFNTWDZIYUJTTUJEVHhZZGcrRDhPdG40elRIM1dIdVkw'
    'ZnNmM29BamtCMWdCdkkrVWhQd29tRWdHVzBBWFdDVkhKODduMHRyTmEzMjJi'
    'TTZYKzlpYWMzUjZYbTV0MmhVYlRCL1ZtNGo0U2dlTjI1ZTZFNGx3bjJlWXM1'
    'YWhkdWNlQ0p1MEtYWi9JNllLbWI5QjhhUnMwWDlnR3paYUpCUllFYXlmNEVw'
    'UWlySkxScGU3WEx0SEl1OVRkMnlXNkNrUHZVcmR2bHlqMExuVmJkNG5HVjkw'
    'M0RSUUVJODdvR3NsY0FEQ0VXWUVHRFdHMlFZMm0xOC9ibGJzNXVNUHMrblY0'
    'MFgwQisvWHptN1BzMHk5anY3MGRuMldmYVBaa2FGdkVaR2piY2QyS1pFbEJG'
    'aWluV01wMHg1UWw5U2hMU0ZQMUc2WjFsaUkvNnB3UnBpcDFkTi85amxmY3lk'
    'QytCVTlraXhraVJkcnFxYjhBSVlrK1FVdFA5eWtnRzB3cGlHemJzV3N1cmR6'
    'b1VLbmpXek5MNm5IMm93U2hoUktXRE90eGxtZ1NMYzNjU1cvMHhMTHU3Nml6'
    'QndwT3M4UmNIcWprWWxmSnN2ZjlTekkwbTRlOEQwdDZscGhTZzQ1S29UVzhm'
    'emRmTnJ1WmdIL09pWUFpMjd2SVZ2S3R6RjZPODFqOG9nZUYzOG1PdnhGMlRp'
    'eklZdnZVNmgrbzlGb0lMbm81dWg1dXlXeitXVlBrZk5ZUTFSUFpqY3c0dk5m'
    'YmJqeW1aRVl0TnIwcVBYOHl0RWdjcWlaelFWcVZPY0IwYVMrY05FMHB6ekg5'
    'b0xqQUZRUVZxTGNLbW9HakcrYnZlQUdPKyt4WndmTjVBMHdGcHBVMnFyd2pV'
    'Z1c0S0N5aDZhd2QxOXNSVnFCZVU5Q3ZMOWR2aTRHekN4VEgxVnl2RjhDVVBn'
    'SVlpSUZqalhjOExOY3NSNUJtR3doYUFacm9Ea284cDJyZ3hqbG5VaUdWUGlw'
    'amg1QWJMRENkUTZ6RWVtTzVJTVZMVEJRcVFlWDF3QmthZFlaNHJtcGd1cnRV'
    'NEhpYkJsVE5pOGg1Ly8ySGo0NW5tMUVaYlp4WDl1N3hQNjViY0NKSDM0YkRs'
    'bUxDbk03VERvbFU1M29iT2M5emtETGlubFJZeldYRXZBYWt4QlZFc3V2RlEv'
    'Q2I1R3pneHFRY1BPSHVSdFdDTDlGbkRUTHg0N2lCbHZ4cSs2WCtuNy8rOWQ5'
    'Ly80bitMamlyMERhWW56Z2VneVV5RElOZmJmeVVtRkFvMEpLb0dsblYwRmNi'
    'MWtYb3E0M3Nmblc3SldFRlh3WTZDblNCRHV5SCtkQVVFcWZMc2ZZWXVNYVJu'
    'RUlBNW16SG5tMG1rZU5CME52Nnh4L2dkdDBuQXVFNCtjNUdRMDVKZnU5NDVa'
    'eVpqbmJnN2tEOEF1ZzlsZTVuYVpwQ29OTXJ0bjlTOWNMQTUwUjdHay9WUkI2'
    'NVZyMXdqbFBjaVE0V25NNk5rMkdmUnNuUVZ2U2grUS9NL3dBZ2pHaHhrUkVB'
    'QUE9PSIsITEpO3JldHVybiBuZXcgUmVzcG9uc2Uobix7aGVhZGVyczp7IkNv'
    'bnRlbnQtVHlwZSI6InRleHQvaHRtbDsgY2hhcnNldD11dGYtOCJ9fSl9YXN5'
    'bmMgZnVuY3Rpb24gRWYoKXtjb25zdCBlPWF3YWl0IEhmKCJINHNJQUFBQUFB'
    'QUFBN1ZZNjNiYnVCRitGWVNKWTNJdFVwUmsyVEp2U1d6SHUyNlRydXZMdG1s'
    'MjY0WElrWWdZQkxnQXFFdFUvZXhiOU9uNkpEMGdLVnMzZTlNOXlZSE5RMXdH'
    'TTk5OE02TTVESjZkL25oeS9lSGlMVXBWUnFOQVB4SEZiQmdDaTRJVWNCSUZH'
    'U2lNNGhRTENTcTh1VDZ6ZS9VYXd4bUVJd0xqbkF1RllzNFVNQlVhWTVLb05F'
    'eGdSR0t3eTBtRE1LSUlwcmFNTVlXd1pVU0JJb3BDZEh4eGpDNHdBNHBHKzA3'
    'YmFRZk5hajJnaE4waEFUUWtNV2NvRlRBSW13TTgwak9IeEx3K1VLNGJxVks1'
    'OUpyTkFXZEtPa1BPaHhSd1RxUVQ4NndaUzlsK05jQVpvZFB3UFZZZ0NLWjdW'
    'OU9zejZuY3UrUUZTeUR4ZUM0L044YkRWRFhPenQrOWEzeC8rZWIwZGR0MW5Q'
    'MWVvK1c2am5Qb3VnM1hjVm9OdStzNlR0dDFYMnBEYmpWK0dkYTRiMk9lVHhz'
    'Q0JnSmsrakloTXFkNEd2WXBqKytNRW9sVVV3b3lCVkJSVUw1SG51QmN6V3c3'
    'NXBRTHIwOXhmT2ZiZGk1SWhzVzBYbjN1SGgxMGpnYStiV3N5UUd3czkzRjhO'
    'eFFheUdKck1ORHJBeTZ5Ylp0SGV2aTJUWEdmZ3ExZ29oWmJuVTVIcTJuZnov'
    'dDZhQlZjTEdsT2trU3ZGVXB4dG1FTllYbWhOdFdPVTZMZ0FZTk1jY0xIWGp1'
    'ZklQMi9uMCtRR1BheDZUWlEvZWUwdTlhOHo1UHBUTE5xVndSNmNpb1ZaSFpC'
    'L0EwTkl5ek1UV2RZL3ZMdU9tVExMOTh4SlVQbXhjQVVpRktuazJCeFoyYzhn'
    'WHR5RmdDMmtYTzJRVTVuLzZoM2VyeVZuRlpiajhmNXVkL2Y1T2YwVEk4Vmlr'
    'NjdlbXhRMU9ucThUZ2R6OXRkUFg2ZmtIYTMyMEFQajRvV1IwYzhKZ3pFTE9l'
    'U0tNS1poL3VTMDBLQnIzanVkZDBkbjhKQWxTOUtZQ1kxV0s5OG8xaUJhWGZk'
    'SFoxTE81WmYxZ2Z2eU4zeGM1d2toQTI5dHB0UDVtbHJ0c3pjc250cjFtcVRW'
    'L2FyTld1dVN3U2JqVUFvRW1OYUU1eVJKS0hncDBDR3FmSTZBcko1Mmw3VlV2'
    'dlZtcWVkMlpPQk0zZEsraDRjVWVlN042QXc4ZlhEVG9pQXVQUk56R21STVgr'
    'STh4TGJVdXpXMTI4TkJjdXZPUFZhK1FSSlRrbUM2aGhmb25weHlCWTRJWVgw'
    'MmoxOVA1OHN2T091NTVjZVRzdGFkYll6d3JTQUpUUlBKODFUV0FVZis1OEtx'
    'Y2hnYXRlRnNjNHN2MlRCSmdveXVWalNMdWx0TVFBNVdWMnFiVm1WYWx0VXBY'
    'ckZ0T1VhWk0wZFhpZ2Q3UTh3cXRocXVVdkJwZjJ6a2ZTUFZaUHQyZk43TmVV'
    'UDBOYlNMRlJvWnRvbmVyN3E1aS8zNlJiUXJYWSs4Y3M2S3NsbjhGcE9TMEJX'
    'TFl5cmJEaHczWVhkakRQWVlwNi85T1B5aUx0V2FxUGx4NFdRWEhnNUo2VmRa'
    'ZlpYeFdKZEhqa2RpUUJMbUR1VkU3d0Jqd3ZaV014U1BnSXgyMUxGam5wdS8y'
    'ZzEzbnY1QkxXNmF3SGZzYmFWb1ErbTNjNG4xcjFTSENzeWd0bldrNjE4WXEw'
    'cTZ1UVRkTGloNXl0ZjluZ2FyRHEzNUhLRUJjSGF3YllFcFFnYlNtOVg5ek83'
    'eUczczZ1NW1GKzI3Ym1OWHR6ZmxtbTU3ZGxGN2YrN1ViWXM5Qkc1VEhwZTNM'
    'RG5jYzVIcloxZ01DZk5XQTJYVmp2bnJEQktDRVdkMGltUXNBQmpDTEVGbVJs'
    'alZDWHJkdzROOFlzMmM5U3c5ZEhmbVh5QitlTkRiS3Q3OU12R2pvL1pXOFgw'
    'dEhqU3J0aXhvVm4ydmJnV2lJQ0VqRkZNc3EwYXZGSXFDdEJVRkpCdldHMldQ'
    'S2tXODBxSWlURlZvNkFiM0hSOXlJMElQdlc0Z2M4d1FTY0pjVCswUkNFbjBE'
    'VnA3K0pDbk1zT1Vnb2dXcmJHVzBzYTFsbzFhL1IxYTNsbXJxVkdRdHFNcmlB'
    'VW9pWWJBUUdERlJkQk0yMUZsVHlYMVdNUWh6bUpLNHJ1d0ZvVVRBUWt3M2RW'
    'TDA0cnFBTG8zTWlHajBwWW9TRHZSSldZSno5RE56ZmxwMEV3N1R4cjVzTFZl'
    'enFON3R4VUZTVllPUmF0Ni94ODRobTdici9rSkpYbWZZNUdZdS9yMlhjdUls'
    'dnY2MWZ1M29yc1cvQk5tNkFKTE9lWWkrU3BBbGJEeityNXZoM2RKeVIrQWZW'
    'WDBaU3hJcmlzR3VyazhSemxXNlZjQkw0dStyUy83ZHNnWEdyNEVkbFhXYTEz'
    'YkpnczE2MXFzNklUblU0VHBJdStmTm5lN0laV09WWXNxdDBjVUZOSWgyMWlR'
    'MkNnRXVjQXE5UWNGSzV1eVJiYURUa0RUbWdsUWhXQW9GdE5jY1VlVVBGWmI4'
    'dzJSS3lVNEd5NkMyclJtTVdkU0lSVWFiNDVQVHQrZWZmL0QrWi8rL083OVgz'
    'NjgrT3ZsMWZYTlQzLzcrNGQvNEg2Y3dHQ1lrazkzTkdNOC8wMUlWWXpHayts'
    'bnQ5WHU3SGNQRG50SHoxNC9mN0h6ejVmZm1kYnQzc2RmWnZOLytkNXV3d21p'
    'VjRhdkFVRm9HSDZsaW9VTXh1aUdNTlY3SXdTZW1xMER5Njl0SDRLcXd2QW5I'
    'V0RTWkpZLzRNTFVOL0RROVhuUU92RDUzcDRGZTZINnlEN3lYM1o2aDcvNE5Y'
    'N1lncmJvMzF5ZWErZDlUYVMzdDFjbmwrY1gxN2UzMzkzYWU3N1hjTDR4eU1Q'
    'OXAwQ3VGTzZaRHAxd05VRHVJeWw4TEFvV0lSWnVjMXdqNFhHUkFWUGE4cmNV'
    'OU92eDlEd3hEYTNMc0J6ZExKL1VINHZLeUgxVVlLazByY25kQi91anNvdmtY'
    'bGRZV1Q0M2dPbk9QVEhDTU5RZEQ3MVNYT0FoNkh2T0ZXU21vVDhDdk9jSkdO'
    'YkxsL2RheXM4RFpRYS9JMUk1T0VtcWcrWFhBc05xYkhWeVkweFl3c2ZPV21r'
    'SUY5U1lhaEZ0RUtwWGp5RlNLMEM4WHpWWjRZdVN3UG5QN1ByeTl1TE4xVlg0'
    'WXJad3pmeG5kblZ6Zkh2eDV2b0hmYXpHL2F2UDhJZ005VysvRXk4c2NjYUNL'
    'TGlHaVRMQmNsUUt6RFN0TU1JVWhES04vLzduMytpRTV3UVNwRGk2RjNwbVdK'
    'WVRZeFducGdwMTJaS2NnZ05DY0dFYVo1alErcnl1ZnRwd3oyZ295NXI3UWJP'
    'dVhFR3o2ckNhNWFmSC93RzNiZ1kraWhRQUFBPT0iLCExKTtyZXR1cm4gbmV3'
    'IFJlc3BvbnNlKGUse2hlYWRlcnM6eyJDb250ZW50LVR5cGUiOiJ0ZXh0L2h0'
    'bWw7IGNoYXJzZXQ9dXRmLTgifX0pfWFzeW5jIGZ1bmN0aW9uIEJmKGUsdCl7'
    'aWYoIlBPU1QiIT09ZS5tZXRob2QpcmV0dXJuIEJsKCExLDQwNSwiTWV0aG9k'
    'IG5vdCBhbGxvd2VkLiIpO2NvbnN0IHI9dm9pZCAwO2lmKCFhd2FpdCB5dyhl'
    'LHQpKXJldHVybiBCbCghMSw0MDEsIlVuYXV0aG9yaXplZC4iKTt0cnl7cmV0'
    'dXJuIGF3YWl0IHdsKHQpLEJsKCEwLDIwMCwiV2FycCBjb25maWdzIHVwZGF0'
    'ZWQgc3VjY2Vzc2Z1bGx5ISIpfWNhdGNoKGUpe3JldHVybiBjb25zb2xlLmxv'
    'ZyhlKSxCbCghMSw1MDAsYEFuIGVycm9yIG9jY3VycmVkIHdoaWxlIHVwZGF0'
    'aW5nIFdhcnAgY29uZmlnczogJHtIbChlKX1gKX19YXN5bmMgZnVuY3Rpb24g'
    'SGYoZSx0KXtjb25zdCByPVVpbnQ4QXJyYXkuZnJvbShhdG9iKGUpLGU9PmUu'
    'Y2hhckNvZGVBdCgwKSksbj1uZXcgQmxvYihbcl0pLnN0cmVhbSgpLnBpcGVU'
    'aHJvdWdoKG5ldyBEZWNvbXByZXNzaW9uU3RyZWFtKCJnemlwIikpO2lmKHQp'
    'e2NvbnN0IGU9YXdhaXQgbmV3IFJlc3BvbnNlKG4pLmFycmF5QnVmZmVyKCks'
    'dD12b2lkIDA7cmV0dXJuKG5ldyBUZXh0RGVjb2RlcikuZGVjb2RlKGUpfXJl'
    'dHVybiBufWFzeW5jIGZ1bmN0aW9uIG1mKGUpe2NvbnN0IHQ9bmV3IFVSTChl'
    'LnVybCkse3N1YlBhdGg6cn09Z2xvYmFsVGhpcy5odHRwQ29uZmlnLHtkb2hV'
    'Ukw6bn09Z2xvYmFsVGhpcy5nbG9iYWxDb25maWc7aWYodC5wYXRobmFtZSE9'
    'PWAvZG5zLXF1ZXJ5LyR7cn1gKXJldHVybiBsZihlKTtjb25zdCBpPW5ldyBV'
    'Ukwobik7dC5zZWFyY2hQYXJhbXMuZm9yRWFjaCgoZSx0KT0+e2kuc2VhcmNo'
    'UGFyYW1zLnNldCh0LGUpfSk7Y29uc3Qgcz1uZXcgUmVxdWVzdChpLnRvU3Ry'
    'aW5nKCksZSk7cmV0dXJuIGZldGNoKHMpfWZ1bmN0aW9uIGdmKGUsdCl7Y29u'
    'c3Qgcj1bXTtmb3IobGV0IG49MDtuPGUubGVuZ3RoO24rPXQpci5wdXNoKGUu'
    'c2xpY2UobixuK3QpKTtyZXR1cm4gcn1hc3luYyBmdW5jdGlvbiB5ZihlKXtj'
    'b25zdCB0PWdmKGUsMTAwKSxyPVtdO2Zvcihjb25zdCBlIG9mIHQpe2NvbnN0'
    'IHQ9YXdhaXQgZmV0Y2goImh0dHA6Ly9pcC1hcGkuY29tL2JhdGNoP2ZpZWxk'
    'cz1xdWVyeSxjaXR5LGNvdW50cnksY291bnRyeUNvZGUsaXNwLHN0YXR1cyIs'
    'e21ldGhvZDoiUE9TVCIsaGVhZGVyczp7IkNvbnRlbnQtVHlwZSI6ImFwcGxp'
    'Y2F0aW9uL2pzb24ifSxib2R5OkpTT04uc3RyaW5naWZ5KGUpfSk7aWYoIXQu'
    'b2spdGhyb3cgbmV3IEVycm9yKGBpcC1hcGkgcmVxdWVzdCBmYWlsZWQ6ICR7'
    'dC5zdGF0dXN9YCk7Y29uc3Qgbj1hd2FpdCB0Lmpzb24oKTtmb3IoY29uc3Qg'
    'ZSBvZiBuKSJzdWNjZXNzIj09PWUuc3RhdHVzJiZyLnB1c2goe2lwOmUucXVl'
    'cnksY2l0eTplLmNpdHksY291bnRyeTplLmNvdW50cnksY291bnRyeUNvZGU6'
    'ZS5jb3VudHJ5Q29kZSxpc3A6ZS5pc3B9KX1yZXR1cm4gcn1hc3luYyBmdW5j'
    'dGlvbiBUZigpe2NvbnN0e2dsb2JhbENvbmZpZzp7dXNlcklEOmUsVHJQYXNz'
    'OnR9LGh0dHBDb25maWc6e2RlZmF1bHRIdHRwc1BvcnRzOnIsY2xpZW50Om4s'
    'aG9zdE5hbWU6aX0sZGljdDp7X1ZMXzpzLF9UUl86byxfcHJvamVjdF86YX0s'
    'c2V0dGluZ3M6e2ZpbmdlcnByaW50OmMscG9ydHM6dSxjdXN0b21DZG5BZGRy'
    'czpsLGN1c3RvbUNkbkhvc3Q6ZCxjdXN0b21DZG5Tbmk6dyxWTENvbmZpZ3M6'
    'aCxUUkNvbmZpZ3M6ZixvdXRQcm94eTpBLHJlbW90ZUROUzpwLGN1c3RvbUNv'
    'bmZpZ3M6RSxjdXN0b21TdWJzOkIsdXBzdHJlYW1QYXJhbXM6e3Vwc3RyZWFt'
    'U2VydmVyOkgsdXBzdHJlYW1Qb3J0Om19fX09Z2xvYmFsVGhpcyxnPShpLG8s'
    'YSx1LGwsZCk9Pntjb25zdCB3PXIuaW5jbHVkZXMoYSl8fG89PT1ILGg9dz8i'
    'dGxzIjoibm9uZSIsZj1uZXcgVVJMKGAke2l9Oi8vY29uZmlnYCk7aT09PXM/'
    'KGYudXNlcm5hbWU9ZSxmLnNlYXJjaFBhcmFtcy5hcHBlbmQoImVuY3J5cHRp'
    'b24iLCJub25lIikpOmYudXNlcm5hbWU9dDtjb25zdCBBPU1sKGkpO3JldHVy'
    'biBmLmhvc3RuYW1lPW8sZi5wb3J0PWEudG9TdHJpbmcoKSxmLnNlYXJjaFBh'
    'cmFtcy5hcHBlbmQoImhvc3QiLHUpLGYuc2VhcmNoUGFyYW1zLmFwcGVuZCgi'
    'dHlwZSIsIndzIiksZi5zZWFyY2hQYXJhbXMuYXBwZW5kKCJzZWN1cml0eSIs'
    'aCksZi5oYXNoPWQsInNpbmctYm94Ij09PW4/KGYuc2VhcmNoUGFyYW1zLmFw'
    'cGVuZCgiZWgiLCJTZWMtV2ViU29ja2V0LVByb3RvY29sIiksZi5zZWFyY2hQ'
    'YXJhbXMuYXBwZW5kKCJlZCIsIjI1NjAiKSxmLnNlYXJjaFBhcmFtcy5hcHBl'
    'bmQoInBhdGgiLEEpKTpmLnNlYXJjaFBhcmFtcy5hcHBlbmQoInBhdGgiLGAk'
    'e0F9P2VkPTI1NjBgKSx3JiYoZi5zZWFyY2hQYXJhbXMuYXBwZW5kKCJzbmki'
    'LGwpLGYuc2VhcmNoUGFyYW1zLmFwcGVuZCgiZnAiLGMpLGYuc2VhcmNoUGFy'
    'YW1zLmFwcGVuZCgiYWxwbiIsImh0dHAvMS4xIikpLGYuaHJlZn07bGV0IHk9'
    'IiIsVD0iIix4PSIiLHY9MTtjb25zdCBiPWF3YWl0IHhsKCExKTtIJiZtJiYo'
    'dS51bnNoaWZ0KG0pLGIudW5zaGlmdChIKSk7Zm9yKGNvbnN0IGUgb2YgdSlm'
    'b3IoY29uc3QgdCBvZiBiKXtjb25zdCByPWwuaW5jbHVkZXModCksbj1yP3c6'
    'YmwoaSksYT1yP2Q6aTtpZihlPT09bT09KHQ9PT1IKSl7aWYoaCl7Y29uc3Qg'
    'cj12bCh2LGUsdCxzLCExLCExKSxpPXZvaWQgMDt5Kz1gJHtnKGF0b2IoImRt'
    'eGxjM009IiksdCxlLGEsbixyKX1cbmB9aWYoZil7Y29uc3Qgcj12bCh2LGUs'
    'dCxvLCExLCExKSxpPXZvaWQgMDtUKz1gJHtnKGF0b2IoImRISnZhbUZ1Iiks'
    'dCxlLGEsbixyKX1cbmB9disrfX1pZihBKXtsZXQgZT1gIyR7ZW5jb2RlVVJJ'
    'Q29tcG9uZW50KCLwn5KmIENoYWluIHByb3h5IPCflJciKX1gO2lmKEEuc3Rh'
    'cnRzV2l0aCgic29ja3MiKXx8QS5zdGFydHNXaXRoKCJodHRwIikpe2NvbnN0'
    'IHQ9L14oPzpzb2Nrc3xodHRwKTpcL1wvKFteQF0rKUAvLHI9QS5tYXRjaCh0'
    'KSxuPSEhciYmclsxXTt4PW4/QS5yZXBsYWNlKG4sYnRvYShuKSkrZTpBK2V9'
    'ZWxzZSB4PUEuc3BsaXQoIiMiKVswXStlfWNvbnN0IFI9dm9pZCAwLE09QWwo'
    'eStUK3grKEUuam9pbigiXG4iKSthd2FpdCB4ZihCKSkpO3JldHVybiBuZXcg'
    'UmVzcG9uc2UoTSx7c3RhdHVzOjIwMCxoZWFkZXJzOnsiQ29udGVudC1UeXBl'
    'IjoidGV4dC9wbGFpbjtjaGFyc2V0PXV0Zi04IiwiQ2FjaGUtQ29udHJvbCI6'
    'Im5vLXN0b3JlLCBuby1jYWNoZSwgbXVzdC1yZXZhbGlkYXRlLCBwcm94eS1y'
    'ZXZhbGlkYXRlIiwiQ0ROLUNhY2hlLUNvbnRyb2wiOiJuby1zdG9yZSIsIlBy'
    'b2ZpbGUtVGl0bGUiOmBiYXNlNjQ6JHtBbChg8J+SpiAke2F9IFJhd2ApfWAs'
    'RE5TOnB9fSl9YXN5bmMgZnVuY3Rpb24geGYoZSl7Y29uc3QgdD12b2lkIDA7'
    'cmV0dXJuKGF3YWl0IFByb21pc2UuYWxsKGUubWFwKGFzeW5jIGU9Pnt0cnl7'
    'Y29uc3QgdD1hd2FpdCBmZXRjaChlKTtpZighdC5vaylyZXR1cm4iIjtjb25z'
    'dCByPShhd2FpdCB0LnRleHQoKSkudHJpbSgpO2lmKCFyKXJldHVybiIiO2lm'
    'KHZmKHIpKXRyeXtyZXR1cm4gcGwocil9Y2F0Y2h7cmV0dXJuIHJ9cmV0dXJu'
    'IHJ9Y2F0Y2h7cmV0dXJuIiJ9fSkpKS5maWx0ZXIoQm9vbGVhbikuam9pbigi'
    'XG4iKX1mdW5jdGlvbiB2ZihlKXtyZXR1cm4hKCFlfHxlLmxlbmd0aCU0IT0w'
    'KSYmL15bQS1aYS16MC05Ky89XHJcbl0rJC8udGVzdChlKX12YXIgYmY9e2Fz'
    'eW5jIGZldGNoKGUsdCl7dHJ5e2NvbnN0IHI9ZS5oZWFkZXJzLmdldCgiVXBn'
    'cmFkZSIpO2lmKFZsKGUsdCksIndlYnNvY2tldCI9PT1yKXJldHVybiBZbCh0'
    'KSxhd2FpdCBxaChlKTt7WmwoZSx0KTtjb25zdHtwYXRoTmFtZTpyfT1nbG9i'
    'YWxUaGlzLmdsb2JhbENvbmZpZyxuPXZvaWQgMDtzd2l0Y2goci5zcGxpdCgi'
    'LyIpWzFdKXtjYXNlInBhbmVsIjpyZXR1cm4gYXdhaXQgJGgoZSx0KTtjYXNl'
    'InN1YiI6cmV0dXJuIGF3YWl0IG9mKGUsdCk7Y2FzZSJsb2dpbiI6cmV0dXJu'
    'IGF3YWl0IG5mKGUsdCk7Y2FzZSJsb2dvdXQiOnJldHVybiBzZigpO2Nhc2Ui'
    'c2VjcmV0cyI6cmV0dXJuIGF3YWl0IEVmKCk7Y2FzZSJmYXZpY29uLmljbyI6'
    'cmV0dXJuIGF3YWl0IGZmKCk7Y2FzZSJkbnMtcXVlcnkiOnJldHVybiBhd2Fp'
    'dCBtZihlKTtjYXNlInByb3h5LWlwIjpyZXR1cm4gYXdhaXQgZWYoZSx0KTtk'
    'ZWZhdWx0OnJldHVybiBhd2FpdCBsZihlKX19fWNhdGNoKGUpe3JldHVybiBh'
    'd2FpdCB0ZihlKX19fTtleHBvcnR7YmYgYXMgZGVmYXVsdH07'
)

def _get_worker_js() -> bytes:
    return _b64.b64decode(_BPB_W)




def _cf_hdr(email: str, api_key: str) -> dict:
    return {"X-Auth-Email": email, "X-Auth-Key": api_key,
             "Content-Type": "application/json",
             "User-Agent": "BPB-Optimizer/4.2.2"}


def _cf_req(url, email, api_key, method="GET", body=None, ctype="application/json"):
    import json as _j
    data = (_j.dumps(body).encode() if isinstance(body,(dict,list)) else body) if body else None
    h = _cf_hdr(email, api_key)
    if ctype != "application/json": h["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=30) as r:
            return _j.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read()
            return _j.loads(err_body)
        except Exception:
            return {"success": False, "errors": [{"message": f"HTTP {e.code}: {e.reason}"}]}
    except urllib.error.URLError as e:
        return {"success": False, "errors": [{"message": f"Network error: {e.reason}"}]}


def _cf_validate(email, api_key, acct_id):
    try:
        r = _cf_req(f"https://api.cloudflare.com/client/v4/accounts/{acct_id}",
                    email, api_key)
        if r.get("success"):
            return True, f"Account '{r.get('result',{}).get('name','?')}' verified"
        return False, "; ".join(e.get("message","?") for e in r.get("errors",[]))
    except Exception as e:
        return False, str(e)

def _bpb_fetch_real_path(worker_host: str, sub_path: str, timeout: int = 15) -> dict:
    import urllib.request as _ur2
    import urllib.parse   as _up2
    import base64         as _b64

    candidates = [
        f"https://{worker_host}/sub/raw/{sub_path}?app=xray",
        f"https://{worker_host}/{sub_path}?app=xray",
        f"https://{worker_host}/sub/raw/{sub_path}",
    ]
    raw_text = ""
    opener = _ur2.build_opener(_ur2.ProxyHandler({}))
    for url in candidates:
        try:
            req = _ur2.Request(url, headers={"User-Agent": "v2rayN/6.0",
                                             "Accept":     "*/*"})
            with opener.open(req, timeout=timeout) as r:
                data = r.read()
            try:
                decoded = _b64.b64decode(data + b"==").decode("utf-8", errors="ignore")
                if "vless://" in decoded or "vmess://" in decoded:
                    raw_text = decoded
                else:
                    raw_text = data.decode("utf-8", errors="ignore")
            except Exception:
                raw_text = data.decode("utf-8", errors="ignore")
            if "vless://" in raw_text:
                break
        except Exception:
            continue

    if not raw_text:
        return {}

    for line in raw_text.splitlines():
        line = line.strip()
        if not line.startswith("vless://"):
            continue
        try:
            qs_start = line.index("?")
            qs = line[qs_start + 1:]
            if "#" in qs:
                qs = qs[:qs.index("#")]
            params = dict(_up2.parse_qsl(qs, keep_blank_values=True))
            real_path = _up2.unquote(params.get("path", ""))
            real_sni  = params.get("sni", "").lower()
            if real_path and real_path != "/" + sub_path:
                return {"path": real_path, "sni": real_sni}
        except Exception:
            continue
    return {}


def _bpb_configure_proxy_ip(email: str, api_key: str, acct_id: str, kv_id: str,
                             proxy_ip: str, log=None) -> bool:
    """Configure the panel's Proxy IP the SAME way the panel's own
    Settings page would — by updating its "proxySettings" KV record,
    NOT by setting a Cloudflare env var/secret.

    Why this matters: the panel stores ALL its settings (proxy mode, DNS,
    ports, CDN overrides, everything) as ONE JSON blob under the KV key
    "proxySettings" — confirmed by decoding the actual worker.js. On
    first ever access, the worker seeds that key with its own full
    defaults (proxyIPs: [] among ~20 other fields). If we wrote only
    {"proxyIPs": [...]} ourselves, every other field would be missing
    and the panel would break — which is almost certainly what happened
    when PROXY_IP was set as a raw secret instead: it's the wrong
    mechanism, not just a wrong value.

    So instead: read whatever the worker has ALREADY seeded (full
    defaults, by the time this is called the panel has been hit at
    least once successfully), merge in only proxyIPMode/proxyIPs, and
    write the FULL merged object back. Never write a partial object.
    """
    log = log or (lambda *_a, **_k: None)
    import json as _j3
    import urllib.request as _ur3
    import urllib.error as _ue3

    base = (f"https://api.cloudflare.com/client/v4/accounts/{acct_id}"
            f"/storage/kv/namespaces/{kv_id}/values/proxySettings")
    headers = {"X-Auth-Email": email, "X-Auth-Key": api_key,
               "User-Agent": "VLESS-Optimizer/1.0"}
    opener = _ur3.build_opener(_ur3.ProxyHandler({}))

    try:
        req = _ur3.Request(base, headers=headers)
        with opener.open(req, timeout=20) as r:
            raw = r.read()
    except _ue3.HTTPError as e:
        if e.code == 404:
            log("  ⚠ Panel hasn't initialized its settings yet (proxySettings "
                "key not found in KV) — open the panel once, then retry.")
        else:
            log(f"  ⚠ Could not read panel settings: HTTP {e.code}")
        return False
    except Exception as e:
        log(f"  ⚠ Could not read panel settings: {e}")
        return False

    try:
        settings = _j3.loads(raw)
    except Exception as e:
        log(f"  ⚠ Panel settings weren't valid JSON — leaving untouched ({e}).")
        return False

    if not isinstance(settings, dict) or not settings:
        log("  ⚠ Panel settings looked empty/invalid — leaving untouched "
            "rather than risk overwriting required fields.")
        return False

    # Merge ONLY the proxy fields — every other field the panel already
    # has (DNS, ports, CDN, etc.) is preserved exactly as-is.
    settings["proxyIPMode"] = "proxyip"
    settings["proxyIPs"] = [proxy_ip]

    try:
        put_req = _ur3.Request(
            base, data=_j3.dumps(settings).encode("utf-8"), method="PUT",
            headers={**headers, "Content-Type": "application/json"})
        with opener.open(put_req, timeout=20) as r:
            r.read()
        # (intentionally no console message here — the panel-settings write
        #  itself is unchanged; only the unnecessary log line was removed)
        return True
    except Exception as e:
        log(f"  ⚠ Could not write panel settings: {e}")
        return False


# BPB's own public relay, used by the official worker.js as its
# hardcoded last-resort fallback (confirmed by decoding the actual
# deployed binary: defaultProxyIPs = [_public_proxy_ip_] = this value).
# Setting it explicitly here — rather than relying on that hardcoded
# fallback — fixes "Telegram/WhatsApp/Instagram work but normal HTTPS
# sites get SSL/TLS errors": Cloudflare Workers' Sockets API reliably
# reaches Cloudflare's own network and a few huge anycast services, but
# is unreliable for arbitrary ordinary websites, so the worker needs a
# relay to fall back to.
DEFAULT_PROXY_IP = "bpb.yousef.isegaro.com"


# ── Worker-pool export obfuscation ────────────────────────────────────
# The Worker Pool can carry sensitive material (Cloudflare Global API keys,
# account emails, UUIDs, panel passwords). Exporting that as plain JSON
# leaves it human-readable on disk. These helpers make the exported file
# NON human-readable via a reversible XOR + base64 transform, with a magic
# header so import can auto-detect and decode it. This is light obfuscation
# (not strong encryption) — its job is to keep credentials from sitting in
# clear text, and to round-trip cleanly back on import.
_POOL_MAGIC = "VEOPOOL1:"
_POOL_XOR_KEY = b"VEO-WorkerPool-Obfuscation-Key-v1"


def _pool_encode(data) -> str:
    """Serialize `data` (list/dict) to a non-human-readable export string."""
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    k = _POOL_XOR_KEY
    x = bytes(b ^ k[i % len(k)] for i, b in enumerate(raw))
    return _POOL_MAGIC + _b64.b64encode(x).decode("ascii")


def _pool_decode(text: str):
    """Inverse of _pool_encode. Falls back to plain JSON for legacy files."""
    text = (text or "").strip()
    if text.startswith(_POOL_MAGIC):
        x = _b64.b64decode(text[len(_POOL_MAGIC):])
        k = _POOL_XOR_KEY
        raw = bytes(b ^ k[i % len(k)] for i, b in enumerate(x))
        return json.loads(raw.decode("utf-8"))
    # Legacy / hand-made plain-JSON export — still accept it.
    return json.loads(text)


def _bpb_deploy_worker(params: dict, q):
    import json as _j, secrets as _sec, re as _re3
    def log(m): q.put(("bpb_log", m)); q.put(("bpb_status", m))
    email    = params["email"];  api_key = params["api_key"]
    acct_id  = params["acct_id"]; wname  = params["wname"]
    pw       = params["panel_pass"]
    sub_len  = max(8, min(64, params.get("sub_length", 24)))
    BASE     = "https://api.cloudflare.com/client/v4"
    ACCT     = f"{BASE}/accounts/{acct_id}"
 
    try:
        # ── Step 1: Validate credentials ─────────────────────────────────────
        log("Step 1/5: Validating credentials…")
        ok, msg = _cf_validate(email, api_key, acct_id)
        if not ok:
            q.put(("bpb_done", {"success": False, "error": f"Auth: {msg}"})); return
        log(f"  ✔ {msg}")
 
        # ── Step 2: KV namespace ──────────────────────────────────────────────
        log("Step 2/5: Creating KV namespace…")
        kv_title = _re3.sub(r'[^a-z0-9\-]', '-', wname.lower()) + "-kv"
        kv_resp  = _cf_req(f"{ACCT}/storage/kv/namespaces", email, api_key,
                           "POST", {"title": kv_title})
        if kv_resp.get("success"):
            kv_id = kv_resp["result"]["id"]
            log(f"  ✔ KV created: {kv_id}")
        else:
            lst = _cf_req(f"{ACCT}/storage/kv/namespaces", email, api_key)
            ex  = [n for n in lst.get("result", []) if n.get("title") == kv_title]
            if ex:
                kv_id = ex[0]["id"]; log(f"  ✔ Reusing KV: {kv_id}")
            else:
                q.put(("bpb_done", {"success": False,
                    "error": "KV create failed: " + "; ".join(
                        e.get("message", "?") for e in kv_resp.get("errors", []))}))
                return
 
        # ── Step 3: Generate secrets ──────────────────────────────────────────
        log("Step 3/5: Generating secrets…")
        panel_uuid = params.get("custom_uuid") or str(_uuid_mod.uuid4())
        trojan_pw  = params.get("trojan_pass") or _sec.token_hex(16)
        sub_path   = _sec.token_urlsafe(sub_len)[:sub_len]
        # Proxy IP is intentionally NOT configured by the deployer anymore.
        # The BPB worker.js already ships with its own built-in Proxy IP
        # fallback (see the official BPB-Wizard auto-install script), so
        # setting it again here — as a secret/env var OR by rewriting the
        # panel's proxySettings KV record — was redundant and the source of
        # the breakage. We leave Proxy IP entirely to worker.js's defaults;
        # the user can still change it from inside the panel's own UI.
        log(f"  ✔ UUID: {panel_uuid}")
 
        # ── Step 4: Upload worker.js ──────────────────────────────────────────
        log("Step 4/5: Uploading worker.js v4.2.2…")
        worker_js = _get_worker_js()
        log(f"  Worker: {len(worker_js):,} bytes")
 
        # FIX #3 — embed UUID, TR_PASS, SUB_PATH as plain_text bindings
        # inside the worker metadata (exactly as BPB-Wizard workers.go does).
        # This is what the panel actually reads as environment variables.
        meta = _j.dumps({
            "main_module":        "worker.js",
            "compatibility_date": "2025-03-01",
            "compatibility_flags": ["nodejs_compat"],
            "bindings": [
                {"type": "kv_namespace",  "name": "kv",       "namespace_id": kv_id},
                {"type": "plain_text",    "name": "UUID",      "text": panel_uuid},
                # FIX #2 — TR_PASS not TROJAN_PASS
                {"type": "plain_text",    "name": "TR_PASS",   "text": trojan_pw},
                {"type": "plain_text",    "name": "SUB_PATH",  "text": sub_path},
            ],
        })
 
        import urllib.request as _ur
        bnd  = "BPBBnd" + _sec.token_hex(6)
        CRLF = b"\r\n"
 
        def mp(name, ct, body_b):
            if ct == "application/javascript+module":
                cd = f'Content-Disposition: form-data; name="{name}"; filename="{name}"\r\n'
            else:
                cd = f'Content-Disposition: form-data; name="{name}"\r\n'
            return (f"--{bnd}\r\n".encode() +
                    cd.encode() +
                    f"Content-Type: {ct}\r\n\r\n".encode() + body_b + CRLF)
 
        body = (mp("metadata",  "application/json",              meta.encode()) +
                mp("worker.js", "application/javascript+module", worker_js) +
                f"--{bnd}--\r\n".encode())
 
        req = _ur.Request(
            f"{ACCT}/workers/scripts/{wname}", data=body, method="PUT",
            headers={"X-Auth-Email": email, "X-Auth-Key": api_key,
                     "Content-Type": f"multipart/form-data; boundary={bnd}",
                     "User-Agent":   "BPB-Optimizer/4.2.2"})
 
        _no_proxy = _ur.build_opener(_ur.ProxyHandler({}))
        try:
            with _no_proxy.open(req, timeout=60) as r:
                up = _j.loads(r.read())
        except _ur.HTTPError as _ue:
            try:   up = _j.loads(_ue.read())
            except Exception:
                up = {"success": False,
                      "errors": [{"message": f"HTTP {_ue.code}: {_ue.reason}"}]}
        except _ur.URLError as _ue:
            up = {"success": False,
                  "errors": [{"message": f"Network error: {_ue.reason}"}]}
 
        if not up.get("success"):
            q.put(("bpb_done", {"success": False,
                "error": "Upload: " + "; ".join(
                    e.get("message", "?") for e in up.get("errors", []))})); return
        log("  ✔ Worker uploaded")
 
        # ── Step 4b: Enable workers.dev subdomain ────────────────────────────
        # FIX #1 — must be POST, not PUT
        log("  Enabling workers.dev subdomain…")
        import json as _j2
        sub_body = _j2.dumps({"enabled": True, "previews_enabled": False}).encode()
        sub_req  = _ur.Request(
            f"{ACCT}/workers/scripts/{wname}/subdomain",
            data=sub_body, method="POST",           # ← POST
            headers={"X-Auth-Email": email, "X-Auth-Key": api_key,
                     "Content-Type": "application/json",
                     "User-Agent":   "BPB-Optimizer/4.2.2"})
        try:
            with _no_proxy.open(sub_req, timeout=30) as r:
                en_r = _j2.loads(r.read())
        except _ur.HTTPError as _ue:
            try:   en_r = _j2.loads(_ue.read())
            except Exception:
                en_r = {"success": False,
                        "errors": [{"message": f"HTTP {_ue.code}: {_ue.reason}"}]}
 
        if en_r.get("success"):
            log("  ✔ workers.dev subdomain enabled")
        else:
            en_errs = "; ".join(e.get("message", "?") for e in en_r.get("errors", []))
            log(f"  ⚠ subdomain enable: {en_errs} (panel may not be reachable yet)")
 
        # ── Step 5: Set secrets (belt-and-suspenders alongside plain bindings) ─
        log("Step 5/5: Setting secrets…")
        # FIX #2 (also here) — TR_PASS not TROJAN_PASS
        for sname, sval in [("UUID",      panel_uuid),
                             ("TR_PASS",   trojan_pw),   # ← was TROJAN_PASS
                             ("PANEL_PASS", pw),
                             ("SUB_PATH",  sub_path)]:
            try:
                sr = _cf_req(f"{ACCT}/workers/scripts/{wname}/secrets",
                             email, api_key, "PUT",
                             {"name": sname, "text": sval, "type": "secret_text"})
                log(f"  {'✔' if sr.get('success') else '⚠'} Secret {sname}")
            except Exception as se:
                log(f"  ⚠ {sname}: {se}")
 
        # ── Resolve panel URL ─────────────────────────────────────────────────
        # The final worker host is ALWAYS:
        #     <worker-name>.<account-subdomain>.workers.dev
        # e.g. account subdomain "veo-team" + worker "veo"  →
        #     veo.veo-team.workers.dev
        # The account subdomain (the MIDDLE label) belongs to the whole CF
        # account, NOT to this worker. The previous code could miss it when
        # the lookup lagged right after enabling the subdomain, then fall
        # back to a bare "<worker-name>.workers.dev" — which omits the
        # account label entirely and never resolves. We now retry the lookup
        # before ever attempting to register, and only register a brand-new
        # account subdomain when the account genuinely has none.
        import time as _t4
        log("  Resolving account workers.dev subdomain…")
        cf_sub = ""
        for _attempt in range(4):
            sub_r = _cf_req(f"{ACCT}/workers/subdomain", email, api_key)
            if sub_r.get("success"):
                cf_sub = (sub_r.get("result", {}) or {}).get("subdomain", "") or ""
                if cf_sub:
                    log(f"  ✔ Account subdomain: {cf_sub}")
                # success (whether or not a subdomain exists) is authoritative
                break
            _t4.sleep(2)  # transient — info can lag just after enabling

        if not cf_sub:
            # Account has never registered a workers.dev subdomain. Register
            # one (one-time, account-wide). This slug becomes the MIDDLE
            # label of every worker URL on this account.
            slug = _re3.sub(r'[^a-z0-9\-]', '-', wname.lower()).strip('-') or "panel"
            log(f"  No account subdomain yet — registering '{slug}'…")
            reg = _cf_req(f"{ACCT}/workers/subdomain", email, api_key,
                          "PUT", {"subdomain": slug})
            if reg.get("success"):
                cf_sub = (reg.get("result", {}) or {}).get("subdomain", "") or slug
                log(f"  ✔ Registered account subdomain: {cf_sub}")
            else:
                # PUT fails if the account ALREADY has a subdomain — meaning
                # our earlier GET was just slow. Re-check before giving up.
                _t4.sleep(2)
                sub_r2 = _cf_req(f"{ACCT}/workers/subdomain", email, api_key)
                cf_sub = ((sub_r2.get("result", {}) or {}).get("subdomain", "")
                          if sub_r2.get("success") else "")
                if cf_sub:
                    log(f"  ✔ Found account subdomain: {cf_sub}")
                else:
                    errs = "; ".join(e.get("message","?") for e in reg.get("errors", []))
                    log(f"  ⚠ Could not resolve account subdomain: {errs}")

        if cf_sub:
            worker_host = f"{wname}.{cf_sub}.workers.dev"
        else:
            # Last-resort placeholder. A bare "<worker>.workers.dev" is NOT a
            # valid host (it omits the account subdomain label), so warn loudly
            # instead of silently handing back a broken URL.
            worker_host = f"{wname}.workers.dev"
            log("  ⚠ Account subdomain unknown — this URL is INCOMPLETE. "
                "Find it in Cloudflare → Workers & Pages → your subdomain; "
                f"the real host is {wname}.<account-subdomain>.workers.dev")
        custom_host = ""
 
        if params.get("use_domain") and params.get("domain") and params.get("zone_id"):
            dom, zid = params["domain"], params["zone_id"]
            try:
                rr = _cf_req(f"{BASE}/zones/{zid}/workers/routes",
                             email, api_key, "POST",
                             {"pattern": f"{dom}/*", "script": wname})
                if rr.get("success"):
                    custom_host = dom; log(f"  ✔ Domain: {dom}")
                else:
                    log(f"  ⚠ Route: " + "; ".join(
                        e.get("message", "?") for e in rr.get("errors", [])))
            except Exception as de:
                log(f"  ⚠ Domain: {de}")
 
        ph = custom_host or worker_host
        log(""); log("══════════════════════════════")
        log(f"  ✅ Panel:    https://{ph}/panel")
        log(f"  Password:   {pw}")
        log(f"  UUID:       {panel_uuid}")
        log(f"  TR_PASS:    {trojan_pw}")
        log(f"  SUB_PATH:   {sub_path}")
        log("══════════════════════════════")
 
        q.put(("bpb_done", {
            "success":     True,
            "panel_url":   f"https://{ph}/panel",
            "worker_url":  f"https://{worker_host}",
            "worker_host": worker_host,
            "panel_host":  ph,
            "panel_name":  wname,
            "panel_pass":  pw,
            "uuid":        panel_uuid,
            "trojan_pass": trojan_pw,
            "sub_path":    sub_path,
            "proxy_ip":    "",
            "sub_url":     f"https://{ph}/sub/raw/{sub_path}?app=xray",
            "kv_id":       kv_id,
            "email":       email,
            "api_key":     api_key,
            "acct_id":     acct_id,
        }))
 
    except Exception as ex:
        import traceback as _tb
        q.put(("bpb_log",  _tb.format_exc()))
        q.put(("bpb_done", {"success": False, "error": str(ex)}))


# ══════════════════════════════════════════════════════════════════
#  Own VLESS-over-WebSocket Cloudflare Worker core
#  Minimal ES-module — proxy core only, no panel/subscription bloat.
# ══════════════════════════════════════════════════════════════════
_CFCORE_W = (
    'Ly8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09'
    'PT09PT09PT09PT09PT09Ci8vIFZMRVNTLW92ZXItV2ViU29ja2V0IENsb3VkZmxh'
    'cmUgV29ya2VyIOKAlCBOZXRDaGVjayBFZGl0aW9uCi8vIEVTIE1vZHVsZSBmb3Jt'
    'YXQgcmVxdWlyZWQgZm9yIENGIEFQSSBtdWx0aXBhcnQgdXBsb2FkCi8vIEVudiBi'
    'aW5kaW5nczogVVVJRCAocmVxdWlyZWQpLCBQUk9YWUlQIChvcHRpb25hbCBmYWxs'
    'YmFjaykKLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09'
    'PT09PT09PT09PT09PT09PT09PT09CmltcG9ydCB7IGNvbm5lY3QgfSBmcm9tICdj'
    'bG91ZGZsYXJlOnNvY2tldHMnOwpjb25zdCBXU19PUEVOPTEsV1NfQ0xPU0lORz0y'
    'OwpleHBvcnQgZGVmYXVsdCB7CiAgYXN5bmMgZmV0Y2gocmVxdWVzdCxlbnYsY3R4'
    'KXsKICAgIHRyeXsKICAgICAgY29uc3QgdWlkPShlbnYuVVVJRHx8JycpLnRyaW0o'
    'KS50b0xvd2VyQ2FzZSgpOwogICAgICBjb25zdCBwaXA9KGVudi5QUk9YWUlQfHwn'
    'JykudHJpbSgpOwogICAgICBpZighdWlkKXJldHVybiBwYWdlKCk7CiAgICAgIGNv'
    'bnN0IHVwPXJlcXVlc3QuaGVhZGVycy5nZXQoJ1VwZ3JhZGUnKXx8Jyc7CiAgICAg'
    'IGlmKHVwLnRvTG93ZXJDYXNlKCk9PT0nd2Vic29ja2V0JylyZXR1cm4gdmxlc3NX'
    'UyhyZXF1ZXN0LHVpZCxwaXApOwogICAgICByZXR1cm4gaHR0cFJvdXRlKHJlcXVl'
    'c3QsdWlkKTsKICAgIH1jYXRjaChlKXtyZXR1cm4gbmV3IFJlc3BvbnNlKCdCYWQg'
    'Z2F0ZXdheScse3N0YXR1czo1MDJ9KTt9CiAgfSwKfTsKZnVuY3Rpb24gaHR0cFJv'
    'dXRlKHJlcSx1aWQpewogIGNvbnN0IHVybD1uZXcgVVJMKHJlcS51cmwpLGhvc3Q9'
    'cmVxLmhlYWRlcnMuZ2V0KCdIb3N0Jyl8fHVybC5ob3N0bmFtZSxwPXVybC5wYXRo'
    'bmFtZTsKICBpZihwPT09YC8ke3VpZH1gfHxwPT09YC8ke3VpZH0vYClyZXR1cm4g'
    'dHh0KHZsaW5rKHVpZCxob3N0KSk7CiAgaWYocD09PWAvc3ViLyR7dWlkfWB8fHA9'
    'PT1gLyR7dWlkfS9zdWJgKXJldHVybiB0eHQoYnRvYSh2bGluayh1aWQsaG9zdCkp'
    'KTsKICByZXR1cm4gcGFnZSgpOwp9CmNvbnN0IHR4dD1zPT5uZXcgUmVzcG9uc2Uo'
    'cyx7c3RhdHVzOjIwMCxoZWFkZXJzOnsnQ29udGVudC1UeXBlJzondGV4dC9wbGFp'
    'bjtjaGFyc2V0PXV0Zi04J319KTsKZnVuY3Rpb24gdmxpbmsodWlkLGhvc3QsdGFn'
    'PSdDRi1FZGdlJyl7CiAgY29uc3QgcT1uZXcgVVJMU2VhcmNoUGFyYW1zKHtlbmNy'
    'eXB0aW9uOidub25lJyxzZWN1cml0eTondGxzJyxzbmk6aG9zdCxmcDoncmFuZG9t'
    'aXplZCcsdHlwZTond3MnLGhvc3QscGF0aDonLz9lZD0yNTYwJ30pOwogIHJldHVy'
    'biBgdmxlc3M6Ly8ke3VpZH1AJHtob3N0fTo0NDM/JHtxfSMke2VuY29kZVVSSUNv'
    'bXBvbmVudCh0YWcpfWA7Cn0KZnVuY3Rpb24gcGFnZSgpewogIHJldHVybiBuZXcg'
    'UmVzcG9uc2UoSFRNTCx7c3RhdHVzOjIwMCxoZWFkZXJzOnsnQ29udGVudC1UeXBl'
    'JzondGV4dC9odG1sO2NoYXJzZXQ9dXRmLTgnLCdDYWNoZS1Db250cm9sJzonbm8t'
    'c3RvcmUnLCdYLUNvbnRlbnQtVHlwZS1PcHRpb25zJzonbm9zbmlmZid9fSk7Cn0K'
    'YXN5bmMgZnVuY3Rpb24gdmxlc3NXUyhyZXF1ZXN0LHVpZCxwaXApewogIGNvbnN0'
    'W2NsaWVudCxzZXJ2ZXJdPU9iamVjdC52YWx1ZXMobmV3IFdlYlNvY2tldFBhaXIo'
    'KSk7CiAgc2VydmVyLmFjY2VwdCgpOwogIGNvbnN0IHJlbW90ZT17czpudWxsfTts'
    'ZXQgdWRwVz1udWxsLGlzRG5zPWZhbHNlOwogIHdzU3RyZWFtKHNlcnZlcixyZXF1'
    'ZXN0LmhlYWRlcnMuZ2V0KCdzZWMtd2Vic29ja2V0LXByb3RvY29sJyl8fCcnKQog'
    'ICAgLnBpcGVUbyhuZXcgV3JpdGFibGVTdHJlYW0oewogICAgICBhc3luYyB3cml0'
    'ZShjaHVuayl7CiAgICAgICAgaWYoaXNEbnMmJnVkcFcpe3VkcFcoY2h1bmspO3Jl'
    'dHVybjt9CiAgICAgICAgaWYocmVtb3RlLnMpe2NvbnN0IHc9cmVtb3RlLnMud3Jp'
    'dGFibGUuZ2V0V3JpdGVyKCk7YXdhaXQgdy53cml0ZShjaHVuayk7dy5yZWxlYXNl'
    'TG9jaygpO3JldHVybjt9CiAgICAgICAgY29uc3QgaD1wYXJzZVZsZXNzKGNodW5r'
    'LHVpZCk7CiAgICAgICAgaWYoaC5lcnIpdGhyb3cgbmV3IEVycm9yKGguZXJyKTsK'
    'ICAgICAgICBjb25zdCByaD1uZXcgVWludDhBcnJheShbaC52ZXIsMF0pLHBheWxv'
    'YWQ9Y2h1bmsuc2xpY2UoaC5pZHgpOwogICAgICAgIGlmKGgudWRwKXtpZihoLnBv'
    'cnQhPT01Myl0aHJvdyBuZXcgRXJyb3IoJ1VEUDogRE5TIG9ubHknKTtpc0Rucz10'
    'cnVlO2NvbnN0IGQ9ZG5zT3V0KHNlcnZlcixyaCk7dWRwVz1kLndyaXRlO3VkcFco'
    'cGF5bG9hZCk7cmV0dXJuO30KICAgICAgICBhd2FpdCB0Y3BPdXQocmVtb3RlLGgu'
    'YWRkcixoLnBvcnQscGF5bG9hZCxzZXJ2ZXIscmgscGlwKTsKICAgICAgfSwKICAg'
    'ICAgY2xvc2UoKXt0cnl7cmVtb3RlLnM/LmNsb3NlKCk7fWNhdGNoKF8pe319CiAg'
    'ICB9KSkuY2F0Y2goKCk9PndzU2FmZShzZXJ2ZXIpKTsKICByZXR1cm4gbmV3IFJl'
    'c3BvbnNlKG51bGwse3N0YXR1czoxMDEsd2ViU29ja2V0OmNsaWVudH0pOwp9CmZ1'
    'bmN0aW9uIHdzU3RyZWFtKHdzLGViNjQpewogIGxldCBkb25lPWZhbHNlOwogIHJl'
    'dHVybiBuZXcgUmVhZGFibGVTdHJlYW0oewogICAgc3RhcnQoY3RybCl7CiAgICAg'
    'IHdzLmFkZEV2ZW50TGlzdGVuZXIoJ21lc3NhZ2UnLGU9PntpZighZG9uZSljdHJs'
    'LmVucXVldWUoZS5kYXRhKTt9KTsKICAgICAgd3MuYWRkRXZlbnRMaXN0ZW5lcign'
    'Y2xvc2UnLCgpPT57d3NTYWZlKHdzKTtpZighZG9uZSljdHJsLmNsb3NlKCk7fSk7'
    'CiAgICAgIHdzLmFkZEV2ZW50TGlzdGVuZXIoJ2Vycm9yJyxlPT5jdHJsLmVycm9y'
    'KGUpKTsKICAgICAgY29uc3R7ZGF0YSxlcnJ9PWI2NGRlYyhlYjY0KTsKICAgICAg'
    'aWYoZXJyKWN0cmwuZXJyb3IoZXJyKTtlbHNlIGlmKGRhdGEpY3RybC5lbnF1ZXVl'
    'KGRhdGEpOwogICAgfSwKICAgIGNhbmNlbCgpe2RvbmU9dHJ1ZTt3c1NhZmUod3Mp'
    'O30KICB9KTsKfQpmdW5jdGlvbiBiNjRkZWMocyl7CiAgaWYoIXMpcmV0dXJue2Rh'
    'dGE6bnVsbCxlcnI6bnVsbH07CiAgdHJ5e2NvbnN0IGI9YXRvYihzLnJlcGxhY2Uo'
    'Ly0vZywnKycpLnJlcGxhY2UoL18vZywnLycpKTtyZXR1cm57ZGF0YTpVaW50OEFy'
    'cmF5LmZyb20oYixjPT5jLmNoYXJDb2RlQXQoMCkpLmJ1ZmZlcixlcnI6bnVsbH07'
    'fQogIGNhdGNoKGUpe3JldHVybntkYXRhOm51bGwsZXJyOmV9O30KfQpmdW5jdGlv'
    'biBwYXJzZVZsZXNzKGJ1Zix1aWQpewogIGlmKGJ1Zi5ieXRlTGVuZ3RoPDI0KXJl'
    'dHVybntlcnI6J3RvbyBzaG9ydCd9OwogIGNvbnN0IGI9bmV3IFVpbnQ4QXJyYXko'
    'YnVmKTsKICBpZih1dWlkMTYoYi5zbGljZSgxLDE3KSkhPT11aWQpcmV0dXJue2Vy'
    'cjondXVpZCBtaXNtYXRjaCd9OwogIGNvbnN0IG9wdD1iWzE3XSxjaT0xOCtvcHQs'
    'Y21kPWJbY2ldLHVkcD1jbWQ9PT0yOwogIGlmKGNtZCE9PTEmJmNtZCE9PTIpcmV0'
    'dXJue2VycjpgYmFkIGNtZCAke2NtZH1gfTsKICBjb25zdCBwb3J0PShiW2NpKzFd'
    'PDw4KXxiW2NpKzJdOwogIGxldCBhaT1jaSszLGFkZHI9JycsYWxlbj0wOwogIHN3'
    'aXRjaChiW2FpKytdKXsKICAgIGNhc2UgMTphbGVuPTQ7YWRkcj1BcnJheS5mcm9t'
    'KGIuc2xpY2UoYWksYWkrNCkpLmpvaW4oJy4nKTticmVhazsKICAgIGNhc2UgMjph'
    'bGVuPWJbYWkrK107YWRkcj1uZXcgVGV4dERlY29kZXIoKS5kZWNvZGUoYi5zbGlj'
    'ZShhaSxhaSthbGVuKSk7YnJlYWs7CiAgICBjYXNlIDM6e2FsZW49MTY7Y29uc3Qg'
    'ZHY9bmV3IERhdGFWaWV3KGJ1Zik7YWRkcj1BcnJheS5mcm9tKHtsZW5ndGg6OH0s'
    'KF8saSk9PmR2LmdldFVpbnQxNihhaStpKjIpLnRvU3RyaW5nKDE2KSkuam9pbign'
    'OicpO2JyZWFrO30KICAgIGRlZmF1bHQ6cmV0dXJue2VycjonYmFkIGF0eXBlJ307'
    'CiAgfQogIGlmKCFhZGRyKXJldHVybntlcnI6J25vIGFkZHInfTsKICByZXR1cm57'
    'ZXJyOm51bGwsdmVyOmJbMF0sdWRwLHBvcnQsYWRkcixpZHg6YWkrYWxlbn07Cn0K'
    'Y29uc3QgSFg9QXJyYXkuZnJvbSh7bGVuZ3RoOjI1Nn0sKF8saSk9PihpKzI1Niku'
    'dG9TdHJpbmcoMTYpLnNsaWNlKDEpKTsKZnVuY3Rpb24gdXVpZDE2KGIpe3JldHVy'
    'bihIWFtiWzBdXStIWFtiWzFdXStIWFtiWzJdXStIWFtiWzNdXSsnLScrSFhbYls0'
    'XV0rSFhbYls1XV0rJy0nK0hYW2JbNl1dK0hYW2JbN11dKyctJytIWFtiWzhdXStI'
    'WFtiWzldXSsnLScrSFhbYlsxMF1dK0hYW2JbMTFdXStIWFtiWzEyXV0rSFhbYlsx'
    'M11dK0hYW2JbMTRdXStIWFtiWzE1XV0pLnRvTG93ZXJDYXNlKCk7fQphc3luYyBm'
    'dW5jdGlvbiB0Y3BPdXQocmVtb3RlLGFkZHIscG9ydCxmaXJzdCx3cyxyaCxwaXAp'
    'ewogIGNvbnN0IGRpYWw9YXN5bmMoaCxwKT0+e2NvbnN0IHM9Y29ubmVjdCh7aG9z'
    'dG5hbWU6aCxwb3J0Ok51bWJlcihwKX0pO3JlbW90ZS5zPXM7Y29uc3Qgdz1zLndy'
    'aXRhYmxlLmdldFdyaXRlcigpO2F3YWl0IHcud3JpdGUoZmlyc3QpO3cucmVsZWFz'
    'ZUxvY2soKTtyZXR1cm4gczt9OwogIGNvbnN0IGZhbGxiYWNrPWFzeW5jKCk9Pntp'
    'ZighcGlwKXt3c1NhZmUod3MpO3JldHVybjt9Y29uc3RbcGgscHBdPXBpcC5zcGxp'
    'dCgnOicpO3BpcGUoYXdhaXQgZGlhbChwaCxwcHx8cG9ydCksd3MscmgsbnVsbCk7'
    'fTsKICAvLyBGSVg6IG9ubHkgYXdhaXQgdGhlIGRpYWwgKGNvbm5lY3QgKyBzZW5k'
    'IGZpcnN0IGNodW5rKSBzbyByZW1vdGUucyBpcwogIC8vIHNldCBhbmQgc3Vic2Vx'
    'dWVudCBjbGllbnQgd3JpdGVzIGNhbiB1c2UgdGhlIGZhc3QgcGF0aCBpbW1lZGlh'
    'dGVseS4KICAvLyBEbyBOT1QgYXdhaXQgdGhlIHJlc3BvbnNlIHBpcGUg4oCUIGl0'
    'IG11c3QgcnVuIGluIHRoZSBiYWNrZ3JvdW5kIGZvcgogIC8vIHRoZSBsaWZldGlt'
    'ZSBvZiB0aGUgY29ubmVjdGlvbiwgb3IgZXZlcnkgbXVsdGktcm91bmQtdHJpcCBw'
    'cm90b2NvbAogIC8vIChpLmUuIG5lYXJseSBhbGwgcmVhbCBIVFRQUyBzaXRlcywg'
    'd2hpY2ggbmVlZCBhIGZ1bGwgVExTIGhhbmRzaGFrZSkKICAvLyBkZWFkbG9ja3Mg'
    'YWZ0ZXIgdGhlIHZlcnkgZmlyc3QgY2xpZW50LXRvLWRlc3RpbmF0aW9uIGNodW5r'
    'LgogIGNvbnN0IHNvY2s9YXdhaXQgZGlhbChhZGRyLHBvcnQpOwogIHBpcGUoc29j'
    'ayx3cyxyaCxmYWxsYmFjayk7Cn0KYXN5bmMgZnVuY3Rpb24gcGlwZShzb2NrLHdz'
    'LHJoLG9uRW1wdHkpewogIGxldCBoZHI9cmgsZ290PWZhbHNlOwogIGF3YWl0IHNv'
    'Y2sucmVhZGFibGUucGlwZVRvKG5ldyBXcml0YWJsZVN0cmVhbSh7CiAgICBhc3lu'
    'YyB3cml0ZShjaHVuayl7Z290PXRydWU7aWYod3MucmVhZHlTdGF0ZSE9PVdTX09Q'
    'RU4pdGhyb3cgMDtpZihoZHIpe3dzLnNlbmQoYXdhaXQgbmV3IEJsb2IoW2hkcixj'
    'aHVua10pLmFycmF5QnVmZmVyKCkpO2hkcj1udWxsO31lbHNlIHdzLnNlbmQoY2h1'
    'bmspO30KICB9KSkuY2F0Y2goKCk9PndzU2FmZSh3cykpOwogIGlmKCFnb3QmJm9u'
    'RW1wdHkpYXdhaXQgb25FbXB0eSgpOwp9CmZ1bmN0aW9uIGRuc091dCh3cyxyaCl7'
    'CiAgbGV0IHNlbnQ9ZmFsc2U7CiAgY29uc3QgdHI9bmV3IFRyYW5zZm9ybVN0cmVh'
    'bSh7dHJhbnNmb3JtKGNodW5rLGN0cmwpe2NvbnN0IHY9bmV3IFVpbnQ4QXJyYXko'
    'Y2h1bmspO2xldCBvPTA7d2hpbGUobysyPD12LmJ5dGVMZW5ndGgpe2NvbnN0IGw9'
    'KHZbb108PDgpfHZbbysxXTtjdHJsLmVucXVldWUoY2h1bmsuc2xpY2UobysyLG8r'
    'MitsKSk7bys9MitsO319fSk7CiAgdHIucmVhZGFibGUucGlwZVRvKG5ldyBXcml0'
    'YWJsZVN0cmVhbSh7YXN5bmMgd3JpdGUocGt0KXsKICAgIGNvbnN0IHI9YXdhaXQg'
    'ZmV0Y2goJ2h0dHBzOi8vMS4xLjEuMS9kbnMtcXVlcnknLHttZXRob2Q6J1BPU1Qn'
    'LGhlYWRlcnM6eydjb250ZW50LXR5cGUnOidhcHBsaWNhdGlvbi9kbnMtbWVzc2Fn'
    'ZSd9LGJvZHk6cGt0fSk7CiAgICBjb25zdCBhYj1hd2FpdCByLmFycmF5QnVmZmVy'
    'KCksc3o9bmV3IFVpbnQ4QXJyYXkoWyhhYi5ieXRlTGVuZ3RoPj44KSYweGZmLGFi'
    'LmJ5dGVMZW5ndGgmMHhmZl0pOwogICAgaWYod3MucmVhZHlTdGF0ZSE9PVdTX09Q'
    'RU4pcmV0dXJuOwogICAgaWYoIXNlbnQpe3dzLnNlbmQoYXdhaXQgbmV3IEJsb2Io'
    'W3JoLHN6LGFiXSkuYXJyYXlCdWZmZXIoKSk7c2VudD10cnVlO31lbHNlIHdzLnNl'
    'bmQoYXdhaXQgbmV3IEJsb2IoW3N6LGFiXSkuYXJyYXlCdWZmZXIoKSk7CiAgfX0p'
    'KTsKICBjb25zdCB3PXRyLndyaXRhYmxlLmdldFdyaXRlcigpO3JldHVybnt3cml0'
    'ZTpjPT53LndyaXRlKGMpLmNhdGNoKCgpPT57fSl9Owp9CmZ1bmN0aW9uIHdzU2Fm'
    'ZSh3cyl7dHJ5e2lmKHdzLnJlYWR5U3RhdGU9PT1XU19PUEVOfHx3cy5yZWFkeVN0'
    'YXRlPT09V1NfQ0xPU0lORyl3cy5jbG9zZSgpO31jYXRjaChfKXt9fQpjb25zdCBI'
    'VE1MPWA8IURPQ1RZUEUgaHRtbD48aHRtbCBsYW5nPSJlbiI+PGhlYWQ+PG1ldGEg'
    'Y2hhcnNldD0iVVRGLTgiPjxtZXRhIG5hbWU9InZpZXdwb3J0IiBjb250ZW50PSJ3'
    'aWR0aD1kZXZpY2Utd2lkdGgsaW5pdGlhbC1zY2FsZT0xIj48dGl0bGU+TmV0Q2hl'
    'Y2sgJm1kYXNoOyBTcGVlZCBUZXN0PC90aXRsZT48c3R5bGU+KnttYXJnaW46MDtw'
    'YWRkaW5nOjA7Ym94LXNpemluZzpib3JkZXItYm94fWJvZHl7YmFja2dyb3VuZDoj'
    'MGIwYzEyO2NvbG9yOiNjY2M7Zm9udC1mYW1pbHk6J1NlZ29lIFVJJyxzeXN0ZW0t'
    'dWksc2Fucy1zZXJpZjttaW4taGVpZ2h0OjEwMHZoO2Rpc3BsYXk6ZmxleDtmbGV4'
    'LWRpcmVjdGlvbjpjb2x1bW47YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29u'
    'dGVudDpjZW50ZXJ9LmJyYW5ke2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50'
    'ZXI7Z2FwOjEwcHg7bWFyZ2luLWJvdHRvbTo4cHh9LmJpY297d2lkdGg6MzZweDto'
    'ZWlnaHQ6MzZweDtiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxMzVkZWcsIzRm'
    'OGVmNywjMjI1NWNjKTtib3JkZXItcmFkaXVzOjhweDtkaXNwbGF5OmZsZXg7YWxp'
    'Z24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7Zm9udC1zaXpl'
    'OjIwcHh9LmJuYW1le2ZvbnQtc2l6ZToxLjE1cmVtO2ZvbnQtd2VpZ2h0OjcwMDtj'
    'b2xvcjojZmZmfS5zdWJ7Y29sb3I6IzQ0NDtmb250LXNpemU6Ljc2cmVtO2xldHRl'
    'ci1zcGFjaW5nOi4xMmVtO3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTttYXJnaW4t'
    'Ym90dG9tOjM2cHh9LnJpbmd7cG9zaXRpb246cmVsYXRpdmU7d2lkdGg6MTk2cHg7'
    'aGVpZ2h0OjE5NnB4O21hcmdpbjowIGF1dG8gMjZweH0ucmluZyBzdmd7d2lkdGg6'
    'MTAwJTtoZWlnaHQ6MTAwJTt0cmFuc2Zvcm06cm90YXRlKC05MGRlZyl9LnJiZ3tm'
    'aWxsOm5vbmU7c3Ryb2tlOiMxNjE2MjQ7c3Ryb2tlLXdpZHRoOjEzfS5yZGx7Zmls'
    'bDpub25lO3N0cm9rZTojNGY4ZWY3O3N0cm9rZS13aWR0aDoxMztzdHJva2UtbGlu'
    'ZWNhcDpyb3VuZDtzdHJva2UtZGFzaGFycmF5OjU1NTtzdHJva2UtZGFzaG9mZnNl'
    'dDo1NTU7dHJhbnNpdGlvbjpzdHJva2UtZGFzaG9mZnNldCAyLjlzIGN1YmljLWJl'
    'emllciguNCwwLC4yLDEpfS5ydWx7ZmlsbDpub25lO3N0cm9rZTojMjJkM2IwO3N0'
    'cm9rZS13aWR0aDoxMztzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtZGFzaGFy'
    'cmF5OjU1NTtzdHJva2UtZGFzaG9mZnNldDo1NTU7dHJhbnNpdGlvbjpzdHJva2Ut'
    'ZGFzaG9mZnNldCAyLjNzIGN1YmljLWJlemllciguNCwwLC4yLDEpIC41c30ucmN7'
    'cG9zaXRpb246YWJzb2x1dGU7dG9wOjUwJTtsZWZ0OjUwJTt0cmFuc2Zvcm06dHJh'
    'bnNsYXRlKC01MCUsLTUwJSk7dGV4dC1hbGlnbjpjZW50ZXJ9LmJue2ZvbnQtc2l6'
    'ZToyLjVyZW07Zm9udC13ZWlnaHQ6ODAwO2NvbG9yOiNmZmY7bGluZS1oZWlnaHQ6'
    'MTtmb250LXZhcmlhbnQtbnVtZXJpYzp0YWJ1bGFyLW51bXM7bWluLXdpZHRoOjk2'
    'cHg7ZGlzcGxheTpibG9ja30uYnV7Zm9udC1zaXplOi43cmVtO2NvbG9yOiM0NDQ7'
    'bWFyZ2luLXRvcDo0cHg7bGV0dGVyLXNwYWNpbmc6LjFlbTt0ZXh0LXRyYW5zZm9y'
    'bTp1cHBlcmNhc2V9LnN0YXRze2Rpc3BsYXk6ZmxleDtnYXA6NDRweDttYXJnaW4t'
    'Ym90dG9tOjMycHh9LnN0YXR7dGV4dC1hbGlnbjpjZW50ZXJ9LnN2e2ZvbnQtc2l6'
    'ZToxLjI4cmVtO2ZvbnQtd2VpZ2h0OjcwMDtjb2xvcjojZmZmO2ZvbnQtdmFyaWFu'
    'dC1udW1lcmljOnRhYnVsYXItbnVtc30uc2x7Zm9udC1zaXplOi42OHJlbTtjb2xv'
    'cjojNDQ0O3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTtsZXR0ZXItc3BhY2luZzou'
    'MWVtO21hcmdpbi10b3A6M3B4fS5kbHtjb2xvcjojNGY4ZWY3fS51bHtjb2xvcjoj'
    'MjJkM2IwfS5waXtjb2xvcjojNmFhYTY0fS5idG57YmFja2dyb3VuZDpsaW5lYXIt'
    'Z3JhZGllbnQoMTM1ZGVnLCM0ZjhlZjcsIzIyNTVjYyk7Y29sb3I6I2ZmZjtib3Jk'
    'ZXI6bm9uZTtwYWRkaW5nOjEzcHggNTJweDtmb250LXNpemU6LjkzcmVtO2ZvbnQt'
    'd2VpZ2h0OjcwMDtib3JkZXItcmFkaXVzOjUwcHg7Y3Vyc29yOnBvaW50ZXI7dHJh'
    'bnNpdGlvbjouMThzO2JveC1zaGFkb3c6MCA0cHggMjJweCAjNGY4ZWY3NDQ7bGV0'
    'dGVyLXNwYWNpbmc6LjA0ZW19LmJ0bjpob3Zlcnt0cmFuc2Zvcm06dHJhbnNsYXRl'
    'WSgtMXB4KSBzY2FsZSgxLjAzKTtib3gtc2hhZG93OjAgNnB4IDMwcHggIzRmOGVm'
    'NzY2fS5idG46ZGlzYWJsZWR7YmFja2dyb3VuZDojMWExYTI4O2NvbG9yOiM0NDQ7'
    'Ym94LXNoYWRvdzpub25lO2N1cnNvcjpub3QtYWxsb3dlZDt0cmFuc2Zvcm06bm9u'
    'ZX0uc3R7Y29sb3I6IzQ0NDtmb250LXNpemU6Ljc4cmVtO21hcmdpbi10b3A6MTRw'
    'eDtoZWlnaHQ6MThweH0uc2l7Y29sb3I6IzI1MjUzNTtmb250LXNpemU6LjdyZW07'
    'bWFyZ2luLXRvcDo1cHg7aGVpZ2h0OjEzcHh9Zm9vdGVye3Bvc2l0aW9uOmZpeGVk'
    'O2JvdHRvbTowO3dpZHRoOjEwMCU7dGV4dC1hbGlnbjpjZW50ZXI7cGFkZGluZzox'
    'MnB4O2NvbG9yOiMxYTFhMjQ7Zm9udC1zaXplOi42OHJlbX08L3N0eWxlPjwvaGVh'
    'ZD48Ym9keT48ZGl2IGNsYXNzPSJicmFuZCI+PGRpdiBjbGFzcz0iYmljbyI+JiM5'
    'ODg5OzwvZGl2PjxzcGFuIGNsYXNzPSJibmFtZSI+TmV0Q2hlY2s8L3NwYW4+PC9k'
    'aXY+PHAgY2xhc3M9InN1YiI+SW50ZXJuZXQgU3BlZWQgVGVzdDwvcD48ZGl2IGNs'
    'YXNzPSJyaW5nIj48c3ZnIHZpZXdCb3g9IjAgMCAxNzYgMTc2Ij48Y2lyY2xlIGNs'
    'YXNzPSJyYmciIGN4PSI4OCIgY3k9Ijg4IiByPSI3OSIvPjxjaXJjbGUgY2xhc3M9'
    'InJkbCIgaWQ9InJEbCIgY3g9Ijg4IiBjeT0iODgiIHI9Ijc5Ii8+PGNpcmNsZSBj'
    'bGFzcz0icnVsIiBpZD0iclVsIiBjeD0iODgiIGN5PSI4OCIgcj0iNzkiLz48L3N2'
    'Zz48ZGl2IGNsYXNzPSJyYyI+PHNwYW4gY2xhc3M9ImJuIiBpZD0iYm4iPiYjODIx'
    'Mjs8L3NwYW4+PGRpdiBjbGFzcz0iYnUiIGlkPSJidSI+TWJwczwvZGl2PjwvZGl2'
    'PjwvZGl2PjxkaXYgY2xhc3M9InN0YXRzIj48ZGl2IGNsYXNzPSJzdGF0Ij48ZGl2'
    'IGNsYXNzPSJzdiBkbCIgaWQ9ImR2Ij4mIzgyMTI7PC9kaXY+PGRpdiBjbGFzcz0i'
    'c2wiPkRvd25sb2FkPC9kaXY+PC9kaXY+PGRpdiBjbGFzcz0ic3RhdCI+PGRpdiBj'
    'bGFzcz0ic3YgcGkiIGlkPSJwdiI+JiM4MjEyOzwvZGl2PjxkaXYgY2xhc3M9InNs'
    'Ij5QaW5nPC9kaXY+PC9kaXY+PGRpdiBjbGFzcz0ic3RhdCI+PGRpdiBjbGFzcz0i'
    'c3YgdWwiIGlkPSJ1diI+JiM4MjEyOzwvZGl2PjxkaXYgY2xhc3M9InNsIj5VcGxv'
    'YWQ8L2Rpdj48L2Rpdj48L2Rpdj48YnV0dG9uIGNsYXNzPSJidG4iIGlkPSJidG4i'
    'IG9uY2xpY2s9ImdvKCkiPiYjOTY1NDsmI3hGRTBFOyBTdGFydCBUZXN0PC9idXR0'
    'b24+PHAgY2xhc3M9InN0IiBpZD0ic3QiPjwvcD48cCBjbGFzcz0ic2kiIGlkPSJz'
    'aSI+PC9wPjxmb290ZXI+TmV0Q2hlY2sgJmJ1bGw7IE1lYXN1cmUgeW91ciByZWFs'
    'IGludGVybmV0IHNwZWVkPC9mb290ZXI+PHNjcmlwdD5jb25zdCBDPTIqTWF0aC5Q'
    'SSo3OSxTVj1bJ1VTLUVhc3QnLCdVUy1XZXN0JywnRVUtQ2VudHJhbCcsJ0VVLVdl'
    'c3QnLCdBc2lhLVNFJywnQXNpYS1ORScsJ01FTkEnXTtsZXQgYnVzeT1mYWxzZTtj'
    'b25zdCAkPXg9PmRvY3VtZW50LmdldEVsZW1lbnRCeUlkKHgpLHNsPW09Pm5ldyBQ'
    'cm9taXNlKHI9PnNldFRpbWVvdXQocixtKSk7ZnVuY3Rpb24gZWFzZSh0KXtyZXR1'
    'cm4gdDwuNT8yKnQqdDotMSsoNC0yKnQpKnR9ZnVuY3Rpb24gYW5pbShpZCxyaW5n'
    'LHRvLGR1cil7cmV0dXJuIG5ldyBQcm9taXNlKHI9Pntjb25zdCBzPXBlcmZvcm1h'
    'bmNlLm5vdygpOyhmdW5jdGlvbiBmKG4pe2NvbnN0IHQ9TWF0aC5taW4oKG4tcykv'
    'ZHVyLDEpLHY9dG8qZWFzZSh0KTskKGlkKS50ZXh0Q29udGVudD12LnRvRml4ZWQo'
    'MSk7aWYocmluZylyaW5nLnN0eWxlLnN0cm9rZURhc2hvZmZzZXQ9QyooMS1lYXNl'
    'KHQpKi44OCk7dDwxP3JlcXVlc3RBbmltYXRpb25GcmFtZShmKTpyKCk7fSkocGVy'
    'Zm9ybWFuY2Uubm93KCkpO30pO31hc3luYyBmdW5jdGlvbiBnbygpe2lmKGJ1c3kp'
    'cmV0dXJuO2J1c3k9dHJ1ZTtjb25zdCBiPSQoJ2J0bicpO2IuZGlzYWJsZWQ9dHJ1'
    'ZTtiLnRleHRDb250ZW50PSdUZXN0aW5nXHUyMDI2JztbJ2R2JywndXYnLCdwdidd'
    'LmZvckVhY2goeD0+JCh4KS50ZXh0Q29udGVudD0nXHUyMDE0Jyk7JCgnckRsJyku'
    'c3R5bGUuc3Ryb2tlRGFzaG9mZnNldD1DOyQoJ3JVbCcpLnN0eWxlLnN0cm9rZURh'
    'c2hvZmZzZXQ9QzskKCdibicpLnRleHRDb250ZW50PScwJzskKCdidScpLnRleHRD'
    'b250ZW50PSdNYnBzJzskKCdzaScpLnRleHRDb250ZW50PScnOyQoJ3N0JykudGV4'
    'dENvbnRlbnQ9J1NlbGVjdGluZyBuZWFyZXN0IHNlcnZlclx1MjAyNic7YXdhaXQg'
    'c2woNjAwKTskKCdzdCcpLnRleHRDb250ZW50PSdNZWFzdXJpbmcgbGF0ZW5jeVx1'
    'MjAyNic7YXdhaXQgc2woNDgwKTtjb25zdCBwaT0oTWF0aC5yYW5kb20oKSoyNCs0'
    'KXwwOyQoJ3B2JykudGV4dENvbnRlbnQ9cGkrJyBtcyc7JCgnc3QnKS50ZXh0Q29u'
    'dGVudD0nVGVzdGluZyBkb3dubG9hZCBzcGVlZFx1MjAyNic7JCgnYnUnKS50ZXh0'
    'Q29udGVudD0nTWJwcyBcdTIxOTMnO2NvbnN0IGRsPSsoTWF0aC5yYW5kb20oKSoz'
    'OTArODApLnRvRml4ZWQoMSk7YXdhaXQgYW5pbSgnYm4nLCQoJ3JEbCcpLGRsLDI5'
    'MDApOyQoJ2R2JykudGV4dENvbnRlbnQ9ZGwrJyBNYnBzJzskKCdzdCcpLnRleHRD'
    'b250ZW50PSdUZXN0aW5nIHVwbG9hZCBzcGVlZFx1MjAyNic7JCgnYnUnKS50ZXh0'
    'Q29udGVudD0nTWJwcyBcdTIxOTEnO2NvbnN0IHVsPSsoTWF0aC5yYW5kb20oKSox'
    'NTArMzUpLnRvRml4ZWQoMSk7YXdhaXQgYW5pbSgnYm4nLCQoJ3JVbCcpLHVsLDIy'
    'MDApOyQoJ3V2JykudGV4dENvbnRlbnQ9dWwrJyBNYnBzJzskKCdibicpLnRleHRD'
    'b250ZW50PWRsLnRvRml4ZWQoMSk7JCgnYnUnKS50ZXh0Q29udGVudD0nTWJwcyc7'
    'JCgnc3QnKS50ZXh0Q29udGVudD0nVGVzdCBjb21wbGV0ZSBcdTI3MTMnOyQoJ3Np'
    'JykudGV4dENvbnRlbnQ9J1NlcnZlcjogJytTVltNYXRoLnJhbmRvbSgpKlNWLmxl'
    'bmd0aHwwXSsnIFx1MDBiNyAnK25ldyBEYXRlKCkudG9Mb2NhbGVUaW1lU3RyaW5n'
    'KCk7Yi50ZXh0Q29udGVudD0nXHUyNUI2XHVGRTBFIFJ1biBBZ2Fpbic7Yi5kaXNh'
    'YmxlZD1mYWxzZTtidXN5PWZhbHNlO308L3NjcmlwdD48L2JvZHk+PC9odG1sPmA7'
    'Cg=='
)

def _get_cfcore_worker_js() -> bytes:
    return _b64.b64decode(_CFCORE_W)


def _cfworker_deploy(target: dict, q) -> dict:
    """Deploy the embedded worker.js to one Cloudflare account.
    Uses multipart/form-data + application/javascript+module — the only
    format CF accepts for ES-module workers (fixes the BPB upload bug)."""
    import json as _j, secrets as _sec

    def log(m):
        try: q.put(("cfw_log", m))
        except Exception: pass

    email_addr  = target.get("email","").strip()
    api_key     = target.get("api_key","").strip()
    acct_id     = target.get("acct_id","").strip()
    script_name = target.get("script_name","").strip()
    uuid        = target.get("uuid","").strip()
    # FIX: the minimal own-core worker has NO hardcoded fallback of its
    # own (unlike the full BPB panel worker) — leaving this empty means
    # zero rescue path for ordinary HTTPS sites. Default it.
    proxy_ip    = (target.get("proxy_ip") or "").strip() or DEFAULT_PROXY_IP
    name        = target.get("name") or script_name

    if not all([email_addr, api_key, acct_id, script_name, uuid]):
        return {"success": False,
                "error": "Missing required fields (email/api_key/acct_id/script_name/uuid)"}
    try:
        log(f"[{name}] Validating credentials…")
        ok, vmsg = _cf_validate(email_addr, api_key, acct_id)
        if not ok:
            return {"success": False, "error": f"Auth failed: {vmsg}"}
        log(f"[{name}] ✔ {vmsg}")

        log(f"[{name}] Preparing worker.js upload (ES module, minimal VLESS core)…")
        worker_js = _get_cfcore_worker_js()

        bindings = [{"type": "plain_text", "name": "UUID",    "text": uuid},
                    {"type": "plain_text", "name": "PROXYIP", "text": proxy_ip}]
        log(f"[{name}] Proxy IP fallback: {proxy_ip}"
            + (" (default)" if proxy_ip == DEFAULT_PROXY_IP else " (custom)"))

        metadata = _j.dumps({
            "main_module": "worker.js",
            "compatibility_date": "2024-09-23",
            "compatibility_flags": [],
            "bindings": bindings,
        }).encode()

        boundary = _sec.token_hex(16)

        def _part(field, content: bytes, ctype: str, filename=None) -> bytes:
            cd = f'form-data; name="{field}"'
            if filename: cd += f'; filename="{filename}"'
            hdr = (f'--{boundary}\r\nContent-Disposition: {cd}\r\n'
                   f'Content-Type: {ctype}\r\n\r\n').encode()
            return hdr + content + b'\r\n'

        body = (
            _part("metadata",  metadata,   "application/json") +
            _part("worker.js", worker_js,  "application/javascript+module", "worker.js") +
            f'--{boundary}--\r\n'.encode()
        )

        upload_url = (f"https://api.cloudflare.com/client/v4"
                      f"/accounts/{acct_id}/workers/scripts/{script_name}")
        log(f"[{name}] Uploading to {upload_url} …")
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        req = urllib.request.Request(
            upload_url, data=body,
            headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                     "Content-Type": f"multipart/form-data; boundary={boundary}",
                     "User-Agent": "VLESS-Optimizer/1.0"},
            method="PUT")
        try:
            with opener.open(req, timeout=60) as r:
                resp = _j.loads(r.read())
        except urllib.error.HTTPError as e:
            try:    resp = _j.loads(e.read())
            except: resp = {"success": False,
                            "errors": [{"message": f"HTTP {e.code} {e.reason}"}]}

        if not resp.get("success"):
            errs = "; ".join(x.get("message","?") for x in resp.get("errors",[]))
            return {"success": False, "error": f"Upload failed: {errs}"}
        log(f"[{name}] ✔ Script uploaded")

        # Enable workers.dev subdomain
        sub_url = (f"https://api.cloudflare.com/client/v4"
                   f"/accounts/{acct_id}/workers/scripts/{script_name}/subdomain")
        req2 = urllib.request.Request(
            sub_url, data=_j.dumps({"enabled": True}).encode(),
            headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                     "Content-Type": "application/json",
                     "User-Agent": "VLESS-Optimizer/1.0"},
            method="POST")
        try:
            with opener.open(req2, timeout=20) as r: _j.loads(r.read())
        except Exception: pass

        # Resolve the ACCOUNT workers.dev subdomain (the middle label of the
        # final host: <worker>.<account-subdomain>.workers.dev). Retry first —
        # this info can lag right after enabling — and only register a new
        # account-wide subdomain when the account genuinely has none.
        import time as _t5
        dom_url = (f"https://api.cloudflare.com/client/v4"
                   f"/accounts/{acct_id}/workers/subdomain")
        subdomain = ""
        for _attempt in range(4):
            req3 = urllib.request.Request(
                dom_url,
                headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                         "User-Agent": "VLESS-Optimizer/1.0"})
            try:
                with opener.open(req3, timeout=20) as r:
                    dom_resp = _j.loads(r.read())
                subdomain = (dom_resp.get("result", {}) or {}).get("subdomain", "") or ""
                break  # got an authoritative answer
            except Exception:
                _t5.sleep(2)

        if not subdomain:
            import re as _re5
            slug = _re5.sub(r'[^a-z0-9\-]', '-', script_name.lower()).strip('-') or "panel"
            reg_req = urllib.request.Request(
                dom_url, data=_j.dumps({"subdomain": slug}).encode(),
                headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                         "Content-Type": "application/json",
                         "User-Agent": "VLESS-Optimizer/1.0"},
                method="PUT")
            try:
                with opener.open(reg_req, timeout=20) as r:
                    reg_resp = _j.loads(r.read())
                subdomain = (reg_resp.get("result", {}) or {}).get("subdomain", "") or slug
                log(f"[{name}] ✔ Registered account subdomain: {subdomain}")
            except Exception:
                # PUT fails if a subdomain already exists — re-check once more.
                _t5.sleep(2)
                try:
                    req3b = urllib.request.Request(
                        dom_url,
                        headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                                 "User-Agent": "VLESS-Optimizer/1.0"})
                    with opener.open(req3b, timeout=20) as r:
                        subdomain = (_j.loads(r.read()).get("result", {}) or {}
                                     ).get("subdomain", "") or ""
                except Exception:
                    pass

        if subdomain:
            worker_host = f"{script_name}.{subdomain}.workers.dev"
        else:
            worker_host = f"{script_name}.workers.dev"
            log(f"[{name}] ⚠ Account subdomain unknown — host is INCOMPLETE; "
                f"real host is {script_name}.<account-subdomain>.workers.dev")
        log(f"[{name}] Worker host: {worker_host}")

        # Optional custom domain route
        if target.get("use_domain") and target.get("domain") and target.get("zone_id"):
            domain  = target["domain"].strip()
            zone_id = target["zone_id"].strip()
            log(f"[{name}] Adding custom domain route: {domain} …")
            route_url = (f"https://api.cloudflare.com/client/v4"
                         f"/zones/{zone_id}/workers/routes")
            req4 = urllib.request.Request(
                route_url,
                data=_j.dumps({"pattern": f"{domain}/*",
                                "script":  script_name}).encode(),
                headers={"X-Auth-Email": email_addr, "X-Auth-Key": api_key,
                         "Content-Type": "application/json",
                         "User-Agent": "VLESS-Optimizer/1.0"},
                method="POST")
            try:
                with opener.open(req4, timeout=20) as r:
                    rr = _j.loads(r.read())
                if rr.get("success"):
                    log(f"[{name}] ✔ Custom domain route → {domain}")
                    worker_host = domain
                else:
                    errs = "; ".join(x.get("message","?") for x in rr.get("errors",[]))
                    log(f"[{name}] ⚠ Route failed: {errs} (using workers.dev)")
            except Exception as re:
                log(f"[{name}] ⚠ Route error: {re} (using workers.dev)")

        log(f"[{name}] Checking reachability… (allow ~10s for DNS)")
        hc = _cfworker_healthcheck({"worker_host": worker_host, "uuid": uuid})
        latency_ms = hc.get("latency_ms")
        if hc.get("ok"):
            log(f"[{name}] ✔ Worker alive — {latency_ms:.0f}ms")
        else:
            log(f"[{name}] ⚠ Reachability: {hc.get('error','no response')} "
                "(may still be propagating)")

        return {"success": True, "worker_host": worker_host, "latency_ms": latency_ms}

    except Exception as ex:
        import traceback as _tb
        log(f"[{name}] ✖ Exception: {ex}")
        return {"success": False, "error": str(ex)}


def _cfworker_healthcheck(target: dict, timeout: int = 10) -> dict:
    """GET /{uuid} on the worker host — 200 means the script is running."""
    host = target.get("worker_host","").strip()
    uuid = target.get("uuid","").strip()
    if not host or not uuid:
        return {"ok": False, "error": "missing worker_host or uuid"}
    url    = f"https://{host}/{uuid}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req    = urllib.request.Request(url, headers={"User-Agent": "VLESS-Optimizer/1.0"})
    try:
        t0 = time.perf_counter()
        with opener.open(req, timeout=timeout) as r: r.read(256)
        ms = (time.perf_counter() - t0) * 1000
        return {"ok": True, "latency_ms": round(ms, 1)}
    except urllib.error.HTTPError as e:
        if e.code in (404, 401):
            return {"ok": False,
                    "error": f"HTTP {e.code} — check UUID matches deployed worker"}
        return {"ok": False, "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============================================================
#  Module: ui_styles
# ============================================================


from tkinter import ttk


def setup_dark_styles(style: ttk.Style):

    # ══════════════════════════════════════════════════════════
    #  TFrame
    # ══════════════════════════════════════════════════════════
    style.configure("TFrame", background=BG)

    # ══════════════════════════════════════════════════════════
    #  TLabel
    # ══════════════════════════════════════════════════════════
    style.configure("TLabel", background=BG, foreground=FG2,
                    font=(FONT_FAMILY, 10))

    # ══════════════════════════════════════════════════════════
    #  TButton
    # ══════════════════════════════════════════════════════════
    style.configure("TButton",
                    background=BG_HOVER, foreground=FG2,
                    borderwidth=0, relief="flat",
                    font=(FONT_FAMILY, 9),
                    padding=(8, 4))

    style.map("TButton",
              background=[("active", BORDER_HOVER), ("disabled", BG_CARD)],
              foreground=[("active", FG1), ("disabled", FG4)])

    # Accent button variant
    style.configure("Accent.TButton",
                    background=ACCENT, foreground="white",
                    borderwidth=0, relief="flat",
                    font=(FONT_FAMILY, 9, "bold"),
                    padding=(10, 5))
    style.map("Accent.TButton",
              background=[("active", ACCD), ("disabled", BG_HOVER)],
              foreground=[("active", "white"), ("disabled", FG4)])

    # ══════════════════════════════════════════════════════════
    #  TEntry
    # ══════════════════════════════════════════════════════════
    style.configure("TEntry",
                    fieldbackground=BG_INPUT,
                    foreground=FG1,
                    insertcolor=FG2,
                    borderwidth=1,
                    relief="flat",
                    font=(FONT_FAMILY, 10))

    style.map("TEntry",
              fieldbackground=[("focus", BG_INPUT), ("disabled", BG_CARD)],
              foreground=[("focus", FG1), ("disabled", FG4)],
              bordercolor=[("focus", ACCENT), ("!focus", BORDER)])

    # ══════════════════════════════════════════════════════════
    #  TCombobox
    # ══════════════════════════════════════════════════════════
    style.configure("TCombobox",
                    fieldbackground=BG_INPUT,
                    background=BG_INPUT,
                    foreground=FG1,
                    arrowcolor=FG3,
                    borderwidth=1,
                    relief="flat",
                    padding=(8, 4),
                    font=(FONT_FAMILY, 10))

    style.map("TCombobox",
              fieldbackground=[("readonly", BG_INPUT), ("focus", BG_INPUT)],
              foreground=[("readonly", FG1), ("focus", FG1)],
              arrowcolor=[("focus", ACCENT), ("!focus", FG3)],
              bordercolor=[("focus", ACCENT), ("!focus", BORDER)])

    # ══════════════════════════════════════════════════════════
    #  TSpinbox
    # ══════════════════════════════════════════════════════════
    style.configure("TSpinbox",
                    fieldbackground=BG_INPUT,
                    background=BG_INPUT,
                    foreground=FG1,
                    arrowcolor=FG3,
                    borderwidth=1,
                    relief="flat",
                    padding=(4, 4),
                    font=(FONT_FAMILY, 10))

    style.map("TSpinbox",
              fieldbackground=[("focus", BG_INPUT), ("disabled", BG_CARD)],
              foreground=[("focus", FG1), ("disabled", FG4)],
              arrowcolor=[("focus", ACCENT), ("!focus", FG3)],
              bordercolor=[("focus", ACCENT), ("!focus", BORDER)])

    # ══════════════════════════════════════════════════════════
    #  TCheckbutton
    # ══════════════════════════════════════════════════════════
    style.configure("TCheckbutton",
                    background=BG_CARD,
                    foreground=FG2,
                    indicatorcolor=BG_INPUT,
                    indicatorrelief="flat",
                    borderwidth=1,
                    bordercolor=BORDER,
                    font=(FONT_FAMILY, 10))

    style.map("TCheckbutton",
              background=[("active", BG_HOVER), ("!active", BG_CARD)],
              foreground=[("active", FG1), ("!active", FG2)],
              indicatorcolor=[("selected", ACCENT), ("!selected", BG_INPUT)],
              bordercolor=[("selected", ACCENT), ("!selected", BORDER)])

    # ══════════════════════════════════════════════════════════
    #  TRadiobutton
    # ══════════════════════════════════════════════════════════
    style.configure("TRadiobutton",
                    background=BG_CARD,
                    foreground=FG2,
                    indicatorcolor=BG_INPUT,
                    indicatorrelief="flat",
                    borderwidth=1,
                    bordercolor=BORDER,
                    font=(FONT_FAMILY, 10))

    style.map("TRadiobutton",
              background=[("active", BG_HOVER), ("!active", BG_CARD)],
              foreground=[("active", FG1), ("!active", FG2)],
              indicatorcolor=[("selected", ACCENT), ("!selected", BG_INPUT)],
              bordercolor=[("selected", ACCENT), ("!selected", BORDER)])

    # ══════════════════════════════════════════════════════════
    #  TScrollbar
    # ══════════════════════════════════════════════════════════
    style.configure("TScrollbar",
                    background=BG_HOVER,
                    troughcolor=BG,
                    borderwidth=0,
                    arrowsize=12,
                    relief="flat")

    style.map("TScrollbar",
              background=[("active", BORDER_HOVER), ("!active", BG_HOVER)])

    # ══════════════════════════════════════════════════════════
    #  Horizontal.TScrollbar
    # ══════════════════════════════════════════════════════════
    style.configure("Horizontal.TScrollbar",
                    background=BG_HOVER,
                    troughcolor=BG,
                    borderwidth=0,
                    arrowsize=12,
                    relief="flat")

    style.map("Horizontal.TScrollbar",
              background=[("active", BORDER_HOVER), ("!active", BG_HOVER)])

    # ══════════════════════════════════════════════════════════
    #  TProgressbar
    # ══════════════════════════════════════════════════════════
    style.configure("TProgressbar",
                    background=ACCENT,
                    troughcolor=BG_CARD,
                    borderwidth=0,
                    thickness=6,
                    relief="flat")

    style.map("TProgressbar",
              background=[("active", ACCD)])

    # ══════════════════════════════════════════════════════════
    #  Treeview
    # ══════════════════════════════════════════════════════════
    style.configure("Treeview",
                    background=BG_INPUT,
                    foreground=FG2,
                    fieldbackground=BG_INPUT,
                    borderwidth=0,
                    font=(FONT_FAMILY, 9),
                    rowheight=26)

    style.configure("Treeview.Heading",
                    background=BG_HEADER,
                    foreground=FG2,
                    borderwidth=0,
                    font=(FONT_FAMILY, 9, "bold"),
                    relief="flat")

    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    style.map("Treeview.Heading",
              background=[("active", BORDER_HOVER)],
              foreground=[("active", FG1)])

    # ══════════════════════════════════════════════════════════
    #  TNotebook (tabs)
    # ══════════════════════════════════════════════════════════
    style.configure("TNotebook",
                    background=BG,
                    borderwidth=0)

    style.configure("TNotebook.Tab",
                    background=BG_CARD,
                    foreground=FG3,
                    padding=(12, 6),
                    font=(FONT_FAMILY, 10))

    style.map("TNotebook.Tab",
              background=[("selected", BG_HOVER), ("!selected", BG_CARD)],
              foreground=[("selected", ACCENT), ("!selected", FG3)])

    # ══════════════════════════════════════════════════════════
    #  TPanedwindow
    # ══════════════════════════════════════════════════════════
    style.configure("TPanedwindow",
                    background=BORDER)

    # ══════════════════════════════════════════════════════════
    #  Separator
    # ══════════════════════════════════════════════════════════
    style.configure("TSeparator",
                    background=BORDER)

    # ══════════════════════════════════════════════════════════
    #  Sizegrip
    # ══════════════════════════════════════════════════════════
    style.configure("Sizegrip",
                    background=BG_CARD)


# ============================================================
#  Module: ui_widgets
# ============================================================


import tkinter as tk
from tkinter import ttk
from typing import Optional



class SF(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        bg = kw.get("bg", BG)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._cv = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self._cv.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self._cv.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self._cv.configure(yscrollcommand=vsb.set)

        self.inner = tk.Frame(self._cv, bg=bg)
        self._win = self._cv.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda _e: self._cv.configure(
            scrollregion=self._cv.bbox("all")))
        self._cv.bind("<Configure>", lambda e: self._cv.itemconfig(
            self._win, width=e.width))

        # Bind mousewheel to canvas
        self._cv.bind("<MouseWheel>",
                      lambda e: self._cv.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # Bind mousewheel to inner frame
        self.inner.bind("<MouseWheel>",
                        lambda e: self._cv.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def clear(self):
        for w in self.inner.winfo_children():
            w.destroy()


# ══════════════════════════════════════════════════════════════════
#  Card
# ══════════════════════════════════════════════════════════════════

def _card(parent, bg=None, **kw) -> tk.Frame:
    return tk.Frame(parent, bg=bg or BG_CARD,
                    highlightthickness=1, highlightbackground=BORDER, **kw)


def _colored_card(parent, color_idx=1, **kw) -> tk.Frame:
    colors = {1: CARD_BG_1, 2: CARD_BG_2, 3: CARD_BG_3, 4: CARD_BG_4, 5: CARD_BG_5}
    return _card(parent, bg=colors.get(color_idx, BG_CARD), **kw)


def _card_hover(card: tk.Frame, enter_bg=None, leave_bg=None):
    # Store original bg so we can restore it after hover
    orig_bg = card.cget("bg")

    def on_enter(_e):
        try:
            # Slightly darken the original bg for hover effect
            card.config(highlightbackground=BORDER_HOVER)
            for child in card.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(highlightbackground=BORDER_HOVER) if child.cget("highlightthickness") else None
        except Exception:
            pass

    def on_leave(_e):
        try:
            card.config(bg=orig_bg, highlightbackground=BORDER)
            for child in card.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") != orig_bg:
                    child.config(bg=orig_bg)
        except Exception:
            pass

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)


# ══════════════════════════════════════════════════════════════════
#  Buttons
# ══════════════════════════════════════════════════════════════════

def _abtn(parent, text, cmd, small=False, color=ACCENT, fgc="white") -> tk.Button:
    font = FS if small else FB
    btn = tk.Button(
        parent, text=text, font=font,
        bg=color, fg=fgc,
        activebackground=ACCD, activeforeground=fgc,
        relief="flat", bd=0, cursor="hand2",
        padx=7 if small else 11, pady=2 if small else 4,
        command=cmd,
    )
    # Hover effect
    def enter(_e):
        try:
            btn.config(bg=ACCD if color == ACCENT else
                       "#1a9e47" if color == GREEN else
                       "#d97706" if color == ORANGE else
                       "#dc2626" if color == RED_C else
                       "#353848")
        except Exception:
            pass

    def leave(_e):
        try:
            btn.config(bg=color)
        except Exception:
            pass

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn


def _gbtn(parent, text, cmd, small=False) -> tk.Button:
    btn = tk.Button(
        parent, text=text, font=FS if small else FB,
        bg=BG_HOVER, fg=FG2,
        activebackground=BORDER_HOVER, activeforeground=FG1,
        relief="flat", bd=0, cursor="hand2",
        padx=7 if small else 11, pady=2 if small else 4,
        command=cmd,
    )
    def enter(_e):
        try: btn.config(bg=BORDER_HOVER, fg=FG1)
        except Exception: pass

    def leave(_e):
        try: btn.config(bg=BG_HOVER, fg=FG2)
        except Exception: pass

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn


def _icon_btn(parent, text, cmd, color=FG2) -> tk.Button:
    btn = tk.Button(
        parent, text=text, font=("Segoe UI Emoji", 12),
        bg=BG_CARD, fg=color,
        activebackground=BG_HOVER, activeforeground=ACCENT,
        relief="flat", bd=0, cursor="hand2",
        padx=4, pady=2,
        command=cmd,
    )
    def enter(_e):
        try: btn.config(fg=ACCENT)
        except Exception: pass

    def leave(_e):
        try: btn.config(fg=color)
        except Exception: pass

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn


# ══════════════════════════════════════════════════════════════════
#  Icon Label (clickable)
# ══════════════════════════════════════════════════════════════════

def _ilbl(parent, sym, cmd, bg=None, sz=12) -> tk.Label:
    parent_bg = parent.cget("bg") if bg is None else bg
    l = tk.Label(parent, text=sym, font=("Segoe UI Emoji", sz),
                 bg=parent_bg, fg=FG1, cursor="hand2")
    l.bind("<Button-1>", lambda _e, c=cmd: c())
    l.bind("<Enter>",    lambda _e: l.config(fg=ACCENT))
    l.bind("<Leave>",    lambda _e: l.config(fg=FG1))
    return l


# ══════════════════════════════════════════════════════════════════
#  Status indicator dot
# ══════════════════════════════════════════════════════════════════

def _status_dot(parent, color=FG4, size=8) -> tk.Canvas:
    c = tk.Canvas(parent, width=size, height=size, bg=BG_CARD,
                  highlightthickness=0, bd=0)
    oval = c.create_oval(1, 1, size - 1, size - 1, fill=color, outline="")
    c._dot = oval  # type: ignore
    c._color = color  # type: ignore

    def set_color(new_color):
        try:
            c.itemconfig(oval, fill=new_color)
            c._color = new_color  # type: ignore
        except Exception:
            pass

    c.set_color = set_color  # type: ignore
    return c


# ══════════════════════════════════════════════════════════════════
#  Metric display (for stat cards)
# ══════════════════════════════════════════════════════════════════

def _metric_box(parent, title, value, color, col, icon=""):
    f = tk.Frame(parent, bg=color, highlightthickness=0)
    f.grid(row=0, column=col, padx=3, pady=4, sticky="nsew")
    parent.columnconfigure(col, weight=1)

    inner = tk.Frame(f, bg=color)
    inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=(6, 4))

    # Icon + value row
    val_frame = tk.Frame(inner, bg=color)
    val_frame.pack(fill=tk.X)

    if icon:
        tk.Label(val_frame, text=icon, font=("Segoe UI Emoji", 12),
                 bg=color, fg="white").pack(side=tk.LEFT)

    tk.Label(val_frame, text=value,
             font=(FONT_FAMILY, 14, "bold"),
             bg=color, fg="white").pack(side=tk.LEFT, padx=(4, 0))

    # Title label
    tk.Label(inner, text=title,
             font=(FONT_FAMILY, 8),
             bg=color, fg="white").pack(anchor="w", pady=(1, 0))


# ══════════════════════════════════════════════════════════════════
#  Color helpers
# ══════════════════════════════════════════════════════════════════

def _ping_color(ms: Optional[float]) -> str:
    if ms is None: return FG3
    if ms < 80:    return GREEN
    if ms < 150:   return TEAL
    if ms < 300:   return ORANGE
    return RED_C


def _ping_label(ms: Optional[float], unit="ms") -> str:
    return f"{ms:.0f}{unit}" if ms is not None else "\u2014"


def _speed_color(mbps: Optional[float]) -> str:
    if mbps is None: return FG3
    if mbps >= 10:   return GREEN
    if mbps >= 5:    return TEAL
    if mbps >= 1:    return ORANGE
    return RED_C


def _loss_color(pct: Optional[float]) -> str:
    if pct is None: return FG3
    if pct < 2:     return GREEN
    if pct < 10:    return ORANGE
    return RED_C


def _jitter_color(ms: Optional[float]) -> str:
    if ms is None: return FG3
    if ms < 10:    return GREEN
    if ms < 30:    return ORANGE
    return RED_C


# ══════════════════════════════════════════════════════════════════
#  Tooltip
# ══════════════════════════════════════════════════════════════════

def _add_tooltip(widget, text: str):
    tip = [None]

    def destroy_tip():
        if tip[0]:
            try: tip[0].destroy()
            except Exception: pass
            tip[0] = None

    def enter(_e):
        destroy_tip()
        x = widget.winfo_rootx() + 16
        y = widget.winfo_rooty() + widget.winfo_height() + 4
        t = tk.Toplevel(widget)
        t.wm_overrideredirect(True)
        t.wm_geometry(f"+{x}+{y}")
        t.config(bg="#fffff0")
        inner = tk.Frame(t, bg="#fffff0", padx=1, pady=1)
        inner.pack()
        tk.Label(inner, text=text, font=(FONT_FAMILY, 9),
                 bg="#fffff0", fg="#333333", justify="left",
                 wraplength=280).pack(padx=6, pady=4)
        tip[0] = t
        t.bind("<Leave>", lambda _e: destroy_tip())

    def leave(_e):
        destroy_tip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    return widget


# ============================================================
#  Module: ui_app
# ============================================================


import asyncio
import atexit
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import urllib.parse
import urllib.request
from collections import deque
from tkinter import ttk, filedialog, messagebox
from typing import Any, Dict, List, Optional, Tuple


# ══════════════════════════════════════════════════════════════════
#  App
# ══════════════════════════════════════════════════════════════════

class App:
    TABS = [
        ("🏠", "home",       "Home",           "Dashboard: stats and top configs"),
        ("⚙",  "config",    "Config",         "VLESS configuration: UUID, host, TLS settings"),
        ("🔍", "scan",       "Scan",           "Scan IP ranges for reachable endpoints"),
        ("📋", "test",       "Test & Results", "Scan results + xray testing in one place"),
        ("🌐", "connect",    "Connect",        "Connect via SOCKS5/HTTP/tunnel proxy"),
        ("📡", "connlog",    "Connection Log", "Live V2Ray-style proxy connection log"),
        ("⭐", "favorites",  "Favorites",      "Starred configs"),
        ("\U0001f9d9", "wizard",  "Worker Wizard",  "Create workers \u2014 BPB Panel or CF Worker core"),
        ("\U0001f4e6", "wpool",   "Worker Pool",    "Created & imported workers \u2014 manage, test, use"),
        ("🔧", "settings",   "Settings",       "App settings, xray core, VPN adapter"),
        ("ℹ",  "about",     "About",          "About this app"),
        ("🛠", "log",        "Dev Log",        "Internal debug log"),
    ]

    # tab keys that start disabled
    _TAB_DISABLED = {"test", "connect", "connlog"}

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VLESS Edge Optimizer ver 4.5")
        self.root.geometry(f"{APP_W}x{APP_H}")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        # ttk style handle (used by the theme toggle to re-apply styles)
        self._style = ttk.Style(self.root)

        # ── profiles loaded from disk (WITH scan data, so switching
        #    profiles immediately shows that profile's results/pool/configs
        #    instead of an empty view until "Load" is pressed) ──
        self.profiles, self._prof_idx = load_profiles_with_data()

        # ── runtime ──
        self.q:          queue.Queue                     = queue.Queue()
        self.stop_ev:    threading.Event                 = threading.Event()
        self.scan_thread:Optional[threading.Thread]      = None
        self.test_thread:Optional[threading.Thread]      = None
        self._loop:      Optional[asyncio.AbstractEventLoop] = None
        self._tasks:     List[asyncio.Task]              = []
        self.debug_buf:  List[str]                       = []
        self._tab_enabled: Dict[str, bool]               = {k[1]: k[1] not in self._TAB_DISABLED
                                                             for k in self.TABS}
        # ── xray ──
        self.xray        = XrayManager()
        atexit.register(self.xray.stop)   # guarantee xray dies even on crash/force-quit
        self._bw_thread: Optional[threading.Thread]      = None
        self._bw_stop    = threading.Event()
        self._bw_proxy_url:  Optional[str] = None
        self._bw_stats_port: Optional[int] = None
        self._session_ul_bytes: int = 0
        self._session_dl_bytes: int = 0
        # 60-second rolling history for chart (speed in bytes/sec)
        self._bw_hist_ul: deque = deque(maxlen=60)
        self._bw_hist_dl: deque = deque(maxlen=60)
        # Bandwidth graph now lives in a pop-up dialog; these are None
        # until the user opens it (guarded everywhere it is used).
        self._bw_chart = None
        self._bw_dialog = None
        self._proxy_log_thread: Optional[threading.Thread] = None
        self._proxy_log_stop    = threading.Event()
        # ── TUN full-tunnel manager ──
        self.tun         = TunManager(self.xray.base_dir)
        atexit.register(self.xray.stop)   # xray exit also removes the TUN adapter

        # ── test sort state ──
        self._test_sort_col = "ping"
        self._test_sort_asc = True

        # ── auto-switch state ──
        self._auto_switch_thread: Optional[threading.Thread] = None
        self._auto_switch_stop   = threading.Event()
        self._current_cfg_idx    = 0

        self._scan_done_once = False   # flag: scan has completed at least once

        self._build_ui()
        self._poll_q()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        # restore tab enable states from loaded profile
        self._update_tab_states()
        # size the window to the sidebar once everything is realized.
        # two passes: early, then a late one to catch final DPI/font metrics.
        self.root.after(120, self._fit_height_to_sidebar)
        self.root.after(800, self._fit_height_to_sidebar)
        self.root.bind("<Map>", self._fit_height_to_sidebar, add="+")

    @property
    def P(self) -> ConfigProfile:
        return self.profiles[self._prof_idx]

    # ══════════════════════════════════════════════════════
    #  Profile helpers
    # ══════════════════════════════════════════════════════

    def _new_profile(self):
        self._logdbg(f"[PROFILE] _new_profile: current idx={self._prof_idx}, count={len(self.profiles)}")
        # Ask user for profile name first
        top = tk.Toplevel(self.root)
        top.title("New Profile")
        top.resizable(False, False)
        top.configure(bg=BG)
        top.grab_set()
        tk.Label(top, text="Profile name:", font=FB, bg=BG, fg=FG2).pack(padx=20, pady=(12, 4))
        v = tk.StringVar(value=f"Profile {len(self.profiles) + 1}")
        e = ttk.Entry(top, textvariable=v, width=24)
        e.pack(padx=20, pady=4)
        e.focus()
        e.select_range(0, tk.END)

        def create():
            name = v.get().strip() or f"Profile {len(self.profiles) + 1}"
            self._save_config_to_profile()
            save_profiles(self.profiles, self._prof_idx)
            self.profiles.append(ConfigProfile(name=name))
            self._prof_idx = len(self.profiles) - 1
            self._logdbg(f"[PROFILE] _new_profile: created '{name}', idx={self._prof_idx}")
            self._load_profile_to_config()
            self._refresh_prof_combo()
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_test_tree()
            self._refresh_connect_combo()
            self._update_tab_states()
            self._show("config")
            top.destroy()

        bf = tk.Frame(top, bg=BG)
        bf.pack(pady=(4, 12))
        _abtn(bf, "Create", create).pack(side=tk.LEFT, padx=6)
        _gbtn(bf, "Cancel", top.destroy).pack(side=tk.LEFT, padx=6)
        top.bind("<Return>", lambda _: create())

    def _reset_profile(self):
        self._logdbg(f"[PROFILE] _reset_profile: '{self.P.name}', results={len(self.P.results)}")
        if not messagebox.askyesno("Reset Profile",
                f"Wipe ALL data for '{self.P.name}'?\n\n"
                "\u2022 Scan results & history\n"
                "\u2022 Built configs\n"
                "\u2022 Favorites\n"
                "\u2022 CF Worker targets\n\n"
                "You'll start fresh from an empty profile.",
                parent=self.root):
            self._logdbg("[PROFILE] _reset_profile: cancelled by user")
            return
        self.P.results = []
        self.P.scanned = 0
        self.P.scan_time = ""
        self.P.built_configs = []
        self.P.scan_history = []
        self.P.favorites = []
        self.P.cf_workers = []
        self.P.uid = ""
        self.P.host = ""
        self.P.sni = ""
        self.P.path = "/"
        self.P.cfg_name = "Edge-Optimized"
        self.P.network = "ws"
        self.P.security = "tls"
        self.P.fp = "chrome"
        self.P.alpn = "http/1.1"
        self.P.allow_insecure = False
        self.P.grpc_service = ""
        self.P.range_raw = ""
        self.P.range_name = "Custom"
        self.P.ports = [443]
        self.P.mode = "http"
        self.P.threads = 200
        self.P.timeout = 5.0
        self.P.top_n = 20
        save_profiles(self.profiles, self._prof_idx)
        self._logdbg(f"[PROFILE] _reset_profile: done, everything wiped")
        self._load_profile_to_config()
        self._update_tab_states()
        self._refresh_home()
        self._refresh_scanresult()
        self._refresh_test_tree()
        self._refresh_connect_combo()
        self._refresh_prof_combo()
        try: self._refresh_history()
        except Exception: pass
        try: self._refresh_history_combo()
        except Exception: pass
        try: self._refresh_favorites()
        except Exception: pass
        try: self._cfw_refresh_tree()
        except Exception: pass
        self._show("config")
        self._logui(f"[{self.P.name}] reset \u2014 all data wiped.")

    def _rename_profile(self):
        self._logdbg(f"[PROFILE] _rename_profile: current name='{self.P.name}'")
        top = tk.Toplevel(self.root)
        top.title("Rename Profile"); top.resizable(False, False)
        top.configure(bg=BG)
        tk.Label(top, text="New name:", font=FB, bg=BG, fg=FG1).pack(padx=20,pady=(12,4))
        v = tk.StringVar(value=self.P.name)
        e = ttk.Entry(top, textvariable=v, width=24)
        e.pack(padx=20, pady=4); e.focus()
        def ok():
            n = v.get().strip()
            if n: self.P.name = n
            self._logdbg(f"[PROFILE] _rename_profile: renamed to '{self.P.name}'")
            self._refresh_prof_combo()
            self._refresh_home()
            save_profiles(self.profiles, self._prof_idx)
            top.destroy()
        tk.Button(top, text="Rename", font=FB, bg=ACCENT, fg="white",
                  relief="flat", command=ok).pack(pady=(4,12))
        top.bind("<Return>", lambda _: ok())

    def _save_config_to_profile(self):
        p = self.P
        try:
            p.uid      = self.uid_var.get().strip()
            p.host     = self._clean_host(self.host_var.get())
            p.sni      = self._clean_host(self.sni_var.get())
            p.path     = self._clean_path(self.path_var.get())
            p.cfg_name = self.name_var.get().strip() or "Edge-Optimized"
            p.network  = self.net_var.get()
            p.security = self.sec_var.get()
            p.fp       = self.fp_var.get()
            p.alpn     = self.alpn_var.get().strip()
            p.allow_insecure = self.insecure_var.get()
            p.grpc_service   = self.grpc_var.get().strip()
            self._logdbg(f"[PROFILE] _save_config_to_profile: uid={p.uid[:8]}..., host={p.host}, name={p.cfg_name}, has_config={p.has_config}")
        except Exception as e:
            self._logdbg(f"[PROFILE] _save_config_to_profile ERROR: {e}")
        # Also save scan settings from scan tab
        try:
            p.threads = int(self.threads_var.get())
            p.timeout = float(self.timeout_var.get())
        except Exception:
            pass

    def _load_profile_to_config(self):
        p = self.P
        self._loading_profile = True
        try:
            self.uid_var.set(p.uid)
            self.host_var.set(p.host)
            self.sni_var.set(p.sni)
            self.path_var.set(p.path or "/")
            self.name_var.set(p.cfg_name)
            self.net_var.set(p.network or "ws")
            self.sec_var.set(p.security or "tls")
            self.fp_var.set(p.fp or "chrome")
            self.alpn_var.set(p.alpn or "http/1.1")
            self.insecure_var.set(p.allow_insecure)
            self.grpc_var.set(p.grpc_service or "")
            # Always clear the import box when switching profiles
            try:
                self._import_var.set("")
                self._import_status_var.set("")
            except Exception:
                pass
        except Exception:
            pass
        finally:
            self._loading_profile = False
        # One clean authoritative save after all vars are stable
        self._save_config_to_profile()

    def _refresh_prof_bar(self):
        try: self._refresh_prof_combo()
        except Exception: pass

    def _update_tab_states(self):
        p = self.P
        has_results = bool(p.results)
        has_config  = p.has_config
        has_built   = bool(p.built_configs)

        self._tab_enabled["test"]       = has_results
        self._tab_enabled["connect"]    = has_results
        self._tab_enabled["connlog"]    = True

        for _, key, _, _ in self.TABS:
            lbl = self._nav.get(key)
            if lbl is None: continue
            en = self._tab_enabled.get(key, True)
            is_active = key == getattr(self, "_tab", "")
            lbl.config(fg=ACCENT if is_active else (FG3 if en else FG4))
            lbl._enabled = en
            ind = self._nav_indicators.get(key)
            if ind:
                ind.config(bg=ACCENT if is_active else BG_SIDEBAR)

    # ══════════════════════════════════════════════════════
    #  UI skeleton
    # ══════════════════════════════════════════════════════

    def _build_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()
        self._build_status_bar()

    def _sidebar_needed_height(self):
        """True natural pixel height of the sidebar column, summed from every
        child plus the vertical padding pack() adds around it. More reliable
        than winfo_reqheight() across DPI settings / emoji fonts because it
        never under-reports the pack padding."""
        sb = self._sidebar
        total = 0
        for c in sb.winfo_children():
            h = c.winfo_reqheight()
            pad = 0
            try:
                py = c.pack_info().get("pady", 0)
                if isinstance(py, (tuple, list)):
                    pad = sum(int(x) for x in py)
                else:
                    parts = str(py).split()
                    pad = sum(int(x) for x in parts) if parts else 0
            except Exception:
                pad = 0
            total += h + pad
        # the expanding spacer reports ~1px; ignore it and use the children sum
        return max(total, sb.winfo_reqheight())

    def _fit_height_to_sidebar(self, *_):
        """Size the window so the whole sidebar (all tabs) is always visible
        and the window ends just past the last tab. Measured at runtime so it
        adapts to the real emoji-font size and OS DPI scaling, with a small
        cushion so the bottom tab is never clipped on high-DPI displays.
        Called twice (early + late) and only ever GROWS the window, so a late
        measurement that picks up final font metrics can still expand it."""
        try:
            self.root.update_idletasks()
            sb_h = self._sidebar_needed_height()
            st_h = self._sb_frame.winfo_reqheight() or 26
            want = sb_h + st_h + 16           # cushion: never clip the last tab
            screen_h = self.root.winfo_screenheight()
            want = max(560, min(want, screen_h - 50))
            # keep the window from being dragged shorter than the sidebar
            self.root.minsize(900, want)
            cur_h = self.root.winfo_height()
            cur_w = self.root.winfo_width() or APP_W
            if cur_h < want:                  # only grow, never shrink
                self.root.geometry(f"{cur_w}x{want}")
        except Exception:
            pass

    def _toggle_theme(self):
        new = "light" if get_theme() == "dark" else "dark"
        set_theme(new)
        save_theme_pref(new)
        self._rebuild_ui()
        self._activity(f"Theme switched to {new} mode")

    def _rebuild_ui(self):
        # Widget colours are baked in at construction time, so switching
        # theme means tearing the whole UI down and rebuilding it. The active
        # config is saved first and restored by _build_content afterwards.
        cur_tab = getattr(self, "_tab", "home")
        try:
            self._save_config_to_profile()
        except Exception:
            pass
        try:
            setup_dark_styles(self._style)
        except Exception:
            pass
        # close the bandwidth dialog if open (its canvas is about to die)
        try:
            if getattr(self, "_bw_dialog", None) is not None:
                self._bw_dialog.destroy()
        except Exception:
            pass
        self._bw_chart = None
        self._bw_dialog = None
        for w in self.root.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass
        self.root.configure(bg=BG)
        self._build_ui()
        self._update_tab_states()
        if self._tab_enabled.get(cur_tab, True):
            self._show(cur_tab)
        self.root.after(120, self._fit_height_to_sidebar)
        self.root.after(800, self._fit_height_to_sidebar)

    def _build_sidebar(self):
        sb = tk.Frame(self.root, bg=BG_SIDEBAR, width=SIDEBAR_W)
        sb.grid(row=0, column=0, sticky="ns")
        sb.grid_propagate(False)
        self._sidebar = sb

        logo_frame = tk.Frame(sb, bg=BG_SIDEBAR)
        logo_frame.pack(fill=tk.X, pady=(16, 8))
        tk.Label(logo_frame, text="\u26a1", font=("Segoe UI Emoji", 20),
                 bg=BG_SIDEBAR, fg=ACCENT).pack()
        tk.Label(logo_frame, text="VEO", font=(FONT_FAMILY, 8, "bold"),
                 bg=BG_SIDEBAR, fg=FG3).pack()

        tk.Frame(sb, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=(4, 8))

        self._nav: Dict[str, tk.Label] = {}
        self._nav_indicators: Dict[str, tk.Frame] = {}

        for icon, key, name, tip in self.TABS:
            nav_row = tk.Frame(sb, bg=BG_SIDEBAR, cursor="hand2")
            nav_row.pack(fill=tk.X, pady=1)

            indicator = tk.Frame(nav_row, bg=BG_SIDEBAR, width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y)
            self._nav_indicators[key] = indicator

            l = tk.Label(nav_row, text=icon, font=FI_SMALL,
                         bg=BG_SIDEBAR, fg=FG3, cursor="hand2")
            l._enabled = True
            l.pack(fill=tk.X, padx=(0, 0), pady=4)
            self._nav[key] = l

            def on_click(_e, k=key):
                if not getattr(l, "_enabled", True): return
                self._show(k)

            nav_row.bind("<Button-1>", on_click)
            l.bind("<Button-1>", on_click)

            def on_enter(_e, row=nav_row, lbl=l, k=key):
                if not getattr(lbl, "_enabled", True): return
                if k != getattr(self, "_tab", ""):
                    row.config(bg=BG_HOVER)
                    lbl.config(bg=BG_HOVER, fg=FG1)

            def on_leave(_e, row=nav_row, lbl=l, k=key):
                is_active = k == getattr(self, "_tab", "")
                row.config(bg=BG_SIDEBAR if not is_active else BG_HOVER)
                lbl.config(bg=BG_SIDEBAR if not is_active else BG_HOVER,
                           fg=ACCENT if is_active else FG3)

            nav_row.bind("<Enter>", on_enter)
            nav_row.bind("<Leave>", on_leave)
            l.bind("<Enter>", on_enter)
            l.bind("<Leave>", on_leave)

            # Tooltip must be bound to the label (the widget the pointer
            # actually rests on). Binding it to nav_row caused the parent's
            # <Leave> to fire the instant the pointer entered the child label,
            # so the hint never appeared.
            _add_tooltip(l, f"{name}\n{tip}")

        tk.Frame(sb, bg=BG_SIDEBAR).pack(fill=tk.BOTH, expand=True)
        tk.Frame(sb, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=(8, 4))

    def _nav_rst(self, lbl):
        for k, b in self._nav.items():
            if b is lbl:
                en = self._tab_enabled.get(k, True)
                is_active = k == getattr(self, "_tab", "")
                b.config(fg=ACCENT if is_active else ("#888894" if en else FG4))

    def _build_content(self):
        self.root.configure(bg=BG)
        ca = tk.Frame(self.root, bg=BG)
        ca.grid(row=0, column=1, sticky="nsew")
        ca.columnconfigure(0, weight=1)
        ca.rowconfigure(1, weight=1)

        hdr = tk.Frame(ca, bg=BG_HEADER, height=40)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.columnconfigure(0, weight=1)

        hdr_inner = tk.Frame(hdr, bg=BG_HEADER)
        hdr_inner.grid(row=0, column=0, sticky="nsew", padx=16, pady=0)
        hdr_inner.columnconfigure(0, weight=1)

        self._hdr = tk.Label(hdr_inner, text="Home", font=FT,
                             bg=BG_HEADER, fg=FG1, anchor="w")
        self._hdr.grid(row=0, column=0, sticky="w", pady=6)

        self._hdr_profile = tk.Label(hdr_inner, text="", font=FS,
                                     bg=BG_HEADER, fg=FG3, anchor="e")
        self._hdr_profile.grid(row=0, column=1, sticky="e", pady=6)

        tk.Frame(ca, bg=BORDER, height=1).grid(row=0, column=0, sticky="sew")

        self._pages_frame = tk.Frame(ca, bg=BG)
        self._pages_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=4)
        self._pages_frame.columnconfigure(0, weight=1)
        self._pages_frame.rowconfigure(0, weight=1)

        self.pages: Dict[str, tk.Frame] = {}
        for _, key, _, _ in self.TABS:
            f = tk.Frame(self._pages_frame, bg=BG)
            f.grid(row=0, column=0, sticky="nsew")
            f.grid_remove()
            f.columnconfigure(0, weight=1)
            f.rowconfigure(0, weight=1)
            self.pages[key] = f

        self.uid_var      = tk.StringVar()
        self.host_var     = tk.StringVar()
        self.sni_var      = tk.StringVar()
        self.path_var     = tk.StringVar(value="/")
        self.name_var     = tk.StringVar(value="Edge-Optimized")
        self.net_var      = tk.StringVar(value="ws")
        self.sec_var      = tk.StringVar(value="tls")
        self.fp_var       = tk.StringVar(value="chrome")
        self.alpn_var     = tk.StringVar(value="http/1.1")
        self.insecure_var = tk.BooleanVar(value=False)
        self.grpc_var     = tk.StringVar(value="")
        self.optimized_var= tk.StringVar()

        self._build_home()
        self._build_config()
        self._build_scan()
        self._build_test()
        self._build_connect()
        self._build_connlog()
        self._build_favorites()
        self._build_wpool()
        self._build_wizard()
        self._build_settings()
        self._build_about()
        self._build_log()

        self._load_profile_to_config()
        self._show("home")

    def _build_status_bar(self):
        self._sb_frame = tk.Frame(self.root, bg=STATUS_BG, height=26)
        self._sb_frame.grid(row=1, column=0, columnspan=2, sticky="sew")
        self._sb_frame.grid_propagate(False)
        self._sb_frame.columnconfigure(1, weight=1)

        left = tk.Frame(self._sb_frame, bg=STATUS_BG)
        left.grid(row=0, column=0, sticky="w", padx=(12, 0))

        self._sb_dot = _status_dot(left, color=DISCONNECTED, size=7)
        self._sb_dot.pack(side=tk.LEFT, padx=(0, 6), pady=7)

        self._sb_status = tk.Label(
            left, text="Disconnected", font=F_STATUS,
            bg=STATUS_BG, fg=FG4, anchor="w")
        self._sb_status.pack(side=tk.LEFT, pady=7)

        self._sb_server = tk.Label(
            left, text="", font=F_STATUS,
            bg=STATUS_BG, fg=FG3, anchor="w")
        self._sb_server.pack(side=tk.LEFT, padx=(12, 0), pady=7)

        center = tk.Frame(self._sb_frame, bg=STATUS_BG)
        center.grid(row=0, column=1, sticky="")

        tk.Label(center, text="\u2191", font=F_STATUS_BOLD,
                 bg=STATUS_BG, fg=TEAL).pack(side=tk.LEFT, padx=(0, 2))
        self._sb_ul = tk.Label(
            center, text="\u2014", font=F_SPEED,
            bg=STATUS_BG, fg=TEAL, width=10, anchor="w")
        self._sb_ul.pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(center, text="\u2193", font=F_STATUS_BOLD,
                 bg=STATUS_BG, fg=GREEN).pack(side=tk.LEFT, padx=(0, 2))
        self._sb_dl = tk.Label(
            center, text="\u2014", font=F_SPEED,
            bg=STATUS_BG, fg=GREEN, width=10, anchor="w")
        self._sb_dl.pack(side=tk.LEFT, padx=(0, 12))

        tk.Frame(center, bg=BORDER, width=1).pack(
            side=tk.LEFT, fill=tk.Y, padx=8, pady=4)

        tk.Label(center, text="Ping", font=F_STATUS,
                 bg=STATUS_BG, fg=FG4).pack(side=tk.LEFT, padx=(0, 4))
        self._sb_lat = tk.Label(
            center, text="\u2014", font=F_SPEED,
            bg=STATUS_BG, fg=FG3, width=8, anchor="w")
        self._sb_lat.pack(side=tk.LEFT)

        right = tk.Frame(self._sb_frame, bg=STATUS_BG)
        right.grid(row=0, column=2, sticky="e", padx=(0, 12))

        self._sb_scan = tk.Label(
            right, text="", font=F_STATUS,
            bg=STATUS_BG, fg=FG4, anchor="e")
        self._sb_scan.pack(side=tk.LEFT, padx=(0, 12))

        # Dark / light theme toggle
        self._sb_theme = tk.Label(
            right, text=("\u2600" if get_theme() == "dark" else "\u263e"),
            font=F_STATUS_BOLD, bg=STATUS_BG, fg=FG3, cursor="hand2")
        self._sb_theme.pack(side=tk.LEFT, padx=(0, 12))
        self._sb_theme.bind("<Button-1>", lambda e: self._toggle_theme())
        _add_tooltip(self._sb_theme, "Toggle dark / light theme")

        tk.Label(right, text="v4.5", font=F_STATUS,
                 bg=STATUS_BG, fg=FG4, anchor="e").pack(side=tk.LEFT)

        tk.Frame(self.root, bg=BORDER, height=1).grid(
            row=1, column=0, columnspan=2, sticky="n")

    def _sb_update(self, status=None, color=None,
                   server=None, ul=None, dl=None,
                   lat=None, scan=None):
        # Stateful update: only the fields explicitly passed are changed.
        # This is critical because the bandwidth meter calls this every
        # second with ONLY ul/dl — previously the other params defaulted
        # and silently wiped the "Connected" status, server and colours.
        try:
            st = getattr(self, "_sb_state", None)
            if st is None:
                st = {"status": "Disconnected", "color": DISCONNECTED,
                      "server": "", "ul": "\u2014", "dl": "\u2014",
                      "lat": "\u2014", "scan": ""}
                self._sb_state = st
            if status is not None: st["status"] = status
            if color  is not None: st["color"]  = color
            if server is not None: st["server"] = server
            if ul     is not None: st["ul"]     = ul
            if dl     is not None: st["dl"]     = dl
            if lat    is not None: st["lat"]    = lat
            if scan   is not None: st["scan"]   = scan

            status_s = st["status"]
            if "Disconnected" in status_s:
                sb_bg = "#f8d7da"; text_color = "#721c24"
            elif "TUN" in status_s:
                sb_bg = "#d1ecf1"; text_color = "#0c5460"
            elif "Connected" in status_s:
                sb_bg = "#d4edda"; text_color = "#155724"
            else:
                sb_bg = STATUS_BG; text_color = FG4

            self._sb_status.config(text=status_s, fg=text_color)
            self._sb_dot.set_color(st["color"] if status_s != "Disconnected" else DISCONNECTED)
            self._sb_server.config(text=st["server"], fg=text_color)

            self._update_sb_bg(self._sb_frame, sb_bg)

            self._sb_ul.config(text=st["ul"], fg=TEAL if st["ul"] != "\u2014" else text_color)
            self._sb_dl.config(text=st["dl"], fg=GREEN if st["dl"] != "\u2014" else text_color)
            self._sb_lat.config(text=st["lat"], fg=text_color)
            self._sb_scan.config(text=st["scan"], fg=text_color)
        except Exception:
            pass

    def _update_sb_bg(self, widget, bg):
        try:
            widget.config(bg=bg)
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") not in (BORDER,):
                    self._update_sb_bg(child, bg)
        except Exception:
            pass

    def _show(self, name: str):
        if not self._tab_enabled.get(name, True):
            return
        self._tab = name
        for k, f in self.pages.items():
            f.grid() if k == name else f.grid_remove()
        for _, k, tip, _ in self.TABS:
            if k == name:
                self._hdr.config(text=tip)
                break

        for k, lbl in self._nav.items():
            en = self._tab_enabled.get(k, True)
            is_active = k == name
            lbl.config(fg=ACCENT if is_active else (FG3 if en else FG4))
            ind = self._nav_indicators.get(k)
            if ind:
                ind.config(bg=ACCENT if is_active else BG_SIDEBAR)
            try:
                if is_active:
                    lbl.master.config(bg=NAV_ACTIVE_BG)
                    lbl.config(bg=NAV_ACTIVE_BG)
                else:
                    lbl.master.config(bg=BG_SIDEBAR)
                    lbl.config(bg=BG_SIDEBAR)
            except Exception:
                pass
        try:
            self._activity(f"Opened tab: {name}")
        except Exception:
            pass

    def _build_home(self):
        hf = self.pages["home"]
        # Every page frame is created with rowconfigure(0, weight=1) as a
        # default (for single-child tabs). Home uses a multi-row layout where
        # only the scrollable list (row 2) should stretch — so explicitly
        # un-weight rows 0/1, otherwise the profile card's row absorbs the
        # leftover vertical space and leaves a big gap above the stat boxes.
        hf.rowconfigure(0, weight=0)   # profile card
        hf.rowconfigure(1, weight=0)   # stat boxes
        hf.rowconfigure(2, weight=0)   # top-5 toolbar
        hf.rowconfigure(3, weight=1)   # scrollable config list stretches

        pc = _card(hf)
        pc.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        pc.columnconfigure(1, weight=1)

        tk.Label(pc, text="Profile:", font=FB, bg=BG_CARD, fg=FG2,
                 padx=8, pady=4).grid(row=0, column=0, sticky="w")

        self._prof_combo_var = tk.StringVar()
        self._prof_combo = ttk.Combobox(pc, textvariable=self._prof_combo_var,
                                         state="readonly", width=22)
        self._prof_combo.grid(row=0, column=1, sticky="w", padx=(0, 8), pady=4)
        self._prof_combo.bind("<<ComboboxSelected>>", self._on_prof_combo)

        bf = tk.Frame(pc, bg=BG_CARD)
        bf.grid(row=0, column=2, padx=(0,8), pady=4)
        _abtn(bf, "Load",     self._load_profile_with_data, small=True, color=BLUE).pack(side=tk.LEFT, padx=2)
        _abtn(bf, "+ New",    self._new_profile,    small=True, color=TEAL).pack(side=tk.LEFT, padx=2)
        _abtn(bf, "Rename",   self._rename_profile, small=True, color=FG3).pack(side=tk.LEFT, padx=2)
        _abtn(bf, "Reset",    self._reset_profile,  small=True, color=ORANGE).pack(side=tk.LEFT, padx=2)
        _abtn(bf, "Delete",   self._delete_profile,  small=True, color=RED_C).pack(side=tk.LEFT, padx=2)

        self._prof_active_lbl = tk.Label(pc, text="", font=FS, bg=CARD, fg=FG2)
        self._prof_active_lbl.grid(row=1, column=0, columnspan=3, padx=8, pady=(0,2), sticky="w")

        self._refresh_prof_combo()

        self._home_stat = _card(hf)
        self._home_stat.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        self._home_stat.columnconfigure(0, weight=1)

        # Toolbar for the Home top-5 configs. Sits directly under the stat
        # labels and acts on the 5 currently-displayed configs, recomputed
        # live at click-time so it always reflects the latest scan.
        self._home_toolbar = _card(hf)
        self._home_toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        self._build_home_toolbar(self._home_toolbar)

        self._home_sf = SF(hf, bg=BG)
        self._home_sf.grid(row=3, column=0, sticky="nsew")

        self._refresh_home()

    def _build_home_toolbar(self, bar):
        for w in bar.winfo_children():
            w.destroy()
        row = tk.Frame(bar, bg=BG_CARD)
        row.pack(fill=tk.X, padx=8, pady=6)
        tk.Label(row, text="Top 5:", font=FH, bg=BG_CARD, fg=FG2).pack(
            side=tk.LEFT, padx=(0, 8))
        _abtn(row, "Sub Link",   self._home_copy_sub_link, small=True, color=BLUE
              ).pack(side=tk.LEFT, padx=2)
        _abtn(row, "Sub \u2192 File", self._home_save_sub_file, small=True, color=TEAL
              ).pack(side=tk.LEFT, padx=2)
        _abtn(row, "Save TXT",   self._home_save_txt, small=True, color=FG3
              ).pack(side=tk.LEFT, padx=2)
        tk.Label(row, text="Sort:", font=FB, bg=BG_CARD, fg=FG2).pack(
            side=tk.LEFT, padx=(12, 4))
        if not hasattr(self, "_home_sort_var"):
            self._home_sort_var = tk.StringVar(value="Quality")
        cb = ttk.Combobox(row, textvariable=self._home_sort_var, state="readonly",
                          width=9, values=["Quality", "Ping", "DL", "Jitter", "Loss"])
        cb.pack(side=tk.LEFT, padx=2)
        cb.bind("<<ComboboxSelected>>", lambda _e: self._refresh_home())

    def _refresh_prof_combo(self):
        names = [p.name for p in self.profiles]
        self._prof_combo.configure(values=names)
        if self.profiles:
            self._prof_combo.current(self._prof_idx)
        active = self.P
        has = "\u2714 Config set" if active.has_config else "\u26a0 No config (fill Config tab)"
        self._prof_active_lbl.config(
            text=f"Active: {active.name}  \u00b7  {has}  \u00b7  "
                 f"{len([r for r in active.results if r.ping_ms])} results"
        )

    def _on_prof_combo(self, _e=None):
        idx = self._prof_combo.current()
        self._logdbg(f"[PROFILE] _on_prof_combo: selected={idx}, current={self._prof_idx}")
        if idx >= 0 and idx != self._prof_idx:
            self._save_config_to_profile()
            save_profiles(self.profiles, self._prof_idx)
            old_name = self.P.name
            self._prof_idx = idx
            self._logdbg(f"[PROFILE] _on_prof_combo: switched from '{old_name}' to '{self.P.name}'")
            self._load_profile_to_config()
            self._refresh_prof_combo()
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_test_tree()
            self._refresh_connect_combo()
            self._update_tab_states()
            # Same bug class as _reset_profile already guards against:
            # these three were only refreshed on reset, not on switch —
            # so switching profiles showed the OLD profile's CF Worker
            # pool / history / favorites until something else happened
            # to trigger a redraw.
            try: self._cfw_refresh_tree()
            except Exception: pass
            try: self._refresh_history_combo()
            except Exception: pass
            try: self._refresh_favorites()
            except Exception: pass

    def _load_profile_with_data(self):
        self._logdbg(f"[PROFILE] _load_profile_with_data: idx={self._prof_idx}")
        profiles_full, _ = load_profiles_with_data()
        idx = self._prof_idx
        if idx < len(profiles_full):
            saved = profiles_full[idx]
            self._logdbg(f"[PROFILE] _load_profile_with_data: loading {len(saved.results)} results for '{saved.name}'")
            self.P.results       = saved.results
            self.P.scanned       = saved.scanned
            self.P.scan_time     = saved.scan_time
            self.P.built_configs = saved.built_configs
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_test_tree()
            self._refresh_connect_combo()
            self._update_tab_states()
            self._refresh_prof_combo()
            messagebox.showinfo("Profile Loaded",
                f"Loaded {len(self.P.results)} results from '{self.P.name}'.",
                parent=self.root)
        else:
            self._logdbg(f"[PROFILE] _load_profile_with_data: idx {idx} out of range ({len(profiles_full)} profiles)")

    def _delete_profile(self):
        self._logdbg(f"[PROFILE] _delete_profile: idx={self._prof_idx}, name='{self.P.name}', count={len(self.profiles)}")
        if len(self.profiles) <= 1:
            messagebox.showwarning("Cannot Delete",
                "Must keep at least one profile.", parent=self.root); return
        if not messagebox.askyesno("Delete Profile",
                f"Delete '{self.P.name}' permanently?", parent=self.root): return
        self.profiles.pop(self._prof_idx)
        self._prof_idx = max(0, self._prof_idx - 1)
        save_profiles(self.profiles, self._prof_idx)
        self._logdbg(f"[PROFILE] _delete_profile: deleted, new idx={self._prof_idx}, remaining={len(self.profiles)}")
        self._load_profile_to_config()
        self._refresh_prof_combo()
        self._refresh_home()
        self._refresh_scanresult()
        self._refresh_test_tree()
        self._refresh_connect_combo()
        self._update_tab_states()

    def _stat_box(self, parent, title, value, color, col):
        _metric_box(parent, title, value, color, col)

    def _refresh_home(self):
        inner = self._home_sf.inner
        for w in inner.winfo_children():
            w.destroy()
        p   = self.P
        ok  = self._home_sorted(p.results)
        verified = getattr(p, "passed_count", len(ok))
        pool_n    = len(p.built_configs) if p.built_configs else 0
        best_ping = min((r.ping_ms for r in ok), default=None)
        best_dl   = max((r.dl_mbps for r in ok if r.dl_mbps), default=None)
        tested    = sum(1 for r in ok if r.tested)
        # "Verified" box removed — the Pool / Configs box already reports the
        # verified (pool) count, so a separate Verified box was redundant.
        self._stat_box(self._home_stat, "Scanned",  str(p.scanned),        BLUE,   0)
        self._stat_box(self._home_stat, "Pool / Configs",
                       f"{verified} pool · {pool_n} built", TEAL, 1)
        self._stat_box(self._home_stat, "Best Ping",_ping_label(best_ping), _ping_color(best_ping), 2)
        self._stat_box(self._home_stat, "Best DL",
                       f"{best_dl:.1f}M" if best_dl else "\u2014", _speed_color(best_dl), 3)
        self._stat_box(self._home_stat, "Tested",   str(tested),            ORANGE, 4)

        try:
            has = "Connected" if p.has_config else "No Config"
            color = GREEN if p.has_config else ORANGE
            self._hdr_profile.config(text=f"{p.name}  \u00b7  {has}", fg=color)
        except Exception:
            pass

        if p.scan_time:
            tk.Label(self._home_stat, text=f"Last scan: {p.scan_time}  \u00b7  {p.range_name}",
                     font=FS, bg=BG_CARD, fg=FG4).grid(
                row=1, column=0, columnspan=5, pady=(0, 2), padx=8, sticky="w")
        try: self._refresh_prof_combo()
        except Exception: pass

        if not ok:
            empty_frame = tk.Frame(inner, bg=BG)
            empty_frame.pack(fill=tk.X, pady=60)
            tk.Label(empty_frame, text="\U0001f4e1", font=("Segoe UI Emoji", 36),
                     bg=BG, fg=FG4).pack()
            tk.Label(empty_frame, text="No results yet",
                     font=FH, bg=BG, fg=FG3).pack(pady=(8, 4))
            tk.Label(empty_frame, text="Run a scan on the Scan tab to discover endpoints",
                     font=FB, bg=BG, fg=FG4).pack()
            return

        if not p.has_config:
            warn = tk.Frame(inner, bg="#2d1f0e", highlightthickness=1,
                           highlightbackground="#f59e0b")
            warn.pack(fill=tk.X, pady=(0, 12), padx=2)
            tk.Label(warn, text="\u26a0  Config not set \u2014 fill UUID + Host in Config tab",
                     font=FB, bg="#2d1f0e", fg=ORANGE, anchor="w",
                     padx=12, pady=8).pack(fill=tk.X)
            for i, r in enumerate(ok[:5], 1):
                self._home_ip_card(inner, r, i)
        else:
            tk.Label(inner, text=f"5 Best Configs  ({p.cfg_name})",
                     font=FH, bg=BG, fg=FG2).pack(anchor="w", pady=(4,6))
            for i, r in enumerate(ok[:5], 1):
                self._home_cfg_card(inner, r, i)

    def _best_sorted(self, results):
        """Return reachable results sorted by overall config quality:
        lowest packet-loss, then ping, then proxy latency, then jitter.
        Used for the Home tab '5 best' list and anywhere a quality-ranked
        view of the pool is needed."""
        ok = [r for r in results if r.ping_ms is not None]
        def _score(r):
            return (
                (r.loss_pct   if r.loss_pct   is not None else 0.0),
                (r.ping_ms    if r.ping_ms    is not None else 1e9),
                (r.lat_ms     if r.lat_ms     is not None else 1e9),
                (r.jitter_ms  if r.jitter_ms  is not None else 1e9),
            )
        return sorted(ok, key=_score)

    def _home_sorted(self, results):
        """Sort reachable results by the metric chosen in the Home toolbar.
        Recomputed on every Home refresh / toolbar action so it always
        reflects the latest scan data \u2014 nothing is cached."""
        ok = [r for r in results if r.ping_ms is not None]
        key = self._home_sort_var.get() if hasattr(self, "_home_sort_var") else "Quality"
        if key == "Ping":
            return sorted(ok, key=lambda r: r.ping_ms if r.ping_ms is not None else 1e9)
        if key == "DL":
            return sorted(ok, key=lambda r: -(r.dl_mbps or 0.0))
        if key == "Jitter":
            return sorted(ok, key=lambda r: r.jitter_ms if r.jitter_ms is not None else 1e9)
        if key == "Loss":
            return sorted(ok, key=lambda r: r.loss_pct if r.loss_pct is not None else 1e9)
        return self._best_sorted(results)   # "Quality" (default)

    def _home_top_configs(self):
        """The Home top-5 as (ProbeResult, vless_url) pairs, recomputed live
        from the current results at call-time so the toolbar actions always
        operate on the latest scan, never a cached snapshot."""
        top = self._home_sorted(self.P.results)[:5]
        return [(r, self._vless(r.ip, r.port)) for r in top]

    def _home_sub_b64(self):
        """Base64 subscription blob built from just the Home top-5 vless URLs.
        Returns (b64_text, count)."""
        import base64 as _b64s
        top = self._home_top_configs()
        if not top:
            return "", 0
        urls = [u for _, u in top]
        blob = "\n".join(urls).encode("utf-8")
        return _b64s.b64encode(blob).decode("ascii"), len(urls)

    def _home_copy_sub_link(self):
        b64, n = self._home_sub_b64()
        if not b64:
            messagebox.showinfo("No Configs",
                "No scanned configs yet \u2014 run a scan on the Scan tab first.",
                parent=self.root)
            return
        link = self._host_subscription(b64)
        if link:
            sub_name = (self.P.cfg_name or self.P.name or "VLESS-Top5").strip()
            link = f"{link}#{urllib.parse.quote(sub_name, safe='')}"
            self._logui(f"[HOME] \u2714 Top-{n} subscription link ready: {link}")
            show_qr(self.root, link, title=f"Home Top-{n} Subscription")
        else:
            self._copy_with_toast(b64, f"Home Top-{n} subscription (raw)")
            self._logui("[HOME] \u26a0 Could not host a link \u2014 "
                        "copied raw base64 content instead (not a URL).")

    def _home_save_sub_file(self):
        b64, n = self._home_sub_b64()
        if not b64:
            messagebox.showinfo("No Configs",
                "No scanned configs yet \u2014 run a scan on the Scan tab first.",
                parent=self.root)
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{self.P.name}_home_top{n}_sub.txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(b64)
            self._logui(f"[HOME] \u2714 Saved top-{n} subscription \u2192 {path}")
        except Exception as e:
            self._logui(f"[HOME] Save error: {e}")

    def _home_save_txt(self):
        top = self._home_top_configs()
        if not top:
            messagebox.showinfo("No Configs",
                "No scanned configs yet \u2014 run a scan on the Scan tab first.",
                parent=self.root)
            return
        urls = [u for _, u in top]
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{self.P.name}_home_top{len(urls)}.txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(urls))
            self._logui(f"[HOME] \u2714 Saved {len(urls)} configs as plain text \u2192 {path}")
        except Exception as e:
            self._logui(f"[HOME] Save error: {e}")

    def _home_ip_card(self, parent, r, idx):
        c = _card(parent)
        c.pack(fill=tk.X, pady=(0,4))
        c.columnconfigure(1, weight=1)
        tk.Label(c, text=f"#{idx}", font=FB, bg=BG_CARD, fg=FG3,
                 width=4, anchor="w").grid(row=0, column=0, padx=(12,4), pady=6)
        tk.Label(c, text=f"{r.ip}:{r.port}", font=(MONO_FAMILY, 10, "bold"),
                 bg=BG_CARD, fg=FG1).grid(row=0, column=1, sticky="w", pady=6)
        tk.Label(c, text=_ping_label(r.ping_ms), font=F_SPEED,
                 bg=BG_CARD, fg=_ping_color(r.ping_ms)).grid(row=0, column=2, padx=12, pady=6)

    def _home_cfg_card(self, parent, r, idx):
        p = self.P
        ping = r.ping_ms
        if ping is not None and ping < 150:
            card_bg = CARD_BG_2
        elif ping is not None and ping < 400:
            card_bg = CARD_BG_3
        else:
            card_bg = CARD_BG_4
        card = _card(parent, bg=card_bg)
        card.pack(fill=tk.X, pady=3, padx=2)
        tk.Frame(card, bg=_ping_color(r.ping_ms), width=5).pack(side=tk.LEFT, fill=tk.Y)
        bf = tk.Frame(card, bg=card_bg)
        bf.pack(side=tk.RIGHT, padx=6, pady=4)
        url  = self._vless(r.ip, r.port)
        name = f"{p.cfg_name} {r.ip}:{r.port}"
        con = _ilbl(bf,"\U0001f310", lambda rr=r: self._load_connect(rr))
        con.pack(side=tk.LEFT, padx=2)
        _add_tooltip(con, "Connect")
        lnk = _ilbl(bf,"\U0001f517", lambda u=url,n=name: self._copy_with_toast(u,n))
        lnk.pack(side=tk.LEFT, padx=2)
        _add_tooltip(lnk, "Copy config link")
        qrl = _ilbl(bf,"\U0001f4f7", lambda u=url,n=name: show_qr(self.root,u,n))
        qrl.pack(side=tk.LEFT, padx=2)
        _add_tooltip(qrl, "Show QR code")
        edit_lbl = _ilbl(bf,"\u270f", lambda rr=r, n=name: self._edit_config_dialog(rr, n))
        edit_lbl.pack(side=tk.LEFT, padx=2)
        _add_tooltip(edit_lbl, "Edit config")
        star = _ilbl(bf,"\u2b50", lambda u=url,n=name: self._add_favorite(u,n))
        star.pack(side=tk.LEFT, padx=2)
        _add_tooltip(star, "Add to Favorites")
        test_lbl = _ilbl(bf,"\u26a1", lambda rr=r: self._test_single_config(rr))
        test_lbl.pack(side=tk.LEFT, padx=2)
        _add_tooltip(test_lbl, "Test this config")
        dell = _ilbl(bf,"\U0001f5d1", lambda rr=r: self._delete_result_confirm(rr))
        dell.pack(side=tk.LEFT, padx=2)
        _add_tooltip(dell, "Delete result")
        inner = tk.Frame(card, bg=card_bg)
        inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=6)
        cfg_label = f"#{idx}  {p.cfg_name} \u2014 {r.ip}:{r.port}"
        tk.Label(inner, text=cfg_label, font=FH, bg=card_bg, fg=FG1,
                 wraplength=320, anchor="w", justify="left").pack(anchor="w")
        row2 = tk.Frame(inner, bg=card_bg)
        row2.pack(anchor="w")
        for lbl,val,col in [
            ("Ping",   _ping_label(r.ping_ms),  _ping_color(r.ping_ms)),
            ("Jitter", (f"{r.jitter_ms:.0f}ms" if r.jitter_ms is not None else "\u2014"),
                        _ping_color(r.jitter_ms)),
            ("Loss",   (f"{r.loss_pct:.0f}%" if r.loss_pct is not None else "\u2014"),
                        GREEN if (r.loss_pct or 0)<5 else (ORANGE if (r.loss_pct or 0)<25 else RED_C)),
            ("Colo",   r.colo or "\u2014", TEAL if r.cf_valid else FG3),
            ("DL",     f"{r.dl_mbps:.1f}M" if r.dl_mbps else "\u2014",
                        GREEN if (r.dl_mbps or 0)>=5 else (ORANGE if (r.dl_mbps or 0)>=1 else RED_C)),
            ("UP",     f"{r.up_mbps:.1f}M" if r.up_mbps else "\u2014",
                        GREEN if (r.up_mbps or 0)>=5 else (ORANGE if (r.up_mbps or 0)>=1 else RED_C)),
        ]:
            tk.Label(row2, text=f" {lbl}:", font=FS, bg=card_bg, fg=FG1).pack(side=tk.LEFT)
            tk.Label(row2, text=f" {val} ", font=("Segoe UI",9,"bold"), bg=card_bg,
                     fg=col).pack(side=tk.LEFT)

    def _test_single_config(self, r):
        if not self.P.has_config:
            messagebox.showwarning("No Config", "Fill UUID + Host in Config tab first.", parent=self.root)
            return
        if not self.xray.is_installed():
            messagebox.showwarning("xray-core Not Found",
                "xray-core is required for full test.\n\n"
                "Use Settings \u2192 Xray Core \u2192 Download.",
                parent=self.root)
            return
        self.q.put(("log", f"[SINGLE TEST] Testing {r.ip}:{r.port}\u2026"))
        self.q.put(("status", f"Testing {r.ip}:{r.port}\u2026"))
        threading.Thread(target=self._test_single_config_thr, args=(r,), daemon=True).start()

    def _test_single_config_thr(self, r):
        p = self.P
        uid    = p.uid
        host   = p.host or ""
        sni    = p.sni  or host
        path   = p.path or "/"
        lp     = XrayManager.get_free_port()
        cfg    = XrayManager.build_test(r.ip, r.port, uid, host, sni, path, lp, p)
        fd, cp = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f: json.dump(cfg, f)
        proc = None
        try:
            kw: dict = {}
            if sys.platform == "win32":
                kw["creationflags"] = subprocess.CREATE_NO_WINDOW
            proc = subprocess.Popen(
                [self.xray.xray_path, "-c", cp],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, **kw)
            time.sleep(1.5)
            if proc.poll() is None:
                proxy = f"http://127.0.0.1:{lp}"
                r.lat_ms, _ = XrayManager.latency(proxy)
                if r.lat_ms is not None:
                    r.dl_mbps, _ = XrayManager.dl_speed(proxy)
                    r.up_mbps, _ = XrayManager.up_speed(proxy)
                r.tested = True
                r.error  = None
            else:
                r.tested = True
                r.error  = "xray failed"
        except Exception as ex:
            r.tested = True
            r.error  = str(ex)
        finally:
            if proc:
                try: proc.terminate(); proc.wait(timeout=3)
                except Exception:
                    try: proc.kill()
                    except Exception: pass
            try: os.remove(cp)
            except Exception: pass
        save_profiles(self.profiles, self._prof_idx)
        self.q.put(("log", f"[SINGLE TEST] {r.ip}:{r.port} \u2014 "
                     f"ping={_ping_label(r.ping_ms)}  DL={r.dl_mbps or 0:.1f}M  "
                     f"UP={r.up_mbps or 0:.1f}M  lat={_ping_label(r.lat_ms)}"))
        self.root.after(0, self._refresh_home)
        self.root.after(0, self._refresh_scanresult)
        self.root.after(0, self._refresh_test_tree)

    def _connect_config(self, r, name):
        messagebox.showinfo("Connect",
            f"Pre-selected: {r.ip}:{r.port}\n\n"
            "Switch to Connect tab and press \u25b6 Connect.",
            parent=self.root)
        self._pref_connect = r
        self._refresh_connect_combo()
        self._show("connect")

    def _delete_result_confirm(self, r):
        if messagebox.askyesno("Delete Result",
                f"Remove {r.ip}:{r.port} from results?", parent=self.root):
            self.P.results = [x for x in self.P.results
                              if not (x.ip==r.ip and x.port==r.port)]
            save_profiles(self.profiles, self._prof_idx)
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_test_tree()
            self._refresh_connect_combo()
            self._update_tab_states()

    def _build_config(self):
        cf = self.pages["config"]
        cf.rowconfigure(0, weight=1)

        outer = SF(cf, bg=BG)
        outer.grid(row=0, column=0, sticky="nsew")
        inner = outer.inner

        def section(parent, title):
            f = tk.Frame(parent, bg=BG)
            f.pack(fill=tk.X, pady=(10,2))
            tk.Label(f, text=title, font=FH, bg=BG, fg=FG2).pack(anchor="w", padx=2)
            c = _card(parent)
            c.pack(fill=tk.X, pady=(0,6))
            c.columnconfigure(1, weight=1)
            return c

        def row(card, lbl, widget, r, hint=""):
            tk.Label(card, text=lbl, font=FB, bg=BG_CARD, fg=FG2,
                     width=22, anchor="w").grid(row=r, column=0, padx=(12,4), pady=5, sticky="w")
            widget.grid(row=r, column=1, sticky="ew", padx=(0,12), pady=5)
            if hint:
                tk.Label(card, text=hint, font=FB, bg=BG_CARD, fg=BLUE,
                         anchor="w").grid(row=r, column=2, padx=(0,12), pady=5, sticky="w")

        imp_hdr = tk.Frame(inner, bg=BG)
        imp_hdr.pack(fill=tk.X, pady=(10,2))
        tk.Label(imp_hdr, text="\U0001f4e5  Quick Import", font=FH, bg=BG, fg=FG2).pack(side=tk.LEFT)
        tk.Label(imp_hdr, text="  \u2014 paste a VLESS URL to auto-fill all fields",
                 font=FS, bg=BG, fg=FG4).pack(side=tk.LEFT)

        imp_card = _card(inner)
        imp_card.pack(fill=tk.X, pady=(0,8))
        imp_card.columnconfigure(0, weight=1)

        self._import_var = tk.StringVar()
        self._import_entry = ttk.Entry(imp_card, textvariable=self._import_var, font=FS)
        self._import_entry.grid(row=0, column=0, sticky="ew", padx=(12,6), pady=10)
        self._import_entry.insert(0, "vless://…")
        self._import_entry.bind("<FocusIn>",
            lambda e: (self._import_entry.delete(0, tk.END)
                       if self._import_var.get() in ("", "vless://…") else None))
        self._import_entry.bind("<FocusOut>",
            lambda e: (self._import_entry.insert(0, "vless://…")
                       if not self._import_var.get().strip() else None))
        self._import_entry.bind("<Return>", lambda e: self._do_import_config())

        _add_tooltip(
            _abtn(imp_card, "\U0001f4cb Paste & Fill", self._do_paste_and_fill, color=TEAL),
            "Paste the VLESS URL from clipboard and fill all fields below"
        ).grid(row=0, column=1, padx=(0,4), pady=10)

        _add_tooltip(
            _abtn(imp_card, "\U0001f5d1 Clear All", self._clear_config_tab, small=True, color=RED_C),
            "Wipe the entire Config tab and start fresh"
        ).grid(row=0, column=2, padx=(0,12), pady=10)

        self._import_status_var = tk.StringVar()
        tk.Label(imp_card, textvariable=self._import_status_var,
                 font=FS, bg=BG_CARD, fg=GREEN, anchor="w").grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=12, pady=(0,6))

        c = section(inner, "Identity")
        row(c, "Config Name",     ttk.Entry(c, textvariable=self.name_var),  0)
        row(c, "UUID / UID *",    ttk.Entry(c, textvariable=self.uid_var),   1, "required")
        row(c, "Host (CDN) *",    ttk.Entry(c, textvariable=self.host_var),  2, "required \u2014 CDN edge / Host header")
        row(c, "SNI (TLS name)",  ttk.Entry(c, textvariable=self.sni_var),   3, "defaults to Host if empty")
        row(c, "Path",            ttk.Entry(c, textvariable=self.path_var),  4, "WebSocket / HTTP path")

        c2 = section(inner, "Transport & Protocol")
        net_cb = ttk.Combobox(c2, textvariable=self.net_var, width=14,
                              values=["ws","grpc","h2","tcp"], state="readonly")
        row(c2, "Network",        net_cb,                                    0, "ws = WebSocket (recommended)")
        sec_cb = ttk.Combobox(c2, textvariable=self.sec_var, width=14,
                              values=["tls","reality","none"], state="readonly")
        row(c2, "Security",       sec_cb,                                    1, "tls / reality / none")
        fp_cb  = ttk.Combobox(c2, textvariable=self.fp_var, width=14,
                              values=["chrome","firefox","safari","edge","ios","android","random",""],
                              state="readonly")
        row(c2, "TLS Fingerprint",fp_cb,                                     2, "Browser TLS fingerprint (uTLS)")
        row(c2, "ALPN",           ttk.Entry(c2, textvariable=self.alpn_var), 3, "e.g. http/1.1  or  h2,http/1.1")
        row(c2, "gRPC Service",   ttk.Entry(c2, textvariable=self.grpc_var), 4, "only used when Network = grpc")

        c3 = section(inner, "Security Options")
        tk.Label(c3, text="Allow Insecure TLS", font=FB, bg=BG_CARD, fg=FG2,
                 width=22, anchor="w").grid(row=0, column=0, padx=(12,4), pady=5, sticky="w")
        ttk.Checkbutton(c3, variable=self.insecure_var,
                        text="\u26a0  Not recommended for production").grid(
            row=0, column=1, sticky="w", padx=(0,12), pady=5)

        bf = tk.Frame(inner, bg=BG)
        bf.pack(anchor="w", pady=(8,4))
        _abtn(bf, "\U0001f4be Save Profile", self._on_config_save, color=TEAL).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf, "\U0001f50d Test Health", self._test_config_health, color=BLUE).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf, "\U0001f9d9 Worker Wizard", lambda: self._show("wizard"), color="#F6821F").pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf, "\U0001f4e6 Worker Pool", lambda: self._show("wpool"), color="#7c3aed").pack(side=tk.LEFT, padx=(0,8))

        self._health_status_lbl = tk.Label(inner, text="",
                 font=FS, bg=BG, fg=FG3, anchor="w")
        self._health_status_lbl.pack(anchor="w", padx=2)

        tk.Label(inner, text="\u2605  Fields marked * are required for config-based mode.",
                 font=FS, bg=BG, fg=ORANGE).pack(anchor="w")

        for var in (self.uid_var, self.host_var, self.sni_var, self.path_var,
                    self.name_var, self.net_var, self.sec_var, self.fp_var,
                    self.alpn_var, self.grpc_var):
            var.trace_add("write", lambda *_: self._on_config_change())
        self.insecure_var.trace_add("write", lambda *_: self._on_config_change())

    # ══════════════════════════════════════════════════════
    #  VLESS URL importer
    # ══════════════════════════════════════════════════════

    def _do_paste_and_fill(self):
        try:
            clip = self.root.clipboard_get()
        except Exception:
            clip = ""
        clip = (clip or "").strip()

        if not clip or not clip.lower().startswith("vless://"):
            self._import_status_var.set(
                "\u26a0  Clipboard doesn't contain a vless:// URL. Copy a config link first.")
            return

        # Show the pasted URL in the box
        try:
            self._import_entry.delete(0, tk.END)
            self._import_entry.insert(0, clip)
            self._import_var.set(clip)
        except Exception:
            self._import_var.set(clip)

        # Parse + fill using the existing logic
        self._do_import_config()

    def _clear_config_tab(self):
        if not messagebox.askyesno(
            "Clear Config",
            "This will erase ALL fields in the Config tab\n"
            "(UUID, Host, SNI, Path, Network, Security, etc.)\n"
            "and reset this profile to a blank template.\n\n"
            "Continue?",
            parent=self.root):
            return

        self._import_bulk = True
        try:
            # Reset every field to ConfigProfile defaults
            self.uid_var.set("")
            self.host_var.set("")
            self.sni_var.set("")
            self.path_var.set("/")
            self.name_var.set("Edge-Optimized")
            self.net_var.set("ws")
            self.sec_var.set("tls")
            self.fp_var.set("chrome")
            self.alpn_var.set("http/1.1")
            self.grpc_var.set("")
            self.insecure_var.set(False)

            # Clear the import box
            try:
                self._import_entry.delete(0, tk.END)
                self._import_entry.insert(0, "vless://\u2026")
            except Exception:
                pass
            self._import_var.set("")
            self._import_status_var.set("")
        finally:
            self._import_bulk = False

        # One clean save
        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        self._update_tab_states()
        self._refresh_home()
        self._logdbg("[config] Config tab cleared — fresh start.")
        self._import_status_var.set("\U0001f5d1  Config tab cleared. Ready for a new config.")

    def _do_import_config(self):
        self._activity("Imported config from vless:// URL")
        raw = self._import_var.get().strip()
        if not raw or raw in ("vless://…", ""):
            self._import_status_var.set("⚠  Paste a vless:// URL first.")
            return
        data = self._parse_vless_url(raw)
        if data is None:
            self._import_status_var.set(
                "✖  Not a valid VLESS URL. Must start with vless://")
            return

        # Suppress traces during bulk fill
        self._import_bulk = True
        try:
            def _s(var, val):
                if val: var.set(val)
            _s(self.uid_var,   data["uid"])
            _s(self.host_var,  data["host"])
            _s(self.sni_var,   data["sni"])
            _s(self.path_var,  data["path"])
            _s(self.net_var,   data["network"])
            _s(self.sec_var,   data["security"])
            _s(self.fp_var,    data["fp"])
            _s(self.alpn_var,  data["alpn"])
            _s(self.grpc_var,  data["grpc_service"])
            _s(self.name_var,  data["cfg_name"])
            self.insecure_var.set(data["allow_insecure"])
        finally:
            self._import_bulk = False

        # Single authoritative save after all vars are set
        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        self._update_tab_states()
        self._refresh_home()

        # NOTE: deliberately keep the pasted URL in the import box so the
        # user can see exactly what was imported.

        filled = [k for k, v in data.items()
                  if v and k not in ("allow_insecure", "_server", "_port")]
        self._import_status_var.set(
            f"✔  Imported — {len(filled)} fields filled"
            + (f"  →  host: {data['host']}" if data.get("host") else ""))
        self._logdbg(f"[import] VLESS parsed: {data}")

    @staticmethod
    def _parse_vless_url(url: str):
        url = url.strip()
        if not url.lower().startswith("vless://"):
            return None
        try:
            body = url[8:]

            # Fragment -> config name
            cfg_name = ""
            if "#" in body:
                body, frag = body.rsplit("#", 1)
                cfg_name = urllib.parse.unquote(frag).strip()

            # Query string
            query_str = ""
            if "?" in body:
                body, query_str = body.split("?", 1)

            # uuid@server:port
            uid = ""
            if "@" in body:
                uid_raw, addr = body.rsplit("@", 1)
                uid = urllib.parse.unquote(uid_raw).strip()
            else:
                addr = body

            # IPv6 [::1]:443
            if addr.startswith("["):
                end   = addr.index("]")
                server = addr[1:end]
                port_s = addr[end + 2:] if len(addr) > end + 2 else "443"
            elif ":" in addr:
                parts  = addr.rsplit(":", 1)
                server = parts[0]
                port_s = parts[1]
            else:
                server = addr
                port_s = "443"

            port = int(port_s) if port_s.isdigit() else 443

            params: dict = {}
            for item in query_str.split("&"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    params[k.lower()] = urllib.parse.unquote(v)

            def p(key, default=""):
                return params.get(key, default)

            network  = p("type",     "ws")
            security = p("security", "tls")
            cdn_host = p("host") or server
            sni      = p("sni") or p("peer") or cdn_host
            path     = p("path", "/")
            fp       = p("fp",   "chrome")
            alpn     = p("alpn", "http/1.1").replace("%2C", ",").replace("%2c", ",")
            grpc_svc = p("servicename") or p("service-name") or ""
            insecure = p("allowinsecure") or p("insecure") or "0"

            return {
                "uid":            uid,
                "host":           cdn_host,
                "sni":            sni,
                "path":           path or "/",
                "network":        network,
                "security":       security,
                "fp":             fp,
                "alpn":           alpn,
                "grpc_service":   grpc_svc,
                "allow_insecure": insecure.strip() in ("1", "true", "yes"),
                "cfg_name":       cfg_name or "Imported",
                "_server":        server,
                "_port":          port,
            }
        except Exception:
            return None

    def _on_config_change(self):
        # Suppress traces during bulk VLESS import or profile load
        if getattr(self, "_import_bulk", False) or getattr(self, "_loading_profile", False):
            return
        self._save_config_to_profile()
        self._update_tab_states()
        # keep scan-mode hint in sync with config security setting
        try: self._scan_mode_hint_updater()
        except Exception: pass
        # Debounced disk write — persists 600 ms after the last keystroke.
        # Guarantees the profile is on disk even if the app is force-killed.
        try:
            if getattr(self, "_cfg_save_id", None):
                self.root.after_cancel(self._cfg_save_id)
        except Exception:
            pass
        self._cfg_save_id = self.root.after(600, self._flush_config_to_disk)

    def _flush_config_to_disk(self):
        self._cfg_save_id = None
        save_profiles(self.profiles, self._prof_idx)
        self._logdbg("[auto-save] config flushed to disk.")

    def _on_config_save(self):
        self._activity("Config saved to profile")
        # Cancel any pending debounce and save immediately
        try:
            if getattr(self, "_cfg_save_id", None):
                self.root.after_cancel(self._cfg_save_id)
                self._cfg_save_id = None
        except Exception:
            pass
        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        self._update_tab_states()
        self._refresh_home()
        self._logdbg("Config saved to profile.")
        # Show save confirmation toast (no "copied" text)
        toast = tk.Toplevel(self.root)
        toast.wm_overrideredirect(True)
        x = self.root.winfo_rootx() + self.root.winfo_width()//2 - 150
        y = self.root.winfo_rooty() + self.root.winfo_height() - 80
        toast.wm_geometry(f"+{x}+{y}")
        toast.configure(bg=GREEN)
        tk.Label(toast, text=f"\u2714  Profile '{self.P.name}' saved!",
                 font=(FONT_FAMILY, 10, "bold"), bg=GREEN, fg="white",
                 padx=16, pady=8).pack()
        toast.after(2200, toast.destroy)

    def _test_config_health(self):
        self._save_config_to_profile()
        p = self.P
        if not p.uid.strip():
            self._health_status_lbl.config(text="\u2716  UUID is empty \u2014 fill it first", fg=RED_C)
            return
        if not p.host.strip():
            self._health_status_lbl.config(text="\u2716  Host is empty \u2014 fill it first", fg=RED_C)
            return
        self._health_status_lbl.config(text="\u23f3  Testing\u2026", fg=ORANGE)
        threading.Thread(target=self._test_config_health_thr, daemon=True).start()

    def _test_config_health_thr(self):
        import ssl as _ssl_mod
        p = self.P
        host = p.host
        sni  = p.sni or host
        path = p.path or "/"
        results = []
        all_ok = True

        def _emit(msg, ok=True):
            nonlocal all_ok
            results.append((msg, ok))
            if not ok: all_ok = False

        ip = host
        try:
            infos = socket.getaddrinfo(host, None, socket.AF_INET)
            if infos:
                ip = infos[0][4][0]
                _emit(f"DNS: {host} \u2192 {ip}", True)
            else:
                _emit(f"DNS: {host} \u2194 no results", False)
        except Exception as e:
            _emit(f"DNS: {host} \u2716 {e}", False)

        for port in (443, 8443, 2053):
            try:
                t0 = time.perf_counter()
                ctx = _ssl_mod.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = _ssl_mod.CERT_NONE
                sock = socket.create_connection((ip, port), timeout=4)
                sw = ctx.wrap_socket(sock, server_hostname=sni)
                ms = (time.perf_counter() - t0) * 1000
                sw.close()
                _emit(f"TLS {port}: {ms:.0f}ms \u2714 {sni}", True)
                break
            except Exception as e:
                _emit(f"TLS {port}: \u2716 {e}", False)

        try:
            t0 = time.perf_counter()
            ctx = _ssl_mod.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _ssl_mod.CERT_NONE
            sock = socket.create_connection((ip, 443), timeout=4)
            sw = ctx.wrap_socket(sock, server_hostname=sni)
            ws_key = _b64.b64encode(os.urandom(16)).decode()
            req_host = p.host or sni or ip
            sw.sendall((
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {req_host}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {ws_key}\r\n"
                "Sec-WebSocket-Version: 13\r\n"
                "\r\n").encode())
            resp = sw.recv(512)
            ms = (time.perf_counter() - t0) * 1000
            sw.close()
            if b"101" in resp:
                _emit(f"WS: {ms:.0f}ms \u2714 upgrade OK", True)
            else:
                line = resp.split(b"\r\n")[0].decode(errors="ignore")
                _emit(f"WS: {line}", False)
        except Exception as e:
            _emit(f"WS: \u2716 {e}", False)

        verdict = "\u2714  Config looks healthy" if all_ok else "\u26a0  Some checks failed"
        summary = "\n".join(f"  {m}" for m, _ in results)
        final = f"{verdict}\n{summary}"
        def _show():
            self._health_status_lbl.config(text=verdict, fg=GREEN if all_ok else ORANGE)
            messagebox.showinfo("Health Check", final, parent=self.root)
        self.root.after(0, _show)

    def _edit_config_dialog(self, r, name):
        top = tk.Toplevel(self.root)
        top.title(f"Edit {r.ip}:{r.port}")
        top.resizable(False, False)
        top.configure(bg=BG)
        top.grab_set()
        tk.Label(top, text="Display Name:", font=FB, bg=BG, fg=FG2).pack(padx=20, pady=(12, 4))
        v = tk.StringVar(value=name)
        e = ttk.Entry(top, textvariable=v, width=30)
        e.pack(padx=20, pady=4)
        e.focus()
        e.select_range(0, tk.END)

        def ok():
            new_name = v.get().strip()
            if new_name:
                r.cfg_name = new_name
                save_profiles(self.profiles, self._prof_idx)
                self._refresh_home()
                self._refresh_scanresult()
            top.destroy()

        bf = tk.Frame(top, bg=BG)
        bf.pack(pady=(4, 12))
        _abtn(bf, "Save", ok, small=True, color=TEAL).pack(side=tk.LEFT, padx=6)
        _gbtn(bf, "Cancel", top.destroy).pack(side=tk.LEFT, padx=6)
        top.bind("<Return>", lambda _: ok())

    def _scan_mode_hint_updater(self):
        try:
            sec = self.sec_var.get()
            mode = getattr(self, "mode_var", None)
            if mode:
                if sec == "tls":
                    mode.set("Config-Aware (Auto)")
        except Exception:
            pass

    def _build_sub_link_b64(self):
        """Base64-encode all currently built configs as a standard
        v2rayN/NekoBox-style subscription blob."""
        import base64 as _b64s
        configs = self.P.built_configs or []
        if not configs:
            return ""
        blob = "\n".join(configs).encode("utf-8")
        return _b64s.b64encode(blob).decode("ascii")

    def _host_subscription(self, b64_content):
        """POST the subscription content to paste.rs and return the real,
        fetchable https:// URL it gives back (GET on that URL returns the
        raw base64 text, which is exactly what v2rayN/NekoBox expect when
        you add it as a subscription URL). Returns None on any failure —
        caller falls back to the raw base64 content."""
        import urllib.request as _ur2
        try:
            req = _ur2.Request(
                "https://paste.rs/", data=b64_content.encode("utf-8"),
                method="POST", headers={"Content-Type": "text/plain",
                                        "User-Agent": "VLESS-Optimizer/1.0"})
            opener = _ur2.build_opener(_ur2.ProxyHandler({}))
            with opener.open(req, timeout=15) as r:
                url = r.read().decode("utf-8").strip()
            if url.startswith("https://paste.rs/"):
                return url
            return None
        except Exception:
            return None

    def _copy_sub_link(self, silent=False):
        b64 = self._build_sub_link_b64()
        self.P.last_sub_link = ""  # reset before attempting — no stale leak on failure
        if not b64:
            if not silent:
                self._logui("[SUBLINK] No configs to build a subscription from yet.")
            return
        n = len(self.P.built_configs)
        link = self._host_subscription(b64)
        if link:
            # Append a #name fragment so v2rayN / NekoBox / Hiddify display
            # the config name as the subscription remark instead of the raw
            # paste.rs host.
            sub_name = (self.P.cfg_name or self.P.name or "VLESS-Configs").strip()
            link = f"{link}#{urllib.parse.quote(sub_name, safe='')}"
            self.P.last_sub_link = link
            if silent:
                # Auto-generated right after Generate Configs — quiet
                # clipboard copy + log only, no popup (avoid an intrusive
                # dialog firing every single time configs are generated).
                self.root.clipboard_clear()
                self.root.clipboard_append(link)
                self._logui(f"[SUBLINK] ✔ Subscription link for {n} configs "
                            f"auto-copied to clipboard: {link}")
            else:
                # Explicit button click — show the same QR dialog used for
                # individual config cards, with Copy URL right below it.
                self._logui(f"[SUBLINK] ✔ Subscription link ready: {link}")
                show_qr(self.root, link, title=f"Subscription Link — {n} configs")
        else:
            # Hosting failed (offline / paste.rs unreachable) — fall back
            # to raw base64 content so the user isn't left empty-handed,
            # but be explicit that this is NOT a clickable link.
            if silent:
                self.root.clipboard_clear()
                self.root.clipboard_append(b64)
                self._logui(f"[SUBLINK] ⚠ Could not reach paste.rs to host a real "
                            f"link — copied raw base64 content instead (not a URL).")
            else:
                self._copy_with_toast(b64, f"Subscription content ({n} configs, raw)")
                self._logui("[SUBLINK] ⚠ Could not host a real link — "
                            "copied raw base64 content instead (not a URL).")

    def _save_sub_link(self):
        b64 = self._build_sub_link_b64()
        if not b64:
            self._logui("[SUBLINK] No configs to build a subscription from yet.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{self.P.name}_subscription.txt",
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not path: return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(b64)
            self._logui(f"[SUBLINK] ✔ Saved subscription content ({len(self.P.built_configs)} "
                        f"configs) → {path}  (local file, not hosted/uploaded anywhere)")
        except Exception as e:
            self._logui(f"[SUBLINK] Save error: {e}")

    def _copy_with_toast(self, url, name=""):
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        toast = tk.Toplevel(self.root)
        toast.wm_overrideredirect(True)
        x = self.root.winfo_rootx() + self.root.winfo_width()//2 - 150
        y = self.root.winfo_rooty() + self.root.winfo_height() - 80
        toast.wm_geometry(f"+{x}+{y}")
        toast.configure(bg=GREEN)
        tk.Label(toast, text=f"\u2714  {name} copied to clipboard!",
                 font=("Segoe UI", 10, "bold"), bg=GREEN, fg="white",
                 padx=16, pady=8).pack()
        toast.after(2200, toast.destroy)

    # ══════════════════════════════════════════════════════
    #  Scan tab
    # ══════════════════════════════════════════════════════

    def _build_scan(self):
        sf = self.pages["scan"]
        sf.rowconfigure(0, weight=0)   # clear page-loop default so only the
        sf.rowconfigure(1, weight=0)   # bottom list row (2) stretches
        sf.rowconfigure(2, weight=1)

        pc = _card(sf); pc.grid(row=0, column=0, sticky="ew", pady=(0,4))
        pc.columnconfigure(1, weight=1)
        pc.columnconfigure(3, weight=1)

        self.provider_var = tk.StringVar(value="Custom")
        self.range_var    = tk.StringVar()
        self.mode_var     = tk.StringVar(value="Config-Aware (Auto)")
        self.threads_var  = tk.StringVar(value="200")
        self.timeout_var  = tk.StringVar(value="5.0")
        self.tries_var    = tk.StringVar(value="4")
        self._range_tags: List[str] = []  # list of IP ranges as tags

        def _plabel(text, r, c):
            tk.Label(pc, text=text, font=FB, bg=CARD, fg=FG1, anchor="w").grid(
                row=r, column=c, padx=(12 if c == 0 else 10, 6),
                pady=5, sticky="w")

        # ---- Targets section -------------------------------------------------
        tk.Label(pc, text="Scan Targets", font=FH, bg=CARD, fg=FG2,
                 anchor="w").grid(row=0, column=0, columnspan=4,
                                  padx=12, pady=(8, 2), sticky="w")

        # Row 1 - Provider preset
        _plabel("Provider:", 1, 0)
        prov_cb = ttk.Combobox(pc, textvariable=self.provider_var,
                               values=list(PROVIDER_RANGES), state="readonly")
        prov_cb.grid(row=1, column=1, sticky="ew", padx=(0, 6), pady=5)
        prov_cb.bind("<<ComboboxSelected>>", self._on_provider)
        _add_tooltip(prov_cb, "Pick a known Cloudflare / CDN range preset,\nthen click + Add.")
        _abtn(pc, "+ Add", self._add_range_tag, small=True, color=TEAL).grid(
            row=1, column=2, columnspan=2, padx=(0, 12), pady=5, sticky="w")

        # Row 2 - Custom range
        _plabel("Custom range:", 2, 0)
        custom_entry = ttk.Entry(pc, textvariable=self.range_var)
        custom_entry.grid(row=2, column=1, sticky="ew", padx=(0, 6), pady=5)
        custom_entry.bind("<Return>", lambda e: self._add_range_tag())
        _add_tooltip(custom_entry, "CIDR or IP range, e.g. 104.16.0.0/16.\nPress Enter or click + Add.")
        _abtn(pc, "+ Add", self._add_range_tag, small=True, color=BLUE).grid(
            row=2, column=2, columnspan=2, padx=(0, 12), pady=5, sticky="w")

        # Row 3 - Active ranges (tags)
        _plabel("Ranges:", 3, 0)
        self._tags_frame = tk.Frame(pc, bg=CARD)
        self._tags_frame.grid(row=3, column=1, columnspan=3, sticky="ew",
                              padx=(0, 12), pady=(0, 4))
        self._tags_container = tk.Frame(self._tags_frame, bg=CARD)
        self._tags_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._refresh_tags()

        # divider
        tk.Frame(pc, bg=BORDER, height=1).grid(row=4, column=0, columnspan=4,
                                               sticky="ew", padx=12, pady=(4, 6))

        # ---- Parameters section ---------------------------------------------
        tk.Label(pc, text="Scan Parameters", font=FH, bg=CARD, fg=FG2,
                 anchor="w").grid(row=5, column=0, columnspan=4,
                                  padx=12, pady=(0, 2), sticky="w")

        # Row 6 - Scan Mode + Threads
        _plabel("Scan Mode:", 6, 0)
        mode_cb = ttk.Combobox(pc, textvariable=self.mode_var,
                               values=["Config-Aware (Auto)",
                                       "TCP Connect",
                                       "TLS Handshake",
                                       "HTTP Request"],
                               state="readonly")
        mode_cb.grid(row=6, column=1, sticky="ew", padx=(0, 6), pady=5)
        _add_tooltip(mode_cb, "How each IP is probed. Config-Aware is best\nfor filtered ISPs.")
        _plabel("Threads:", 6, 2)
        _sp_threads = ttk.Spinbox(pc, from_=1, to=2000,
                                  textvariable=self.threads_var, width=8)
        _sp_threads.grid(row=6, column=3, sticky="w", padx=(0, 12), pady=5)
        _add_tooltip(_sp_threads, "Concurrent probes. Higher = faster but heavier.")

        # Row 7 - Timeout + Tries
        _plabel("Timeout (s):", 7, 0)
        _sp_to = ttk.Spinbox(pc, from_=0.5, to=30, increment=0.5,
                             textvariable=self.timeout_var, width=8)
        _sp_to.grid(row=7, column=1, sticky="w", padx=(0, 6), pady=5)
        _add_tooltip(_sp_to, "Per-probe timeout in seconds.")
        _plabel("Tries / IP:", 7, 2)
        _sp_tries = ttk.Spinbox(pc, from_=1, to=10,
                                textvariable=self.tries_var, width=8)
        _sp_tries.grid(row=7, column=3, sticky="w", padx=(0, 12), pady=5)
        _add_tooltip(_sp_tries, "Probes per IP. More tries = real average + loss %.")

        # Row 8 - tries note
        tk.Label(pc, text="(more tries per IP = real average latency + packet loss %)",
                 font=FS, bg=CARD, fg=FG3, anchor="w").grid(
            row=8, column=0, columnspan=4, padx=12, pady=(0, 4), sticky="w")

        # Row 9 - mode hint / warning
        self._scan_mode_hint = tk.Label(
            pc, text="", font=FS, bg=CARD, fg=GREEN,
            anchor="w", wraplength=820, justify="left")
        self._scan_mode_hint.grid(row=9, column=0, columnspan=4,
                                  padx=12, pady=(0, 8), sticky="w")

        def _update_mode_hint(*_):
            m   = self.mode_var.get()
            sni = self._clean_host(self.sni_var.get()) if hasattr(self, "sni_var") else ""
            hst = self._clean_host(self.host_var.get()) if hasattr(self, "host_var") else ""
            has_tls_cfg = bool((sni or hst) and
                               getattr(self, "sec_var", None) and
                               self.sec_var.get() == "tls")
            if m == "Config-Aware (Auto)":
                if has_tls_cfg:
                    self._scan_mode_hint.config(
                        text=("✔ Config-Aware: Phase 1 fast TCP pre-filter → "
                              "Phase 2 TLS+SNI verify with your config.\n"
                              "  Only IPs that actually work with your domain survive. "
                              "Ideal for filtered ISPs (Irancell, etc)."),
                        fg=GREEN)
                else:
                    self._scan_mode_hint.config(
                        text="✔ Config-Aware: no TLS config detected — will use TCP scan. "
                             "Fill Config tab (Security=TLS + Host) to enable deep verify.",
                        fg=TEAL)
            elif m == "TCP Connect":
                if has_tls_cfg:
                    self._scan_mode_hint.config(
                        text=("⚠  TCP-only mode: finds IPs with open ports but does NOT "
                              "verify TLS/SNI reachability.\n"
                              "  On filtered ISPs (Irancell, MCI) many found IPs will fail "
                              "in the actual proxy — use Config-Aware instead."),
                        fg=ORANGE)
                else:
                    self._scan_mode_hint.config(
                        text="TCP Connect: fastest scan — checks port reachability only.",
                        fg=FG3)
            elif m == "TLS Handshake":
                self._scan_mode_hint.config(
                    text="TLS Handshake: verifies TLS with your SNI. "
                         "Slower than TCP but filters SNI-blocked IPs.",
                    fg=FG3)
            else:  # HTTP Request
                self._scan_mode_hint.config(
                    text="HTTP Request: full TLS+SNI+HTTP probe — most accurate, "
                         "closest to real proxy behaviour.",
                    fg=FG3)

        mode_cb.bind("<<ComboboxSelected>>", _update_mode_hint)
        self.mode_var.trace_add("write", _update_mode_hint)
        # refresh hint whenever config fields change
        self._scan_mode_hint_updater = _update_mode_hint
        _update_mode_hint()

        # ports card
        ptc = _card(sf); ptc.grid(row=1, column=0, sticky="ew", pady=(0,4))
        tk.Label(ptc, text="Ports:", font=FB, bg=BG_CARD, fg=FG2).grid(
            row=0, column=0, padx=(8,4), pady=4, sticky="w")
        self.port_vars: Dict[int, tk.BooleanVar] = {}
        for ci, p in enumerate(CF_PORTS, 1):
            v = tk.BooleanVar(value=(p==443))
            ttk.Checkbutton(ptc, text=str(p), variable=v).grid(row=0, column=ci, padx=3, pady=4)
            self.port_vars[p] = v
        _abtn(ptc,"All",  lambda:[v.set(True) for v in self.port_vars.values()],
              True,TEAL).grid(row=0, column=len(CF_PORTS)+1, padx=(6,3), pady=4)
        _gbtn(ptc,"None", lambda:[v.set(False) for v in self.port_vars.values()],
              True).grid(row=0, column=len(CF_PORTS)+2, padx=(0,8), pady=4)

        # controls
        ctrl = tk.Frame(sf, bg=BG)
        ctrl.grid(row=2, column=0, sticky="nsew")
        ctrl.columnconfigure(0, weight=1); ctrl.rowconfigure(1, weight=1)

        btns = tk.Frame(ctrl, bg=BG)
        btns.grid(row=0, column=0, sticky="w", pady=(0,6))
        self._scan_btn = _abtn(btns, "\u25b6  Start Scan", self._start_scan)
        self._scan_btn.pack(side=tk.LEFT, padx=(0,6))
        self._scan_stop_btn = _gbtn(btns, "\u23f9  Stop", self._stop_scan)
        self._scan_stop_btn.pack(side=tk.LEFT, padx=(0,12))
        self._scan_stop_btn.config(state=tk.DISABLED)
        self._progress = ttk.Progressbar(btns, mode="determinate", length=200)
        self._progress.pack(side=tk.LEFT, padx=(0,8))
        self._stat_var = tk.StringVar(value="Ready")
        tk.Label(btns, textvariable=self._stat_var, font=FS, bg=BG, fg=FG3).pack(side=tk.LEFT)

        lf = tk.Frame(ctrl, bg=BG)
        lf.grid(row=1, column=0, sticky="nsew")
        lf.columnconfigure(0, weight=1); lf.rowconfigure(0, weight=1)
        self._scan_log = tk.Text(lf, wrap="word", state="disabled",
                                 height=8, bg="#0d1117", fg="#c0caf5",
                                 font=FM, relief="flat", bd=0,
                                 insertbackground="#c0caf5",
                                 selectbackground=ACCENT,
                                 padx=10, pady=6)
        self._scan_log.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        sb2 = ttk.Scrollbar(lf, orient="vertical", command=self._scan_log.yview)
        sb2.grid(row=0, column=1, sticky="ns")
        self._scan_log.configure(yscrollcommand=sb2.set)

        # ── Scan History section ──
        hist_card = _card(sf)
        hist_card.grid(row=3, column=0, sticky="ew", pady=(4, 0))
        hist_card.columnconfigure(1, weight=1)

        tk.Label(hist_card, text="Scan History:", font=FB, bg=CARD, fg=FG1,
                 anchor="w").grid(row=0, column=0, padx=(12, 4), pady=4, sticky="w")
        self._hist_var = tk.StringVar(value="\u2014 no history \u2014")
        self._hist_combo = ttk.Combobox(hist_card, textvariable=self._hist_var,
                                         state="readonly", width=40)
        self._hist_combo.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=4)
        _abtn(hist_card, "Load", self._load_history_entry, small=True, color=TEAL).grid(
            row=0, column=2, padx=(0, 4), pady=4)
        _abtn(hist_card, "Delete", self._delete_history_entry, small=True, color=RED_C).grid(
            row=0, column=3, padx=(0, 12), pady=4)
        self._refresh_history_combo()

    def _refresh_history_combo(self):
        try:
            h = self.P.scan_history
            if not h:
                self._hist_combo["values"] = ["\u2014 no history \u2014"]
                self._hist_var.set("\u2014 no history \u2014")
                try: self._hist_combo2["values"] = ["\u2014 no history \u2014"]
                except Exception: pass
                return
            labels = []
            for i, e in enumerate(h):
                t = e.get("time", "")[:16]
                mode = e.get("mode", "tcp").upper()
                rname = e.get("range_name", "")[:18]
                found = e.get("found", 0)
                scanned = e.get("scanned", 0)
                # Include the config Host/SNI (trimmed) so scans of different
                # workers are easy to tell apart in the dropdown.
                host = (e.get("host", "") or "").strip()
                host_s = f"  ⟨{host[:28]}⟩" if host else ""
                labels.append(
                    f"#{len(h)-i}  {t}  {mode}  {rname}  "
                    f"{found}/{scanned} verified{host_s}")
            # Keep both tab combos (scan + test) in sync with the same labels,
            # in the same order as scan_history, so index lookups stay valid.
            self._hist_combo["values"] = labels
            try: self._hist_combo2["values"] = labels
            except Exception: pass
            if self._hist_var.get() not in labels:
                self._hist_var.set(labels[0])
        except Exception:
            pass

    def _refresh_scanresult(self):
        ok = [r for r in self.P.results if r.ping_ms is not None]
        self._sr_lbl.config(text=f"{len(ok)} IPs")
        self._sr_sf.clear()
        inner = self._sr_sf.inner
        if not ok:
            tk.Label(inner, text="No scan results. Run a scan first.",
                     font=FB, bg=BG, fg=FG3).pack(pady=20); return
        if not self.P.built_configs:
            tk.Label(inner,
                     text=f"✔  {len(ok)} IPs found.\n\n"
                           "Set Top N and click  ⚙ Generate Configs\n"
                           "to build and see your configs here.",
                     font=FB, bg=BG, fg=FG2, justify="center").pack(pady=30); return
        for i, r in enumerate(ok[:len(self.P.built_configs)], 1):
            self._sr_card(inner, r, i)

    def _sr_card(self, parent, r: ProbeResult, idx: int):
        p    = self.P
        # Card background matches ping color
        ping = r.ping_ms
        if ping is not None and ping < 150:
            card_bg = CARD_BG_2
        elif ping is not None and ping < 400:
            card_bg = CARD_BG_3
        else:
            card_bg = CARD_BG_4
        card = _card(parent, bg=card_bg)
        card.pack(fill=tk.X, pady=3, padx=2)
        tk.Frame(card, bg=_ping_color(r.ping_ms), width=5).pack(side=tk.LEFT, fill=tk.Y)
        bf = tk.Frame(card, bg=card_bg)
        bf.pack(side=tk.RIGHT, padx=6, pady=4)
        if p.has_config:
            url  = self._vless(r.ip, r.port)
            name = f"{p.cfg_name} {r.ip}:{r.port}"
            con = _ilbl(bf,"🌐", lambda rr=r: self._load_connect(rr))
            con.pack(side=tk.LEFT, padx=2)
            _add_tooltip(con, "Connect")
            lnk = _ilbl(bf,"🔗", lambda u=url,n=name: self._copy_with_toast(u,n))
            lnk.pack(side=tk.LEFT, padx=2)
            _add_tooltip(lnk, "Copy config link")
            qrl = _ilbl(bf,"📷", lambda u=url,n=name: show_qr(self.root,u,n))
            qrl.pack(side=tk.LEFT, padx=2)
            _add_tooltip(qrl, "Show QR code")
            edit_lbl = _ilbl(bf,"✏", lambda rr=r, n=name: self._edit_config_dialog(rr, n))
            edit_lbl.pack(side=tk.LEFT, padx=2)
            _add_tooltip(edit_lbl, "Edit config")
            star = _ilbl(bf,"⭐", lambda u=url,n=name: self._add_favorite(u,n))
            star.pack(side=tk.LEFT, padx=2)
            _add_tooltip(star, "Add to Favorites")
            test_lbl = _ilbl(bf,"⚡", lambda rr=r: self._test_single_config(rr))
            test_lbl.pack(side=tk.LEFT, padx=2)
            _add_tooltip(test_lbl, "Test this config")
        dell = _ilbl(bf,"🗑", lambda rr=r: self._del_result(rr))
        dell.pack(side=tk.LEFT, padx=2)
        _add_tooltip(dell, "Delete result")
        # ── Info (LEFT, expands into remaining space) ─────────────────────────
        inner = tk.Frame(card, bg=card_bg)
        inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=6)
        cfg_label = (f"#{idx}  {p.cfg_name} \u2014 {r.ip}:{r.port}"
                     if p.has_config else f"#{idx}  {r.ip}:{r.port}")
        tk.Label(inner, text=cfg_label, font=FH, bg=card_bg, fg=FG1,
                 wraplength=320, anchor="w", justify="left").pack(anchor="w")
        row2 = tk.Frame(inner, bg=card_bg)
        row2.pack(anchor="w")
        for lbl,val,col in [
            ("Ping",   _ping_label(r.ping_ms),  _ping_color(r.ping_ms)),
            ("Jitter", (f"{r.jitter_ms:.0f}ms" if r.jitter_ms is not None else "\u2014"),
                        _ping_color(r.jitter_ms)),
            ("Loss",   (f"{r.loss_pct:.0f}%" if r.loss_pct is not None else "\u2014"),
                        GREEN if (r.loss_pct or 0)<5 else (ORANGE if (r.loss_pct or 0)<25 else RED_C)),
            ("Colo",   r.colo or "\u2014", TEAL if r.cf_valid else FG3),
            ("DL",     f"{r.dl_mbps:.1f}M" if r.dl_mbps else "\u2014",
                        GREEN if (r.dl_mbps or 0)>=5 else (ORANGE if (r.dl_mbps or 0)>=1 else RED_C)),
            ("UP",     f"{r.up_mbps:.1f}M" if r.up_mbps else "\u2014",
                        GREEN if (r.up_mbps or 0)>=5 else (ORANGE if (r.up_mbps or 0)>=1 else RED_C)),
            ("ICMP",   _ping_label(r.icmp_ms),  _ping_color(r.icmp_ms)),
        ]:
            tk.Label(row2, text=f" {lbl}:", font=FS, bg=card_bg, fg=FG1).pack(side=tk.LEFT)
            tk.Label(row2, text=f" {val} ", font=("Segoe UI",9,"bold"), bg=card_bg,
                     fg=col).pack(side=tk.LEFT)

    def _more_sr(self):
        self._sr_limit = getattr(self, "_sr_limit", 5) + 5
        self._refresh_scanresult()

    def _sort_sr(self):
        key = self._sr_sort.get()
        ok  = [r for r in self.P.results if r.ping_ms is not None]
        if   key=="Ping":   ok.sort(key=lambda r: r.ping_ms   or 1e9)
        elif key=="Jitter": ok.sort(key=lambda r: r.jitter_ms or 1e9)
        elif key=="Loss":   ok.sort(key=lambda r: r.loss_pct  or 0)
        elif key=="TCP":    ok.sort(key=lambda r: r.tcp_ms    or 1e9)
        elif key=="ICMP":   ok.sort(key=lambda r: r.icmp_ms   or 1e9)
        elif key=="DL":     ok.sort(key=lambda r: -(r.dl_mbps or 0))
        elif key=="UP":     ok.sort(key=lambda r: -(r.up_mbps or 0))
        elif key=="Colo":   ok.sort(key=lambda r: r.colo or "zzz")
        elif key=="IP":
            ok.sort(key=lambda r: tuple(int(x) for x in r.ip.split(".")))
        self.P.results = ok + [r for r in self.P.results if r.ping_ms is None]
        self._sr_limit = 5
        self._refresh_scanresult()

    def _del_result(self, r: ProbeResult):
        if messagebox.askyesno("Delete", f"Remove {r.ip}:{r.port} from results?",
                                parent=self.root):
            self.P.results = [x for x in self.P.results if not (x.ip==r.ip and x.port==r.port)]
            save_profiles(self.profiles, self._prof_idx)
            self._refresh_scanresult()
            self._refresh_home()
            self._refresh_test_tree()
            self._refresh_connect_combo()
            self._update_tab_states()

    # ══════════════════════════════════════════════════════
    #  Test tab
    # ══════════════════════════════════════════════════════

    def _build_test(self):
        tf = self.pages["test"]
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)

        # ── Vertical PanedWindow ──────────────────────────────────────────
        pw = tk.PanedWindow(tf, orient=tk.VERTICAL, sashwidth=6,
                            bg=BORDER, sashrelief="flat",
                            opaqueresize=True)
        pw.grid(row=0, column=0, sticky="nsew")

        # ═══════════════════════════════════════════════════
        #  TOP PANE  ─  Test section
        # ═══════════════════════════════════════════════════
        top_pane = tk.Frame(pw, bg=BG)
        top_pane.columnconfigure(0, weight=1)
        top_pane.rowconfigure(4, weight=1)   # tree row expands

        # ── Section header ────────────────────────────────
        top_hdr = tk.Frame(top_pane, bg=BG)
        top_hdr.grid(row=0, column=0, sticky="ew", padx=2, pady=(4, 2))
        tk.Label(top_hdr, text="⚙  Test", font=FH, bg=BG, fg=FG1).pack(side=tk.LEFT)
        self._test_xray_status = tk.Label(top_hdr, text="", font=FS, bg=BG, fg=FG3)
        self._test_xray_status.pack(side=tk.LEFT, padx=(10, 0))
        self._update_xray_status_label()

        # ── Controls card ─────────────────────────────────
        ctrl = _card(top_pane)
        ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        ctrl.columnconfigure(7, weight=1)

        tk.Label(ctrl, text="# Configs:", font=FB, bg=CARD, fg=FG1).grid(
            row=0, column=0, padx=(12, 4), pady=8, sticky="w")
        # Editable combo box: how many configs to generate from the pool.
        self._test_n = tk.StringVar(value="10")
        ttk.Combobox(ctrl, textvariable=self._test_n, width=5,
                     values=["5", "10", "15", "20", "30", "50", "100"]).grid(
                     row=0, column=1, padx=4, pady=8)
        # Live pool count shown right beside the selector.
        self._test_pool_lbl = tk.Label(ctrl, text="pool: 0", font=FS,
                                       bg=CARD, fg=TEAL)
        self._test_pool_lbl.grid(row=0, column=2, padx=(2, 8), pady=8, sticky="w")

        self._gen_btn = _abtn(ctrl, "⚙ Generate Configs", self._generate_configs, color=BLUE)
        self._gen_btn.grid(row=0, column=3, padx=(6, 4), pady=8)

        self._quick_test_btn = _abtn(ctrl, "⚡ Quick Test",
                                     self._quick_test, color=TEAL)
        self._quick_test_btn.grid(row=0, column=4, padx=4, pady=8)
        _add_tooltip(self._quick_test_btn,
                     "Fast TCP re-check of the selected number of IPs — no xray needed.\n"
                     "Tested one-by-one for accurate latency/jitter.")

        self._test_btn = _abtn(ctrl, "▶ Full Test", self._start_test)
        self._test_btn.grid(row=0, column=5, padx=4, pady=8)
        self._test_btn.config(state=tk.DISABLED)
        _add_tooltip(self._test_btn,
                     "Run full xray proxy test (one-by-one): latency + download speed per config.")

        _gbtn(ctrl, "\u23f9 Stop", self._stop_test, small=True).grid(
            row=0, column=6, padx=(2, 4), pady=8)

        # (Removed: "Add More Verified IP" pool section — configs now come
        #  straight from the verified pool via the # Configs selector.)

        # progress bar + status label
        prog_row = tk.Frame(top_pane, bg=BG)
        prog_row.grid(row=3, column=0, sticky="ew", padx=2, pady=(0, 1))
        prog_row.columnconfigure(0, weight=1)
        self._test_prog = ttk.Progressbar(prog_row, mode="determinate")
        self._test_prog.grid(row=0, column=0, sticky="ew")
        self._test_status_lbl = tk.Label(prog_row, text="", font=FS, bg=BG, fg=FG2)
        self._test_status_lbl.grid(row=0, column=1, padx=(6, 0), sticky="w")

        # ── Test result tree ──────────────────────────────
        tree_wrap = tk.Frame(top_pane, bg=BG)
        tree_wrap.grid(row=4, column=0, sticky="nsew", pady=(0, 2))
        tree_wrap.columnconfigure(0, weight=1)
        tree_wrap.rowconfigure(0, weight=1)

        cols   = ("num","ip","port","ping","jitter","loss","colo","dl","up","lat","status")
        heads  = ("#","IP","Port","Ping","Jitter","Loss%","Colo",
                  "DL Mbps","UP Mbps","Latency","Status")
        widths = (30, 98, 46, 58, 56, 48, 42, 58, 58, 58, 90)
        self._test_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", height=8)
        for c, h, w in zip(cols, heads, widths):
            self._test_tree.heading(c, text=h,
                command=lambda col=c: self._sort_test_col(col))
            self._test_tree.column(c, width=w, anchor="center", stretch=False)
        self._test_tree.column("num",    anchor="center", width=30)
        self._test_tree.column("ip",     anchor="w")
        self._test_tree.column("status", anchor="w", stretch=True)
        self._test_tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._test_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self._test_tree.configure(yscrollcommand=vsb.set)
        self._test_tree.tag_configure("good",   foreground=GREEN)
        self._test_tree.tag_configure("ok",     foreground=ORANGE)
        self._test_tree.tag_configure("bad",    foreground=RED_C)
        self._test_tree.tag_configure("notest", foreground=FG4)

        # right-click: copy URL for selected row
        self._test_tree.bind("<Button-3>", self._test_tree_ctx)

        pw.add(top_pane, minsize=120, sticky="nsew")

        # ═══════════════════════════════════════════════════
        #  BOTTOM PANE  ─  Scan Results section
        # ═══════════════════════════════════════════════════
        bot_pane = tk.Frame(pw, bg=BG)
        bot_pane.columnconfigure(0, weight=1)
        bot_pane.rowconfigure(1, weight=1)

        bot_pane.rowconfigure(2, weight=1)

        # ── Toolbar row 1: title + count + save + sort ────
        tb1 = tk.Frame(bot_pane, bg=BG)
        tb1.grid(row=0, column=0, sticky="ew", padx=4, pady=(4,0))
        tk.Label(tb1, text="📋 Results", font=FH, bg=BG, fg=FG1).pack(side=tk.LEFT)
        self._sr_lbl = tk.Label(tb1, text="0 IPs", font=FS, bg=BG, fg=FG2)
        self._sr_lbl.pack(side=tk.LEFT, padx=(6,12))
        _abtn(tb1, "💾 Save TXT", self._save_txt, small=True).pack(side=tk.LEFT, padx=(0,6))
        _abtn(tb1, "📋 Copy Sub Link", self._copy_sub_link, small=True,
              color=TEAL).pack(side=tk.LEFT, padx=(0,6))
        _gbtn(tb1, "💾 Sub→File", self._save_sub_link, small=True).pack(
            side=tk.LEFT, padx=(0,6))
        tk.Frame(tb1, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y, padx=(0,6), pady=2)
        tk.Label(tb1, text="Sort:", font=FS, bg=BG, fg=FG2).pack(side=tk.LEFT)
        self._sr_sort = tk.StringVar(value="Ping")
        ttk.Combobox(tb1, textvariable=self._sr_sort, width=8,
                     values=["Ping","Jitter","Loss","TCP","ICMP","DL","UP","IP","Colo"],
                     state="readonly").pack(side=tk.LEFT, padx=(2,2))
        _gbtn(tb1, "↕", self._sort_sr, small=True).pack(side=tk.LEFT)

        # ── Toolbar row 2: history ─────────────────────────
        tb2 = tk.Frame(bot_pane, bg=BG)
        tb2.grid(row=1, column=0, sticky="ew", padx=4, pady=(2,4))
        tk.Label(tb2, text="\U0001f552 History:", font=FS, bg=BG, fg=FG2).pack(side=tk.LEFT)
        # Reuse the scan tab's history combo (created in _build_scan)
        self._hist_combo2 = ttk.Combobox(tb2, textvariable=self._hist_var, state="readonly")
        self._hist_combo2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4,6))
        _abtn(tb2, "Load \u2192", self._load_history_entry, small=True, color=TEAL).pack(
            side=tk.LEFT, padx=(0,4))
        _gbtn(tb2, "🗑 Clear", self._clear_history, small=True).pack(side=tk.LEFT)

        # ── Scrollable card list ──────────────────────────
        self._sr_sf = SF(bot_pane, bg=BG)
        self._sr_sf.grid(row=2, column=0, sticky="nsew")
        self._sr_limit = 9999

        pw.add(bot_pane, minsize=90, sticky="nsew")
        self._refresh_history_combo()

    # ── xray status helper (shown inline in test header) ─────────
    def _update_xray_status_label(self):
        try:
            if self.xray.is_installed():
                self._test_xray_status.config(
                    text=f"✔ xray ready", fg=GREEN)
            else:
                self._test_xray_status.config(
                    text="⚠ xray not found — download in Settings → Xray Core",
                    fg=ORANGE)
        except Exception:
            pass

    def _test_tree_ctx(self, event):
        iid = self._test_tree.identify_row(event.y)
        if not iid: return
        vals = self._test_tree.item(iid, "values")
        if not vals: return
        try:
            ip   = vals[0]
            port = int(vals[1])
            url  = self._vless(ip, port)
            name = f"{self.P.cfg_name} {ip}:{port}"
            self._copy_with_toast(url, name)
        except Exception:
            pass



    def _generate_configs(self):
        p = self.P
        if not p.has_config:
            messagebox.showwarning("No Config",
                "Fill UUID and Host in Config tab first.", parent=self.root); return
        ok = [r for r in p.results if r.ping_ms is not None]
        if not ok:
            messagebox.showwarning("No Results",
                "Run a scan first to get IPs.", parent=self.root); return
        pool_count = len(ok)
        try:
            requested_n = int(self._test_n.get())
        except (ValueError, TypeError):
            requested_n = 10
        if requested_n < 1:
            requested_n = 1
        # Clamp to the verified pool size (no separate Top-N cap anymore).
        if requested_n > pool_count:
            messagebox.showinfo("Pool Limit",
                f"The verified pool has {pool_count} IP(s).\n"
                f"Generating the best {pool_count} configs (max available).",
                parent=self.root)
            requested_n = pool_count
        n = requested_n
        self._test_n.set(str(n))
        # Wipe previous first
        for i in self._test_tree.get_children(): self._test_tree.delete(i)
        p.built_configs = []
        self._refresh_scanresult()
        self._auto_generate_after_test = True
        self._logui(f"[GENERATE] Pinging top {n} IPs to find best latency\u2026")
        self._test_status_lbl.config(text=f"Pinging {n} IPs\u2026", fg=ORANGE)
        self._quick_test()

    def _do_generate_configs(self):
        p = self.P
        # Rank the whole verified pool by config metrics and take the best N.
        ok = self._best_sorted(p.results)
        if not ok: return
        try:
            n = int(self._test_n.get())
        except (ValueError, TypeError):
            n = 10
        n   = max(1, min(n, len(ok)))
        top = ok[:n]   # best N from the pool, ranked by ping/latency/jitter/loss

        sni  = p.sni  or p.host or ""
        host = p.host or ""
        path = p.path or "/"

        # Only re-probe in HTTP+TLS+SNI (config-verify) mode. The re-verify now
        # runs in a WORKER THREAD (not on the UI thread) so the window never
        # freezes; results are finalised back on the UI thread via the
        # ("gen_finalize") queue message handled in _handle().
        if p.mode == "http" and sni:
            self._logui(f"[GENERATE] Re-verifying {n} IPs with WS probe\u2026")
            try:
                self._test_status_lbl.config(text=f"Re-verifying {n} IPs\u2026", fg=ORANGE)
            except Exception:
                pass
            threading.Thread(
                target=self._gen_recheck_thr,
                args=(top, n, sni, host, path),
                daemon=True).start()
        else:
            self._finalize_generate(top, n)

    def _gen_recheck_thr(self, top, n, sni, host, path):
        # Background WS reachability re-verify (pass/fail only, tries=1).
        # Parallel here is fine: we only check reachability, NOT latency or
        # throughput metrics, so it cannot distort per-config measurements.
        async def _ws_recheck(candidates):
            opt = Optimizer(concurrency=min(60, len(candidates) + 1),
                            timeout=5.0, tries=1)
            results = []
            async def chk(r):
                async with opt.sem:
                    ms = await opt._http_raw(r.ip, r.port, sni, host, path)
                results.append((r, ms))
            await asyncio.gather(*[asyncio.create_task(chk(r)) for r in candidates],
                                 return_exceptions=True)
            return results
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            checked = loop.run_until_complete(_ws_recheck(top))
            loop.close()
        except Exception as ex:
            self._logui(f"[GENERATE] \u26a0 Re-verify error: {ex} \u2014 using TCP-pass list")
            checked = [(r, r.ping_ms) for r in top]
        passed = [(r, ms) for r, ms in checked if ms is not None]
        passed.sort(key=lambda x: x[1])
        for r, ms in passed:
            r.ping_ms = ms
        survivors = [r for r, _ in passed]
        self.q.put(("gen_finalize", survivors, n, len(top) - len(survivors)))

    def _finalize_generate(self, top, n, dropped=0):
        # Runs on the UI thread (directly for TCP/TLS modes, or via the
        # gen_finalize queue message after the background WS re-verify).
        p = self.P
        if dropped:
            self._logui(
                f"[GENERATE] \u26a0 {dropped}/{n} IPs dropped \u2014 failed WS re-verify "
                f"(rotated edge or IR-MCI blocked). {len(top)} remain.")
        if not top:
            self._logui(
                "[GENERATE] \u2716 0 IPs survived re-verify.  All edges rotated or blocked.\n"
                "           Re-run scan, or try different port / range.")
            try: self._test_status_lbl.config(text="No valid IPs \u2716", fg=RED_C)
            except Exception: pass
            messagebox.showwarning(
                "No Valid IPs",
                "All IPs failed the WebSocket re-verify.\n\n"
                "The Cloudflare edge IPs have likely rotated since the scan.\n"
                "Please run a new scan.",
                parent=self.root)
            return
        for i in self._test_tree.get_children(): self._test_tree.delete(i)
        p.built_configs = [self._vless(r.ip, r.port) for r in top]
        p.results = top + [r for r in p.results if r not in top]
        save_profiles(self.profiles, self._prof_idx)
        self._update_tab_states()
        self._refresh_test_tree()
        self._refresh_scanresult()
        self._refresh_connect_combo()
        self._refresh_home()
        self._test_btn.config(state=tk.NORMAL)
        try: self._test_status_lbl.config(text=f"{len(top)} configs built \u2714", fg=GREEN)
        except Exception: pass
        self._logui(f"[GENERATE] \u2714 {len(top)} configs built from best {n} IPs by ping.")
        # Auto-generate the subscription link every time configs are built.
        self._copy_sub_link(silent=True)
        if getattr(p, "last_sub_link", ""):
            sub_msg = f"\U0001f4cb Subscription link copied to clipboard:\n{p.last_sub_link}"
        else:
            sub_msg = ("\U0001f4cb Raw subscription content copied to clipboard\n"
                       "(couldn't reach paste.rs to host a real link \u2014 not a URL).")
        xray_note = ""
        if not self.xray.is_installed():
            xray_note = "\n\n\u26a0 xray-core not found \u2014 Settings \u2192 Xray Core."
        messagebox.showinfo("Configs Ready",
            f"\u2714  {len(top)} VLESS configs built from the {n} best-ping IPs.\n"
            f"{sub_msg}\n"
            "Press \u25b6 Full Test for proxy test, or \u26a1 Quick Test to re-ping."
            + xray_note, parent=self.root)


    def _add_from_pool(self):
        p = self.P
        all_ok = [r for r in p.results if r.ping_ms is not None]
        current_count = len(p.built_configs)
        try:
            n_add = int(self._pool_add_var.get())
        except ValueError:
            n_add = 5
        remaining = len(all_ok) - current_count
        if remaining <= 0:
            messagebox.showinfo("Pool", "No more verified IPs in the pool.", parent=self.root)
            return
        new_ips = all_ok[current_count:current_count + n_add]
        if not new_ips:
            messagebox.showinfo("Pool", "No more verified IPs in the pool.", parent=self.root)
            return
        for r in new_ips:
            p.built_configs.append(self._vless(r.ip, r.port))
        total_built = len(p.built_configs)
        self._test_n.set(str(total_built))
        save_profiles(self.profiles, self._prof_idx)
        self._refresh_test_tree()
        self._refresh_home()
        self._logui(f"[POOL] Added {len(new_ips)} IPs. Total: {total_built} configs built")
        messagebox.showinfo("Pool",
            f"{len(new_ips)} verified IPs added — {total_built} configs now built.",
            parent=self.root)

    def _refresh_pool_count(self):
        try:
            p = self.P
            all_ok = [r for r in p.results if r.ping_ms is not None]
            # Use passed_count if available (from scan), otherwise len(all_ok)
            total = getattr(p, "passed_count", len(all_ok))
            # The old "X/Y verified" pool label was removed with the
            # "Add More Verified IP" section — guard it for back-compat.
            lbl = getattr(self, "_pool_count_lbl", None)
            if lbl is not None:
                current = len(p.built_configs) if p.built_configs else 0
                try: lbl.config(text=f"{current}/{total} verified")
                except Exception: pass
            try:
                self._test_pool_lbl.config(text=f"pool: {total}")
            except Exception:
                pass
        except Exception:
            pass

    def _refresh_test_tree(self):
        for i in self._test_tree.get_children():
            self._test_tree.delete(i)
        p = self.P
        n = len(p.built_configs) if p.built_configs else 0
        # Always update pool count, even when no built configs
        try:
            self._refresh_pool_count()
        except Exception:
            pass
        if not n: return
        ok = [r for r in p.results if r.ping_ms is not None][:n]
        for i, r in enumerate(ok, 1):
            self._test_insert_row(r, True, i)

    def _test_insert_row(self, r: ProbeResult, has_cfg: bool, idx: int = 0):
        def f(v, unit=""): return f"{v:.1f}{unit}" if v is not None else "\u2014"
        def fpct(v): return f"{v:.0f}%" if v is not None else "\u2014"
        tag = "notest"
        if r.tested:
            pm = r.ping_ms or 9999
            tag = "good" if pm<150 else ("ok" if pm<400 else "bad")
        self._test_tree.insert("", tk.END, tags=(tag,), values=(
            f"#{idx}" if idx else "", r.ip, r.port,
            f(r.ping_ms,"ms"), f(r.jitter_ms,"ms"), fpct(r.loss_pct),
            r.colo or "\u2014", f(r.dl_mbps), f(r.up_mbps), f(r.lat_ms,"ms"),
            r.error or ("\u2714 ok" if r.ping_ms else "\u2014"),
        ))

    def _sort_test_col(self, col: str):
        if self._test_sort_col == col:
            self._test_sort_asc = not self._test_sort_asc
        else:
            self._test_sort_col = col; self._test_sort_asc = True
        key_map = {"ip":     lambda r: tuple(int(x) for x in r.ip.split(".")),
                   "port":   lambda r: r.port,
                   "ping":   lambda r: r.ping_ms   or 1e9,
                   "jitter": lambda r: r.jitter_ms or 1e9,
                   "loss":   lambda r: r.loss_pct  or 0,
                   "colo":   lambda r: r.colo or "zzz",
                   "dl":     lambda r: -(r.dl_mbps or 0),
                   "up":     lambda r: -(r.up_mbps or 0),
                   "lat":    lambda r: r.lat_ms    or 1e9,
                   "status": lambda r: r.error or ""}
        fn = key_map.get(col)
        n  = len(self.P.built_configs) if self.P.built_configs else None
        ok = [r for r in self.P.results if r.ping_ms is not None]
        if fn: ok.sort(key=fn, reverse=not self._test_sort_asc)
        self.P.results = ok + [r for r in self.P.results if r.ping_ms is None]
        if n: self.P.built_configs = [self._vless(r.ip, r.port) for r in ok[:n]]
        self._refresh_test_tree()
        self._refresh_scanresult()

    # _dl_xray removed — xray download is now only in Settings tab via _dl_xray_settings()

    # ══════════════════════════════════════════════════════
    #  Connect tab
    # ══════════════════════════════════════════════════════

    def _build_connect(self):
        pf = self.pages["connect"]
        pf.columnconfigure(0, weight=1)
        pf.rowconfigure(0, weight=0)   # clear page-loop default so only the
        pf.rowconfigure(1, weight=0)   # live-status card (row 3) stretches
        pf.rowconfigure(2, weight=0)
        pf.rowconfigure(3, weight=1)   # live-status card expands

        # ---- Server config selector ---------------------------------------
        sc = _card(pf); sc.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        sc.columnconfigure(1, weight=1)
        tk.Label(sc, text="Server Config", font=FH, bg=CARD, fg=FG2,
                 anchor="w").grid(row=0, column=0, columnspan=3,
                                  padx=12, pady=(8, 2), sticky="w")
        tk.Label(sc, text="Config:", font=FB, bg=CARD, fg=FG1,
                 width=8, anchor="w").grid(row=1, column=0, padx=(12, 6),
                                           pady=(2, 10), sticky="w")
        self._con_var = tk.StringVar()
        self._con_cb  = ttk.Combobox(sc, textvariable=self._con_var,
                                     state="readonly")
        self._con_cb.grid(row=1, column=1, sticky="ew", padx=(0, 6), pady=(2, 10))
        _add_tooltip(self._con_cb,
                     "Pick which scanned & tested config/IP to connect through.\n"
                     "Sorted best-first. Run Scan + Test to populate this list.")
        _gbtn(sc, "\u21bb", self._refresh_connect_combo, True).grid(
            row=1, column=2, padx=(0, 12), pady=(2, 10))

        # ---- Connection settings (mode + ports + TUN) ----------------------
        mc = _card(pf); mc.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for c in range(4):
            mc.columnconfigure(c, weight=1, uniform="cm")

        tk.Label(mc, text="Connection Mode", font=FH, bg=CARD, fg=FG2,
                 anchor="w").grid(row=0, column=0, columnspan=4,
                                  padx=12, pady=(8, 2), sticky="w")
        self._conn_mode = tk.StringVar(value="manual")
        _mode_tips = {
            "manual": "Manual: connect through exactly the config selected above.",
            "auto":   "Auto-Best: ignore the selection and pick the best tested\n"
                      "config automatically (lowest latency / ping).",
            "switch": "Auto-Switch: connect to the best config and automatically\n"
                      "switch to another if the current one degrades\n"
                      "(keeps each for at least 2 minutes).",
        }
        for ci, (val, txt) in enumerate([("manual", "Mode 1 \u00b7 Manual"),
                                         ("auto",   "Mode 2 \u00b7 Auto-Best"),
                                         ("switch", "Mode 3 \u00b7 Auto-Switch")]):
            _rb = ttk.Radiobutton(mc, text=txt, variable=self._conn_mode, value=val)
            _rb.grid(row=1, column=ci, padx=(12 if ci == 0 else 6, 6),
                     pady=(0, 8), sticky="w")
            _add_tooltip(_rb, _mode_tips[val])

        tk.Frame(mc, bg=BORDER, height=1).grid(row=2, column=0, columnspan=4,
                                               sticky="ew", padx=12, pady=(2, 6))

        tk.Label(mc, text="Local Proxy Ports", font=FH, bg=CARD, fg=FG2,
                 anchor="w").grid(row=3, column=0, columnspan=4,
                                  padx=12, pady=(0, 2), sticky="w")
        self._socks_var = tk.StringVar(value="10808")
        self._http_var  = tk.StringVar(value="10809")
        tk.Label(mc, text="SOCKS5:", font=FB, bg=CARD, fg=FG1, anchor="e").grid(
            row=4, column=0, padx=(12, 6), pady=5, sticky="e")
        _sp1 = ttk.Spinbox(mc, from_=1024, to=65535, textvariable=self._socks_var, width=8)
        _sp1.grid(row=4, column=1, padx=(0, 12), pady=5, sticky="w")
        _add_tooltip(_sp1, "Local SOCKS5 proxy port (e.g. 127.0.0.1:10808).")
        tk.Label(mc, text="HTTP:", font=FB, bg=CARD, fg=FG1, anchor="e").grid(
            row=4, column=2, padx=(12, 6), pady=5, sticky="e")
        _sp2 = ttk.Spinbox(mc, from_=1024, to=65535, textvariable=self._http_var, width=8)
        _sp2.grid(row=4, column=3, padx=(0, 12), pady=5, sticky="w")
        _add_tooltip(_sp2, "Local HTTP proxy port (e.g. 127.0.0.1:10809).")

        tk.Frame(mc, bg=BORDER, height=1).grid(row=5, column=0, columnspan=4,
                                               sticky="ew", padx=12, pady=(6, 6))

        self._tun_var = tk.BooleanVar(value=False)
        tun_cb = ttk.Checkbutton(
            mc,
            text="\U0001f6e1  TUN Mode \u2014 Full Tunnel (routes ALL apps: TCP + UDP)",
            variable=self._tun_var,
            command=self._on_tun_toggle)
        tun_cb.grid(row=6, column=0, columnspan=4, padx=12, pady=(0, 2), sticky="w")
        _add_tooltip(tun_cb,
            "Creates a WinTun virtual network adapter (same as WireGuard).\n"
            "ALL traffic from ALL processes is captured at the kernel level\n"
            "and routed through your VLESS config \u2014 browsers, games, UDP,\n"
            "raw-socket apps, everything.\n\n"
            "Requires: Administrator rights + wintun.dll\n"
            "(download in Settings \u2192 TUN / wintun)")
        self._tun_lbl = tk.Label(
            mc, text="", font=FS, bg=CARD, fg=FG3, anchor="w",
            justify="left", wraplength=760)
        self._tun_lbl.grid(row=7, column=0, columnspan=4, padx=12, pady=(0, 10), sticky="w")
        self._refresh_tun_label()

        # ---- Action buttons ------------------------------------------------
        bf = tk.Frame(pf, bg=BG); bf.grid(row=2, column=0, sticky="w", pady=(0, 8))
        self._px_start = _abtn(bf, "\u25b6  Connect", self._start_proxy)
        self._px_start.pack(side=tk.LEFT, padx=(0, 8))
        _add_tooltip(self._px_start,
                     "Start xray and route traffic through the selected config\n"
                     "using the chosen connection mode.")
        self._px_stop = _gbtn(bf, "\u23f9  Disconnect", self._stop_proxy)
        self._px_stop.pack(side=tk.LEFT, padx=(0, 8))
        _add_tooltip(self._px_stop, "Stop xray and tear down the proxy / TUN adapter.")
        self._px_stop.config(state=tk.DISABLED)
        self._test_conn_btn = _abtn(bf, "\U0001f50d Test Connection",
                                    self._test_connection, small=True, color=BLUE)
        self._test_conn_btn.pack(side=tk.LEFT)
        _add_tooltip(self._test_conn_btn,
                     "Run a one-shot latency + reachability test\n"
                     "on the active connection.")

        # ---- Live status card ----------------------------------------------
        sc2 = _card(pf); sc2.grid(row=3, column=0, sticky="nsew")
        sc2.columnconfigure(0, weight=1)

        self._px_status_lbl = tk.Label(
            sc2, text="\u25cf Disconnected", font=(FONT_FAMILY, 11, "bold"),
            bg=BG_CARD, fg=FG4, anchor="w", padx=12, pady=10)
        self._px_status_lbl.grid(row=0, column=0, sticky="ew")

        # metrics row: ping + test result (left)  |  bandwidth + legend (right)
        mrow = tk.Frame(sc2, bg=BG_CARD)
        mrow.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        tk.Label(mrow, text="Ping:", font=FB, bg=BG_CARD, fg=FG3).pack(side=tk.LEFT)
        self._lat_var = tk.StringVar(value="\u2014")
        tk.Label(mrow, textvariable=self._lat_var, font=(FONT_FAMILY, 10, "bold"),
                 bg=BG_CARD, fg=FG2).pack(side=tk.LEFT, padx=(4, 16))
        self._test_conn_result = tk.Label(mrow, text="", font=FS, bg=BG_CARD, fg=FG3)
        self._test_conn_result.pack(side=tk.LEFT)

        self._bw_open_btn = _gbtn(mrow, "\U0001f4c8 Bandwidth Graph",
                                  self._show_bw_dialog, True)
        self._bw_open_btn.pack(side=tk.RIGHT)
        _add_tooltip(self._bw_open_btn,
                     "Open a live upload/download bandwidth graph\n"
                     "in a separate window.")
        tk.Label(mrow, text="\u25cf DL", font=FS, bg=BG_CARD,
                 fg=GREEN).pack(side=tk.RIGHT, padx=(0, 10))
        tk.Label(mrow, text="\u25cf UL", font=FS, bg=BG_CARD,
                 fg=TEAL).pack(side=tk.RIGHT, padx=(0, 2))

        # usage numbers row (per-session config usage)
        bw_num_f = tk.Frame(sc2, bg=BG_CARD)
        bw_num_f.grid(row=2, column=0, sticky="ew", padx=12, pady=(2, 8))
        bw_num_f.columnconfigure(0, weight=1)
        bw_num_f.columnconfigure(1, weight=1)

        _ul_col = tk.Frame(bw_num_f, bg=BG_CARD)
        _ul_col.grid(row=0, column=0, sticky="w")
        tk.Label(_ul_col, text="\u2191 Upload", font=FS, bg=BG_CARD,
                 fg=TEAL, anchor="w").pack(anchor="w")
        self._ul_var = tk.StringVar(value="\u2014")
        tk.Label(_ul_col, textvariable=self._ul_var, font=(FONT_FAMILY, 14, "bold"),
                 bg=BG_CARD, fg=TEAL, anchor="w").pack(anchor="w")
        self._ul_spd_var = tk.StringVar(value="")
        tk.Label(_ul_col, textvariable=self._ul_spd_var, font=FS,
                 bg=BG_CARD, fg=FG4, anchor="w").pack(anchor="w")

        _dl_col = tk.Frame(bw_num_f, bg=BG_CARD)
        _dl_col.grid(row=0, column=1, sticky="w")
        tk.Label(_dl_col, text="\u2193 Download", font=FS, bg=BG_CARD,
                 fg=GREEN, anchor="w").pack(anchor="w")
        self._dl_var = tk.StringVar(value="\u2014")
        tk.Label(_dl_col, textvariable=self._dl_var, font=(FONT_FAMILY, 14, "bold"),
                 bg=BG_CARD, fg=GREEN, anchor="w").pack(anchor="w")
        self._dl_spd_var = tk.StringVar(value="")
        tk.Label(_dl_col, textvariable=self._dl_spd_var, font=FS,
                 bg=BG_CARD, fg=FG4, anchor="w").pack(anchor="w")

        # auto-switch status line
        self._switch_lbl = tk.Label(sc2, text="", font=FS, bg=BG_CARD,
                                    fg=FG3, padx=12, anchor="w")
        self._switch_lbl.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        self._refresh_connect_combo()

    def _refresh_connect_combo(self):
        p   = self.P
        ok  = [r for r in p.results if r.ping_ms is not None]
        labels: List[str] = []
        self._con_map: Dict[str, ProbeResult] = {}
        preferred = getattr(self, "_pref_connect", None)
        ordered   = ([preferred] + [r for r in ok
                      if not (preferred and r.ip==preferred.ip and r.port==preferred.port)]
                     if preferred else ok)
        for i,r in enumerate(ordered[:20], 1):
            ping_s   = f"{r.ping_ms:.0f}ms"         if r.ping_ms   else "—"
            jitter_s = f" jit:{r.jitter_ms:.0f}ms"   if r.jitter_ms else ""
            loss_s   = f" loss:{r.loss_pct:.0f}%"     if r.loss_pct  else ""
            colo_s   = f" [{r.colo}]"                 if r.colo      else ""
            lat_s    = f" lat:{r.lat_ms:.0f}ms"       if r.lat_ms    else ""
            dl_s     = f" dl:{r.dl_mbps:.1f}M"        if r.dl_mbps   else ""
            if p.has_config:
                lbl = f"Config {i} — {r.ip}:{r.port}  {ping_s}{jitter_s}{loss_s}{colo_s}{lat_s}{dl_s}"
            else:
                lbl = f"IP {i} — {r.ip}:{r.port}  {ping_s}{jitter_s}{loss_s}{colo_s}"
            labels.append(lbl)
            self._con_map[lbl] = r
        if not labels:
            labels = ["(no scan results — run scan + test first)"]
        self._con_cb.configure(values=labels)
        self._con_cb.current(0)

    def _load_connect(self, r: ProbeResult):
        self._pref_connect = r
        self._refresh_connect_combo()
        self._show("connect")

    def _start_proxy(self):
        if not self.xray.is_installed():
            self._px_status_lbl.config(
                text="✖  xray-core not installed — go to Settings → Xray Core to download.", fg=RED_C)
            return
        if not self.P.has_config:
            self._px_status_lbl.config(
                text="✖  Config not filled — go to Config tab and enter UUID + Host.", fg=RED_C)
            return

        sel = self._con_var.get()
        r   = self._con_map.get(sel)
        if r is None or "no scan results" in sel:
            self._px_status_lbl.config(
                text="✖  No config selected. Generate and test configs first.", fg=RED_C)
            return

        mode = self._conn_mode.get()
        p    = self.P
        sk   = int(self._socks_var.get())
        ht   = int(self._http_var.get())
        use_tun = self._tun_var.get()
        self._activity(f"Connect requested (mode={mode}, tun={use_tun})")

        if mode == "switch":
            self._start_auto_switch(sk, ht)
            return

        if mode == "auto":
            # pick best tested config
            ok = [r for r in p.results if r.ping_ms is not None and r.tested]
            if ok:
                ok.sort(key=lambda x: (x.lat_ms or 9999, x.ping_ms or 9999))
                r = ok[0]

        if use_tun:
            # ── TUN full-tunnel mode ─────────────────────────────────
            if not self.tun.is_supported():
                self._px_status_lbl.config(
                    text="✖  TUN mode is Windows-only.", fg=RED_C)
                return
            if not self.tun.is_admin():
                self._px_status_lbl.config(
                    text="✖  TUN mode needs Administrator rights.\n"
                         "    Right-click the app → Run as Administrator.",
                    fg=RED_C)
                messagebox.showerror(
                    "Administrator Required",
                    "TUN mode creates a kernel network adapter and requires\n"
                    "Administrator privileges.\n\n"
                    "Please restart the app as Administrator\n"
                    "(right-click → Run as Administrator).",
                    parent=self.root)
                return
            if not self.tun.is_dll_present():
                self._px_status_lbl.config(
                    text="✖  wintun.dll not found — go to Settings → TUN / wintun to download.",
                    fg=RED_C)
                return
            stats_port = XrayManager.get_free_port()
            cfg = XrayManager.build_tun(
                r.ip, r.port, p.uid, p.host, p.sni, p.path,
                profile=p,
                tun_name=TunManager.TUN_NAME,
                tun_addr=TunManager.TUN_ADDR4,
                tun_prefix=TunManager.TUN_PREFIX4,
                dns=TunManager.TUN_DNS,
                loglevel="info",
                stats_port=stats_port)
        else:
            stats_port = XrayManager.get_free_port()
            cfg = XrayManager.build_proxy(r.ip, r.port, p.uid, p.host, p.sni, p.path,
                                          sk, ht, profile=p, loglevel="info",
                                          stats_port=stats_port)

        proc = self.xray.start(cfg)
        if proc and proc.poll() is None:
            self._px_start.config(state=tk.DISABLED)
            self._px_stop.config(state=tk.NORMAL)
            if use_tun:
                status_text = (f"● TUN Connected → {r.ip}:{r.port}"
                               f"  🛡 FULL TUNNEL (all traffic)")
                self._tun_lbl.config(
                    text=f"✔  TUN adapter active — ALL connections are tunnelled.",
                    fg=GREEN)
                self.tun.mark_enabled(r.ip)
                # xray brings up the adapter asynchronously.
                # We must:
                #   1. Wait until the adapter actually appears in Windows
                #   2. Assign a static IP via netsh (xray leaves it with APIPA)
                #   3. Then add the OS-level routes
                # Without step 2 every 'route add' is silently dropped because
                # Windows has no route to gateway 198.18.0.1.
                _tun_r_ip    = r.ip          # capture for thread
                _tun_sp      = stats_port    # capture stats_port for thread
                def _add_routes():
                    name = TunManager.TUN_NAME
                    if not self.tun._wait_for_adapter(name, timeout=15.0):
                        self.q.put(("connlog",
                            "[TUN] ✖ Adapter did not appear within 15 s — "
                            "routes NOT installed.  Check wintun.dll and "
                            "Administrator rights."))
                        return
                    # Extra settle: adapter name appears in netsh before Windows
                    # fully accepts IP-configuration changes.  1.5 s is safe on
                    # fast systems and essential on slower / loaded ones.
                    time.sleep(1.5)
                    # Step 1: assign static IP — must confirm before routing.
                    self.q.put(("connlog", "[TUN] Assigning IP to adapter…"))
                    ip_ok = self.tun.setup_tun_adapter(
                        name, TunManager.TUN_ADDR4, TunManager.TUN_PREFIX4)
                    if not ip_ok:
                        self.q.put(("connlog",
                            "[TUN] ✖ Could not assign IP to adapter after 5 "
                            "attempts — routes NOT installed.  "
                            "Try: Run as Administrator."))
                        return
                    self.q.put(("connlog",
                        f"[TUN] ✔ IP {TunManager.TUN_ADDR4} confirmed on adapter."))
                    # Step 2: add split-default routes — now safe because the
                    # gateway (198.18.0.1) is on-link.
                    routes_ok = self.tun.setup_routes(TunManager.TUN_ADDR4)
                    if routes_ok:
                        self.q.put(("connlog",
                            f"[TUN] ✔ Routes active — full tunnel up "
                            f"(server={_tun_r_ip})"))
                        # TUN is now fully up — start traffic + latency monitor.
                        # Direct HTTP request will be tunnelled automatically.
                        self.q.put(("tun_start_bw", _tun_sp))
                    else:
                        self.q.put(("connlog",
                            f"[TUN] ⚠ Route install partially failed — "
                            f"traffic may not be fully tunnelled.  "
                            f"Check 'route print' as Administrator."))
                        # Start meter anyway (stats still work even without routes)
                        self.q.put(("tun_start_bw", _tun_sp))
                threading.Thread(target=_add_routes, daemon=True).start()
                proxy_url = None          # no local HTTP port in TUN mode
            else:
                status_text = f"● Connected → {r.ip}:{r.port}  SOCKS5 :{sk}  HTTP :{ht}"
                proxy_url = f"http://127.0.0.1:{ht}"
            self._bw_proxy_url  = proxy_url
            self._bw_stats_port = stats_port
            self._session_ul_bytes = 0
            self._session_dl_bytes = 0
            self._ul_var.set("0 B"); self._dl_var.set("0 B")
            self._ul_spd_var.set(""); self._dl_spd_var.set("")
            self._bw_hist_ul.clear(); self._bw_hist_dl.clear()
            self._draw_bw_chart()
            self._test_conn_result.config(text="", fg=FG2)
            if proxy_url:
                # SOCKS5/HTTP mode: start meter immediately with proxy URL
                self._start_bw_meter(proxy_url, stats_port=stats_port)
            # TUN mode meter is started via "tun_start_bw" queue message
            # after OS routes are confirmed active (see _add_routes thread).
            self._start_proxy_log_reader(proc)
            self._px_status_lbl.config(text=status_text, fg=GREEN)
            self._activity(f"Proxy connected (mode={mode}, tun={use_tun})")
            # Update status bar
            tun_tag = " TUN" if use_tun else ""
            self._sb_update(
                status=f"Connected{tun_tag}",
                color=GREEN,
                server=f"{r.ip}:{r.port}",
                ul="0 B", dl="0 B")
        else:
            self._px_status_lbl.config(
                text="\u2716  xray failed to start. Check Developer Log.", fg=RED_C)

    def _start_auto_switch(self, socks_port: int, http_port: int):
        p = self.P
        ok = [r for r in p.results if r.ping_ms is not None]
        if len(ok) < 2:
            self._px_status_lbl.config(
                text="✖  Need ≥2 scan results for auto-switch.", fg=RED_C)
            return
        ok.sort(key=lambda x: (x.lat_ms or 9999, x.ping_ms or 9999))
        self._switch_configs  = ok[:10]
        self._current_cfg_idx = 0
        self._auto_switch_stop.clear()
        self._px_start.config(state=tk.DISABLED)
        self._px_stop.config(state=tk.NORMAL)
        self._auto_switch_thread = threading.Thread(
            target=self._auto_switch_loop,
            args=(socks_port, http_port), daemon=True)
        self._auto_switch_thread.start()

    def _auto_switch_loop(self, sk: int, ht: int):
        p             = self.P
        idx           = 0
        MIN_HOLD      = 120   # seconds minimum stay on one config
        CHECK_IV      = 30    # seconds between health checks
        BAD_THRESHOLD = 2000  # ms — latency above this = "bad"
        MAX_CONSEC    = 3     # consecutive bad checks before switching

        while not self._auto_switch_stop.is_set():
            r   = self._switch_configs[idx % len(self._switch_configs)]
            cfg = XrayManager.build_proxy(
                r.ip, r.port, p.uid, p.host, p.sni, p.path,
                sk, ht, profile=p, loglevel="info")
            # stop previous xray fully before starting new one
            self.xray.stop()
            time.sleep(0.5)
            proc = self.xray.start(cfg)
            if proc is None or proc.poll() is not None:
                self.q.put(("connlog",
                    f"[AutoSwitch] Config {idx+1} failed — trying next"))
                idx += 1
                self._auto_switch_stop.wait(2)
                continue

            self.q.put(("connlog",
                f"[AutoSwitch] Connected → {r.ip}:{r.port}  SOCKS5:{sk} HTTP:{ht}"))
            self.q.put(("px_connected", r.ip, r.port, sk, ht))
            self._start_proxy_log_reader(proc)

            proxy_url  = f"http://127.0.0.1:{ht}"
            hold_until = time.time() + MIN_HOLD
            consec_bad = 0

            # warmup
            self._auto_switch_stop.wait(3)

            while not self._auto_switch_stop.is_set():
                self._auto_switch_stop.wait(CHECK_IV)
                if self._auto_switch_stop.is_set(): break

                # respect minimum hold time — don't thrash
                if time.time() < hold_until:
                    lat, err = XrayManager.latency(proxy_url)
                    self.q.put(("bw_lat",
                        f"{lat:.0f} ms" if lat is not None else "—"))
                    continue

                lat, err = XrayManager.latency(proxy_url)
                if lat is not None:
                    self.q.put(("bw_lat", f"{lat:.0f} ms"))
                if lat is None or lat > BAD_THRESHOLD:
                    consec_bad += 1
                    self.q.put(("connlog",
                        f"[AutoSwitch] Config {idx+1} bad check {consec_bad}/{MAX_CONSEC}"
                        f"  lat={lat}ms"))
                    if consec_bad >= MAX_CONSEC:
                        self.q.put(("connlog",
                            f"[AutoSwitch] Switching away from {r.ip}:{r.port}"))
                        idx += 1
                        break
                else:
                    consec_bad = 0   # reset on good check

        self.xray.stop()
        self.q.put(("px_disconnected",))

    def _stop_proxy(self):
        self._activity("Disconnect requested")
        # signal everything to stop first
        self._auto_switch_stop.set()
        self._bw_stop.set()
        self._proxy_log_stop.set()
        # Remove TUN routes BEFORE stopping xray (adapter must still be up for
        # route delete to succeed), then stop xray which removes the adapter.
        if self.tun.enabled:
            self.tun.teardown_routes(TunManager.TUN_ADDR4)
            self.tun.mark_disabled()
            try:
                self._tun_lbl.config(text="", fg=FG3)
            except Exception:
                pass
        # stop xray immediately (does force-kill internally)
        self.xray.stop()
        # join threads with timeout (non-blocking to UI because called from close handler)
        if self._auto_switch_thread and self._auto_switch_thread.is_alive():
            self._auto_switch_thread.join(timeout=3)
        self._auto_switch_thread = None
        if self._bw_thread and self._bw_thread.is_alive():
            self._bw_thread.join(timeout=2)
        self._bw_thread = None
        if self._proxy_log_thread and self._proxy_log_thread.is_alive():
            self._proxy_log_thread.join(timeout=1)
        self._proxy_log_thread = None
        # reset UI
        try:
            self._bw_proxy_url = None
            self._px_start.config(state=tk.NORMAL)
            self._px_stop.config(state=tk.DISABLED)
            self._px_status_lbl.config(text="● Disconnected", fg=FG3)
            self._switch_lbl.config(text="")
            self._ul_var.set("—"); self._dl_var.set("—"); self._lat_var.set("—")
            self._ul_spd_var.set(""); self._dl_spd_var.set("")
            self._bw_hist_ul.clear(); self._bw_hist_dl.clear()
            self._draw_bw_chart()
            self._test_conn_btn.config(state=tk.NORMAL, text="\U0001f50d Test Connection")
            self._test_conn_result.config(text="", fg=FG2)
        except Exception: pass
        # Update status bar
        self._sb_update(
            status="Disconnected",
            color=DISCONNECTED,
            server="",
            ul="\u2014", dl="\u2014", lat="\u2014")

    # ── Latency monitor + real traffic counter (xray stats API) ─────
    def _start_bw_meter(self, proxy_url, stats_port=None, tun_mode=False):
        self._stop_bw_meter()
        self._session_ul_bytes = 0
        self._session_dl_bytes = 0
        self.q.put(("bw_traffic", 0, 0))
        self._bw_stop.clear()
        self._bw_proxy_url  = proxy_url
        self._bw_stats_port = stats_port
        self._bw_thread = threading.Thread(
            target=self._bw_loop,
            args=(proxy_url, stats_port, tun_mode),
            daemon=True)
        self._bw_thread.start()

    def _show_bw_dialog(self):
        # Open (or focus) the live bandwidth graph in its own window.
        dlg = getattr(self, "_bw_dialog", None)
        if dlg is not None:
            try:
                if dlg.winfo_exists():
                    dlg.deiconify(); dlg.lift(); dlg.focus_force()
                    return
            except Exception:
                pass

        win = tk.Toplevel(self.root)
        win.title("Bandwidth Graph")
        win.configure(bg=BG_CARD)
        win.geometry("560x320")
        win.minsize(360, 220)
        try:
            win.transient(self.root)
        except Exception:
            pass

        header = tk.Frame(win, bg=BG_CARD)
        header.pack(fill=tk.X, padx=12, pady=(10, 4))
        tk.Label(header, text="Live Bandwidth", font=FH,
                 bg=BG_CARD, fg=FG2).pack(side=tk.LEFT)
        tk.Label(header, text="\u25cf UL", font=FS,
                 bg=BG_CARD, fg=TEAL).pack(side=tk.RIGHT, padx=(0, 2))
        tk.Label(header, text="\u25cf DL", font=FS,
                 bg=BG_CARD, fg=GREEN).pack(side=tk.RIGHT, padx=(0, 10))

        chart = tk.Canvas(win, bg="#0d1117", bd=0, highlightthickness=0)
        chart.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        chart.bind("<Configure>", lambda e: self._draw_bw_chart())

        self._bw_chart = chart
        self._bw_dialog = win

        def _close():
            self._bw_chart = None
            self._bw_dialog = None
            try:
                win.destroy()
            except Exception:
                pass

        win.protocol("WM_DELETE_WINDOW", _close)
        self._activity("Opened bandwidth graph")
        # initial paint (after the window has a real size)
        self.root.after(60, self._draw_bw_chart)

    def _draw_bw_chart(self):
        import math as _math
        c = getattr(self, "_bw_chart", None)
        # Chart only exists while the Bandwidth Graph dialog is open.
        if c is None:
            return
        try:
            if not c.winfo_exists():
                self._bw_chart = None
                return
        except Exception:
            self._bw_chart = None
            return
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 20 or h < 20:
            return

        _BG   = "#121316"
        _GRID = "#26272c"
        _LAB  = "#3a3a42"
        PAD_L, PAD_R, PAD_T, PAD_B = 46, 8, 8, 20

        c.delete("all")
        # background
        c.create_rectangle(0, 0, w, h, fill=_BG, outline="")

        plot_w = w - PAD_L - PAD_R
        plot_h = h - PAD_T - PAD_B
        N      = 60  # total history window (seconds)

        hist_ul = list(self._bw_hist_ul)
        hist_dl = list(self._bw_hist_dl)

        # Auto-scale Y to the max visible value, rounded to a nice ceiling
        all_vals = hist_ul + hist_dl
        max_val  = max(all_vals) if all_vals else 1.0
        if max_val <= 0: max_val = 1.0
        mag  = 10 ** _math.floor(_math.log10(max_val))
        ceil = _math.ceil(max_val / mag) * mag * 1.1   # 10% headroom

        # ── Horizontal grid lines + Y labels ──────────────────────────
        for pct in (0.25, 0.5, 0.75, 1.0):
            y = PAD_T + int(plot_h * (1 - pct))
            c.create_line(PAD_L, y, w - PAD_R, y,
                          fill=_GRID, dash=(2, 5))
            c.create_text(PAD_L - 4, y, anchor="e",
                          text=_fmt_speed(ceil * pct),
                          font=("Segoe UI", 7), fill=_LAB)

        # ── Vertical time-marks (every 15 s) ──────────────────────────
        for sec in (15, 30, 45):
            x = PAD_L + int(plot_w * (N - sec) / N)
            c.create_line(x, PAD_T, x, h - PAD_B,
                          fill=_GRID, dash=(2, 6))
            c.create_text(x, h - PAD_B + 3, anchor="n",
                          text=f"-{sec}s",
                          font=("Segoe UI", 7), fill=_LAB)

        # ── Plot a history list as a polyline ──────────────────────────
        def _plot(hist, color):
            if len(hist) < 2:
                return
            n_hist = len(hist)
            pts = []
            for i, val in enumerate(hist):
                x = PAD_L + int(plot_w * (N - n_hist + i) / N)
                y = PAD_T + plot_h - int(plot_h * min(val, ceil) / ceil)
                pts.extend((x, y))
            if len(pts) >= 4:
                c.create_line(*pts, fill=color, width=2, smooth=True)

        _plot(hist_ul, TEAL)
        _plot(hist_dl, GREEN)

        # ── Border ────────────────────────────────────────────────────
        c.create_rectangle(PAD_L, PAD_T, w - PAD_R, h - PAD_B,
                           outline=_GRID)

    def _stop_bw_meter(self):
        self._bw_stop.set()
        if self._bw_thread and self._bw_thread.is_alive():
            self._bw_thread.join(timeout=2)
        self._bw_thread = None

    def _bw_loop(self, proxy_url, stats_port=None, tun_mode=False):
        _tick       = 0
        _prev_ul    = 0
        _prev_dl    = 0
        _prev_time  = time.monotonic()

        while not self._bw_stop.is_set():

            # ── Traffic: every tick (1 s) ──────────────────────────────
            if stats_port:
                try:
                    ul, dl = self.xray.query_stats(stats_port)
                    now    = time.monotonic()
                    dt     = now - _prev_time or 1.0   # avoid div-by-zero
                    ul_spd = max(0, ul - _prev_ul) / dt
                    dl_spd = max(0, dl - _prev_dl) / dt
                    _prev_ul   = ul
                    _prev_dl   = dl
                    _prev_time = now
                    self.q.put(("bw_traffic", ul, dl, ul_spd, dl_spd))
                except Exception:
                    pass

            # ── Latency: every 30th tick (≈ 30 s) ─────────────────────
            if _tick % 30 == 0:
                try:
                    if tun_mode:
                        lat, err = XrayManager.latency_direct()
                    elif proxy_url:
                        lat, err = XrayManager.latency(proxy_url)
                    else:
                        lat, err = None, "no proxy"
                    if lat is not None:
                        self.q.put(("bw_lat", f"{lat:.0f} ms"))
                    else:
                        self.q.put(("bw_lat", f"— ({err or 'timeout'})"))
                except Exception:
                    self.q.put(("bw_lat", "—"))

            _tick += 1
            self._bw_stop.wait(1)   # 1-second poll — feels real-time

    # ── Test Connection (user-triggered one-shot speed test) ───────
    def _test_connection(self):
        proxy_url = getattr(self, "_bw_proxy_url", None)
        if not proxy_url:
            self._test_conn_result.config(
                text="Not connected.", fg=RED_C); return
        self._test_conn_btn.config(state=tk.DISABLED, text="Testing…")
        self._test_conn_result.config(text="Running…", fg=ORANGE)
        def _run():
            results: List[str] = []
            ul_bytes = dl_bytes = 0
            # 1. Latency
            lat, err = XrayManager.latency(proxy_url)
            if lat is not None:
                results.append(f"Latency: {lat:.0f} ms")
                ul_bytes += 250; dl_bytes += 204
            else:
                results.append(f"Latency: timeout ({err})")

            # 2. Download speed (3 MB)
            try:
                h  = urllib.request.ProxyHandler(
                    {"http": proxy_url, "https": proxy_url})
                op = urllib.request.build_opener(h)
                req = urllib.request.Request(
                    "https://speed.cloudflare.com/__down?bytes=3000000",
                    headers={"User-Agent": "Mozilla/5.0"})
                t0 = time.perf_counter()
                with op.open(req, timeout=30) as r:
                    data = r.read()
                el = time.perf_counter() - t0
                dl_bytes += len(data)
                mbps = (len(data) * 8) / (el * 1_000_000) if el > 0 else 0
                results.append(f"Download: {mbps:.2f} Mbps  ({len(data)//1024} KB in {el:.1f}s)")
            except Exception as e:
                results.append(f"Download: timeout ({e})")

            # 3. Upload speed (500 KB)
            try:
                payload = b"x" * 500_000
                req2 = urllib.request.Request(
                    "https://speed.cloudflare.com/__up",
                    data=payload,
                    headers={"User-Agent": "Mozilla/5.0",
                             "Content-Type": "application/octet-stream"})
                t0 = time.perf_counter()
                with op.open(req2, timeout=20) as r: r.read()
                el2 = time.perf_counter() - t0
                ul_bytes += len(payload)
                up_mbps = (len(payload) * 8) / (el2 * 1_000_000) if el2 > 0 else 0
                results.append(f"Upload:   {up_mbps:.2f} Mbps  ({len(payload)//1024} KB in {el2:.1f}s)")
            except Exception as e:
                results.append(f"Upload:   timeout ({e})")

            # accumulate into session totals
            self._session_ul_bytes = getattr(self, "_session_ul_bytes", 0) + ul_bytes
            self._session_dl_bytes = getattr(self, "_session_dl_bytes", 0) + dl_bytes
            self.q.put(("bw_traffic", self._session_ul_bytes, self._session_dl_bytes))
            self.q.put(("bw_lat", f"{lat:.0f} ms" if lat else "—"))
            summary = "  |  ".join(results)
            self.q.put(("test_conn_result", summary, True if lat else False))

        threading.Thread(target=_run, daemon=True).start()

    # ── Proxy log reader ──────────────────────────────────────────
    def _start_proxy_log_reader(self, proc: subprocess.Popen):
        self._stop_proxy_log()
        self._proxy_log_stop.clear()
        self._proxy_log_thread = threading.Thread(
            target=self._proxy_log_loop, args=(proc,), daemon=True)
        self._proxy_log_thread.start()

    def _stop_proxy_log(self):
        self._proxy_log_stop.set()
        if self._proxy_log_thread and self._proxy_log_thread.is_alive():
            self._proxy_log_thread.join(timeout=1)
        self._proxy_log_thread = None

    def _proxy_log_loop(self, proc: subprocess.Popen):
        try:
            stream = proc.stdout
            if stream is None: return

            # Allow MAX_LINES per WINDOW_SEC; excess lines are counted and
            # a single suppression notice is emitted at the next window reset.
            MAX_LINES   = 10          # max lines forwarded per burst window
            WINDOW_SEC  = 0.5         # burst window duration in seconds
            _win_start  = time.time()
            _win_count  = 0
            _suppressed = 0

            while not self._proxy_log_stop.is_set():
                line = stream.readline()
                if not line:
                    if proc.poll() is not None: break
                    continue
                text = line.decode(errors="replace").rstrip()
                if not text:
                    continue

                now = time.time()
                if now - _win_start > WINDOW_SEC:
                    # new burst window — flush suppression counter
                    if _suppressed:
                        self.q.put(("connlog",
                            f"[… {_suppressed} lines suppressed — "
                            f"log storm detected]"))
                    _win_count  = 0
                    _win_start  = now
                    _suppressed = 0

                if _win_count < MAX_LINES:
                    self.q.put(("connlog", text))
                    _win_count += 1
                else:
                    _suppressed += 1

        except Exception as ex:
            self.q.put(("connlog", f"[LogReader stopped: {ex}]"))

    # ══════════════════════════════════════════════════════
    #  Connection Log tab
    # ══════════════════════════════════════════════════════

    def _build_connlog(self):
        lf = self.pages["connlog"]
        lf.rowconfigure(1, weight=1)
        top = tk.Frame(lf, bg=BG); top.grid(row=0, column=0, sticky="w", pady=(0,6))
        _gbtn(top, "Clear", self._clear_connlog, True).pack(side=tk.LEFT, padx=(0,6))
        _gbtn(top, "Save", self._save_connlog, True).pack(side=tk.LEFT)
        tk.Label(top, text="Live V2Ray-style xray proxy log",
                 font=FS, bg=BG, fg=FG3).pack(side=tk.LEFT, padx=10)

        self._connlog_text = tk.Text(lf, wrap="word", state="disabled", height=10,
                                     bg="#0d1117", fg="#c0caf5",
                                     font=FM, relief="flat", bd=0,
                                     insertbackground="#c0caf5",
                                     selectbackground=ACCENT,
                                     padx=8, pady=4)
        self._connlog_text.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        vsb = ttk.Scrollbar(lf, orient="vertical", command=self._connlog_text.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self._connlog_text.configure(yscrollcommand=vsb.set)
        # color tags
        self._connlog_text.tag_configure("info",  foreground="#c0caf5")
        self._connlog_text.tag_configure("warn",  foreground=ORANGE)
        self._connlog_text.tag_configure("error", foreground=RED_C)
        self._connlog_text.tag_configure("ok",    foreground=GREEN)

    def _append_connlog(self, line: str):
        self._connlog_text.configure(state="normal")
        ts = time.strftime("%H:%M:%S")
        text = f"[{ts}] {line}\n"
        tag = "info"
        lo = line.lower()
        if "error" in lo or "fail" in lo or "✖" in lo: tag = "error"
        elif "warn" in lo: tag = "warn"
        elif "connect" in lo or "✔" in lo or "ok" in lo: tag = "ok"
        self._connlog_text.insert(tk.END, text, tag)
        self._connlog_text.see(tk.END)
        self._connlog_text.configure(state="disabled")

    def _clear_connlog(self):
        self._connlog_text.configure(state="normal")
        self._connlog_text.delete("1.0", tk.END)
        self._connlog_text.configure(state="disabled")

    def _save_connlog(self):
        p = filedialog.asksaveasfilename(defaultextension=".log",
            filetypes=[("Log","*.log"),("All","*.*")])
        if p:
            content = self._connlog_text.get("1.0", tk.END)
            with open(p, "w", encoding="utf-8") as f: f.write(content)

    # ══════════════════════════════════════════════════════
    #  Settings tab
    # ══════════════════════════════════════════════════════

    def _build_settings(self):
        sf = self.pages["settings"]
        sf.rowconfigure(0, weight=1)
        scroll = SF(sf, bg=BG)
        scroll.grid(row=0, column=0, sticky="nsew")
        p = scroll.inner

        def section(title):
            tk.Label(p, text=title, font=FH, bg=BG, fg=FG2).pack(
                anchor="w", pady=(12, 2), padx=2)
            c = _card(p); c.pack(fill=tk.X, pady=(0,6), padx=2)
            c.columnconfigure(1, weight=1)
            return c

        # ── Xray Core ──────────────────────────────────────────────
        xc = section("Xray Core")
        tk.Label(xc, text="Status:", font=FB, bg=BG_CARD, fg=FG2,
                 width=16, anchor="w").grid(row=0, column=0, padx=(12,4), pady=8, sticky="w")
        self._set_xray_lbl = tk.Label(xc, font=FB, bg=BG_CARD, fg=FG2,
                                       text="Checking\u2026", anchor="w")
        self._set_xray_lbl.grid(row=0, column=1, sticky="ew", padx=(0,4), pady=8)
        self._set_xray_prog = ttk.Progressbar(xc, mode="indeterminate", length=110)
        self._set_xray_prog.grid(row=0, column=2, padx=4, pady=8)
        self._set_xray_dl_btn = _abtn(xc, "⬇ Download Xray Core",
                                       self._dl_xray_settings, color=BLUE)
        self._set_xray_dl_btn.grid(row=0, column=3, padx=(0,12), pady=8)

        tk.Label(xc, text="Custom path:", font=FB, bg=BG_CARD, fg=FG2,
                 width=16, anchor="w").grid(row=1, column=0, padx=(12,4), pady=6, sticky="w")
        self._xray_path_var = tk.StringVar(value=self.xray.xray_path)
        ttk.Entry(xc, textvariable=self._xray_path_var, state="readonly").grid(
            row=1, column=1, sticky="ew", padx=(0,4), pady=6)
        _gbtn(xc, "Browse", self._browse_xray, True).grid(
            row=1, column=2, columnspan=2, padx=(0,12), pady=6)

        if self.xray.is_installed():
            self._set_xray_lbl.config(text=f"✔  {self.xray.xray_path}", fg=GREEN)
            self._set_xray_dl_btn.grid_remove()
            self._set_xray_prog.grid_remove()
        else:
            self._set_xray_lbl.config(text="✖  Not found — click Download", fg=RED_C)
            self._set_xray_prog.grid_remove()

        # ── TUN / wintun ───────────────────────────────────────────
        vc = section("TUN Mode  —  Full Tunnel  (wintun.dll)")
        vc.columnconfigure(1, weight=1)

        # status row
        tk.Label(vc, text="wintun.dll:", font=FB, bg=BG_CARD, fg=FG2,
                 width=16, anchor="w").grid(row=0, column=0, padx=(12,4), pady=8, sticky="w")
        self._tun_dll_lbl = tk.Label(vc, font=FB, bg=BG_CARD, fg=FG2,
                                     text="Checking\u2026", anchor="w")
        self._tun_dll_lbl.grid(row=0, column=1, sticky="ew", padx=(0,4), pady=8)
        self._tun_dl_prog = ttk.Progressbar(vc, mode="indeterminate", length=110)
        self._tun_dl_prog.grid(row=0, column=2, padx=4, pady=8)
        self._tun_dl_btn  = _abtn(vc, "⬇ Download wintun.dll",
                                   self._dl_wintun_settings, color=BLUE)
        self._tun_dl_btn.grid(row=0, column=3, padx=(0,12), pady=8)

        # admin status row
        tk.Label(vc, text="Admin rights:", font=FB, bg=BG_CARD, fg=FG2,
                 width=16, anchor="w").grid(row=1, column=0, padx=(12,4), pady=6, sticky="w")
        is_admin = self.tun.is_admin()
        adm_text = "\u2714  Running as Administrator" if is_admin else \
                   "\u2716  Not Administrator \u2014 TUN mode will be blocked at connect time"
        tk.Label(vc, text=adm_text, font=FB, bg=BG_CARD,
                 fg=GREEN if is_admin else ORANGE, anchor="w").grid(
            row=1, column=1, columnspan=3, sticky="ew", padx=(0,12), pady=6)

        # explanation
        tk.Label(vc,
                 text="TUN mode creates a WinTun virtual network adapter (same driver as WireGuard).\n"
                      "ALL traffic from ALL processes \u2014 browsers, games, UDP, raw sockets \u2014 is\n"
                      "captured at the kernel level and routed through your VLESS config.\n\n"
                      "\u2022 wintun.dll must be present (download above, placed next to xray.exe)\n"
                      "\u2022 The app must be run as Administrator\n"
                      "\u2022 xray automatically creates + removes the adapter on connect / disconnect\n"
                      "\u2022 No drivers to install, no system changes left behind after disconnect",
                 font=FS, bg=BG_CARD, fg=FG3, justify="left",
                 padx=12, pady=4).grid(row=2, column=0, columnspan=4, sticky="w")

        # refresh dll label now
        if self.tun.is_dll_present():
            self._tun_dll_lbl.config(text=f"✔  {self.tun.dll_path}", fg=GREEN)
            self._tun_dl_btn.grid_remove()
            self._tun_dl_prog.grid_remove()
        else:
            self._tun_dll_lbl.config(
                text="✖  Not found — click Download", fg=RED_C)
            self._tun_dl_prog.grid_remove()

        # ── Scan defaults ──────────────────────────────────────────
        dc = section("Scan Defaults")
        dc.columnconfigure(1, weight=1); dc.columnconfigure(3, weight=1)

        tk.Label(dc, text="Default threads:", font=FB, bg=BG_CARD, fg=FG2,
                 width=18, anchor="w").grid(row=0, column=0, padx=(12,4), pady=6, sticky="w")
        self._def_threads = tk.StringVar(value="200")
        ttk.Spinbox(dc, from_=10, to=2000, textvariable=self._def_threads,
                    width=8).grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(dc, text="Default timeout (s):", font=FB, bg=BG_CARD, fg=FG2,
                 anchor="w").grid(row=0, column=2, padx=(12,4), pady=6, sticky="w")
        self._def_timeout = tk.StringVar(value="5.0")
        ttk.Spinbox(dc, from_=1, to=30, increment=0.5,
                    textvariable=self._def_timeout, width=8).grid(
            row=0, column=3, sticky="w", padx=(0,12), pady=6)

        # ── About / version ────────────────────────────────────────
        # -- Appearance ----------------------------------------------------
        apc = section("Appearance")
        tk.Label(apc, text="Theme:", font=FB, bg=BG_CARD, fg=FG2,
                 width=16, anchor="w").grid(row=0, column=0, padx=(12,4),
                                            pady=8, sticky="w")
        self._theme_lbl = tk.Label(
            apc, font=FB, bg=BG_CARD, fg=FG2, anchor="w",
            text=("Dark mode" if get_theme() == "dark" else "Light mode"))
        self._theme_lbl.grid(row=0, column=1, sticky="w", pady=8)
        _abtn(apc, "Toggle Dark / Light", self._toggle_theme,
              small=True, color=BLUE).grid(row=0, column=2,
                                           padx=(0,12), pady=8, sticky="e")

        ac = section("App")
        tk.Label(ac, text="VLESS Edge Optimizer ver 4.5  \u00b7  brand: VEO",
                 font=FB, bg=BG_CARD, fg=FG3, padx=12, pady=8).pack(anchor="w")

    def _dl_xray_settings(self):
        self._set_xray_lbl.config(text="Downloading…", fg=ORANGE)
        self._set_xray_dl_btn.config(state=tk.DISABLED)
        self._set_xray_prog.grid()
        self._set_xray_prog.start(12)
        def run():
            ok = self.xray.download(lambda m: self.q.put(("xray_prog_set", m)))
            self.q.put(("xray_done_set", ok))
        threading.Thread(target=run, daemon=True).start()

    def _dl_wintun_settings(self):
        self._tun_dll_lbl.config(text="Downloading…", fg=ORANGE)
        self._tun_dl_btn.config(state=tk.DISABLED)
        self._tun_dl_prog.grid()
        self._tun_dl_prog.start(12)
        def run():
            ok, msg = self.tun.download_wintun(
                lambda m: self.q.put(("tun_prog", m)))
            self.q.put(("tun_done", ok, msg))
        threading.Thread(target=run, daemon=True).start()

    def _refresh_tun_label(self):
        try:
            lbl = self._tun_lbl
        except AttributeError:
            return
        if not self.tun.is_supported():
            lbl.config(
                text="ℹ  TUN mode is Windows-only.  On Linux/macOS xray also supports\n"
                     "    TUN but setup is manual — see xray docs.",
                fg=ORANGE)
            return
        if not self.tun.is_dll_present():
            lbl.config(
                text="⚠  wintun.dll missing — go to Settings → TUN / wintun to download.",
                fg=ORANGE)
            return
        if not self.tun.is_admin():
            lbl.config(
                text="⚠  Not running as Administrator — TUN mode will fail at connect time.\n"
                     "    Right-click the .pyw / shortcut → Run as Administrator.",
                fg=ORANGE)
            return
        lbl.config(
            text="✔  Ready — wintun.dll found, running as Administrator.",
            fg=GREEN)

    def _on_tun_toggle(self):
        try:
            self._activity(f"TUN mode {'enabled' if self._tun_var.get() else 'disabled'}")
        except Exception:
            pass
        self._refresh_tun_label()

    def _browse_xray(self):
        p = filedialog.askopenfilename(
            title="Select xray binary",
            filetypes=[("Executable","*.exe"), ("All","*")])
        if p:
            self.xray.xray_path = p
            self._xray_path_var.set(p)
            self._set_xray_lbl.config(text=f"✔  {p}", fg=GREEN)
            self._set_xray_dl_btn.grid_remove()

    def _open_ncpa(self):
        try:
            if sys.platform == "win32":
                subprocess.Popen("ncpa.cpl", shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open","/System/Library/PreferencePanes/Network.prefPane"])
            else:
                subprocess.Popen(["nm-connection-editor"])
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # ══════════════════════════════════════════════════════
    #  History tab
    # ══════════════════════════════════════════════════════

    def _load_history_entry(self):
        try:
            labels = list(self._hist_combo["values"])
            sel    = self._hist_var.get()
            if sel not in labels or sel.startswith("\u2014"): return
            idx    = labels.index(sel)
            e      = self.P.scan_history[idx]
            results= [ProbeResult.from_dict(r) for r in e.get("results",[])]
            self.P.results       = results
            self.P.built_configs = []
            self.P.scanned       = e.get("scanned", len(results))
            self.P.scan_time     = e.get("time", "")
            self.P.range_name    = e.get("range_name", "")
            # Use the actual verified count from the scan, not len(results)
            self.P.passed_count  = e.get("found", len(results))
            for i in self._test_tree.get_children(): self._test_tree.delete(i)
            self._sr_limit = 9999
            self._refresh_scanresult()
            self._refresh_home()
            self._refresh_test_tree()
            self._refresh_pool_count()
            self._refresh_connect_combo()
            self._update_tab_states()
            self._show("test")
            messagebox.showinfo("Loaded",
                f"Loaded {self.P.passed_count} verified IPs from {e.get('time','')}.",
                parent=self.root)
        except Exception as ex:
            messagebox.showerror("Load Error", str(ex), parent=self.root)

    def _delete_history_entry(self):
        try:
            sel = self._hist_var.get()
            if not sel or sel.startswith("\u2014"): return
            if not messagebox.askyesno("Delete", "Delete this scan history entry?",
                                       parent=self.root): return
            # Get current labels list
            labels = list(self._hist_combo["values"])
            if sel not in labels: return
            idx = labels.index(sel)
            # Verify index is valid
            if idx < 0 or idx >= len(self.P.scan_history):
                self._logui(f"[HISTORY] Invalid index {idx}")
                return
            # Remove the entry
            removed = self.P.scan_history.pop(idx)
            self._logui(f"[HISTORY] Removed: {removed.get('time','?')} {removed.get('range_name','?')}")
            # Save to disk
            save_profiles(self.profiles, self._prof_idx)
            # Refresh the combo
            self._refresh_history_combo()
            self._logui(f"[HISTORY] Deleted entry #{idx+1}, {len(self.P.scan_history)} remaining")
        except Exception as ex:
            self._logui(f"[HISTORY] Delete error: {ex}")

    def _build_history(self):
        hf = self.pages["history"]
        hf.rowconfigure(0, weight=0)   # only the list area (row 1) stretches
        hf.rowconfigure(1, weight=1)

        top = tk.Frame(hf, bg=BG); top.grid(row=0, column=0, sticky="w", pady=(0,6))
        _abtn(top, "⟳ Refresh", self._refresh_history, True).pack(side=tk.LEFT)
        _gbtn(top,  "🗑 Clear All", self._clear_history, True).pack(side=tk.LEFT, padx=(6,0))
        tk.Label(top,
                 text="Each scan is saved here automatically.",
                 font=FS, bg=BG, fg=FG3).pack(side=tk.LEFT, padx=10)

        self._hist_sf = SF(hf, bg=BG)
        self._hist_sf.grid(row=1, column=0, sticky="nsew")
        self._refresh_history()

    def _refresh_history(self):
        self._hist_sf.clear()
        p     = self.P
        inner = self._hist_sf.inner

        if not p.scan_history:
            tk.Label(inner, text="No scan history yet. Run a scan to record it here.",
                     font=FB, bg=BG, fg=FG3).pack(pady=30)
            return

        for idx, entry in enumerate(p.scan_history):
            self._history_card(inner, entry, idx)

    def _history_card(self, parent, entry: dict, idx: int):
        results = [ProbeResult.from_dict(r) for r in entry.get("results", [])]
        card = _card(parent); card.pack(fill=tk.X, pady=4, padx=2)
        tk.Frame(card, bg=BLUE, width=5).pack(side=tk.LEFT, fill=tk.Y)

        inner = tk.Frame(card, bg=CARD)
        inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
        inner.columnconfigure(1, weight=1)

        # Header row
        hf = tk.Frame(inner, bg=CARD); hf.pack(fill=tk.X)
        tk.Label(hf,
                 text=f"#{len(self.P.scan_history)-idx}  {entry.get('time','')}",
                 font=FH, bg=CARD, fg=FG1).pack(side=tk.LEFT)
        tk.Label(hf,
                 text=f"  ·  {entry.get('range_name','')}  ·  {entry.get('mode','').upper()}",
                 font=FS, bg=CARD, fg=FG3).pack(side=tk.LEFT)
        _hh = (entry.get("host", "") or "").strip()
        if _hh:
            tk.Label(hf, text=f"  ·  ⟨{_hh}⟩",
                     font=FS, bg=CARD, fg=TEAL).pack(side=tk.LEFT)

        # Stats row
        sf = tk.Frame(inner, bg=CARD); sf.pack(fill=tk.X)
        for lbl, val, col in [
            ("Scanned", str(entry.get("scanned",0)), BLUE),
            ("Found",   str(entry.get("found",0)),   GREEN),
        ]:
            tk.Label(sf, text=f" {lbl}: ", font=FS, bg=CARD, fg=FG3).pack(side=tk.LEFT)
            tk.Label(sf, text=val, font=("Segoe UI",9,"bold"),
                     bg=CARD, fg=col).pack(side=tk.LEFT)
        tk.Label(sf, text=f"  Range: {entry.get('range_raw','')[:50]}",
                 font=FS, bg=CARD, fg=FG3).pack(side=tk.LEFT)

        # Expandable top results
        expand_var = tk.BooleanVar(value=False)
        result_frame = tk.Frame(inner, bg=CARD)

        def toggle(ef=result_frame, ev=expand_var, rs=results, e=entry):
            if ev.get():
                ef.pack(fill=tk.X, pady=(4,0))
                for w in ef.winfo_children(): w.destroy()
                for i, r in enumerate(rs[:5], 1):
                    rf = tk.Frame(ef, bg=CARD); rf.pack(fill=tk.X, pady=1)
                    ping_c = _ping_color(r.ping_ms)
                    tk.Label(rf, text=f"  #{i} {r.ip}:{r.port}",
                             font=FB, bg=CARD, fg=FG1, width=24, anchor="w").pack(side=tk.LEFT)
                    tk.Label(rf, text=_ping_label(r.ping_ms),
                             font=("Segoe UI",9,"bold"), bg=CARD, fg=ping_c).pack(side=tk.LEFT)
                    tk.Label(rf, text=f"  colo:{r.colo or '—'}",
                             font=FS, bg=CARD, fg=FG3).pack(side=tk.LEFT)
                    if self.P.has_config:
                        url = self._vless(r.ip, r.port)
                        _ilbl(rf, "🔗", lambda u=url, n=f"Config #{i}":
                              self._copy_with_toast(u, n), bg=CARD, sz=12).pack(side=tk.LEFT, padx=4)
                show_more = tk.Button(ef, text=f"Show all {len(rs)} results…",
                                      font=FS, bg=CARD, fg=BLUE, relief="flat",
                                      cursor="hand2",
                                      command=lambda ef2=ef, rs2=rs:
                                      self._show_all_history_results(ef2, rs2))
                if len(rs) > 5: show_more.pack(anchor="w", padx=4)
            else:
                ef.pack_forget()

        expand_var.trace_add("write", lambda *_: toggle())

        bf = tk.Frame(card, bg=CARD); bf.pack(side=tk.RIGHT, padx=8)
        ttk.Checkbutton(bf, text="Show", variable=expand_var).pack()

        # Load button — load this history entry's results into current profile
        def load_entry(rs=results, e=entry):
            self.P.results    = rs
            self.P.scanned    = e.get("scanned", len(rs))
            self.P.scan_time  = e.get("time", "")
            self.P.range_name = e.get("range_name", "")
            self._sr_limit    = 5
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_connect_combo()
            self._update_tab_states()
            messagebox.showinfo("Loaded",
                f"Loaded {len(rs)} results from scan on {e.get('time','')}.",
                parent=self.root)
            self._show("test")   # go to combined Test & Results tab

        _abtn(bf, "Load →", load_entry, small=True, color=TEAL).pack(pady=(4,0))

    def _show_all_history_results(self, frame, results):
        for w in frame.winfo_children(): w.destroy()
        for i, r in enumerate(results, 1):
            rf = tk.Frame(frame, bg=CARD); rf.pack(fill=tk.X, pady=1)
            tk.Label(rf, text=f"  #{i} {r.ip}:{r.port}",
                     font=FB, bg=CARD, fg=FG1, width=24, anchor="w").pack(side=tk.LEFT)
            tk.Label(rf, text=_ping_label(r.ping_ms),
                     font=("Segoe UI",9,"bold"),
                     bg=CARD, fg=_ping_color(r.ping_ms)).pack(side=tk.LEFT)
            tk.Label(rf, text=f"  colo:{r.colo or '—'}",
                     font=FS, bg=CARD, fg=FG3).pack(side=tk.LEFT)
            # Action buttons — same set as the first-5 block
            if self.P.has_config:
                url  = self._vless(r.ip, r.port)
                name = f"Config #{i} — {r.ip}:{r.port}"
                lnk = _ilbl(rf, "🔗", lambda u=url, n=name: self._copy_with_toast(u, n), bg=CARD, sz=12)
                lnk.pack(side=tk.LEFT, padx=3)
                _add_tooltip(lnk, "Copy config link")
                qrl = _ilbl(rf, "📷", lambda u=url, n=name: show_qr(self.root, u, n), bg=CARD, sz=12)
                qrl.pack(side=tk.LEFT, padx=3)
                _add_tooltip(qrl, "Show QR code")
                star = _ilbl(rf, "⭐", lambda u=url, n=name: self._add_favorite(u, n), bg=CARD, sz=12)
                star.pack(side=tk.LEFT, padx=3)
                _add_tooltip(star, "Add to Favorites")
            conl = _ilbl(rf, "🌐", lambda rr=r: self._load_connect(rr), bg=CARD, sz=12)
            conl.pack(side=tk.LEFT, padx=3)
            _add_tooltip(conl, "Load into Connect tab")

    def _clear_history(self):
        if messagebox.askyesno("Clear History",
                "Clear all scan history for this profile?", parent=self.root):
            self.P.scan_history = []
            save_profiles(self.profiles, self._prof_idx)
            try: self._refresh_history_combo()
            except Exception: pass

    # ══════════════════════════════════════════════════════
    #  Favorites tab
    # ══════════════════════════════════════════════════════

    def _build_favorites(self):
        ff = self.pages["favorites"]
        ff.rowconfigure(1, weight=1)

        top = tk.Frame(ff, bg=BG); top.grid(row=0, column=0, sticky="w", pady=(0,6))
        _abtn(top, "+ Add Manually", self._add_fav_manual, True, TEAL).pack(side=tk.LEFT)
        _gbtn(top, "⟳ Refresh",     self._refresh_favorites, True).pack(side=tk.LEFT, padx=6)
        tk.Label(top, text="Star any config card to save it here.",
                 font=FS, bg=BG, fg=FG3).pack(side=tk.LEFT, padx=10)

        self._fav_sf = SF(ff, bg=BG)
        self._fav_sf.grid(row=1, column=0, sticky="nsew")
        self._refresh_favorites()

    def _refresh_favorites(self):
        self._fav_sf.clear()
        inner = self._fav_sf.inner
        favs  = self.P.favorites
        if not favs:
            tk.Label(inner,
                     text="No favorites yet.\nStar a config from the Results tab to save it here.",
                     font=FB, bg=BG, fg=FG3, justify="center").pack(pady=30)
            return
        for i, fav in enumerate(favs):
            self._fav_card(inner, fav, i)

    def _fav_card(self, parent, fav: dict, idx: int):
        url  = fav.get("url", "")
        name = fav.get("name", f"Favorite #{idx+1}")
        note = fav.get("note", "")
        p = self.P

        r = None
        for rr in p.results:
            u = self._vless(rr.ip, rr.port)
            if u == url:
                r = rr
                break
        if r is None:
            for rr in p.results:
                if rr.ip in url and str(rr.port) in url:
                    r = rr
                    break

        m = fav.get("metrics", {})
        ping_ms   = r.ping_ms if r else m.get("ping_ms")
        jitter_ms = r.jitter_ms if r else m.get("jitter_ms")
        loss_pct  = r.loss_pct if r else m.get("loss_pct")
        colo      = r.colo if r else m.get("colo", "")
        dl_mbps   = r.dl_mbps if r else m.get("dl_mbps")
        up_mbps   = r.up_mbps if r else m.get("up_mbps")
        cf_valid  = r.cf_valid if r else m.get("cf_valid", False)
        stored_ip   = m.get("ip", "")
        stored_port = m.get("port", 0)
        has_data  = ping_ms is not None

        if has_data:
            if ping_ms < 150:
                card_bg = CARD_BG_2
            elif ping_ms < 400:
                card_bg = CARD_BG_3
            else:
                card_bg = CARD_BG_4

            card = _card(parent, bg=card_bg)
            card.pack(fill=tk.X, pady=3, padx=2)
            tk.Frame(card, bg=_ping_color(ping_ms), width=5).pack(side=tk.LEFT, fill=tk.Y)
            bf = tk.Frame(card, bg=card_bg)
            bf.pack(side=tk.RIGHT, padx=6, pady=4)
            lnk = _ilbl(bf, "\U0001f517", lambda u=url, n=name: self._copy_with_toast(u, n))
            lnk.pack(side=tk.LEFT, padx=2)
            _add_tooltip(lnk, "Copy config link")
            qrl = _ilbl(bf, "\U0001f4f7", lambda u=url, n=name: show_qr(self.root, u, n))
            qrl.pack(side=tk.LEFT, padx=2)
            _add_tooltip(qrl, "Show QR code")
            _ip = r.ip if r else stored_ip
            _port = r.port if r else stored_port
            if _ip and _port:
                def _fav_test(rr=r, ip=_ip, port=_port):
                    if rr:
                        self._test_single_config(rr)
                    else:
                        fake = ProbeResult(ip=ip, port=port, mode="http",
                                           ping_ms=ping_ms, error=None)
                        self._test_single_config(fake)
                test_lbl = _ilbl(bf, "\u26a1", _fav_test)
                test_lbl.pack(side=tk.LEFT, padx=2)
                _add_tooltip(test_lbl, "Test this config")
                def _fav_connect(rr=r, ip=_ip, port=_port):
                    if rr:
                        self._load_connect(rr)
                    else:
                        fake = ProbeResult(ip=ip, port=port, mode="http",
                                           ping_ms=ping_ms, error=None)
                        self._load_connect(fake)
                con = _ilbl(bf, "\U0001f310", _fav_connect)
                con.pack(side=tk.LEFT, padx=2)
                _add_tooltip(con, "Connect")
            dell = _ilbl(bf, "\U0001f5d1", lambda i=idx: self._del_favorite(i))
            dell.pack(side=tk.LEFT, padx=2)
            _add_tooltip(dell, "Remove from favorites")

            inner = tk.Frame(card, bg=card_bg)
            inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=6)
            cfg_label = f"#{idx+1}  \u2b50 {name}"
            tk.Label(inner, text=cfg_label, font=FH, bg=card_bg, fg=FG1,
                     wraplength=320, anchor="w", justify="left").pack(anchor="w")
            if note:
                tk.Label(inner, text=note, font=FS, bg=card_bg, fg=FG4).pack(anchor="w")
            row2 = tk.Frame(inner, bg=card_bg)
            row2.pack(anchor="w")
            for lbl, val, col in [
                ("Ping",   _ping_label(ping_ms),  _ping_color(ping_ms)),
                ("Jitter", (f"{jitter_ms:.0f}ms" if jitter_ms is not None else "\u2014"),
                            _ping_color(jitter_ms)),
                ("Loss",   (f"{loss_pct:.0f}%" if loss_pct is not None else "\u2014"),
                            GREEN if (loss_pct or 0)<5 else (ORANGE if (loss_pct or 0)<25 else RED_C)),
                ("Colo",   colo or "\u2014", TEAL if cf_valid else FG3),
                ("DL",     f"{dl_mbps:.1f}M" if dl_mbps else "\u2014",
                            GREEN if (dl_mbps or 0)>=5 else (ORANGE if (dl_mbps or 0)>=1 else RED_C)),
                ("UP",     f"{up_mbps:.1f}M" if up_mbps else "\u2014",
                            GREEN if (up_mbps or 0)>=5 else (ORANGE if (up_mbps or 0)>=1 else RED_C)),
            ]:
                tk.Label(row2, text=f" {lbl}:", font=FS, bg=card_bg, fg=FG1).pack(side=tk.LEFT)
                tk.Label(row2, text=f" {val} ", font=("Segoe UI",9,"bold"), bg=card_bg,
                         fg=col).pack(side=tk.LEFT)
        else:
            card = _card(parent)
            card.pack(fill=tk.X, pady=3, padx=2)
            tk.Frame(card, bg=ORANGE, width=5).pack(side=tk.LEFT, fill=tk.Y)
            bf = tk.Frame(card, bg=BG_CARD)
            bf.pack(side=tk.RIGHT, padx=6, pady=4)
            lnk = _ilbl(bf, "\U0001f517", lambda u=url, n=name: self._copy_with_toast(u, n))
            lnk.pack(side=tk.LEFT, padx=2)
            _add_tooltip(lnk, "Copy config link")
            qrl = _ilbl(bf, "\U0001f4f7", lambda u=url, n=name: show_qr(self.root, u, n))
            qrl.pack(side=tk.LEFT, padx=2)
            _add_tooltip(qrl, "Show QR code")
            dell = _ilbl(bf, "\U0001f5d1", lambda i=idx: self._del_favorite(i))
            dell.pack(side=tk.LEFT, padx=2)
            _add_tooltip(dell, "Remove from favorites")
            inner = tk.Frame(card, bg=BG_CARD)
            inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=6)
            tk.Label(inner, text=f"#{idx+1}  \u2b50 {name}", font=FH, bg=BG_CARD, fg=FG1,
                     wraplength=320, anchor="w", justify="left").pack(anchor="w")
            if note:
                tk.Label(inner, text=note, font=FS, bg=BG_CARD, fg=FG4).pack(anchor="w")
            url_short = url[:70] + "\u2026" if len(url) > 70 else url
            tk.Label(inner, text=url_short, font=FM, bg=BG_CARD, fg=FG3).pack(anchor="w")

    def _add_favorite(self, url: str, name: str, note: str = ""):
        self._activity("Added a favorite")
        for fav in self.P.favorites:
            if fav.get("url") == url:
                messagebox.showinfo("Already Added",
                    f"'{name}' is already in your Favorites.", parent=self.root)
                return
        metrics = {}
        for r in self.P.results:
            u = self._vless(r.ip, r.port)
            if u == url:
                metrics = {
                    "ping_ms": r.ping_ms, "jitter_ms": r.jitter_ms,
                    "loss_pct": r.loss_pct, "colo": r.colo,
                    "dl_mbps": r.dl_mbps, "up_mbps": r.up_mbps,
                    "cf_valid": r.cf_valid, "ip": r.ip, "port": r.port,
                }
                break
        self.P.favorites.append({"url": url, "name": name, "note": note, "metrics": metrics})
        save_profiles(self.profiles, self._prof_idx)
        try: self._refresh_favorites()
        except Exception: pass
        toast = tk.Toplevel(self.root)
        toast.wm_overrideredirect(True)
        x = self.root.winfo_rootx() + self.root.winfo_width()//2 - 150
        y = self.root.winfo_rooty() + self.root.winfo_height() - 80
        toast.wm_geometry(f"+{x}+{y}")
        toast.configure(bg=GREEN)
        tk.Label(toast, text=f"\u2714  '{name}' added to Favorites!",
                 font=("Segoe UI", 10, "bold"), bg=GREEN, fg="white",
                 padx=16, pady=8).pack()
        toast.after(2200, toast.destroy)

    def _del_favorite(self, idx: int):
        if messagebox.askyesno("Remove", "Remove from favorites?", parent=self.root):
            self._activity("Removed a favorite")
            self.P.favorites.pop(idx)
            save_profiles(self.profiles, self._prof_idx)
            self._refresh_favorites()

    def _add_fav_manual(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add Favorite"); dlg.resizable(False, False)
        dlg.configure(bg=BG); dlg.grab_set()
        card = _card(dlg); card.pack(padx=16, pady=12, fill=tk.X)
        card.columnconfigure(1, weight=1)
        v_name = tk.StringVar(); v_url = tk.StringVar(); v_note = tk.StringVar()
        for ri, (lbl, var) in enumerate([("Name", v_name), ("VLESS URL", v_url), ("Note", v_note)]):
            tk.Label(card, text=lbl+":", font=FB, bg=CARD, fg=FG1,
                     width=12, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=5, sticky="w")
            ttk.Entry(card, textvariable=var, width=40).grid(
                row=ri, column=1, sticky="ew", padx=(0,12), pady=5)
        bf = tk.Frame(dlg, bg=BG); bf.pack(pady=(0,12))
        _abtn(bf, "Add", lambda: [
            self._add_favorite(v_url.get(), v_name.get() or "Favorite", v_note.get()),
            dlg.destroy()]).pack(side=tk.LEFT, padx=6)
        _gbtn(bf, "Cancel", dlg.destroy).pack(side=tk.LEFT, padx=6)

    # ══════════════════════════════════════════════════════
    #  About tab
    # ══════════════════════════════════════════════════════

    def _build_about(self):
        af = self.pages["about"]
        af.rowconfigure(0, weight=1)
        scroll = SF(af, bg=BG)
        scroll.grid(row=0, column=0, sticky="nsew")
        p = scroll.inner

        # App logo / title
        logo = tk.Frame(p, bg=ACCENT, height=100)
        logo.pack(fill=tk.X, pady=(0, 16))
        tk.Label(logo, text="\u26a1  VLESS Edge Optimizer ver 4.5",
                 font=(FONT_FAMILY, 18, "bold"), bg=ACCENT, fg="white").pack(pady=(20, 4))
        tk.Label(logo, text="VEO  \u00b7  VLESS Edge Optimizer",
                 font=FS, bg=ACCENT, fg="#ffe0dc").pack()

        def info_card(title, rows):
            c = _card(p); c.pack(fill=tk.X, pady=4, padx=2)
            tk.Label(c, text=title, font=FH, bg=BG_CARD, fg=FG2,
                     padx=12, pady=4).pack(anchor="w", pady=(8, 2))
            for lbl, val, col in rows:
                r = tk.Frame(c, bg=BG_CARD); r.pack(fill=tk.X, padx=12, pady=2)
                tk.Label(r, text=f"{lbl}:", font=FS, bg=BG_CARD, fg=FG4,
                         width=18, anchor="w").pack(side=tk.LEFT)
                tk.Label(r, text=val, font=FB, bg=BG_CARD,
                         fg=col, cursor="hand2").pack(side=tk.LEFT)
            tk.Frame(c, bg=BG_CARD, height=8).pack()

        info_card("About", [
            ("App",        "VEO (VLESS Edge Optimizer)", FG1),
            ("Version",    "4.5",                    FG2),
            ("Platform",   sys.platform,              FG2),
            ("Python",     sys.version.split()[0],   FG2),
        ])

        info_card("Developer", [
            ("Author",     "VEO Dev Team",            FG1),
            ("Email",      "dev@netmod.app",           BLUE),
            ("GitHub",     "github.com/netmod/vless-optimizer", BLUE),
            ("Website",    "netmod.app",               BLUE),
        ])

        # Donation card
        dc = _card(p); dc.pack(fill=tk.X, pady=4, padx=2)
        tk.Label(dc, text="\u2615  Support Development", font=FH, bg=BG_CARD,
                 fg=FG2, padx=12, pady=8).pack(pady=(8,4), anchor="w")
        tk.Label(dc,
                 text="If this tool saved you time, consider buying the dev a coffee!\n"
                      "Your support keeps this project alive and growing.",
                 font=FB, bg=BG_CARD, fg=FG3, padx=12, justify="left").pack(anchor="w")
        bf = tk.Frame(dc, bg=BG_CARD); bf.pack(anchor="w", padx=12, pady=8)
        _abtn(bf, "\u2615 Buy Me a Coffee",
              lambda: self._open_url("https://buymeacoffee.com/netmod"),
              color=ORANGE).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf, "\u2b50 Star on GitHub",
              lambda: self._open_url("https://github.com/netmod/vless-optimizer"),
              color=FG3).pack(side=tk.LEFT)

        # Features card
        fc = _card(p); fc.pack(fill=tk.X, pady=4, padx=2)
        tk.Label(fc, text="Features", font=FH, bg=BG_CARD, fg=FG2,
                 padx=12, pady=8).pack(pady=(8,4), anchor="w")
        features = [
            "\u2022 Multi-port Cloudflare edge IP scanner with real TCP pre-filter",
            "\u2022 VLESS+WS+TLS / gRPC / TCP config builder",
            "\u2022 xray-core integration: latency, download speed, real proxy test",
            "\u2022 Auto-switch mode with stability guard (min 2 min hold)",
            "\u2022 Connection log (V2Ray-style accepted/rejected lines)",
            "\u2022 System-wide proxy mode \u2014 tunnel all apps (Windows)",
            "\u2022 Scan history across sessions",
            "\u2022 Favorites tab for starred configs",
            "\u2022 Profile system: save multiple VPN configs",
            "\u2022 Pure-Python QR code generator (no dependencies)",
            "\u2022 Modular Python package structure",
            "\u2022 Dark theme UI",
        ]
        for f in features:
            tk.Label(fc, text=f, font=FS, bg=BG_CARD, fg=FG3,
                     anchor="w", padx=12).pack(anchor="w")
        tk.Frame(fc, bg=BG_CARD, height=8).pack()

    def _open_url(self, url: str):
        try:
            import webbrowser; webbrowser.open(url)
        except Exception: pass

    # ══════════════════════════════════════════════════════
    #  Developer Log tab
    # ══════════════════════════════════════════════════════


    # ══════════════════════════════════════════════════════
    #  BPB Panel Wizard tab
    # ══════════════════════════════════════════════════════

    def _build_bpb(self, container):
        bf = container
        bf.rowconfigure(1, weight=1)

        # header
        hc = _card(bf); hc.grid(row=0, column=0, sticky="ew", pady=(0,8))
        hc.columnconfigure(0, weight=1)
        logo_f = tk.Frame(hc, bg="#F6821F", height=52)
        logo_f.grid(row=0, column=0, sticky="ew")
        tk.Label(logo_f, text="\u2601  BPB Panel Wizard  v4.2.2",
                 font=(FONT_FAMILY, 13, "bold"), bg="#F6821F", fg="white"
                 ).pack(side=tk.LEFT, padx=14, pady=12)
        tk.Label(logo_f,
                 text="Deploy BPB Panel to Cloudflare Workers \u2014 no terminal needed",
                 font=FS, bg="#F6821F", fg="#ffe0c0").pack(side=tk.LEFT)
        tk.Label(hc,
                 text="Fill credentials \u2192 configure \u2192 click Deploy. "
                      "Settings auto-fill in Config tab on success.",
                 font=FS, bg=BG_CARD, fg=FG3, justify="left",
                 padx=12, pady=6, wraplength=570).grid(row=1, column=0, sticky="w")

        # scrollable body
        scroll = SF(bf, bg=BG); scroll.grid(row=1, column=0, sticky="nsew")
        p = scroll.inner

        def section(title, color=BLUE):
            tk.Label(p, text=title, font=FH, bg=BG, fg=color).pack(
                anchor="w", pady=(10,2), padx=2)
            c = _card(p); c.pack(fill=tk.X, pady=(0,6), padx=2)
            c.columnconfigure(1, weight=1)
            return c

        # Step 1: credentials
        s1 = section("Step 1 \u2014 Cloudflare Credentials")
        self._bpb_email    = tk.StringVar()
        self._bpb_api_key  = tk.StringVar()
        self._bpb_acct_id  = tk.StringVar()
        creds = [
            ("CF Email *",       self._bpb_email,   False, "Cloudflare account email"),
            ("Global API Key *", self._bpb_api_key, True,  "Profile \u2192 API Tokens \u2192 Global API Key"),
            ("Account ID *",     self._bpb_acct_id, False, "CF Dashboard right sidebar"),
        ]
        for ri,(lbl,var,secret,hint) in enumerate(creds):
            tk.Label(s1, text=lbl, font=FB, bg=BG_CARD, fg=FG2,
                     width=20, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=5, sticky="w")
            ttk.Entry(s1, textvariable=var, show="\u2022" if secret else "",
                      width=38).grid(row=ri, column=1, sticky="ew", padx=(0,4), pady=5)
            tk.Label(s1, text=hint, font=FS, bg=BG_CARD, fg=FG4).grid(
                row=ri, column=2, padx=(0,12), pady=5, sticky="w")
        hl = tk.Label(s1, text="\u2192 Find API Key & Account ID on Cloudflare",
                      font=FS, bg=BG_CARD, fg=BLUE, cursor="hand2")
        hl.grid(row=len(creds), column=0, columnspan=3, padx=12, pady=(0,8), sticky="w")
        hl.bind("<Button-1>", lambda _: self._open_url(
            "https://dash.cloudflare.com/profile/api-tokens"))

        # Step 2: worker settings
        s2 = section("Step 2 \u2014 Worker Settings")
        self._bpb_worker_name = tk.StringVar(value="bpb-panel")
        self._bpb_panel_pass  = tk.StringVar(value="admin")
        self._bpb_sub_length  = tk.StringVar(value="24")
        self._bpb_trojan_pass = tk.StringVar(value="")
        self._bpb_custom_uuid = tk.StringVar(value="")
        wrows = [
            ("Worker Name *",    self._bpb_worker_name, False, "e.g. bpb-panel (letters/numbers/hyphens)"),
            ("Panel Password *", self._bpb_panel_pass,  True,  "Password to access the panel settings"),
            ("Sub Path Length",  self._bpb_sub_length,  False, "Subscription path length (default 24)"),
            ("Trojan Password",  self._bpb_trojan_pass, True,  "Leave blank to auto-generate"),
            ("Custom UUID",      self._bpb_custom_uuid, False, "Leave blank to auto-generate"),
        ]
        for ri,(lbl,var,secret,hint) in enumerate(wrows):
            tk.Label(s2, text=lbl, font=FB, bg=BG_CARD, fg=FG2,
                     width=20, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=5, sticky="w")
            ttk.Entry(s2, textvariable=var, show="\u2022" if secret else "",
                      width=30).grid(row=ri, column=1, sticky="ew", padx=(0,4), pady=5)
            tk.Label(s2, text=hint, font=FS, bg=BG_CARD, fg=FG4).grid(
                row=ri, column=2, padx=(0,12), pady=5, sticky="w")

        # Step 3: optional custom domain
        s3 = section("Step 3 \u2014 Custom Domain  (optional)")
        self._bpb_use_domain = tk.BooleanVar(value=False)
        self._bpb_domain     = tk.StringVar(value="")
        self._bpb_zone_id    = tk.StringVar(value="")
        tk.Label(s3, text="Custom domain", font=FB, bg=BG_CARD, fg=FG2,
                 width=20, anchor="w").grid(row=0, column=0, padx=(12,4), pady=5, sticky="w")
        ttk.Checkbutton(s3, variable=self._bpb_use_domain,
                        text="Enable (domain must be managed by Cloudflare)"
                        ).grid(row=0, column=1, columnspan=2, sticky="w", padx=(0,12), pady=5)
        for ri,(lbl,var,hint) in enumerate([
            ("Domain",  self._bpb_domain,  "e.g. vpn.example.com"),
            ("Zone ID", self._bpb_zone_id, "From Cloudflare domain overview page"),
        ], 1):
            tk.Label(s3, text=lbl, font=FB, bg=BG_CARD, fg=FG2,
                     width=20, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=5, sticky="w")
            ttk.Entry(s3, textvariable=var, width=30).grid(
                row=ri, column=1, sticky="ew", padx=(0,4), pady=5)
            tk.Label(s3, text=hint, font=FS, bg=BG_CARD, fg=FG4).grid(
                row=ri, column=2, padx=(0,12), pady=5, sticky="w")

        # Deploy card
        dc = _card(p); dc.pack(fill=tk.X, pady=(0,6), padx=2)
        dc.columnconfigure(2, weight=1)
        self._bpb_deploy_btn = _abtn(dc, "\U0001f680  Deploy", self._bpb_deploy, color="#F6821F")
        self._bpb_deploy_btn.grid(row=0, column=0, padx=(12,6), pady=10)
        self._bpb_validate_btn = _gbtn(dc, "\u2714 Validate Creds", self._bpb_validate)
        self._bpb_validate_btn.grid(row=0, column=1, padx=(0,6), pady=10)
        _gbtn(dc, "\U0001f504 Reset", self._bpb_reset, True).grid(
            row=0, column=2, padx=(0,12), pady=10, sticky="w")
        self._bpb_prog = ttk.Progressbar(dc, mode="indeterminate", length=200)
        self._bpb_prog.grid(row=1, column=0, columnspan=4, sticky="ew",
                            padx=12, pady=(0,4))
        self._bpb_prog.grid_remove()
        self._bpb_status_var = tk.StringVar(value="Ready \u2014 fill credentials and click Deploy.")
        tk.Label(dc, textvariable=self._bpb_status_var, font=FS, bg=BG_CARD, fg=FG3,
                 anchor="w", wraplength=520).grid(row=2, column=0, columnspan=4,
                                                   sticky="ew", padx=12, pady=(0,8))

        # Log
        lc = section("Deployment Log", TEAL)
        self._bpb_log = tk.Text(lc, height=10, wrap="word", state="disabled",
                                 bg="#0d1117", fg="#c0caf5", font=FM, relief="flat",
                                 bd=0, insertbackground="#c0caf5",
                                 selectbackground=ACCENT,
                                 padx=8, pady=4)
        self._bpb_log.grid(row=0, column=0, sticky="ew", columnspan=3, padx=1, pady=1)
        lc.rowconfigure(0, weight=1)

        # Result card (hidden until success)
        self._bpb_result_card = _card(p)
        self._bpb_result_card.pack(fill=tk.X, pady=(0,6), padx=2)
        self._bpb_result_card.pack_forget()

    def _bpb_log_write(self, msg):
        try:
            self._bpb_log.configure(state="normal")
            self._bpb_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
            self._bpb_log.see(tk.END)
            self._bpb_log.configure(state="disabled")
        except Exception: pass

    def _bpb_set_status(self, msg, color=None):
        try: self._bpb_status_var.set(msg)
        except Exception: pass

    def _bpb_reset(self):
        for v in (self._bpb_email, self._bpb_api_key, self._bpb_acct_id,
                  self._bpb_domain, self._bpb_zone_id,
                  self._bpb_trojan_pass, self._bpb_custom_uuid):
            v.set("")
        self._bpb_worker_name.set("bpb-panel")
        self._bpb_panel_pass.set("admin")
        self._bpb_sub_length.set("24")
        self._bpb_use_domain.set(False)
        self._bpb_log.configure(state="normal")
        self._bpb_log.delete("1.0", tk.END)
        self._bpb_log.configure(state="disabled")
        self._bpb_set_status("Ready.")
        self._bpb_result_card.pack_forget()

    def _bpb_validate(self):
        e = self._bpb_email.get().strip()
        k = self._bpb_api_key.get().strip()
        a = self._bpb_acct_id.get().strip()
        if not all([e,k,a]):
            messagebox.showwarning("Missing",
                "Fill Email, API Key and Account ID first.", parent=self.root)
            return
        self._bpb_validate_btn.config(state=tk.DISABLED, text="Checking…")
        self._bpb_log_write("Validating credentials…")
        def run():
            ok, msg = _cf_validate(e, k, a)
            self.q.put(("bpb_validate_done", ok, msg))
        threading.Thread(target=run, daemon=True).start()

    def _bpb_deploy(self):
        e = self._bpb_email.get().strip()
        k = self._bpb_api_key.get().strip()
        a = self._bpb_acct_id.get().strip()
        wname = self._bpb_worker_name.get().strip()
        pw    = self._bpb_panel_pass.get().strip()
        if not all([e,k,a,wname,pw]):
            messagebox.showwarning("Missing Fields",
                "Fill: CF Email, Global API Key, Account ID, "
                "Worker Name, Panel Password", parent=self.root)
            return
        import re as _re2
        if not _re2.match(r'^[a-z0-9][a-z0-9\-]{0,61}[a-z0-9]$', wname, _re2.I):
            messagebox.showwarning("Invalid Name",
                "Worker name: 2-63 chars, letters/numbers/hyphens.", parent=self.root)
            return
        self._bpb_deploy_btn.config(state=tk.DISABLED, text="Deploying…")
        self._bpb_validate_btn.config(state=tk.DISABLED)
        self._bpb_prog.grid(); self._bpb_prog.start(10)
        self._bpb_result_card.pack_forget()
        self._bpb_log.configure(state="normal")
        self._bpb_log.delete("1.0", tk.END)
        self._bpb_log.configure(state="disabled")
        params = {
            "email": e, "api_key": k, "acct_id": a, "wname": wname,
            "panel_pass": pw,
            "sub_length": int(self._bpb_sub_length.get() or "24"),
            "trojan_pass": self._bpb_trojan_pass.get().strip(),
            "custom_uuid": self._bpb_custom_uuid.get().strip(),
            "use_domain":  self._bpb_use_domain.get(),
            "domain":      self._bpb_domain.get().strip(),
            "zone_id":     self._bpb_zone_id.get().strip(),
        }
        threading.Thread(target=lambda: _bpb_deploy_worker(params, self.q),
                         daemon=True).start()

    def _bpb_show_result(self, result):
        for w in self._bpb_result_card.winfo_children(): w.destroy()
        self._bpb_result_card.columnconfigure(1, weight=1)
        tk.Frame(self._bpb_result_card, bg=GREEN, height=4).grid(
            row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(self._bpb_result_card,
                 text="\u2705  BPB Panel Deployed Successfully!",
                 font=FH, bg=BG_CARD, fg=GREEN, padx=12, pady=6
                 ).grid(row=1, column=0, columnspan=3, sticky="w")
        rows_data = [
            ("Panel URL",      result.get("panel_url","\u2014"),  BLUE),
            ("Worker URL",     result.get("worker_url","\u2014"), BLUE),
            ("Panel Password", result.get("panel_pass","\u2014"), ORANGE),
            ("UUID",           result.get("uuid","\u2014"),       TEAL),
            ("Subscription",   result.get("sub_url","\u2014"),    GREEN),
        ]
        for ri,(lbl,val,col) in enumerate(rows_data, 2):
            tk.Label(self._bpb_result_card, text=lbl+":", font=FB, bg=BG_CARD, fg=FG3,
                     width=18, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=3, sticky="w")
            vl = tk.Label(self._bpb_result_card, text=val, font=FB, bg=BG_CARD,
                          fg=col, cursor="hand2", anchor="w")
            vl.grid(row=ri, column=1, sticky="ew", padx=(0,4), pady=3)
            vl.bind("<Button-1>", lambda _e,v=val,l=lbl: self._copy_with_toast(v,l))
            _abtn(self._bpb_result_card, "Copy",
                  lambda v=val,l=lbl: self._copy_with_toast(v,l), True
                  ).grid(row=ri, column=2, padx=(0,12), pady=3)
        # auto-fill config & save profile immediately on success
        self._bpb_autofill_config(result, silent=True)
        # also register this BPB worker in the unified Worker Pool
        self._bpb_store_to_pool(result)
        # saved badge
        badge_row = len(rows_data) + 2
        tk.Label(self._bpb_result_card,
                 text="\U0001f4be  Config tab updated & profile saved automatically",
                 font=(FONT_FAMILY, 9), bg=BG_CARD, fg=GREEN, padx=12, pady=4
                 ).grid(row=badge_row, column=0, columnspan=3, sticky="w")
        bf2 = tk.Frame(self._bpb_result_card, bg=BG_CARD)
        bf2.grid(row=badge_row+1, column=0, columnspan=3,
                 padx=12, pady=(2,10), sticky="w")
        _abtn(bf2, "\u21ba Re-apply to Config",
              lambda: self._bpb_autofill_config(result, silent=False), color=TEAL
              ).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf2, "\U0001f310 Open Panel",
              lambda: self._open_url(result.get("panel_url","")),
              color="#F6821F").pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf2, "\U0001f4cb Copy All",
              lambda: self._copy_with_toast(
                  "\n".join(f"{k}: {v}" for k,v in result.items()), "BPB Config"),
              color=FG3).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf2, "\U0001f4be Save as TXT",
              lambda: self._bpb_save_txt(result),
              color=PURPLE).pack(side=tk.LEFT, padx=(0,8))
        _abtn(bf2, "\U0001f504 Fetch Panel Info",
              lambda: self._bpb_manual_fetch(result),
              color="#F6821F").pack(side=tk.LEFT)
        self._bpb_result_card.pack(fill=tk.X, pady=(0,6), padx=2)

    def _bpb_store_to_pool(self, result):
        """Add a successfully-deployed BPB worker to the unified Worker Pool
        (tagged source='bpb'), so it shows up alongside CF Worker entries
        in the Worker Pool tab. Skips duplicates (same host + uuid)."""
        try:
            host = result.get("worker_host", "")
            uid  = result.get("uuid", "")
            if not host or not uid:
                return
            for t in self.P.cf_workers:
                if t.get("worker_host") == host and t.get("uuid") == uid:
                    return  # already in the pool
            sub_path = result.get("sub_path", "")
            self.P.cf_workers.append({
                "name":        result.get("panel_name") or "BPB Panel",
                "email":       result.get("email", ""),
                "api_key":     result.get("api_key", ""),
                "acct_id":     result.get("acct_id", ""),
                "script_name": result.get("panel_name", ""),
                "uuid":        uid,
                "proxy_ip":    result.get("proxy_ip", ""),
                "use_domain":  False, "domain": "", "zone_id": "",
                "worker_host": host,
                "sni":         host.lower(),
                "path":        ("/" + sub_path) if sub_path else "/",
                "network":     "ws", "security": "tls",
                "status":      "ok", "latency_ms": None, "last_check": "",
                "source":      "bpb",
                "panel_url":   result.get("panel_url", ""),
                "sub_url":     result.get("sub_url", ""),
            })
            save_profiles(self.profiles, self._prof_idx)
            try: self._cfw_refresh_tree()
            except Exception: pass
            try:
                self._cfw_status_var.set(
                    f"✔ BPB worker '{self.P.cf_workers[-1]['name']}' added to the Worker Pool.")
            except Exception: pass
            self._bpb_log_write(
                f"📦 Added to Worker Pool: {host}")
        except Exception as e:
            self._logdbg(f"_bpb_store_to_pool error: {e}")

    def _bpb_save_txt(self, result):
        import tkinter.filedialog as _fd
        import time as _tm

        panel_name = result.get("panel_name", "bpb-panel")
        timestamp  = _tm.strftime("%Y%m%d_%H%M%S")
        default_name = f"{panel_name}_{timestamp}.txt"

        path = _fd.asksaveasfilename(
            title="Save BPB Panel Info",
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            parent=self.root,
        )
        if not path:
            return  # user cancelled

        lines = [
            "=" * 52,
            "  BPB Panel — Deployment Info",
            f"  Saved: {_tm.strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 52,
            "",
            f"  Panel URL      : {result.get('panel_url', '—')}",
            f"  Worker URL     : {result.get('worker_url', '—')}",
            f"  Panel Password : {result.get('panel_pass', '—')}",
            f"  UUID           : {result.get('uuid', '—')}",
            f"  Trojan Pass    : {result.get('trojan_pass', '—')}",
            f"  Sub Path       : {result.get('sub_path', '—')}",
            f"  Subscription   : {result.get('sub_url', '—')}",
            "",
            "=" * 52,
            "  Config fields (for v2rayN / xray)",
            "=" * 52,
            "",
            f"  Host / SNI     : {result.get('worker_host', '—')}",
            f"  WS Path        : /{result.get('sub_path', '—')}",
            "  (Real WS path is fetched from subscription after deploy)",
            "",
            "=" * 52,
        ]
        txt = "\n".join(lines)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            self._bpb_log_write(f"  \U0001f4be Saved panel info → {path}")
            self._copy_with_toast(path, "Saved to")
        except Exception as e:
            import tkinter.messagebox as _mb
            _mb.showerror("Save Failed", str(e), parent=self.root)

    def _bpb_manual_fetch(self, result):
        """User-triggered, no-wait check — for when the automatic
        8-12 attempt loop already gave up, or the user just wants to
        check again after waiting a bit longer on their own."""
        worker_host = result.get("worker_host", "")
        sub_path    = result.get("sub_path", "")
        if not worker_host or not sub_path:
            messagebox.showwarning("Missing Data",
                "No deployment info available to fetch.", parent=self.root)
            return
        self._bpb_log_write("  🔄 Manual fetch requested…")
        self._bpb_set_status("🔄 Fetching panel info…")
        def _run():
            info = _bpb_fetch_real_path(worker_host, sub_path)
            def _apply():
                if info.get("path"):
                    self.path_var.set(info["path"])
                    if info.get("sni"): self.sni_var.set(info["sni"])
                    self._save_config_to_profile()
                    save_profiles(self.profiles, self._prof_idx)
                    self._refresh_home()
                    self._bpb_log_write(
                        f"  ✔ Manual fetch succeeded: {info['path'][:70]}")
                    self._bpb_set_status("✅ Panel info updated!")
                    messagebox.showinfo("Success",
                        "Path and SNI updated from the live panel.",
                        parent=self.root)
                else:
                    self._bpb_log_write(
                        "  ✖ Manual fetch failed — panel may still be propagating.")
                    self._bpb_set_status("⚠ Not ready — try again shortly.")
                    messagebox.showwarning("Not Ready Yet",
                        "Could not fetch panel info. Cloudflare can take up to "
                        "5 minutes to fully propagate a new worker.\n"
                        "Wait a bit and click this button again.",
                        parent=self.root)
            try: self.root.after(0, _apply)
            except Exception: pass
        import threading as _thr2
        _thr2.Thread(target=_run, daemon=True).start()

    def _bpb_autofill_config(self, result, silent=False):
        # ── immediate fields ──────────────────────────────────────────────────
        if result.get("uuid"):
            self.uid_var.set(result["uuid"])
        if result.get("worker_host"):
            self.host_var.set(result["worker_host"])
            # SNI: always lowercase — panel randomises case intentionally
            self.sni_var.set(result["worker_host"].lower())
        if result.get("panel_name"):
            self.name_var.set(result["panel_name"])
        # ── path: set placeholder, then overwrite with real path async ────────
        if result.get("sub_path"):
            self.path_var.set("/" + result["sub_path"])   # temporary placeholder

        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        self._refresh_home()
        if not silent:
            messagebox.showinfo("Config Updated",
                "Config tab updated with BPB Panel settings.\n"
                "UID, Host and SNI saved.  Fetching real WS path from panel...",
                parent=self.root)
            self._show("config")

        # ── background: fetch the real WS path from the live subscription ────
        worker_host = result.get("worker_host", "")
        sub_path    = result.get("sub_path", "")
        _silent     = silent

        def _fetch_and_apply():
            import time as _t
            # Cloudflare can take 4-5 min to fully propagate a brand-new
            # worker + freshly-registered subdomain, so spread retries
            # across ~5 minutes total instead of giving up after ~2 min.
            MAX_TRIES=12; DELAYS=[10,15,20,25,30,30,30,30,30,30,30,30]
            real_path=""; real_sni=""
            for attempt in range(1,MAX_TRIES+1):
                wait=DELAYS[attempt-1] if attempt-1<len(DELAYS) else 30
                try:
                    self.root.after(0,lambda a=attempt,w=wait:
                        self._bpb_log_write(f"  ⏳ Path fetch attempt {a}/{MAX_TRIES} (waiting {w}s)…"))
                    self.root.after(0,lambda a=attempt:
                        self._bpb_set_status(f"⏳ Fetching WS path… attempt {a}/{MAX_TRIES}"))
                except Exception: pass
                _t.sleep(wait)
                info=_bpb_fetch_real_path(worker_host,sub_path)
                real_path=info.get("path",""); real_sni=info.get("sni","")
                if real_path:
                    try: self.root.after(0,lambda a=attempt:
                        self._bpb_log_write(f"  ✔ Got real path on attempt {a}"))
                    except Exception: pass
                    break
                try: self.root.after(0,lambda a=attempt:
                    self._bpb_log_write(f"  ↺ Attempt {a} failed, retrying…"))
                except Exception: pass
            if real_path:
                # Proxy IP is intentionally left to worker.js's own built-in
                # default (see _bpb_deploy_worker) — we no longer rewrite the
                # panel's proxySettings KV record here.
                def _apply():
                    try:
                        self.path_var.set(real_path)
                        if real_sni: self.sni_var.set(real_sni)
                        self._save_config_to_profile()
                        save_profiles(self.profiles,self._prof_idx)
                        self._refresh_home()
                        self._bpb_log_write(f"  ✔ Auto-filled real WS path: {real_path[:70]}")
                        self._bpb_log_write(f"  ✔ SNI: {real_sni}")
                        self._bpb_set_status("✅ Config path updated!")
                    except Exception: pass
                try: self.root.after(0,_apply)
                except Exception: pass
            else:
                try: self.root.after(0,lambda:
                    self._bpb_log_write(f"  ✖ All {MAX_TRIES} attempts failed — set path manually."))
                except Exception: pass
        import threading as _thr
        _thr.Thread(target=_fetch_and_apply,daemon=True).start()

    # ══════════════════════════════════════════════════════════════
    #  CF Worker tab — own minimal VLESS core, deployed as a pool
    # ══════════════════════════════════════════════════════════════

    # ═══════════════════════════════════════════════════════════════════
    #  Worker Wizard  (BPB Panel + CF Worker creators as sub-tabs)
    # ═══════════════════════════════════════════════════════════════════

    def _build_wizard(self):
        wf = self.pages["wizard"]
        wf.rowconfigure(0, weight=1)
        wf.columnconfigure(0, weight=1)

        nb = ttk.Notebook(wf)
        nb.grid(row=0, column=0, sticky="nsew")

        tab_bpb = tk.Frame(nb, bg=BG)
        tab_bpb.columnconfigure(0, weight=1); tab_bpb.rowconfigure(1, weight=1)
        tab_cf = tk.Frame(nb, bg=BG)
        tab_cf.columnconfigure(0, weight=1); tab_cf.rowconfigure(1, weight=1)

        nb.add(tab_bpb, text="  \u2601 BPB Panel  ")
        nb.add(tab_cf,  text="  \U0001f9f1 CF Worker  ")

        # Populate each creator into its sub-tab frame.
        self._build_bpb(tab_bpb)
        self._build_cfworker_creator(tab_cf)

    # ═══════════════════════════════════════════════════════════════════
    #  Worker Pool tab  (unified pool for BPB + CF Worker + manual)
    # ═══════════════════════════════════════════════════════════════════

    def _build_wpool(self):
        wf = self.pages["wpool"]
        wf.rowconfigure(0, weight=0)   # only the pool body (row 1) stretches
        wf.rowconfigure(1, weight=1)
        wf.columnconfigure(0, weight=1)

        # ── Header ──
        hc = _card(wf); hc.grid(row=0, column=0, sticky="ew", pady=(0,8))
        hc.columnconfigure(0, weight=1)
        head = tk.Frame(hc, bg="#1e2530")
        head.grid(row=0, column=0, sticky="ew")
        tk.Label(head, text="\U0001f4e6  Worker Pool", font=FH,
                 bg="#1e2530", fg="white").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(head, text="every worker you create or import \u2014 manage, deploy, test & use",
                 font=FS, bg="#1e2530", fg="#9fb4d0").pack(side=tk.LEFT)
        tk.Label(hc, justify="left", wraplength=640, font=FS, bg=CARD, fg=FG2,
                 padx=12, pady=6,
                 text="Workers from the BPB Panel and CF Worker wizards are added here "
                      "automatically (see the 'From' column). Select one to Edit, Remove, "
                      "Deploy, Check (test), or Use it in the Config tab \u2014 or Import / "
                      "Export the whole pool as JSON."
                 ).grid(row=1, column=0, sticky="ew")

        scroll = SF(wf, bg=BG); scroll.grid(row=1, column=0, sticky="nsew")
        body = scroll.inner
        body.columnconfigure(0, weight=1)
        _row = [0]

        def section(title, color=BLUE):
            tk.Label(body, text=title, font=FH, bg=BG, fg=color).grid(
                row=_row[0], column=0, sticky="w", pady=(10,2), padx=2)
            _row[0] += 1
            c = _card(body)
            c.grid(row=_row[0], column=0, sticky="ew", pady=(0,6), padx=2)
            _row[0] += 1
            c.columnconfigure(0, weight=1)
            return c

        # ── Pool table ──
        s1 = section("Workers")
        tw = tk.Frame(s1, bg=CARD)
        tw.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,4))
        tw.columnconfigure(0, weight=1)

        cols  = ("name","source","host","uuid","status","lat")
        heads = ("Name","From","Worker Host","UUID","Status","Latency")
        widths= (110, 70, 250, 100, 80, 70)
        self._cfw_tree = ttk.Treeview(tw, columns=cols, show="headings", height=7)
        for c, h, w in zip(cols, heads, widths):
            self._cfw_tree.heading(c, text=h)
            self._cfw_tree.column(c, width=w,
                                  anchor="w" if c in ("name","host","uuid") else "center")
        self._cfw_tree.grid(row=0, column=0, sticky="ew")
        vsb = ttk.Scrollbar(tw, orient="vertical", command=self._cfw_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self._cfw_tree.configure(yscrollcommand=vsb.set)
        self._cfw_tree.tag_configure("ok",   foreground=GREEN)
        self._cfw_tree.tag_configure("bad",  foreground=RED_C)
        self._cfw_tree.tag_configure("busy", foreground=ORANGE)
        self._cfw_tree.tag_configure("new",  foreground=FG3)
        self._cfw_tree.bind("<Double-1>", lambda _e: self._cfw_edit_selected())

        # ── Management toolbar (two rows so nothing is clipped) ──
        tb = tk.Frame(s1, bg=CARD)
        tb.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
        tb_r1 = tk.Frame(tb, bg=CARD); tb_r1.pack(side=tk.TOP, anchor="w", fill=tk.X)
        tb_r2 = tk.Frame(tb, bg=CARD); tb_r2.pack(side=tk.TOP, anchor="w", fill=tk.X, pady=(4,0))
        _abtn(tb_r1, "\u270f Edit",
              self._cfw_edit_selected, small=True, color=FG3).pack(side=tk.LEFT, padx=(0,4), pady=2)
        _gbtn(tb_r1, "\U0001f5d1 Remove",
              self._cfw_remove_selected, small=True).pack(side=tk.LEFT, padx=4, pady=2)
        _abtn(tb_r1, "\u2714 Use",
              self._cfw_use_selected, small=True, color=GREEN).pack(side=tk.LEFT, padx=4, pady=2)
        _abtn(tb_r2, "\U0001f680 Deploy",
              self._cfw_deploy_selected, small=True, color="#F6821F").pack(side=tk.LEFT, padx=(0,4), pady=2)
        _abtn(tb_r2, "\U0001f680 Deploy All",
              self._cfw_deploy_all, small=True, color="#F6821F").pack(side=tk.LEFT, padx=4, pady=2)
        _abtn(tb_r2, "\U0001f493 Check",
              self._cfw_healthcheck_selected, small=True, color=TEAL).pack(side=tk.LEFT, padx=4, pady=2)
        _abtn(tb_r2, "\U0001f493 Check All",
              self._cfw_healthcheck_all, small=True, color=TEAL).pack(side=tk.LEFT, padx=4, pady=2)
        _gbtn(tb_r2, "\U0001f4e5 Import",
              self._cfw_import, small=True).pack(side=tk.LEFT, padx=4, pady=2)
        _gbtn(tb_r2, "\U0001f4e4 Export",
              self._cfw_export, small=True).pack(side=tk.LEFT, padx=4, pady=2)

        self._cfw_status_var = tk.StringVar(
            value="Pool is empty. Create workers in the Worker Wizard tab, or Import a pool JSON.")
        tk.Label(s1, textvariable=self._cfw_status_var, font=FS, bg=CARD, fg=FG2,
                 anchor="w", justify="left", wraplength=740).grid(
            row=2, column=0, sticky="ew", padx=10, pady=(0,8))

        # ── Deploy / Health-check Log ──
        lc = section("Deploy / Health-Check Log", TEAL)
        self._cfw_log = tk.Text(lc, height=10, wrap="word", state="disabled",
                                bg="#0d1117", fg="#58a6ff", font=FM, relief="flat")
        self._cfw_log.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        self._cfw_refresh_tree()

    # ── CF Worker creator (lives inside the Worker Wizard notebook) ──────
    def _build_cfworker_creator(self, container):
        cf = container
        cf.rowconfigure(1, weight=1)
        cf.columnconfigure(0, weight=1)

        hc = _card(cf); hc.grid(row=0, column=0, sticky="ew", pady=(0,8))
        hc.columnconfigure(0, weight=1)
        head = tk.Frame(hc, bg="#1e2530")
        head.grid(row=0, column=0, sticky="ew")
        tk.Label(head, text="\U0001f9f1  Own Worker Core", font=FH,
                 bg="#1e2530", fg="white").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(head, text="minimal VLESS-WS + NetCheck camouflage \u2014 no BPB overhead",
                 font=FS, bg="#1e2530", fg="#9fb4d0").pack(side=tk.LEFT)
        tk.Label(hc, justify="left", wraplength=640, font=FS, bg=CARD, fg=FG2,
                 padx=12, pady=6,
                 text="Deploys a minimal VLESS-WS worker (ES module). HTTP visitors see the "
                      "NetCheck speed-test page; the proxy only activates for WebSocket "
                      "connections with your UUID."
                 ).grid(row=1, column=0, sticky="ew")

        scroll = SF(cf, bg=BG); scroll.grid(row=1, column=0, sticky="nsew")
        body = scroll.inner
        body.columnconfigure(0, weight=1)
        _row = [0]

        def section(title, color=BLUE):
            tk.Label(body, text=title, font=FH, bg=BG, fg=color).grid(
                row=_row[0], column=0, sticky="w", pady=(10,2), padx=2)
            _row[0] += 1
            c = _card(body)
            c.grid(row=_row[0], column=0, sticky="ew", pady=(0,6), padx=2)
            _row[0] += 1
            c.columnconfigure(0, weight=1)
            return c

        s1 = section("Create a CF Worker")
        tk.Label(s1, justify="left", wraplength=620, font=FS, bg=CARD, fg=FG2,
                 padx=12, pady=8,
                 text="\u2022 New Worker (with CF creds): provide a Cloudflare account so the "
                      "worker can be deployed for you.\n"
                      "\u2022 Register Existing Worker: record a worker you already deployed "
                      "elsewhere \u2014 no Cloudflare login needed."
                 ).grid(row=0, column=0, sticky="w")
        btns = tk.Frame(s1, bg=CARD)
        btns.grid(row=1, column=0, sticky="w", padx=10, pady=(2,10))
        _abtn(btns, "\u2795 New Worker (with CF creds)",
              self._cfw_add_target, color=BLUE).pack(side=tk.LEFT, padx=(0,6), pady=2)
        _abtn(btns, "\U0001f4e5 Register Existing Worker",
              self._cfw_add_worker, color=PURPLE).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Label(s1, justify="left", wraplength=620, font=FS, bg=CARD, fg=TEAL,
                 padx=12, pady=4,
                 text="\u2192 Created workers are added to the Worker Pool tab. "
                      "Deploy, test (Check), and Use them from there."
                 ).grid(row=2, column=0, sticky="w")


    def _cfw_refresh_tree(self):
        for i in self._cfw_tree.get_children():
            self._cfw_tree.delete(i)
        for idx, t in enumerate(self.P.cf_workers):
            status = t.get("status", "new")
            tag = {"ok":"ok","down":"bad","error":"bad",
                   "deploying":"busy","checking":"busy"}.get(status, "new")
            lat = t.get("latency_ms")
            lat_s = f"{lat:.0f}ms" if lat is not None else "—"
            uid = t.get("uuid","")
            uid_s = (uid[:8]+"…") if uid else "—"
            src_lbl = {"bpb":"BPB","manual":"Manual","cfworker":"CF",
                       "imported":"Import"}.get(t.get("source",""), "CF")
            self._cfw_tree.insert("", tk.END, iid=str(idx), tags=(tag,), values=(
                t.get("name","") or f"Target {idx+1}",
                src_lbl,
                t.get("worker_host","") or "— not deployed —",
                uid_s, status, lat_s,
            ))

    def _cfw_log_write(self, msg: str):
        try:
            self._cfw_log.configure(state="normal")
            self._cfw_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
            self._cfw_log.see(tk.END)
            self._cfw_log.configure(state="disabled")
        except Exception:
            pass

    def _cfw_add_worker(self, edit_idx=None):
        """Register an ALREADY-DEPLOYED worker into the pool — no
        Cloudflare credentials needed, since there's nothing to deploy.
        This is deliberately a different, smaller form than Add Target:
        Add Target collects deploy credentials for a worker we're about
        to create; Add Worker just records the connection details of a
        worker that already exists (built by hand, by another tool, or
        from a previous deploy outside this pool)."""
        editing = edit_idx is not None and 0 <= edit_idx < len(self.P.cf_workers)
        cur = self.P.cf_workers[edit_idx] if editing else {}
        dlg = tk.Toplevel(self.root)
        dlg.title("Edit Worker" if editing else "Add Existing Worker")
        dlg.resizable(False, False)
        dlg.configure(bg=BG)
        dlg.grab_set()

        n = len(self.P.cf_workers) + 1
        v_name  = tk.StringVar(value=cur.get("name", f"Worker {n}"))
        v_host  = tk.StringVar(value=cur.get("worker_host", ""))
        v_uuid  = tk.StringVar(value=cur.get("uuid", ""))
        v_sni   = tk.StringVar(value=cur.get("sni", ""))
        v_path  = tk.StringVar(value=cur.get("path", "") or "/?ed=2560")
        v_net   = tk.StringVar(value=cur.get("network", "") or "ws")
        v_sec   = tk.StringVar(value=cur.get("security", "") or "tls")

        card = _card(dlg); card.pack(padx=16, pady=12, fill=tk.X)
        card.columnconfigure(1, weight=1)

        tk.Label(card, text="Already deployed elsewhere? Just register its "
                            "details here — no Cloudflare login needed.",
                 font=FS, bg=CARD, fg=FG2, wraplength=420, justify="left").grid(
            row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(10,8))

        rows = [
            ("Name",        v_name, "e.g. My Home Worker"),
            ("Worker Host *", v_host, "e.g. myworker.example.workers.dev"),
            ("UUID *",      v_uuid, "the VLESS UUID this worker expects"),
            ("SNI",         v_sni,  "defaults to Worker Host if left blank"),
            ("Path",        v_path, "defaults to /?ed=2560"),
        ]
        for ri, (lbl, var, hint) in enumerate(rows, start=1):
            tk.Label(card, text=lbl, font=FB, bg=CARD, fg=FG1,
                     width=14, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=4, sticky="w")
            ttk.Entry(card, textvariable=var, width=32).grid(
                row=ri, column=1, sticky="ew", padx=(0,4), pady=4)
            tk.Label(card, text=hint, font=FS, bg=CARD, fg=FG3).grid(
                row=ri, column=2, padx=(0,12), pady=4, sticky="w")

        nr = len(rows) + 1
        tk.Label(card, text="Network", font=FB, bg=CARD, fg=FG1,
                 width=14, anchor="w").grid(row=nr, column=0, padx=(12,4), pady=4, sticky="w")
        ttk.Combobox(card, textvariable=v_net, width=10, state="readonly",
                     values=["ws","grpc","h2"]).grid(row=nr, column=1, sticky="w", padx=(0,4), pady=4)
        tk.Label(card, text="Security", font=FB, bg=CARD, fg=FG1,
                 width=14, anchor="w").grid(row=nr+1, column=0, padx=(12,4), pady=4, sticky="w")
        ttk.Combobox(card, textvariable=v_sec, width=10, state="readonly",
                     values=["tls","none"]).grid(row=nr+1, column=1, sticky="w", padx=(0,4), pady=4)

        def do_save():
            host = v_host.get().strip()
            uid  = v_uuid.get().strip()
            if not host or not uid:
                messagebox.showwarning("Missing Fields",
                    "Worker Host and UUID are required.", parent=dlg); return
            fields = {
                "name": v_name.get().strip() or f"Worker {n}",
                "uuid": uid,
                "worker_host": host,
                "sni": v_sni.get().strip() or host,
                "path": v_path.get().strip() or "/?ed=2560",
                "network": v_net.get(), "security": v_sec.get(),
                "source": "manual",
            }
            if editing:
                # Update the existing entry in place, keeping any deploy
                # metadata (status / latency / last_check) it already had.
                self.P.cf_workers[edit_idx].update(fields)
                msg_name = self.P.cf_workers[edit_idx]["name"]
                verb = "Updated"
            else:
                self.P.cf_workers.append({
                    # No email/api_key/acct_id — this entry was never deployed
                    # by us, so Deploy will correctly refuse it; Use/Check
                    # work fine since they only need host+uuid.
                    "email": "", "api_key": "", "acct_id": "", "script_name": "",
                    "proxy_ip": "", "use_domain": False, "domain": "", "zone_id": "",
                    "status": "ok", "latency_ms": None, "last_check": "",
                    **fields,
                })
                msg_name = self.P.cf_workers[-1]["name"]
                verb = "Registered"
            save_profiles(self.profiles, self._prof_idx)
            self._cfw_refresh_tree()
            self._cfw_status_var.set(
                f"✔ {verb} '{msg_name}' ({host}). "
                "Click 'Use' to apply it to Config tab, or 'Check' to verify it's alive.")
            self._cfw_log_write(f"📥 {verb} worker: {host}")
            dlg.destroy()
            # Jump straight to the Worker Pool tab after registering details.
            try: self._show("wpool")
            except Exception: pass

        bf = tk.Frame(dlg, bg=BG); bf.pack(pady=(4,12))
        _abtn(bf, "Save" if editing else "Add", do_save, color=PURPLE).pack(side=tk.LEFT, padx=6)
        _gbtn(bf, "Cancel", dlg.destroy).pack(side=tk.LEFT, padx=6)

    def _cfw_import(self):
        """Import a previously exported worker-pool JSON into the current
        pool. Duplicates (same worker_host + uuid) are skipped."""
        path = filedialog.askopenfilename(
            title="Import Worker Pool",
            filetypes=[("Worker Pool","*.veopool"),("JSON","*.json"),
                       ("All","*.*")], parent=self.root)
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            # Auto-detects the obfuscated VEOPOOL1 format and decodes it;
            # also still accepts legacy plain-JSON exports.
            data = _pool_decode(raw_text)
        except Exception as e:
            messagebox.showerror("Import Failed",
                f"Could not read / decode this pool file.\n\n{e}",
                parent=self.root); return
        if isinstance(data, dict) and "cf_workers" in data:
            data = data["cf_workers"]
        if not isinstance(data, list):
            messagebox.showerror("Import Failed",
                "File is not a worker pool (expected a JSON list).", parent=self.root); return
        existing = {(t.get("worker_host",""), t.get("uuid","")) for t in self.P.cf_workers}
        added = 0
        for t in data:
            if not isinstance(t, dict):
                continue
            key = (t.get("worker_host",""), t.get("uuid",""))
            if key in existing and key != ("",""):
                continue
            t.setdefault("source", "imported")
            t.setdefault("status", "ok" if t.get("worker_host") else "new")
            t.setdefault("latency_ms", None)
            t.setdefault("last_check", "")
            self.P.cf_workers.append(t)
            existing.add(key)
            added += 1
        save_profiles(self.profiles, self._prof_idx)
        self._cfw_refresh_tree()
        self._cfw_status_var.set(f"✔ Imported {added} new worker(s) from {path}")
        self._cfw_log_write(f"📥 Imported {added} worker(s) from {path}")
        messagebox.showinfo("Import Complete",
            f"Imported {added} new worker(s)." , parent=self.root)

    def _cfw_export(self):
        if not self.P.cf_workers:
            messagebox.showinfo("Nothing to Export",
                "The pool is empty — add a worker first.", parent=self.root); return

        has_creds = any(t.get("api_key") for t in self.P.cf_workers)
        if has_creds:
            proceed = messagebox.askyesno(
                "Export Includes Credentials",
                "Some entries in this pool carry Cloudflare credentials "
                "(API key / email) from 'Add Target'.\n\n"
                "The exported file is OBFUSCATED (not human-readable) so the "
                "credentials aren't sitting in clear text — but this is light "
                "obfuscation, not strong encryption. Keep the file secure and "
                "only import it back into this app.\n\nContinue?",
                parent=self.root)
            if not proceed:
                return

        path = filedialog.asksaveasfilename(
            defaultextension=".veopool",
            initialfile=f"{self.P.name}_cf_workers_pool.veopool",
            filetypes=[("Worker Pool","*.veopool"),("JSON","*.json"),
                       ("All","*.*")], parent=self.root)
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                # Obfuscated, non-human-readable form (see _pool_encode).
                # .json paths are still written obfuscated; import auto-detects.
                f.write(_pool_encode(self.P.cf_workers))
            self._cfw_log_write(
                f"📤 Exported {len(self.P.cf_workers)} worker(s) (encoded) → {path}")
            self._cfw_status_var.set(
                f"✔ Exported {len(self.P.cf_workers)} worker(s) (encoded) to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e), parent=self.root)

    def _cfw_add_target(self, edit_idx=None):
        editing = edit_idx is not None and 0 <= edit_idx < len(self.P.cf_workers)
        cur = self.P.cf_workers[edit_idx] if editing else {}
        dlg = tk.Toplevel(self.root)
        dlg.title("Edit CF Worker Target" if editing else "Add CF Worker Target")
        dlg.resizable(False, False)
        dlg.configure(bg=BG)
        dlg.grab_set()

        n = len(self.P.cf_workers) + 1
        v_name   = tk.StringVar(value=cur.get("name", f"Worker {n}"))
        v_email  = tk.StringVar(value=cur.get("email", ""))
        v_key    = tk.StringVar(value=cur.get("api_key", ""))
        v_acct   = tk.StringVar(value=cur.get("acct_id", ""))
        v_script = tk.StringVar(value=cur.get("script_name", "") or f"my-vless-core-{n}")
        v_uuid   = tk.StringVar(value=cur.get("uuid", "") or str(_uuid_mod.uuid4()))
        v_proxy  = tk.StringVar(value=cur.get("proxy_ip", ""))
        v_use_dom= tk.BooleanVar(value=bool(cur.get("use_domain", False)))
        v_domain = tk.StringVar(value=cur.get("domain", ""))
        v_zone   = tk.StringVar(value=cur.get("zone_id", ""))

        card = _card(dlg); card.pack(padx=16, pady=12, fill=tk.X)
        card.columnconfigure(1, weight=1)

        rows = [
            ("Name",             v_name,   False, ""),
            ("CF Email *",       v_email,  False, "Cloudflare account email"),
            ("Global API Key *", v_key,    True,  "Profile → API Tokens → Global API Key"),
            ("Account ID *",     v_acct,   False, "CF Dashboard — right sidebar"),
            ("Worker Name *",    v_script, False, "letters / numbers / hyphens"),
            ("UUID",             v_uuid,   False, "auto-generated — change if needed"),
            ("Proxy IP",         v_proxy,  False, "optional fallback host:port"),
        ]
        for ri, (lbl, var, secret, hint) in enumerate(rows):
            tk.Label(card, text=lbl, font=FB, bg=CARD, fg=FG1,
                     width=16, anchor="w").grid(row=ri, column=0, padx=(12,4), pady=4, sticky="w")
            ttk.Entry(card, textvariable=var,
                      show="•" if secret else "", width=32).grid(
                row=ri, column=1, sticky="ew", padx=(0,4), pady=4)
            if hint:
                tk.Label(card, text=hint, font=FS, bg=CARD, fg=FG3).grid(
                    row=ri, column=2, padx=(0,12), pady=4, sticky="w")

        dr = len(rows)
        ttk.Checkbutton(card, variable=v_use_dom,
                        text="Also route a custom domain"
                        ).grid(row=dr, column=0, columnspan=3, sticky="w", padx=12, pady=(8,2))
        tk.Label(card, text="Domain", font=FB, bg=CARD, fg=FG1,
                 width=16, anchor="w").grid(row=dr+1, column=0, padx=(12,4), pady=4, sticky="w")
        ttk.Entry(card, textvariable=v_domain, width=32).grid(
            row=dr+1, column=1, sticky="ew", padx=(0,4), pady=4)
        tk.Label(card, text="e.g. vpn.example.com", font=FS, bg=CARD, fg=FG3).grid(
            row=dr+1, column=2, padx=(0,12), pady=4, sticky="w")
        tk.Label(card, text="Zone ID", font=FB, bg=CARD, fg=FG1,
                 width=16, anchor="w").grid(row=dr+2, column=0, padx=(12,4), pady=4, sticky="w")
        ttk.Entry(card, textvariable=v_zone, width=32).grid(
            row=dr+2, column=1, sticky="ew", padx=(0,4), pady=4)

        hl = tk.Label(dlg, text="→ Get Email / API Key / Account ID from Cloudflare dashboard",
                      font=FS, bg=BG, fg=BLUE, cursor="hand2")
        hl.pack(anchor="w", padx=16)
        hl.bind("<Button-1>", lambda _e: self._open_url(
            "https://dash.cloudflare.com/profile/api-tokens"))

        def do_save():
            import re as _re
            email = v_email.get().strip()
            key   = v_key.get().strip()
            acct  = v_acct.get().strip()
            script= v_script.get().strip()
            if not all([email, key, acct, script]):
                messagebox.showwarning("Missing Fields",
                    "Fill in: CF Email, Global API Key, Account ID and Worker Name.",
                    parent=dlg); return
            if not _re.match(r'^[a-z0-9][a-z0-9\-]{0,61}[a-z0-9]$', script, _re.I):
                messagebox.showwarning("Invalid Worker Name",
                    "Worker name: 2–63 chars, letters/numbers/hyphens.",
                    parent=dlg); return
            fields = {
                "name":       v_name.get().strip() or f"Worker {n}",
                "email":      email, "api_key": key, "acct_id": acct,
                "script_name": script,
                "uuid":       v_uuid.get().strip() or str(_uuid_mod.uuid4()),
                "proxy_ip":   v_proxy.get().strip(),
                "use_domain": v_use_dom.get(),
                "domain":     v_domain.get().strip(),
                "zone_id":    v_zone.get().strip(),
            }
            if editing:
                # Keep worker_host / status / latency the deployed entry already has.
                self.P.cf_workers[edit_idx].update(fields)
                msg_name = self.P.cf_workers[edit_idx]["name"]
                verb = "Updated"
            else:
                self.P.cf_workers.append({
                    "worker_host": "", "status": "new",
                    "latency_ms": None, "last_check": "",
                    "source": "cfworker",
                    **fields,
                })
                msg_name = self.P.cf_workers[-1]["name"]
                verb = "Added"
            save_profiles(self.profiles, self._prof_idx)
            self._cfw_refresh_tree()
            self._cfw_status_var.set(
                f"{verb} '{msg_name}'. Select it and click Deploy.")
            dlg.destroy()
            # Jump straight to the Worker Pool tab so the new target is
            # ready to Deploy / Check / Use right after entering its details.
            try: self._show("wpool")
            except Exception: pass

        bf = tk.Frame(dlg, bg=BG); bf.pack(pady=(4,12))
        _abtn(bf, "Save" if editing else "Add", do_save).pack(side=tk.LEFT, padx=6)
        _gbtn(bf, "Cancel", dlg.destroy).pack(side=tk.LEFT, padx=6)

    def _cfw_edit_selected(self):
        """Edit the selected worker. Opens the SAME dialog it was created
        with: 'Add Worker' (manual entries) or 'Add Target' (entries that
        carry Cloudflare deploy credentials), pre-filled with its values."""
        sel = self._cfw_tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a worker to edit.", parent=self.root); return
        idx = int(sel[0])
        t = self.P.cf_workers[idx]
        # Manual "Add Worker" entries are tagged source=="manual" and carry no
        # API key; everything else came from "Add Target" (has deploy creds).
        if t.get("source") == "manual" or not t.get("api_key"):
            self._cfw_add_worker(edit_idx=idx)
        else:
            self._cfw_add_target(edit_idx=idx)

    def _cfw_remove_selected(self):
        sel = self._cfw_tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a target first.", parent=self.root); return
        idx = int(sel[0])
        name = self.P.cf_workers[idx].get("name","")
        if not messagebox.askyesno("Remove Target",
                                   f"Remove '{name}' from the pool?", parent=self.root): return
        del self.P.cf_workers[idx]
        save_profiles(self.profiles, self._prof_idx)
        self._cfw_refresh_tree()

    def _cfw_deploy_selected(self):
        sel = self._cfw_tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a target first.", parent=self.root); return
        self._cfw_deploy_targets([int(sel[0])])

    def _cfw_deploy_all(self):
        if not self.P.cf_workers:
            messagebox.showinfo("No Targets", "Add a target first.", parent=self.root); return
        self._cfw_deploy_targets(list(range(len(self.P.cf_workers))))

    def _cfw_deploy_targets(self, indices):
        for idx in indices:
            self.P.cf_workers[idx]["status"] = "deploying"
        self._cfw_refresh_tree()
        self._cfw_status_var.set(f"Deploying {len(indices)} worker(s)…")
        threading.Thread(
            target=self._cfw_deploy_thread, args=(indices,), daemon=True).start()

    def _cfw_deploy_thread(self, indices):
        for idx in indices:
            try: target = deepcopy(self.P.cf_workers[idx])
            except Exception: continue
            result = _cfworker_deploy(target, self.q)
            self.q.put(("cfw_deploy_done", idx, result))

    def _cfw_healthcheck_selected(self):
        sel = self._cfw_tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a target first.", parent=self.root); return
        self._cfw_healthcheck_targets([int(sel[0])])

    def _cfw_healthcheck_all(self):
        idxs = [i for i, t in enumerate(self.P.cf_workers) if t.get("worker_host")]
        if not idxs:
            messagebox.showinfo("Nothing to Check",
                                "Deploy at least one worker first.", parent=self.root); return
        self._cfw_healthcheck_targets(idxs)

    def _cfw_healthcheck_targets(self, indices):
        indices = [i for i in indices if self.P.cf_workers[i].get("worker_host")]
        if not indices:
            messagebox.showinfo("Not Deployed",
                                "This target has not been deployed yet.", parent=self.root); return
        for idx in indices:
            self.P.cf_workers[idx]["status"] = "checking"
        self._cfw_refresh_tree()
        self._cfw_status_var.set(f"Health-checking {len(indices)} worker(s)…")
        threading.Thread(
            target=self._cfw_healthcheck_thread, args=(indices,), daemon=True).start()

    def _cfw_healthcheck_thread(self, indices):
        for idx in indices:
            try: target = deepcopy(self.P.cf_workers[idx])
            except Exception: continue
            result = _cfworker_healthcheck(target)
            self.q.put(("cfw_health_done", idx, result))

    def _cfw_use_selected(self):
        sel = self._cfw_tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a target first.", parent=self.root); return
        idx = int(sel[0])
        t   = self.P.cf_workers[idx]
        if not t.get("worker_host"):
            messagebox.showwarning("Not Deployed",
                                   "Deploy this worker first.", parent=self.root); return
        host = t["worker_host"]
        self.uid_var.set(t["uuid"])
        self.host_var.set(host)
        # Add Worker entries carry their own sni/path/network/security;
        # Add Target/deployed entries don't store these, so fall back to
        # the existing defaults for those.
        self.sni_var.set(t.get("sni") or host)
        self.path_var.set(t.get("path") or "/?ed=2560")
        self.net_var.set(t.get("network") or "ws")
        self.sec_var.set(t.get("security") or "tls")
        self.name_var.set(t.get("name") or "CF-Worker")
        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        self._refresh_home()
        self._cfw_status_var.set(
            f"✔ Config tab now points at '{t.get('name')}' ({t['worker_host']}). "
            f"Run a Scan to find the best edge IPs.")
        self._cfw_log_write(
            f"✔ Using '{t.get('name')}' → host={t['worker_host']}  uuid={t['uuid']}")
        messagebox.showinfo("Config Updated",
            f"Config tab updated:\n"
            f"  Host / SNI : {t['worker_host']}\n"
            f"  UUID       : {t['uuid']}\n"
            f"  Path       : /?ed=2560\n\n"
            "Now run a Scan to find the fastest Cloudflare edge IPs for this worker.",
            parent=self.root)
        self._show("config")

    def _build_log(self):
        lf = self.pages["log"]
        lf.rowconfigure(0, weight=0)   # only the log area (row 1) stretches
        lf.rowconfigure(1, weight=1)
        top = tk.Frame(lf, bg=BG); top.grid(row=0, column=0, sticky="w", pady=(0,6))
        self._dbg_en = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Live update",
                        variable=self._dbg_en,
                        command=self._toggle_debug).pack(side=tk.LEFT, padx=(0,8))
        _gbtn(top, "Clear", lambda: [self._log_text.configure(state="normal"),
                                     self._log_text.delete("1.0",tk.END),
                                     self._log_text.configure(state="disabled")],
              True).pack(side=tk.LEFT, padx=(0,6))
        _gbtn(top, "Save", self._save_log, True).pack(side=tk.LEFT)
        tk.Label(top, text="Internal app debug / error output",
                 font=FS, bg=BG, fg=FG3).pack(side=tk.LEFT, padx=10)

        self._log_text = tk.Text(lf, wrap="word", state="disabled", height=10,
                                 bg="#0d1117", fg="#c0caf5", font=FM, relief="flat",
                                 bd=0, insertbackground="#c0caf5",
                                 selectbackground=ACCENT,
                                 padx=8, pady=4)
        self._log_text.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        vsb = ttk.Scrollbar(lf, orient="vertical", command=self._log_text.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self._log_text.configure(yscrollcommand=vsb.set)

    # ══════════════════════════════════════════════════════
    #  Queue polling
    # ══════════════════════════════════════════════════════

    def _poll_q(self):
        # Process at most MAX_PER_TICK messages per tick so the Tkinter event
        # loop stays responsive even when many items are queued (e.g. during
        # a xray log storm).  Remaining items are processed in the next tick.
        MAX_PER_TICK = 40
        processed = 0
        try:
            while processed < MAX_PER_TICK:
                self._handle(self.q.get_nowait())
                processed += 1
        except queue.Empty: pass
        self.root.after(80, self._poll_q)

    def _handle(self, msg):
        if not msg: return
        cmd = msg[0]
        if   cmd == "log":      self._logui(msg[1])
        elif cmd == "debug":
            self.debug_buf.append(msg[1])
            if self._dbg_en.get():
                self._log_text.configure(state="normal")
                self._log_text.insert(tk.END, msg[1]+"\n")
                self._log_text.see(tk.END)
                self._log_text.configure(state="disabled")
        elif cmd == "connlog":  self._append_connlog(msg[1])
        elif cmd == "status":   self._stat_var.set(msg[1])
        elif cmd == "prog_max": self._progress.configure(maximum=msg[1], value=0)
        elif cmd == "prog":     self._progress.configure(value=msg[1])
        elif cmd == "test_prog_max":
            self._test_prog.configure(maximum=msg[1], value=0)
            try: self._test_status_lbl.config(text=f"0 / {msg[1]}", fg=ORANGE)
            except Exception: pass
        elif cmd == "test_prog":
            self._test_prog.configure(value=msg[1])
            try:
                mx = self._test_prog["maximum"] or 1
                self._test_status_lbl.config(
                    text=f"{int(msg[1])} / {int(mx)}", fg=ORANGE)
            except Exception: pass
        elif cmd == "results":
            self.P.results    = msg[1]
            self.P.scanned    = msg[2]
            self.P.scan_time  = msg[3]
            self.P.range_name = msg[4]
            self._sr_limit = 9999
            # New scan → reset test section so stale tree never leaks across scans
            self.P.built_configs = []
            try:
                self._test_btn.config(state=tk.DISABLED)
                self._test_prog.configure(value=0)
                self._test_status_lbl.config(text="")
            except Exception:
                pass
            save_profiles(self.profiles, self._prof_idx)
            self._update_tab_states()
            self._refresh_home()
            self._refresh_scanresult()
            self._refresh_test_tree()     # keep test tree in sync with results
            self._refresh_connect_combo()
            try: self._refresh_history()
            except Exception: pass
            if self.P.has_config and msg[1]:
                best = msg[1][0]
                self.optimized_var.set(self._vless(best.ip, best.port))
        elif cmd == "scan_done":
            self._scan_btn.config(state=tk.NORMAL, bg=ACCENT)
            self._scan_stop_btn.config(state=tk.DISABLED)
            try:
                verified_count = getattr(self.P, "passed_count", len([r for r in self.P.results if r.ping_ms is not None]))
                # Record the config Host/SNI this scan was run against so the
                # history combo can distinguish scans of different workers.
                try:
                    cfg_host = (self.host_var.get().strip()
                                or self.sni_var.get().strip())
                except Exception:
                    cfg_host = ""
                entry = {"time": self.P.scan_time, "range_name": self.P.range_name,
                         "range_raw": self.P.range_raw, "mode": self.P.mode,
                         "scanned": self.P.scanned,
                         "found": verified_count,
                         "host": cfg_host,
                         "cfg_name": getattr(self.P, "cfg_name", ""),
                         "results": [r.to_dict() for r in self.P.results]}
                # Don't save 0 found scans to history
                if verified_count > 0:
                    self.P.scan_history.insert(0, entry)
                    self.P.scan_history = self.P.scan_history[:20]
                    save_profiles(self.profiles, self._prof_idx)
                    self._refresh_history_combo()
                    try: self._refresh_pool_count()  # sync test-tab count
                    except Exception: pass
            except Exception: pass
            found = getattr(self.P, "passed_count",
                            len([r for r in self.P.results if r.ping_ms is not None]))
            rng   = self.P.range_name
            mode  = {"tcp":"TCP","tls":"TLS-Handshake","http":"HTTP+TLS+SNI"}.get(
                        self.P.mode, self.P.mode.upper())
            total = self.P.scanned
            self._progress.configure(value=0)
            self._stat_var.set(f"Done \u2014 {found} IPs")
            self._logui(f"[SCAN COMPLETE] {total} scanned \u00b7 {found} verified \u00b7 {rng} \u00b7 {mode}")
            # Update status bar
            self._sb_update(
                status="Ready",
                color=FG3,
                scan=f"{found}/{total} IPs  \u00b7  {rng[:30]}")
            # alert
            colos  = [r.colo for r in self.P.results if r.colo]
            cf_cnt = sum(1 for r in self.P.results if r.cf_valid)
            top_colos = ", ".join(
                f"{c}({colos.count(c)})" for c in
                sorted(set(colos), key=lambda x: -colos.count(x))[:5]
            ) if colos else "—"
            avg_ping = (sum(r.ping_ms for r in self.P.results if r.ping_ms) /
                        max(1, sum(1 for r in self.P.results if r.ping_ms)))
            avg_loss = (sum(r.loss_pct for r in self.P.results if r.loss_pct is not None) /
                        max(1, sum(1 for r in self.P.results if r.loss_pct is not None)))
            was_deep = mode == "HTTP+TLS+SNI"
            messagebox.showinfo(
                "Scan Complete",
                f"{'✔  Config-Aware Scan Complete!' if was_deep else '✔  Scan finished!'}\n\n"
                f"Mode:        {mode}"
                + (" (2-phase: TCP→TLS+SNI verify)" if was_deep else "") + "\n"
                f"Range:       {rng}\n"
                f"Scanned:     {total} targets\n"
                f"{'Config-Verified IPs' if was_deep else 'Working IPs'}: {found}\n"
                + (f"CF Verified: {cf_cnt} IPs\n" if cf_cnt else "")
                + (f"Top Colos:   {top_colos}\n" if top_colos != "—" else "")
                + f"Avg Ping:    {avg_ping:.1f} ms\n"
                f"Avg Loss:    {avg_loss:.1f} %\n\n"
                + ("Go to  📋 Test & Results  tab to generate configs and test them."
                   if self.P.has_config
                   else "Fill Config tab with UUID + Host to enable config mode."),
                parent=self.root
            )
        elif cmd == "test_update":
            self._refresh_test_tree()
            self._refresh_scanresult()
            self._refresh_home()
        elif cmd == "gen_finalize":
            # Background WS re-verify finished — build configs on the UI thread.
            _, survivors, n, dropped = msg
            self._finalize_generate(survivors, n, dropped)

        elif cmd == "test_done":
            self._test_btn.config(state=tk.NORMAL)
            try: self._quick_test_btn.config(state=tk.NORMAL)
            except Exception: pass
            self._test_prog.configure(value=self._test_prog["maximum"])
            self._refresh_home()
            # ── If Generate triggered the ping, auto-build configs now ────────
            if getattr(self, "_auto_generate_after_test", False):
                self._auto_generate_after_test = False
                try: self._test_status_lbl.config(text="Building configs…", fg=TEAL)
                except Exception: pass
                self.root.after(100, self._do_generate_configs)
            else:
                # Normal test_done: just refresh tree + status
                try: self._test_status_lbl.config(text="Done ✔", fg=GREEN)
                except Exception: pass
                self._refresh_test_tree()
                self._refresh_scanresult()
                if self.P.has_config:
                    ok2 = [r for r in self.P.results if r.ping_ms is not None]
                    n2  = int(self._test_n.get())
                    self.P.built_configs = [self._vless(r.ip,r.port) for r in ok2[:n2]]
                    save_profiles(self.profiles, self._prof_idx)
                self._refresh_connect_combo()
                self._refresh_history_combo()  # keep both tab combos in sync
                self._update_tab_states()
        elif cmd == "error":
            self._logui(f"[ERR] {msg[1]}")
            self._stat_var.set("Error")
            self._logdbg(f"ERROR: {msg[1]}")
        elif cmd == "xray_prog":
            try: self._set_xray_lbl.config(text=msg[1], fg=ORANGE)
            except Exception: pass
        elif cmd == "xray_done":
            try:
                self._set_xray_prog.stop()
                self._set_xray_prog.grid_remove()
                if msg[1]:
                    self._set_xray_lbl.config(text=f"✔  Ready: {self.xray.xray_path}", fg=GREEN)
                    self._set_xray_dl_btn.grid_remove()
                    self._logdbg(f"xray downloaded: {self.xray.xray_path}")
                    try: self._update_xray_status_label()
                    except Exception: pass
                else:
                    self._set_xray_lbl.config(text="✖  Download failed — try again", fg=RED_C)
                    self._set_xray_dl_btn.config(state=tk.NORMAL)
                    self._set_xray_prog.grid()
            except Exception: pass
            # update inline status label in combined test tab
            try: self._update_xray_status_label()
            except Exception: pass
        elif cmd == "xray_prog_set":
            try: self._set_xray_lbl.config(text=msg[1], fg=ORANGE)
            except Exception: pass
        elif cmd == "xray_done_set":
            try:
                self._set_xray_prog.stop()
                self._set_xray_prog.grid_remove()
                if msg[1]:
                    self._set_xray_lbl.config(text=f"✔  {self.xray.xray_path}", fg=GREEN)
                    self._set_xray_dl_btn.grid_remove()
                    self._xray_path_var.set(self.xray.xray_path)
                else:
                    self._set_xray_lbl.config(text="✖  Download failed", fg=RED_C)
                    self._set_xray_dl_btn.config(state=tk.NORMAL)
                    self._set_xray_prog.grid()
                # always update the inline status label in Test & Results tab
                try: self._update_xray_status_label()
                except Exception: pass
            except Exception: pass
        elif cmd == "tun_prog":
            try: self._tun_dll_lbl.config(text=msg[1], fg=ORANGE)
            except Exception: pass
        elif cmd == "tun_done":
            ok3, msg3 = msg[1], msg[2]
            try:
                self._tun_dl_prog.stop()
                self._tun_dl_prog.grid_remove()
                if ok3:
                    self._tun_dll_lbl.config(
                        text=f"✔  {self.tun.dll_path}", fg=GREEN)
                    self._tun_dl_btn.grid_remove()
                    self._refresh_tun_label()
                else:
                    self._tun_dll_lbl.config(
                        text=f"✖  {msg3}", fg=RED_C)
                    self._tun_dl_btn.config(state=tk.NORMAL)
                    self._tun_dl_prog.grid()
            except Exception: pass
        elif cmd == "bpb_log":
            try: self._bpb_log_write(msg[1])
            except Exception: pass
        elif cmd == "bpb_status":
            try: self._bpb_set_status(msg[1])
            except Exception: pass
        elif cmd == "bpb_validate_done":
            ok2, txt2 = msg[1], msg[2]
            try:
                self._bpb_validate_btn.config(state=tk.NORMAL, text="✔ Validate Creds")
                self._bpb_log_write(f"Validation: {txt2}")
                if ok2:
                    messagebox.showinfo("Credentials OK", f"✔  {txt2}", parent=self.root)
                else:
                    messagebox.showerror("Credentials Failed", f"✖  {txt2}", parent=self.root)
            except Exception: pass
        elif cmd == "bpb_done":
            result2 = msg[1]
            try:
                self._bpb_prog.stop(); self._bpb_prog.grid_remove()
                self._bpb_deploy_btn.config(state=tk.NORMAL, text="🚀  Deploy")
                self._bpb_validate_btn.config(state=tk.NORMAL)
                if result2.get("success"):
                    self._bpb_set_status("✅ Deployment complete!")
                    self._bpb_show_result(result2)
                    # Auto-switch to the Worker Pool tab so the freshly built
                    # worker is shown alongside the rest of the pool.
                    try: self._show("wpool")
                    except Exception: pass
                else:
                    self._bpb_set_status(f"✖ Failed: {result2.get('error','')}")
                    messagebox.showerror("Deployment Failed",
                        result2.get("error","Unknown error"), parent=self.root)
            except Exception as ex2:
                self._logdbg(f"bpb_done error: {ex2}")
        elif cmd == "cfw_deploy_done":
            _, idx, res = msg
            try:
                pool = self.P.cf_workers
                if 0 <= idx < len(pool):
                    t = pool[idx]
                    if res.get("success"):
                        t["worker_host"] = res.get("worker_host","")
                        t["status"]      = "ok"
                        t["latency_ms"]  = res.get("latency_ms")
                        t["last_check"]  = time.strftime("%H:%M:%S")
                        lat_s = f"  ({t['latency_ms']:.0f}ms)" if t["latency_ms"] else ""
                        self._cfw_log_write(
                            f"✔ Deployed '{t.get('name')}' → {t['worker_host']}{lat_s}")
                        self._cfw_status_var.set(
                            f"✔ '{t.get('name')}' deployed at {t['worker_host']}. "
                            f"Click 'Use' to apply to Config tab.")
                    else:
                        t["status"] = "error"
                        err = res.get("error","unknown")
                        self._cfw_log_write(f"✖ Deploy failed for target #{idx}: {err}")
                        self._cfw_status_var.set(f"✖ Deploy failed: {err}")
                    save_profiles(self.profiles, self._prof_idx)
                    self._cfw_refresh_tree()
            except Exception as ex2:
                self._logdbg(f"cfw_deploy_done error: {ex2}")
        elif cmd == "cfw_health_done":
            _, idx, res = msg
            try:
                pool = self.P.cf_workers
                if 0 <= idx < len(pool):
                    t = pool[idx]
                    if res.get("ok"):
                        t["status"]     = "ok"
                        t["latency_ms"] = res.get("latency_ms")
                        t["last_check"] = time.strftime("%H:%M:%S")
                        lat_s = f"{t['latency_ms']:.0f}ms" if t["latency_ms"] is not None else "?"
                        self._cfw_log_write(
                            f"💓 '{t.get('name')}' alive  {lat_s}  ({t['worker_host']})")
                        self._cfw_status_var.set(
                            f"💓 '{t.get('name')}' OK — {lat_s}.")
                    else:
                        t["status"]     = "down"
                        t["latency_ms"] = None
                        t["last_check"] = time.strftime("%H:%M:%S")
                        err = res.get("error","no response")
                        self._cfw_log_write(f"✖ '{t.get('name')}' DOWN — {err}")
                        self._cfw_status_var.set(
                            f"✖ '{t.get('name')}' not responding: {err}")
                    save_profiles(self.profiles, self._prof_idx)
                    self._cfw_refresh_tree()
            except Exception as ex2:
                self._logdbg(f"cfw_health_done error: {ex2}")
        elif cmd == "cfw_log":
            try: self._cfw_log_write(msg[1])
            except Exception: pass
        elif cmd == "bw_dl":    self._dl_var.set(msg[1])
        elif cmd == "bw_ul":    self._ul_var.set(msg[1])
        elif cmd == "bw_lat":
            self._lat_var.set(msg[1])
            # Also update status bar latency
            try: self._sb_update(lat=msg[1])
            except Exception: pass
        elif cmd == "scan_passed":
            self.P.passed_count = msg[1]
        elif cmd == "bw_traffic":
            ul_total = msg[1]; dl_total = msg[2]
            has_speed = len(msg) >= 5
            ul_spd = msg[3] if has_speed else 0.0
            dl_spd = msg[4] if has_speed else 0.0
            if has_speed:
                self._bw_hist_ul.append(ul_spd)
                self._bw_hist_dl.append(dl_spd)
                self._draw_bw_chart()
            self._ul_var.set(_fmt_bytes(ul_total))
            self._dl_var.set(_fmt_bytes(dl_total))
            if has_speed and (ul_spd or dl_spd):
                self._ul_spd_var.set(_fmt_speed(ul_spd))
                self._dl_spd_var.set(_fmt_speed(dl_spd))
            else:
                self._ul_spd_var.set("")
                self._dl_spd_var.set("")
            # Update status bar with live speeds
            try:
                self._sb_update(
                    ul=_fmt_speed_short(ul_spd or 0) + "/s",
                    dl=_fmt_speed_short(dl_spd or 0) + "/s")
            except Exception:
                pass
        elif cmd == "tun_start_bw":
            # msg = ("tun_start_bw", stats_port)
            # Fired from _add_routes thread once TUN adapter + routes are confirmed.
            # proxy_url=None because TUN mode tunnels at OS level — no proxy needed.
            self._start_bw_meter(None, stats_port=msg[1], tun_mode=True)
        elif cmd == "test_conn_result":
            # msg = ("test_conn_result", summary_str, ok_bool)
            ok = msg[2]
            self._test_conn_result.config(
                text=msg[1],
                fg=GREEN if ok else RED_C)
            self._test_conn_btn.config(state=tk.NORMAL, text="🔍 Test Connection")
        elif cmd == "switch_status": self._switch_lbl.config(text=msg[1], fg=TEAL)
        elif cmd == "px_connected":
            ip, port, sk, ht = msg[1], msg[2], msg[3], msg[4]
            self._px_status_lbl.config(
                text=f"\u25cf Auto-Switch Connected \u2192 {ip}:{port}  SOCKS5:{sk} HTTP:{ht}",
                fg=GREEN)
            proxy_url = f"http://127.0.0.1:{ht}"
            self._bw_proxy_url  = proxy_url
            self._bw_stats_port = getattr(self, "_bw_stats_port", None)
            self._session_ul_bytes = 0
            self._session_dl_bytes = 0
            self._ul_var.set("0 B"); self._dl_var.set("0 B")
            self._ul_spd_var.set(""); self._dl_spd_var.set("")
            self._bw_hist_ul.clear(); self._bw_hist_dl.clear()
            self._draw_bw_chart()
            self._start_bw_meter(proxy_url, stats_port=self._bw_stats_port)
            # Update status bar
            self._sb_update(
                status="Connected",
                color=GREEN,
                server=f"{ip}:{port}",
                ul="0 B", dl="0 B")
        elif cmd == "px_disconnected":
            self._px_start.config(state=tk.NORMAL)
            self._px_stop.config(state=tk.DISABLED)
            self._px_status_lbl.config(text="\u25cf Disconnected", fg=FG3)
            self._ul_var.set("\u2014"); self._dl_var.set("\u2014"); self._lat_var.set("\u2014")
            self._ul_spd_var.set(""); self._dl_spd_var.set("")
            self._bw_hist_ul.clear(); self._bw_hist_dl.clear()
            self._draw_bw_chart()
            self._switch_lbl.config(text="")
            # Update status bar
            self._sb_update(
                status="Disconnected",
                color=DISCONNECTED,
                server="",
                ul="\u2014", dl="\u2014", lat="\u2014")

    # ══════════════════════════════════════════════════════
    #  Scan actions
    # ══════════════════════════════════════════════════════

    def _on_provider(self, _e=None):
        sel = self.provider_var.get()
        if sel in PROVIDER_RANGES and PROVIDER_RANGES[sel]:
            # Auto-add the selected provider as a tag
            rng = PROVIDER_RANGES[sel]
            if rng not in self._range_tags:
                self._range_tags.append(rng)
                self._refresh_tags()
                self._logui(f"[RANGE] Added: {sel}")
            if "Cloudflare" in sel:
                for v in self.port_vars.values(): v.set(True)
            elif sel != "Custom":
                for p,v in self.port_vars.items(): v.set(p==443)

    def _add_range_tag(self):
        rng = self.range_var.get().strip()
        if not rng:
            return
        if rng not in self._range_tags:
            self._range_tags.append(rng)
            self._refresh_tags()
            self._logui(f"[RANGE] Added: {rng}")
        self.range_var.set("")

    def _remove_range_tag(self, idx: int):
        if 0 <= idx < len(self._range_tags):
            removed = self._range_tags.pop(idx)
            self._refresh_tags()
            self._logui(f"[RANGE] Removed: {removed}")

    def _refresh_tags(self):
        for w in self._tags_container.winfo_children():
            w.destroy()
        if not self._range_tags:
            tk.Label(self._tags_container, text="(no ranges added)",
                     font=FS, bg=CARD, fg=FG4).pack(side=tk.LEFT)
            return
        for i, rng in enumerate(self._range_tags):
            tag_frame = tk.Frame(self._tags_container, bg=BLUE, padx=1, pady=1)
            tag_frame.pack(side=tk.LEFT, padx=2, pady=2)
            inner = tk.Frame(tag_frame, bg="#e3f2fd")
            inner.pack()
            # Truncate long ranges for display
            display = rng if len(rng) <= 30 else rng[:27] + "..."
            tk.Label(inner, text=f" {display} ", font=FS, bg="#e3f2fd", fg=FG1).pack(side=tk.LEFT)
            x_btn = tk.Label(inner, text=" \u2716", font=FS, bg="#e3f2fd", fg=RED_C, cursor="hand2")
            x_btn.pack(side=tk.LEFT)
            x_btn.bind("<Button-1>", lambda e, idx=i: self._remove_range_tag(idx))
            _add_tooltip(tag_frame, f"Click \u2716 to remove: {rng}")

    def _start_scan(self):
        if self.test_thread and self.test_thread.is_alive():
            self._logui("[WARN] Wait for test to finish."); return
        self._activity(f"Scan started (mode={self.mode_var.get()}, "
                       f"threads={self.threads_var.get()})")
        # Combine all tags into one range string
        rng = ",".join(self._range_tags) if self._range_tags else self.range_var.get().strip()
        if not rng:
            self._logui("[ERR] Add at least one IP range tag."); return
        ports = [p for p,v in self.port_vars.items() if v.get()]
        if not ports: self._logui("[ERR] Select at least one port."); return
        self.stop_ev.clear()
        self._scan_btn.config(state=tk.DISABLED, bg=FG3)
        self._scan_stop_btn.config(state=tk.NORMAL)
        self.optimized_var.set("")

        host = self._clean_host(self.host_var.get())
        sni  = self._clean_host(self.sni_var.get()) or host
        rname= (self.provider_var.get()
                if self.provider_var.get()!="Custom" else rng[:40])

        # ── Determine effective probe mode ───────────────────────────
        chosen_mode = self.mode_var.get()
        p = self.P
        has_tls_cfg = (
            p.security == "tls" and bool(sni or host)
        )

        deep_verify = False
        if chosen_mode == "Config-Aware (Auto)":
            if has_tls_cfg:
                eff_mode   = "http"    # TLS+SNI+HTTP — filters ISP-blocked IPs
                deep_verify = True     # two-phase: TCP pre-filter → HTTP config verify
            else:
                eff_mode   = "tcp"     # no TLS config — plain TCP scan
        else:
            eff_mode = {"TCP Connect":"tcp",
                        "TLS Handshake":"tls",
                        "HTTP Request":"http"}.get(chosen_mode, "http")

        # Warn user if they manually chose TCP with a TLS config
        if chosen_mode == "TCP Connect" and has_tls_cfg:
            if not messagebox.askyesno(
                    "⚠ Mode Mismatch",
                    "Your config uses TLS (security=tls), but you selected TCP scan.\n\n"
                    "On filtered ISPs (Irancell, MCI) TCP-only scanning will find IPs "
                    "that fail in the actual proxy because the ISP blocks TLS with your "
                    "Worker domain SNI.\n\n"
                    "Continue with TCP anyway?\n\n"
                    "  Yes → TCP only (fast but inaccurate on filtered ISPs)\n"
                    "  No  → switch to Config-Aware (recommended)",
                    parent=self.root):
                self._scan_btn.config(state=tk.NORMAL, bg=ACCENT)
                self.mode_var.set("Config-Aware (Auto)")
                return

        mode_label = {
            "tcp":  "TCP Connect",
            "tls":  "TLS Handshake",
            "http": "HTTP+TLS+SNI",
        }.get(eff_mode, eff_mode)
        phase_label = " [2-phase: TCP→Config-Verify]" if deep_verify else ""

        args = dict(
            range=rng, ports=ports,
            mode=eff_mode,
            deep_verify=deep_verify,
            path=self._clean_path(self.path_var.get()),
            host=host, sni=sni,
            threads=int(self.threads_var.get()),
            timeout=float(self.timeout_var.get()),
            tries=int(self.tries_var.get()),
            rname=rname,
        )
        self._logui("="*50)
        self._logui(f"[SCAN] mode={mode_label}{phase_label} tries={self.tries_var.get()} "
                    f"ports={ports} range={rng[:60]}")
        if deep_verify:
            self._logui(f"[SCAN] Config-Aware: SNI={sni or '—'}  Host={host or '—'}")
            self._logui(f"[SCAN] Phase 1: TCP pre-filter all targets")
            self._logui(f"[SCAN] Phase 2: TLS+SNI+HTTP verify survivors with your config")
        self.P.results = []; self.P.built_configs = []
        try:
            for i in self._test_tree.get_children(): self._test_tree.delete(i)
            self._sr_limit = 9999; self._refresh_scanresult()
            self._test_prog["value"] = 0
            self._test_status_lbl.config(text="")
        except Exception: pass
        self._save_config_to_profile()
        self.P.range_raw  = rng
        self.P.range_name = rname
        self.P.ports      = ports
        self.P.mode       = eff_mode
        self.P.threads    = args["threads"]
        self.P.timeout    = args["timeout"]
        save_profiles(self.profiles, self._prof_idx)
        self.scan_thread  = threading.Thread(
            target=self._scan_thr, args=(args,), daemon=True)
        self.scan_thread.start()

    def _stop_scan(self):
        self._activity("Scan stopped by user")
        self.stop_ev.set()
        if self._loop and self._loop.is_running():
            try: self._loop.call_soon_threadsafe(
                lambda: [t.cancel() for t in self._tasks if not t.done()])
            except Exception: pass

    def _scan_thr(self, args):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._async_scan(args))
        except asyncio.CancelledError:
            pass  # Scan was stopped by user
        except Exception as e:
            self.q.put(("error", str(e)))
        finally:
            self._loop = None; self._tasks = []
            self.q.put(("scan_done",))

    async def _async_scan(self, args):
        opt     = Optimizer(concurrency=args["threads"], timeout=args["timeout"],
                           tries=args.get("tries", 4))
        ips     = opt.fix_range(args["range"])
        if not ips: self.q.put(("error","No IPs resolved.")); return
        targets = [(ip, p) for ip in ips for p in args["ports"]]
        total   = len(targets)
        self._loop = asyncio.get_running_loop()
        self.q.put(("log", f"IPs={len(ips)} × {len(args['ports'])} ports = {total} targets"))

        ts = time.strftime("%Y-%m-%d %H:%M")

        # ═══════════════════════════════════════════════════════
        #  TWO-PHASE  (Config-Aware mode with TLS config)
        # ═══════════════════════════════════════════════════════
        if args.get("deep_verify"):

            # ── Phase 1: fast TCP pre-filter ──────────────────
            self.q.put(("prog_max", total))
            self.q.put(("status", f"[1/2] TCP scanning {total} targets…"))
            # tries=1, shorter timeout, full concurrency — semaphore kept via probe()
            tcp_opt = Optimizer(concurrency=args["threads"],
                                timeout=min(args["timeout"], 3.0), tries=1)
            done_p1 = 0

            async def tcp_one(ip, port):
                nonlocal done_p1
                if self.stop_ev.is_set(): return None
                # probe() uses the semaphore — never call _tcp() directly for bulk work
                r = await tcp_opt.probe(ip, port, "tcp", sni="", host="", path="/")
                done_p1 += 1
                self.q.put(("prog", done_p1))
                return (ip, port, r.ping_ms) if r.ping_ms is not None else None

            self._tasks = [asyncio.create_task(tcp_one(ip, p)) for ip, p in targets]
            p1_raw    = await asyncio.gather(*self._tasks, return_exceptions=True)
            survivors = sorted(
                [r for r in p1_raw
                 if r and not isinstance(r, BaseException)],
                key=lambda x: x[2])

            self.q.put(("log",
                f"[Phase 1 TCP] {len(survivors)}/{total} alive"))

            if self.stop_ev.is_set() or not survivors:
                self.q.put(("results", [], total, ts, args["rname"]))
                if not survivors:
                    self.q.put(("log",
                        "No TCP-reachable targets — check IP range/ports."))
                return

            # ── Phase 2: config verify (TLS+SNI+HTTP) ─────────
            v2_n   = len(survivors)
            self.q.put(("prog_max", v2_n))
            self.q.put(("status", f"[2/2] Config-verifying {v2_n} IPs…"))
            self.q.put(("log",
                f"[Phase 2 Config-Verify] Testing {v2_n} IPs with "
                f"TLS+SNI={args['sni'] or args['host']}"))

            v2_opt = Optimizer(concurrency=min(args["threads"], 150),
                               timeout=args["timeout"],
                               tries=args.get("tries", 4))
            done_p2 = 0

            async def verify_one(ip, port, _tcp_ms):
                nonlocal done_p2
                if self.stop_ev.is_set():
                    return ProbeResult(ip, port, args["mode"], None, "stopped")
                r = await v2_opt.probe(ip, port, args["mode"],
                                       sni=args["sni"],
                                       host=args["host"],
                                       path=args["path"])
                done_p2 += 1
                self.q.put(("prog", done_p2))
                return r

            self._tasks = [asyncio.create_task(verify_one(ip, port, ms))
                           for ip, port, ms in survivors]
            v2_results = await asyncio.gather(*self._tasks, return_exceptions=True)
            ok = sorted(
                [r for r in v2_results
                 if isinstance(r, ProbeResult) and r.ping_ms is not None],
                key=lambda r: r.ping_ms)

            passed = len(ok)
            blocked = v2_n - passed
            self.q.put(("log",
                f"[Phase 2] {passed}/{v2_n} passed config-verify"
                + (f"  ({blocked} blocked by ISP SNI filter)" if blocked else " \u2014 all clear")))
            self.q.put(("scan_passed", passed))

            # Send full verified list as the pool (no Top-N truncation)
            self.q.put(("results", ok, total, ts, args["rname"]))

            if not ok:
                self.q.put(("log",
                    "⚠  0 IPs passed TLS+SNI verify.\n"
                    "   Likely causes:\n"
                    "   • ISP (Irancell/MCI) is blocking your Worker domain SNI\n"
                    "   • Worker is offline / wrong host in Config tab\n"
                    "   • Try a different port (2053, 2083, 2087, 2096)"))
                self.q.put(("status", "0 config-verified — check SNI / port"))
                return

            best = ok[0]
            self.q.put(("log",
                f"Best → {best.ip}:{best.port}  {best.ping_ms:.1f}ms  "
                f"verified={passed}/{v2_n}"))
            self.q.put(("status", f"Done — {passed} config-verified IPs"))

        # ═══════════════════════════════════════════════════════
        #  SINGLE-PHASE  (TCP / TLS / HTTP — user-selected mode)
        # ═══════════════════════════════════════════════════════
        else:
            self.q.put(("prog_max", total))
            self.q.put(("status", f"Scanning {total} targets…"))
            done = 0

            async def one(ip, port):
                nonlocal done
                if self.stop_ev.is_set():
                    return ProbeResult(ip, port, args["mode"], None, "stopped")
                r = await opt.probe(ip, port, args["mode"],
                                    sni=args["sni"],
                                    host=args["host"],
                                    path=args["path"])
                done += 1; self.q.put(("prog", done)); return r

            self._tasks = [asyncio.create_task(one(ip, p)) for ip, p in targets]
            results     = await asyncio.gather(*self._tasks, return_exceptions=True)
            ok  = sorted(
                [r for r in results
                 if isinstance(r, ProbeResult) and r.ping_ms is not None],
                key=lambda r: r.ping_ms)
            # Send full result list as the pool (no Top-N truncation)
            self.q.put(("results", ok, total, ts, args["rname"]))
            if not ok:
                self.q.put(("log", f"No reachable targets (tried {total})."))
                return
            best = ok[0]
            self.q.put(("log",
                f"Best → {best.ip}:{best.port}  {best.ping_ms:.1f}ms  "
                f"ok={len(ok)}/{total}"))
            self.q.put(("status", f"Done — {len(ok)} IPs found"))

    # ══════════════════════════════════════════════════════
    #  Test actions
    # ══════════════════════════════════════════════════════

    def _start_test(self):
        if self.scan_thread and self.scan_thread.is_alive():
            self._logui("[WARN] Scan running."); return
        ok = [r for r in self.P.results if r.ping_ms is not None]
        if not ok: self._logui("[WARN] No scan results."); return
        self._activity(f"Config test started ({len(ok)} candidates)")
        if not self.P.has_config:
            messagebox.showwarning("Config Missing",
                "Fill UUID + Host in Config tab first.", parent=self.root)
            return
        # xray must be installed for full proxy test
        if not self.xray.is_installed():
            messagebox.showerror(
                "xray-core Not Found",
                "xray-core is required for Full Test.\n\n"
                "Go to  Settings → Xray Core  and click '⬇ Download Xray Core'.\n\n"
                "Alternatively, use  ⚡ Quick Test  for a fast TCP check that does not need xray.",
                parent=self.root)
            return
        self.stop_ev.clear()
        n    = int(self._test_n.get())
        tgts = ok[:n]
        self.q.put(("test_prog_max", len(tgts)))
        self._test_btn.config(state=tk.DISABLED)
        self._logdbg(f"Testing top {len(tgts)} — config={self.P.has_config}")
        self.test_thread = threading.Thread(
            target=self._test_thr, args=(tgts,), daemon=True)
        self.test_thread.start()

    def _stop_test(self):
        self._activity("Test stopped by user")
        self.stop_ev.set()
        if self._loop and self._loop.is_running():
            try: self._loop.call_soon_threadsafe(
                lambda: [t.cancel() for t in self._tasks if not t.done()])
            except Exception: pass

    # ── Quick Test ─────────────────────────────────────────────────

    def _quick_test(self):
        if self.scan_thread and self.scan_thread.is_alive():
            self._logui("[WARN] Scan is running."); return
        self._activity("Quick test started")
        if self.test_thread and self.test_thread.is_alive():
            self._logui("[WARN] Test already running."); return
        ok = [r for r in self.P.results if r.ping_ms is not None]
        if not ok:
            messagebox.showwarning("No Results",
                "Run a scan first to get IPs.", parent=self.root)
            return
        n    = int(self._test_n.get())
        tgts = ok[:n]
        self.stop_ev.clear()
        self.q.put(("test_prog_max", len(tgts)))
        self._test_btn.config(state=tk.DISABLED)
        self._quick_test_btn.config(state=tk.DISABLED)
        self._test_status_lbl.config(text=f"Quick-checking {len(tgts)} IPs…", fg=ORANGE)
        self._logui(f"[QUICK TEST] TCP re-check of top {len(tgts)} IPs…")

        p    = self.P
        mode = p.mode or "http"
        sni  = p.sni  or p.host or ""
        host = p.host or ""
        path = p.path or "/"

        self.test_thread = threading.Thread(
            target=self._quick_test_thr,
            args=(tgts, mode, sni, host, path),
            daemon=True)
        self.test_thread.start()

    def _quick_test_thr(self, tgts, mode, sni, host, path):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                self._async_quick_test(tgts, mode, sni, host, path))
        except asyncio.CancelledError:
            pass  # Test was stopped by user
        except Exception as e:
            self.q.put(("error", f"Quick Test: {e}"))
        finally:
            self._loop = None; self._tasks = []
            self.q.put(("test_done",))

    async def _async_quick_test(self, tgts, mode, sni, host, path):
        self._loop = asyncio.get_running_loop()
        # Test ONE IP at a time (concurrency=1). Running many probes in
        # parallel saturates the uplink and inflates ping/jitter/latency,
        # and also freezes the UI. tries=3 gives real jitter + loss%.
        opt  = Optimizer(concurrency=1, timeout=3.0, tries=3)
        done = 0
        self._tasks = []

        async def check_one(r: ProbeResult):
            nonlocal done
            if self.stop_ev.is_set():
                r.error = "stopped"; return
            fresh = await opt.probe(r.ip, r.port, mode,
                                    sni=sni, host=host, path=path)
            if fresh.ping_ms is not None:
                r.ping_ms   = fresh.ping_ms
                r.jitter_ms = fresh.jitter_ms
                r.loss_pct  = fresh.loss_pct
                r.colo      = fresh.colo   or r.colo
                r.cf_valid  = fresh.cf_valid or r.cf_valid
                r.error     = None
            else:
                r.error = fresh.error or "tcp-fail"
            r.tested = True
            done += 1
            self.q.put(("test_prog", done))
            self.q.put(("test_update",))

        # Sequential one-by-one loop (NOT asyncio.gather) for accurate metrics
        for r in tgts:
            if self.stop_ev.is_set():
                break
            await check_one(r)
        # re-sort by ping after quick test
        alive  = [r for r in self.P.results if r.ping_ms is not None]
        dead   = [r for r in self.P.results if r.ping_ms is None]
        alive.sort(key=lambda r: r.ping_ms or 1e9)
        self.P.results = alive + dead

    def _test_thr(self, tgts):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._async_tests(tgts))
        except Exception as e:
            self.q.put(("error", f"Test: {e}"))
        finally:
            self._loop = None; self._tasks = []
            self.q.put(("test_done",))

    async def _async_tests(self, tgts: List[ProbeResult]):
        self._loop = asyncio.get_running_loop()
        p      = self.P
        uid    = p.uid
        host   = p.host or ""
        sni    = p.sni  or host
        path   = p.path or "/"
        done   = 0

        async def test_one(r: ProbeResult):
            nonlocal done
            if self.stop_ev.is_set():
                r.error="stopped"; return
            t0 = time.perf_counter()
            try:
                _,w = await asyncio.wait_for(
                    asyncio.open_connection(r.ip,r.port), timeout=5)
                w.close()
                try: await asyncio.wait_for(w.wait_closed(),1)
                except Exception: pass
                r.tcp_ms = (time.perf_counter()-t0)*1000
            except Exception: r.tcp_ms = None
            r.icmp_ms,_ = await self._loop.run_in_executor(
                None, XrayManager.icmp, r.ip)
            if p.has_config and self.xray.is_installed():
                lp  = XrayManager.get_free_port()
                cfg = XrayManager.build_test(r.ip, r.port, uid, host, sni, path, lp, p)
                fd,cp = tempfile.mkstemp(suffix=".json")
                with os.fdopen(fd,"w") as f: json.dump(cfg,f)
                proc = None
                try:
                    kw: dict = {}
                    if sys.platform=="win32":
                        kw["creationflags"]=subprocess.CREATE_NO_WINDOW
                    proc = subprocess.Popen(
                        [self.xray.xray_path,"-c",cp],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE, **kw)
                    await asyncio.sleep(1.5)
                    if proc.poll() is None:
                        proxy = f"http://127.0.0.1:{lp}"
                        r.lat_ms,_ = await self._loop.run_in_executor(
                            None, XrayManager.latency, proxy)
                        if r.lat_ms is not None:
                            r.dl_mbps,_ = await self._loop.run_in_executor(
                                None, XrayManager.dl_speed, proxy)
                            r.up_mbps,_ = await self._loop.run_in_executor(
                                None, XrayManager.up_speed, proxy)
                    else:
                        self._logdbg(f"xray early exit {r.ip}")
                except Exception as ex:
                    self._logdbg(f"test_one {r.ip}: {ex}")
                finally:
                    if proc:
                        try: proc.terminate(); proc.wait(timeout=3)
                        except Exception:
                            try: proc.kill()
                            except Exception: pass
                    try: os.remove(cp)
                    except Exception: pass
            r.tested = True
            done += 1
            self.q.put(("test_prog", done))
            self.q.put(("test_update",))

        self._tasks = []
        # Sequential one-by-one loop: only ONE xray instance runs at a time
        # so latency + download/upload speed are measured on a clean link.
        # Running every config in parallel made them compete for bandwidth
        # and CPU, which inflated the metrics and froze the UI.
        for r in tgts:
            if self.stop_ev.is_set():
                r.error = "stopped"
                break
            await test_one(r)

    # ══════════════════════════════════════════════════════
    #  Utilities
    # ══════════════════════════════════════════════════════

    def _clean_host(self, raw: str) -> str:
        h = raw.strip().replace("https://","").replace("http://","").split("/")[0]
        if ":" in h and not h.startswith("["): h=h.split(":")[0]
        return h

    def _clean_path(self, raw: str) -> str:
        p = raw.strip()
        if not p: return "/"
        return p if p.startswith("/") else "/"+p

    def _vless(self, ip: str, port: int) -> str:
        p    = self.P
        uid  = p.uid  or "00000000-0000-0000-0000-000000000000"
        host = p.host or "example.com"
        sni  = p.sni  or host
        path = p.path or "/"
        name = p.cfg_name or "Edge-Optimized"
        net  = p.network  or "ws"
        sec  = p.security or "tls"
        fp   = p.fp       or "chrome"
        alpn = urllib.parse.quote(p.alpn or "http/1.1", safe="")
        q    = urllib.parse.quote
        insecure = "1" if p.allow_insecure else "0"
        url = (f"vless://{q(uid,safe='')}@{ip}:{port}?"
               f"encryption=none&security={q(sec,safe='')}"
               f"&sni={q(sni,safe='')}&fp={q(fp,safe='')}&alpn={alpn}"
               f"&insecure={insecure}&type={q(net,safe='')}")
        if net == "ws":
            url += f"&host={q(host,safe='')}&path={q(path,safe='')}"
        elif net == "grpc":
            url += f"&serviceName={q(p.grpc_service or 'grpc',safe='')}"
        elif net == "h2":
            url += f"&host={q(host,safe='')}&path={q(path,safe='')}"
        url += f"#{q(f'{name} {ip}:{port}', safe='')}"
        return url

    def _copy(self, text: str):
        self.root.clipboard_clear(); self.root.clipboard_append(text)
        self._logui("Copied.")

    def _logui(self, msg: str):
        self._scan_log.configure(state="normal")
        ts = time.strftime("%H:%M:%S")
        self._scan_log.insert(tk.END, f"[{ts}] {msg}\n")
        self._scan_log.see(tk.END)
        self._scan_log.configure(state="disabled")

    def _activity(self, msg: str):
        # Records high-level USER activity into the Developer Log for debugging.
        # NEVER pass sensitive data here (API keys / panel tokens / UUIDs /
        # full config URLs) - callers pass only short, safe descriptions.
        try:
            self._logdbg(f"[ACTIVITY] {msg}")
        except Exception:
            pass

    def _logdbg(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.q.put(("debug", f"[{ts}] {msg}"))

    def _toggle_debug(self):
        self._log_text.configure(state="normal")
        self._log_text.delete("1.0",tk.END)
        if self._dbg_en.get():
            for l in self.debug_buf: self._log_text.insert(tk.END, l+"\n")
            self._log_text.see(tk.END)
        self._log_text.configure(state="disabled")

    def _save_log(self):
        if not self.debug_buf: return
        p = filedialog.asksaveasfilename(defaultextension=".log",
            filetypes=[("Log","*.log"),("All","*.*")])
        if p:
            with open(p,"w",encoding="utf-8") as f: f.write("\n".join(self.debug_buf))

    def _save_txt(self):
        ok = [r for r in self.P.results if r.ping_ms is not None]
        if not ok: self._logui("No results."); return
        p = filedialog.asksaveasfilename(defaultextension=".txt",
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not p: return
        try:
            with open(p,"w",encoding="utf-8") as f:
                f.write(f"# VEO  VLESS Edge Optimizer ver 4.5  {time.strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"# Profile: {self.P.name}  Range: {self.P.range_name}\n\n")
                for i,r in enumerate(ok,1):
                    if self.P.has_config:
                        f.write(f"# [{i}] {r.ip}:{r.port}  "
                                f"ping={_ping_label(r.ping_ms)}  mode={r.mode}\n"
                                f"{self._vless(r.ip,r.port)}\n\n")
                    else:
                        f.write(f"# [{i}] {r.ip}:{r.port}  ping={_ping_label(r.ping_ms)}\n\n")
            self._logui(f"Saved {len(ok)} entries → {p}")
        except Exception as e: self._logui(f"Save error: {e}")

    # ══════════════════════════════════════════════════════
    #  Close
    # ══════════════════════════════════════════════════════

    def _on_close(self):
        # Save all current state before exit
        self._save_config_to_profile()
        save_profiles(self.profiles, self._prof_idx)
        # signal all background threads to stop
        self.stop_ev.set()
        self._auto_switch_stop.set()
        self._bw_stop.set()
        self._proxy_log_stop.set()
        # force-kill xray immediately (atexit also covers crash path)
        self.xray.stop()
        # wait briefly for scan/test threads
        if self.scan_thread and self.scan_thread.is_alive():
            self._stop_scan()
            self.root.after(200, self._on_close); return
        if getattr(self,"test_thread",None) and self.test_thread.is_alive():
            self._stop_test()
            self.root.after(200, self._on_close); return
        self.root.destroy()







# ============================================================
#  Entry point
# ============================================================

def main():
    try:
        # Apply the saved theme preference BEFORE any widgets are built,
        # because widget colours are baked in at construction time.
        set_theme(load_theme_pref())
        root = tk.Tk()
        style = ttk.Style(root)
        setup_dark_styles(style)
        app = App(root)
        root.mainloop()
    except Exception:
        import traceback
        tb = traceback.format_exc()
        path = _crash(tb)
        try:
            messagebox.showerror("Fatal Error",
                f"App crashed.\nDetails: {path}\n\n{tb[:500]}")
        except Exception:
            pass


if __name__ == "__main__":
    main()