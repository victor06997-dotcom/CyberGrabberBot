import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import init_db, is_authorized, add_user

# Configuración del Bot
TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") # Ejemplo: https://tu-bot.onrender.com/
ADMIN_ID = 6190912865

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id) or user_id == ADMIN_ID:
        await update.message.reply_text("¡CyberGrabber activo! ⚡ Pega el link.")
    else:
        await update.message.reply_text("Acceso denegado.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not (is_authorized(user_id) or user_id == ADMIN_ID):
        return

    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        return 

    await update.message.reply_text("Procesando... ⏳")
    
    # Ruta absoluta
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
        'outtmpl': 'temp_audio.mp3',
        'cookiefile': cookie_path,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists('temp_audio.mp3'):
            await update.message.reply_audio(audio=open('temp_audio.mp3', 'rb'))
            os.remove('temp_audio.mp3')
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    
    # Usamos Webhook para que Render no se quede "cargando"
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
