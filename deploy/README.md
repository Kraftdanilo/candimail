# Candimail — Déploiement HTTPS derrière un reverse proxy

Candimail est une application Flask qui écoute **en local uniquement**
(`127.0.0.1:5000`). Pour l'exposer sur Internet en HTTPS, on place un reverse
proxy devant : il termine le TLS et relaie les requêtes vers Flask.

```
Internet ──HTTPS(443)──► [ Caddy / Nginx ] ──HTTP(5000)──► Flask (Candimail)
                              (TLS)                         127.0.0.1
```

## 1. Préparer Flask pour être derrière un proxy

Le reverse proxy doit indiquer à Flask que la requête d'origine était en HTTPS.
Candimail le détecte via deux variables d'environnement :

| Variable | Effet |
|---|---|
| `CANDIMAIL_BEHIND_PROXY=1` | Active `ProxyFix` (lit `X-Forwarded-Proto/For/Host`) + cookie de session `Secure` |
| `CANDIMAIL_HTTPS=1` | Force le cookie de session `Secure` même hors proxy |

Lancement derrière un proxy :

```bash
CANDIMAIL_BEHIND_PROXY=1 python app.py
```

> ⚠️ Ne mets **pas** ces variables quand tu testes en local en `http://` : un
> cookie `Secure` ne serait pas renvoyé par le navigateur sur `http://127.0.0.1`
> et le login casserait.

## 2. Option A — Caddy (le plus simple)

Caddy obtient et renouvelle automatiquement le certificat Let's Encrypt.

```bash
# 1. Édite deploy/Caddyfile et remplace candimail.exemple.com par ton domaine
# 2. Lance Candimail en local
CANDIMAIL_BEHIND_PROXY=1 python app.py &

# 3. Lance Caddy
caddy run --config deploy/Caddyfile
```

C'est tout : HTTPS, redirection HTTP→HTTPS et HSTS sont automatiques.

## 3. Option B — Nginx + certbot

```bash
# 1. Installer nginx et certbot
sudo apt install nginx certbot python3-certbot-nginx

# 2. Copier la config (remplace le domaine dedans)
sudo cp deploy/nginx.conf /etc/nginx/sites-available/candimail
sudo ln -s /etc/nginx/sites-available/candimail /etc/nginx/sites-enabled/
sudo nginx -t

# 3. Obtenir le certificat (certbot modifie la config ssl_* automatiquement)
sudo certbot --nginx -d candimail.exemple.com

# 4. Recharger nginx
sudo systemctl reload nginx
```

certbot installe aussi un renouvellement automatique (timer systemd).

## 4. Faire tourner Candimail comme service (Linux)

Un fichier `deploy/candimail.service` est fourni (systemd). Adapte les chemins
puis :

```bash
sudo cp deploy/candimail.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now candimail
```

## 5. En production, ne pas utiliser le serveur de dev Flask

`python app.py` lance le serveur de développement (mono-processus). Pour la
production, utilise un serveur WSGI. C'est `waitress` (portable, Windows/Linux,
pur Python) qui est le plus simple ici :

```bash
pip install waitress
CANDIMAIL_BEHIND_PROXY=1 waitress-serve --listen=127.0.0.1:5000 app:app
```

Ou `gunicorn` sur Linux :

```bash
pip install gunicorn
CANDIMAIL_BEHIND_PROXY=1 gunicorn -w 2 -b 127.0.0.1:5000 app:app
```

> Note : l'envoi groupé (bulk) tourne dans un thread. Avec `gunicorn -w 1` il n'y
> a qu'un seul processus, ce qui évite tout souci d'état partagé. Évite plus d'un
> worker si tu lances des campagnes groupées.

## 6. Vérifier que le HTTPS est bien actif

```bash
curl -I https://candimail.exemple.com
```

Tu dois voir :
- un code 200 (ou 302 vers /login),
- `Strict-Transport-Security: max-age=31536000; ...`,
- et une requête en `http://` qui redirige (301) vers `https://`.
