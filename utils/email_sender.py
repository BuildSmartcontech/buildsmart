# utils/email_sender.py - Envío de correos con soporte UTF-8 completo

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email = os.getenv('EMAIL_USER', '')
        self.password = os.getenv('EMAIL_PASSWORD', '')
    
    def enviar_correo(self, destino, asunto, contenido):
        """Enviar un correo electrónico con soporte UTF-8 completo"""
        if not self.email or not self.password:
            return "❌ Configura EMAIL_USER y EMAIL_PASSWORD en .env"
        
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = destino
            
            # ========== CLAVE: Codificar asunto con UTF-8 ==========
            msg['Subject'] = Header(asunto, 'utf-8').encode()
            
            # Adjuntar contenido con UTF-8
            msg.attach(MIMEText(contenido, 'plain', 'utf-8'))
            
            # Conectar y enviar
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return "✅ Correo enviado correctamente"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def enviar_bienvenida(self, destino, nombre_negocio):
        """Enviar correo de bienvenida"""
        asunto = f"¡Bienvenido a {nombre_negocio}!"
        contenido = f"""
¡Hola!

Gracias por crear tu negocio {nombre_negocio} en BuildSmart Holdings.

Tu negocio está activo y listo para comenzar a crecer.

Puedes acceder a tu panel de control en cualquier momento.

¡Mucho éxito!

El equipo de BuildSmart Holdings
"""
        return self.enviar_correo(destino, asunto, contenido)

# Instancia global
email_sender = EmailSender()