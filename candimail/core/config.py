#!/usr/bin/env python3
"""
Constantes de Candimail — chemins, configuration par défaut,
CV par défaut et templates de lettres prédéfinis.
"""
from pathlib import Path


# ============================================================
# CHEMINS — exécution directe via .venv (pas d'exécutable gelé).
# Racine projet = parent du package (…/autogmail), pas candimail/core.
# ============================================================
def _racine_projet():
    from pathlib import Path as _P
    # candimail/core/config.py → racine = parents[2]
    return _P(__file__).resolve().parents[2]


BASE_DIR = _racine_projet()
RESS_DIR = _racine_projet()
RACINE = _racine_projet()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

CONFIG_FILE = BASE_DIR / "config.json"
LOG_FILE    = BASE_DIR / "envois.json"

# ============================================================
# CONFIG PAR DÉFAUT
# ============================================================
DEFAULT_CONFIG = {
    "candidat": {
        "nom":     "Candidat Démo",
        "tel":     "+000 00 00 00 00",
        "email":   "candidat.demo@exemple.com",
        "ville":   "Ma Ville",
        "pays":    "Côte d'Ivoire",
        "diplome": "Votre diplôme (à personnaliser)",
        "spec":    "Votre spécialité (à personnaliser)",
    },
    "comptes": [{
        "email": "compte.demo@exemple.com",
        "password": "",
        "actif": False,
    }],
    "parametres": {
        "delai_secondes":   40,
        "delai_aleatoire":  False,
        "delai_min":        35,
        "delai_max":        55,
        "max_par_heure":    100,
        "smtp_timeout":     30,
        "smtp_retries":     3,
        "template":         "standard",
    },
    "pieces_jointes": {},
    "imap": {
        "derniere_verif": 0,
        "auto_verif":     True,
        "intervalle_min": 30,
    },
    "filtres_gmail": [],
    "groupes": [],
    "templates_perso": [
        {
            "id": "tpl_candidature",
            "nom": "Candidature stage",
            "categorie": "candidature",
            "objet": "Demande de stage rémunéré — Génie Civil — {entreprise}",
            "corps": """Bonjour,

{contexte}

Titulaire d'une {diplome}, spécialité {spec}, je suis actuellement à la
recherche d'un stage pratique me permettant de mettre en application mes
connaissances et de contribuer concrètement à vos projets.

Je me permets de préciser que je recherche un stage rémunéré, afin de
couvrir mes frais de déplacement et de subsistance pendant cette période
de formation pratique. Je reste néanmoins ouvert à toute formule que
vous jugerez adaptée.

Je suis basé à {ville} et entièrement mobile pour me déplacer sur vos
chantiers ou dans vos bureaux à travers le pays.

Compétences principales :
  • Conception et dimensionnement d'ouvrages (béton armé, charpente)
  • Logiciels CAO/DAO : AutoCAD, ArchiCAD
  • Programmation : Python, VS Code (automatisation, scripts)
  • Suivi de chantier et contrôle qualité
  • Lecture et exploitation de plans d'exécution

Vous trouverez en pièces jointes mon CV détaillé. Je reste à votre
entière disposition pour un entretien à votre convenance.

{nom}
Tél : {tel}
Email : {email}
{ville}, Côte d'Ivoire"""
        },
        {
            "id": "tpl_parents",
            "nom": "Information parents d'élèves",
            "categorie": "parents",
            "objet": "Information importante — {entreprise}",
            "corps": """Bonjour chers parents,

{contexte}

Merci de votre attention et de votre compréhension.

Cordialement,
{nom}
Tél : {tel}"""
        },
        {
            "id": "tpl_collegues",
            "nom": "Message collègues",
            "categorie": "collegues",
            "objet": "{entreprise}",
            "corps": """Bonjour,

{contexte}

Bien cordialement,
{nom}"""
        },
    ],
}

