import os
from openai import OpenAI


class ClientFactory:
    """Factory que crea clientes según el proveedor especificado."""

    @staticmethod
    def create(provider: str) -> OpenAI:
        """
        Crea un cliente para el proveedor especificado.

        Args:
            provider: El nombre del proveedor ("huggingface", "openai", "ollama")

        Returns:
            Una instancia de cliente configurada para ese proveedor.
        """
        if provider == "huggingface":
            return ClientFactory._create_huggingface()
        elif provider == "openai":
            return ClientFactory._create_openai()
        elif provider == "ollama":
            return ClientFactory._create_ollama()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    @staticmethod
    def _create_huggingface() -> OpenAI:
        api_key = os.getenv("HUGGING_FACE_API_KEY")
        base_url = os.getenv("HUGGING_FACE_API_URL")

        if not api_key:
            raise ValueError("HUGGING_FACE_API_KEY environment variable is required.")
        if not base_url:
            raise ValueError("HUGGING_FACE_API_URL environment variable is required.")

        return OpenAI(base_url=base_url, api_key=api_key)

    @staticmethod
    def _create_openai() -> OpenAI:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required.")

        return OpenAI(api_key=api_key)

    @staticmethod
    def _create_ollama() -> OpenAI:
        base_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")

        return OpenAI(base_url=base_url, api_key="ollama")
