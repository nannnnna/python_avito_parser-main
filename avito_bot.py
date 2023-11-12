from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from proba_avito import category_elements

API_TOKEN = '6778465972:AAFIKWomH0GfWS5RWO_WW7ffwQsnI4Ilvsc'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def load_categories():
    categories = {}
    with open('categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if ': ' in line:
                key, value = line.strip().split(': ', 1)
                categories[key] = value
    return categories


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Создание кнопок
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Категории"))
    markup.add(KeyboardButton("Начать сначала"))
    markup.add(KeyboardButton("Назад"))

    # Отправка сообщения
    await message.reply("Привет! Что бы вы хотели сделать?", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Категории")
async def show_categories(message: types.Message):
    categories = load_categories()

    inline_markup = InlineKeyboardMarkup()
    for category in categories.keys():
        inline_markup.add(InlineKeyboardButton(category, callback_data=f"category_{category}"))

    await message.reply("Выберите категорию:", reply_markup=inline_markup)


@dp.message_handler(lambda message: message.text == "Начать сначала")
async def start_again(message: types.Message):
    await send_welcome(message)

@dp.message_handler(lambda message: message.text == "Назад")
async def go_back(message: types.Message):
    # Логика для возвращения на шаг назад
    await message.reply("Вы вернулись на шаг назад.")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('category_'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    category = callback_query.data[len('category_'):]
    await bot.answer_callback_query(callback_query.id)

    # Сохранение выбранной категории
    with open(f'{callback_query.from_user.id}_category.txt', 'w', encoding='utf-8') as file:
        file.write(category)

    # Запрос ввода местоположения
    await bot.send_message(callback_query.from_user.id, 
                           f'Вы выбрали категорию: {category}. Теперь введите ваше местоположение.')


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    user_location = message.location
    user_id = message.from_user.id

    # Загрузка сохраненной категории
    with open(f'{user_id}_category.txt', 'r', encoding='utf-8') as file:
        category = file.read()

    categories = load_categories()
    category_url = categories.get(category, "https://www.avito.ru")

    # Генерация URL с локацией
    location_based_url = category_url.replace('all', f'{user_location.latitude},{user_location.longitude}')

    await message.reply(f"URL для категории '{category}' и вашего местоположения: {location_based_url}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)