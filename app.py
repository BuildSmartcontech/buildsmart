# app.py - BuildSmart Operations Center
# VERSIÓN COMPLETA CON IA (Ollama) + Web Generator + Email + Social + Automation + Research

import streamlit as st
import datetime
import pandas as pd
import random
import json
import os
import re
from datetime import timedelta

# ========== IMPORTAR MÓDULOS ==========
# Primero importar modelos para que estén disponibles
try:
    from utils.modelos import MODELOS_CHINOS
    MODELOS_DISPONIBLE = True
except ImportError:
    MODELOS_DISPONIBLE = False
    MODELOS_CHINOS = {}

# Luego importar IA
try:
    from utils.ia import ia
    IA_DISPONIBLE = True
except ImportError as e:
    IA_DISPONIBLE = False
    ia = None
    print(f"⚠️ Error al importar ia: {e}")

try:
    from utils.web_generator import web_generator
    WEB_DISPONIBLE = True
except ImportError:
    WEB_DISPONIBLE = False
    web_generator = None

try:
    from utils.email_sender import email_sender
    EMAIL_DISPONIBLE = True
except ImportError:
    EMAIL_DISPONIBLE = False
    email_sender = None

try:
    from utils.social_poster import social_poster
    SOCIAL_DISPONIBLE = True
except ImportError:
    SOCIAL_DISPONIBLE = False
    social_poster = None

try:
    from utils.automation import scheduler, tarea_nocturna, tarea_diaria, tarea_semanal
    AUTOMATION_DISPONIBLE = True
except ImportError:
    AUTOMATION_DISPONIBLE = False
    scheduler = None

try:
    from utils.market_research import market_research
    RESEARCH_DISPONIBLE = True
except ImportError:
    RESEARCH_DISPONIBLE = False
    market_research = None

