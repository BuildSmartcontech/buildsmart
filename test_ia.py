# test_ia.py - Probar conexión con DeepSeek

from utils.ia import ia

print("🧠 Probando conexión con DeepSeek...")
print("=" * 50)

# 1. Probar chat simple
print("\n📝 Prueba 1: Chat simple")
respuesta = ia.chat("¿Quién eres y qué puedes hacer?")
print(f"Respuesta: {respuesta[:200]}...")

# 2. Probar investigación
print("\n🔍 Prueba 2: Investigación")
investigacion = ia.investigar("Tendencias en inteligencia artificial para 2026")
print(f"Reporte: {investigacion[:300]}...")

print("\n✅ Pruebas completadas")