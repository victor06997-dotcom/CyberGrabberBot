import os
import yt_dlp
from telethon import TelegramClient, events
import re

API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Regex para detectar si el texto contiene una URL real
URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🤖 **CyberGrabber Activo**\nEnvíame un link para descargar.")

@client.on(events.NewMessage)
async def downloader(event):
    # 1. Filtro: Solo responder a mensajes que tengan una URL
    if not event.text or not URL_PATTERN.search(event.text):
        return

    # 2. Filtro: Ignorar si el mensaje fue enviado por el bot mismo
    if event.sender_id == (await client.get_me()).id:
        return

    url = URL_PATTERN.search(event.text).group(0)
    status = await event.respond("🔍 Procesando link...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await status.edit("📤 Subiendo archivo...")
        await client.send_file(event.chat_id, filename)
        os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ Error al procesar:\n`{str(e)}`")

client.run_until_disconnected()
