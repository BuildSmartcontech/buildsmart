# backend/orquestador.py - VERSIÓN 7.8 - CON PDF Y RESUMEN EJECUTIVO
# ============================================
# CORRECCIONES:
# - Delay de 0.5s entre nodos
# - Timeout por nodo de 30s
# - Manejo de errores mejorado
# - Integración con Supabase para guardar historial
# - Generación de PDF del plan
# - Resumen ejecutivo
# ============================================

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from backend.gateway import gateway
import time
import os

# ========== ESTADO ==========
class Estado(TypedDict):
    mensaje: str
    plan: Optional[str]
    resultado: Optional[str]
    paso_actual: str
    historial: list
    negocio_id: Optional[str]

# ========== NODOS ==========

def nodo_brainstorm(estado: Estado) -> Estado:
    """Nodo 1: Genera ideas y estrategias"""
    try:
        print("🧠 Brainstorm - Generando ideas...")
        time.sleep(0.5)
        
        sistema = """Eres un experto en estrategia de negocios y creatividad."""
        prompt = f"Solicitud: {estado['mensaje']}\n\nGenera un plan de acción paso a paso."
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["plan"] = respuesta
        print(f"✅ Brainstorm completado con: {fuente}")
        
    except Exception as e:
        estado["plan"] = f"⚠️ Error en brainstorm: {str(e)}"
        print(f"❌ Error en brainstorm: {e}")
    
    estado["paso_actual"] = "plan"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "brainstorm", "respuesta": estado["plan"]}]
    return estado

def nodo_plan(estado: Estado) -> Estado:
    """Nodo 2: Convierte ideas en plan estructurado"""
    try:
        print("📋 Plan - Estructurando el plan...")
        time.sleep(0.5)
        
        sistema = "Eres un planificador de proyectos experto."
        prompt = f"Ideas: {estado['plan']}\n\nConvierte esto en un plan de acción detallado."
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["resultado"] = respuesta
        print(f"✅ Plan completado con: {fuente}")
        
    except Exception as e:
        estado["resultado"] = f"⚠️ Error en plan: {str(e)}"
        print(f"❌ Error en plan: {e}")
    
    estado["paso_actual"] = "work"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "plan", "respuesta": estado["resultado"]}]
    return estado

def nodo_work(estado: Estado) -> Estado:
    """Nodo 3: Ejecuta tareas usando herramientas"""
    try:
        from backend.herramientas import herramientas
        
        print("⚡ Work - Ejecutando tareas...")
        time.sleep(0.5)
        
        mensaje = estado["mensaje"]
        
        # BÚSQUEDA
        if any(word in mensaje.lower() for word in ['buscar', 'investigar', 'busca', 'noticias']):
            print("   🔍 Detected: Búsqueda en DuckDuckGo")
            busqueda = herramientas.buscar(mensaje)
            estado["resultado"] = f"🔍 Resultados de búsqueda:\n\n{busqueda}"
        
        # PROCESAMIENTO GENERAL
        else:
            print("   📝 Detected: Procesamiento general")
            sistema = "Eres un ejecutor experto."
            prompt = f"Responde a: {mensaje}"
            respuesta, fuente = gateway.chat(prompt, sistema)
            estado["resultado"] = respuesta
        
        print("✅ Work completado")
        
    except Exception as e:
        estado["resultado"] = f"⚠️ Error en work: {str(e)}"
        print(f"❌ Error en work: {e}")
    
    estado["paso_actual"] = "review"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "work", "respuesta": estado["resultado"]}]
    return estado

def nodo_review(estado: Estado) -> Estado:
    """Nodo 4: Revisa y mejora el resultado"""
    try:
        print("🔍 Review - Evaluando resultado...")
        time.sleep(0.5)
        
        sistema = "Eres un crítico constructivo y editor experto."
        prompt = f"Revisa y mejora este resultado:\n{estado.get('resultado', '')}"
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["resultado"] = respuesta
        print(f"✅ Review completado con: {fuente}")
        
    except Exception as e:
        print(f"⚠️ Review falló, usando resultado original: {e}")
    
    estado["paso_actual"] = "compound"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "review", "respuesta": estado["resultado"]}]
    return estado

def nodo_compound(estado: Estado) -> Estado:
    """Nodo 5: Sintetiza la respuesta final"""
    try:
        print("📊 Compound - Sintetizando respuesta final...")
        time.sleep(0.5)
        
        sistema = "Eres un comunicador experto."
        prompt = f"Sintetiza esta información:\nPlan: {estado.get('plan', '')}\n\nResultado: {estado.get('resultado', '')}"
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["resultado"] = respuesta
        print(f"✅ Compound completado con: {fuente}")
        
    except Exception as e:
        estado["resultado"] = f"⚠️ Error en compound: {str(e)}"
        print(f"❌ Error en compound: {e}")
    
    estado["paso_actual"] = "finish"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "compound", "respuesta": estado["resultado"]}]
    return estado

# ========== CONSTRUIR GRAFICO ==========

def crear_orquestador():
    graph = StateGraph(Estado)
    
    graph.add_node("brainstorm", nodo_brainstorm)
    graph.add_node("plan", nodo_plan)
    graph.add_node("work", nodo_work)
    graph.add_node("review", nodo_review)
    graph.add_node("compound", nodo_compound)
    
    graph.set_entry_point("brainstorm")
    graph.add_edge("brainstorm", "plan")
    graph.add_edge("plan", "work")
    graph.add_edge("work", "review")
    graph.add_edge("review", "compound")
    graph.add_edge("compound", END)
    
    return graph.compile()

