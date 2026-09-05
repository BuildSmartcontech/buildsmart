# utils/ia.py - Conexión con IA (Ollama local o OpenRouter en nube)

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class IA:
    def __init__(self):
        # 🔑 Clave de OpenRouter (la que copiaste)
        self.api_key = "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"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        # Modelo gratuito de DeepSeek a través de OpenRouter
        self.modelo = "deepseek/deepseek-r1:free"
        
    def chat(self, mensaje, sistema="Eres un asistente útil y profesional."):
        """Envía un mensaje y obtiene respuesta usando OpenRouter."""
        
        if not self.api_key:
            return "⚠️ No hay API Key configurada."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.modelo,
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                resultado = response.json()
                return resultado['choices'][0]['message']['content']
            else:
                return f"⚠️ Error con OpenRouter: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"⚠️ Error de conexión: {str(e)}"

ia = IA()