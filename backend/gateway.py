# backend/gateway.py - VERSIÓN 7.6 - OPTIMIZADO
# ============================================
# CORRECCIONES:
# - Backoff aumentado a 3s para Rate Limit (429)
# - 1 solo intento por modelo (más rápido)
# - Prioridad: OpenRouter → Groq → Gemini → Ollama
# - DeepSeek desactivado
# ============================================

import os
import requests
import time
from dotenv import load_dotenv
from typing import Tuple, Optional

load_dotenv()

# ============================================
# MODELOS VERIFICADOS
# ============================================

MODELOS_OPENROUTER = [
    "nvidia/nemotron-3-super-120b-a12b:free",  # ✅ 1M contexto
    "meta-llama/llama-3.2-3b-instruct:free",   # ✅ Rápido
]

MODELOS_GROQ = [
    "qwen/qwen3.6-27b",  # ✅ Principal
    "qwen/qwen3.8-27b",  # ✅ Alternativa
]

MODELOS_GEMINI = [
    "gemini-3.1-flash-lite",  # ✅ Multimodal
]

# ============================================
# 1. OPENROUTER - PRIORIDAD 1
# ============================================

def chat_openrouter(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con OpenRouter - Contexto largo, menos límites"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY no configurada")
    
    for modelo in MODELOS_OPENROUTER:
        try:
            print(f"   Intentando OpenRouter: {modelo}")
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": modelo,
                        "messages": [
                            {"role": "system", "content": sistema},
                            {"role": "user", "content": mensaje}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1500
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"   ✅ OpenRouter OK: {modelo}")
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    print(f"   ⏳ Rate Limit, esperando 3s...")
                    time.sleep(3)
                    continue
                else:
                    print(f"   ❌ OpenRouter error: {response.status_code}")
                    continue
        except Exception as e:
            print(f"   ❌ OpenRouter exception: {str(e)[:50]}...")
            continue
    
    raise Exception("Ningún modelo de OpenRouter disponible")

# ============================================
# 2. GROQ - PRIORIDAD 2
# ============================================

def chat_groq_directo(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Groq - Rápido pero con Rate Limit"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY no configurada")
    
    for modelo in MODELOS_GROQ:
        try:
            print(f"   Intentando Groq: {modelo}")
            with requests.Session() as session:
                response = session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": modelo,
                        "messages": [
                            {"role": "system", "content": sistema},
                            {"role": "user", "content": mensaje}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1500
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"   ✅ Groq OK: {modelo}")
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    print(f"   ⏳ Rate Limit (429), esperando 3s...")
                    time.sleep(3)
                    continue
                else:
                    print(f"   ❌ Groq error: {response.status_code}")
                    continue
        except Exception as e:
            print(f"   ❌ Groq exception: {str(e)[:50]}...")
            continue
    
    raise Exception("Ningún modelo de Groq disponible")

# ============================================
# 3. GEMINI - PRIORIDAD 3
# ============================================

