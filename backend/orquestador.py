# backend/orquestador.py - LangGraph Orquestador con Herramientas (Versión Optimizada)

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from backend.gateway import gateway
import time

# ========== ESTADO ==========
class Estado(TypedDict):
    mensaje: str
    plan: Optional[str]
    resultado: Optional[str]
    paso_actual: str
    historial: list

# ========== NODOS ==========
def nodo_brainstorm(estado: Estado) -> Estado:
    """Genera ideas a partir del mensaje - Nodo 1"""
    try:
        sistema = "Eres un experto en estrategia de negocios. Genera un plan de acción breve."
        prompt = f"Analiza esta solicitud y genera un plan paso a paso: {estado['mensaje']}"
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["plan"] = respuesta
        print(f"✅ Brainstorm completado")
    except Exception as e:
        estado["plan"] = f"⚠️ Error en brainstorm: {str(e)}"
    
    estado["paso_actual"] = "plan"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "brainstorm", "respuesta": estado["plan"]}]
    return estado

def nodo_plan(estado: Estado) -> Estado:
    """Crea un plan detallado - Nodo 2"""
    try:
        sistema = "Eres un planificador de proyectos. Convierte el plan en acciones concretas."
        prompt = f"Convierte este plan en acciones concretas: {estado['plan']}"
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["resultado"] = respuesta
        print(f"✅ Plan completado")
    except Exception as e:
        estado["resultado"] = f"⚠️ Error en plan: {str(e)}"
    
    estado["paso_actual"] = "work"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "plan", "respuesta": estado["resultado"]}]
    return estado

def nodo_work(estado: Estado) -> Estado:
    """Ejecuta el trabajo usando herramientas si es necesario - Nodo 3"""
    try:
        from backend.herramientas import herramientas
        from backend.gateway import gateway
        
        sistema = "Eres un ejecutor experto."
        
        # Detectar si necesita búsqueda
        mensaje = estado["mensaje"]
        if "buscar" in mensaje.lower() or "investigar" in mensaje.lower():
            # Usar DuckDuckGo
            busqueda = herramientas.buscar(mensaje)
            prompt = f"Con esta información:\n{busqueda}\n\nResponde a: {mensaje}"
        else:
            prompt = f"Entrega un resumen final del plan: {estado.get('resultado', mensaje)}"
        
        respuesta, fuente = gateway.chat(prompt, sistema)
        estado["resultado"] = respuesta
        print(f"✅ Work completado")
    except Exception as e:
        estado["resultado"] = f"⚠️ Error en work: {str(e)}"
    
    estado["paso_actual"] = "finish"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "work", "respuesta": estado["resultado"]}]
    return estado

# ========== CONSTRUIR GRAFICO ==========
def crear_orquestador():
    """Crea el grafo de LangGraph (versión simplificada)"""
    graph = StateGraph(Estado)
    
    # Agregar nodos
    graph.add_node("brainstorm", nodo_brainstorm)
    graph.add_node("plan", nodo_plan)
    graph.add_node("work", nodo_work)
    
    # Agregar conexiones
    graph.set_entry_point("brainstorm")
    graph.add_edge("brainstorm", "plan")
    graph.add_edge("plan", "work")
    graph.add_edge("work", END)
    
    return graph.compile()

# ========== EJECUTAR ==========
def ejecutar_orquestador(mensaje: str) -> dict:
    """Ejecuta el orquestador con un mensaje (versión rápida)"""
    try:
        orquestador = crear_orquestador()
        estado_inicial = {
            "mensaje": mensaje,
            "plan": None,
            "resultado": None,
            "paso_actual": "inicio",
            "historial": []
        }
        resultado = orquestador.invoke(estado_inicial)
        return {
            "mensaje": resultado["mensaje"],
            "plan": resultado.get("plan", ""),
            "resultado": resultado.get("resultado", ""),
            "paso_actual": resultado.get("paso_actual", "finish"),
            "historial": resultado.get("historial", [])
        }
    except Exception as e:
        # Si el orquestador falla, devolver un mensaje de error
        return {
            "mensaje": mensaje,
            "plan": "",
            "resultado": f"⚠️ Error en orquestador: {str(e)}",
            "paso_actual": "error",
            "historial": [{"nodo": "error", "respuesta": str(e)}]
        }