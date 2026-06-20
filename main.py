import os
import yt_dlp
import re
from telethon import TelegramClient, events

# Configuración básica
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
MI_ID = 6190912865 

# Inicialización del cliente
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Patrón para detectar links (https, http)
URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("✅ CyberGrabber activo. Pega un link para descargar.")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # 1. Seguridad: Solo responder si el mensaje viene de TI
    if event.sender_id != MI_ID:
        return

    # 2. Ignorar si es un comando o no tiene texto
    if not event.text or event.text.startswith('/'):
        return
    
    # 3. Solo procesar si contiene una URL
    url_match = URL_PATTERN.search(event.text)
    if not url_match:
        return

    url = url_match.group(0)
    status = await event.respond("⏳ Procesando descarga...")

    # Opciones de yt-dlp para máxima compatibilidad
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraer info y descargar
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Confirmar subida
        await status.edit("📤 Subiendo archivo a Telegram...")
        await client.send_file(event.chat_id, filename)
        
        # Limpieza de archivos
        if os.path.exists(filename):
            os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ Error en la descarga:\n`{str(e)}`")

print("Bot iniciado y escuchando solo nuevos mensajes...")
client.run_until_disconnected()
