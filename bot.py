import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Railway se environment variable milega
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

# ===== REGISTER COMMAND =====
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Sirf group me kaam kare
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ Use this command inside group.")
        return

    # Agar serial nahi diya
    if len(context.args) == 0:
        await update.message.reply_text("Usage:\n/register SERIAL")
        return

    serial = context.args[0].strip()

    try:
        response = requests.post(
            API_URL + "/api/register",
            json={"serial": serial},
            timeout=10
        )

        data = response.json()

        if data.get("success"):
            await update.message.reply_text(f"✅ Serial {serial} Registered Successfully")
        else:
            await update.message.reply_text("⚠️ Error Registering Serial")

    except Exception as e:
        await update.message.reply_text("❌ Server Connection Failed")


# ===== BOT START =====
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("register", register))

print("SSTEAM A5 Bot Running 🚀")
app.run_polling()
