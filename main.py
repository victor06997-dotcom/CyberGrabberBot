import os
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from database import init_db, is_authorized

TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
ADMIN_ID = 6190912865

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id) or user_id == ADMIN_ID:
        await update.message.reply_text("¡CyberGrabber activo! ⚡ Pega el link.")
    else:
        await update.message.reply_text("Acceso denegado.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not (is_authorized(user_id) or user_id == ADMIN_ID):
        return

    url = update.message.text
    context.user_data['url'] = url
    
    keyboard = [
        [InlineKeyboardButton("🔊 Solo Audio (MP3)", callback_data='audio')],
        [InlineKeyboardButton("🎥 Video Alta Calidad (MP4)", callback_data='video')]
    ]
    await update.message.reply_text("¿Qué formato prefieres?", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    url = context.user_data.get('url')
    
    await query.edit_message_text("Procesando en servidores... ⏳")
    
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Origin": "https://cobalt.tools",
        "Referer": "https://cobalt.tools/"
    }
    
    payload = {
        "url": url,
        "aFormat": "mp3" if query.data == 'audio' else None,
        "vCodec": "h264" if query.data == 'video' else None,
        "vQuality": "max" if query.data == 'video' else None,
        "disableMetadata": True
    }

    async with aiohttp.ClientSession() as session:
        try:
            # Usando una instancia de espejo más permisiva
            async with session.post("https://cobalt.api.proximite.dev/api/json", 
                                    json=payload, 
                                    headers=headers, 
                                    allow_redirects=True) as resp:
                
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("status") == "success":
                        file_url = data["url"]
                        if query.data == 'audio':
                            await query.message.reply_audio(audio=file_url)
                        else:
                            await query.message.reply_video(video=file_url)
                        await query.message.delete()
                    else:
                        await query.message.reply_text(f"Error de Cobalt: {data.get('text', 'No se pudo procesar')}")
                else:
                    await query.message.reply_text(f"Error de servidor ({resp.status}). Intenta otra instancia.")
        except Exception as e:
            await query.message.reply_text(f"Error de conexión: {str(e)}")

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    app.run_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"{WEBHOOK_URL}/{TOKEN}")
