# -*- coding: utf-8 -*-

import os
import re
from random import random, choice as random_choice
from emoji import emojize, demojize
from emoji.unicode_codes import EMOJI_UNICODE
EMOJI_UNICODE_LIST = list(EMOJI_UNICODE)
import json

import telebot
from telebot import apihelper
from flask import Flask, request
#from psycopg2 import connect

   
token = os.environ['TOKEN']
bot = telebot.TeleBot(token)
server = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
#conn = connect(DATABASE_URL, sslmode='require')
#cur = conn.cursor()

from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)

from sqlalchemy import func
from sql_queries import SqlMessage, SqlUser, SqlChat, SqlReaction, SqlKeyReaction, Base

# Создание таблицы
Base.metadata.create_all(engine) 

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

help_instruction = '''Hi! Forward a meme (post with photo or gif) to this chat and Bot will save it (with no connection to you).
Tap "Go!" and Bot will forward you one of the saved memes. Rate it and you'll get better memes next time!
'''

def __main_keyboard__():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row_width = 2
    keyboard.add('Go! '+emojize(':cat_face_with_wry_smile:'),'Stats '+emojize(':chart_increasing:'))
    return keyboard

### ui
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, help_instruction, reply_markup=__main_keyboard__())
    
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, help_instruction, reply_markup=__main_keyboard__())

@bot.message_handler(commands=['esc'])
def esc_command(message):
    bot.reply_to(message, 'Keyboard removed', reply_markup=telebot.types.ReplyKeyboardRemove())
    
@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['photo','document'])
def save_meme(message):
    session = Session()
    sql_message = SqlMessage(message)
    session.add(sql_message)
    
    sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
    
    if type(sql_chat) is None:
        sql_chat = SqlChat(message)
        session.add(sql_chat)
        sql_chat.state_0 = sql_message.id   
    
    sql_user = session.query(SqlUser).filter_by(id=message.from_user.id).first()
    
    if type(sql_user) is None:
        sql_user = SqlUser(message)
        session.add(sql_user)

    session.commit()
    bot.reply_to(message, 'Saved '+str(message.message_id)+' from '+str(message.from_user.first_name))


@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['text'], regexp='Stats ')
def show_stats(message):
    session = Session()
    try:
        sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        sql_chat.messages_shared  = session.query(func.count(SqlMessage.id)).filter_by(chat_id=message.chat.id)
        sql_chat.messages_received  = session.query(func.count(SqlKeyReaction.id)).filter_by(reaction_chat_id=message.chat.id)
        sql_chat.messages_rated  = session.query(func.count(SqlKeyReaction.id)).filter(SqlKeyReaction.reaction_chat_id==message.chat.id, SqlKeyReaction.emoji_winner!='0')
    except:
        sql_chat = SqlChat(message)
        session.add(sql_chat)
    try:
        # для групповых чатов логика не подойдет, но пока вроде и не надо
        sql_user = session.query(SqlUser).filter_by(id=message.from_user.id).first()
        sql_user.messages_shared  = sql_chat.messages_shared
        sql_user.messages_received  = sql_chat.messages_received
        sql_user.messages_rated  = sql_chat.messages_rated
    except:
        sql_user = SqlUser(message)
        session.add(sql_user)
    bot.reply_to(message, '''You've shared %s memes with Bot \nYou've received %s memes from Bot \nYou've rated %s memes''' % (sql_chat.messages_shared, sql_chat.messages_received, sql_chat.messages_rated))
    session.commit()

    
@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['text'], regexp='Go!')
def forward_meme(message):
    session = Session()
    try:
        sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
        if (sql_chat.state_0 > 0 and re.search(':.+:', demojize(message.text))):
            sql_reaction = SqlReaction(message, sql_chat.state_0)
            session.add(sql_reaction)
            sql_chat.state_0 = 0
    except:
        pass
    session = Session()
    response = session.query(SqlMessage).order_by(func.random()).first()
    #Почему-то не работает
    if type(response) is None:
        bot.reply_to(message, '''Hmm''')
    else:
        bot.forward_message(message.chat.id, response.chat_id, response.message_id)
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row_width = 5
    emoji_challengers = [':rolling_on_the_floor_laughing:',':slightly_smiling_face:',':unamused_face:',':frowning_face_with_open_mouth:',':flushed_face:']+[random_choice(EMOJI_UNICODE_LIST) for i in range(10)]
    sql_key_reaction = SqlKeyReaction(response.id, message.chat.id, str(emoji_challengers), '0')
    session.add(sql_key_reaction)
    rb = []
    for emoji in emoji_challengers:
        rb.append(telebot.types.InlineKeyboardButton(text=emojize(emoji), 
        callback_data=json.dumps([sql_key_reaction.id,EMOJI_UNICODE_LIST.index(emoji)])))
    keyboard.add(*rb)
    bot.send_message(message.chat.id, 'Rate it:', reply_markup=keyboard)

    sql_chat = session.query(SqlChat).filter_by(id=message.chat.id).first()
    
    if type(sql_chat) is None:
        sql_chat = SqlChat(message)
        session.add(sql_chat)
        sql_chat.state_0 = response.id 
    
    session.commit()

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    session = Session()
    cb_data = json.loads(call.data)
    sql_key_reaction = session.query(SqlKeyReaction).filter_by(id=cb_data[0]).first()
    sql_key_reaction.emoji_winner = EMOJI_UNICODE_LIST[cb_data[1]]
    session.commit()
        
### back
@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
'''
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://mighty-stream-47418.herokuapp.com/bot")
    return "!", 200
'''
bot.remove_webhook()
bot.infinity_polling()


if __name__ == '__main__':
	server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
