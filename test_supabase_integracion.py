# test_supabase_integracion.py - Prueba de integración con Supabase
import sys
import os

sys.path.insert(0, os.getcwd())

print("=" * 70)
print("🧪 PRUEBA DE INTEGRACIÓN CON SUPABASE")
print("=" * 70)

# 1. Verificar cliente Supabase
print("\n📡 1. Verificando cliente Supabase...")
try:
    from utils.supabase_client import supabase
    if supabase.disponible:
        print("✅ Supabase client disponible")
    else:
        print("❌ Supabase client NO disponible")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# 2. Probar orquestador
print("\n" + "=" * 70)
print("📡 2. Probando orquestador...")
print("-" * 50)

try:
    from backend.orquestador import ejecutar_orquestador
    
    mensaje = "Necesito un plan de marketing para mi negocio de construcción"
    print(f"📝 Mensaje: {mensaje[:50]}...")
    
    resultado = ejecutar_orquestador(mensaje)
    
    print(f"✅ Plan generado: {resultado['resultado'][:100]}...")
    print(f"📊 Pasos: {len(resultado['historial'])}")
    
except Exception as e:
    print(f"❌ Error en orquestador: {e}")

# 3. Verificar historial en Supabase
print("\n" + "=" * 70)
print("📡 3. Verificando historial en Supabase...")
print("-" * 50)

try:
    from utils.supabase_client import supabase
    historial = supabase.obtener_historial(limite=5)
    
    print(f"📊 Últimos {len(historial)} registros guardados:")
    for item in historial:
        mensaje = item.get('mensaje', '')[:40]
        modelo = item.get('modelo_usado', 'desconocido')
        print(f"   - {mensaje}... → {modelo}")
        
except Exception as e:
    print(f"❌ Error al obtener historial: {e}")

print("\n" + "=" * 70)
print("✅ PRUEBA COMPLETADA")
print("=" * 70)