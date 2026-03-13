import asyncio
import os
import uvicorn
from fastapi import FastAPI

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8751707134:AAFoJo0a8swieJWbRQcos3vB7bOA4r9BkM0"
GROUP_ID = -1003219123503

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

waiting_users = set()
sent_message_map = {}


# START
@dp.message(CommandStart())
async def start_handler(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Bizning jamoa", url="https://t.me/kanalingiz")],
            [InlineKeyboardButton(text="📩 Adminlarga murojaat", callback_data="admin")]
        ]
    )

    await message.answer(
        "Assalomu alaykum!\n\nBizning botga xush kelibsiz.",
        reply_markup=keyboard
    )


# ADMIN MUROJAAT
@dp.callback_query(F.data == "admin")
async def admin_handler(callback: types.CallbackQuery):

    waiting_users.add(callback.from_user.id)

    await callback.message.answer("✍️ Savolingizni yuboring:")
    await callback.answer()


# FOYDALANUVCHI SAVOLI
@dp.message()
async def user_question(message: types.Message):

    if message.from_user.id in waiting_users:

        waiting_users.remove(message.from_user.id)

        username = message.from_user.username
        user_id = message.from_user.id
        question = message.text

        text = f"""
📩 Yangi murojaat

👤 Username: @{username}
🆔 ID: {user_id}

❓ Savol:
{question}
"""

        sent = await bot.send_message(GROUP_ID, text)

        sent_message_map[sent.message_id] = user_id

        await message.answer("✅ Savolingiz yuborildi.")


# ADMIN JAVOBI
@dp.message(F.reply_to_message)
async def admin_reply(message: types.Message):

    replied = message.reply_to_message.message_id

    if replied in sent_message_map:

        user_id = sent_message_map[replied]

        await bot.send_message(
            user_id,
            f"📩 Admin javobi:\n\n{message.text}"
        )


# FASTAPI
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))


@app.get("/")
async def home():
    return {"status": "Bot ishlayapti"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    await callback.message.answer("✍️ Savolingizni yuboring:")
    await callback.answer()


# FOYDALANUVCHI SAVOLI
@dp.message()
async def user_question(message: types.Message):

    if message.from_user.id in waiting_users:

        waiting_users.remove(message.from_user.id)

        username = message.from_user.username
        user_id = message.from_user.id
        question = message.text

        text = f"""
📩 Yangi murojaat

👤 Username: @{username}
🆔 ID: {user_id}

❓ Savol:
{question}
"""

        sent = await bot.send_message(GROUP_ID, text)

        # foydalanuvchi ID ni saqlash
        sent_message_map[sent.message_id] = user_id

        await message.answer("✅ Savolingiz yuborildi.")


sent_message_map = {}


# GURUHDA REPLY QILINGAN JAVOB
@dp.message(F.reply_to_message)
async def admin_reply(message: types.Message):

    replied = message.reply_to_message.message_id

    if replied in sent_message_map:

        user_id = sent_message_map[replied]

        await bot.send_message(
            user_id,
            f"📩 Admin javobi:\n\n{message.text}"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


import asyncio
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
def home():
    return {"status": "Bot ishlayapti"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
