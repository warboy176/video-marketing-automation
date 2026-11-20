"""Thin client for an OpenAI-compatible chat endpoint.

Defaults to a local Ollama server (http://localhost:11434/v1) so the whole
project runs with no API key and no cost. Point it anywhere else with
FORGE_ENDPOINT / FORGE_MODEL / FORGE_API_KEY. Uses only the standard library
so no `openai` package is required.
"""
import json
import urllib.error
import urllib.request

from config import FORGE_ENDPOINT, FORGE_MODEL, FORGE_API_KEY


def call_forge(messages, timeout=8):
    """Call the chat/completions endpoint. Returns the reply text, or None
    if the endpoint is unreachable or returns something unexpected."""
    url = FORGE_ENDPOINT.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {"model": FORGE_MODEL, "messages": messages, "temperature": 0.7}
    ).encode()
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FORGE_API_KEY}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError, OSError):
        return None
