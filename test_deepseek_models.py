import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')

if not api_key:
    print('❌ DEEPSEEK_API_KEY no encontrada')
    exit()

print(f'🔑 Clave DeepSeek: {api_key[:15]}...{api_key[-10:]}')
print('🚀 Probando modelos gratuitos de DeepSeek...\n')

url = 'https://api.deepseek.com/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Modelos disponibles en DeepSeek
modelos = [
    'deepseek-chat',
    'deepseek-reasoner',
    'deepseek-v4-flash',
    'deepseek-v4-pro'
]

for modelo in modelos:
    print(f'🔍 Probando: {modelo}')
    
    payload = {
        'model': modelo,
        'messages': [
            {'role': 'user', 'content': 'Responde "Soy DeepSeek ' + modelo + '" en español.'}
        ],
        'max_tokens': 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f'   ✅ FUNCIONA: {content}\n')
        elif response.status_code == 401:
            print(f'   ❌ Clave inválida\n')
        else:
            print(f'   ❌ Error {response.status_code}: {response.text[:100]}...\n')
            
    except Exception as e:
        print(f'   ❌ Excepción: {str(e)[:50]}\n')