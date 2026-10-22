"""Fixture pytest partagée : base SQLite temporaire + client FastAPI.

Chaque test part d'une base vierge : on pointe `db.DB_FILE` et
`crypto.SECRET_KEY_FILE` vers des fichiers temporaires AVANT d'importer
le reste (les modules lisent ces chemins au chargement).
"""
import io
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Fichiers temporaires créés AVANT tout import de candimail
_TMP = tempfile.mkdtemp(prefix="candimail_test_")
_DB_FILE = Path(_TMP) / "test_app.db"
_KEY_FILE = Path(_TMP) / "test_secret.key"

import candimail.core.db as _db  # noqa: E402
import candimail.core.crypto as _crypto  # noqa: E402

_db.DB_FILE = _DB_FILE
_crypto.SECRET_KEY_FILE = _KEY_FILE
_db.init_db(with_migration=False)


class _CompatResponse:
    """Wrapper compat Flask autour d'une réponse httpx (TestClient FastAPI).

    Ajoute .get_json() et .data pour que les tests écrits pour Flask
    continuent de fonctionner sans modification.
    """
    def __init__(self, response):
        self._r = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.content = response.content
        self.text = response.text
        self.data = response.content

    def get_json(self):
        return self._r.json()

    def get_data(self, as_text=False):
        if as_text:
            return self.text
        return self.content


class _CompatClient:
    """Wrapper compat Flask autour de TestClient FastAPI."""
    def __init__(self, client):
        self._c = client

    def get(self, path, **kwargs):
        return _CompatResponse(self._c.get(path, **kwargs))

    def post(self, path, **kwargs):
        # content_type n'existe pas en httpx ; on l'ignore
        kwargs.pop("content_type", None)
        # Convertir data={"file": (obj, name)} en files= pour httpx
        data = kwargs.pop("data", None)
        if isinstance(data, dict):
            files = {}
            remaining = {}
            for k, v in data.items():
                if isinstance(v, tuple) and len(v) >= 2:
                    fobj, fname = v[0], v[1]
                    content = fobj.read() if hasattr(fobj, "read") else fobj
                    files[k] = (fname, content)
                else:
                    remaining[k] = v
            if files:
                kwargs["files"] = files
            if remaining:
                kwargs["data"] = remaining
        return _CompatResponse(self._c.post(path, **kwargs))

    def put(self, path, **kwargs):
        return _CompatResponse(self._c.put(path, **kwargs))

    def delete(self, path, **kwargs):
        return _CompatResponse(self._c.delete(path, **kwargs))


@pytest.fixture()
def app():
    from candimail.web import api as appmod
    appmod.initialiser()
    yield appmod.app


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient
    return _CompatClient(TestClient(app))
