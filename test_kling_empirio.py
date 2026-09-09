import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('KLING_API_KEY')

if not api_key:
    print('❌ KLING_API_KEY no encontrada')
    exit()

print(f'🔑 Clave Kling: {api_key[:20]}...{api_key[-10:]}')
print('🚀 Probando Kling AI vía EmpirioLabs...\n')

# Endpoint de EmpirioLabs para Kling AI
url = 'https://api.empiriolabs.ai/v1/videos/generations'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Prueba simple con el modelo Kling 3.0 Turbo
payload = {
    'model': 'kling-3-0-turbo',
    'prompt': 'Un robot construyendo una casa en un paisaje futurista',
    'duration': 5,
    'resolution': '720p'
}

try:
    print('📤 Enviando solicitud a EmpirioLabs...')
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f'📥 Código de respuesta: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print('✅ Conexión exitosa con Kling AI vía EmpirioLabs!')
        print(f'📝 Respuesta: {json.dumps(data, indent=2)[:500]}...')
        
        if 'task_id' in data:
            print(f'\n🎬 Task ID: {data["task_id"]}')
            
    elif response.status_code == 401:
        print('❌ Clave inválida. Verifica KLING_API_KEY')
    elif response.status_code == 402:
        print('💰 Saldo insuficiente. Necesitas recargar créditos')
    elif response.status_code == 429:
        print('⚠️ Límite de tasa excedido. Espera unos minutos.')
    else:
        print(f'❌ Error: {response.text[:500]}...')
        
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')