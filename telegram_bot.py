import os
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def notify_pending(bot_name: str, filepath: str):
    """
    Sends a Telegram message to the admin for each pending post,
    allowing approval or rejection.
    """
    filename = os.path.basename(filepath)
    text = f"🆕 New post ready for *{bot_name}*:\n`{filename}`"

    keyboard = [
        [
            InlineKeyboardButton("✅ Publish", callback_data=f"publish|{bot_name}|{filename}"),
            InlineKeyboardButton("🗑 Reject", callback_data=f"reject|{bot_name}|{filename}")
        ]
    ]

    bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def handle_callback(update: Update, context: CallbackContext):
    """
    Handles Telegram button presses.
    """
    query = update.callback_query
    action, bot_name, filename = query.data.split("|")
    src_path = os.path.join("pending", bot_name, filename)
    dst_path = os.path.join("output", bot_name, filename)

    if action == "publish":
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.move(src_path, dst_path)
        bot.send_message(ADMIN_CHAT_ID, f"✅ Published: `{dst_path}`", parse_mode="Markdown")
    elif action == "reject":
        os.remove(src_path)
        bot.send_message(ADMIN_CHAT_ID, f"🗑 Rejected: `{filename}`", parse_mode="Markdown")
    query.answer()

def start_telegram_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    start_telegram_bot()
