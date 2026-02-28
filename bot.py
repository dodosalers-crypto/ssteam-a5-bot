import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Usage:\n/register SERIAL")
        return

    serial = context.args[0]

    try:
        r = requests.post(
            API_URL,
            json={"serial": serial},
            headers={"Authorization": AUTH_TOKEN}
        )

        if r.status_code == 200 and r.json().get("success"):
            await update.message.reply_text(f"✅ {serial} Registered")
        else:
            await update.message.reply_text("⚠️ Failed or Already Exists")

    except:
        await update.message.reply_text("❌ Server Error")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("register", register))

print("Bot Running...")
app.run_polling()
