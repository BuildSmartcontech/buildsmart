# backend/main.py - FastAPI Backend para BuildSmart con Orquestador LangGraph
# ============================================
# VERSIÓN 7.8 - OPTIMIZADO PARA HUGGING FACE SPACES
# ============================================

import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
from dotenv import load_dotenv

# ========== AGREGAR RUTA DEL PROYECTO AL PATH ==========
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

app = FastAPI(title="BuildSmart API", version="7.8")

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODELOS ==========
class ChatRequest(BaseModel):
    mensaje: str
    sistema: Optional[str] = "Eres un asistente útil y profesional."
    negocio_id: Optional[str] = None
    modelo: Optional[str] = None

class ChatResponse(BaseModel):
    respuesta: str
    modelo_usado: str
    fuente: str
    pdf_url: Optional[str] = None
    resumen_ejecutivo: Optional[str] = None

# ========== RUTAS ==========
@app.get("/")
async def root():
    return {
        "mensaje": "BuildSmart API",
        "version": "7.8",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal con orquestador LangGraph"""
    try:
        # ========== USAR ORQUESTADOR ==========
        from backend.orquestador import ejecutar_orquestador
        
        resultado = ejecutar_orquestador(request.mensaje, request.negocio_id)
        
        # Verificar si el orquestador devolvió un resultado
        if resultado and resultado.get("resultado"):
            return ChatResponse(
                respuesta=resultado["resultado"],
                modelo_usado="openrouter",
                fuente="nube",
                pdf_url=resultado.get("pdf_url"),
                resumen_ejecutivo=resultado.get("resumen_ejecutivo")
            )
        else:
            # Fallback: usar el gateway directamente
            from backend.gateway import gateway
            respuesta, fuente = gateway.chat(request.mensaje, request.sistema)
            return ChatResponse(
                respuesta=respuesta,
                modelo_usado=fuente,
                fuente=fuente
            )
            
    except ImportError as e:
        # Si no está disponible el orquestador, usar el gateway directamente
        print(f"⚠️ Orquestador no disponible: {e}")
        try:
            from backend.gateway import gateway
            respuesta, fuente = gateway.chat(request.mensaje, request.sistema)
            return ChatResponse(
                respuesta=respuesta,
                modelo_usado=fuente,
                fuente=fuente
            )
        except Exception as e2:
            raise HTTPException(status_code=503, detail=f"Error en gateway: {str(e2)}")
            
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== FUNCIONES DE CHAT (FALLBACK) ==========
async def chat_ollama(mensaje: str, sistema: str) -> str:
    """Chat con Ollama local"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:",
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get('response', '')
            raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        raise Exception(f"Ollama falló: {str(e)}")

async def chat_deepseek(mensaje: str, sistema: str) -> str:
    """Chat con DeepSeek API"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise Exception("DeepSeek API Key no configurada")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        raise Exception(f"DeepSeek error: {response.status_code}")

async def chat_openrouter(mensaje: str, sistema: str) -> str:
    """Chat con OpenRouter API"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise Exception("OpenRouter API Key no configurada")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nvidia/nemotron-3-super-120b-a12b:free",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        raise Exception(f"OpenRouter error: {response.status_code}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)