import os
import random
import threading
import sqlite3
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- WEB SERVER FOR RENDER ---
server = Flask(__name__)
@server.route('/')
def home(): return "Phoenix Bot is Alive!"
def run_flask():
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# --- CONFIGURATION ---
TOKEN = '8502751140:AAEAF9JhXkE2amrbZlWK7F07-A7NaIJmG2M'
OWNER_ID = 8440797644# Apni ID yahan daalein
BAD_WORDS = ["gaali1", "gaali2"] 
STICKER_LIST = ['https://t.me/addstickers/JPS_Nachonekodayo'] # Sticker IDs yahan daalein

# --- FONT DICTIONARY ---
FONTS = {
    "bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "italic": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛",
    "mono": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚀𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
    "script": "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
}
NORMAL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def format_text(text, style):
    if style not in FONTS: return text
    table = str.maketrans(NORMAL_CHARS, FONTS[style])
    return text.translate(table)

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('phoenix.db')
    conn.execute('CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY)')
    conn.execute('CREATE TABLE IF NOT EXISTS gban (user_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()

# --- HANDLERS ---

# 1. Font Style Command
async def style_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /style [text]")
        return
    input_text = " ".join(context.args)
    res = f"✨ **Stylish Fonts:**\n\n"
    res += f"**Bold:** `{format_text(input_text, 'bold')}`\n"
    res += f"**Italic:** `{format_text(input_text, 'italic')}`\n"
    res += f"**Mono:** `{format_text(input_text, 'mono')}`\n"
    res += f"**Script:** `{format_text(input_text, 'script')}`"
    await update.message.reply_text(res, parse_mode='Markdown')

# 2. Staff Command
async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admins = await context.bot.get_chat_administrators(chat_id)
    owner, co_owner, normal = [], [], []
    for admin in admins:
        name = admin.user.first_name
        if admin.status == "creator": owner.append(name)
        elif admin.custom_title and "co-owner" in admin.custom_title.lower(): co_owner.append(name)
        else: normal.append(name)
    
    msg = f"👑 **Owner:** {', '.join(owner)}\n🥈 **Co-Owners:** {', '.join(co_owner)}\n👮 **Admins:** {', '.join(normal)}"
    await update.message.reply_text(msg)

# 3. Welcome & Captcha
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for m in update.message.new_chat_members:
        if m.is_bot: continue
        btn = [[InlineKeyboardButton
