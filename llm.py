"""Small wrapper around the OpenAI Python library.

By default it talks to Google Gemini through Gemini's OpenAI-compatible
endpoint (free tier available). Because only the base URL, key and model
names change, the same code also works with OpenAI or any other
OpenAI-compatible provider.

Settings are read from Streamlit secrets (Streamlit Community Cloud) or
environment variables / a local .env file.
"""
import os
import time

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

load_dotenv()

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def setting(name, default=None):
    """Read a setting from Streamlit secrets first, then from the environment."""
    try:
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass  # no secrets file / not running inside Streamlit
    return os.getenv(name, default)


def api_key():
    return setting("GEMINI_API_KEY") or setting("OPENAI_API_KEY")


def make_client():
    key = api_key()
    if not key or key.startswith("your_"):
        raise RuntimeError(
            "No API key found. Add GEMINI_API_KEY to the app's secrets "
            "(Streamlit Cloud: App settings -> Secrets) or to a local .env file."
        )
    return OpenAI(api_key=key, base_url=setting("LLM_BASE_URL", GEMINI_BASE_URL), timeout=60, max_retries=2)


def chat_models():
    """Preferred chat model first, then fallbacks in case a model is retired or overloaded."""
    if "googleapis.com" in setting("LLM_BASE_URL", GEMINI_BASE_URL):
        preferred = setting("CHAT_MODEL", "gemini-flash-latest")
        fallbacks = ["gemini-flash-latest", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-flash-lite-latest"]
    else:  # OpenAI or another OpenAI-compatible provider
        preferred = setting("CHAT_MODEL", "gpt-5.4-mini")
        fallbacks = ["gpt-5.4-mini", "gpt-4.1-mini"]
    return [preferred] + [m for m in fallbacks if m != preferred]


RETRY_STATUS = {429, 500, 502, 503, 504}  # busy / temporarily unavailable


def chat(client, **kwargs):
    """chat.completions.create with retries and model fallback.

    - 404 (model name unknown): try the next model.
    - 429/5xx (overloaded, rate limit): wait briefly, retry, then try the next model.
    """
    last_error = None
    for model in chat_models():
        for attempt in range(2):
            try:
                return client.chat.completions.create(model=model, **kwargs)
            except APIStatusError as e:
                last_error = e
                if e.status_code == 404:
                    break  # next model
                if e.status_code in RETRY_STATUS:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise
            except (APIConnectionError, APITimeoutError) as e:
                last_error = e
                time.sleep(1.5 * (attempt + 1))
    raise last_error


def embed(client, model, texts):
    """embeddings.create with retries for temporary errors."""
    for attempt in range(4):
        try:
            return client.embeddings.create(model=model, input=texts)
        except APIStatusError as e:
            if e.status_code not in RETRY_STATUS or attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))
        except (APIConnectionError, APITimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def friendly_error(e):
    """Turn API errors into a short message for the UI."""
    if isinstance(e, APIStatusError):
        if e.status_code == 429:
            return "The free API limit was reached. Wait a minute and try again."
        if e.status_code in (500, 502, 503, 504):
            return "Google's AI service is busy right now (temporary). Please try again in a few seconds."
        if e.status_code in (401, 403):
            return "The API key was rejected. Check GEMINI_API_KEY in the app secrets."
        return f"The AI service returned an error ({e.status_code})."
    return str(e)
