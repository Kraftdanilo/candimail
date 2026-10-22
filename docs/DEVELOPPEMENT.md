# Développement

> © 2026 Dane hk \Manifest — Tous droits réservés.

---

## 1. Environnement

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyflakes   # outils de dev
```

---

## 2. Lancer en développement

Le **venv du projet est indispensable** à l'IDE :

```powershell
.\.venv\Scripts\Activate.ps1          # ou utiliser .\.venv\Scripts\python.exe
python candimail.py --debug            # interface + logs détaillés
$env:CANDIMAIL_DEBUG = "1"             # active /api/debug/info
```

> ⚠️ `/api/debug/info` n'est accessible qu'avec `CANDIMAIL_DEBUG=1` et
> expose l'état interne. Ne l'utilisez jamais sur un poste exposé.

> ⚠️ Si Pylance affiche « Impossible de résoudre l'importation "uvicorn" /
> "serveur web local" », c'est que VS Code utilise un autre interpréteur que le venv.
> `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv\Scripts\python.exe`
> → **Developer: Reload Window**.

---

## 3. Vérifications

### Analyse statique

```powershell
python -m pyflakes candimail candimail.py scripts
```

Seuls ré-exports attendus : `candimail/core/__init__.py` et `app.py`.

### Syntaxe JavaScript

Le front est en JS inline dans `templates/index.html` :

```powershell
python -c "import re; h=open('templates/index.html',encoding='utf-8').read(); open('_chk.js','w',encoding='utf-8').write('\n'.join(re.findall(r'<script[^>]*>(.*?)</script>',h,re.S)))"
node --check _chk.js
Remove-Item _chk.js
```

### Smoke test des endpoints

```powershell
python -c "from candimail.web.app import app; c=app.test_client(); print([(u, c.get(u).status_code) for u in ['/api/health','/app','/cv','/suivi','/api/config']])"
```

---

## 4. Conventions de code

| Règle | Application |
|---|---|
| **Langage** | Python 3.11, français pour les commentaires et docstrings |
| **Nommage** | `snake_case` (fonctions), `UPPER_CASE` (constantes), préfixe `_` (privé) |
| **Imports** | Standard → tiers → local, séparés par une ligne vide |
| **Docstrings** | Obligatoires sur les fonctions publiques |
| **Type hints** | Occasionnels (projet historique sans annotations systématiques) |
| **Commentaires** | Expliquent le *pourquoi*, pas le *quoi* |

### Règle d'or : anti-fuite

Toute exception passée au front doit passer par le helper :

```python
# ❌ JAMAIS
return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

# ✅
log_erreur("ma_route", e, contexte)
return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="db")[0]}, status_code=500)
```

---

## 5. Ajouter une route

1. Ajouter la route dans `candimail/web/api.py` (section thématique correspondante)
2. Suivre le nommage `api_<ressource>_<action>`
3. **Toujours** valider les entrées
4. **Jamais** renvoyer d'exception brute
5. Utiliser `current_uid()` pour le multi-utilisateur

```python
@bp.route("/api/ma-ressource", methods=["POST"])
def api_ma_ressource():
    data = request.get_json(silent=True) or {}
    valeur = _txt(data.get("valeur")).strip()
    if not valeur:
        return JSONResponse({"ok": False, "error": "Valeur requise"}, status_code=400)
    return {"ok": True, "valeur": valeur}
```

### Adding validation

| Besoin | Outil |
|---|---|
| Texte | `_txt(v)` — convertit non-str en `''` |
| E-mail | `_email_valide(e)` — validation stricte |
| Valeur enum | `if x not in ("a","b"): x = "a"` |
| Entier borné | `min(max(int(v), 1), 365)` dans un `try` |
| Chemin de fichier | `_resoudre_piece(id)` — anti-traversée |

---

## 6. Modifier le schéma de la base

1. Éditer `_SCHEMA` dans `core/db.py`
2. Ajouter la logique de migration dans `init_db()`
3. Utiliser `CREATE TABLE IF NOT EXISTS` / `ALTER TABLE`
4. Marquer la version dans la table `meta`

---

## 7. Points d'attention techniques

| Sujet | Détail |
|---|---|
| **Verrous** | Toujours utiliser les verrous de `noyau.py` pour l'état partagé |
| **Cache config** | Après `db.config_set()` direct : appeler `invalider_cache_config()` |
| **Nettoyage** | Ne jamais importer depuis la racine (`from candimail.core…`) |
| **Chemins** | Utiliser `BASE_DIR` / `RESS_DIR`, jamais `__file__` en dur |
| **Encodage** | UTF-8 partout |
| **Logs** | `print()` pour le serveur, `log`/`logging` pour les exceptions |

### Pièges connus

- `_config_globale()` renvoie l'objet **par référence** : le muter avant un
  `sauver_config()` est normal, mais n'oubliez pas d'appeler `sauver_config()`.
- Le journal est réécrit **en entier** à chaque sauvegarde (`DELETE` + `INSERT`)
- Le worker bulk est **mono-thread** : ne pas introduire de concurrence
- `templates/index.html` est monolithique (~3 000 l.) — extraire le JS est un
  chantier en cours

---

## 9. Administration

```powershell
python scripts/admin_comptes.py list
python scripts/admin_comptes.py reset <email>
python scripts/admin_comptes.py gmail <email>   # affiche le mot de passe en clair
```

L'outil demande le mot de passe **ADMIN** (hash scrypt dans `admin.key`).
Ce n'est **pas** l'authentification de l'interface (qui n'existe pas).

---

## 10. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `cryptography absent → secrets NON chiffrés` | Dépendance manquante | `pip install cryptography` |
| `Mot de passe illisible (clé absente)` | `secret.key` régénéré | Restaurer le fichier sauvegardé |
| `Auth refusée` | Mauvais mot de passe d'application | Régénérer sur Google |
| `Rate limit X/Y` | Quota atteint | Attendre la fenêtre glissante |
| `Attends Ns` | Délai inter-envois | Normal — attendre |
| `Aucun compte Gmail actif` | Aucun compte ou tous en pause | Ajouter / réactiver un compte |
| Le port 9999 échoue | Service Windows sur le port | `--port 9000` |
| Fenêtre blanche | navigateur absent | Installer le runtime navigateur |
| SMTP échoue | Réseau / pare-feu | Vérifier `smtp.gmail.com:465` |
| Erreur sans détail | Anti-fuite active | Consulter `.serveur web local/candimail.log` |

---

**© 2026 Dane hk \Manifest — Tous droits réservés.**