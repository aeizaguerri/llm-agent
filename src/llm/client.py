from src.llm.factory import ClientFactory


class ChatClient:
    """Cliente de chat singleton con inyección de dependencias."""

    _instance = None

    def __new__(cls, client=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, client=None):
        if self._initialized:
            return

        self.client = client or ClientFactory.create("huggingface")
        self._initialized = True

    def get_response(self, model, messages, temperature=0.7, max_tokens=150):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message
