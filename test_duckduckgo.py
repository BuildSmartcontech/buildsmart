import requests
import json

print('🔍 Probando DuckDuckGo con diferentes consultas...\n')

# Lista de consultas de prueba
consultas = [
    'construcción',
    'arquitectura',
    'noticias construcción 2026',
    'inteligencia artificial',
    'python tutorial'
]

for consulta in consultas:
    print(f'📌 Buscando: "{consulta}"')
    
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': consulta,
        'format': 'json',
        'no_html': 1,
        'skip_disambig': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            heading = data.get('Heading', '')
            abstract = data.get('AbstractText', '')
            
            if abstract:
                print(f'   ✅ Resumen: {abstract[:100]}...')
            elif heading:
                print(f'   ✅ Heading: {heading}')
            else:
                print(f'   ⚠️ Sin resultados específicos')
        else:
            print(f'   ❌ Error {response.status_code}')
            
    except Exception as e:
        print(f'   ❌ Error: {str(e)[:50]}')
    
    print()

print('✅ Prueba completada.')