import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# BOT TOKEN (Railway / Render me ENV variable use karo)
BOT_TOKEN = os.getenv("8577319519:AAHnaebOYVy_TdgJW1bJ73hma-5UG4wfG0E")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n\nSend me any direct download link and I will download the file and send it to you."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    try:
        await update.message.reply_text("⏳ Downloading file...")

        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        filename = url.split("/")[-1] or "file"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=10240):
                if chunk:
                    f.write(chunk)

        await update.message.reply_text("📤 Sending file...")
        await update.message.reply_document(document=open(filepath, "rb"))

        os.remove(filepath)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
