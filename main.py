import os, asyncio, threading, yt_dlp, re, tempfile
from telethon import TelegramClient, events
from http.server import HTTPServer, SimpleHTTPRequestHandler

API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))
MI_ID = 6190912865

def run_server():
    HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.sender_id != MI_ID: return
    text = event.text.strip()
    
    if text == '/start':
        await event.respond("✅ CyberGrabber listo. Pega el link.")
        return

    match = re.search(r'https?://[^\s]+', text)
    if match:
        url = match.group(0).split('&list=')[0].split('&start_radio=')[0]
        status = await event.respond("⏳ CyberGrabber esta Procesando la descarga...")
        try:
            temp_path = os.path.join(tempfile.gettempdir(), 'video.mp4')
            with yt_dlp.YoutubeDL({'format': 'best[ext=mp4]/best', 'outtmpl': temp_path}) as ydl:
                ydl.download([url])
            await client.send_file(event.chat_id, temp_path)
            os.remove(temp_path)
            await status.delete()
        except Exception as e:
            await status.edit(f"❌ Error: {str(e)[:50]}")
    else:
        await event.respond("❓ Pega un link válido o usa /start.")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
