# test_gemini_flash.py - Prueba de Gemini con formato correcto
import os
import requests
import json
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

# Probar Gemini 3.6 Flash con el formato correcto
print('\n🚀 Probando Gemini 3.6 Flash...')

# El formato correcto para Gemini 1.5+ es con "generateContent"
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}'

# Estructura correcta para Gemini API
payload = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Responde 'Hola, soy Gemini 3.6 Flash' en español. Solo responde esa frase."
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 100,
        "topP": 0.95,
        "topK": 40
    }
}

# Headers correctos
headers = {
    "Content-Type": "application/json"
}

try:
    print(f'📤 Enviando solicitud a: {url}')
    print(f'📦 Payload: {json.dumps(payload, indent=2)}')
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f'📥 Código de respuesta: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print(f'📄 Respuesta completa: {json.dumps(result, indent=2)[:500]}...')
        
        # Extraer el texto de la respuesta
        try:
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f'\n✅ Gemini 3.6 Flash funciona!')
            print(f'📝 Respuesta: {text}')
        except KeyError as e:
            print(f'❌ Error extrayendo texto: {e}')
            print(f'📄 Estructura: {result}')
    else:
        print(f'❌ Error: {response.status_code}')
        print(f'📝 Mensaje: {response.text[:500]}...')
        
        # Si falla, probar con otros modelos
        print('\n🔄 Probando con modelos alternativos...')
        
        modelos_alternativos = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-pro"
        ]
        
        for modelo in modelos_alternativos:
            print(f'\n🔍 Probando: {modelo}')
            url_alt = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            try:
                response_alt = requests.post(url_alt, json=payload, headers=headers, timeout=30)
                if response_alt.status_code == 200:
                    result_alt = response_alt.json()
                    text = result_alt['candidates'][0]['content']['parts'][0]['text']
                    print(f'✅ {modelo} funciona!')
                    print(f'📝 Respuesta: {text}')
                    break
                else:
                    print(f'❌ {modelo} falló: {response_alt.status_code}')
            except Exception as e:
                print(f'❌ Error con {modelo}: {str(e)[:50]}...')
        
except requests.exceptions.RequestException as e:
    print(f'❌ Error de conexión: {str(e)}')
except KeyError as e:
    print(f'❌ Error en la respuesta: {e}')
    print(f'📄 Respuesta recibida: {response.text[:300]}...')
except Exception as e:
    print(f'❌ Error inesperado: {str(e)}')