import asyncio
import os
import uvicorn
from fastapi import FastAPI

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# =================== TOKEN VA GROUP ===================
BOT_TOKEN = "8751707134:AAHFwvBfKtkxk3lKom8uWYoCjonx-TKVCFc"  # <--- bu yerga tokeningizni qo'ying
GROUP_ID = -1003219123503         # <--- guruh ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

waiting_users = set()
sent_message_map = {}  # message_id -> user_id


# =================== START / MENU ===================
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Bizning jamoa", url="https://t.me/TeleFluss")],
            [InlineKeyboardButton(text="📩 Adminlarga murojaat", callback_data="admin")]
        ]
    )
    await message.answer(
        "Assalomu alaykum!\n\nBizning botga xush kelibsiz.",
        reply_markup=keyboard
    )


# =================== ADMIN TUGMASI ===================
@dp.callback_query(lambda c: c.data == "admin")
async def admin_handler(callback: types.CallbackQuery):
    waiting_users.add(callback.from_user.id)
    await callback.message.answer("✍️ Savolingizni yuboring:")
    await callback.answer()


# =================== FOYDALANUVCHI SAVOLI ===================
@dp.message()
async def user_question(message: types.Message):
    if message.from_user.id in waiting_users:
        waiting_users.remove(message.from_user.id)

        username = message.from_user.username or "NoUsername"
        user_id = message.from_user.id
        question = message.text or "—"

        # Murojaatni guruhga yuborish
        sent = await bot.send_message(
            GROUP_ID,
            f"📩 Yangi murojaat\n\n👤 @{username}\n🆔 {user_id}\n\n❓ Savol:\n{question}"
        )

        # reply uchun map ga qo‘shish
        sent_message_map[sent.message_id] = user_id

        await message.answer("✅ Savolingiz yuborildi.")


# =================== ADMIN REPLY ===================
@dp.message()
async def admin_reply(message: types.Message):
    # Faqat guruhdagi reply xabarlarni tekshirish
    if message.chat.id == GROUP_ID and message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        if replied_id in sent_message_map:
            user_id = sent_message_map[replied_id]

            # Matn yuborish
            if message.text:
                await bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")

            # Rasm yuborish
            if message.photo:
                await bot.send_photo(
                    user_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption
                )

            # Fayl yuborish
            if message.document:
                await bot.send_document(
                    user_id,
                    document=message.document.file_id,
                    caption=message.caption
                )


# =================== FASTAPI START ===================
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))


@app.get("/")
async def home():
    return {"status": "Bot ishlayapti"}


# =================== RUN ===================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)# =================== ADMIN TUGMASI ===================
@dp.callback_query(lambda c: c.data == "admin")
async def admin_handler(callback: types.CallbackQuery):
    waiting_users.add(callback.from_user.id)
    await callback.message.answer("✍️ Savolingizni yuboring:")
    await callback.answer()


# =================== FOYDALANUVCHI SAVOLI ===================
@dp.message()
async def user_question(message: types.Message):
    if message.from_user.id in waiting_users:
        waiting_users.remove(message.from_user.id)

        username = message.from_user.username or "NoUsername"
        user_id = message.from_user.id
        question = message.text or "—"

        # Murojaatni guruhga yuborish
        sent = await bot.send_message(
            GROUP_ID,
            f"📩 Yangi murojaat\n\n👤 @{username}\n🆔 {user_id}\n\n❓ Savol:\n{question}"
        )

        # reply uchun map ga qo‘shish
        sent_message_map[sent.message_id] = user_id

        await message.answer("✅ Savolingiz yuborildi.")


# =================== ADMIN REPLY ===================
@dp.message()
async def admin_reply(message: types.Message):
    # Faqat guruhdagi reply xabarlarni tekshirish
    if message.chat.id == GROUP_ID and message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        if replied_id in sent_message_map:
            user_id = sent_message_map[replied_id]

            # Matn, rasm va faylni foydalanuvchiga yuborish
            if message.text:
                await bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")

            if message.photo:
                await bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)

            if message.document:
                await bot.send_document(user_id, document=message.document.file_id, caption=message.caption)


# =================== FASTAPI START ===================
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))


@app.get("/")
async def home():
    return {"status": "Bot ishlayapti"}


# =================== RUN ===================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
# =================== FOYDALANUVCHI SAVOLI ===================
@dp.message()
async def user_question(message: types.Message):
    if message.from_user.id in waiting_users:
        waiting_users.remove(message.from_user.id)

        username = message.from_user.username or "NoUsername"
        user_id = message.from_user.id
        question = message.text or "—"

        # Murojaatni guruhga yuborish
        sent = await bot.send_message(
            GROUP_ID,
            f"📩 Yangi murojaat\n\n👤 @{username}\n🆔 {user_id}\n\n❓ Savol:\n{question}"
        )

        # reply uchun map ga qo‘shish
        sent_message_map[sent.message_id] = user_id

        await message.answer("✅ Savolingiz yuborildi.")


# =================== ADMIN REPLY ===================
@dp.message()
async def admin_reply(message: types.Message):
    # Faqat guruhdagi reply xabarlarni tekshirish
    if message.chat.id == GROUP_ID and message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        if replied_id in sent_message_map:
            user_id = sent_message_map[replied_id]

            # Matn, rasm va faylni foydalanuvchiga yuborish
            if message.text:
                await bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")

            if message.photo:
                await bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)

            if message.document:
                await bot.send_document(user_id, document=message.document.file_id, caption=message.caption)


# =================== FASTAPI START ===================
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))


@app.get("/")
async def home():
    return {"status": "Bot ishlayapti"}


# =================== RUN ===================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)        username = message.from_user.username
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


@dp.message(F.reply_to_message)
async def admin_reply(message: types.Message):
    replied = message.reply_to_message.message_id
    if replied in sent_message_map:
        user_id = sent_message_map[replied]
        await bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")


# FastAPI startup
@app.on_event("startup")
async def on_startup():
    # Bu yerda await ishlamaydi, shuning uchun asyncio.create_task ishlatamiz
    asyncio.create_task(dp.start_polling(bot))


@app.get("/")
async def home():
    return {"status": "Bot ishlayapti"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
