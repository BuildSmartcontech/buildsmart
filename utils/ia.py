# utils/ia.py - Conexión con IA (Ollama o API en la nube)

import requests
import json
import os
from utils.config import config

class IA:
    def __init__(self):
        self.url = config.OLLAMA_URL + "/api/generate"
        self.modelo = config.OLLAMA_MODEL
        
    def chat(self, mensaje, sistema="Eres un asistente útil y profesional."):
        """Enviar un mensaje a la IA y obtener respuesta"""
        try:
            prompt = f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:"
            
            data = {
                "model": self.modelo,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "num_predict": 2000
            }
            
            response = requests.post(self.url, json=data, timeout=120)
            
            if response.status_code == 200:
                resultado = response.json()
                return resultado.get('response', 'Error: No response')
            else:
                return f"❌ Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Error: Ollama no está corriendo. En producción, usa una API externa."
        except Exception as e:
            return f"❌ Error: {str(e)}"

ia = IA()