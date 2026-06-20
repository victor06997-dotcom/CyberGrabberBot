import os
import yt_dlp
from telethon import TelegramClient, events

# Credenciales
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🤖 **CyberGrabber 2.0**\nEnvíame un link de TikTok, Reels, YouTube, FB o Spotify y lo procesaré.")

@client.on(events.NewMessage)
async def downloader(event):
    if not event.text or event.text.startswith('/'):
        return

    url = event.text
    status = await event.respond("🔍 Detectando plataforma y descargando...")

    # Configuración inteligente
    ydl_opts = {
        'format': 'best', # Descarga la mejor calidad disponible
        'outtmpl': 'downloaded_file.%(ext)s',
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # yt-dlp detecta automáticamente el sitio (FB, IG, TT, YT)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await status.edit("📤 Subiendo a Telegram...")
        await client.send_file(event.chat_id, filename)
        
        # Limpieza
        os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}\n\n(Es posible que el video sea privado o el link no sea compatible)")

print("Bot Multi-Plataforma activo...")
client.run_until_disconnected()
