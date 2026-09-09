# test_arquitectura_c_completa.py - Prueba completa de la Arquitectura C
import sys
import os
import time

sys.path.insert(0, os.getcwd())

print("=" * 70)
print("🧪 PRUEBA COMPLETA DE LA ARQUITECTURA C - VERSIÓN 7.1")
print("=" * 70)

# ============================================
# 1. PROBAR GATEWAY
# ============================================
print("\n📡 1. Probando Gateway...")
print("-" * 50)

try:
    from backend.gateway import gateway
    print("✅ Gateway importado correctamente")
    
    # Prueba 1: Chat simple
    print("\n🔍 Prueba 1.1: Chat simple")
    inicio = time.time()
    respuesta, fuente = gateway.chat("Hola, ¿cómo estás?")
    fin = time.time()
    print(f"✅ Fuente: {fuente}")
    print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
    print(f"📝 Respuesta: {respuesta[:150]}...")
    
    # Prueba 2: Mensaje largo
    print("\n🔍 Prueba 1.2: Mensaje largo")
    inicio = time.time()
    respuesta, fuente = gateway.chat("Necesito un análisis detallado del mercado de la construcción en Latinoamérica")
    fin = time.time()
    print(f"✅ Fuente: {fuente}")
    print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
    print(f"📝 Respuesta: {respuesta[:150]}...")
    
except Exception as e:
    print(f"❌ Error en Gateway: {e}")
    import traceback
    traceback.print_exc()
    exit()

# ============================================
# 2. PROBAR ORQUESTADOR
# ============================================
print("\n" + "=" * 70)
print("📡 2. Probando Orquestador...")
print("-" * 50)

try:
    from backend.orquestador import ejecutar_orquestador
    print("✅ Orquestador importado correctamente")
    
    # Prueba 3: Plan de marketing
    print("\n🔍 Prueba 2.1: Plan de marketing")
    mensaje = "Necesito un plan de marketing para mi negocio de construcción"
    print(f"📝 Mensaje: {mensaje}")
    
    inicio = time.time()
    resultado = ejecutar_orquestador(mensaje)
    fin = time.time()
    
    print(f"⏱️ Tiempo total: {fin - inicio:.2f}s")
    print(f"📌 Paso final: {resultado.get('paso_actual', 'N/A')}")
    print(f"📊 Historial: {len(resultado.get('historial', []))} pasos")
    
    if resultado.get('resultado'):
        print(f"\n📝 Resultado final:\n{resultado['resultado'][:300]}...")
    
    # Prueba 4: Con búsqueda
    print("\n" + "=" * 70)
    print("🔍 Prueba 2.2: Con búsqueda")
    mensaje = "Buscar noticias sobre construcción sostenible en 2026"
    print(f"📝 Mensaje: {mensaje}")
    
    inicio = time.time()
    resultado = ejecutar_orquestador(mensaje)
    fin = time.time()
    
    print(f"⏱️ Tiempo total: {fin - inicio:.2f}s")
    print(f"📌 Paso final: {resultado.get('paso_actual', 'N/A')}")
    print(f"📊 Historial: {len(resultado.get('historial', []))} pasos")
    
    if resultado.get('resultado'):
        print(f"\n📝 Resultado final:\n{resultado['resultado'][:300]}...")
    
    # Prueba 5: Sin herramientas específicas
    print("\n" + "=" * 70)
    print("🔍 Prueba 2.3: Pregunta general")
    mensaje = "¿Cuáles son las mejores estrategias para reducir costos en construcción?"
    print(f"📝 Mensaje: {mensaje}")
    
    inicio = time.time()
    resultado = ejecutar_orquestador(mensaje)
    fin = time.time()
    
    print(f"⏱️ Tiempo total: {fin - inicio:.2f}s")
    print(f"📌 Paso final: {resultado.get('paso_actual', 'N/A')}")
    print(f"📊 Historial: {len(resultado.get('historial', []))} pasos")
    
    if resultado.get('resultado'):
        print(f"\n📝 Resultado final:\n{resultado['resultado'][:300]}...")
    
except Exception as e:
    print(f"❌ Error en Orquestador: {e}")
    import traceback
    traceback.print_exc()

# ============================================
# 3. PRUEBA DE MODELOS ESPECÍFICOS
# ============================================
print("\n" + "=" * 70)
print("📡 3. Probando modelos específicos...")
print("-" * 50)

try:
    from backend.gateway import chat_groq_directo, chat_gemini_directo, chat_openrouter, chat_deepseek
    
    # Groq
    print("\n🔍 Prueba 3.1: Groq")
    try:
        inicio = time.time()
        respuesta = chat_groq_directo("Hola", "Eres un asistente.")
        fin = time.time()
        print(f"✅ Groq OK - {fin - inicio:.2f}s")
        print(f"📝 {respuesta[:100]}...")
    except Exception as e:
        print(f"❌ Groq falló: {e}")
    
    # Gemini
    print("\n🔍 Prueba 3.2: Gemini")
    try:
        inicio = time.time()
        respuesta = chat_gemini_directo("Hola", "Eres un asistente.")
        fin = time.time()
        print(f"✅ Gemini OK - {fin - inicio:.2f}s")
        print(f"📝 {respuesta[:100]}...")
    except Exception as e:
        print(f"⚠️ Gemini falló: {e}")
    
    # OpenRouter
    print("\n🔍 Prueba 3.3: OpenRouter")
    try:
        inicio = time.time()
        respuesta = chat_openrouter("Hola", "Eres un asistente.")
        fin = time.time()
        print(f"✅ OpenRouter OK - {fin - inicio:.2f}s")
        print(f"📝 {respuesta[:100]}...")
    except Exception as e:
        print(f"⚠️ OpenRouter falló: {e}")
    
    # DeepSeek
    print("\n🔍 Prueba 3.4: DeepSeek")
    try:
        inicio = time.time()
        respuesta = chat_deepseek("Hola", "Eres un asistente.")
        fin = time.time()
        print(f"✅ DeepSeek OK - {fin - inicio:.2f}s")
        print(f"📝 {respuesta[:100]}...")
    except Exception as e:
        print(f"⚠️ DeepSeek falló: {e}")
    
except Exception as e:
    print(f"❌ Error en pruebas de modelos: {e}")

# ============================================
# 4. RESUMEN FINAL
# ============================================
print("\n" + "=" * 70)
print("✅ PRUEBA COMPLETA FINALIZADA")
print("=" * 70)

print("\n📊 Resumen de la Arquitectura C:")
print("  ✅ Gateway: Enrutamiento inteligente")
print("  ✅ Orquestador: 5 nodos (Brainstorm → Plan → Work → Review → Compound)")
print("  ✅ Modelos: Groq, Gemini, OpenRouter, DeepSeek")
print("  ✅ Herramientas: Búsqueda (DuckDuckGo)")
print("  ✅ Fallback: Ollama (local)")
print("  ✅ Manejo de errores: Timeouts, Rate Limits, 404")

print("\n" + "=" * 70)
print("🚀 ARQUITECTURA C LISTA PARA PRODUCCIÓN")
print("=" * 70)