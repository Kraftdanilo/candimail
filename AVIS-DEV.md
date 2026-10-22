# Avis Dev Full Stack Senior (20 ans d'expérience)

Avis technique non intrusif sur Candimail v7 — rien de ceci n'a modifié le code,
ce sont des recommandations pour les prochaines itérations.

## 1. Architecture — les bons points
- Découpage propre `core / services / web` : c'est exactement la bonne séparation
  (métier, adaptateurs I/O, couche HTTP). Ne pas y toucher.
- Point d'entrée unique (`candimail.py`) : simple, testable, difficile à mal utiliser.
- Base SQLite unique (`app.db`) : le bon choix pour une app desktop mono-utilisateur.

## 2. Priorités que je recommande (par ordre de rentabilité)

### P1 — Extraire la logique métier des routes
`candimail/web/routes/divers.py` fait ~35 Ko : c'est le signal classique d'une
couche HTTP qui a avalé la logique métier. Règle que j'applique depuis 20 ans :
**une route doit valider, déléguer, répondre** — jamais décider. Déplacer les
règles métier vers `core/` (ex. `core/regles.py`) rend le code testable sans FastAPI
et réduit ce fichier de moitié.

### P2 — Suite de tests minimale
Aucun test visible. Pour une app qui envoie des e-mails en masse, le minimum vital :
- `tests/test_crypto.py` (chiffrement des secrets — régression = fuite de données)
- `tests/test_noyau.py` (logique d'envoi, avec SMTP/IMAP mockés)
- `tests/test_routes.py` (pytest + client httpx/TestClient, DB temporaire)
Une heure de setup, des mois de tranquillité.

### P3 — Purger `uploads/` automatiquement
Les CV uploadés s'accumulent (ex. fichier de 300 Ko jamais nettoyé). Ajouter une
rétention : à la suppression d'un contact, supprimer aussi son fichier uploadé,
+ un balayage au démarrage qui efface les orphelins (fichiers sans contact lié).

### P4 — Rotation des logs
`.webview/candimail.log` et `desktop.log` grossissent sans limite. Utiliser
`RotatingFileHandler` (max 1 Mo × 3) — deux lignes de config, problème réglé à vie.

### P5 — `.webview/EBWebView` re-gonfle à chaque lancement
C'est le cache Chromium de pywebview (~40 Mo ici). On ne peut pas le supprimer
définitivement, mais on peut le **délocaliser hors du projet** via la variable
d'environnement `WEBVIEW2_USER_DATA_FOLDER` (ex. vers `%LOCALAPPDATA%\Candimail`)
: le dossier du projet reste mince et un `git clean` ne casse plus la session.

## 3. Hygiène
- `requirements.txt` sans versions épinglées : épingler (`fastapi==x.y.z`, ...)
  sinon une mise à jour cassera l'app sans que vous sachiez pourquoi.
- Ajouter `__pycache__/`, `.webview/`, `uploads/`, `app.db` au `.gitignore`
  s'ils n'y sont pas déjà (données personnelles = jamais dans git).
- `secret.key` à la racine : correct pour du desktop, mais ne jamais le committer.

## 4. Ce que je ne ferais PAS
- Pas de migration vers Postgres/serveur : inutile pour du mono-utilisateur desktop.
- Pas de réécriture async partout : FastAPI + threads synchrones suffisent à cette échelle.
- Pas d'ajout de dépendances "par principe" — chaque dépendance est une dette.
