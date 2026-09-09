# test_orquestador_v7.4.py
import sys
import os
import time

sys.path.insert(0, os.getcwd())

print("=" * 70)
print("🧪 PRUEBA ORQUESTADOR - VERSIÓN 7.4")
print("=" * 70)

from backend.orquestador import ejecutar_orquestador

# Prueba 1: Búsqueda
print("\n🔍 Prueba 1: Búsqueda en DuckDuckGo")
inicio = time.time()
resultado = ejecutar_orquestador("Buscar noticias sobre construcción sostenible 2026")
fin = time.time()
print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
print(f"📝 Resultado:\n{resultado['resultado'][:500]}...")

# Prueba 2: Plan de marketing
print("\n" + "=" * 70)
print("\n📋 Prueba 2: Plan de marketing")
inicio = time.time()
resultado = ejecutar_orquestador("Necesito un plan de marketing para mi negocio de construcción")
fin = time.time()
print(f"⏱️ Tiempo: {fin - inicio:.2f}s")
print(f"📝 Resultado:\n{resultado['resultado'][:500]}...")

print("\n✅ Prueba completada")