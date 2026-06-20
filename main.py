import os
import asyncio
import threading
from telethon import TelegramClient, events
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Configuración
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    server.serve_forever()

client = TelegramClient('cyber_session_v3', API_ID, API_HASH)

# Handler super simple: si recibe ALGO, responde "Hola"
@client.on(events.NewMessage)
async def handler(event):
    print(f"DEBUG: Mensaje recibido: '{event.text}'")
    await event.respond("¡Hola! El bot está escuchando.")

async def main():
    print("Iniciando bot...")
    await client.start(bot_token=BOT_TOKEN)
    print("Bot conectado.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    asyncio.run(main())
