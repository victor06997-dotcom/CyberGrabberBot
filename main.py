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
# Expresión regular para detectar enlaces
URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.sender_id != MI_ID:
        return

    match = URL_PATTERN.search(event.text)
    if match:
        url = match.group(0)
        
        # FILTRO ESTRICTO: Solo procesar enlaces que parezcan videos
        if not any(x in url for x in ['watch?v=', 'shorts/', 'tiktok.com', 'instagram.com/reel/', 'youtu.be/']):
            await event.respond("❌ Por favor, envía un enlace directo a un video (ej: youtube.com/watch?v=...).")
            return

        status = await event.respond("⏳ Procesando descarga...")
        
        temp_dir = tempfile.gettempdir()
        # Usamos un template que fuerce el nombre para localizarlo fácilmente
        file_template = os.path.join(temp_dir, 'video_%(id)s.mp4')
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_template,
            'quiet': False 
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                final_path = ydl.prepare_filename(info)
            
            if os.path.exists(final_path):
                await status.edit("📤 Subiendo archivo...")
                await client.send_file(event.chat_id, final_path)
                os.remove(final_path)
                await status.delete()
            else:
                await status.edit("❌ Error: El archivo no se generó.")
        except Exception as e:
            print(f"ERROR: {str(e)}")
            await status.edit(f"❌ Error: {str(e)[:100]}")
    else:
        if event.text != '/start':
            await event.respond("Pega un link válido para descargar.")

async def main():
    print("Bot iniciando...")
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    asyncio.run(main())
