# -*- coding: utf-8 -*-
"""Évalue le checkpoint cline fcb84e3 comme base de restauration."""
import subprocess, re

REF = 'fcb84e3'
t = subprocess.run(['git', 'show', REF + ':templates/index.html'],
                   capture_output=True).stdout.decode('utf-8', errors='replace')

pages = ['overview', 'dash', 'envoi', 'suivi', 'imap', 'comptes',
         'messages', 'groupes', 'profil', 'params', 'historique']
m = re.search(r'brand-sub">([^<]*)<', t)
titre = re.search(r'<title>([^<]*)</title>', t)

print('longueur:', len(t))
print('brand-sub:', m.group(1) if m else 'n/a')
print('titre:', titre.group(1) if titre else 'n/a')
print('11 pages:', all('page-' + p in t for p in pages))
print('kpi duplique (ov-total):', t.count('id="ov-total"'))
print('emojis ok:', ('\u2709' in t) and ('\u25c8' in t))
print('accents (Réglages):', 'Réglages' in t)
print('panneau IA inline:', 'ia-provider' in t)
