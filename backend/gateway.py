# backend/gateway.py - LiteLLM Gateway

import litellm
import os
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURACIÓN DE MODELOS ==========
# Prioridad 1: Local (Ollama)
litellm.set_verbose = False

def obtener_modelo_disponible():
    """
    Retorna el primer modelo disponible en orden de prioridad
    """
    modelos = [
        # Prioridad 1: Local
        {"nombre": "ollama/llama3.1:8b", "fuente": "local"},
        {"nombre": "ollama/qwen2.5:7b", "fuente": "local"},
        {"nombre": "ollama/mistral:7b", "fuente": "local"},
        
        # Prioridad 2: Nube gratuita
        {"nombre": "groq/llama-3.1-70b-versatile", "fuente": "groq"},
        {"nombre": "deepseek/deepseek-chat", "fuente": "deepseek"},
        {"nombre": "openrouter/google/gemma-2-27b-it:free", "fuente": "openrouter"},
    ]
    
    for modelo in modelos:
        try:
            # Verificar si el modelo está disponible
            if modelo["fuente"] == "local":
                # Verificar Ollama
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    modelos_local = [m["name"] for m in response.json().get("models", [])]
                    modelo_local = modelo["nombre"].replace("ollama/", "")
                    if any(modelo_local in m for m in modelos_local):
                        return modelo
            else:
                # Para modelos de nube, asumimos que están disponibles (fallarán después)
                return modelo
        except:
            continue
    
    return None

def chat_gateway(mensaje, sistema="Eres un asistente útil y profesional."):
    """
    Envía un mensaje al modelo disponible
    """
    modelo = obtener_modelo_disponible()
    if not modelo:
        return "⚠️ No hay modelos disponibles", "ninguno"
    
    try:
        response = litellm.completion(
            model=modelo["nombre"],
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content, modelo["fuente"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}", modelo["fuente"]

# ========== INSTANCIA GLOBAL ==========
class Gateway:
    def __init__(self):
        self.chat = chat_gateway
        self.obtener_modelo = obtener_modelo_disponible

gateway = Gateway()

if __name__ == "__main__":
    # Prueba
    respuesta, fuente = chat_gateway("Hola, ¿cómo estás?")
    print(f"Fuente: {fuente}")
    print(f"Respuesta: {respuesta}")