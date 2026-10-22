#!/usr/bin/env python3
"""
Agent IA multi-fournisseur — appels d'API LLM pour Candimail.

Configuration PAR TÂCHE : chaque fonctionnalité (rédiger, classer, résumer,
etc.) peut avoir son propre fournisseur, modèle, clé API et paramètres.

Fournisseurs supportés (gratuits, clé API fournie par l'utilisateur) :
- Groq         : openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.8-27b
- Google AI    : gemini-3.5-flash-lite, gemini-2.5-flash
- Mistral AI   : mistral-small-2603, ministral-3b, ministral-8b

Les clés API ne sont JAMAIS stockées en dur : elles viennent du front
(localStorage) ou d'un fichier de config local (data/ia_config.json).
"""
from __future__ import annotations

import json, os, time
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

import httpx

from candimail.core.config import DATA_DIR


# ---------------------------------------------------------------------------
# Modèles gratuits vérifiés (octobre 2026)
# ---------------------------------------------------------------------------
GROQ_MODELS = {
    "openai/gpt-oss-120b": {"ctx": 131072, "rpm_free": 30, "rpd_free": 1000},
    "openai/gpt-oss-20b":  {"ctx": 131072, "rpm_free": 30, "rpd_free": 1000},
    "qwen/qwen3.8-27b":    {"ctx": 131072, "rpm_free": 30, "rpd_free": 1000},
}

GOOGLE_MODELS = {
    "gemini-3.5-flash-lite": {"ctx": 1048576, "rpd_free": 1500},
    "gemini-2.5-flash":      {"ctx": 1048576, "rpd_free": 1500},
}

MISTRAL_MODELS = {
    "mistral-small-2603": {"ctx": 262144},
    "ministral-3b":       {"ctx": 256000},
    "ministral-8b":       {"ctx": 256000},
}

# Tâches IA supportées
IA_TASKS = {
    "rediger":   {"label": "Rédiger une réponse", "default_model": "openai/gpt-oss-120b"},
    "classifier": {"label": "Classer un email", "default_model": "openai/gpt-oss-20b"},
    "resumer":   {"label": "Résumer un fil", "default_model": "gemini-3.5-flash-lite"},
}


IA_CONFIG_FILE = DATA_DIR / "ia_config.json"


