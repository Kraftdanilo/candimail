#!/usr/bin/env python3
"""Build l'executable Windows Candimail.exe via PyInstaller.

Usage :
    pip install pyinstaller
    python scripts/build_exe.py          # dist/Candimail.exe (onefile)
    python scripts/build_exe.py --dir    # dist/Candimail/ (oneddir)

Inclus : templates/, static/ + package candimail.
Les donnees (app.db, uploads/, *.key) restent a cote de l'exe.
"""
import subprocess
import sys
from pathlib import Path

SEP = ";"  # separateur --add-data sous Windows
RACINE = Path(__file__).resolve().parents[1]


def main():
    onefile = "--dir" not in sys.argv
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean",
        "--name", "Candimail",
        "--onedir" if not onefile else "--onefile",
        "--windowed",                       # pas de console (app desktop)
        f"--add-data={RACINE / 'templates'}{SEP}templates",
        f"--add-data={RACINE / 'static'}{SEP}static",
        "--hidden-import=webview",
        "--hidden-import=cryptography",
        "--hidden-import=openpyxl",
        "--hidden-import=candimail",
        "--collect-all=webview",
        "--collect-all=candimail",
        str(RACINE / "desktop.py"),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=str(RACINE))
    print()
    print("  Build termine -> dist/" +
          ("Candimail.exe" if onefile else "Candimail/Candimail.exe"))


if __name__ == "__main__":
    main()

