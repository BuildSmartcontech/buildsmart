# test_groq.py - Prueba de conexión con Groq
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print('❌ GROQ_API_KEY no encontrada en .env')
    exit()

print(f'🔑 Clave encontrada: {api_key[:15]}...{api_key[-10:]}')
print(f'📏 Longitud: {len(api_key)} caracteres')

# Probar conexión
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

try:
    response = requests.get(
        'https://api.groq.com/openai/v1/models',
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        models = response.json()
        print('\n✅ Conexión exitosa! Modelos disponibles:')
        for model in models.get('data', [])[:10]:
            print(f'  - {model["id"]}')
    else:
        print(f'\n❌ Error: {response.status_code}')
        print(f'📝 Mensaje: {response.text}')
        
except Exception as e:
    print(f'\n❌ Error de conexión: {str(e)}')