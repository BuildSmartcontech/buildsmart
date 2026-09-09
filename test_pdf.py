# test_pdf.py - Prueba de PDF
import sys
import os
sys.path.insert(0, os.getcwd())

from utils.pdf_generator import generar_pdf_plan
from backend.orquestador import ejecutar_orquestador

print("🧪 Generando plan y PDF...")

# Generar plan
resultado = ejecutar_orquestador("Necesito un plan de marketing para mi negocio de construcción")
plan = resultado.get("resultado", "")

if plan:
    # Generar PDF
    ruta = generar_pdf_plan(plan, "Plan de Marketing BuildSmart")
    if ruta:
        print(f"✅ PDF guardado en: {ruta}")
    else:
        print("❌ Error generando PDF")
else:
    print("❌ No se generó plan")