"""Tests de la purge des uploads orphelins (P3) — revue sécurité.

Chaque test vérifie non seulement le comportement nominal, mais aussi les
scénarios d'attaque : symlink sortant, fichier critique renommé, fichier
caché, double extension piège.
"""
import os
import platform
import pytest

import candimail.core.db as _db
from candimail.core import purge


@pytest.fixture()
def uploads_isole(tmp_path, monkeypatch):
    """Pointe UPLOADS_DIR vers un répertoire temporaire + DB initialisée."""
    monkeypatch.setattr(purge, "UPLOADS_DIR", tmp_path)
    _db.init_db(with_migration=False)
    return tmp_path


# ---------------------------------------------------------------
# Comportement nominal
# ---------------------------------------------------------------
def test_purge_supprime_orphelin(uploads_isole):
    (uploads_isole / "orphan.pdf").write_bytes(b"x")
    supprimes, octets = purge.purger_orphelins()
    assert "orphan.pdf" in supprimes
    assert octets == 1
    assert not (uploads_isole / "orphan.pdf").exists()


def test_purge_conserve_referencé(uploads_isole, monkeypatch):
    from candimail.core import noyau
    monkeypatch.setattr(noyau, "charger_config",
                        lambda: {"pieces_jointes": {"kept.pdf": {}}})
    (uploads_isole / "kept.pdf").write_bytes(b"x")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []
    assert (uploads_isole / "kept.pdf").exists()


def test_purge_ignorer_sous_repertoires(uploads_isole):
    sub = uploads_isole / "subdir"
    sub.mkdir()
    (sub / "nested.pdf").write_bytes(b"x")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []
    assert (sub / "nested.pdf").exists()


def test_purge_extension_non_geree(uploads_isole):
    (uploads_isole / "notes.exe").write_bytes(b"x")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []   # whitelist : on ne touche qu'aux types de l'app


# ---------------------------------------------------------------
# Revue sécurité — défense en profondeur
# ---------------------------------------------------------------
def test_purge_ne_supprime_jamais_une_cle(uploads_isole):
    """Un secret déposé (ou renommé) dans uploads/ ne part JAMAIS."""
    for nom in ("secret.key", "app.db", "config.json", "backup.bak"):
        (uploads_isole / nom).write_bytes(b"critique")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []
    for nom in ("secret.key", "app.db", "config.json", "backup.bak"):
        assert (uploads_isole / nom).exists(), f"{nom} aurait dû survivre"


def test_purge_ne_supprime_jamais_fichier_cache(uploads_isole):
    (uploads_isole / ".env").write_bytes(b"x")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []
    assert (uploads_isole / ".env").exists()


def test_purge_refuse_double_extension_piège(uploads_isole):
    """`cv.pdf.exe` n'a pas l'extension .pdf → jamais supprimé (whitelist)."""
    (uploads_isole / "cv.pdf.exe").write_bytes(b"x")
    (uploads_isole / "malware.pdf.bat").write_bytes(b"x")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []


def test_purge_fichier_trop_lourd_ignoré(uploads_isole, monkeypatch):
    """Un fichier > TAILLE_MAX n'est pas un CV : on ne le touche pas."""
    (uploads_isole / "gros.pdf").write_bytes(b"x")
    monkeypatch.setattr(purge, "TAILLE_MAX", 0)
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []
    assert (uploads_isole / "gros.pdf").exists()


@pytest.mark.skipif(platform.system() == "Windows" and not hasattr(os, "symlink"),
                    reason="symlinks nécessitent des privilèges sous Windows")
def test_purge_refuse_symlink(uploads_isole, tmp_path_factory):
    """Un symlink dans uploads/ pointant sur un fichier critique ailleurs
    ne doit JAMAIS être suivi/supprimé (attaque par redirection)."""
    cible_exterieure = tmp_path_factory.mktemp("hors_sandbox") / "secret.key"
    cible_exterieure.write_bytes(b"cle-critique-hors-uploads")
    lien = uploads_isole / "secret.pdf"     # nom de whitelist, cible hors sandbox
    try:
        lien.symlink_to(cible_exterieure)
    except (OSError, NotImplementedError):
        pytest.skip("création de symlink non permise sur ce système")
    supprimes, _ = purge.purger_orphelins()
    assert supprimes == []                  # symlink ignoré
    assert cible_exterieure.exists()        # cible intacte


def test_purge_erreur_os_ne_bloque_pas_le_balayage(uploads_isole, monkeypatch):
    """Un fichier verrouillé (PermissionError) n'arrête pas le balayage :
    les autres orphelins restent supprimés."""
    bloque = uploads_isole / "verrouille.pdf"
    bloque.write_bytes(b"x")
    autre = uploads_isole / "orphan2.pdf"
    autre.write_bytes(b"x")
    original_unlink = type(bloque).unlink

    def unlink_bloque(self, *a, **k):
        if self.name == "verrouille.pdf":
            raise PermissionError(13, "fichier ouvert ailleurs")
        return original_unlink(self, *a, **k)

    monkeypatch.setattr(type(bloque), "unlink", unlink_bloque)
    supprimes, _ = purge.purger_orphelins()
    assert "orphan2.pdf" in supprimes       # le balayage a continué
    assert "verrouille.pdf" not in supprimes
    assert bloque.exists()                  # le verrouillé a survécu


def test_purge_uploads_indisponible_renvoie_vide(tmp_path, monkeypatch):
    """UPLOADS_DIR inexistant/inaccessible → ([], 0), jamais d'exception."""
    inexistant = tmp_path / "n-existe-pas"
    monkeypatch.setattr(purge, "UPLOADS_DIR", inexistant)
    supprimes, octets = purge.purger_orphelins()
    assert (supprimes, octets) == ([], 0)
