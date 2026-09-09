import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('KIMI_API_KEY')

if not api_key:
    print('❌ KIMI_API_KEY no encontrada')
    exit()

print(f'🔑 Clave: {api_key[:15]}...{api_key[-10:]}')

# Endpoint de Kimi (Moonshot)
url = 'https://api.moonshot.cn/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'moonshot-v1-8k',  # Modelo de Kimi (8k contexto)
    'messages': [
        {'role': 'user', 'content': 'Responde "Hola, soy Kimi" en español.'}
    ],
    'temperature': 0.7,
    'max_tokens': 100
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f'📥 Código: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        text = result['choices'][0]['message']['content']
        print(f'✅ Kimi funciona!')
        print(f'📝 Respuesta: {text}')
    else:
        print(f'❌ Error: {response.text[:500]}...')
        
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')