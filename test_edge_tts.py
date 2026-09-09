import edge_tts
import asyncio
import os

print('🚀 Probando Edge-TTS (Texto a voz)...\n')

async def test_tts():
    texto = "Hola, soy Edge TTS, un sistema de texto a voz gratuito."
    voz = "es-ES-ElviraNeural"  # Voz en español de España
    archivo = "test_edge_tts.mp3"
    
    print(f'📝 Texto: "{texto}"')
    print(f'🗣️ Voz: {voz}')
    
    try:
        communicate = edge_tts.Communicate(texto, voz)
        await communicate.save(archivo)
        
        print(f'✅ Audio generado correctamente: {archivo}')
        print(f'📁 Tamaño: {os.path.getsize(archivo)} bytes')
        
    except Exception as e:
        print(f'❌ Error: {str(e)}')

# Ejecutar la prueba
asyncio.run(test_tts())