def chat_gemini_directo(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Gemini - Multimodal"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY no configurada")
    
    for modelo in MODELOS_GEMINI:
        try:
            print(f"   Intentando Gemini: {modelo}")
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            prompt_completo = f"{sistema}\n\nUsuario: {mensaje}"
            
            payload = {
                'contents': [
                    {
                        'role': 'user',
                        'parts': [{'text': prompt_completo}]
                    }
                ],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 1500,
                    'topP': 0.95,
                    'topK': 40
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   ✅ Gemini OK: {modelo}")
                return text
            elif response.status_code == 503:
                print(f"   ⏳ Servicio ocupado (503), esperando 3s...")
                time.sleep(3)
                continue
            else:
                print(f"   ❌ Gemini error: {response.status_code}")
                continue
                
        except Exception as e:
            print(f"   ❌ Gemini exception: {str(e)[:50]}...")
            continue
    
    raise Exception("Ningún modelo de Gemini disponible")

# ============================================
# 4. OLLAMA - LOCAL (RESPALDO)
# ============================================

def chat_ollama(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Ollama - Local (último recurso)"""
    try:
        print("   Intentando Ollama (local)...")
        with requests.Session() as session:
            response = session.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:",
                    "stream": False,
                    "temperature": 0.7,
                    "max_tokens": 1500
                },
                timeout=120
            )
            
            if response.status_code == 200:
                print("   ✅ Ollama OK")
                return response.json().get('response', '')
            else:
                raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        raise Exception(f"Ollama exception: {str(e)}")

# ============================================
# 5. ENRUTADOR PRINCIPAL - NUEVO ORDEN
# ============================================

def chat_gateway(mensaje: str, sistema: str = "Eres un asistente útil.") -> Tuple[str, str]:
    """
    NUEVO ORDEN DE PRIORIDAD (OPTIMIZADO):
    1. OpenRouter (contexto largo, menos Rate Limit)
    2. Groq (rápido)
    3. Gemini (multimodal)
    4. Ollama (local)
    """
    
    # ============================================
    # PRIORIDAD 1: OPENROUTER
    # ============================================
    try:
        print("🔍 Probando: OpenRouter")
        respuesta = chat_openrouter(mensaje, sistema)
        return respuesta, "openrouter"
    except Exception as e:
        print(f"⚠️ OpenRouter: {str(e)[:50]}...")
    
    # ============================================
    # PRIORIDAD 2: GROQ
    # ============================================
    try:
        print("🔍 Probando: Groq")
        respuesta = chat_groq_directo(mensaje, sistema)
        return respuesta, "groq"
    except Exception as e:
        print(f"⚠️ Groq: {str(e)[:50]}...")
    
    # ============================================
    # PRIORIDAD 3: GEMINI
    # ============================================
    try:
        print("🔍 Probando: Gemini")
        respuesta = chat_gemini_directo(mensaje, sistema)
        return respuesta, "gemini"
    except Exception as e:
        print(f"⚠️ Gemini: {str(e)[:50]}...")
    
    # ============================================
    # PRIORIDAD 4: OLLAMA (LOCAL)
    # ============================================
    try:
        print("🔍 Probando: Ollama (local)")
        respuesta = chat_ollama(mensaje, sistema)
        return respuesta, "ollama"
    except Exception as e:
        print(f"⚠️ Ollama: {str(e)[:50]}...")
    
    return "⚠️ No hay modelos disponibles.", "ninguno"

# ============================================
# FUNCIONES ADICIONALES
# ============================================

def generar_imagen_gemini(prompt: str) -> str:
    """Genera una imagen usando Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ GEMINI_API_KEY no configurada"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-image:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 1.0,
            "candidateCount": 1
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            parts = data['candidates'][0]['content']['parts']
            for part in parts:
                if 'inlineData' in part:
                    import base64
                    image_data = part['inlineData']['data']
                    ruta = f"imagenes/gemini_{int(time.time())}.png"
                    os.makedirs("imagenes", exist_ok=True)
                    with open(ruta, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    return ruta
        return f"❌ Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generar_video_kling(prompt: str, duracion: int = 5, resolucion: str = "720p") -> dict:
    """Genera un video usando Kling AI"""
    api_key = os.getenv("KLING_API_KEY")
    if not api_key:
        return {"error": "KLING_API_KEY no configurada"}
    
    url = "https://api.klingai.com/v1/videos/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "kling-v3",
        "prompt": prompt,
        "duration": duracion,
        "resolution": resolucion
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "task_id": data.get("data", {}).get("task_id"),
                "status": data.get("data", {}).get("status"),
                "video_url": data.get("data", {}).get("video_url")
            }
        return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def consultar_video_kling(task_id: str) -> dict:
    """Consulta el estado de un video en Kling AI"""
    api_key = os.getenv("KLING_API_KEY")
    if not api_key:
        return {"error": "KLING_API_KEY no configurada"}
    
    url = f"https://api.klingai.com/v1/videos/generations/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "status": data.get("data", {}).get("status"),
                "video_url": data.get("data", {}).get("video_url")
            }
        return {"error": f"Error {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ============================================
# INSTANCIA GLOBAL
# ============================================

class Gateway:
    def __init__(self):
        self.chat = chat_gateway
        self.generar_imagen = generar_imagen_gemini
        self.generar_video = generar_video_kling
        self.consultar_video = consultar_video_kling
    
    def chat(self, mensaje: str, sistema: str = "Eres un asistente útil.") -> Tuple[str, str]:
        return chat_gateway(mensaje, sistema)

gateway = Gateway()

# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PROBANDO GATEWAY - VERSIÓN 7.6")
    print("=" * 60)
    print("\n✅ ORDEN DE PRIORIDAD:")
    print("   1. OpenRouter (contexto largo, menos límites)")
    print("   2. Groq (rápido)")
    print("   3. Gemini (multimodal)")
    print("   4. Ollama (local)")
    print("\n" + "=" * 60 + "\n")
    
    respuesta, fuente = chat_gateway("Hola, ¿cómo estás?")
    print(f"\n📌 Fuente final: {fuente}")
    print(f"💬 Respuesta: {respuesta[:200]}...")