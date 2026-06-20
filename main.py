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
    print(f"Servidor web iniciado en puerto {PORT}")
    server.serve_forever()

# --- LANZAR SERVIDOR EN HILO SEPARADO PRIMERO ---
threading.Thread(target=run_server, daemon=True).start()

# --- LÓGICA DEL BOT ---
client = TelegramClient('cyber_session_v5', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if event.sender_id != MI_ID:
        return
    await event.respond("✅ Bot operativo.")

async def main():
    print("--- INICIANDO BOT ---")
    await client.start(bot_token=BOT_TOKEN)
    print("--- BOT CONECTADO ---")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
