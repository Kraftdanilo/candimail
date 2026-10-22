#!/usr/bin/env python3
"""
Couche de persistance SQLite.
Remplace le stockage par fichiers JSON (config.json / envois.json) par une
vraie base de données : config (blob), log (envois), companies, cv.
Au premier lancement, migre automatiquement les anciens fichiers JSON.
"""
import json
import sqlite3
import threading

from candimail.core.config import BASE_DIR, DATA_DIR

DB_FILE  = DATA_DIR / "app.db"

_lock = threading.RLock()

# --------------------------------
# SCHÉMA
# --------------------------------
_SCHEMA = """
CREATE TABLE IF NOT EXISTS config (
    cle    TEXT PRIMARY KEY,
    valeur TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS log (
    entreprise TEXT NOT NULL,
    uid        INTEGER DEFAULT 0,
    data       TEXT NOT NULL,
    PRIMARY KEY (entreprise, uid)
);
CREATE TABLE IF NOT EXISTS companies (
    name    TEXT NOT NULL,
    uid     INTEGER DEFAULT 0,
    cat     TEXT,
    email   TEXT,
    context TEXT,
    custom  INTEGER DEFAULT 0,
    PRIMARY KEY (name, uid)
);
CREATE TABLE IF NOT EXISTS cv (
    cle    TEXT PRIMARY KEY,
    valeur TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (
    cle    TEXT PRIMARY KEY,
    valeur TEXT
);
CREATE TABLE IF NOT EXISTS profils (
    uid        INTEGER PRIMARY KEY,
    nom        TEXT NOT NULL,
    date_creation TEXT
);
CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email     TEXT UNIQUE NOT NULL,
    pass_hash TEXT NOT NULL,
    created   TEXT
);
CREATE TABLE IF NOT EXISTS historique (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    uid     INTEGER NOT NULL DEFAULT 0,
    type    TEXT NOT NULL,
    label   TEXT,
    undo    TEXT,          -- JSON : donnees necessaires pour ANNULER
    redo    TEXT,          -- JSON : donnees pour RETABLIR
    undone   INTEGER DEFAULT 0,
    created TEXT
);
CREATE INDEX IF NOT EXISTS idx_hist_uid ON historique(uid, id DESC);
"""

_LOG_UID_MIGRATED = "log_uid_col"

