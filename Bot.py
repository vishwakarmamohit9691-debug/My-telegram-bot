import os
import subprocess
import re
import random
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- APNA TOKEN YAHAN DALEN ---
TOKEN = "8502751140:AAGcIoj6al-fv6BZBvSveHRg9g496Et_y9U"

# 1. Start & Help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Phoenix Pro Bot Active hai! 🔥\n\n"
        "🎮 **Games:** /guess, /dice\n"
        "🛡 **Admin:** /ban, /mute, /staff\n"
        "🆔 **Info:** /id"
    )

# 2. Game: Number Guessing
async def guess_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 10)
    context.chat_data['secret'] = number
    await update.message.reply_text("🎮 **Game Shuru!**\nMaine 1 se 10 ke beech ek number socha hai. Guess karo kya hai?")

# 3. Game: Dice Roll
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

# 4. ID Feature
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await update.message.reply_text(f"👤 Name: {target.first_name}\n🆔 ID: `{target.id}`", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"🆔 Aapki ID: `{update.effective_user.id}`", parse_mode='Markdown')

# 5. Security: Delete Links & Media
async def security_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Check if Admin
    member = await context.bot.get_chat_member(chat_id, user_id)
    if member.status in ['creator', 'administrator']:
        # Admin ke liye Guess Check logic
        await check_guess_logic(update, context)
        return

    # Anti-Link
    text = update.message.text or update.message.caption or ""
    if re.findall(r'(https?://\S+|www\.\S+)', text):
        await update.message.delete()
        return

    # Anti-Media (Nudes/Spam protection)
    if update.message.photo or update.message.video or update.message.animation:
        await update.message.delete()
        return
        
    # Guess check for normal users
    await check_guess_logic(update, context)

async def check_guess_logic(update, context):
    if 'secret' in context.chat_data and update.message.text:
        try:
            guess = int(update.message.text)
            if guess == context.chat_data['secret']:
                await update.message.reply_text(f"🥳 Waah! @{update.effective_user.username} ne sahi pehchana! Number {guess} tha.")
                del context.chat_data['secret']
        except ValueError:
            pass

# Main Application
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("guess", guess_game))
    app.add_handler(CommandHandler("dice", roll_dice))
    app.add_handler(CommandHandler("id", get_id))
    
    # Combined filter for Security and Games
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), security_filter))

    print("Bot is running with Games & Security...")
    subprocess.Popen(["python", "-m", "http.server", os.environ.get("PORT", "8080")])
    app.run_polling()
