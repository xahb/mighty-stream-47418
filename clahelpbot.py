# -*- coding: utf-8 -*-

import os
import re
from random import random
import pickle
import pandas as pd

import telebot
from flask import Flask, request
import numpy as np
#from sklearn.neighbors import BallTree
#from sklearn.base import BaseEstimator
#import numpy as np
#from psycopg2 import connect

from answers import hzpool
import scenarios


'''
def softmax(x):
    proba=np.exp(-x)
    return proba / sum(proba)

class NeighborSampler(BaseEstimator):
    def __init__(self, k=5, temperature=1.0):
        self.k=k
        self.temperature=temperature
    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)
    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p=softmax(distance * self.temperature)))
        return self.y_[result]

with open('dale_chatbot2.pickle', 'rb') as fh:
    dale_chatbot = pickle.load(fh)
'''
with open('memebase.pickle', 'rb') as mb:
    memebase = pickle.load(mb)
    
token = os.environ['TOKEN']
bot = telebot.TeleBot(token)
server = Flask(__name__)

#DATABASE_URL = os.environ['DATABASE_URL']
#conn = connect(DATABASE_URL, sslmode='require')
#memebase = pd.read_csv('memebase.csv')
 

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, message.from_user.first_name.decode('utf-8').encode('utf-8', 'replace'))
    #bot.reply_to(message, 'Привет, ' + message.from_user.first_name.decode('utf-8').encode('utf-8', 'replace') + '!')
    #bot.reply_to(message, 'Привет!' + ' вжжжж')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, '''Можешб обращаться "бот" или "пёс"''')
    
@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['photo','document'])
def write_photo(message,memebase=memebase):
    #cur = conn.cursor()
    #cur.execute("INSERT INTO memebase (num, data) VALUES (%s, %s)", ())
    new_row = {'message_id':message.message_id,'from_user':message.from_user,'date':message.date,'chat':message.chat,'id':memebase.shape[0]}
    memebase = memebase.append(pd.DataFrame(new_row,index=[memebase.shape[0]]))
#    with open('memebase.pickle', 'wb') as mb:
#        pickle.dump(memebase, mb)
#    bot.reply_to(message, 'Сохранил'+str(new_row['message_id']))
    bot.reply_to(message, 'Сохранил'+str(memebase['message_id'][0]))

@bot.message_handler(func=lambda message: message.chat.type=='private', content_types=['text'])
def private_message(message):
    if re.search('[Кк]ин[оцч]|[Фф]ильм', message.text):
        scenarios.movie_scenario(message,bot)
    elif re.search('[Аа]н[еи]к', message.text):
        #scenarios.anek_scenario(message, bot)
        bot.reply_to(message, hzpool[0])
#    elif re.search('[Мм]ем', message.text):
    else:
        try:
            row = memebase.iloc[int(np.random.random()*len(memebase.index)),:]
            bot.forward_message(message.chat, row['chat'], row['message_id'])
        except: bot.reply_to(message, "дррр")
#    else:
#        bot.reply_to(message, hzpool[int(round(random()*len(hzpool)))])
        #bot.reply_to(message, dale_chatbot.predict([message.text.lower()])[0])

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
