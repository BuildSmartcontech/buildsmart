# test_orquestador.py - Prueba rápida del orquestador
import sys
import os

sys.path.insert(0, os.getcwd())

print("=" * 60)
print("🧪 PROBANDO ORQUESTADOR - VERSIÓN 7.6")
print("=" * 60)

from backend.orquestador import ejecutar_orquestador

print("\n📝 Probando: Plan de marketing")
resultado = ejecutar_orquestador("Necesito un plan de marketing para mi negocio de construcción")

print("\n📊 RESULTADO:")
print(f"✅ Plan: {resultado['plan'][:200]}...")
print(f"✅ Resultado: {resultado['resultado'][:200]}...")
print(f"✅ Paso actual: {resultado['paso_actual']}")
print(f"✅ Historial: {len(resultado['historial'])} pasos")

print("\n✅ Prueba completada")