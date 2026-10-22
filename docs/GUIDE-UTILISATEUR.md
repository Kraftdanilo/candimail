# Guide utilisateur

> © 2026 Dane hk \Manifest — Licence MIT

Guide fonctionnel complet, du premier lancement à l'envoi de masse.

---

## Sommaire

1. [Premiers pas](#1-premiers-pas) · 2. [Comptes Gmail](#2-comptes-gmail) ·
3. [Profil](#3-profil) · 4. [CV](#4-cv) ·
5. [Modèles de lettres](#5-modèles-de-lettres) ·
6. [Entreprises](#6-entreprises) · 7. [Envoyer un e-mail](#7-envoyer-un-e-mail) ·
8. [Envoi de masse](#8-envoi-de-masse) · 9. [Groupes](#9-groupes) ·
10. [Suivi des envois](#10-suivi-des-envois) ·
11. [Filtres Gmail](#11-filtres-gmail) · 12. [Pièces jointes](#12-pièces-jointes) ·
13. [Paramètres](#13-paramètres) · 14. [Sauvegarde](#14-sauvegarde)

---

## 1. Premiers pas

Au lancement, la le navigateur s'ouvre sur l'application. La barre supérieure donne
accès aux sections : **Messagerie**, **Cibles**, **Envois**, **Réponses & filtres**, **Réglages**.

**Ordre de configuration recommandé**

1. Renseigner le **profil candidat** (section 3)
2. Ajouter un **compte Gmail** (section 2)
3. Vérifier le **modèle de lettre** (section 5)
4. Ajouter des **entreprises** (section 6)
5. Joindre le **CV** (section 12)
6. Lancer un **envoi de masse** (section 8)

---

## 2. Comptes Gmail

### Ajouter un compte

1. Onglet **Comptes** → bouton d'ajout
2. Adresse Gmail
3. Mot de passe d'application (16 caractères)
4. Modèle de message : « Message global » ou un modèle spécifique
5. **Enregistrer**

Le mot de passe est chiffré avant stockage.

### Tester la connexion

Le bouton **🧪 Tester** ouvre une connexion SMTP réelle.
- ✅ `SMTP OK` : identifiants valides
- ❌ `Auth refusée` : mot de passe d'application incorrect
- ⚠️ Erreur réseau : vérifiez votre connexion

### Plusieurs comptes

Les comptes sont utilisés en **rotation round-robin**. Répartir les envois sur
plusieurs boîtes réduit le risque de signalement de spam.

### Statut des comptes

| Icône | État |
|---|---|
| ▶️ | En pause (ignoré par la rotation) |
| ⏸️ | Actif |
| 🗑️ | Supprimer |

---

## 3. Profil candidat

Ces informations sont injectées dans les lettres via les variables
`{nom}`, `{tel}`, `{email}`, `{ville}`, `{diplome}`, `{spec}`.

| Champ | Usage |
|---|---|
| Nom | Signature `{nom}` |
| Téléphone | Signature `{tel}` |
| Email | Signature `{email}` et adresse d'envoi |
| Ville | Signature `{ville}` |
| Diplôme | `{diplome}` |
| Spécialité | `{spec}` |

---

## 4. CV

L'onglet **CV** permet de saisir et organiser un curriculum complet :

- **Identité** : titre, nom, ville, résumé
- **Expériences** : date, titre, lieu, description
- **Formations**, **Références**, **Compétences**, **Langues**

Le bouton **🖨️ Imprimer** génère un document mis en page.

> ⚠️ Si la page paraît vide, enregistrez d'abord (le CV n'existe pas tant
> qu'aucune sauvegarde n'a été faite).

---

## 5. Modèles de lettres

### Modèles prédéfinis (3)

| Modèle | Ton | Usage |
|---|---|---|
| **Standard** | Équilibré | Candidature classique |
| **Direct** | Concis | Approche rapide |
| **Formel** | Soutenu | Grands groupes, administrations |

### Créer un modèle personnalisé

1. Onglet **Templates** → **✏️ Nouveau message**
2. Nom, catégorie, objet, corps
3. **Variables disponibles** :

| Variable | Remplacée par |
|---|---|
| `{entreprise}` | Nom de l'entreprise |
| `{contexte}` | Contexte saisi pour cette entreprise |
| `{nom}` `{tel}` `{email}` `{ville}` `{diplome}` `{spec}` | Profil candidat |

4. **📋** duplique, **🗑️** supprime

---

## 6. Entreprises

### Ajouter manuellement

1. Onglet **Entreprises**
2. Nom, e-mail de contact, catégorie, contexte
3. **Enregistrer**

### Catégories

| Catégorie | Usage |
|---|---|
| **Grands groupes** | Grandes entreprises, administrations |
| **PME** | Petites et moyennes entreprises |
| **Porte-à-porte** | Prospection directe |

### Importer en masse

Le bouton d'import permet d'ajouter une liste d'un coup
(`POST /api/companies/seed`). Les doublons sont ignorés automatiquement.

### Modifier

Le bouton ✏️ permet de corriger un nom ou un e-mail.
**Un renommage déplace aussi l'entrée du journal** : l'historique est conservé.

---

## 7. Envoyer un e-mail

### Étapes

1. Sélectionnez une entreprise (ou saisissez le destinataire)
2. Choisissez un **modèle**
3. Renseignez le **contexte** (projet, chantier, poste visé…)
4. **👁️ Aperçu** pour vérifier le rendu
5. **📤 Envoyer**

### Deux modes

| Mode | Comportement |
|---|---|
| **Individuel** (défaut) | Un e-mail par destinataire, avec `{entreprise}` personnalisé |
| **Groupe** | Un seul e-mail, tous les destinataires **en copie cachée** |

> Le mode groupe est plus rapide mais les destinataires ne se voient pas.

### Pièces jointes

Cochez les PDF à joindre (section 12). La ligne **Sans PJ** du journal
indique si l'envoi en comportait.

---

## 8. Envoi de masse

### Lancer

1. Onglet **Envoi de masse**
2. Sélectionner les entreprises à contacter
3. Choisir le modèle et le contexte
4. **▶️ Démarrer**

Le worker envoie **un e-mail à la fois**, en respectant :
- le **délai** entre chaque envoi (40 s par défaut)
- le **plafond horaire** (100 envois)

### Pendant l'envoi

La barre de progression indique l'entreprise en cours, le compteur
`envoyés/erreurs` et le temps d'attente éventuel.

| Situation | Comportement |
|---|---|
| Quota atteint | **Attend** que la fenêtre d'1 h se libère, puis reprend |
| Pause de la fenêtre | Ferme l'application proprement |
| En cours | Affiche ⏳ attente rate limit (Xs) |

### Arrêter

Le bouton **⏹️ Arrêter** provoque un arrêt **coopératif** : l'entreprise en
cours est terminée, puis le traitement s'interrompt.

> ⚠️ Le respect des quotas est la protection principale de la réputation de
> votre boîte. Ne réduisez pas excessivement le délai.

---

## 9. Groupes

Un **groupe** regroupe plusieurs contacts pour un envoi identique.

### Créer

1. Onglet **Groupes** → nom, description
2. Saisir les adresses (séparées par virgules ou point-virgule)
3. **Enregistrer**

Les adresses sont **validées strictement** : les entrées invalides sont
écartées.

### Envoyer à un groupe

1. Bouton d'envoi sur le groupe
2. Objet, corps (ou modèle)
3. Mode **individuel** ou **groupe**
4. Cocher **joindre les pièces** si souhaité
5. Valider

Le journal enregistre une entrée `[GROUPE] <nom>` avec le détail des envois.

---

## 10. Suivi des envois

La page **`/suivi`** présente :

| Indicateur | Signification |
|---|---|
| **Total** | Entreprises contactées |
| **Envoyés** | Envois réussis |
| **Réponses** | Réponses reçues (détection IMAP) |
| **Bounces** | Adresses invalides |
| **Graphique** | Répartition sur 7 jours |

### Détection automatique

La boucle IMAP (toutes les 60 s) :
1. Recherche les messages reçus depuis N jours
2. Compare l'expéditeur aux adresses du journal
3. Marque les entreprises ayant répondu
4. Détecte les bounces (`X-Failed-Recipients`)

Vous pouvez forcer une vérification via le bouton dédié.

### Marquer manuellement

Le bouton **✔** bascule l'état « répondu » à la main.

### Exports

| Format | Contenu |
|---|---|
| **CSV** | Journal complet |
| **Excel** | 3 feuilles : Envois, Statistiques, Candidat |
| **JSON** | Sauvegarde complète (hors secrets) |

---

## 11. Filtres Gmail

Des règles classent automatiquement les e-mails reçus.

### Règles par défaut (6)

Bourse · Opportunité · Travail · Université · Social · Annonce

### Actions possibles

| Action | Effet |
|---|---|
| `label` | Applique un libellé Gmail |
| `archive` | Archive le message |
| `marquer_lu` | Marque comme lu |
| `supprimer` | Supprime le message |
| `notify` | Génère une notification dans l'app |

### Priorité

Les règles sont triées par **`priority` croissante** : la **première règle qui
correspond** classe le message, les suivantes sont ignorées pour ce message.
Les règles issues de l'apprentissage utilisent `priority: 0` et gagnent donc
sur tout.

### Réordonner

Le glisser-déposer modifie la priorité (1, 2, 3…).

### Apprentissage

Quand un mail est mal classé, indiquez l'expéditeur et le libellé correct :
la règle est créée/mise à jour automatiquement et ses corrections sont
comptées. Au-delà de 3 corrections, une **suggestion** est proposée.

### Libellés

Le bouton de création des libellés crée directement dans Gmail les libellés
définis par les règles — y compris ceux sans mail correspondant.

---

## 12. Pièces jointes

### Ajouter

1. Onglet **Pièces jointes**
2. **PDF uniquement**, 20 Mo maximum

### Activer / désactiver

Chaque PDF a un interrupteur : un PDF désactivé n'est pas joint, sans être
supprimé.

### Supprimer

Le bouton 🗑️ supprime définitivement le fichier.

---

## 13. Paramètres

| Paramètre | Défaut | Rôle |
|---|---|---|
| Délai entre envois | 40 s | Pause minimale |
| Délai aléatoire | non | Active une durée variable |
| Bornes aléatoires | 35–55 s | Amplitude |
| Max par heure | 100 | Quota horaire |
| Timeout SMTP | 30 s | Délai de connexion |
| Retries SMTP | 3 | Nombre de tentatives |
| Modèle global | standard | Modèle par défaut |

### IMAP

| Paramètre | Défaut |
|---|---|
| Vérification auto | activée |
| Intervalle | 30 minutes |
| Jours d'historique | 30 |

---

## 14. Sauvegarde

### Sauvegarde automatique

Le bouton **Reset log** archive le journal dans `envois.backup.json` avant de
le vider.

### Export manuel

L'export JSON produit un fichier contenant la configuration et le journal.

### Restauration

**Importer un JSON** fusionne les entrées dans le journal existant.

> 🔴 **Sauvegardez `secret.key` séparément.** Sans cette clé, les mots de passe
> Gmail chiffrés sont irrécupérables.

---

**© 2026 Dane hk \Manifest — Licence MIT**