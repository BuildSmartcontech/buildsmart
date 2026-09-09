import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('❌ GEMINI_API_KEY no encontrada')
    exit()

print(f'🔑 Clave Gemini: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando Gemini Imagen...\n')

# Endpoint para generar imágenes con Gemini
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-image:generateContent?key={api_key}'

payload = {
    'contents': [
        {
            'parts': [
                {'text': 'Genera una imagen de un robot construyendo una casa en un paisaje futurista'}
            ]
        }
    ],
    'generationConfig': {
        'temperature': 1.0,
        'candidateCount': 1
    }
}

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f'📥 Código de respuesta: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        
        # Buscar la imagen en la respuesta
        if 'candidates' in data and len(data['candidates']) > 0:
            parts = data['candidates'][0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    image_data = part['inlineData'].get('data')
                    mime_type = part['inlineData'].get('mimeType', 'image/png')
                    
                    if image_data:
                        # Guardar la imagen
                        with open('gemini_imagen_test.png', 'wb') as f:
                            f.write(base64.b64decode(image_data))
                        print('✅ Imagen generada y guardada: gemini_imagen_test.png')
                        break
        else:
            print('⚠️ No se encontró imagen en la respuesta')
            print(f'📄 Respuesta: {data}')
    else:
        print(f'❌ Error: {response.text[:300]}...')
        
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')