import os
import asyncio
import threading
import yt_dlp
import re
import tempfile
from telethon import TelegramClient, events
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Configuración
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))
MI_ID = 6190912865 

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    server.serve_forever()

client = TelegramClient('cyber_session_v4', API_ID, API_HASH)
URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Procesar solo si eres tú
    if event.sender_id != MI_ID:
        return

    # Si es un link, lo descarga
    match = URL_PATTERN.search(event.text)
    if match:
        url = match.group(0)
        status = await event.respond("⏳ Procesando descarga...")
        
        # Usamos /tmp para asegurar permisos de escritura
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, 'video.mp4')
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'quiet': False # Cambiado a False para ver errores en los logs de Render
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(file_path):
                await status.edit("📤 Subiendo archivo...")
                await client.send_file(event.chat_id, file_path)
                os.remove(file_path)
                await status.delete()
            else:
                await status.edit("❌ Error: El archivo no se generó.")
        except Exception as e:
            print(f"ERROR: {str(e)}") # Esto es vital: mira los logs de Render si falla
            await status.edit(f"❌ Error: {str(e)[:100]}")
    else:
        # Solo responde si no es un link para no saturar
        if event.text != '/start':
            await event.respond("Pega un link válido para descargar.")

async def main():
    print("Bot iniciando...")
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Iniciar servidor web en hilo separado
    threading.Thread(target=run_server, daemon=True).start()
    # Iniciar el bot
    asyncio.run(main())
