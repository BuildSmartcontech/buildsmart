# test_gateway_v7.3.py
import sys
import os
import time

sys.path.insert(0, os.getcwd())

print("=" * 70)
print("🧪 PRUEBA GATEWAY - VERSIÓN 7.3")
print("=" * 70)

from backend.gateway import gateway

# Pruebas
pruebas = [
    ("Hola, ¿cómo estás?", "Chat simple"),
    ("Necesito un plan de marketing", "Plan de marketing"),
    ("Buscar noticias sobre construcción", "Búsqueda"),
]

for mensaje, nombre in pruebas:
    print(f"\n🔍 Prueba: {nombre}")
    inicio = time.time()
    try:
        respuesta, fuente = gateway.chat(mensaje)
        fin = time.time()
        print(f"✅ Fuente: {fuente}")
        print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
        print(f"📝 Respuesta: {respuesta[:150]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✅ Prueba completada")