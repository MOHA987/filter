import os
import telebot
from telebot import apihelper

# قراءة المتغيرات من Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN is not defined.")
if not SOURCE_CHANNEL or not TARGET_CHANNEL:
    raise Exception("❌ SOURCE_CHANNEL or TARGET_CHANNEL missing.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

print(f"🤖 Bot is running!\n📡 Listening from {SOURCE_CHANNEL}\n➡️ Forwarding to {TARGET_CHANNEL}")

def is_valid_message(text):
    return any(keyword in text for keyword in ["Liquidity", "Market Cap", "$", "Token"])

@bot.channel_post_handler(func=lambda m: True)
def handle_post(message):
    try:
        if message.chat.username == SOURCE_CHANNEL.replace("@", ""):
            text = message.text or ""
            if is_valid_message(text):
                bot.send_message(TARGET_CHANNEL, f"🚀 Filtered Message:\n\n{text}")
                print(f"✅ Forwarded: {text[:60]}...")
            else:
                print(f"⚠️ Ignored: {text[:60]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

print("🔄 Starting polling loop...")
while True:
    try:
        bot.polling(none_stop=True, skip_pending=True, interval=3)
    except Exception as e:
        print(f"⚠️ Polling error, retrying... {e}")
