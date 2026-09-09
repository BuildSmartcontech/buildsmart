import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if not url or not key:
    print('❌ SUPABASE_URL o SUPABASE_KEY no encontradas')
    exit()

print(f'🔗 URL: {url}')
print(f'🔑 Key: {key[:20]}...')

headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}'
}

try:
    response = requests.get(f'{url}/rest/v1/', headers=headers, timeout=10)
    print(f'📥 Código: {response.status_code}')
    
    if response.status_code == 200:
        print('✅ Supabase responde correctamente!')
        print(f'📝 Content-Type: {response.headers.get("content-type", "desconocido")}')
    elif response.status_code == 401:
        print('❌ Error de autenticación. Verifica la clave.')
    else:
        print(f'⚠️ Respuesta: {response.text[:200]}')
        
except Exception as e:
    print(f'❌ Error: {str(e)[:100]}')