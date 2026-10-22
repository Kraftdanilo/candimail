# -*- coding: utf-8 -*-
t = open('templates/index.html', encoding='utf-8').read()
import re
print('IA codee en dur:', ('IA_MODELS' in t) or ('qwen/qwen3.8-27b' in t))
print('catalogue fetch:', 'api/ia/catalogue' in t)
print('recherche endpoint:', 'suivi/recherche' in t)
print('kpi duplique:', t.count('id="ov-total"'))
print('styles neo inline:', t.count('box-shadow:4px 4px 0'))
m = re.search(r'brand-sub">([^<]*)<', t)
print('brand-sub:', m.group(1) if m else 'absent')
m2 = re.search(r'<title>([^<]*)</title>', t)
print('titre:', m2.group(1))
