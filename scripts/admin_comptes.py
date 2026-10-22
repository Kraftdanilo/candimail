#!/usr/bin/env python3
"""
Outil d'administration local — récupération de compte.

À lancer SUR LE SERVEUR, dans le dossier du projet :
    python admin_comptes.py list                → liste les identifiants
    python admin_comptes.py reset <email>       → réinitialise le mot de passe
    python admin_comptes.py reset <email> mdp   → avec le mot de passe voulu
                                                  (sinon généré aléatoirement)
    python admin_comptes.py gmail <email>       → mot de passe Gmail en clair

Sécurité :
- Les mots de passe d'accès sont stockés en hash scrypt (irréversible).
  On ne peut PAS les « voir en clair » — par conception. L'outil ne fait
  que les RÉINITIALISER.
- Les mots de passe d'application Gmail, eux, sont chiffrés (Fernet, clé
  dans secret.key) et donc relisibles en clair ici — c'est l'option `gmail`.
- Les commandes `reset` et `gmail` demandent le MOT DE PASSE ADMIN.
  Il est défini au premier appel (hash stocké dans admin.key, à côté de
  secret.key). Le fichier admin.key ne quitte JAMAIS le serveur.
"""
import getpass
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from candimail.core import crypto, db
from candimail.core.config import DATA_DIR

ADMIN_KEY_FILE = DATA_DIR / "admin.key"


# ---- Mot de passe admin (hash scrypt dans admin.key) ----
def _admin_existe():
    return ADMIN_KEY_FILE.exists()


def _definir_admin():
    print("\nPremière utilisation : choisis le mot de passe ADMIN de cet outil.")
    mdp = getpass.getpass("  Nouveau mot de passe admin : ")
    if len(mdp) < 8:
        print("❌ 8 caractères minimum.")
        sys.exit(1)
    if mdp != getpass.getpass("  Confirmer : "):
        print("❌ Les deux saisies diffèrent.")
        sys.exit(1)
    ADMIN_KEY_FILE.write_text(crypto.hash_mdp(mdp), encoding="utf-8")
    try:
        ADMIN_KEY_FILE.chmod(0o600)   # Unix ; sans effet sous Windows
    except OSError:
        pass
    print("✅ Mot de passe admin enregistré (fichier admin.key).")


def _verifier_admin():
    """Demande le mot de passe admin ; le crée au premier lancement."""
    if not _admin_existe():
        _definir_admin()
        return
    stocke = ADMIN_KEY_FILE.read_text(encoding="utf-8").strip()
    for tentative in range(3):
        mdp = getpass.getpass("Mot de passe admin : ")
        if crypto.verifier_mdp(mdp, stocke):
            return
        print(f"❌ Mot de passe admin incorrect ({2 - tentative} essai(s) restant(s)).")
    print("Abandon.")
    sys.exit(1)


def lister():
    print("\nUtilisateurs (identifiants en clair) :")
    print("-" * 60)
    with db._lock:
        conn = db._connect()
        try:
            rows = conn.execute(
                "SELECT id, email, created FROM users ORDER BY id"
            ).fetchall()
        finally:
            conn.close()
    for r in rows:
        print(f"  [{r['id']}] {r['email']}  (cré {r['created'] or '?'})")
    if not rows:
        print("  (aucun)")
    print()


def reset(email, mdp=None):
    _verifier_admin()
    u = db.users_get_by_email(email)
    if not u:
        print(f"❌ Aucun utilisateur avec l'email « {email} ».")
        sys.exit(1)
    if not mdp:
        mdp = secrets.token_urlsafe(12)   # ~16 caractères lisibles
    with db._lock:
        conn = db._connect()
        try:
            conn.execute("UPDATE users SET pass_hash=? WHERE id=?",
                         (crypto.hash_mdp(mdp), u["id"]))
            conn.commit()
        finally:
            conn.close()
    print(f"\n✅ Mot de passe réinitialisé pour {u['email']} (id {u['id']})")
    print(f"   Nouveau mot de passe : {mdp}")
    print("   (À communiquer à l'utilisateur, puis le faire changer.)")


def montrer_gmail(email):
    """Affiche en clair le mot de passe d'application Gmail d'un compte configuré."""
    _verifier_admin()
    cfg = db.config_get(0)
    for c in cfg.get("comptes", []):
        if c.get("email", "").lower() == email.lower():
            clair = crypto.dechiffrer(c.get("password", ""))
            print(f"\n{email} → mot de passe Gmail : {clair or '(vide/illisible)'}")
            return
    print(f"❌ Compte Gmail « {email} » introuvable dans la configuration.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1].lower()
    if cmd == "list":
        lister()
    elif cmd == "reset" and len(sys.argv) >= 3:
        reset(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "gmail" and len(sys.argv) >= 3:
        montrer_gmail(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
