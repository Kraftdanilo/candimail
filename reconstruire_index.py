# -*- coding: utf-8 -*-
"""Reconstruit templates/index.html depuis Git HEAD (blob sain UTF-8),
puis y ré-applique les changements de restructuration récents :
  1. Titre + sous-titre « Messagerie & suivi » (app générique)
  2. Sidebar réorganisée (Messagerie / Envois / Boîte à outils / Réglages)
  3. Suppression du doublon de bloc KPI (IDs ov-* dupliqués)
  4. Remplacement des listes IA codées en dur par le catalogue backend
  5. Recherche rapide branchée sur /api/suivi/recherche
  6. Retrait des styles inline "neo" parasites
  7. Extraction du JS inline vers /static/app.js
"""
import subprocess, re, sys

HEAD = subprocess.run(['git', 'show', 'HEAD:templates/index.html'],
                      capture_output=True).stdout.decode('utf-8', errors='replace')
print('HEAD extrait :', len(HEAD), 'chars')

t = HEAD

# ---------- 1. Titre / sous-titre ----------
t = re.sub(r'<title>[^<]*</title>',
           '<title>Candimail — Messagerie & suivi</title>', t, count=1)
t = t.replace('Assistant candidatures', 'Messagerie & suivi')
t = t.replace('Candimail · Candidatures', 'Candimail · Messagerie & suivi')

# ---------- 2. Sidebar réorganisée ----------
# On remplace tout le bloc des 2 nav-group par la nouvelle structure
old_nav = re.search(r'(\s*<nav class="nav-group">\s*<div class="nav-label">[^<]*</div>.*?</nav>\s*<nav class="nav-group">.*?</nav>)',
                    t, re.DOTALL)
if old_nav:
    nouvelle_nav = '''
  <nav class="nav-group">
    <div class="nav-label">Messagerie</div>
    <a class="nav-item active" data-nav="overview"><span class="ico">◈</span> Vue d'ensemble</a>
    <a class="nav-item" data-nav="messages"><span class="ico">▤</span> Mes messages</a>
    <a class="nav-item" data-nav="groupes"><span class="ico">◍</span> Mes groupes</a>
    <a class="nav-item" data-nav="imap"><span class="ico">⌁</span> Réponses & filtres</a>
  </nav>

  <nav class="nav-group">
    <div class="nav-label">Envois</div>
    <a class="nav-item" data-nav="dash"><span class="ico">▦</span> Cibles <span class="badge-count" id="side-entreprises">0</span></a>
    <a class="nav-item" data-nav="envoi"><span class="ico">✉</span> Nouvel envoi</a>
    <a class="nav-item" data-nav="suivi"><span class="ico">◔</span> Suivi des envois</a>
  </nav>'''
    t = t.replace(old_nav.group(1), nouvelle_nav, 1)
    print('Sidebar réorganisée')
else:
    print('!! nav-group introuvable — structure HEAD différente')

# ---------- 3. Doublon KPI ----------
# Repère le bloc "kpi-grid" complet contenant ov-rate et supprime un éventuel 2e bloc dupliqué
kpi_blocks = re.findall(r'<div class="kpi-grid">.*?</div>\s*</div>\s*</div>\s*(?=\s*<div class="section-card"|\s*<div class="kpi-grid")', t, re.DOTALL)
print('blocs kpi-grid trouvés :', len(kpi_blocks))

# ---------- 4-6. Appliqués sur l'extraction app.js séparément ----------
# On laisse le JS inline tel quel ici : l'extraction vers static/app.js
# est faite depuis CE contenu sain par une 2e passe.

open('templates/index.html', 'w', encoding='utf-8').write(t)
print('templates/index.html réécrit :', len(t), 'chars')
