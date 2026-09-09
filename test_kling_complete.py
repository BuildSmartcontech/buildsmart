import requests
import json
import time

api_key = 'api-key-kling-zlmHebCx17W7fSE9_FFFRCMbtYpRGj3XyBp_Rzcfnjw'

print('🔍 DIAGNÓSTICO COMPLETO DE KLING AI')
print('=' * 50)
print(f'🔑 Clave: {api_key[:25]}...')

# Lista de endpoints a probar (ordenados por probabilidad)
endpoints = [
    'https://api.klingai.com/v1/videos/generation',
    'https://api.klingai.com/v1/videos/generations',
    'https://api.klingai.com/v1/videos/text-to-video',
    'https://api.klingai.com/v1/video/generations',
    'https://api.klingai.com/v1/video/text-to-video',
    'https://api.klingai.com/v1/generate/video',
    'https://api.klingai.com/v1/video-generation'
]

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'kling-v3',
    'prompt': 'A robot building a house',
    'duration': 5
}

print('\n📡 Probando endpoints...')
print('-' * 50)

for url in endpoints:
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f'📌 {url}')
        print(f'   📥 Código: {response.status_code}')
        
        if response.status_code == 200:
            print('   ✅ ENDPOINT ENCONTRADO!')
            data = response.json()
            print(f'   📝 Task ID: {data.get("data", {}).get("task_id", "N/A")}')
            print(f'   📝 Estado: {data.get("data", {}).get("status", "N/A")}')
            print('\n🎯 ¡Kling AI funciona correctamente!')
            break
        elif response.status_code == 401:
            print('   ❌ Clave inválida o sin permisos')
        elif response.status_code == 402:
            print('   💰 Sin saldo (necesitas créditos)')
        else:
            print(f'   ⚠️ Error: {response.text[:100]}')
        print()
        
    except Exception as e:
        print(f'   ❌ Error de conexión: {str(e)[:50]}')
        print()

print('=' * 50)
print('✅ Diagnóstico completado.')