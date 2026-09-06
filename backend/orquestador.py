# backend/orquestador.py - LangGraph Orquestador

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import httpx
import os

# ========== ESTADO ==========
class Estado(TypedDict):
    idea: str
    plan: Optional[str]
    trabajo: Optional[str]
    revision: Optional[str]
    final: Optional[str]
    paso_actual: str

# ========== NODOS ==========
def nodo_brainstorm(estado: Estado) -> Estado:
    """Genera ideas a partir de la idea inicial"""
    # Aquí iría la lógica de IA para hacer brainstorming
    estado["plan"] = f"Plan generado para: {estado['idea']}"
    estado["paso_actual"] = "plan"
    return estado

def nodo_plan(estado: Estado) -> Estado:
    """Crea un plan detallado"""
    estado["trabajo"] = f"Trabajo planificado basado en: {estado['plan']}"
    estado["paso_actual"] = "work"
    return estado

def nodo_work(estado: Estado) -> Estado:
    """Ejecuta el trabajo"""
    estado["revision"] = f"Revisión del trabajo: {estado['trabajo']}"
    estado["paso_actual"] = "review"
    return estado

def nodo_review(estado: Estado) -> Estado:
    """Revisa el trabajo"""
    estado["final"] = f"Resultado final: {estado['revision']}"
    estado["paso_actual"] = "compound"
    return estado

def nodo_compound(estado: Estado) -> Estado:
    """Consolida el resultado"""
    estado["paso_actual"] = "finish"
    return estado

# ========== CONSTRUIR GRÁFICO ==========
def crear_orquestador():
    """Crea el grafo de LangGraph"""
    graph = StateGraph(Estado)
    
    # Agregar nodos
    graph.add_node("brainstorm", nodo_brainstorm)
    graph.add_node("plan", nodo_plan)
    graph.add_node("work", nodo_work)
    graph.add_node("review", nodo_review)
    graph.add_node("compound", nodo_compound)
    
    # Agregar conexiones
    graph.set_entry_point("brainstorm")
    graph.add_edge("brainstorm", "plan")
    graph.add_edge("plan", "work")
    graph.add_edge("work", "review")
    graph.add_edge("review", "compound")
    graph.add_edge("compound", END)
    
    return graph.compile()

# ========== EJECUTAR ==========
def ejecutar_orquestador(idea: str) -> dict:
    """Ejecuta el orquestador con una idea"""
    orquestador = crear_orquestador()
    estado_inicial = {
        "idea": idea,
        "plan": None,
        "trabajo": None,
        "revision": None,
        "final": None,
        "paso_actual": "inicio"
    }
    resultado = orquestador.invoke(estado_inicial)
    return {
        "idea": resultado["idea"],
        "plan": resultado["plan"],
        "trabajo": resultado["trabajo"],
        "revision": resultado["revision"],
        "final": resultado["final"]
    }

if __name__ == "__main__":
    # Prueba
    resultado = ejecutar_orquestador("Crear un negocio de construcción")
    print(resultado)