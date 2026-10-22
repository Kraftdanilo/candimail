"""Tests du chiffrement des secrets — une régression ici = fuite de données."""
import pytest

from candimail.core import crypto


def test_chiffrement_basique():
    clair = "motdepasse-gmail-2026"
    chiffre = crypto.chiffrer(clair)
    assert chiffre != clair
    assert crypto.est_chiffre(chiffre)
    assert crypto.dechiffrer(chiffre) == clair


def test_chiffrement_idempotent():
    """Déjà chiffré → inchangé (pas de double encodage)."""
    once = crypto.chiffrer("secret")
    deux = crypto.chiffrer(once)
    assert deux == once


def test_dechiffrer_legacy_en_clair():
    """Une valeur non chiffrée (legacy) ressort telle quelle."""
    assert crypto.dechiffrer("ancien-mdp") == "ancien-mdp"


def test_dechiffrer_invalide_renvoie_vide():
    """Marqueur présent mais token invalide → '' (jamais d'exception)."""
    assert crypto.dechiffrer("enc$Zm9yY2VtZW50LWludmFsaWRl") == ""


def test_dechiffrer_vide():
    assert crypto.dechiffrer("") == ""
    assert crypto.dechiffrer(None) == ""


def test_hash_mdp_roundtrip():
    stocke = crypto.hash_mdp("MonMotDePasse!")
    assert stocke != "MonMotDePasse!"
    assert "$" in stocke
    assert crypto.verifier_mdp("MonMotDePasse!", stocke)
    assert not crypto.verifier_mdp("MauvaisMotDePasse", stocke)


def test_hash_mdp_sels_differents():
    """Deux hashs du même mot de passe diffèrent (salt aléatoire)."""
    a = crypto.hash_mdp("mdp")
    b = crypto.hash_mdp("mdp")
    assert a != b


def test_verifier_mdp_format_invalide():
    assert not crypto.verifier_mdp("x", "pas-un-hash")
    assert not crypto.verifier_mdp("x", "")
    assert not crypto.verifier_mdp("x", None)


def test_generer_secret():
    a, b = crypto.generer_secret(), crypto.generer_secret()
    assert a != b
    assert len(a) == 64  # 32 octets hexadécimaux
