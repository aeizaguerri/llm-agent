import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración centralizada de la aplicación."""

    # HuggingFace
    HUGGING_FACE_API_KEY: str = os.getenv("HUGGING_FACE_API_KEY", "")
    HUGGING_FACE_API_URL: str = os.getenv("HUGGING_FACE_API_URL", "")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Ollama
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")

    # GitHub
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

    # Modelo por defecto
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "openai/gpt-oss-120b:fastest")
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "huggingface")
