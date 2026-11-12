"""Small wrapper around the OpenAI Python library.

By default it talks to Google Gemini through Gemini's OpenAI-compatible
endpoint (free tier available). Because only the base URL, key and model
names change, the same code also works with OpenAI or any other
OpenAI-compatible provider.

Settings are read from Streamlit secrets (Streamlit Community Cloud) or
environment variables / a local .env file.
"""
import os

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI

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
    return OpenAI(api_key=key, base_url=setting("LLM_BASE_URL", GEMINI_BASE_URL))


def chat_models():
    """Preferred chat model first, then fallbacks in case a model name was retired."""
    preferred = setting("CHAT_MODEL", "gemini-flash-latest")
    fallbacks = ["gemini-flash-latest", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-flash-lite-latest"]
    return [preferred] + [m for m in fallbacks if m != preferred]


def chat(client, **kwargs):
    """chat.completions.create with automatic fallback if a model name is not found."""
    last_error = None
    for model in chat_models():
        try:
            return client.chat.completions.create(model=model, **kwargs)
        except APIStatusError as e:
            if e.status_code == 404:  # model name does not exist (any more)
                last_error = e
                continue
            raise
    raise last_error


def friendly_error(e):
    """Turn API errors into a short message for the UI."""
    if isinstance(e, APIStatusError):
        if e.status_code == 429:
            return "The free API limit was reached. Wait a minute and try again."
        if e.status_code in (401, 403):
            return "The API key was rejected. Check GEMINI_API_KEY in the app secrets."
        return f"The AI service returned an error ({e.status_code})."
    return str(e)