# ============================================================
# CV PAR DÉFAUT
# ============================================================
DEFAULT_CV = {
    "titre": "Stagiaire Génie Civil",
    "resume": "Étudiant en génie civil, motivé et mobile sur tout le territoire, "
              "je recherche un stage pratique pour mettre en application mes "
              "connaissances théoriques et contribuer concrètement aux projets "
              "de votre entreprise.",
    "experiences": [
        {"date": "2022 — Aujourd'hui", "titre": "Projets académiques",
         "lieu": "Soubré / Abidjan", "description":
            "Conception et dimensionnement d'ouvrages (béton armé, charpente), "
            "métrés et études de prix, lecture et exploitation de plans d'exécution."},
    ],
    "formations": [
        {"date": "2023 — 2026", "titre": "Licence en Génie Civil — option Bâtiment",
         "lieu": "Abidjan", "description":
            "Structure, matériaux, topographie, technologie de construction, "
            "informatique appliquée au BTP (AutoCAD, ArchiCAD, Python)."},
    ],
    "competences": [
        "Conception et dimensionnement (béton armé, charpente)",
        "Logiciels CAO/DAO : AutoCAD, ArchiCAD",
        "Programmation : Python, VS Code (automatisation, scripts)",
        "Suivi de chantier et contrôle qualité",
        "Lecture et exploitation de plans d'exécution",
        "Métrés, études de prix et dossiers techniques",
    ],
    "langues": ["Français (courant)", "Anglais (intermédiaire)"],
    "references": [],
}

# ============================================================
# TEMPLATES PRÉDÉFINIS
# ============================================================
TEMPLATES = {
    "standard": {
        "nom": "Standard (équilibré)",
        "objet": "Demande de stage rémunéré — Génie Civil — {entreprise}",
        "corps": """Bonjour,

{contexte}

Titulaire d'une {diplome}, spécialité {spec}, je suis actuellement à la recherche
d'un stage pratique me permettant de mettre en application mes connaissances et
de contribuer concrètement à vos projets.

Je me permets de préciser que je recherche un stage rémunéré, afin de couvrir
mes frais de déplacement et de subsistance pendant cette période de formation
pratique. Je reste néanmoins ouvert à toute formule que vous jugerez adaptée.

Je suis basé à {ville} et entièrement mobile pour me déplacer sur vos chantiers
ou dans vos bureaux à travers le pays.

Compétences principales :
  • Conception et dimensionnement d'ouvrages (béton armé, charpente)
  • Logiciels CAO/DAO : AutoCAD, ArchiCAD
  • Programmation : Python, VS Code (automatisation, scripts)
  • Suivi de chantier et contrôle qualité
  • Lecture et exploitation de plans d'exécution

Vous trouverez en pièces jointes mon CV détaillé. Je reste à votre entière
disposition pour un entretien à votre convenance, en présentiel ou en
visioconférence.

Je vous remercie par avance pour l'attention que vous porterez à ma candidature
et vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations
distinguées.

{nom}
Tél : {tel}
Email : {email}
{ville}, {pays}""",
    },
    "direct": {
        "nom": "Direct (concis)",
        "objet": "Stage Génie Civil — {entreprise}",
        "corps": """Bonjour,

{contexte}

Étudiant en {diplome} (spécialité {spec}), je cherche un stage rémunéré pour
mettre en pratique ma formation et apprendre à vos côtés.

Disponible immédiatement, mobile depuis {ville}, je peux rejoindre vos équipes
sur chantier ou en bureau d'études.

Compétences : AutoCAD, ArchiCAD, suivi de chantier, lecture de plans, Python.

CV en pièce jointe. Disponible pour un entretien à votre convenance.

Cordialement,
{nom}
{tel} — {email}""",
    },
    "formel": {
        "nom": "Formel (grands groupes)",
        "objet": "Candidature pour un stage — Génie Civil — {entreprise}",
        "corps": """Madame, Monsieur,

{contexte}

Je me permets de vous soumettre ma candidature pour un stage au sein de votre
entreprise, dans le cadre de ma formation en {diplome}, spécialité {spec}.

Actuellement à la recherche d'une structure d'accueil pour un stage rémunéré,
je souhaite mettre à profit mes connaissances théoriques et mon envie
d'apprendre au service de vos projets.

Mon profil :
  • Formation : {diplome}, spécialité {spec}
  • Outils : AutoCAD, ArchiCAD, Python, VS Code
  • Mobilité : basé à {ville}, disponible partout dans le pays

Vous trouverez mon curriculum vitæ en pièce jointe. Je me tiens à votre
disposition pour tout complément d'information et pour un entretien à votre
meilleure convenance.

Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur,
l'expression de ma considération distinguée.

{nom}
Tél : {tel}
Email : {email}""",
    },
}
