# fluss.py
from fastapi import FastAPI
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberStatus
import logging

logging.basicConfig(level=logging.INFO)

# --- Bot va guruh ma'lumotlari ---
BOT_TOKEN = "8751707134:AAFoJo0a8swieJWbRQcos3vB7bOA4r9BkM0"
TARGET_CHAT_ID = -1003219123503
CHANNEL_USERNAME = "@TeleFluss"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_messages = {}  # Guruh xabar ID -> foydalanuvchi ID

app = FastAPI()

# --- Kanal obuna tekshiruvi ---
async def check_subscription(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

# --- /start komandasi ---
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if await check_subscription(user_id):
        await message.answer(
            "Salom! Siz botdan foydalanishingiz mumkin.\n"
            "Murojaatingizni yuborish uchun /murojaat buyrug'ini ishlating."
        )
    else:
        await message.answer(
            f"⚠️ Botdan foydalanish uchun avval kanalimizga obuna bo'ling: {CHANNEL_USERNAME}\n"
            "Obuna bo'lgach /start buyrug'ini qayta yuboring."
        )

# --- /murojaat komandasi ---
@dp.message(Command("murojaat"))
async def handle_murojaat(message: types.Message):
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        await message.answer(f"⚠️ Avval kanalimizga obuna bo'ling: {CHANNEL_USERNAME}")
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "Yo'q"
    full_name = f"{user.first_name} {user.last_name or ''}".strip()
    murojaat_text = message.text.replace("/murojaat", "").strip() or "Yo'q matn"

    text_to_send = (
        f"📌 Murojaat:\n"
        f"👤 Ism: {full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: {username}\n\n"
        f"✉️ Murojaat matni: {murojaat_text}"
    )

    sent = await bot.send_message(chat_id=TARGET_CHAT_ID, text=text_to_send)
    user_messages[sent.message_id] = user.id

# --- Guruh reply orqali javob ---
@dp.message()
async def reply_from_group(message: types.Message):
    if message.chat.id != TARGET_CHAT_ID or not message.reply_to_message:
        return
    original_msg_id = message.reply_to_message.message_id
    if original_msg_id in user_messages:
        user_id = user_messages[original_msg_id]
        if message.text:
            await bot.send_message(chat_id=user_id, text=f"📬 Admin javobi:\n\n{message.text}")

# --- FastAPI startup ---
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def root():
    return {"status": "Bot ishlayapti"}

# --- Render porti bilan ishga tushirish ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fluss:app", host="0.0.0.0", port=8000)
