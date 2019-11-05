# -*- coding: utf-8 -*-

import os
import re
from random import random

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
from sql_queries import SqlMessage, SqlUser, SqlChat, Base
'''
from sqlalchemy import Column, Integer, String, BigInteger#, DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class SqlMessage(Base):
    __tablename__ = 'messages'
    id = Column(BigInteger, primary_key=True)
    message_id = Column(Integer)
    from_user_id = Column(String)
    #date = Column(DateTime)
    chat_id = Column(Integer)

    def __init__(self, message):
        self.message_id = message.message_id
        self.from_user_id = message.from_user.id
        #self.date = Column(DateTime)
        self.chat_id = message.chat.id
        self.id = int(str(self.chat_id)+str(self.message_id))
'''
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
    '''
    sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
    sql_chat.messages_count += 1
    '''
    try:
        sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        sql_chat.messages_count += 1
    except:
        sql_chat = SqlChat(message)
        session.add(sql_chat)    
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
    if re.search('[Кк]ин[оцч]|[Фф]ильм', message.text):
        scenarios.movie_scenario(message,bot)
    elif re.search('[Аа]н[еи]к', message.text):
        scenarios.anek_scenario(message, bot)
        #bot.reply_to(message, hzpool[0])
    elif re.search('[Мм]ем', message.text):
#    else:
        #cur.execute('select chat_id, message_id from public.memebase order by random() limit 1')
        #chat_id, message_id = cur.fetchone()
        session = Session()
        response = session.query(SqlMessage).order_by(func.random()).first()
        bot.forward_message(message.chat.id, response.chat_id, response.message_id)
#        bot.send_poll(message.chat.id, 'Чё как?', [':joy_cat:',':shrug:',':facepalm:'])


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
