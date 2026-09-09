# test_openrouter.py - Prueba de OpenRouter
import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave
api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print('❌ OPENROUTER_API_KEY no encontrada en .env')
    exit()

print(f'🔑 API Key encontrada: {api_key[:15]}...{api_key[-10:]}')
print(f'📏 Longitud: {len(api_key)} caracteres')

# Probar OpenRouter con modelo gratuito
print('\n🚀 Probando OpenRouter con modelo gratuito...')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'https://buildsmart.com',
    'X-Title': 'BuildSmart Holdings'
}

# Lista de modelos gratuitos a probar
modelos = [
    'google/gemma-2-2b-it:free',
    'microsoft/phi-3-mini-128k-instruct:free',
    'meta-llama/llama-3.2-3b-instruct:free',
    'openrouter/free'
]

for modelo in modelos:
    print(f'\n🔍 Probando modelo: {modelo}')
    
    payload = {
        'model': modelo,
        'messages': [
            {'role': 'user', 'content': 'Responde "Hola, soy OpenRouter" en español. Solo responde esa frase.'}
        ],
        'temperature': 0.7,
        'max_tokens': 100
    }
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f'📥 Código de respuesta: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content']
            print(f'✅ OpenRouter funciona con {modelo}!')
            print(f'📝 Respuesta: {text}')
            print('\n✅ Modelo encontrado, actualiza gateway.py con:')
            print(f'   "openrouter/{modelo}"')
            break
        else:
            print(f'❌ Error: {response.status_code}')
            print(f'📝 {response.text[:200]}...')
            
    except Exception as e:
        print(f'❌ Error de conexión: {str(e)[:100]}...')

print('\n✅ Prueba completada.')