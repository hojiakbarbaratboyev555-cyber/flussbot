import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberStatus

BOT_TOKEN = "8751707134:AAFoJo0a8swieJWbRQcos3vB7bOA4r9BkM0"
GROUP_ID = -1003219123503
CHANNEL = "@TeleFluss"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()

user_messages = {}

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@dp.message(Command("start"))
async def start(message: types.Message):

    if not await check_sub(message.from_user.id):
        await message.answer(f"Kanalga obuna bo'ling:\n{CHANNEL}")
        return

    await message.answer(
        "Murojaat yuborish:\n\n"
        "/murojaat sizning xabaringiz"
    )


@dp.message(Command("murojaat"))
async def murojaat(message: types.Message):

    if not await check_sub(message.from_user.id):
        await message.answer(f"Kanalga obuna bo'ling:\n{CHANNEL}")
        return

    text = message.text.replace("/murojaat", "").strip()

    if text == "":
        await message.answer("Murojaat yozing.")
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "yo'q"

    msg = (
        "📩 Yangi murojaat\n\n"
        f"👤 {user.first_name}\n"
        f"🆔 {user.id}\n"
        f"🔗 {username}\n\n"
        f"{text}"
    )

    sent = await bot.send_message(GROUP_ID, msg)

    user_messages[sent.message_id] = user.id

    await message.answer("Murojaatingiz yuborildi.")


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
            f"Admin javobi:\n\n{message.text}"
        )


@app.get("/")
async def root():
    return {"status": "ok"}


@app.on_event("startup")
async def start_bot():
    asyncio.create_task(dp.start_polling(bot))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
