import requests
import json

api_key = 'api-key-kling-der_cHtSLR0JhVIBMrdHc_cd7jdzokdjzhdzpgUJi8g'

print('🚀 Probando NUEVA clave de Kling AI...')
print(f'🔑 Clave: {api_key[:25]}...')

# Endpoint correcto para generar videos
url = 'https://api.klingai.com/v1/videos/text-to-video'
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

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f'📥 Código de respuesta: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print('✅ Kling AI funciona correctamente!')
        print(f'📝 Task ID: {data.get("data", {}).get("task_id", "N/A")}')
        print(f'📝 Estado: {data.get("data", {}).get("status", "N/A")}')
        print(f'📝 Respuesta completa: {json.dumps(data, indent=2)[:500]}...')
    elif response.status_code == 401:
        print('❌ Clave inválida o sin permisos')
    elif response.status_code == 402:
        print('⚠️ Sin saldo (necesitas créditos)')
    else:
        print(f'❌ Error: {response.text[:500]}')
        
except Exception as e:
    print(f'❌ Error de conexión: {str(e)[:100]}')