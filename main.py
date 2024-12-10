import os
import telebot

API_TOKEN = "7272715477:AAGvjBEXoXqX9-5e_X3V5WrOTmcYTHf2ziw"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, """
    не существует такой команды""")



bot.infinity_polling()