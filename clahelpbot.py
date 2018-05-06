# -*- coding: utf-8 -*-

import os
import re
from random import random

import telebot
from flask import Flask, request
from answers import hzpool
import scenarios
import numpy as np
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator
from dale_chatbotclass import NeighborSampler
from sklearn.externals import joblib
dale_chatbot = joblib.load('dale_chatbot.pkl')
#import pickle
#with open('dale_chatbot.pkl', 'rb') as fh:
#    dale_chatbot = pickle.load(fh)

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name + '!')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, '''Можешб обращаться "бот" или "пёс"''')

@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['text'])
def private_message(message):
    if re.search("[Кк]ин[оцч]|[Фф]ильм", message.text):
        scenarios.movie_scenario(message,bot)
    elif re.search("[Аа]н[еи]к", message.text):
        scenarios.anek_scenario(message, bot)
    else:
        bot.reply_to(message, hzpool[round(random()*len(hzpool))])
        #bot.reply_to(message, dale_chatbot.predict([message.text.lower()])[0])

@bot.message_handler(func=lambda message: message.chat.type=='group', content_types=['text'])
def group_message(message):
    if re.search("[Бб]о+т|[Пп][её]+с", message.text):
        if re.search("[Кк]ин[оцч]|[Фф]ильм", message.text):
            scenarios.movie_scenario(message,bot)
        elif re.search("[Аа]н[еи]к", message.text):
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
