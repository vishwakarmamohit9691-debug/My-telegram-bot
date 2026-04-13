from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8502751140:AAFGLaPXmzDC8ON4ColkIdzu_1nspuqcxeM' # Apna token yahan phir se dalein

# /start command par buttons dikhane ke liye
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Channel 📢", url="https://t.me/your_channel"),
         InlineKeyboardButton("Support 💬", url="https://t.me/your_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Phoenix Bot mein aapka swagat hai! 🔥\nMain abhi active hoon.", 
        reply_markup=reply_markup
    )

# Jo bhi user likhega, bot wahi wapas bolega
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"Aapne kaha: {user_text}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    # 'filters.TEXT' se bot messages ko read kar payega
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    print("Bot fully active hai...")
    app.run_polling()
