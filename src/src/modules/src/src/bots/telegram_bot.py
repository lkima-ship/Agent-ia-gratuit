"""
Bot Telegram gratuit
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text(
        "🤖 Assistant IA Gratuit\n"
        "Je peux vous aider avec:\n"
        "/emails - Gérer emails\n"
        "/calendar - Rendez-vous\n"
        "/voice - Messages vocaux"
    )

async def handle_message(update: Update, context):
    await update.message.reply_text("Message reçu !")

def run_telegram_bot():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Token Telegram manquant.")
        print("👉 Obtenez-le sur: https://t.me/BotFather")
        return
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot Telegram démarré...")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
