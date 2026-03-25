"""Config adapter: maps Streamlit UI provider selections to (model_id, base_url, api_key).

Does NOT read environment variables or mutate global state.
"""

# Default model - using Cerebras provider which supports structured outputs and is FREE (1M tokens/day)
DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct:cerebras"

# Models that support structured outputs (Pydantic schema)
# Cerebras and OpenAI support it; HuggingFace standard and Ollama don't
SUPPORTS_STRUCTURED_OUTPUT = {
    "openai": True,  # All OpenAI models
    "cerebras": True,  # Cerebras supports structured outputs via HF router
    "huggingface": False,  # Standard HF doesn't support it
    "ollama": False,  # Ollama doesn't support it well
}

PROVIDERS: dict[str, dict[str, str]] = {
    "cerebras": {
        "base_url": "https://router.huggingface.co/v1",
        "key_label": "HuggingFace API Key",
        "default_model": "meta-llama/Llama-3.1-8B-Instruct:cerebras",
        "description": "FREE - 1M tokens/day, very fast",
    },
    "huggingface": {
        "base_url": "https://router.huggingface.co/v1",
        "key_label": "HuggingFace API Key",
        "default_model": "moonshotai/Kimi-K2-Instruct",
        "description": "Uses standard HF inference (no structured outputs)",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_label": "OpenAI API Key",
        "default_model": "gpt-4o-mini",
        "description": "Paid - requires OpenAI API key",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_label": "Not required",
        "default_model": "llama3",
        "description": "Local - requires Ollama running",
    },
}


def build_provider_config(
    provider: str,
    model: str,
    api_key: str,
    base_url_override: str = "",
) -> tuple[str, str, str]:
    """Build (model_id, base_url, api_key) from UI form inputs.

    Args:
        provider: One of "huggingface", "openai", "ollama".
        model: Model ID string. If empty, falls back to provider default.
        api_key: API key string. For ollama, always replaced with "ollama".
        base_url_override: Custom base URL (used for ollama custom endpoint).

    Returns:
        Tuple of (model_id, base_url, api_key) matching Config.get_model_config() shape.

    Raises:
        ValueError: If the provider is not in PROVIDERS.
    """
    provider = provider.lower()
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unknown provider: '{provider}'. Must be one of {list(PROVIDERS)}"
        )

    provider_info = PROVIDERS[provider]
    model_id = (
        model.strip() if model and model.strip() else provider_info["default_model"]
    )
    base_url = (
        base_url_override.strip()
        if base_url_override and base_url_override.strip()
        else provider_info["base_url"]
    )

    # Ollama never needs a real API key
    if provider == "ollama":
        resolved_key = "ollama"
    else:
        resolved_key = api_key

    return model_id, base_url, resolved_key


def provider_supports_structured_output(provider: str) -> bool:
    """Check if the given provider supports structured outputs."""
    return SUPPORTS_STRUCTURED_OUTPUT.get(provider.lower(), False)
