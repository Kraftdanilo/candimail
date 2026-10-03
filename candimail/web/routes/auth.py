#!/usr/bin/env python3
"""
Routes Flask — application mono-utilisateur (blueprint).

L'authentification a été retirée : Candimail est un outil local
personnel. L'utilisateur 1 est automatiquement considéré comme
connecté sur chaque requête (cf. app.py / _utilisateur_courant).
"""
import io, csv, json, os, re, socket, time, threading, uuid
from datetime import datetime, timedelta
from pathlib import Path

from flask import (Blueprint, jsonify, request, render_template, Response,
                   send_file, session, redirect)

from candimail.core import db, crypto
from candimail.core.config import (BASE_DIR, UPLOADS_DIR, CONFIG_FILE, LOG_FILE,
                        DEFAULT_CONFIG, DEFAULT_CV, TEMPLATES)
from candimail.core.noyau import (current_uid, charger_config, sauver_config, _config_globale,
                   charger_log, sauver_log, get_delai, check_rate_limit,
                   maintenant_str, parse_emails, get_comptes_actifs,
                   compte_suivant, _get_template, build_letter, build_subject,
                   get_pieces_actives, recharger_pieces, _pieces,
                   _config_lock, _config_cache, _log_lock, _send_lock,
                   _log_send_lock, _bulk_lock, _bulk_running, _bulk_state,
                   _compte_index, _auth_attempts, _send_timestamps,
                   _last_send_time, _txt, _email_valide)
from candimail.services.smtp import envoyer_email, _envoyer_un_email
from candimail.services.imap import (check_imap_compte, verifier_toutes_boites,
                          appliquer_filtres_compte, _filtre_valide,
                          _ACTIONS_VALIDES)

bp = Blueprint("auth", __name__)