def charger_config_ia() -> dict:
    """Charge la config IA depuis le fichier local (data/ia_config.json)."""
    try:
        if IA_CONFIG_FILE.exists():
            return json.loads(IA_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def sauver_config_ia(data: dict) -> None:
    """Sauvegarde la config IA dans le fichier local."""
    IA_CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class IAConfig:
    provider: str = "groq"          # groq | google | mistral
    api_key: str = ""
    model: str = "openai/gpt-oss-120b"
    temperature: float = 0.7
    max_tokens: int = 2048
    base_url: str = ""

    def default_base_url(self) -> str:
        if self.provider == "groq":
            return "https://api.groq.com/openai/v1"
        if self.provider == "google":
            return "https://generativelanguage.googleapis.com/v1beta"
        if self.provider == "mistral":
            return "https://api.mistral.ai/v1"
        return ""


@dataclass
class IAResponse:
    text: str
    model: str
    provider: str
    tokens_in: Optional[int] = None
    tokens_out: Optional[int] = None
    duration_ms: int = 0


class IAAgentError(Exception):
    """Erreur agente IA — message public sans détail technique."""


class IAAgent:
    """Appelle l'API LLM du fournisseur choisi avec la clé de l'utilisateur.

    Configuration par tâche : chaque méthode métier utilise la config de sa
    propre tâche (rédiger, classifier, resumer...).
    """

    def __init__(self):
        self._configs: dict[str, IAConfig] = {}
        self._load_all()
        self._client: Optional[httpx.AsyncClient] = None

    def _load_all(self) -> None:
        """Charge toutes les configs de tâches depuis le fichier."""
        data = charger_config_ia()
        for task_id in IA_TASKS:
            task_data = data.get(task_id, {})
            self._configs[task_id] = IAConfig(
                provider=task_data.get("provider", "groq"),
                api_key=task_data.get("apiKey", ""),
                model=task_data.get("model", IA_TASKS[task_id]["default_model"]),
                temperature=task_data.get("temperature", 0.7),
                max_tokens=task_data.get("max_tokens", 2048),
            )

    def get_config(self, task_id: str) -> IAConfig:
        """Renvoie la config de la tâche demandée (défaut groq si inconnue)."""
        return self._configs.get(task_id, IAConfig())

    def set_config(self, task_id: str, cfg: IAConfig) -> None:
        """Définit la config d'une tâche et la persiste."""
        self._configs[task_id] = cfg
        data = charger_config_ia()
        data[task_id] = asdict(cfg)
        # Normaliser les clés pour le front
        data[task_id]["provider"] = cfg.provider
        data[task_id]["apiKey"] = cfg.api_key
        data[task_id]["model"] = cfg.model
        data[task_id]["temperature"] = cfg.temperature
        data[task_id]["max_tokens"] = cfg.max_tokens
        sauver_config_ia(data)

    def get_all_configs(self) -> dict[str, dict]:
        """Renvoie toutes les configs sérialisables pour le front."""
        out = {}
        for task_id, cfg in self._configs.items():
            out[task_id] = {
                "provider": cfg.provider,
                "apiKey": cfg.api_key,
                "model": cfg.model,
                "temperature": cfg.temperature,
                "max_tokens": cfg.max_tokens,
            }
        return out

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    async def close(self):
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # ---------------------------------------------------------------
    # CHAT COMPLETION (point d'entrée unique par tâche)
    # ---------------------------------------------------------------
    async def chat(self, task_id: str, messages: list[dict[str, str]]) -> IAResponse:
        cfg = self.get_config(task_id)
        start = time.time()
        try:
            if cfg.provider == "groq":
                return await self._chat_groq(cfg, messages, start, task_id)
            if cfg.provider == "google":
                return await self._chat_google(cfg, messages, start, task_id)
            if cfg.provider == "mistral":
                return await self._chat_mistral(cfg, messages, start, task_id)
            raise IAAgentError(f"Fournisseur IA inconnu : {cfg.provider}")
        except httpx.HTTPStatusError as e:
            detail = ""
            try:
                detail = e.response.json().get("error", {}).get("message", str(e))
            except Exception:
                detail = e.response.text[:200]
            raise IAAgentError(f"Erreur API IA ({e.response.status_code}) : {detail}")
        except httpx.RequestError as e:
            raise IAAgentError(f"Impossible de joindre l'API IA : {type(e).__name__}")
        except IAAgentError:
            raise
        except Exception as e:
            raise IAAgentError(f"Erreur IA inattendue : {type(e).__name__}")

    # ---------------------------------------------------------------
    # GROQ (OpenAI-compatible)
    # ---------------------------------------------------------------
    async def _chat_groq(self, cfg, messages, start, task_id):
        client = await self._get_client()
        url = f"{cfg.default_base_url()}/chat/completions"
        payload = {
            "model": cfg.model,
            "messages": messages,
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_tokens,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        }
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        choice = data["choices"][0]
        text = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})
        return IAResponse(
            text=text,
            model=cfg.model,
            provider=cfg.provider,
            tokens_in=usage.get("prompt_tokens"),
            tokens_out=usage.get("completion_tokens"),
            duration_ms=int((time.time() - start) * 1000),
        )

    # ---------------------------------------------------------------
    # GOOGLE AI STUDIO (Gemini)
    # ---------------------------------------------------------------
    async def _chat_google(self, cfg, messages, start, task_id):
        client = await self._get_client()
        model_id = cfg.model
        url = f"{cfg.default_base_url()}/models/{model_id}:generateContent?key={cfg.api_key}"

        contents = []
        system_instruction = None
        for m in messages:
            role = m.get("role", "user")
            parts = [{"text": m.get("content", "")}]
            if role == "system":
                system_instruction = {"parts": parts}
            elif role == "user":
                contents.append({"role": "user", "parts": parts})
            elif role == "assistant":
                contents.append({"role": "model", "parts": parts})

        payload: dict[str, Any] = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = system_instruction
        payload["generationConfig"] = {
            "temperature": cfg.temperature,
            "maxOutputTokens": cfg.max_tokens,
        }

        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise IAAgentError("Aucune réponse générée par Gemini")
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        usage = data.get("usageMetadata", {})
        return IAResponse(
            text=text,
            model=model_id,
            provider=cfg.provider,
            tokens_in=usage.get("promptTokenCount"),
            tokens_out=usage.get("candidatesTokenCount"),
            duration_ms=int((time.time() - start) * 1000),
        )

    # ---------------------------------------------------------------
    # MISTRAL AI (La Plateforme)
    # ---------------------------------------------------------------
    async def _chat_mistral(self, cfg, messages, start, task_id):
        client = await self._get_client()
        url = f"{cfg.default_base_url()}/chat/completions"
        payload = {
            "model": cfg.model,
            "messages": messages,
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        }
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        choice = data["choices"][0]
        text = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})
        return IAResponse(
            text=text,
            model=cfg.model,
            provider=cfg.provider,
            tokens_in=usage.get("prompt_tokens"),
            tokens_out=usage.get("completion_tokens"),
            duration_ms=int((time.time() - start) * 1000),
        )

    # ---------------------------------------------------------------
    # HELPERS MÉTIER (Gmail) — chaque méthode utilise sa propre tâche
    # ---------------------------------------------------------------
    async def classifier_email(
        self, sujet: str, expediteur: str, corps: str
    ) -> dict[str, Any]:
        """Classifie un email (libellé, urgence, catégorie) — tâche 'classifier'."""
        prompt = (
            "Tu es un assistant de classement d'emails professionnels. "
            "Réponds UNIQUEMENT en JSON avec les clés : libelle, urgence, categorie, raison.\n"
            f"Sujet : {sujet}\nExpéditeur : {expediteur}\nCorps : {corps[:2000]}"
        )
        resp = await self.chat("classifier", [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Classifie cet email."},
        ])
        try:
            return json.loads(resp.text)
        except Exception:
            return {"libelle": "Autre", "urgence": "normale", "categorie": "divers", "raison": resp.text[:200]}

    async def rediger_reponse(
        self, email_origine: str, profil_candidat: str, contexte: str = ""
    ) -> str:
        """Rédige une réponse à un email de recrutement — tâche 'rediger'."""
        prompt = (
            "Tu rédiges une réponse professionnelle en français à un email de recrutement. "
            f"Profil candidat : {profil_candidat}. Contexte : {contexte}.\n"
            f"Email à traiter : {email_origine}\n"
            "Produis uniquement le corps du message, sans salutation générique inutile."
        )
        resp = await self.chat("rediger", [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Rédige la réponse."},
        ])
        return resp.text

    async def resumer_fil(self, emails: list[dict[str, str]]) -> str:
        """Résume un fil de conversation email — tâche 'resumer'."""
        texte = "\n\n".join(
            f"[{e.get('date','?')}] {e.get('expediteur','?')} : {e.get('sujet','')}\n{e.get('corps','')}"
            for e in emails
        )
        resp = await self.chat("resumer", [
            {"role": "system", "content": "Résume ce fil d'emails en 3 points clés en français."},
            {"role": "user", "content": texte[:4000]},
        ])
        return resp.text


# Instance par défaut (reconfigurable depuis le front)
agent_par_defaut = IAAgent()
