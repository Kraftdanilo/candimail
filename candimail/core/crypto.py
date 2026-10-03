"""
Chiffrement des secrets + mot de passe d'accès à l'interface.

- Clé Fernet générée une seule fois, stockée dans secret.key
  (fichier séparé, JAMAIS dans app.db) → copier app.db seul ne suffit
  plus à récupérer les mots de passe Gmail.
- Mots de passe d'application Gmail chiffrés dans la base (marqueur enc$).
- Mot de passe d'accès : hash scrypt (salt + hash hex), jamais stocké en clair.
"""
import base64, hashlib, hmac, os

from candimail.core.config import BASE_DIR

SECRET_KEY_FILE = BASE_DIR / "secret.key"
MARK            = "enc$"


def _charger_ou_creer_cle():
    if SECRET_KEY_FILE.exists():
        # Tolérant aux annotations : on ignore lignes vides et commentaires (# ...).
        # Ne garde que la 1re ligne réellement « clé ».
        for ligne in SECRET_KEY_FILE.read_text(encoding="utf-8",
                                                errors="replace").splitlines():
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                return ligne.encode()
        # Fichier vide / que des commentaires → on régénère une clé valide
    key = base64.urlsafe_b64encode(os.urandom(32))
    SECRET_KEY_FILE.write_bytes(key)
    try:
        SECRET_KEY_FILE.chmod(0o600)  # Unix ; sans effet sous Windows
    except OSError:
        pass
    return key


try:
    from cryptography.fernet import Fernet, InvalidToken
    _f = Fernet(_charger_ou_creer_cle())

    def chiffrer(txt):
        """Chiffre une chaîne (idempotent : déjà chiffré → inchangé)."""
        if not txt or str(txt).startswith(MARK):
            return txt
        return MARK + _f.encrypt(str(txt).encode()).decode()

    def dechiffrer(txt):
        """Déchiffre ; renvoie tel quel si legacy en clair, '' si invalide."""
        if not txt:
            return ""
        t = str(txt)
        if t.startswith(MARK):
            try:
                return _f.decrypt(t[len(MARK):].encode()).decode()
            except InvalidToken:
                return ""
        return t

    def est_chiffre(txt):
        return str(txt).startswith(MARK)

    DISPONIBLE = True
except ImportError:
    # cryptography absent : fallback sans chiffrement (UI affiche un avertissement)
    DISPONIBLE = False

    def chiffrer(txt):
        return txt

    def dechiffrer(txt):
        return txt or ""

    def est_chiffre(txt):
        return False


# ---- Mot de passe d'accès à l'interface (scrypt, lib stdlib) ----
def hash_mdp(mdp):
    salt = os.urandom(16)
    h = hashlib.scrypt(mdp.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    return f"{salt.hex()}${h.hex()}"


def verifier_mdp(mdp, stocke):
    try:
        salt_hex, h_hex = stocke.split("$", 1)
        h = hashlib.scrypt(mdp.encode(), salt=bytes.fromhex(salt_hex),
                           n=16384, r=8, p=1, dklen=32)
        return hmac.compare_digest(h.hex(), h_hex)
    except Exception:
        return False


def generer_secret(n=32):
    return os.urandom(n).hex()