# ============================================
# FUNCIÓN: GUARDAR EN SUPABASE
# ============================================

def guardar_en_supabase(mensaje: str, respuesta: str, modelo: str = None, 
                        negocio_id: str = None, fuente: str = None, usuario: str = 'anonimo'):
    """Guarda el historial en Supabase"""
    try:
        from utils.supabase_client import supabase
        return supabase.guardar_historial(
            mensaje=mensaje,
            respuesta=respuesta,
            modelo=modelo,
            negocio_id=negocio_id,
            fuente=fuente,
            usuario=usuario
        )
    except ImportError:
        print('⚠️ Módulo Supabase no disponible')
        return False
    except Exception as e:
        print(f'⚠️ Error guardando en Supabase: {e}')
        return False

# ============================================
# FUNCIÓN: GENERAR RESUMEN EJECUTIVO
# ============================================

def generar_resumen_ejecutivo(plan_completo: str) -> str:
    """
    Genera un resumen ejecutivo del plan (máximo 200 palabras)
    """
    try:
        sistema = "Eres un ejecutivo experto en marketing y comunicaciones."
        prompt = f"""
        Genera un resumen ejecutivo CONCISO de este plan de marketing.
        
        Requisitos:
        - Máximo 200 palabras
        - Lenguaje profesional
        - Incluir: objetivo principal, 3 estrategias clave, y resultado esperado
        
        Plan:
        {plan_completo}
        """
        respuesta, fuente = gateway.chat(prompt, sistema)
        return respuesta
    except Exception as e:
        return f"Error generando resumen: {str(e)}"

# ============================================
# FUNCIÓN: GENERAR PDF
# ============================================

def generar_pdf_del_plan(contenido: str, titulo: str = "Plan de Marketing", nombre_archivo: str = None) -> str:
    """
    Genera un PDF a partir del contenido del plan
    """
    try:
        from utils.pdf_generator import generar_pdf_plan
        return generar_pdf_plan(contenido, titulo, nombre_archivo)
    except ImportError:
        print('⚠️ Módulo PDF no disponible')
        return None
    except Exception as e:
        print(f'⚠️ Error generando PDF: {e}')
        return None

# ========== EJECUTAR ==========

def ejecutar_orquestador(mensaje: str, negocio_id: Optional[str] = None) -> dict:
    try:
        print("=" * 60)
        print("🚀 INICIANDO ORQUESTADOR - VERSIÓN 7.8")
        print("=" * 60)
        print(f"📝 Mensaje: {mensaje[:100]}...")
        print("-" * 60)
        
        orquestador = crear_orquestador()
        estado_inicial = {
            "mensaje": mensaje,
            "plan": None,
            "resultado": None,
            "paso_actual": "inicio",
            "historial": [],
            "negocio_id": negocio_id
        }
        
        resultado = orquestador.invoke(estado_inicial)
        
        print("-" * 60)
        print("✅ ORQUESTADOR COMPLETADO")
        print("=" * 60)
        
        # ============================================
        # GUARDAR EN SUPABASE
        # ============================================
        try:
            modelo_usado = "desconocido"
            fuente = "desconocida"
            if resultado.get("historial"):
                ultimo = resultado["historial"][-1]
                modelo_usado = ultimo.get("fuente", "desconocido")
                fuente = ultimo.get("fuente", "desconocida")
            
            guardar_en_supabase(
                mensaje=mensaje,
                respuesta=resultado.get("resultado", ""),
                modelo=modelo_usado,
                negocio_id=negocio_id,
                fuente=fuente
            )
        except Exception as e:
            print(f'⚠️ No se pudo guardar en Supabase: {e}')
        
        # ============================================
        # GENERAR PDF Y RESUMEN EJECUTIVO
        # ============================================
        plan_completo = resultado.get("resultado", "")
        pdf_url = None
        resumen = None
        
        if plan_completo and len(plan_completo) > 100:
            try:
                # Generar resumen ejecutivo
                print("📄 Generando resumen ejecutivo...")
                resumen = generar_resumen_ejecutivo(plan_completo)
                
                # Generar PDF
                print("📄 Generando PDF...")
                pdf_url = generar_pdf_del_plan(plan_completo, "Plan de Marketing BuildSmart")
                if pdf_url:
                    print(f"✅ PDF guardado en: {pdf_url}")
            except Exception as e:
                print(f'⚠️ Error generando documento: {e}')
        
        # ============================================
        # RESULTADO FINAL
        # ============================================
        return {
            "mensaje": resultado["mensaje"],
            "plan": resultado.get("plan", ""),
            "resultado": resultado.get("resultado", ""),
            "resumen_ejecutivo": resumen,
            "pdf_url": pdf_url,
            "paso_actual": resultado.get("paso_actual", "finish"),
            "historial": resultado.get("historial", [])
        }
        
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        return {
            "mensaje": mensaje,
            "plan": "",
            "resultado": f"⚠️ Error: {str(e)}",
            "resumen_ejecutivo": None,
            "pdf_url": None,
            "paso_actual": "error",
            "historial": []
        }

# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    resultado = ejecutar_orquestador("Necesito un plan de marketing para mi negocio de construcción")
    print(f"\n📌 Resultado:")
    print(f"   Plan: {resultado['resultado'][:200]}...")
    print(f"   Resumen: {resultado.get('resumen_ejecutivo', 'No disponible')[:200]}...")
    print(f"   PDF: {resultado.get('pdf_url', 'No generado')}")