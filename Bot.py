import os
import subprocess
import re
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- APNA TOKEN YAHAN DALEN ---
TOKEN = "8502751140:AAFp61fB5hZLj6u8pWltvFiWgkf-7wAjkPY"

# 1. Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Phoenix Pro Bot Active hai! 🔥\nID nikalne ke liye /id use karein.")

# 2. User ID & Group ID nikalne ka feature
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if update.message.reply_to_message:
        # Agar kisi ke message par reply kiya hai
        target_user = update.message.reply_to_message.from_user
        await update.message.reply_text(
            f"👤 **User Info:**\n"
            f"Name: {target_user.first_name}\n"
            f"User ID: `{target_user.id}`\n"
            f"Group ID: `{chat_id}`",
            parse_mode='Markdown'
        )
    else:
        # Agar sirf /id likha hai
        user_id = update.effective_user.id
        await update.message.reply_text(
            f"🆔 **Aapki Info:**\n"
            f"User ID: `{user_id}`\n"
            f"Group ID: `{chat_id}`",
            parse_mode='Markdown'
        )

# 3. Staff/Admin List dekhne ke liye
async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await update.effective_chat.get_administrators()
    admin_list = "🛡 **Group Admins:**\n"
    for admin in admins:
        admin_list += f"• @{admin.user.username or admin.user.first_name}\n"
    await update.message.reply_text(admin_list)

# 4. Anti-Link (Pehle wala feature)
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    if member.status in ['creator', 'administrator']:
        return
    text = update.message.text or update.message.caption or ""
    if re.findall(r'(https?://\S+|www\.\S+)', text):
        await update.message.delete()
        await update.message.chat.send_message(f"🚫 @{update.effective_user.username}, Links allowed nahi hain!")

# 5. Media Filter (Nudes/Spam rokne ke liye)
async def filter_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    if member.status in ['creator', 'administrator']:
        return
    await update.message.delete()

# Main Application
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("staff", staff))
    
    # Filters
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.ANIMATION, filter_media))

    print("Bot is running with Advanced ID features...")
    
    # Render Workaround
    subprocess.Popen(["python", "-m", "http.server", os.environ.get("PORT", "8080")])
    
    app.run_polling()
