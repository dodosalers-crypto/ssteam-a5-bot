import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

OWNER_ID = 123456789  # apni telegram id yaha likho

approved_users = set()
pending_users = {}


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    if user_id in approved_users:
        await update.message.reply_text(
"""
🚀 *WELCOME*

Your account is *approved*.

Just send your *Serial Number* directly to register.
""",
parse_mode="Markdown"
        )
        return

    pending_users[user_id] = username

    await update.message.reply_text(
"""
━━━━━━━━━━━━━━━━━━
🔒 *ACCESS PENDING*
━━━━━━━━━━━━━━━━━━

Your account is waiting for *Admin Approval*.

📩 Contact Owner
@ilcapo_7

Once approved you can register unlimited serials.
""",
parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"""
🚨 *NEW USER REQUEST*

👤 Username: @{username}
🆔 User ID: `{user_id}`

Approve with:
/approve_user {user_id}
""",
parse_mode="Markdown"
    )


# SERIAL MESSAGE HANDLER
async def serial_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    serial = update.message.text.strip()

    if user_id not in approved_users:

        await update.message.reply_text(
"""
⛔ *ACCESS DENIED*

Your account is not approved yet.

Contact owner:
@ilcapo_7
""",
parse_mode="Markdown"
        )
        return

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
f"""
✅ *SERIAL REGISTERED*

━━━━━━━━━━━━━━━━━━
🔑 Serial:
`{serial}`
━━━━━━━━━━━━━━━━━━

Activation Successful.
""",
parse_mode="Markdown"
            )

        elif response.status_code == 400:

            await update.message.reply_text(
f"""
⚠️ *DUPLICATE SERIAL*

Serial already registered:

`{serial}`
""",
parse_mode="Markdown"
            )

        else:

            await update.message.reply_text(
"❌ Registration failed.",
parse_mode="Markdown"
            )

    except:

        await update.message.reply_text(
"⚠️ Server error occurred.",
parse_mode="Markdown"
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
        text="""
🎉 *ACCESS APPROVED*

You can now send *Serial Numbers* directly to register.
""",
        parse_mode="Markdown"
    )

    await update.message.reply_text("✅ User Approved")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve_user", approve_user))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, serial_handler))

app.run_polling(drop_pending_updates=True)
