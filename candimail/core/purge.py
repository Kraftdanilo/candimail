"""
Purge des fichiers uploadés orphelins (`uploads/`).

- À la suppression d'un contact/pièce jointe : le fichier part aussi.
- Au démarrage : un balayage efface les fichiers de `uploads/` qui ne sont
  référencés par AUCUNE pièce jointe dans la base (`pieces_jointes`).
  Le fichier de la pièce jointe active — même désactivée — est conservé.

Sécurité :
- whitelist stricte d'extensions (jamais de blacklist seule) ;
- les fichiers critiques (`*.key`, `*.db`, `*.json`, cachés `.*`) sont
  TOUJOURS ignorés, même si quelqu'un les dépose renommés dans uploads/ ;
- symlinks refusés : un lien dans uploads/ pourrait pointer vers
  secret.key ou app.db ailleurs sur le disque (suppression hors sandbox) ;
- taille plafonnée : un fichier > 100 Mo n'est pas un CV, on ne le touche pas ;
- erreurs OSError par fichier : un fichier verrouillé n'arrête pas le balayage.
"""
from pathlib import Path

from candimail.core.config import UPLOADS_DIR
from candimail.core import noyau

# Whitelist : uniquement les types que l'app crée elle-même via /api/pieces.
EXTENSIONS_OK = frozenset({
    ".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".txt", ".zip",
})

# Défense en profondeur : ces extensions ne partent JAMAIS, même si un
# attaquant (ou un bug d'import) les dépose dans uploads/.
NE_JAMAIS_SUPPRIMER = frozenset({
    ".key", ".db", ".db-journal", ".db-wal", ".db-shm", ".json",
    ".sqlite", ".sqlite3", ".bak", ".py", ".exe", ".bat", ".cmd", ".ps1",
    ".sh", ".dll", ".ini", ".cfg", ".env",
})

# Un fichier de plus de 100 Mo n'est pas un CV : on ne le touche pas.
TAILLE_MAX = 100 * 1024 * 1024


def fichiers_references():
    """Ensemble des noms de fichiers connus de la base (toutes clés)."""
    refs = set()
    cfg = noyau.charger_config()
    for pid in cfg.get("pieces_jointes", {}):
        refs.add(str(pid))
    return refs


def purger_orphelins(verbose=False):
    """Supprime les fichiers de `uploads/` non référencés par la base.

    Renvoie (supprimes, liberes_octets). Sécurité : whitelist d'extensions,
    blacklist dure (clés, bases, scripts, cachés), symlinks refusés,
    taille plafonnée, fichiers directement dans `uploads/` uniquement.
    """
    refs = fichiers_references()
    supprimes, octets = [], 0
    try:
        entrees = list(UPLOADS_DIR.iterdir())
    except OSError:
        return [], 0
    for f in entrees:
        try:
            # Symlink : peut pointer n'importe où sur le disque
            # (secret.key, app.db…) → suppression interdite.
            if f.is_symlink():
                continue
            if not f.is_file():          # sous-dossier, device, socket…
                continue
            suffixe = f.suffix.lower()
            if suffixe in NE_JAMAIS_SUPPRIMER or f.name.startswith("."):
                continue                  # blacklist dure + fichiers cachés
            if suffixe not in EXTENSIONS_OK:
                continue                  # whitelist : on ne crée que ça
            if f.name in refs:
                continue
            st = f.stat()
            if st.st_size > TAILLE_MAX:
                continue
            f.unlink()
            supprimes.append(f.name)
            octets += st.st_size
            if verbose:
                print(f"  🧹 uploads: orphelin supprimé {f.name}")
        except OSError:
            continue                      # fichier verrouillé : on passe
    return supprimes, octets
