# backend/orquestador.py - LangGraph Orquestador con Herramientas

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from backend.gateway import gateway

# ========== ESTADO ==========
class Estado(TypedDict):
    mensaje: str
    plan: Optional[str]
    resultado: Optional[str]
    paso_actual: str
    historial: list

# ========== NODOS ==========
def nodo_brainstorm(estado: Estado) -> Estado:
    """Genera ideas a partir del mensaje"""
    sistema = "Eres un experto en estrategia de negocios. Genera un plan de acción."
    prompt = f"Analiza esta solicitud: {estado['mensaje']}. Genera un plan paso a paso."
    
    respuesta, fuente = gateway.chat(prompt, sistema)
    estado["plan"] = respuesta
    estado["paso_actual"] = "plan"
    estado["historial"].append({"nodo": "brainstorm", "respuesta": respuesta})
    return estado

def nodo_plan(estado: Estado) -> Estado:
    """Crea un plan detallado"""
    sistema = "Eres un planificador de proyectos."
    prompt = f"Convierte este plan en acciones concretas: {estado['plan']}"
    
    respuesta, fuente = gateway.chat(prompt, sistema)
    estado["resultado"] = respuesta
    estado["paso_actual"] = "work"
    estado["historial"].append({"nodo": "plan", "respuesta": respuesta})
    return estado

def nodo_work(estado: Estado) -> Estado:
    """Ejecuta el trabajo usando herramientas si es necesario"""
    from backend.herramientas import herramientas
    from backend.gateway import gateway
    
    sistema = "Eres un ejecutor experto. Usa herramientas disponibles si son necesarias."
    
    # Detectar si necesita búsqueda
    mensaje = estado["mensaje"]
    if "buscar" in mensaje.lower() or "investigar" in mensaje.lower():
        # Usar DuckDuckGo
        busqueda = herramientas.buscar(mensaje)
        prompt = f"Con esta información:\n{busqueda}\n\nResponde a: {mensaje}"
    else:
        prompt = f"Ejecuta este plan y entrega resultados: {estado.get('resultado', mensaje)}"
    
    respuesta, fuente = gateway.chat(prompt, sistema)
    estado["resultado"] = respuesta
    estado["paso_actual"] = "review"
    estado["historial"].append({"nodo": "work", "respuesta": respuesta})
    return estado

def nodo_review(estado: Estado) -> Estado:
    """Revisa el trabajo"""
    sistema = "Eres un revisor crítico."
    prompt = f"Revisa este resultado y sugiere mejoras: {estado['resultado']}"
    
    respuesta, fuente = gateway.chat(prompt, sistema)
    estado["resultado"] = respuesta
    estado["paso_actual"] = "compound"
    estado["historial"].append({"nodo": "review", "respuesta": respuesta})
    return estado

def nodo_compound(estado: Estado) -> Estado:
    """Consolida el resultado final"""
    sistema = "Eres un presentador ejecutivo."
    prompt = f"Resume el trabajo final en un mensaje claro y conciso: {estado['resultado']}"
    
    respuesta, fuente = gateway.chat(prompt, sistema)
    estado["resultado"] = respuesta
    estado["paso_actual"] = "finish"
    estado["historial"].append({"nodo": "compound", "respuesta": respuesta})
    return estado

# ========== CONSTRUIR GRAFICO ==========
def crear_orquestador():
    """Crea el grafo de LangGraph"""
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

# ========== EJECUTAR ==========
def ejecutar_orquestador(mensaje: str) -> dict:
    """Ejecuta el orquestador con un mensaje"""
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
        "plan": resultado["plan"],
        "resultado": resultado["resultado"],
        "paso_actual": resultado["paso_actual"],
        "historial": resultado["historial"]
    }