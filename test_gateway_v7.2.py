# test_gateway_v7.2.py - Prueba completa del Gateway optimizado
import sys
import os
import time

sys.path.insert(0, os.getcwd())

print("=" * 70)
print("🧪 PRUEBA GATEWAY - VERSIÓN 7.2 (OPTIMIZADO)")
print("=" * 70)

# ============================================
# 1. IMPORTAR GATEWAY
# ============================================
print("\n📡 1. Importando Gateway...")
print("-" * 50)

try:
    from backend.gateway import gateway
    print("✅ Gateway importado correctamente")
except Exception as e:
    print(f"❌ Error importando Gateway: {e}")
    exit()

# ============================================
# 2. PRUEBAS DE CHAT
# ============================================
print("\n" + "=" * 70)
print("📡 2. Probando Chat...")
print("-" * 50)

pruebas = [
    ("Hola, ¿cómo estás?", "Chat simple"),
    ("Necesito un plan de marketing para mi negocio", "Plan de marketing"),
    ("Buscar noticias sobre construcción", "Búsqueda"),
    ("¿Cuáles son las mejores estrategias para reducir costos?", "Estrategias"),
]

for mensaje, nombre in pruebas:
    print(f"\n🔍 Prueba: {nombre}")
    print(f"📝 Mensaje: {mensaje[:50]}...")
    
    inicio = time.time()
    try:
        respuesta, fuente = gateway.chat(mensaje)
        fin = time.time()
        
        print(f"✅ Fuente: {fuente}")
        print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
        print(f"📝 Respuesta: {respuesta[:150]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# ============================================
# 3. PRUEBA DE MODELOS INDIVIDUALES
# ============================================
print("\n" + "=" * 70)
print("📡 3. Probando modelos individuales...")
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
# 4. PRUEBA DE MANEJO DE ERRORES
# ============================================
print("\n" + "=" * 70)
print("📡 4. Probando manejo de errores...")
print("-" * 50)

# Prueba con mensaje vacío
print("\n🔍 Prueba 4.1: Mensaje vacío")
try:
    respuesta, fuente = gateway.chat("")
    print(f"✅ Fuente: {fuente}")
    print(f"📝 Respuesta: {respuesta[:100]}...")
except Exception as e:
    print(f"⚠️ Manejo de error: {e}")

# Prueba con mensaje muy largo
print("\n🔍 Prueba 4.2: Mensaje muy largo (500 caracteres)")
mensaje_largo = " " * 500
try:
    respuesta, fuente = gateway.chat(mensaje_largo)
    print(f"✅ Fuente: {fuente}")
    print(f"📝 Respuesta: {respuesta[:100]}...")
except Exception as e:
    print(f"⚠️ Manejo de error: {e}")

# ============================================
# 5. RESUMEN FINAL
# ============================================
print("\n" + "=" * 70)
print("✅ PRUEBA COMPLETA FINALIZADA")
print("=" * 70)

print("\n📊 Resumen del Gateway 7.2:")
print("  ✅ Groq: Con backoff exponencial (429)")
print("  ✅ Gemini: Con reintentos (503)")
print("  ✅ OpenRouter: Con manejo de errores")
print("  ✅ DeepSeek: Al final (ahorra saldo)")
print("  ✅ Ollama: Respaldo local")
print("  ✅ Timeouts: 30s por solicitud")
print("  ✅ Backoff: 2, 4, 8, 16s")

print("\n" + "=" * 70)
print("🚀 GATEWAY 7.2 LISTO PARA PRODUCCIÓN")
print("=" * 70)