# --------------------------------
# CONNEXION
# --------------------------------
def _connect():
    conn = sqlite3.connect(str(DB_FILE), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db(with_migration=True):
    """Crée le schéma et, au besoin, migre les anciennes structures."""
    with _lock:
        conn = _connect()
        try:
            # Migration anciennes tables (PK sans uid) → nouvelles avec uid
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(log)").fetchall()]
            if cols and "uid" not in cols:
                conn.execute("DROP TABLE log")   # ancien log : repris via envois.json si besoin
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(companies)").fetchall()]
            if cols and "uid" not in cols:
                conn.execute("ALTER TABLE companies RENAME TO companies_old")
                conn.executescript(_SCHEMA)
                conn.execute(
                    "INSERT OR REPLACE INTO companies(name, uid, cat, email, context, custom) "
                    "SELECT name, 0, cat, email, context, custom FROM companies_old")
                conn.execute("DROP TABLE companies_old")
            else:
                conn.executescript(_SCHEMA)
            conn.commit()
        finally:
            conn.close()
        if with_migration:
            _migrate_legacy()


def _meta_get(cle):
    with _lock:
        conn = _connect()
        try:
            row = conn.execute("SELECT valeur FROM meta WHERE cle=?", (cle,)).fetchone()
        finally:
            conn.close()
        return row["valeur"] if row else None


def _meta_set(cle, valeur="1"):
    with _lock:
        conn = _connect()
        try:
            conn.execute("INSERT OR REPLACE INTO meta(cle, valeur) VALUES(?, ?)",
                         (cle, valeur))
            conn.commit()
        finally:
            conn.close()


def _migrate_legacy():
    """Importe une éventuelle config.json / envois.json legacy (une seule fois).

    Les flags `migrated_config` / `migrated_log` de la table `meta` empêchent
    toute ré-import ultérieur : ces fichiers deviennent des RELIQUES une fois
    migrés et ne doivent plus jamais écraser la base (ils contiennent des mots
    de passe en clair — voir crypto.py).
    """
    cfg_file = BASE_DIR / "config.json"
    log_file = BASE_DIR / "envois.json"
    if cfg_file.exists() and not _meta_get("migrated_config"):
        try:
            cfg = json.loads(cfg_file.read_text(encoding="utf-8-sig"))
            config_set(cfg)
            _meta_set("migrated_config")
            _purge_legacy(cfg_file, "config.json")
        except Exception:
            pass
    if log_file.exists() and not _meta_get("migrated_log"):
        try:
            log = json.loads(log_file.read_text(encoding="utf-8-sig"))
            log_set(log)
            _meta_set("migrated_log")
            _purge_legacy(log_file, "envois.json")
        except Exception:
            pass


def _purge_legacy(path, nom):
    """Archive puis supprime un fichier legacy migré (il contient des
    secrets en clair). Un fichier .legacy-save est conservé en sécurité."""
    try:
        archive = path.with_suffix(path.suffix + ".legacy-save")
        if not archive.exists():
            archive.write_bytes(path.read_bytes())
        path.unlink()
        print(f"  🗑️  {nom} migré vers app.db — archivé en {archive.name}")
    except Exception:
        pass


# --------------------------------
# CONFIG (un blob JSON par utilisateur : cle = u<uid>, uid 0 = legacy)
# --------------------------------
CONFIG_KEY = "main"


def config_get(uid=0):
    key = CONFIG_KEY if uid in (0, None) else f"u{int(uid)}"
    with _lock:
        conn = _connect()
        try:
            row = conn.execute(
                "SELECT valeur FROM config WHERE cle=?", (key,)
            ).fetchone()
        finally:
            conn.close()
        if row is None:
            return None
        try:
            return json.loads(row["valeur"])
        except Exception:
            return None


def config_set(cfg, uid=0):
    key = CONFIG_KEY if uid in (0, None) else f"u{int(uid)}"
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO config(cle, valeur) VALUES(?, ?)",
                (key, json.dumps(cfg, ensure_ascii=False))
            )
            conn.commit()
        finally:
            conn.close()


# --------------------------------
# LOG des envois  {entreprise: info}  (par utilisateur)
# --------------------------------
def log_get(uid=0):
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute(
                "SELECT entreprise, data FROM log WHERE uid=?", (int(uid or 0),)
            ).fetchall()
        finally:
            conn.close()
    out = {}
    for r in rows:
        try:
            out[r["entreprise"]] = json.loads(r["data"])
        except Exception:
            continue
    return out


def log_set(log, uid=0):
    u = int(uid or 0)
    with _lock:
        conn = _connect()
        try:
            conn.execute("DELETE FROM log WHERE uid=?", (u,))
            conn.executemany(
                "INSERT OR REPLACE INTO log(entreprise, uid, data) VALUES(?, ?, ?)",
                [(k, u, json.dumps(v, ensure_ascii=False))
                 for k, v in (log or {}).items()]
            )
            conn.commit()
        finally:
            conn.close()


