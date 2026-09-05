# utils/modelos.py - Lista de modelos chinos

MODELOS_CHINOS = {
    "ox_alpha": {
        "nombre": "Google Gemma 4 31B (Gratuito)",
        "proveedor": "Google",
        "identificador": "google/gemma-4-31b:free",
        "descripcion": "Modelo gratuito de Google. Multimodal y potente.",
        "contexto": "256K tokens",
        "gratuito": True
    },
    "qwen3_coder": {
        "nombre": "Google Gemma 4 31B",
        "proveedor": "Google",
        "identificador": "google/gemma-4-31b:free",
        "descripcion": "Multimodal. Buen equilibrio calidad/velocidad.",
        "contexto": "256K tokens",
        "gratuito": True
    },
    "gemma4": {
        "nombre": "Google Gemma 4 31B",
        "proveedor": "Google",
        "identificador": "google/gemma-4-31b:free",
        "descripcion": "Multimodal potente. Buen equilibrio calidad/velocidad.",
        "contexto": "256K tokens",
        "gratuito": True
    },
    "nemotron": {
        "nombre": "NVIDIA Nemotron Nano 12B V2 VL",
        "proveedor": "NVIDIA",
        "identificador": "nvidia/nemotron-nano-12b-v2-vl:free",
        "descripcion": "Optimizado para tareas visuales y lenguaje.",
        "contexto": "128K tokens",
        "gratuito": True
    },
    "ling3": {
        "nombre": "Ling-3.0-flash",
        "proveedor": "Ant Group",
        "identificador": "inclusionai/ling-3.0-flash:free",
        "descripcion": "Diseñado para agentes de IA. Contexto 256K.",
        "contexto": "256K tokens",
        "gratuito": True
    },
    "glm52": {
        "nombre": "GLM-5.2",
        "proveedor": "Zhipu AI",
        "identificador": "z-ai/glm-5.2:free",
        "descripcion": "Excelente en chino y tareas de agente.",
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