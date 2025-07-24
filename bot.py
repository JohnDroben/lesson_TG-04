# Задание 1: Создание простого меню с кнопками
# При отправке команды /start бот будет показывать меню с кнопками "Привет" и "Пока".
# При нажатии на кнопку "Привет" бот должен отвечать "Привет, {имя пользователя}!",
# а при нажатии на кнопку "Пока" бот должен отвечать "До свидания, {имя пользователя}!".
#
# Задание 2: Кнопки с URL-ссылками
# При отправке команды /links бот будет показывать инлайн-кнопки с URL-ссылками.
# Создайте три кнопки с ссылками на новости/музыку/видео
#
# Задание 3: Динамическое изменение клавиатуры
# При отправке команды /dynamic бот будет показывать инлайн-кнопку "Показать больше".
# При нажатии на эту кнопку бот должен заменять её на две новые кнопки "Опция 1" и "Опция 2".
# При нажатии на любую из этих кнопок бот должен отправлять сообщение с текстом выбранной опции.

import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import F
import asyncio



load_dotenv()

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()


# Задание 1: Простое меню с кнопками
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем клавиатуру с кнопками "Привет" и "Пока"
    buttons = [
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие:\\n /links - задание 2: кнопки с URL-ссылками \\n /dynamic - задание 3: динамическое изменение клавиатуры",
    )

    await message.answer(
        f"Привет, {message.from_user.full_name}!\n"
        "Для просмотра 1 задания нажмите кнопки \"Привет\" и \"Пока\".\n "
        "Для просмотра 2 и 3 заданий нажмите соответствующие команды:\n "
        "/links - задание 2: кнопки с URL-ссылками; \n "
        "/dynamic - задание 3: динамическое изменение клавиатуры.\n",
        reply_markup=keyboard
    )


# Обработчики для кнопок "Привет" и "Пока"
@dp.message(F.text == "Привет")
async def say_hello(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(F.text == "Пока")
async def say_goodbye(message: types.Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# Задание 2: Кнопки с URL-ссылками
@dp.message(Command("links"))
async def send_links(message: types.Message):
    # Создаем инлайн-клавиатуру с URL-кнопками
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Новости",
            url="https://news.yandex.ru/"
        ),
        InlineKeyboardButton(
            text="Музыка",
            url="https://music.yandex.ru/"
        ),
        InlineKeyboardButton(
            text="Видео",
            url="https://www.youtube.com/"
        )
    )
    # Распределяем кнопки по 2 в ряд
    builder.adjust(2, 1)

    await message.answer(
        "Выберите интересующую вас тему:",
        reply_markup=builder.as_markup()
    )


# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command("dynamic"))
async def dynamic_keyboard(message: types.Message):
    # Создаем инлайн-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Показать больше",
            callback_data="show_more"
        )
    )

    await message.answer(
        "Нажмите на кнопку, чтобы увидеть больше опций:",
        reply_markup=builder.as_markup()
    )


# Обработчик для callback-запросов
@dp.callback_query(F.data == "show_more")
async def show_more_options(callback: CallbackQuery):
    # Создаем новую клавиатуру с двумя кнопками
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Опция 1",
            callback_data="option_1"
        ),
        InlineKeyboardButton(
            text="Опция 2",
            callback_data="option_2"
        )
    )

    # Редактируем сообщение, заменяя клавиатуру
    await callback.message.edit_text(
        "Выберите опцию:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


# Обработчики для выбранных опций
@dp.callback_query(F.data.startswith("option_"))
async def handle_option(callback: CallbackQuery):
    option = callback.data.split("_")[1]
    await callback.message.answer(f"Вы выбрали: Опция {option}")
    await callback.answer()


# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))