def log_reset(backup_to=None, uid=0):
    """Vide le log. Si backup_to est un Path, essaie une exportation JSON."""
    if backup_to is not None:
        try:
            backup_to.write_text(
                json.dumps(log_get(uid), ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass
    log_set({}, uid)


# --------------------------------
# ENTREPRISES  [{name, cat, email, context, custom}]  (par utilisateur)
# --------------------------------
def companies_get(uid=0):
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute(
                "SELECT name, cat, email, context, custom FROM companies "
                "WHERE uid=?", (int(uid or 0),)
            ).fetchall()
        finally:
            conn.close()
    return [{
        "name":    r["name"],
        "cat":     r["cat"] or "pme",
        "email":   r["email"] or "",
        "context": r["context"] or "",
        "custom":  bool(r["custom"]),
    } for r in rows]


def companies_replace(companies, uid=0):
    u = int(uid or 0)
    with _lock:
        conn = _connect()
        try:
            conn.execute("DELETE FROM companies WHERE uid=?", (u,))
            conn.executemany(
                "INSERT OR REPLACE INTO companies(name, uid, cat, email, context, custom) "
                "VALUES(?, ?, ?, ?, ?, ?)",
                [(c["name"], u, c.get("cat", "pme"), c.get("email", ""),
                  c.get("context", ""), 1 if c.get("custom") else 0)
                 for c in (companies or [])]
            )
            conn.commit()
        finally:
            conn.close()


def companies_add(company, uid=0):
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO companies(name, uid, cat, email, context, custom) "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (company["name"], int(uid or 0), company.get("cat", "pme"),
                 company.get("email", ""), company.get("context", ""),
                 1 if company.get("custom") else 0)
            )
            conn.commit()
        finally:
            conn.close()


def companies_delete(name, uid=0):
    with _lock:
        conn = _connect()
        try:
            conn.execute("DELETE FROM companies WHERE name=? AND uid=?",
                         (name, int(uid or 0)))
            conn.commit()
        finally:
            conn.close()


# --------------------------------
# CV (blob JSON, par utilisateur)
# --------------------------------
def cv_get(uid=0):
    key = "main" if uid in (0, None) else f"u{int(uid)}"
    with _lock:
        conn = _connect()
        try:
            row = conn.execute(
                "SELECT valeur FROM cv WHERE cle=?", (key,)
            ).fetchone()
        finally:
            conn.close()
        if row is None:
            return None
        try:
            return json.loads(row["valeur"])
        except Exception:
            return None


def cv_set(data, uid=0):
    key = "main" if uid in (0, None) else f"u{int(uid)}"
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO cv(cle, valeur) VALUES(?, ?)",
                (key, json.dumps(data, ensure_ascii=False),)
            )
            conn.commit()
        finally:
            conn.close()


# --------------------------------
# UTILISATEURS
# --------------------------------
def migrate_legacy_user(uid):
    """Donne à ce premier utilisateur les données legacy (uid 0)."""
    u = int(uid)
    with _lock:
        conn = _connect()
        try:
            if not conn.execute("SELECT 1 FROM config WHERE cle='main'").fetchone():
                return False
            conn.execute("UPDATE config SET cle=? WHERE cle='main'", (f"u{u}",))
            conn.execute("UPDATE log SET uid=? WHERE uid=0", (u,))
            conn.execute("UPDATE companies SET uid=? WHERE uid=0", (u,))
            conn.execute("UPDATE cv SET cle=? WHERE cle='main'", (f"u{u}",))
            conn.commit()
            return True
        finally:
            conn.close()


def users_create(email, pass_hash):
    with _lock:
        conn = _connect()
        try:
            cur = conn.execute(
                "INSERT INTO users(email, pass_hash, created) VALUES(?, ?, ?)",
                (email.lower().strip(), pass_hash,
                 datetime_now_str()))
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()


def users_get_by_email(email):
    with _lock:
        conn = _connect()
        try:
            r = conn.execute(
                "SELECT id, email, pass_hash FROM users WHERE email=?",
                (email.lower().strip(),)
            ).fetchone()
        finally:
            conn.close()
    return dict(r) if r else None


def users_get(uid):
    with _lock:
        conn = _connect()
        try:
            r = conn.execute(
                "SELECT id, email, pass_hash FROM users WHERE id=?", (int(uid),)
            ).fetchone()
        finally:
            conn.close()
    return dict(r) if r else None


def users_count():
    with _lock:
        conn = _connect()
        try:
            r = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()
        finally:
            conn.close()
    return r["n"]


def uids_actifs():
    """UIDs ayant une config en base (0 inclus = config globale)."""
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute("SELECT cle FROM config").fetchall()
        finally:
            conn.close()
    uids = [0]
    for r in rows:
        if r["cle"].startswith("u") and r["cle"][1:].isdigit():
            uids.append(int(r["cle"][1:]))
    return uids


