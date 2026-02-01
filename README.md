# Agente LLM

Wrapper unificado para interactuar con múltiples proveedores de LLM (Large Language Models) usando una interfaz común basada en OpenAI.

## Proveedores soportados

- **HuggingFace** - Modelos hospedados en HuggingFace Inference API
- **OpenAI** - API oficial de OpenAI
- **Ollama** - Modelos locales con Ollama

## Requisitos

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes recomendado)

## Instalacion

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd <carpeta-del-repositorio>

# Copiar el fichero de configuracion y editar con tus API keys
cp dummy.env .env

# Instalar dependencias con uv
uv sync
```

## Configuracion

Edita el archivo `.env` con tus API keys. Las variables disponibles son:

```env
# HuggingFace
HUGGING_FACE_API_KEY=tu_api_key
HUGGING_FACE_API_URL=https://api-inference.huggingface.co/v1

# OpenAI (opcional)
OPENAI_API_KEY=tu_api_key

# Ollama (opcional)
OLLAMA_API_URL=http://localhost:11434/v1

# Configuracion por defecto
DEFAULT_MODEL=moonshotai/Kimi-K2-Instruct
DEFAULT_PROVIDER=huggingface
```

## Uso

### Ejecutar el chatbot

```bash
uv run python main.py
```

## Estructura del proyecto

```text
.
├── main.py              # Punto de entrada del chatbot
├── src/
│   ├── core/            # Configuracion y utilidades
│   │   ├── config.py    # Variables de entorno
│   │   └── exceptions.py
│   ├── llm/             # Clientes de LLM
│   │   ├── client.py    # ChatClient singleton
│   │   └── factory.py   # Factory de proveedores
│   ├── api/             # API REST (en desarrollo)
│   ├── github/          # Integracion GitHub (en desarrollo)
│   └── reviewer/        # Code reviewer (en desarrollo)
├── tests/               # Tests unitarios
├── pyproject.toml       # Configuracion del proyecto
└── .env                 # Variables de entorno (no incluido en git)
```

## Dependencias

- `openai` - Cliente unificado para APIs compatibles con OpenAI
- `python-dotenv` - Carga de variables de entorno desde `.env`
