import os
import telebot
from telebot import types

# ✅ قراءة المتغيرات من Environment Variables في Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

# 🔒 فحص إذا المتغيرات ناقصة
if not BOT_TOKEN:
    raise Exception("❌ Bot token is not defined in environment variables.")
if not SOURCE_CHANNEL or not TARGET_CHANNEL:
    raise Exception("❌ SOURCE_CHANNEL or TARGET_CHANNEL is missing in environment variables.")

# ✅ تهيئة البوت
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

print(f"🤖 Bot connected successfully!\n📡 Listening from {SOURCE_CHANNEL}\n➡️ Forwarding to {TARGET_CHANNEL}")

# ✅ دالة الفلترة – يمكن تعديلها لاحقًا حسب شروطك
def is_valid_message(text):
    if "Liquidity" in text or "Market Cap" in text:
        return True
    return False

# ✅ استماع للرسائل الجديدة
@bot.channel_post_handler(func=lambda message: True)
def forward_message(message):
    try:
        if message.chat.username == SOURCE_CHANNEL.replace("@", ""):
            text = message.text or ""
            if is_valid_message(text):
                bot.send_message(TARGET_CHANNEL, f"🚀 Filtered Message:\n\n{text}")
                print(f"✅ Forwarded message: {text[:50]}...")
            else:
                print(f"⚠️ Message ignored: {text[:50]}...")
    except Exception as e:
        print(f"❌ Error forwarding message: {e}")

# ✅ تشغيل البوت
print("🔄 Bot is now running...")
bot.infinity_polling(skip_pending=True)
