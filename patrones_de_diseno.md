# Patrones de Diseño en Python

Este documento explica tres patrones de diseño aplicados a un cliente de chat que se conecta a APIs de LLMs (HuggingFace, OpenAI, Ollama).

---

## 1. Singleton

### ¿Qué es?

Garantiza que una clase tenga **una única instancia** en toda la aplicación. Cada vez que intentas crear un nuevo objeto, obtienes el mismo que ya existe.

### ¿Cuándo usarlo?

- Cuando solo necesitas una conexión a un servicio (como una API)
- Para evitar crear recursos duplicados (conexiones, clientes HTTP)
- Cuando múltiples partes de la aplicación deben compartir el mismo estado

### Conceptos clave de Python

#### Variables de clase vs variables de instancia

```python
class Ejemplo:
    compartida = "soy de clase"  # Variable de CLASE - compartida por todos

    def __init__(self):
        self.propia = "soy de instancia"  # Variable de INSTANCIA - única por objeto
```

#### `cls` y `self`

Ambos son **convenciones de nombre**, no palabras reservadas. Podrías usar cualquier nombre, pero la comunidad Python usa:

- `self` → Referencia a la **instancia** (el objeto creado)
- `cls` → Referencia a la **clase** (el molde)

```python
class Ejemplo:
    def metodo_instancia(self):  # self = el objeto
        pass

    @classmethod
    def metodo_clase(cls):  # cls = la clase
        pass

    def __new__(cls):  # cls porque el objeto aún no existe
        pass
```

#### `__new__` vs `__init__`

Cuando llamas a `MiClase()`, Python ejecuta internamente:

1. `__new__(cls)` → **Crea** el objeto en memoria (reserva espacio)
2. `__init__(self)` → **Inicializa** el objeto (asigna atributos)

```
MiClase()
    │
    ▼
┌─────────────────────────────────┐
│ __new__(cls)                    │  ← Crea objeto vacío en memoria
│   return objeto                 │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ __init__(self)                  │  ← self = lo que retornó __new__
│   self.atributo = valor         │
└─────────────────────────────────┘
    │
    ▼
  objeto listo
```

Normalmente no defines `__new__` porque `object.__new__` es suficiente. Solo lo sobrescribes cuando necesitas controlar **cómo** se crea el objeto.

#### `super().__new__(cls)`

- `super()` accede a la **clase padre** (en este caso `object`)
- `super().__new__(cls)` llama al método `__new__` de `object` para crear el objeto en memoria
- Le pasamos `cls` para indicar "crea una instancia de esta clase"

### Implementación

```python
class ChatClient:
    _instance = None  # Variable de clase que almacena la única instancia

    def __new__(cls, client=None):
        # __new__ se ejecuta ANTES que __init__
        if cls._instance is None:
            # Solo crea una instancia si no existe ninguna
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance  # Siempre retorna la misma instancia

    def __init__(self, client=None):
        # Evita reinicializar si ya fue inicializado
        if self._initialized:
            return

        self.client = client
        self._initialized = True
```

### Flujo de ejecución

```
Primera llamada: ChatClient()
┌─────────────────────────────────────┐
│ __new__(cls)                        │
│   _instance es None? → SÍ           │
│   super().__new__(cls) → crea obj   │
│   _instance = obj                   │
│   return obj                        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ __init__(self)                      │
│   _initialized es False? → SÍ      │
│   configura atributos               │
│   _initialized = True               │
└─────────────────────────────────────┘

Segunda llamada: ChatClient()
┌─────────────────────────────────────┐
│ __new__(cls)                        │
│   _instance es None? → NO           │
│   return _instance (el mismo)       │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ __init__(self)                      │
│   _initialized es True? → SÍ       │
│   return (no hace nada)             │
└─────────────────────────────────────┘
```

### Relación entre `self` y `cls._instance`

Cuando `__new__` retorna `cls._instance`, ese objeto se pasa a `__init__` como `self`. En ese momento, ambos apuntan al **mismo objeto en memoria**:

```
Memoria
───────────────────────────────────
       ┌─────────────────────┐
       │  Objeto ChatClient  │ ← Dirección: 0x7f8b8c0
       └─────────────────────┘
              ▲    ▲
              │    │
   cls._instance   self
   (en __new__)    (en __init__)
```

---

## 2. Dependency Injection (Inyección de Dependencias)

### ¿Qué es?

Las dependencias (objetos que una clase necesita para funcionar) se **pasan desde fuera** en lugar de crearlas internamente.

### ¿Cuándo usarlo?

- Para facilitar testing (puedes inyectar mocks)
- Cuando quieres desacoplar componentes
- Para poder cambiar implementaciones sin modificar la clase

### El problema sin DI

```python
class ChatClient:
    def __init__(self):
        # ChatClient CREA su dependencia internamente
        # Está acoplado a OpenAI - difícil de testear o cambiar
        self.client = OpenAI(api_key="...", base_url="...")
```

### Solución con DI

