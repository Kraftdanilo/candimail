# Installation

> © 2026 Dane hk \Manifest — Licence MIT

---

## 1. Prérequis

| Élément | Exigence |
|---|---|
| Système | Windows 10 / 11 (le code fonctionne aussi sur macOS/Linux) |
| Python | **3.11 ou supérieur** |
| Navigateur | Edge ou Chrome (**navigateur** obligatoire sous Windows) |
| Compte Gmail | Validation en deux étapes **activée** |
| Espace disque | ~100 Mo + vos pièces jointes |

> navigateur est préinstallé sur Windows 10/11. S'il manque :

---

## 2. Installation depuis les sources

```powershell
# 1. Environnement virtuel (OBLIGATOIRE pour l'IDE)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Dépendances
pip install -r requirements.txt
```

> ⚠️ **VS Code / Pylance** : `.vscode/settings.json` pointe sur
> `.venv\Scripts\python.exe`. Sans ce venv, Pylance signale
> « Impossible de résoudre l'importation "uvicorn" / "serveur web local" » car ces
> paquets ne sont pas installés dans le Python système.
>
> Si les avertissements persistent : `Ctrl+Shift+P` → **Python: Select
> Interpreter** → choisir `.venv\Scripts\python.exe`, puis
> **Developer: Reload Window**.

### Dépendances installées

| Paquet | Version |
|---|---|
| fastapi | 0.115.0 |
| uvicorn | 0.30.6 |
| cryptography | 46.0.7 |
| openpyxl | 3.1.2 |
| httpx | 0.27.0 |
| python-multipart | 0.0.9 |

---

## 3. Lancement

Candimail est une **application web locale** (serveur + navigateur).
Un seul point d'entrée :

```bash
python candimail.py
```

Le serveur démarre sur un port libre ≥ **9999**, puis le navigateur
s'ouvre automatiquement sur `http://127.0.0.1:<port>/app`.

### Options de `candimail.py`

| Option | Effet |
|---|---|
| `--port 9000` | Impose le port (prioritaire sur `CANDIMAIL_PORT`) |
| `--lan` | Écoute sur `0.0.0.0` — accessible depuis téléphone/tablette/autre PC du réseau |
| `--debug` | Logs détaillés + `/api/debug/info` |
| `--help` | Affiche l'aide |

### Variables d'environnement

```bash
CANDIMAIL_PORT=9000          # port imposé
CANDIMAIL_HOST=0.0.0.0       # équivaut à --lan
CANDIMAIL_DEBUG=1            # logs détaillés
```

## 3.1 Plateformes : Windows, Linux, macOS

Le code est **portable** : chemins via `pathlib`, encodage UTF-8 explicite,
`socket` standard, aucune API Windows. Python ≥ 3.11 suffit.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python candimail.py
```

### Linux

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python candimail.py
```

### macOS

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python candimail.py
```

> **macOS** : la première utilisation peut déclencher une demande
> d'autorisation du pare-feu pour Python — acceptez-la. Le package
> `cryptography` nécessite parfois `brew install openssl` sur les vieux
> systèmes.

### Réseau, routeurs, changement d'IP

L'application est **insensible** à l'environnement réseau :

| Situation | Effet |
|---|---|
| Changement de routeur | Aucun — le serveur écoute, les clients se reconnectent à la nouvelle IP affichée au démarrage |
| IP dynamique (DHCP) | Aucun — `--lan` affiche l'IP détectée à chaque lancement (`ip_locale()`, UDP vers 10.255.255.255, portable) |
| Nouvelle IP publique | Aucun — tout le trafic sortant (SMTP/IMAP/IA) part de la machine, l'IP publique n'est jamais stockée |
| Wi-Fi ↔ Ethernet | Aucun — reconnexion automatique au prochain accès |

En mode **`--lan`**, notez l'URL affichée au démarrage
(`📱 Accès réseau local : http://<ip>:<port>/app`) : c'est celle que les
autres appareils du réseau doivent utiliser. Si elle change (DHCP),
relancez l'application ou réservez une IP fixe au PC dans le routeur
(bail statique) pour une adresse stable.

---

## 4. Configuration d'un compte Gmail

### 4.1 Obtenir un mot de passe d'application

1. Activez la **validation en deux étapes** :
   https://myaccount.google.com/security
2. Générez un mot de passe d'application :
   https://myaccount.google.com/apppasswords
3. Nom de l'application : `Candimail`
4. Copiez les **16 caractères** affichés (ils disparaissent ensuite)

### 4.2 L'ajouter dans l'application

Dans l'onglet **Comptes** :

1. Saisissez l'adresse Gmail et le mot de passe d'application
2. Choisissez un modèle de message (ou « Message global »)
3. Cliquez sur **🧪 Tester** pour vérifier la connexion
4. Le mot de passe est **chiffré** avant stockage

> Le bouton 👁️ de révélation est masqué par défaut. Voir
> [SECURITE.md](SECURITE.md#4-révélation-des-mots-de-passe--double-contrôle).

---

## 5. Premier lancement

Au premier démarrage, l'application :

1. **Crée la base** `app.db` (schéma SQLite + mode WAL)
2. **Migre** les anciens fichiers `config.json` et `envois.json` s'ils existent
3. **Génère** `secret.key` (clé de chiffrement Fernet)
4. **Chiffre** les mots de passe Gmail qui seraient encore en clair
5. **Crée** `uploads/` et `.serveur web local/`

### Bannière de démarrage

```
================================================================
  📧 CANDIMAIL — r0.0.1 — application de bureau (usage personnel)
  Créateur : Dane hk \Manifest   |   © 2026 — Licence MIT
================================================================
  Comptes Gmail : 1 actif(s)
  Pièces jointes: 1 active(s)
  Groupes       : 0
  Templates     : 1 perso + 3 prédéfinis
  Délai         : 40s (aléatoire)
  Serveur local : http://127.0.0.1:9999 (interne à la fenêtre)
================================================================
```

---

## 7. Mise à jour

```powershell
git pull
pip install -r requirements.txt
```

Les migrations de schéma sont automatiques (`db.init_db()`).

---

## 8. Sauvegarde

| Élément | Importance |
|---|---|
| `app.db` | 🔴 Données, journal, entreprises |
| `secret.key` | 🔴 **Sans lui, les mots de passe sont irrécupérables** |
| `uploads/` | 🟡 Pièces jointes |
| `config.json` | 🟡 Legacy — peut être supprimé après migration |

L'export JSON (`/api/export-json`) sauvegarde la config et le journal, mais
**pas** `secret.key`.

---

## 9. Désinstallation

1. Fermer l'application
2. Supprimer le dossier (ou `dist/` pour l'exe)
3. Supprimer les raccourcis éventuels

Aucune entrée de registre ni installation système : l'application est
entièrement contenue dans son dossier.

---

**© 2026 Dane hk \Manifest — Licence MIT**