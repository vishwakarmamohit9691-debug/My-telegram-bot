import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Phoenix is ALIVE! 🔥")

def main():
    # APNA TOKEN YAHA DAALEIN
    TOKEN = "8502751140:AAEk1237snZo_tsc4eU4-kw1yKgfrY6NSdk"
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
