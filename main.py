import asyncio
import logging
from models import User, add_user, startup
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command


bot = Bot(token='bot token')  # users token add new users
bot_username: str = "bot_username"
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    referred_by_code = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
    user = await User.get_or_none(user_id=message.from_user.id)

    if not user:
        await add_user(user_id=message.from_user.id, referred_by_code=referred_by_code)
        await message.answer("Welcome! You have been successfully registered.")
    else:
        await message.answer("You are already registered.")


@dp.message(Command("ref"))
async def my_referral(message: types.Message):
    user = await User.get_or_none(user_id=message.from_user.id)

    if not user:
        await message.answer("You are not registered. Please start the bot using /start.")
    else:
        referral_link = f"https://t.me/{bot_username}?start={user.referral_code}"
        if user.referral_count > 0:
            await message.answer(
                f"Your referral link: {referral_link}\n"
                f"Number of people referred: {user.referral_count}"
            )
        else:
            await message.answer(
                f"Your referral link: {referral_link}\n"
                f"No one has used your referral link yet."
            )


async def main():
    await startup()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