# ========== CONFIGURACIÓN ==========
st.set_page_config(
    page_title="BuildSmart Operations",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS PERSONALIZADO ==========
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a1a2e, #16213e, #0f3460);
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #0f3460;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .business-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
        cursor: pointer;
    }
    .business-card:hover {
        border-color: #0f3460;
        box-shadow: 0 4px 12px rgba(15,52,96,0.2);
    }
    .business-card.selected {
        border-color: #0f3460;
        background: #f0f4ff;
    }
    .status-active {
        color: #00a65a;
        font-weight: bold;
    }
    .task-card {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
        transition: all 0.2s;
    }
    .task-card:hover {
        border-color: #0f3460;
        box-shadow: 0 2px 8px rgba(15,52,96,0.1);
    }
    .task-card.todo {
        border-left: 4px solid #f39c12;
    }
    .task-card.done {
        border-left: 4px solid #2ecc71;
        opacity: 0.7;
    }
    .task-card.in-progress {
        border-left: 4px solid #3498db;
    }
    .agent-badge {
        background: #0f3460;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
    }
    .credit-badge {
        background: #f39c12;
        color: white;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .footer {
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        color: #888;
        font-size: 0.8rem;
        text-align: center;
    }
    .chat-message-user {
        background: #0f3460;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-message-agent {
        background: #e8ecf1;
        color: #1a1a2e;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-message-processing {
        background: #fff3cd;
        color: #856404;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #ffc107;
    }
    .timeline-item {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.9rem;
    }
    .section-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #0f3460;
        margin-bottom: 0.5rem;
    }
    .status-badge {
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .status-badge.activo {
        background: #d4edda;
        color: #155724;
    }
    .status-badge.inactivo {
        background: #f8d7da;
        color: #721c24;
    }
    .status-badge.en-pausa {
        background: #fff3cd;
        color: #856404;
    }
    .social-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    .social-card:hover {
        border-color: #0f3460;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .processing-text {
        animation: pulse 1.5s ease-in-out infinite;
    }
    .feature-badge {
        background: #28a745;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.6rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 5px;
    }
    .feature-badge.off {
        background: #dc3545;
    }
    .modelo-actual {
        background: #e8f4fd;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #0f3460;
        border: 1px solid #0f3460;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "negocio_seleccionado" not in st.session_state:
    st.session_state.negocio_seleccionado = None

if "chat_historial" not in st.session_state:
    st.session_state.chat_historial = [
        {"role": "agent", "agente": "Orquestador", "content": "👋 ¡Bienvenido a BuildSmart Holdings! Soy tu asistente. Puedes crear nuevos negocios, gestionar tareas y mucho más. (IA: Ollama)"},
    ]

if "scheduler_activo" not in st.session_state:
    st.session_state.scheduler_activo = False

if "modelo_actual" not in st.session_state:
    st.session_state.modelo_actual = "ox_alpha"

# ========== DATOS DE NEGOCIOS CON TODAS LAS SECCIONES ==========
if "negocios" not in st.session_state:
    st.session_state.negocios = {
        "buildsmart": {
            "id": "buildsmart",
            "nombre": "BuildSmart",
            "icono": "🏗️",
            "descripcion": "Mi negocio de construcción",
            "metricas": {"Proyectos": 0, "Clientes": 0, "Ingresos": "$0", "Prospectos": 0},
            "creditos": 12,
            "sitio_web": {
                "url": "https://buildsmart-digest.polsia.io",
                "visitantes": 8,
                "ingresos": "$0.00",
                "actualizado": "HACE 1 HORA",
                "archivo_generado": None
            },
            "rutinas": {
                "turno_nocturno": True,
                "diario": True,
                "semanal": False
            },
            "equipos": [
                {"nombre": "Antonio", "rol": "Fundador", "email": "antonio@buildsmart.com"}
            ],
            "agentes": [
                {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
                {"nombre": "Marketing", "estado": "Activo", "rol": "Contenido y SEO"},
                {"nombre": "Ventas", "estado": "Activo", "rol": "Prospección y Cierre"},
                {"nombre": "Investigación", "estado": "Activo", "rol": "Análisis de Mercado"}
            ],
            "tareas": [
                {"id": 1, "titulo": "Definir misión y visión del negocio", "categoria": "ESTRATEGIA", "estado": "TODO", "creditos": 1, "tiempo": "HACE 2H"},
                {"id": 2, "titulo": "Crear landing page del sitio web", "categoria": "DISEÑO", "estado": "EN_PROGRESO", "creditos": 2, "tiempo": "HACE 1H"},
                {"id": 3, "titulo": "Configurar redes sociales", "categoria": "MARKETING", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"}
            ],
            "documentos": [
                {"nombre": "Brief de investigación: Priorización de lectores", "estado": "Completado", "fecha": "2026-09-03"},
                {"nombre": "Comparación de medios de comunicación ConTech", "estado": "En progreso", "fecha": "2026-09-02"},
                {"nombre": "BuildSmart Digest - Media Kit", "estado": "Pendiente", "fecha": "2026-09-01"}
            ],
            "redes_sociales": {
                "twitter": {"conectado": True, "usuario": "@BuildSmartCo", "ultimo_tweet": "8:25 AM - 3 DE SEPTIEMBRE 2026"},
                "instagram": {"conectado": True, "usuario": "@buildsmart", "ultimo_post": "HACE 36 MINUTOS"},
                "linkedin": {"conectado": False, "usuario": ""}
            },
            "anuncios": {
                "activo": False,
                "presupuesto_diario": "$0",
                "experimentos": [
                    {"nombre": "A/B Test Landing", "estado": "Activo", "conversion": "0.5%"}
                ]
            },
            "correo": {
                "email": "buildsmart-digest@polsia.app",
                "enviados": 1,
                "recibidos": 0,
                "ultimo": "¡Bienvenido a BuildSmart!"
            },
            "timeline": [
                {"accion": "Negocio creado", "fecha": "2026-09-03 10:00", "tipo": "info"},
                {"accion": "Agentes configurados", "fecha": "2026-09-03 10:05", "tipo": "info"},
                {"accion": "Tarea 'Definir misión' creada", "fecha": "2026-09-03 10:10", "tipo": "tarea"}
            ],
            "color": "#0f3460"
        },
        "contech": {
            "id": "contech",
            "nombre": "ConTech Digest",
            "icono": "📰",
            "descripcion": "Newsletter de tecnología en construcción",
            "metricas": {"Proyectos": 0, "Clientes": 0, "Ingresos": "$0", "Prospectos": 0},
            "creditos": 10,
            "sitio_web": {
                "url": "https://contech-digest.polsia.io",
                "visitantes": 3,
                "ingresos": "$0.00",
                "actualizado": "HACE 2 HORAS",
                "archivo_generado": None
            },
            "rutinas": {
                "turno_nocturno": True,
                "diario": True,
                "semanal": True
            },
            "equipos": [
                {"nombre": "Antonio", "rol": "Fundador", "email": "antonio@contech.com"}
            ],
            "agentes": [
                {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
                {"nombre": "Contenido", "estado": "Activo", "rol": "Redacción y Edición"},
                {"nombre": "Redes Sociales", "estado": "Activo", "rol": "Gestión de Redes"}
            ],
            "tareas": [
                {"id": 1, "titulo": "Definir tema de la primera edición", "categoria": "CONTENIDO", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"},
                {"id": 2, "titulo": "Crear plantilla de newsletter", "categoria": "DISEÑO", "estado": "TODO", "creditos": 2, "tiempo": "PENDIENTE"}
            ],
            "documentos": [
                {"nombre": "Plan editorial ConTech", "estado": "Completado", "fecha": "2026-09-02"},
                {"nombre": "Análisis de competencia newsletters", "estado": "Completado", "fecha": "2026-09-01"}
            ],
            "redes_sociales": {
                "twitter": {"conectado": False, "usuario": "", "ultimo_tweet": ""},
                "instagram": {"conectado": False, "usuario": "", "ultimo_post": ""},
                "linkedin": {"conectado": False, "usuario": ""}
            },
            "anuncios": {
                "activo": False,
                "presupuesto_diario": "$0",
                "experimentos": []
            },
            "correo": {
                "email": "contech-digest@polsia.app",
                "enviados": 0,
                "recibidos": 0,
                "ultimo": ""
            },
            "timeline": [
                {"accion": "Negocio creado", "fecha": "2026-09-02 15:00", "tipo": "info"},
                {"accion": "Plan editorial completado", "fecha": "2026-09-02 16:30", "tipo": "info"}
            ],
            "color": "#e74c3c"
        }
    }

# ========== FUNCIONES DE NEGOCIOS ==========

def crear_negocio(nombre, icono, descripcion):
    import re
    id_generado = re.sub(r'[^a-zA-Z0-9]', '_', nombre.lower())
    id_generado = id_generado + "_" + str(len(st.session_state.negocios) + 1)
    
    colores = ["#2ecc71", "#f39c12", "#9b59b6", "#1abc9c", "#e67e22", "#3498db", "#e74c3c", "#2c3e50"]
    color_idx = len(st.session_state.negocios) % len(colores)
    
    nuevo_negocio = {
        "id": id_generado,
        "nombre": nombre,
        "icono": icono,
        "descripcion": descripcion,
        "metricas": {"Proyectos": 0, "Clientes": 0, "Ingresos": "$0", "Prospectos": 0},
        "creditos": 10,
        "sitio_web": {
            "url": f"https://{nombre.lower().replace(' ', '-')}.polsia.io",
            "visitantes": 0,
            "ingresos": "$0.00",
            "actualizado": "AHORA",
            "archivo_generado": None
        },
        "rutinas": {
            "turno_nocturno": True,
            "diario": True,
            "semanal": False
        },
        "equipos": [
            {"nombre": "Fundador", "rol": "Propietario", "email": "fundador@empresa.com"}
        ],
        "agentes": [
            {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
            {"nombre": "Marketing", "estado": "Activo", "rol": "Contenido y SEO"},
            {"nombre": "Ventas", "estado": "Activo", "rol": "Prospección y Cierre"}
        ],
        "tareas": [
            {"id": 1, "titulo": "Definir la misión y visión", "categoria": "ESTRATEGIA", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"},
            {"id": 2, "titulo": "Crear la página web", "categoria": "DISEÑO", "estado": "TODO", "creditos": 2, "tiempo": "PENDIENTE"},
            {"id": 3, "titulo": "Conseguir los primeros clientes", "categoria": "VENTAS", "estado": "TODO", "creditos": 2, "tiempo": "PENDIENTE"}
        ],
        "documentos": [],
        "redes_sociales": {
            "twitter": {"conectado": False, "usuario": "", "ultimo_tweet": ""},
            "instagram": {"conectado": False, "usuario": "", "ultimo_post": ""},
            "linkedin": {"conectado": False, "usuario": ""}
        },
        "anuncios": {
            "activo": False,
            "presupuesto_diario": "$0",
            "experimentos": []
        },
        "correo": {
            "email": f"{nombre.lower().replace(' ', '-')}@polsia.app",
            "enviados": 0,
            "recibidos": 0,
            "ultimo": ""
        },
        "timeline": [
            {"accion": f"Negocio '{nombre}' creado", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"}
        ],
        "color": colores[color_idx]
    }
    
    st.session_state.negocios[id_generado] = nuevo_negocio
    
    mensaje_confirmacion = f"✅ ¡Excelente! He creado el negocio **{nombre}** {icono}. Tienes 10 créditos disponibles para comenzar. ¿Qué te gustaría hacer primero?"
    st.session_state.chat_historial.append({
        "role": "agent",
        "agente": "Orquestador",
        "content": mensaje_confirmacion
    })
    
    st.session_state.negocio_seleccionado = id_generado
    return id_generado

def mover_tarea(negocio_id, tarea_id, nuevo_estado):
    negocio = st.session_state.negocios.get(negocio_id)
    if negocio:
        for tarea in negocio["tareas"]:
            if tarea["id"] == tarea_id:
                tarea["estado"] = nuevo_estado
                tarea["tiempo"] = f"HACE {random.randint(1, 60)} MIN"
                negocio["timeline"].append({
                    "accion": f"Tarea '{tarea['titulo'][:30]}...' movida a {nuevo_estado}",
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "tipo": "tarea"
                })
                if nuevo_estado == "HECHO":
                    negocio["creditos"] = negocio.get("creditos", 10) + 1
                return True
    return False

# ========== FUNCIONES DE NUEVAS CARACTERÍSTICAS ==========

def generar_sitio_web(negocio_id):
    """Generar sitio web para un negocio"""
    if not WEB_DISPONIBLE:
        return False, "❌ Módulo web no disponible. Crea utils/web_generator.py"
    
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio:
        return False, "❌ Negocio no encontrado"
    
    try:
        ruta = web_generator.generar_landing_page(
            negocio_id,
            negocio['nombre'],
            negocio['descripcion'],
            negocio['icono']
        )
        negocio['sitio_web']['archivo_generado'] = ruta
        negocio['sitio_web']['url'] = ruta
        negocio['timeline'].append({
            "accion": f"🌐 Sitio web generado: {ruta}",
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": "info"
        })
        return True, f"✅ Sitio web generado en: {ruta}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def enviar_correo_negocio(negocio_id, destino, asunto, contenido):
    """Enviar correo desde un negocio"""
    if not EMAIL_DISPONIBLE:
        return "❌ Módulo email no disponible. Crea utils/email_sender.py"
    
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio:
        return "❌ Negocio no encontrado"
    
    try:
        resultado = email_sender.enviar_correo(destino, asunto, contenido)
        negocio['correo']['enviados'] += 1
        negocio['correo']['ultimo'] = asunto
        negocio['timeline'].append({
            "accion": f"📧 Correo enviado: {asunto}",
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": "info"
        })
        return resultado
    except Exception as e:
        return f"❌ Error: {str(e)}"

def publicar_en_twitter(negocio_id, mensaje):
    """Publicar en Twitter"""
    if not SOCIAL_DISPONIBLE:
        return "❌ Módulo social no disponible. Crea utils/social_poster.py"
    
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio:
        return "❌ Negocio no encontrado"
    
    try:
        resultado = social_poster.publicar_twitter(mensaje)
        if "✅" in resultado:
            negocio['redes_sociales']['twitter']['ultimo_tweet'] = datetime.datetime.now().strftime("%H:%M - %d DE %B %Y")
            negocio['timeline'].append({
                "accion": f"🐦 Tweet publicado",
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "tipo": "info"
            })
        return resultado
    except Exception as e:
        return f"❌ Error: {str(e)}"

def iniciar_automatizacion():
    """Iniciar el scheduler de automatización"""
    if not AUTOMATION_DISPONIBLE:
        return "❌ Módulo de automatización no disponible. Crea utils/automation.py"
    
    if st.session_state.scheduler_activo:
        return "⏹️ La automatización ya está activa"
    
    try:
        scheduler.agregar_tarea("Turno Nocturno", tarea_nocturna, 60)
        scheduler.agregar_tarea("Tarea Diaria", tarea_diaria, 360)
        scheduler.agregar_tarea("Tarea Semanal", tarea_semanal, 10080)
        resultado = scheduler.iniciar()
        st.session_state.scheduler_activo = True
        return resultado
    except Exception as e:
        return f"❌ Error: {str(e)}"

def detener_automatizacion():
    """Detener el scheduler"""
    if not AUTOMATION_DISPONIBLE:
        return "❌ Módulo de automatización no disponible"
    
    try:
        resultado = scheduler.detener()
        st.session_state.scheduler_activo = False
        return resultado
    except Exception as e:
        return f"❌ Error: {str(e)}"

def investigar_mercado(tema):
    """Realizar investigación de mercado"""
    if not RESEARCH_DISPONIBLE:
        return "❌ Módulo de investigación no disponible. Crea utils/market_research.py"
    
    try:
        return market_research.investigar(tema)
    except Exception as e:
        return f"❌ Error: {str(e)}"

def obtener_nombre_modelo():
    """Obtener el nombre legible del modelo actual"""
    if MODELOS_DISPONIBLE and st.session_state.modelo_actual in MODELOS_CHINOS:
        return MODELOS_CHINOS[st.session_state.modelo_actual]["nombre"]
    return st.session_state.modelo_actual

# ========== FUNCIÓN DE CHAT CON CORREO INTEGRADO ==========

def responder_chat(mensaje):
    """Responde usando IA real (Ollama o modelo chino)"""
    
    mensaje_lower = mensaje.lower()
    
    # ========== COMANDO: CAMBIAR MODELO ==========
    if "cambiar modelo" in mensaje_lower or "modelo" in mensaje_lower:
        if not MODELOS_DISPONIBLE:
            return "❌ Módulo de modelos no disponible. Crea utils/modelos.py", "Sistema"
        
        # Verificar si el usuario especificó un modelo
        for key in MODELOS_CHINOS.keys():
            if key in mensaje_lower:
                # Verificar que ia esté disponible
                if not IA_DISPONIBLE or ia is None:
                    return "❌ El módulo de IA no está disponible. Verifica utils/ia.py", "Sistema"
                try:
                    resultado = ia.cambiar_modelo(key)
                    st.session_state.modelo_actual = key
                    return resultado, "Sistema"
                except Exception as e:
                    return f"❌ Error al cambiar modelo: {str(e)}", "Sistema"
        
        # Si no especificó, mostrar los modelos disponibles
        lista = "\n".join([f"  • `{key}`: {m['nombre']} - {m['descripcion'][:50]}..." for key, m in MODELOS_CHINOS.items()])
        actual = obtener_nombre_modelo()
        return f"""
📚 **Modelos Chinos Disponibles:**

{lista}

**Modelo actual:** {actual}

Para cambiar, escribe: `cambiar modelo ox_alpha` (reemplaza con el nombre del modelo)
""", "Sistema"
    
    # ========== COMANDO: MODELO ACTUAL ==========
    if "modelo actual" in mensaje_lower or "que modelo" in mensaje_lower:
        actual = obtener_nombre_modelo()
        return f"🧠 **Modelo actual:** {actual}", "Sistema"
    
    # ========== COMANDO: ENVIAR CORREO DESDE EL CHAT ==========
    if "enviar correo" in mensaje_lower or "mandar correo" in mensaje_lower:
        
        # Buscar destinatario (usando el mensaje original para preservar tildes y ñ)
        email_match = re.search(r'a\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', mensaje)
        asunto_match = re.search(r'asunto[:\s]+([^\n]+?)(?=contenido:|cuerpo:|$)', mensaje, re.IGNORECASE)
        contenido_match = re.search(r'(?:contenido:|cuerpo:)\s*(.+?)(?=$)', mensaje, re.IGNORECASE | re.DOTALL)
        
        if not email_match:
            return """
📧 **Formato para enviar correo desde el chat:**

`enviar correo a correo@ejemplo.com asunto: Tu asunto contenido: El mensaje`

**Ejemplo:**
`enviar correo a antonioempresarial9@gmail.com asunto: Hola contenido: Este es un mensaje de prueba`
""", "Sistema"
        
        destino = email_match.group(1)
        asunto = asunto_match.group(1).strip() if asunto_match else "Mensaje desde BuildSmart"
        contenido = contenido_match.group(1).strip() if contenido_match else "Este es un correo enviado desde BuildSmart Holdings."
        
        if not EMAIL_DISPONIBLE:
            return "❌ El sistema de correo no está disponible. Configura EMAIL_USER y EMAIL_PASSWORD en .env", "Sistema"
        
        try:
            # Forzar que el contenido sea string UTF-8
            contenido = str(contenido).encode('utf-8').decode('utf-8')
            asunto = str(asunto).encode('utf-8').decode('utf-8')
            
            resultado = email_sender.enviar_correo(destino, asunto, contenido)
            
            if "✅" in resultado and st.session_state.negocio_seleccionado:
                negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
                negocio['correo']['enviados'] += 1
                negocio['correo']['ultimo'] = asunto
                negocio['timeline'].append({
                    "accion": f"📧 Correo enviado desde chat a {destino}: {asunto}",
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "tipo": "info"
                })
            
            return f"{resultado}\n\n📨 **Detalles:**\n- Para: {destino}\n- Asunto: {asunto}", "Correo"
            
        except Exception as e:
            return f"❌ Error al enviar correo: {str(e)}", "Sistema"

    # ========== COMANDO: VER CORREOS ENVIADOS ==========
    if "correos enviados" in mensaje_lower or "cuantos correos" in mensaje_lower:
        if st.session_state.negocio_seleccionado:
            negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
            enviados = negocio['correo']['enviados']
            ultimo = negocio['correo']['ultimo']
            return f"📊 Has enviado {enviados} correo(s). Último: {ultimo if ultimo else 'Ninguno'}", "Correo"
        else:
            return "📊 Selecciona un negocio primero para ver sus correos.", "Correo"

    # ========== COMANDOS RÁPIDOS ==========
    if "credito" in mensaje_lower or "crédito" in mensaje_lower:
        if st.session_state.negocio_seleccionado:
            negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
            creditos = negocio.get("creditos", 0)
            return f"💳 En {negocio['nombre']} tienes {creditos} créditos disponibles.", "Finanzas"
        else:
            return "💳 Selecciona un negocio primero para ver tus créditos.", "Finanzas"
    
    if "tarea" in mensaje_lower and "pendiente" in mensaje_lower:
        if st.session_state.negocio_seleccionado:
            negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
            pendientes = [t for t in negocio["tareas"] if t["estado"] != "HECHO"]
            if pendientes:
                lista = "\n".join([f"  • {t['titulo']} ({t['estado']})" for t in pendientes])
                return f"📋 Tareas pendientes:\n{lista}", "Operaciones"
            else:
                return "✅ No hay tareas pendientes.", "Operaciones"
        else:
            return "📋 Selecciona un negocio primero para ver sus tareas.", "Operaciones"
    
    if "ayuda" in mensaje_lower or "help" in mensaje_lower:
        return """
📚 **COMANDOS DISPONIBLES:**

**🧠 Modelos:**
• `modelo` - Ver modelos disponibles
• `cambiar modelo ox_alpha` - Cambiar a Ox Alpha
• `modelo actual` - Ver modelo en uso

**📧 Correo:**
• `enviar correo a correo@ejemplo.com asunto: ... contenido: ...` - Enviar correo
• `correos enviados` - Ver cuántos correos has enviado

**📋 Negocios y Tareas:**
• `¿Cuántos agentes tengo?` - Ver agentes
• `¿Qué tareas tengo?` - Ver tareas pendientes
• `¿Cuántos créditos tengo?` - Ver saldo
• `¿Qué negocios tengo?` - Ver todos los negocios

**🌐 Acciones:**
• `Generar sitio web` - Crear landing page
• `Investigar mercado` - Realizar investigación
""", "Orquestador"
    
    # ========== COMANDOS DE ACCIONES ==========
    if "generar sitio" in mensaje_lower or "crear web" in mensaje_lower or "landing" in mensaje_lower:
        if st.session_state.negocio_seleccionado:
            resultado, msg = generar_sitio_web(st.session_state.negocio_seleccionado)
            return msg, "Web Generator" if resultado else "Sistema"
        else:
            return "🌐 Selecciona un negocio primero para generar su sitio web.", "Sistema"
    
    if "investigar" in mensaje_lower or "investigación" in mensaje_lower:
        return "🔍 Para investigar un tema, usa la sección 'Investigación de Mercado' en el dashboard.", "Sistema"
    
    # ========== IA REAL ==========
    if IA_DISPONIBLE and ia is not None:
        try:
            contexto = ""
            if st.session_state.negocio_seleccionado:
                negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
                contexto = f"El usuario está hablando sobre el negocio '{negocio['nombre']}' que tiene {negocio['metricas']['Proyectos']} proyectos y {negocio['metricas']['Clientes']} clientes."
            
            sistema = f"""
            Eres el asistente virtual de BuildSmart Holdings, una plataforma de creación y gestión de negocios.
            
            {contexto}
            
            Funcionalidades disponibles:
            - Crear negocios
            - Gestionar tareas con Kanban
            - Sistema de créditos
            - Generar páginas web automáticas
            - Enviar correos
            - Publicar en redes sociales
            - Automatización 24/7
            - Investigación de mercado
            
            Reglas:
            1. Sé breve y directo (máximo 3 párrafos)
            2. Da respuestas útiles y prácticas
            3. Si no sabes algo, dilo honestamente
            4. Ofrece sugerencias cuando sea apropiado
            5. Responde en el mismo idioma que el usuario
            
            El usuario pregunta:
            """
            
            respuesta = ia.chat(mensaje, sistema)
            # Mostrar el modelo actual en la respuesta
            modelo_nombre = obtener_nombre_modelo()
            return f"{respuesta}\n\n---\n🧠 *Usando: {modelo_nombre}*", f"Asistente IA ({modelo_nombre})"
            
        except Exception as e:
            return f"❌ Error con la IA: {str(e)}\n\n💡 Prueba con 'ayuda' para comandos básicos.", "Sistema"
    else:
        respuestas = [
            "📝 No entendí tu pregunta. Prueba: '¿Cuántos créditos tengo?', '¿Qué tareas tengo?', o 'ayuda'.",
            "🤔 ¿Puedes ser más específico?",
            "💡 Escribe 'ayuda' para ver todos los comandos disponibles."
        ]
        return random.choice(respuestas), "Asistente"

# ========== ENCABEZADO ==========
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0;">🏗️ BuildSmart Holdings</h1>
            <p style="margin: 0; opacity: 0.8;">
                Panel de Control Multi-Negocio 
                {'🤖 (IA Activada)' if IA_DISPONIBLE else ''}
                {'🌐' if WEB_DISPONIBLE else ''}
                {'📧' if EMAIL_DISPONIBLE else ''}
                {'🐦' if SOCIAL_DISPONIBLE else ''}
                {'⚡' if AUTOMATION_DISPONIBLE else ''}
                {'🔍' if RESEARCH_DISPONIBLE else ''}
            </p>
        </div>
        <div>
            <span class="status-active">✅ SISTEMA ACTIVO</span>
            <span style="margin-left: 1rem;">🔄 {datetime.datetime.now().strftime("%H:%M")}</span>
            <span style="margin-left: 1rem;" class="modelo-actual">🧠 {obtener_nombre_modelo()}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== BARRA LATERAL ==========
with st.sidebar:
    st.markdown("### 🏗️ BuildSmart")
    st.divider()
    
    st.success("✅ Sistema Operativo")
    st.caption(f"🔄 {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Estado de módulos
    st.markdown("**🧩 Módulos:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"🧠 IA: {'✅' if IA_DISPONIBLE else '❌'}")
        st.markdown(f"🌐 Web: {'✅' if WEB_DISPONIBLE else '❌'}")
        st.markdown(f"📧 Email: {'✅' if EMAIL_DISPONIBLE else '❌'}")
    with col2:
        st.markdown(f"🐦 Social: {'✅' if SOCIAL_DISPONIBLE else '❌'}")
        st.markdown(f"⚡ Auto: {'✅' if AUTOMATION_DISPONIBLE else '❌'}")
        st.markdown(f"🔍 Research: {'✅' if RESEARCH_DISPONIBLE else '❌'}")
    st.divider()
    
    st.markdown("**⚙️ Modos**")
    col1, col2 = st.columns(2)
    with col1:
        modo_auto = st.toggle("🤖 Automático", value=True)
    with col2:
        modo_dios = st.toggle("🧠 Modo Dios", value=True)
    
    if modo_auto:
        st.caption("✅ Los agentes ejecutan tareas automáticamente")
    if modo_dios:
        st.caption("👤 Requiere aprobación para acciones críticas")
    st.divider()
    
    st.markdown("**💳 Créditos Globales**")
    total_creditos = sum(n.get("creditos", 0) for n in st.session_state.negocios.values())
    col1, col2 = st.columns(2)
    col1.metric("Total", total_creditos)
    col2.metric("Negocios", len(st.session_state.negocios))
    st.divider()
    
    st.markdown("**🏢 Negocios**")
    with st.expander("➕ CREAR NUEVO NEGOCIO", expanded=False):
        nuevo_nombre = st.text_input("Nombre", placeholder="Ej: Mi Empresa", key="nuevo_nombre")
        nuevo_icono = st.text_input("Icono (emoji)", placeholder="🏢", max_chars=2, key="nuevo_icono")
        nueva_descripcion = st.text_area("Descripción", placeholder="Breve descripción", key="nueva_descripcion")
        
        if st.button("🚀 CREAR NEGOCIO", use_container_width=True, key="crear_negocio_btn"):
            if nuevo_nombre and nuevo_icono and nueva_descripcion:
                crear_negocio(nuevo_nombre, nuevo_icono, nueva_descripcion)
                st.success(f"✅ Negocio '{nuevo_nombre}' creado!")
                st.rerun()
            else:
                st.warning("⚠️ Completa todos los campos.")
    
    st.divider()
    for key, negocio in st.session_state.negocios.items():
        creditos = negocio.get("creditos", 0)
        label = f"{negocio['icono']} {negocio['nombre']} ({creditos}💳)"
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.negocio_seleccionado = key
            st.rerun()
    
    st.divider()
    st.caption("v3.0 · Todas las funciones")

# ========== SELECCIÓN DE NEGOCIO ==========
st.subheader("📋 Tus Negocios")

if st.session_state.negocios:
    cols = st.columns(min(len(st.session_state.negocios), 4))
    for idx, (key, negocio) in enumerate(st.session_state.negocios.items()):
        with cols[idx % 4]:
            selected = st.session_state.negocio_seleccionado == key
            border_color = negocio["color"] if selected else "#e0e0e0"
            bg_color = "#f0f4ff" if selected else "white"
            creditos = negocio.get("creditos", 0)
            
            st.markdown(f"""
            <div class="business-card {'selected' if selected else ''}" 
                 style="border-color: {border_color}; background: {bg_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 2rem;">{negocio['icono']}</span>
                        <h4 style="margin: 0; color: {negocio['color']};">{negocio['nombre']}</h4>
                        <small style="color: #888;">{negocio['descripcion'][:40]}...</small>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem;">{'✅' if selected else '🔘'}</span>
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem;">
                    <span>📋 {negocio['metricas']['Proyectos']}</span>
                    <span>👥 {negocio['metricas']['Clientes']}</span>
                    <span>💰 {negocio['metricas']['Ingresos']}</span>
                    <span>💳 {creditos}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Seleccionar", key=f"select_{key}", use_container_width=True):
                st.session_state.negocio_seleccionado = key
                st.rerun()
else:
    st.info("👈 Crea tu primer negocio usando el botón '➕ CREAR NEGOCIO' en el panel lateral.")

st.divider()

# ========== DASHBOARD DEL NEGOCIO SELECCIONADO ==========
if st.session_state.negocio_seleccionado and st.session_state.negocio_seleccionado in st.session_state.negocios:
    negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
    st.markdown(f"## {negocio['icono']} {negocio['nombre']}")

    # ===== FILA 1: Métricas =====
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📋 Proyectos", negocio["metricas"]["Proyectos"])
    with col2:
        st.metric("👥 Clientes", negocio["metricas"]["Clientes"])
    with col3:
        st.metric("💰 Ingresos", negocio["metricas"]["Ingresos"])
    with col4:
        st.metric("🎯 Prospectos", negocio["metricas"]["Prospectos"])
    with col5:
        st.metric("💳 Créditos", negocio.get("creditos", 0))

    # ===== FILA 2: Sitio Web =====
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🌐 Sitio Web")
            st.markdown(f"**URL:** {negocio['sitio_web']['url']}")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("👀 Visitantes", negocio['sitio_web']['visitantes'])
            with col_b:
                st.metric("💰 Ingresos", negocio['sitio_web']['ingresos'])
            with col_c:
                st.caption(f"🔄 {negocio['sitio_web']['actualizado']}")
            
            if WEB_DISPONIBLE:
                if st.button("🚀 GENERAR SITIO WEB", use_container_width=True):
                    resultado, msg = generar_sitio_web(st.session_state.negocio_seleccionado)
                    if resultado:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("⚠️ Módulo web no disponible")
            
            st.checkbox("PAGOS DE PREPARACIÓN", value=False)

    with col2:
        with st.container(border=True):
            st.markdown("### 📊 Estadísticas")
            st.metric("VISITANTES", negocio['sitio_web']['visitantes'])
            st.metric("INGRESOS", negocio['sitio_web']['ingresos'])
            st.caption(f"ACTUALIZADO {negocio['sitio_web']['actualizado']}")
            if negocio['sitio_web'].get('archivo_generado'):
                st.success(f"📁 Archivo: {negocio['sitio_web']['archivo_generado']}")

    # ===== FILA 3: Tareas (Kanban) =====
    st.subheader("📋 Tareas")
    
    total_tareas = len(negocio["tareas"])
    tareas_todo = len([t for t in negocio["tareas"] if t["estado"] == "TODO"])
    tareas_progreso = len([t for t in negocio["tareas"] if t["estado"] == "EN_PROGRESO"])
    tareas_hecho = len([t for t in negocio["tareas"] if t["estado"] == "HECHO"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total", total_tareas)
    with col2:
        st.metric("⏳ TODO", tareas_todo)
    with col3:
        st.metric("🔄 En Progreso", tareas_progreso)
    with col4:
        st.metric("✅ HECHO", tareas_hecho)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ⏳ TODO")
        for tarea in negocio["tareas"]:
            if tarea["estado"] == "TODO":
                with st.container(border=True):
                    st.markdown(f"**{tarea['titulo']}**")
                    st.caption(f"🏷️ {tarea['categoria']} | 💳 {tarea['creditos']}")
                    if st.button(f"▶️ Iniciar", key=f"iniciar_{tarea['id']}"):
                        mover_tarea(st.session_state.negocio_seleccionado, tarea["id"], "EN_PROGRESO")
                        st.rerun()
    
    with col2:
        st.markdown("### 🔄 En Progreso")
        for tarea in negocio["tareas"]:
            if tarea["estado"] == "EN_PROGRESO":
                with st.container(border=True):
                    st.markdown(f"**{tarea['titulo']}**")
                    st.caption(f"🏷️ {tarea['categoria']} | 💳 {tarea['creditos']}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"⬅️", key=f"volver_{tarea['id']}"):
                            mover_tarea(st.session_state.negocio_seleccionado, tarea["id"], "TODO")
                            st.rerun()
                    with col_b:
                        if st.button(f"✅", key=f"completar_{tarea['id']}"):
                            mover_tarea(st.session_state.negocio_seleccionado, tarea["id"], "HECHO")
                            st.rerun()
    
    with col3:
        st.markdown("### ✅ HECHO")
        for tarea in negocio["tareas"]:
            if tarea["estado"] == "HECHO":
                with st.container(border=True):
                    st.markdown(f"**{tarea['titulo']}**")
                    st.caption(f"🏷️ {tarea['categoria']} | {tarea['tiempo']}")

    with st.expander("➕ Agregar nueva tarea"):
        nueva_tarea_titulo = st.text_input("Título", key="nueva_tarea_titulo")
        nueva_tarea_categoria = st.selectbox("Categoría", ["ESTRATEGIA", "DISEÑO", "MARKETING", "VENTAS", "CONTENIDO", "INVESTIGACIÓN", "FINANZAS"], key="nueva_tarea_categoria")
        nueva_tarea_creditos = st.number_input("Créditos", min_value=1, max_value=5, value=1, key="nueva_tarea_creditos")
        
        if st.button("➕ Crear tarea", key="crear_tarea_btn"):
            if nueva_tarea_titulo:
                nuevo_id = max([t["id"] for t in negocio["tareas"]] + [0]) + 1
                negocio["tareas"].append({
                    "id": nuevo_id,
                    "titulo": nueva_tarea_titulo,
                    "categoria": nueva_tarea_categoria,
                    "estado": "TODO",
                    "creditos": nueva_tarea_creditos,
                    "tiempo": "PENDIENTE"
                })
                st.success("✅ Tarea creada")
                st.rerun()
            else:
                st.warning("⚠️ Ingresa un título")

    st.divider()

    # ===== FILA 4: Rutinas + Equipos =====
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🔄 Rutinas")
            st.checkbox("🌙 Turno de noche", value=negocio['rutinas']['turno_nocturno'])
            st.checkbox("📅 DIARIO", value=negocio['rutinas']['diario'])
            st.checkbox("📊 SEMANAL", value=negocio['rutinas']['semanal'])
            
            if AUTOMATION_DISPONIBLE:
                if st.session_state.scheduler_activo:
                    if st.button("⏹️ DETENER AUTOMATIZACIÓN", use_container_width=True):
                        resultado = detener_automatizacion()
                        st.info(resultado)
                        st.rerun()
                else:
                    if st.button("▶️ INICIAR AUTOMATIZACIÓN", use_container_width=True):
                        resultado = iniciar_automatizacion()
                        st.info(resultado)
                        st.rerun()
            else:
                st.warning("⚠️ Módulo de automatización no disponible")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 👥 Equipos")
            for miembro in negocio['equipos']:
                st.markdown(f"👤 **{miembro['nombre']}** - {miembro['rol']}")
                st.caption(f"📧 {miembro['email']}")
            st.button("➕ AÑADIR MIEMBRO", use_container_width=True)

    # ===== FILA 5: Agentes + Documentos =====
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🤖 Agentes")
            for agente in negocio["agentes"]:
                estado_color = "🟢" if agente["estado"] == "Activo" else "🔴"
                st.markdown(f"""
                <div class="task-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{agente['nombre']}</strong>
                            <small style="color: #888; display: block;">{agente['rol']}</small>
                        </div>
                        <div>
                            <span>{estado_color} {agente['estado']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("### 📄 Documentos")
            if negocio.get("documentos"):
                for doc in negocio["documentos"]:
                    st.markdown(f"📄 **{doc['nombre']}**")
                    st.caption(f"Estado: {doc['estado']} | {doc['fecha']}")
            else:
                st.caption("No hay documentos aún")
            st.button("📂 VER TODO", use_container_width=True)

    # ===== FILA 6: Redes Sociales =====
    st.subheader("📱 Redes Sociales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐦 Twitter")
            if negocio['redes_sociales']['twitter']['conectado']:
                st.success(f"✅ {negocio['redes_sociales']['twitter']['usuario']}")
                st.caption(f"🕐 {negocio['redes_sociales']['twitter']['ultimo_tweet']}")
            else:
                st.warning("❌ No conectado")
            
            if SOCIAL_DISPONIBLE:
                tweet_mensaje = st.text_area("Mensaje para Twitter", value=f"🚀 {negocio['nombre']} está en marcha!", key="tweet_msg")
                if st.button("🐦 PUBLICAR TWEET", use_container_width=True):
                    resultado = publicar_en_twitter(st.session_state.negocio_seleccionado, tweet_mensaje)
                    st.info(resultado)
                    if "✅" in resultado:
                        st.rerun()
            else:
                st.warning("⚠️ Módulo social no disponible")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 📸 Instagram")
            if negocio['redes_sociales']['instagram']['conectado']:
                st.success(f"✅ {negocio['redes_sociales']['instagram']['usuario']}")
                st.caption(f"🕐 {negocio['redes_sociales']['instagram']['ultimo_post']}")
            else:
                st.warning("❌ No conectado")
    
    with col3:
        with st.container(border=True):
            st.markdown("### 💼 LinkedIn")
            if negocio['redes_sociales']['linkedin']['conectado']:
                st.success(f"✅ {negocio['redes_sociales']['linkedin']['usuario']}")
            else:
                st.warning("❌ No conectado")
    
    st.button("🔗 CONECTAR REDES SOCIALES", use_container_width=True)

    # ===== FILA 7: Correo + Anuncios =====
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📧 Correo Electrónico")
            st.markdown(f"📨 {negocio['correo']['email']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("📤 ENVIADOS", negocio['correo']['enviados'])
            with col_b:
                st.metric("📥 RECIBIDOS", negocio['correo']['recibidos'])
            if negocio['correo']['ultimo']:
                st.caption(f"📩 Último: {negocio['correo']['ultimo']}")
            
            if EMAIL_DISPONIBLE:
                with st.expander("📝 Enviar correo"):
                    email_destino = st.text_input("Destino", key="email_destino")
                    email_asunto = st.text_input("Asunto", key="email_asunto")
                    email_contenido = st.text_area("Contenido", key="email_contenido")
                    if st.button("📤 ENVIAR CORREO", use_container_width=True):
                        if email_destino and email_asunto and email_contenido:
                            resultado = enviar_correo_negocio(
                                st.session_state.negocio_seleccionado,
                                email_destino,
                                email_asunto,
                                email_contenido
                            )
                            st.info(resultado)
                            if "✅" in resultado:
                                st.rerun()
                        else:
                            st.warning("⚠️ Completa todos los campos")
            else:
                st.warning("⚠️ Módulo email no disponible")
            
            st.button("📬 VER TODO", use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("### 📢 Anuncios")
            if negocio['anuncios']['activo']:
                st.success("✅ Campañas activas")
                st.metric("Presupuesto diario", negocio['anuncios']['presupuesto_diario'])
            else:
                st.warning("⏸️ Todavía no está corriendo")
                st.caption("Establece un presupuesto diario y los agentes crearán anuncios automáticamente.")
            st.button("📊 CONFIGURAR ANUNCIOS", use_container_width=True)
            
            # ===== INVESTIGACIÓN DE MERCADO =====
            with st.expander("🔍 Investigación de Mercado"):
                tema_investigacion = st.text_input("¿Qué quieres investigar?", key="tema_investigacion")
                if st.button("🔍 INVESTIGAR", use_container_width=True):
                    if tema_investigacion:
                        with st.spinner("Investigando..."):
                            resultado = investigar_mercado(tema_investigacion)
                            st.markdown(resultado)
                            if resultado and not resultado.startswith("❌"):
                                st.session_state.negocios[st.session_state.negocio_seleccionado]['timeline'].append({
                                    "accion": f"🔍 Investigación: {tema_investigacion[:30]}...",
                                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "tipo": "info"
                                })
                    else:
                        st.warning("⚠️ Ingresa un tema para investigar")

    # ===== FILA 8: Timeline =====
    st.subheader("📜 Timeline de Actividades")
    
    if negocio.get("timeline"):
        for item in negocio["timeline"][-8:]:
            icono = "📌" if item["tipo"] == "info" else "📋"
            st.markdown(f"""
            <div class="timeline-item">
                <span>{icono} {item['accion']}</span>
                <span style="float: right; font-size: 0.7rem; color: #888;">{item['fecha']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No hay actividad reciente")

else:
    st.info("👈 Selecciona un negocio para ver su dashboard o crea uno nuevo.")

st.divider()

# ========== CHAT CON AGENTES (CON SPINNER DE PROCESANDO) ==========
st.subheader("💬 Chat con Agentes")

with st.container(border=True):
    if st.session_state.chat_historial:
        for msg in st.session_state.chat_historial[-10:]:
            if msg["role"] == "user":
                st.markdown(f"**👤 Tú:** {msg['content']}")
            else:
                agente_nombre = msg.get('agente', 'Agente')
                if agente_nombre == "⏳ Procesando...":
                    st.markdown(f"""
                    <div class="chat-message-processing">
                        <strong>🤖 ⏳ Procesando...</strong><br>
                        <span class="processing-text">🔄 {msg['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**🤖 {agente_nombre}:** {msg['content']}")
            st.divider()
    else:
        st.caption("💬 Escribe un mensaje para comenzar a conversar con los agentes.")

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        mensaje = st.text_input(
            "Pregunta a BuildSmart lo que quieras...",
            key="chat_input",
            placeholder="Ej: ¿Cuántas tareas tengo? o cambiar modelo ox_alpha",
            label_visibility="collapsed"
        )
    with col2:
        enviar = st.form_submit_button("📤 Enviar", use_container_width=True)
    
    if enviar and mensaje:
        st.session_state.chat_historial.append({"role": "user", "content": mensaje})
        st.session_state.chat_historial.append({
            "role": "agent",
            "agente": "⏳ Procesando...",
            "content": "Estoy procesando tu pregunta... esto puede tomar unos segundos. ⏳"
        })
        st.rerun()

if st.session_state.chat_historial:
    ultimo_msg = st.session_state.chat_historial[-1]
    if ultimo_msg.get("agente") == "⏳ Procesando...":
        if len(st.session_state.chat_historial) >= 2:
            user_msg = st.session_state.chat_historial[-2]["content"]
            try:
                respuesta, agente = responder_chat(user_msg)
            except Exception as e:
                respuesta = f"❌ Error al procesar: {str(e)}"
                agente = "Sistema"
            
            st.session_state.chat_historial[-1] = {
                "role": "agent",
                "agente": agente,
                "content": respuesta
            }
            st.rerun()

if st.button("🗑️ Limpiar chat", use_container_width=False):
    st.session_state.chat_historial = [
        {"role": "agent", "agente": "Orquestador", "content": "👋 ¡Bienvenido a BuildSmart Holdings! Soy tu asistente. (IA: Ollama)"}
    ]
    st.rerun()

# ========== PIE DE PÁGINA ==========
total_agentes = sum(len(n.get('agentes', [])) for n in st.session_state.negocios.values())
total_creditos = sum(n.get("creditos", 0) for n in st.session_state.negocios.values())
st.markdown(f"""
<div class="footer">
    BuildSmart Holdings v3.0 | 
    Negocios: {len(st.session_state.negocios)} | 
    Agentes: {total_agentes} | 
    Créditos: {total_creditos} 💳 |
    IA: {'✅' if IA_DISPONIBLE else '❌'} |
    Web: {'✅' if WEB_DISPONIBLE else '❌'} |
    Email: {'✅' if EMAIL_DISPONIBLE else '❌'} |
    Social: {'✅' if SOCIAL_DISPONIBLE else '❌'} |
    Auto: {'✅' if AUTOMATION_DISPONIBLE else '❌'} |
    Research: {'✅' if RESEARCH_DISPONIBLE else '❌'} |
    Modelo: {obtener_nombre_modelo()} |
    Última actualización: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)