# backend/herramientas.py - Herramientas gratuitas

from duckduckgo_search import DDGS
import edge_tts

# ========== BÚSQUEDA ==========
def buscar(query: str, max_results: int = 5) -> list:
    """Buscar en DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        return [{"error": str(e)}]

# ========== TTS ==========
async def texto_a_voz(texto: str, archivo_salida: str = "output.mp3"):
    """Convertir texto a voz usando Edge-TTS"""
    try:
        communicate = edge_tts.Communicate(texto, "es-ES-ElviraNeural")
        await communicate.save(archivo_salida)
        return archivo_salida
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Prueba de búsqueda
    resultados = buscar("IA en construcción")
    print(resultados)