# utils/modelos.py - Lista de modelos chinos gratuitos (Verificados en OpenRouter)

MODELOS_CHINOS = {
    "gemma2_27b": {
        "nombre": "Google Gemma 2 27B",
        "proveedor": "Google",
        "identificador": "google/gemma-2-27b-it:free",
        "descripcion": "Modelo gratuito de Google. Buen equilibrio calidad/velocidad. Contexto 8K.",
        "contexto": "8K tokens",
        "gratuito": True
    },
    "llama3_2_3b": {
        "nombre": "Meta Llama 3.2 3B",
        "proveedor": "Meta",
        "identificador": "meta-llama/llama-3.2-3b-instruct:free",
        "descripcion": "Modelo gratuito de Meta. Rápido y eficiente. Contexto 128K.",
        "contexto": "128K tokens",
        "gratuito": True
    },
    "mistral_7b": {
        "nombre": "Mistral 7B",
        "proveedor": "Mistral AI",
        "identificador": "mistralai/mistral-7b-instruct:free",
        "descripcion": "Buen rendimiento general. Rápido y fiable. Contexto 8K.",
        "contexto": "8K tokens",
        "gratuito": True
    },
    "phi3_mini": {
        "nombre": "Microsoft Phi-3 Mini",
        "proveedor": "Microsoft",
        "identificador": "microsoft/phi-3-mini-128k-instruct:free",
        "descripcion": "Rápido y eficiente. Buen razonamiento. Contexto 128K.",
        "contexto": "128K tokens",
        "gratuito": True
    },
    "qwen2_5_72b": {
        "nombre": "Qwen 2.5 72B",
        "proveedor": "Alibaba",
        "identificador": "qwen/qwen-2.5-72b-instruct:free",
        "descripcion": "Modelo gratuito de Alibaba. Especializado en tareas generales.",
        "contexto": "128K tokens",
        "gratuito": True
    },
    "deepseek_v3": {
        "nombre": "DeepSeek V3",
        "proveedor": "DeepSeek",
        "identificador": "deepseek/deepseek-v3:free",
        "descripcion": "Modelo gratuito de DeepSeek. Buen rendimiento en razonamiento.",
        "contexto": "128K tokens",
        "gratuito": True
    }
}

def get_modelo(identificador):
    """Obtener la configuración de un modelo por su identificador"""
    for key, modelo in MODELOS_CHINOS.items():
        if modelo["identificador"] == identificador:
            return modelo
    return None

def listar_modelos():
    """Listar todos los modelos disponibles"""
    return MODELOS_CHINOS