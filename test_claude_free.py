import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print('❌ OPENROUTER_API_KEY no encontrada')
    exit()

print(f'🔑 Clave OpenRouter: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando Claude 3.5 Sonnet (versión gratuita)...\n')

url = 'https://openrouter.ai/api/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'anthropic/claude-3.5-sonnet:free',
    'messages': [
        {'role': 'user', 'content': 'Responde "Hola, soy Claude gratis" en español.'}
    ],
    'max_tokens': 100
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f'📥 Código de respuesta: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        content = data['choices'][0]['message']['content']
        print('✅ Claude gratis funciona!')
        print(f'📝 Respuesta: {content}')
    else:
        print(f'❌ Error: {response.text[:300]}...')
        
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')