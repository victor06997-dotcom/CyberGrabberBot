import os
import asyncio
from telethon import TelegramClient
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Configuración
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

# Servidor "fantasma" para que Render no cierre el bot
def run_server():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    server.serve_forever()

async def main():
    client = TelegramClient('bot_session', API_ID, API_HASH)
    print("Iniciando bot...")
    await client.start(bot_token=BOT_TOKEN)
    print("Bot conectado.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Lanzar servidor en segundo plano
    threading.Thread(target=run_server, daemon=True).start()
    # Lanzar el bot
    asyncio.run(main())
