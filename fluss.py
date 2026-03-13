# fluss.py
import os
import asyncio
import logging
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberStatus

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8751707134:AAFoJo0a8swieJWbRQcos3vB7bOA4r9BkM0"
GROUP_ID = -1003219123503
CHANNEL = "@TeleFluss"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()

# xabarlarni saqlash
user_messages = {}

# kanal obunasini tekshirish
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]
    except:
        return False

# start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if await check_sub(message.from_user.id):
        await message.answer(
            "Salom!\n\nMurojaat yuborish uchun:\n"
            "/murojaat sizning xabaringiz"
        )
    else:
        await message.answer(
            f"Botdan foydalanish uchun kanalga obuna bo'ling:\n{CHANNEL}"
        )

# murojaat yuborish
@dp.message(Command("murojaat"))
async def send_request(message: types.Message):

    if not await check_sub(message.from_user.id):
        await message.answer(f"Avval kanalga obuna bo'ling:\n{CHANNEL}")
        return

    user = message.from_user
    text = message.text.replace("/murojaat", "").strip()

    if text == "":
        await message.answer("Murojaat matnini yozing.")
        return

    username = f"@{user.username}" if user.username else "yo'q"

    msg = (
        "📩 Yangi murojaat\n\n"
        f"👤 Ism: {user.first_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: {username}\n\n"
        f"✉️ Xabar:\n{text}"
    )

    sent = await bot.send_message(GROUP_ID, msg)

    user_messages[sent.message_id] = user.id

    await message.answer("✅ Murojaatingiz yuborildi.")

# guruh reply javobi
@dp.message()
async def reply_handler(message: types.Message):

    if message.chat.id != GROUP_ID:
        return

    if not message.reply_to_message:
        return

    msg_id = message.reply_to_message.message_id

    if msg_id in user_messages:

        user_id = user_messages[msg_id]

        await bot.send_message(
            user_id,
            f"📬 Admin javobi:\n\n{message.text}"
        )

# FastAPI start
@app.on_event("startup")
async def start_bot():
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def home():
    return {"status": "bot ishlayapti"}

# Render port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("fluss:app", host="0.0.0.0", port=port)