```python
class ChatClient:
    def __init__(self, client=None):
        # ChatClient RECIBE su dependencia desde fuera
        # Si no recibe nada, crea una por defecto (conveniente)
        self.client = client or self._create_default_client()
```

### Beneficio principal: Testing

```python
# En producción
chat = ChatClient()  # Usa cliente real

# En tests - inyectas un mock sin tocar la red
class MockClient:
    def chat_completions_create(self, ...):
        return respuesta_falsa

chat = ChatClient(client=MockClient())
```

### Visualización

```
ANTES (acoplamiento fuerte):
┌─────────────────────────────────┐
│ ChatClient                      │
│   └── crea OpenAI internamente  │ ← Difícil de testear
└─────────────────────────────────┘

DESPUÉS (Dependency Injection):
┌─────────────────────────────────┐
│ ChatClient                      │
│   └── recibe cliente desde fuera│ ← Fácil de testear/cambiar
└─────────────────────────────────┘
         ▲
         │
    Se inyecta
```

### Concepto clave

`ChatClient` se convierte en un **wrapper** (envoltorio) alrededor del cliente. Desacoplamos el constructor de la clase de la instanciación del cliente, permitiendo usar esta clase con distintos clientes: un mock para testing u otro proveedor en el futuro.

---

## 3. Factory

### ¿Qué es?

Centraliza la lógica de creación de objetos en un único lugar. En lugar de crear objetos directamente, llamas a la Factory y ella decide qué crear y cómo configurarlo.

### ¿Cuándo usarlo?

- Cuando tienes múltiples tipos de objetos similares (ej: diferentes proveedores)
- Cuando la creación de objetos es compleja o requiere configuración
- Para centralizar y organizar la lógica de construcción

### Implementación

```python
class ClientFactory:
    """Factory que crea clientes según el proveedor especificado."""

    @staticmethod
    def create(provider: str) -> OpenAI:
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
        return OpenAI(base_url=base_url, api_key=api_key)

    @staticmethod
    def _create_openai() -> OpenAI:
        api_key = os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key=api_key)

    @staticmethod
    def _create_ollama() -> OpenAI:
        base_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")
        return OpenAI(base_url=base_url, api_key="ollama")
```

### `@staticmethod`

Los métodos de la Factory son `@staticmethod` porque no necesitan acceso a `self` ni `cls`. Son funciones puras que reciben parámetros y retornan objetos.

### Flujo

```
                ClientFactory.create("provider")
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        "huggingface"      "openai"       "ollama"
              │               │               │
              ▼               ▼               ▼
    _create_huggingface  _create_openai  _create_ollama
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                      Cliente configurado
```

### Beneficios

1. **Extensibilidad**: Añadir un nuevo proveedor = añadir un método `_create_nuevo()` y un `elif`
2. **Centralización**: Toda la lógica de creación en un solo lugar
3. **Configuración aislada**: Cada proveedor maneja sus propias variables de entorno

---

## Combinando los tres patrones

### Arquitectura final

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
│                                                         │
│   ChatClient()  ← Singleton + Factory (huggingface)    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    ChatClient                           │
│                    (Singleton)                          │
│                                                         │
│  - Una única instancia en toda la app                   │
│  - Recibe cliente via DI (o crea default)               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   ClientFactory                         │
│                                                         │
│  - Centraliza creación de clientes                      │
│  - Soporta: huggingface, openai, ollama                 │
│  - Extensible para nuevos proveedores                   │
└─────────────────────────────────────────────────────────┘
```

### Cómo trabajan juntos

```python
# Factory crea el cliente
client = ClientFactory.create("openai")

# DI lo inyecta en ChatClient
chat = ChatClient(client=client)

# Singleton garantiza una única instancia
chat2 = ChatClient()  # Retorna el mismo objeto que chat
```

**Factory**: Decide *qué* cliente crear y *cómo* configurarlo.

**Dependency Injection**: Permite que `ChatClient` reciba *cualquier* cliente sin importar de dónde vino.

**Singleton**: Garantiza que solo exista una instancia de `ChatClient`, evitando conexiones duplicadas.

### Consideración importante

El Singleton limita a usar **un solo proveedor** durante toda la ejecución. Si necesitas múltiples proveedores simultáneos, deberías quitar el Singleton o implementar un "Singleton por proveedor":

```python
class ChatClient:
    _instances = {}  # Un dict en lugar de una sola instancia

    def __new__(cls, provider="huggingface"):
        if provider not in cls._instances:
            cls._instances[provider] = super().__new__(cls)
        return cls._instances[provider]
```

---

## Principio SOLID relacionado

Estos patrones implementan la **Inversión de Dependencias** (la "D" de SOLID):

> "Depende de abstracciones, no de implementaciones concretas."

`ChatClient` depende de "cualquier cliente con el método `chat.completions.create`", no de `OpenAI` específicamente. Esto permite:

- **Testing**: Inyectar mocks sin tocar la red
- **Flexibilidad**: Cambiar de proveedor sin modificar `ChatClient`
- **Desacoplamiento**: `ChatClient` no sabe ni le importa cómo se construye el cliente
