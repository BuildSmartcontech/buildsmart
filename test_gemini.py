# test_gemini.py - Prueba de conexión con Google Gemini
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('❌ GEMINI_API_KEY no encontrada en .env')
    exit()

print(f'🔑 API Key encontrada: {api_key[:15]}...{api_key[-10:]}')
print(f'📏 Longitud: {len(api_key)} caracteres')

# Probar conexión con Gemini - Listar modelos disponibles
url = f'https://generativelanguage.googleapis.com/v1beta/models?key={api_key}'

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        models = response.json()
        print('\n✅ Conexión exitosa! Modelos disponibles:')
        for model in models.get('models', [])[:15]:
            print(f'  - {model["name"].replace("models/", "")}')
        
        # Probar chat con el modelo más reciente
        print('\n🚀 Probando chat con Gemini...')
        chat_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}'
        
        payload = {
            'contents': [
                {'parts': [{'text': 'Responde "Hola, soy Gemini" en español, solo esa frase.'}]}
            ],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 100
            }
        }
        
        chat_response = requests.post(chat_url, json=payload, timeout=30)
        if chat_response.status_code == 200:
            result = chat_response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f'✅ Gemini respondió: {text}')
        else:
            print(f'❌ Error en chat: {chat_response.status_code}')
            print(f'📝 {chat_response.text[:200]}...')
            
    else:
        print(f'\n❌ Error: {response.status_code}')
        print(f'📝 Mensaje: {response.text[:300]}...')
        
except Exception as e:
    print(f'\n❌ Error de conexión: {str(e)}')