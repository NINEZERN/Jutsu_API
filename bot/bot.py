from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api import Jutsu

API_TOKEN = '5806291416:AAH-IfIn79VThNjdFkkLS--xGRnXQbkPhMg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Напишите название аниме.")


@dp.message_handler()
async def echo(message: types.Message):
    jutsu = Jutsu()
    keyboard = InlineKeyboardMarkup()
    animes = jutsu.search(message.text)
    print("fuck")
    await message.reply("Пожалуйста подождите...")
    if animes:
        for anime in animes:
            # создаю клавиатуру с кнопочками аниме calbaack - ссылка
            keyboard.add(InlineKeyboardButton(anime.title, callback_data=anime.link))
            print(anime.title + " " + anime.link + "" + str(anime.get_seasons()))
        return await message.answer("Аниме найденные по вашему запросу:", reply_markup=keyboard)
    else:
        return await message.answer("Аниме не найдено!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
