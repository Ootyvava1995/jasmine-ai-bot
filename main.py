import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

# Create Gemini Client
client = genai.Client(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Sanju! I am Jasmine. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_text,
        )
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("I couldn't generate a response. Please try again.")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please check again later.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
