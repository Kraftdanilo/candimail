"""Test de fumee : le package s'importe et les routes repondent."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from candimail.web.app import PORT_DEFAUT, app


def test_port_defaut():
    assert PORT_DEFAUT == 8765


def test_pages():
    c = app.test_client()
    # "/" redirige vers l'app (la vitrine a été déplacée sur /vitrine)
    assert c.get("/").status_code == 302
    assert c.get("/app").status_code == 200
    assert c.get("/vitrine").status_code == 200


def test_auth_supprimee():
    """L'authentification a été retirée : plus aucune route /api/auth ni /login."""
    c = app.test_client()
    assert c.get("/login").status_code == 404
    assert c.get("/api/auth/status").status_code == 404


def test_sondes():
    c = app.test_client()
    assert c.get("/api/health").get_json()["ok"] is True
    assert c.get("/api/debug/info").get_json()["ok"] is True
