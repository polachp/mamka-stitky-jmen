#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dávkový generátor PDF štítků z render.html přes Chrome headless.

Páruje jména po pořadí (1+2, 3+4, ...). Nastavení: Segoe UI, 40 pt, 8 řádků.
Výstup do ../Generated/.
"""
import os, subprocess, sys, unicodedata, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "Generated")
RENDER = os.path.join(HERE, "render.html").replace("\\", "/")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

# Pořadí dle Jmena_SK.md (žebříček podle počtu nositelů).
NAMES = [
    "Mária", "Ján", "Anna", "Jozef", "Štefan", "Peter", "Helena", "Michal",
    "Milan", "Zuzana", "Eva", "Pavol", "Katarína", "František", "Ladislav",
    "Juraj", "Alžbeta", "Miroslav", "Marta", "Jana", "Margita", "Vladimír",
    "Martin", "Emília", "Ondrej", "Jaroslav", "Viera", "Anton", "Andrej", "Dušan",
]

ROWS = 8
FONT = 40
FAMILY = '"Segoe UI", Arial, sans-serif'


def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return "".join(c for c in s if c.isalnum()) or "x"


def chrome_path():
    for p in CHROME_CANDIDATES:
        if os.path.isfile(p):
            return p
    sys.exit("Chrome ani Edge nenalezen.")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chrome = chrome_path()
    pairs = [NAMES[i:i + 2] for i in range(0, len(NAMES), 2)]
    for idx, pair in enumerate(pairs, start=1):
        a = pair[0]
        b = pair[1] if len(pair) > 1 else ""
        qs = urllib.parse.urlencode(
            {"a": a, "b": b, "rows": ROWS, "font": FONT, "family": FAMILY}
        )
        url = f"file:///{RENDER}?{qs}"
        fname = f"{idx:02d}_{ascii_slug(a)}_{ascii_slug(b)}.pdf"
        out = os.path.join(OUT_DIR, fname).replace("\\", "/")
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             "--virtual-time-budget=4000", f"--print-to-pdf={out}", url],
            check=True, capture_output=True,
        )
        print(f"{fname}: {a} + {b}")
    print(f"\nHotovo: {len(pairs)} PDF v {OUT_DIR}")


if __name__ == "__main__":
    main()
