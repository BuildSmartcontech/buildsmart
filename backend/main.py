# backend/main.py - FastAPI Backend para BuildSmart con Orquestador LangGraph

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="BuildSmart API", version="1.0")

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
    fuente: str  # "local" o "nube"

# ========== RUTAS ==========
@app.get("/")
async def root():
    return {"mensaje": "BuildSmart API", "version": "1.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal con orquestador LangGraph"""
    try:
        # ========== INTENTAR USAR ORQUESTADOR ==========
        from backend.orquestador import ejecutar_orquestador
        resultado = ejecutar_orquestador(request.mensaje)
        
        # Si el orquestador devuelve un resultado
        if resultado and resultado.get("resultado"):
            return ChatResponse(
                respuesta=resultado["resultado"],
                modelo_usado="langgraph",
                fuente="local"
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
        # Fallback final: usar funciones directas
        print(f"⚠️ Error en orquestador: {e}")
        try:
            # 1. Intentar usar Ollama (local)
            try:
                resultado = await chat_ollama(request.mensaje, request.sistema)
                return ChatResponse(
                    respuesta=resultado,
                    modelo_usado="ollama",
                    fuente="local"
                )
            except:
                pass
            
            # 2. Fallback: DeepSeek (nube)
            try:
                resultado = await chat_deepseek(request.mensaje, request.sistema)
                return ChatResponse(
                    respuesta=resultado,
                    modelo_usado="deepseek",
                    fuente="nube"
                )
            except:
                pass
            
            # 3. Fallback: OpenRouter (nube)
            try:
                resultado = await chat_openrouter(request.mensaje, request.sistema)
                return ChatResponse(
                    respuesta=resultado,
                    modelo_usado="openrouter",
                    fuente="nube"
                )
            except Exception as e3:
                raise HTTPException(status_code=503, detail=f"No hay IA disponible: {str(e3)}")
        except Exception as e4:
            raise HTTPException(status_code=503, detail=f"Error general: {str(e4)}")

# ========== FUNCIONES DE CHAT (FALLBACK) ==========
async def chat_ollama(mensaje: str, sistema: str) -> str:
    """Chat con Ollama local"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:",
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        raise Exception(f"Ollama error: {response.status_code}")

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
                "model": "google/gemma-2-27b-it:free",
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
    uvicorn.run(app, host="0.0.0.0", port=8000)