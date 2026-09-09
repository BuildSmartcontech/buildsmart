import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print('❌ OPENROUTER_API_KEY no encontrada')
    exit()

print(f'🔑 Clave OpenRouter: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando Qwen gratis en OpenRouter...\n')

url = 'https://openrouter.ai/api/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Modelos de Qwen gratis en OpenRouter
modelos = [
    'qwen/qwen3.6-plus:free',
    'qwen/qwen3-coder-480b-a35b:free',
    'qwen/qwen3-4b:free'
]

for modelo in modelos:
    print(f'🔍 Probando: {modelo}')
    
    payload = {
        'model': modelo,
        'messages': [
            {'role': 'user', 'content': 'Responde "Hola, soy Qwen" en español.'}
        ],
        'max_tokens': 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f'   ✅ Respuesta: {content}\n')
            break
        else:
            print(f'   ❌ Error {response.status_code}: {response.text[:100]}...\n')
            
    except Exception as e:
        print(f'   ❌ Excepción: {str(e)[:50]}\n')