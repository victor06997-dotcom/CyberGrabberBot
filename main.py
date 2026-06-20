import os
from telethon import TelegramClient, events

# Tus credenciales (las que sacamos de my.telegram.org)
API_ID = 35308373
API_HASH = 'b89737de4be9433f9c42f50ca7514097'
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Usamos el cliente para iniciar sesión. 
# Telethon gestiona la conexión de forma mucho más eficiente que los webhooks.
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    await event.respond("¡CyberGrabber activo y listo! Pega el link.")

# El bot ahora simplemente escucha. No se queda "cargando" porque no depende
# de un servidor web externo, sino de la conexión directa a Telegram.
print("Bot operando mediante el protocolo nativo de Telegram...")
client.run_until_disconnected()
