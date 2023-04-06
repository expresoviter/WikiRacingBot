import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
import wikiracing
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
racer = wikiracing.WikiRacer()

mainKb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
helpBtn = types.KeyboardButton("Help...")
findBtn = types.KeyboardButton("Find your path!")
mainKb.add(helpBtn)
mainKb.add(findBtn)


class PathPages(StatesGroup):
    source = State()
    destination = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I`m Wikiracing Bot!\n"
                        "I'll help you to find path from one Wikipedia page to another through the links on the pages."),
    await message.reply("Just type /find",
                        reply_markup=mainKb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("The bot supports one functional command: /find\n"
                        "Type the command, then enter necessary info.\n"
                        "Then wait and you will receive info!")


@dp.message_handler(commands=['find'])
async def process_find_command(message: types.Message):
    await message.reply("Enter source page: ")
    await PathPages.source.set()


@dp.message_handler(lambda message: racer.request(message.text)[1] == -1, state=PathPages.destination)
async def process_invalid_destination(message: types.Message):
    return await message.reply("The page doesn`t exists.")


@dp.message_handler(lambda message: (racer.request(message.text)[0] == [] or racer.request(message.text)[1] == -1),
                    state=PathPages.source)
async def process_invalid_source(message: types.Message):
    return await message.reply("The page doesn`t exists or it doesn`t have links in it.")


@dp.message_handler(state=PathPages.source)
async def process_source(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['source'] = message.text

    await PathPages.next()
    await message.reply("Enter destination page: ")


@dp.message_handler(state=PathPages.destination)
async def process_source(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['destination'] = message.text

    await state.finish()
    path = racer.find_path(data["source"], data["destination"])
    text = "Your path: " + " -> ".join(path[0])
    text += "\nSearching time: " + str(path[1])
    await message.reply(text)


@dp.message_handler(lambda message: message.text in ["Help...", "Find your path!"])
async def processBtnAnswer(message: types.Message):
    if message.text == "Help...":
        await process_help_command(message)
    elif message.text == "Find your path!":
        await process_find_command(message)
    else:
        await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
