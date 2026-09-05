# test_db.py - Probar conexión a base de datos

from utils.database import db

print("🔌 Probando conexión a PostgreSQL...")

if db.connect():
    print("✅ Conexión exitosa")
    negocios = db.get_negocios()
    print(f"📊 Negocios encontrados: {len(negocios)}")
    if not negocios.empty:
        print(negocios[['id', 'nombre', 'icono']])
    else:
        print("⚠️ No hay negocios en la base de datos")
    db.disconnect()
else:
    print("❌ Error de conexión")