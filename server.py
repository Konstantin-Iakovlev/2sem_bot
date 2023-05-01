"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random

import exceptions
import translations

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TRUE_ID = 0

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        text(
            bold("Бот для запоминания английских слов и выражений"), "\n\n"
            "Добавить слово: <english> <russian>\n"  # input
            "Последние слова: /last\n"  # output
            "Выучить случайное слово: /learn\n"  # input + output
        ),
        parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['last'])
async def last_translations(message: types.Message):
    """Предоставляет последние добавления"""
    last_tr = translations.last()
    answer_msg = "\n".join([f"{t.src} => {t.trg}" for t in last_tr])
    await message.answer(answer_msg)


@dp.message_handler(commands=['learn'])
async def learn_words(message: types.Message):
    last_trs = translations.last()
    selected_idx = random.randint(0, len(last_trs))
    global TRUE_ID
    TRUE_ID = random.randint(0, 1)
    markup = InlineKeyboardMarkup()
    for i in range(2):
        markup = markup.add(InlineKeyboardButton(
            text=last_trs[selected_idx if i == TRUE_ID else (
                selected_idx + 1) % len(last_trs)].trg,
            callback_data=f'button_{i}'))
    await message.answer(f"Переведи слово {last_trs[selected_idx].src}", reply_markup=markup)


@dp.callback_query_handler(text=[f'button_{i}' for i in range(2)])
async def trans_answer(call: types.CallbackQuery):
    await call.message.answer('Правильно!' if call.data.endswith(f'{TRUE_ID}') else 'Неверно!')
    await call.answer()


@dp.message_handler()
async def add_word_pair(message: types.Message):
    """Добавляет новую пару слов"""
    try:
        translation = translations.add_translation(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = text(
        "Добавлен перевод\n", italic(f"{translation.src}"), "=>", italic(f"{translation.trg}"), "\n\n")
    await message.answer(answer_message, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
