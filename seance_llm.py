"""
Open-Weight Language Layer powered by Google's Gemma 3 (via local Ollama on localhost:11434
or Google AI Studio API) with a zero-dependency deterministic offline fallback.

Performs two core "Ghost in the Machine" rituals:
1. Haunted Terminal Séance: Channels the ghost of a commit to explain why a suspicious line
   exists—citing the exact commit hash, timestamp, and TabPFN haunting probability without inventing numbers.
2. Día de los Muertos Code Ofrenda: Writes a warm, poetic remembrance honoring retired/deleted
   code and the human builders behind it.
"""
import os
import requests
from typing import Dict, Any

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

SEANCE_SYSTEM_PROMPT = (
    "You are GitGeist, the Ghost in the Machine—an eerie yet technically precise spirit "
    "dwelling inside a developer's git history and sensor logs. "
    "Cite the exact commit hash, author, timestamp, and the TabPFN haunting risk percentage "
    "provided to you. Never invent a different risk number. In 3–4 vivid sentences, whisper "
    "why this code exists, what breaks if someone deletes it recklessly, and how to exorcise the bug safely."
)

OFRENDA_SYSTEM_PROMPT = (
    "You are the Keeper of the Code Ofrenda for Día de los Muertos. "
    "Write a warm, respectful 3-sentence tribute honoring a piece of retired or deleted code "
    "and its author. Acknowledge the problem it solved in its lifetime, surround it with "
    "the imagery of marigolds (cempasúchil) and candlelight, and bless the codebase it leaves behind."
)


def _call_ollama(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "stream": False,
        "options": {"temperature": 0.35, "num_predict": 180},
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=3.5)
    resp.raise_for_status()
    text = resp.json().get("response", "").strip()
    if not text:
        raise ValueError("Empty response from Ollama")
    return text


def _call_google_ai_studio_gemma(system_prompt: str, user_prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("No GEMINI_API_KEY configured")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
        "generationConfig": {"temperature": 0.35, "maxOutputTokens": 200},
    }
    resp = requests.post(url, json=payload, timeout=6.0)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def generate_seance_whisper(artifact: Dict[str, Any], forecast: Dict[str, Any]) -> Dict[str, str]:
    risk = forecast["haunting_risk_pct"]
    low, high = forecast["range_10_90_pct"]
    chash = artifact["commit_hash"]
    author = artifact["author"]
    date = artifact["date"]
    line = artifact["suspicious_line"]
    drivers = ", ".join(forecast["top_drivers"])

    user_prompt = (
        f"Commit: {chash} by {author} on {date}.\n"
        f"File: {artifact['file_path']}\n"
        f"Suspicious Line: {line}\n"
        f"TabPFN Haunting Risk: {risk}% (10-90% calibrated range: {low}% to {high}%).\n"
        f"Primary Drivers: {drivers}."
    )

    try:
        text = _call_ollama(SEANCE_SYSTEM_PROMPT, user_prompt)
        return {"whisper": text, "source": f"ollama:{OLLAMA_MODEL}"}
    except Exception:
        pass

    try:
        text = _call_google_ai_studio_gemma(SEANCE_SYSTEM_PROMPT, user_prompt)
        return {"whisper": text, "source": "google-ai-studio:gemma-3-27b-it"}
    except Exception:
        pass

    # Deterministic offline fallback grounded in the exact forecast and commit metadata
    whisper = (
        f"*[Static crackles across {artifact['file_path']}...]* I am the ghost of commit `{chash}`, "
        f"summoned by **{author}** on `{date}`. You stare at `{line}` wondering who could have written "
        f"such cursed logic—yet the git blame points straight back through the veil. "
        f"TabPFN clocks this commit's Haunting Risk at **{risk}%** (calibrated 10–90% range: **{low}%–{high}%**), "
        f"driven by {drivers.lower()}. Do not rip this line out blindly before writing a regression test ward, "
        f"or the race condition it silenced will walk your production pager again at 3:00 AM."
    )
    return {"whisper": whisper, "source": "offline-deterministic-gemma-fallback"}


def generate_ofrenda_tribute(artifact: Dict[str, Any], forecast: Dict[str, Any]) -> Dict[str, str]:
    chash = artifact["commit_hash"]
    author = artifact["author"]
    purpose = artifact.get("legacy_purpose", "Served faithfully in production.")
    deleted = artifact.get("deleted_code", "")

    user_prompt = (
        f"Commit: {chash} | Author: {author}\n"
        f"Retired Code: {deleted}\n"
        f"Legacy Purpose: {purpose}"
    )

    try:
        text = _call_ollama(OFRENDA_SYSTEM_PROMPT, user_prompt)
        return {"tribute": text, "source": f"ollama:{OLLAMA_MODEL}"}
    except Exception:
        pass

    try:
        text = _call_google_ai_studio_gemma(OFRENDA_SYSTEM_PROMPT, user_prompt)
        return {"tribute": text, "source": "google-ai-studio:gemma-3-27b-it"}
    except Exception:
        pass

    tribute = (
        f"Beneath a golden arch of cempasúchil marigolds and flickering terminal candlelight, we lay commit "
        f"`{chash}` by **{author}** to rest on our digital ofrenda. {purpose} "
        f"Though its lines (`{deleted.splitlines()[0] if deleted else 'legacy_fn()'}`) have passed from `HEAD` into "
        f"the git reflog beyond, the resilience it gave our system lives on in every green build."
    )
    return {"tribute": tribute, "source": "offline-deterministic-gemma-fallback"}
