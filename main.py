import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import init_db, is_authorized, add_user

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 6190912865 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id) or user_id == ADMIN_ID:
        await update.message.reply_text("¡Bienvenido, CyberGrabber activo! ⚡ Pega el link.")
    else:
        await update.message.reply_text("Acceso denegado. Contacta al admin.")

async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        new_id = int(context.args[0])
        add_user(new_id)
        await update.message.reply_text(f"Usuario {new_id} autorizado correctamente.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (tu código de autorización se mantiene igual)

    url = update.message.text
    await update.message.reply_text("Procesando tu solicitud... ⏳")

    # AÑADE ESTOS PARÁMETROS NUEVOS:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
        'outtmpl': 'temp_audio.mp3',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await update.message.reply_audio(audio=open('temp_audio.mp3', 'rb'))
        os.remove('temp_audio.mp3')
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", authorize))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()
