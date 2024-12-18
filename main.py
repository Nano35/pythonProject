import sqlite3
from email.policy import default

import requests

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.get_api_key())
conn = sqlite3.connect('db/python.db', check_same_thread=False)
cursor = conn.cursor()

global fio
global birthday
global when_i_birth
global my_present
global my_future
global file_path

STATE_WAITING_FOR_ANSWER = 0
ANSWER_RECEIVED = 1

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
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
       reg_btn = types.KeyboardButton("📕 Собрать книгу жизни")
       keyboard.add(reg_btn)
       bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=keyboard)
   elif message.text == '📕 Собрать книгу жизни':
       bot.send_message(message.from_user.id, "Напишите ФИО ребенка")
       bot.register_next_step_handler(message, add_child_data)

def add_child_data(message):
    global fio
    fio = message.text
    bot.reply_to(message, f"ФИО ребенка: {fio}")
    bot.send_message(message.from_user.id, "Загрузите фото ребенка")
    bot.register_next_step_handler(message, add_child_photo)

def add_child_photo(message):
    file = bot.get_file(message.photo[-1].file_id)
    global file_path
    file_path = file.file_path  # Путь к сохраненному файлу который сохраняется в бд
    file_url = f"https://api.telegram.org/file/bot{config.get_api_key()}/{file_path}" # Реальный путь (можете по нему перейти там в консоли он выводится) НЕ ИСПОЛЬЗОВАТЬ В БД ТАК КАК ПАЛИТСЯ BOT API KEY
    print(file_url)
    response = requests.get(file_url, stream=True)
    response.raise_for_status()  # Проверяем на ошибки

    with open(f"photo_{file.file_id}.jpg", "wb") as f:  # Сохраняем файл на сервер
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    bot.send_message(message.from_user.id, "Напишите день рождения ребенка:")
    bot.register_next_step_handler(message, add_birthday)

def add_birthday(message):
    global birthday
    birthday = message.text
    bot.reply_to(message, f"День рождения ребенка: {birthday}")
    bot.send_message(message.from_user.id, """*Моё прошлое*
Расскажите о прошлом ребенка \(о том когда он родился и где он родился\)""", parse_mode="MarkdownV2")
    bot.send_message(message.from_user.id, "Напишите информацию о том когда он родился и где он родился", parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, add_when_i_birth)

def add_when_i_birth(message):
    global when_i_birth
    when_i_birth = message.text
    bot.send_message(message.from_user.id, """*Моё настоящее*
Расскажите о настоящем ребенка \(о том где он сейчас живет, люди которые с ним, распорядок дня и его свободное время\)""", parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, add_my_present)

def add_my_present(message):
    global my_present
    my_present = message.text
    bot.send_message(message.from_user.id, """*Моё будущее*
Расскажите о будущем ребенка \(о том кем он хочет быть, о его будущей семье, о его будущем доме\)""", parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, add_child_db)

def add_child_db(message): # Сохраняем path в базу данных
    global my_future
    my_future = message.text
    resume = when_i_birth + "\n" + my_present + "\n" + my_future

    cursor.execute("INSERT INTO child (fio, birthday, resume, photo) VALUES (?, ?, ?, ?)",
                   (fio, birthday, resume, file_path))  # user_id - ID пользователя из Telegram
    conn.commit()
    conn.close()

def check_user(user_id):
    cursor.execute('SELECT 1 FROM test WHERE user_id = ? LIMIT 1', (user_id,))
    result = cursor.fetchone()
    return result

def add_user(user_id: int, user_name: str, user_surname: str, username: str):

    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()

bot.infinity_polling()
