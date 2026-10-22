# Installation

> © 2026 Dane hk \Manifest — Tous droits réservés.

---

## 1. Prérequis

| Élément | Exigence |
|---|---|
| Système | Windows 10 / 11 (le code fonctionne aussi sur macOS/Linux) |
| Python | **3.11 ou supérieur** |
| Navigateur | Edge ou Chrome (**WebView2** obligatoire sous Windows) |
| Compte Gmail | Validation en deux étapes **activée** |
| Espace disque | ~100 Mo + vos pièces jointes |

> WebView2 est préinstallé sur Windows 10/11. S'il manque :
> https://developer.microsoft.com/microsoft-edge/webview2/

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
> « Impossible de résoudre l'importation "waitress" / "webview" » car ces
> paquets ne sont pas installés dans le Python système.
>
> Si les avertissements persistent : `Ctrl+Shift+P` → **Python: Select
> Interpreter** → choisir `.venv\Scripts\python.exe`, puis
> **Developer: Reload Window**.

### Dépendances installées

| Paquet | Version |
|---|---|
| Flask | 3.0.0 |
| cryptography | 46.0.7 |
| openpyxl | 3.1.2 |
| pywebview | 6.2.1 |
| waitress | 3.0.2 |

---

## 3. Lancement

Candimail est une **application de bureau**. Un seul point d'entrée :

```powershell
python candimail.py
```

Le serveur démarre sur un port libre ≥ **9999** (interne à la fenêtre), puis
une fenêtre native s'ouvre. L'application attend `/api/health` avant de
l'afficher.

### Options de `candimail.py`

| Option | Effet |
|---|---|
| `--port 9000` | Impose le port (prioritaire sur `CANDIMAIL_PORT`) |
| `--debug` | Logs détaillés + console de développement WebView2 |
| `--plein-ecran` | Démarre en plein écran |
| `--help` | Affiche l'aide |

### Variables d'environnement

```powershell
$env:CANDIMAIL_PORT = "9000"          # port imposé
$env:CANDIMAIL_DEBUG = "1"            # logs détaillés + /api/debug/info
```

> Il n'existe **pas** de mode serveur ni de mode navigateur : l'application
> fonctionne exclusivement dans sa fenêtre pywebview.

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
5. **Crée** `uploads/` et `.webview/`

### Bannière de démarrage

```
================================================================
  📧 CANDIMAIL — v7 — application de bureau (usage personnel)
  Créateur : Dane hk \Manifest   |   © 2026 — Tous droits réservés
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

**© 2026 Dane hk \Manifest — Tous droits réservés.**