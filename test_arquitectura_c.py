# test_arquitectura_c.py - Prueba de la Arquitectura C
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

print("=" * 60)
print("🧪 PROBANDO ARQUITECTURA C - VERSIÓN 7.0")
print("=" * 60)

# ============================================
# 1. PROBAR GATEWAY
# ============================================
print("\n📡 1. Probando Gateway...")
print("-" * 40)

try:
    from backend.gateway import gateway
    
    print("✅ Gateway importado correctamente")
    
    # Probar chat simple
    print("\n🔍 Probando chat simple...")
    respuesta, fuente = gateway.chat("Hola, ¿cómo estás?")
    print(f"✅ Fuente: {fuente}")
    print(f"📝 Respuesta: {respuesta[:150]}...")
    
except Exception as e:
    print(f"❌ Error en Gateway: {e}")
    exit()

# ============================================
# 2. PROBAR ORQUESTADOR
# ============================================
print("\n" + "=" * 60)
print("📡 2. Probando Orquestador...")
print("-" * 40)

try:
    from backend.orquestador import ejecutar_orquestador
    
    print("✅ Orquestador importado correctamente")
    
    # Probar orquestador
    print("\n🔍 Probando orquestador...")
    mensaje = "Necesito un plan de marketing para mi negocio de construcción"
    print(f"📝 Mensaje: {mensaje}")
    
    resultado = ejecutar_orquestador(mensaje)
    
    print("\n📊 Resultado del Orquestador:")
    print(f"  - Paso actual: {resultado.get('paso_actual', 'N/A')}")
    print(f"  - Plan: {resultado.get('plan', 'N/A')[:150]}...")
    print(f"  - Resultado final: {resultado.get('resultado', 'N/A')[:150]}...")
    print(f"  - Historial: {len(resultado.get('historial', []))} pasos")
    
except Exception as e:
    print(f"❌ Error en Orquestador: {e}")
    import traceback
    traceback.print_exc()

# ============================================
# 3. RESUMEN FINAL
# ============================================
print("\n" + "=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)