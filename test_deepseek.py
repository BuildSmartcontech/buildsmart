import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')

headers = {'Authorization': f'Bearer {api_key}'}
payload = {
    'model': 'deepseek-chat',
    'messages': [{'role': 'user', 'content': 'Responde "Hola, soy DeepSeek" en español.'}],
    'temperature': 0.7,
    'max_tokens': 100
}

response = requests.post('https://api.deepseek.com/v1/chat/completions', headers=headers, json=payload)

if response.status_code == 200:
    print('✅ DeepSeek funciona!')
    print('Respuesta:', response.json()['choices'][0]['message']['content'])
else:
    print('❌ Error:', response.status_code, response.text[:200])