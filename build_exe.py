#!/usr/bin/env python3
"""CALQUE racine -> scripts/. Garde les anciens chemins valides."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from build_exe import *  # noqa: F401,F403
from build_exe import main  # noqa: F401

if __name__ == "__main__":
    main()

