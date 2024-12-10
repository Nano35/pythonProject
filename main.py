import sqlite3
import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.get_api_key())
conn = sqlite3.connect('db/python.db', check_same_thread=False)
cursor = conn.cursor()

@bot.message_handler(commands=['start']) #команды
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Я бот фонда: "Измени Одну Жизнь"
Я здесь чтобы помочь приемным родителям собрать всю информацию о прошлом их приемного ребенка и его настоящем уже в новой семье\
""")
    inline_markup = types.InlineKeyboardMarkup()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://changeonelife.ru/about/mission/')
    hi_btn = types.KeyboardButton("Привет")
    inline_markup.add(btn1)
    keyboard.add(hi_btn)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup = inline_markup)
    bot.send_message(message.from_user.id, "Выберите действия, которые вы хотите совершить:" , reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
   if message.text == 'Привет':
       if check_user(message.from_user.id):
           bot.send_message(message.from_user.id, 'Привет! Вы уже были зарегистрированы!')
       else:
        add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        bot.send_message(message.from_user.id, 'Привет! Ваше имя добавлено в базу данных!')

def check_user(user_id):
    cursor.execute('SELECT 1 FROM test WHERE user_id = ? LIMIT 1', (user_id,))
    result = cursor.fetchone()
    return result

def add_user(user_id: int, user_name: str, user_surname: str, username: str):

    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()

#
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')
#         us_id = message.from_user.id
#         us_name = message.from_user.first_name
#         us_sname = message.from_user.last_name
#         username = message.from_user.username
#
#         db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
#
#
#

bot.infinity_polling()
