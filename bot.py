import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

OWNER_ID = 6374332180  # apni telegram id yaha likho

approved_users = set()
pending_users = {}

# REGISTER COMMAND
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ Wrong format\n\n"
            "Use:\n/register SERIAL\n\n"
            "Example:\n/register C39X69ZAKPHF"
        )
        return

    serial = context.args[0].strip()
    user_id = update.effective_user.id
    username = update.effective_user.username

    # If user already approved
    if user_id in approved_users:

        try:
            response = requests.post(
                f"{API_URL}/api/register",
                json={
                    "serial": serial,
                    "telegram_id": user_id
                }
            )

            if response.status_code == 200:
                await update.message.reply_text(
                    f"✅ Serial Registered Successfully\n\n{serial}"
                )
            elif response.status_code == 400:
                await update.message.reply_text(
                    f"⚠️ Serial Already Registered\n\n{serial}"
                )
            else:
                await update.message.reply_text("❌ Registration Failed")

        except:
            await update.message.reply_text("⚠️ Server Error")

        return

    # If user not approved
    pending_users[user_id] = username

    await update.message.reply_text(
        "⏳ Your account is waiting for admin approval."
    )

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"""
📢 NEW USER APPROVAL REQUEST

User: @{username}
User ID: {user_id}

Approve:
/approve_user {user_id}
"""
    )


# APPROVE USER
async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text("Use: /approve_user USERID")
        return

    user_id = int(context.args[0])

    approved_users.add(user_id)

    if user_id in pending_users:
        del pending_users[user_id]

    await context.bot.send_message(
        chat_id=user_id,
        text="✅ Your account has been approved.\nNow you can register unlimited serials."
    )

    await update.message.reply_text("✅ User Approved")


# BOT START
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("register", register))
app.add_handler(CommandHandler("approve_user", approve_user))

app.run_polling(drop_pending_updates=True)
