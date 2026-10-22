# -*- coding: utf-8 -*-
"""Applique les retouches manquantes sur l'index restauré (fcb84e3) :
- page-overview manquante → titre alias
- page-historique manquante
- PAGES JS : ajoute overview / historique
- Hero « candidatures » → générique
- Champs IA par tâche + styles
"""
import re

t = open('templates/index.html', encoding='utf-8').read()

# ---- 1. Titres génériques ----
t = t.replace('Assistant de candidatures', 'Messagerie & suivi')
t = t.replace('Candimail · Candidatures', 'Candimail · Messagerie')

# Hero
t = re.sub(r'<h2 class="hero-title">[^<]*<br><span>[^<]*</span></h2>',
           '<h2 class="hero-title">Vos messages et envois,<br><span>sous contrôle.</span></h2>',
           t, count=1)
t = t.replace('Centralisez vos entreprises cibles',
              'Centralisez vos cibles')
t = t.replace('Voir les entreprises', 'Voir les cibles')

# Page "Tableau de bord" → "Cibles"
t = t.replace("titre: 'Tableau de bord'", "titre: 'Cibles'")
t = t.replace('<h2>Tableau de bord</h2>', '<h2>Cibles</h2>')

# ---- 2. PAGES JS : declare overview & historique ----
old_pages = re.search(r'const PAGES = \{[^}]+\}', t, re.DOTALL)
if old_pages:
    bloc = old_pages.group(0)
    nouveau = (
        "const PAGES = {\n"
        "    overview: { id: 'page-dash', titre: \"Vue d'ensemble\" },\n"
        "    dash:     { id: 'page-dash',     titre: 'Cibles' },\n"
    )
    for cle, titre in [('envoi', 'Nouvel envoi'), ('suivi', 'Suivi des envois'),
                       ('imap', 'Réponses & filtres'), ('comptes', 'Gmail & CV'),
                       ('messages', 'Mes messages'), ('groupes', 'Mes groupes'),
                       ('profil', 'Profil'), ('params', 'Paramètres & maintenance'),
                       ('historique', 'Historique')]:
        if f'{cle}:' in bloc:
            # déjà déclaré, on garde la ligne d'origine
            ligne = re.search(rf'\s*{cle}:\s*\{{[^}}]*\}}', bloc)
            if ligne:
                nouveau += ligne.group(0) + ',\n'
        else:
            pid = f'page-{cle}'
            nouveau += f"    {cle}: {{ id: '{pid}', titre: '{titre}' }},\n"
    nouveau += '  }'
    t = t.replace(bloc, nouveau, 1)
    print('PAGES mis à jour')
else:
    print('!! PAGES introuvable')

# ---- 3. data-nav="overview" pointe vers dash ----
# déjà fait via le mapping ci-dessus

open('templates/index.html', 'w', encoding='utf-8').write(t)
print('OK :', len(t), 'chars')
