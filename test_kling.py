
import requests
import json
import time

api_key = 'api-key-kling-zlmHebCx17W7fSE9_FFFRCMbtYpRGj3XyBp_Rzcfnjw'

print('🚀 Probando Kling AI...')
print(f'🔑 Clave: {api_key[:25]}...')

# 1. CREAR TAREA DE VIDEO
url = 'https://api.klingai.com/v1/videos/generations'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
payload = {
    'model': 'kling-v3',
    'prompt': 'Un robot construyendo una casa en un paisaje futurista',
    'duration': 5,
    'resolution': '720p'
}

print('\n📤 Creando tarea de video...')
response = requests.post(url, headers=headers, json=payload, timeout=30)
print(f'📥 Código: {response.status_code}')

if response.status_code == 200:
    data = response.json()
    task_id = data.get('data', {}).get('task_id')
    status = data.get('data', {}).get('status')
    print(f'✅ Tarea creada!')
    print(f'📝 Task ID: {task_id}')
    print(f'📝 Estado: {status}')
    
    # 2. CONSULTAR ESTADO DE LA TAREA
    if task_id:
        print('\n🔍 Consultando estado del video...')
        time.sleep(3)  # Esperar 3 segundos
        
        url_status = f'https://api.klingai.com/v1/videos/generations/{task_id}'
        response_status = requests.get(url_status, headers=headers, timeout=30)
        print(f'📥 Código: {response_status.status_code}')
        
        if response_status.status_code == 200:
            data_status = response_status.json()
            status = data_status.get('data', {}).get('status')
            print(f'📊 Estado actual: {status}')
            
            if status == 'completed':
                video_url = data_status.get('data', {}).get('video_url')
                print(f'🎬 Video generado: {video_url}')
            elif status == 'processing':
                print('⏳ El video está en procesamiento. Espera unos segundos...')
            else:
                print(f'📄 Detalles: {json.dumps(data_status, indent=2)[:500]}')
        else:
            print(f'❌ Error consultando: {response_status.text[:200]}')
            
elif response.status_code == 401:
    print('❌ Clave inválida o sin permisos')
elif response.status_code == 402:
    print('⚠️ Saldo insuficiente (necesitas créditos)')
else:
    print(f'❌ Error: {response.text[:500]}')