# --------------------------------
# PROFILS UTILISATEURS
# --------------------------------
def profils_lister():
    """Liste tous les profils avec leur uid et nom."""
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute(
                "SELECT uid, nom, date_creation FROM profils ORDER BY uid"
            ).fetchall()
        finally:
            conn.close()
    return [dict(r) for r in rows]


def profil_creer(uid, nom):
    """Crée un nouveau profil. Retourne True si créé, False si déjà existant."""
    with _lock:
        conn = _connect()
        try:
            exists = conn.execute(
                "SELECT 1 FROM profils WHERE uid=?", (uid,)
            ).fetchone()
            if exists:
                return False
            conn.execute(
                "INSERT INTO profils(uid, nom, date_creation) VALUES(?, ?, ?)",
                (uid, nom, datetime_now_str()),
            )
            conn.commit()
            return True
        finally:
            conn.close()


def profil_existe(uid):
    """Vérifie si un profil existe."""
    with _lock:
        conn = _connect()
        try:
            r = conn.execute(
                "SELECT 1 FROM profils WHERE uid=?", (uid,)
            ).fetchone()
        finally:
            conn.close()
    return r is not None


def datetime_now_str():
    from datetime import datetime as _dt
    return _dt.now().strftime("%Y-%m-%d %H:%M")


# --------------------------------
# HISTORIQUE DES ACTIONS (annulation / rétablissement)
# --------------------------------
HISTORIQUE_MAX = 100


def hist_ajouter(type_action, label, undo=None, redo=None, uid=0):
    """Enregistre une action réversible. `undo`/`redo` sont des dicts
    sérialisés en JSON : ils suffisent à rejouer l'opération inverse."""
    u = int(uid or 0)
    with _lock:
        conn = _connect()
        try:
            cur = conn.execute(
                "INSERT INTO historique(uid, type, label, undo, redo, created) "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (u, type_action, label,
                 json.dumps(undo, ensure_ascii=False) if undo is not None else None,
                 json.dumps(redo, ensure_ascii=False) if redo is not None else None,
                 datetime_now_str()),
            )
            conn.commit()
            hid = cur.lastrowid
            # Purge : on garde seulement les N actions les plus récentes
            conn.execute(
                "DELETE FROM historique WHERE uid=? AND id NOT IN "
                "(SELECT id FROM historique WHERE uid=? ORDER BY id DESC LIMIT ?)",
                (u, u, HISTORIQUE_MAX),
            )
            conn.commit()
            return hid
        finally:
            conn.close()


def hist_lister(uid=0, limite=60):
    u = int(uid or 0)
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute(
                "SELECT id, type, label, undone, created FROM historique "
                "WHERE uid=? ORDER BY id DESC LIMIT ?", (u, int(limite)),
            ).fetchall()
        finally:
            conn.close()
    return [dict(r) for r in rows]


def hist_get(hid, uid=0):
    with _lock:
        conn = _connect()
        try:
            r = conn.execute(
                "SELECT id, uid, type, label, undo, redo, undone FROM historique "
                "WHERE id=? AND uid=?", (int(hid), int(uid or 0)),
            ).fetchone()
        finally:
            conn.close()
    if not r:
        return None
    d = dict(r)
    for k in ("undo", "redo"):
        try:
            d[k] = json.loads(d[k]) if d[k] else None
        except Exception:
            d[k] = None
    return d


def hist_marquer(hid, undone, uid=0):
    with _lock:
        conn = _connect()
        try:
            conn.execute("UPDATE historique SET undone=? WHERE id=? AND uid=?",
                         (1 if undone else 0, int(hid), int(uid or 0)))
            conn.commit()
        finally:
            conn.close()


def hist_purger(uid=0):
    with _lock:
        conn = _connect()
        try:
            conn.execute("DELETE FROM historique WHERE uid=?", (int(uid or 0),))
            conn.commit()
        finally:
            conn.close()