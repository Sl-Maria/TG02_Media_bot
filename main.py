import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
import os
import random
from googletrans import Translator, LANGUAGES

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(Command(commands='help'))
async def help(message: Message):
    await message.answer("/motiv - Мотивация дня \n/photo - Сохраню твою фотку")

@dp.message(Command(commands='motiv'))
async def motiv(message: Message):
    motiv_list = [
        "Успех — это не ключ к счастью. Но, эй, по крайней мере, ты можешь купить себе что-то красивое на пути к разочарованию!",
        "Помни: если ничего не поделать, мечты сами себя не разрушат. Так что лучше постарайся хоть немного!",
        "Не бойся быть уникальным. В худшем случае, ты всегда можешь сказать, что это был социальный эксперимент.",
        "Каждый день — это новая возможность всё испортить по-другому. Удачи!",
        "Никогда не сдавайся на пути к своим мечтам. Ведь потом можно будет сказать, что ты хотя бы попробовал!"
                  ]
    rand_motiv = random.choice(motiv_list)
    tts = gTTS(text=rand_motiv, lang='ru')
    file_name = 'audio/motivation_of_the_day.ogg'
    tts.save(file_name)
    audio = FSInputFile(file_name)
    await bot.send_voice(message.from_user.id, audio)
    os.remove(file_name)

@dp.message(F.photo)
async def photo(message: Message):
    await message.answer("Классная фотка, сохраню себе!")
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message()
async def common(message: Message):
    if translator.detect(message.text).lang == 'ru':
        translated_text = translator.translate(message.text, src='ru', dest='en').text
        await message.answer(translated_text)
    else:
        await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())