import os
import yt_dlp
import re
import asyncio
from telethon import TelegramClient, events

# Configuración
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
MI_ID = 6190912865 

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("✅ CyberGrabber activo. Pega un link.")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.sender_id != MI_ID or not URL_PATTERN.search(event.text):
        return

    url = URL_PATTERN.search(event.text).group(0)
    status = await event.respond("⏳ Procesando...")

    # Forzamos formato mp4 y evitamos extensiones desconocidas
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.mp4', 
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        filename = 'video.mp4'
        
        # Pausa de seguridad: esperar a que el archivo exista y esté completo
        await asyncio.sleep(2) 
        
        if os.path.exists(filename):
            await status.edit("📤 Subiendo...")
            await client.send_file(event.chat_id, filename)
            os.remove(filename)
            await status.delete()
        else:
            raise Exception("El archivo no se generó correctamente.")
        
    except Exception as e:
        await status.edit(f"❌ Error: `{str(e)}`")

client.run_until_disconnected()
