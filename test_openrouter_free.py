import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print('❌ OPENROUTER_API_KEY no encontrada')
    exit()

print(f'🔑 Clave OpenRouter: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando modelos gratuitos de OpenRouter...\n')

url = 'https://openrouter.ai/api/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Modelos gratuitos confirmados
modelos = [
    'qwen/qwen3-coder:free',
    'nvidia/nemotron-3-super-120b-a12b:free',
    'deepseek/deepseek-v4-flash:free',
    'google/gemma-2-9b-it:free'
]

for modelo in modelos:
    print(f'🔍 Probando: {modelo}')
    
    payload = {
        'model': modelo,
        'messages': [{'role': 'user', 'content': 'Responde "Soy gratis" en español.'}],
        'max_tokens': 30
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f'   ✅ FUNCIONA: {content}\n')
            print(f'🎯 Modelo recomendado: {modelo}')
            break
        elif response.status_code == 404:
            print(f'   ❌ No disponible\n')
        else:
            print(f'   ❌ Error {response.status_code}: {response.text[:80]}...\n')
            
    except Exception as e:
        print(f'   ❌ Excepción: {str(e)[:50]}\n')