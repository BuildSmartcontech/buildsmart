# test_email.py - Probar envío de correo

from utils.email_sender import email_sender
import os
from dotenv import load_dotenv

load_dotenv()

print("📧 Probando envío de correo...")
print("=" * 50)

# Verificar configuración
email_user = os.getenv('EMAIL_USER', '')
if not email_user:
    print("❌ ERROR: No has configurado EMAIL_USER en .env")
    print("📝 Agrega: EMAIL_USER=tu_correo@gmail.com")
    exit()

print(f"📧 Correo configurado: {email_user}")

# Enviar correo de prueba
destino = input("📧 Correo de destino para la prueba: ")
asunto = "🧪 Prueba de BuildSmart Holdings"
contenido = """
¡Hola!

Este es un correo de prueba enviado desde BuildSmart Holdings.

Si estás leyendo esto, ¡el sistema de correo funciona correctamente!

Saludos,
El equipo de BuildSmart
"""

print(f"\n📤 Enviando correo a {destino}...")
resultado = email_sender.enviar_correo(destino, asunto, contenido)

print(f"\n📊 Resultado:")
print(resultado)