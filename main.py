import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from deep_translator import GoogleTranslator

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Store user language preferences
user_languages = {}

# User sets language
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        lang = context.args[0].lower()
        user_languages[update.effective_user.id] = lang
        await update.message.reply_text(f"✅ Language set to {lang}")
    else:
        await update.message.reply_text("Usage: /setlang en")

# Add translate button to messages
async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Translate", callback_data="translate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
        "🌐",
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )

# Handle button click
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    target_lang = user_languages.get(user_id, "en")

    original_message = query.message.reply_to_message.text

    try:
        translated = GoogleTranslator(
            source="auto",
            target=target_lang
        ).translate(original_message)

        # Shows popup only to the person who clicked
        await query.answer(text=translated[:200], show_alert=True)

    except Exception:
        await query.answer(text="Translation error.", show_alert=True)




