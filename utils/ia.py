# utils/ia.py - Conexión con IA (Ollama local o DeepSeek en nube)

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class IA:
    def __init__(self):
        # 🔑 CLAVE DIRECTA PARA LA NUBE (se usa si no encuentra variable de entorno)
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY', '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')
        self.entorno = os.getenv('ENTORNO', 'desarrollo')
        
    def chat(self, mensaje, sistema="Eres un asistente útil y profesional."):
        """Envía un mensaje y obtiene respuesta, usando la IA adecuada según el entorno."""
        
        # SIEMPRE usar DeepSeek si hay clave (en nube o local)
        if self.deepseek_key:
            return self._chat_deepseek(mensaje, sistema)
        else:
            # Si no hay clave, usar Ollama
            return self._chat_ollama(mensaje, sistema)
    
    def _chat_ollama(self, mensaje, sistema):
        """Usa Ollama en local."""
        try:
            prompt = f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:"
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get('response', '')
            return "⚠️ Ollama no está disponible en este entorno."
        except:
            return "⚠️ Error: Ollama no está corriendo o no es accesible."
    
    def _chat_deepseek(self, mensaje, sistema):
        """Usa DeepSeek API en la nube."""
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7
            }
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"⚠️ Error con DeepSeek: {response.status_code}"
        except Exception as e:
            return f"⚠️ Error de conexión con DeepSeek: {str(e)}"

ia = IA()