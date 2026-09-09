import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALIBABA_API_KEY')

if not api_key:
    print('❌ ALIBABA_API_KEY no encontrada')
    exit()

print(f'🔑 Clave: {api_key[:20]}...{api_key[-10:]}')
print('=' * 60)

# Lista de URLs a probar
urls = [
    'https://ws-jkf2g755bnibb506.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions',
    'https://ws-jkf2g755bnibb506.ap-southeast-1.maas.aliyuncs.com/api/v1/chat/completions',
    'https://ws-jkf2g755bnibb506.ap-southeast-1.maas.aliyuncs.com/v1/chat/completions',
    'https://dashscope.aliyuncs.com/api/v1/chat/completions',
    'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
]

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

for url in urls:
    print(f'\n🔍 Probando: {url}')
    try:
        # Probar con qwen-plus
        payload = {
            'model': 'qwen-plus',
            'messages': [{'role': 'user', 'content': 'Hola'}]
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f'   Código: {r.status_code}')
        
        if r.status_code == 200:
            print('   ✅ FUNCIONA!')
            print(f'   Respuesta: {r.json()}')
            break
        elif r.status_code == 404:
            print('   ❌ URL no encontrada')
        else:
            print(f'   ❌ Error: {r.text[:100]}')
            
    except Exception as e:
        print(f'   ❌ Excepción: {str(e)[:50]}')