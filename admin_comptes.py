#!/usr/bin/env python3
"""CALQUE racine -> scripts/. Garde les anciens chemins valides."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from admin_comptes import *  # noqa: F401,F403
import admin_comptes as _m  # noqa: F401

if __name__ == "__main__":
    sys.argv[0] = str(Path(__file__).resolve().parent
                      / "scripts" / "admin_comptes.py")
    exec(compile((_m.__file__ and Path(_m.__file__).read_text(
        encoding="utf-8")).replace('if __name__ == "__main__":',
                                   'if True:'),
        _m.__file__, "exec"), _m.__dict__)

