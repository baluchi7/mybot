import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "8558358164:AAE7OdhXomygrm93snr0wiPFlCh0qtDq6R4"

async def start(update: Update, context):
    await update.message.reply_text("سلام! لینک بفرست")

async def download_and_send(update: Update, context):
    url = update.message.text
    await update.message.reply_text("در حال دریافت فایل...")

    try:
        os.makedirs("downloads", exist_ok=True)
        ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as f:
            await update.message.reply_document(document=f, filename=os.path.basename(file_path))

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))

print("ربات روشن شد...")
app.run_polling()