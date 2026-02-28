import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Format check
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ Wrong format\n\n"
            "✅ Use:\n"
            "/register SERIALNUMBER\n\n"
            "Example:\n"
            "/register C39X69ZAKPHF"
        )
        return

    serial = context.args[0].strip()

    try:
        response = requests.post(
            f"{API_URL}/api/register",
            json={
                "serial": serial,
                "telegram_id": update.effective_user.id
            }
        )

        data = response.json()

        # Already registered case
        if response.status_code == 400:
            await update.message.reply_text(
                f"⚠️ Serial Already Registered\n\n{serial}"
            )
            return

        # Success case
        if response.status_code == 200:
            await update.message.reply_text(
                f"✅ Serial Registered Successfully\n\n{serial}"
            )
        else:
            await update.message.reply_text("❌ Registration Failed")

    except Exception:
        await update.message.reply_text("⚠️ Server Error")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("register", register))
app.run_polling()

app.run_polling(drop_pending_updates=True)
