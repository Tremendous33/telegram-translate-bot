import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator


logging.basicConfig(level=logging.INFO)

translator = Translator()
user_languages = {}

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_languages[update.effective_user.id] = context.args[0]
        await update.message.reply_text("Language set!")
    else:
        await update.message.reply_text("Usage: /setlang en")

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    for user_id, lang in user_languages.items():
        translated = translator.translate(message, dest=lang).text
        try:
            await context.bot.send_message(chat_id=user_id, text=translated)
        except:
            pass

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("setlang", set_language))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

app.run_polling()
