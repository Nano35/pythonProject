import sqlite3
import telebot
from telebot import types
#Токен бота
API_TOKEN = "7272715477:AAGvjBEXoXqX9-5e_X3V5WrOTmcYTHf2ziw"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start']) #команды
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Я бот фонда: "Измени Одну Жизнь"
Я здесь чтобы помочь приемным родителям собрать всю информацию о прошлом их приемного ребенка и его настоящем уже в новой семье\
""")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://changeonelife.ru/about/mission/')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup = markup)


#@bot.message_handler(content_types=['text'])
#def get_text_messages(message):
#    if message.text == '👋 Поздороваться':
#        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
#        btn1 = types.KeyboardButton('Как стать автором на Хабре?')
#        btn2 = types.KeyboardButton('Правила сайта')
#        btn3 = types.KeyboardButton('Советы по оформлению публикации')
#        markup.add(btn1, btn2, btn3)
#        bot.send_message(message.from_user.id, '❓ Задайте интересующий вопрос', reply_markup=markup) #ответ бота



conn = sqlite3.connect('db/python.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
    conn.commit()



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)



@bot.message_handler(func=lambda message: True) #Отвечает на сообщение если не видит команду
def echo_message(message):
    bot.reply_to(message, """
    Не существует такой команды""")

bot.infinity_polling()
