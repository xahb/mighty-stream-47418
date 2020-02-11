# -*- coding: utf-8 -*-

import os
import re
from random import random
from emoji import emojize, demojize
from emoji.unicode_codes import EMOJI_UNICODE

import telebot
from flask import Flask, request
from psycopg2 import connect

from answers import hzpool
import scenarios
#import sql_queries
   
token = os.environ['TOKEN']
bot = telebot.TeleBot(token)
server = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)

from sqlalchemy import func
from sql_queries import SqlMessage, SqlUser, SqlChat, SqlReaction, Base

# Создание таблицы
Base.metadata.create_all(engine) 

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, message.from_user.first_name.decode('utf-8').encode('utf-8', 'replace'))
    #bot.reply_to(message, 'Привет, ' + message.from_user.first_name.decode('utf-8').encode('utf-8', 'replace') + '!')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, '''Можешб обращаться "бот" или "пёс"''')
    
@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['photo','document'])
def write_photo(message):
    session = Session()
    sql_message = SqlMessage(message)
    session.add(sql_message)

    try:
        sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        sql_chat.messages_count += 1
    except:
        sql_chat = SqlChat(message)
        session.add(sql_chat)
    sql_chat.state_0 = sql_message.id
    
    try:
        sql_user = session.query(SqlUser).filter_by(id=message.from_user.id).first()
        sql_user.messages_count += 1
    except:
        sql_user = SqlUser(message)
        session.add(sql_user)

    session.commit()
    bot.reply_to(message, 'Сохранил '+str(message.message_id)+' от '+str(message.from_user.first_name))

@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['text'])
def private_message(message):
    session = Session()
    try:
        sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        if (sql_chat.state_0 > 0 and re.search(':.+:', demojize(message.text))):
            sql_reaction = SqlReaction(message, sql_chat.state_0)
            session.add(sql_reaction)
            sql_chat.state_0 = 0
    except:
        pass       
    if re.search('[Кк]ин[оцч]|[Фф]ильм', message.text):
        scenarios.movie_scenario(message,bot)
    elif re.search('[Аа]н[еи]к', message.text):
        scenarios.anek_scenario(message, bot)
    elif re.search('[Мм]ем', message.text):
        session = Session()
        response = session.query(SqlMessage).order_by(func.random()).first()
        bot.forward_message(message.chat.id, response.chat_id, response.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(3):
            emoji = random.choice(list(EMOJI_UNICODE))
            keyboard.add(telebot.types.InlineKeyboardButton(text=emojize(emoji), callback_data=emoji))
        bot.send_message(message.chat.id, '?', reply_markup=keyboard)
        try:
            sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        except:
            sql_chat = SqlChat(message)
            sql_chat.messages_count = 0
            session.add(sql_chat)
        sql_chat.state_0 = response.id
    session.commit()


@bot.message_handler(func=lambda message: message.chat.type=='group', content_types=['text'])
def group_message(message):
    #if re.search('[Бб]о+т|[Пп][её]+с', message.text):
        if re.search('[Кк]ин[оцч]|[Фф]ильм', message.text):
            scenarios.movie_scenario(message,bot)
        elif re.search('[Аа]н[еи]к', message.text):
            scenarios.anek_scenario(message, bot)
        else:
            bot.reply_to(message, hzpool[round(random()*len(hzpool))])
            #bot.reply_to(message, dale_chatbot.predict([message.text.lower()])[0])

         

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://mighty-stream-47418.herokuapp.com/bot")
    return "!", 200

if __name__ == '__main__':
	server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
