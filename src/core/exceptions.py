class PRReviewerError(Exception):
    """Excepción base para el proyecto."""
    pass


class ProviderError(PRReviewerError):
    """Error relacionado con proveedores de LLM."""
    pass


class ConfigurationError(PRReviewerError):
    """Error de configuración (variables de entorno faltantes, etc.)."""
    pass


class GitHubError(PRReviewerError):
    """Error relacionado con la API de GitHub."""
    pass
