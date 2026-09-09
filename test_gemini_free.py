import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('❌ GEMINI_API_KEY no encontrada')
    exit()

print(f'🔑 Clave Gemini: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando modelos gratuitos de Gemini...\n')

# Modelos gratuitos de Gemini
modelos = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
    'gemini-3.6-flash',
    'gemini-3-flash',
    'gemini-3.1-flash-lite'
]

headers = {
    'Content-Type': 'application/json'
}

for modelo in modelos:
    print(f'🔍 Probando: {modelo}')
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
    
    payload = {
        'contents': [
            {
                'parts': [
                    {'text': 'Responde "Soy Gemini ' + modelo + '" en español.'}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 50
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content = data['candidates'][0]['content']['parts'][0]['text']
            print(f'   ✅ FUNCIONA: {content}\n')
        elif response.status_code == 404:
            print(f'   ❌ No disponible\n')
        else:
            print(f'   ❌ Error {response.status_code}: {response.text[:100]}...\n')
            
    except Exception as e:
        print(f'   ❌ Excepción: {str(e)[:50]}\n')