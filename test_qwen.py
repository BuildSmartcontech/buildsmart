import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALIBABA_API_KEY')

if not api_key:
    print('❌ ALIBABA_API_KEY no encontrada')
    exit()

print(f'🔑 Clave: {api_key[:20]}...{api_key[-10:]}')

# Endpoint de Bailian (OpenAI Compatible) - CORREGIDO
url = "https://ws-jkf2g755bnibb506.ap-southeast-1.maas.aliyuncs.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "qwen-turbo",
    "messages": [
        {"role": "user", "content": "Responde 'Hola, soy Qwen' en español."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f'📥 Código: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        text = result['choices'][0]['message']['content']
        print(f'✅ Qwen funciona!')
        print(f'📝 Respuesta: {text}')
    else:
        print(f'❌ Error: {response.text[:500]}...')
        
except Exception as e:
    print(f'❌ Error: {str(e)}')