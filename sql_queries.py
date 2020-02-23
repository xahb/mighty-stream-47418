# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:59:10 2019

@author: Lenovo
"""

from sqlalchemy import Column, BigInteger, DateTime, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from emoji import demojize

Base = declarative_base()

class SqlMessage(Base):
    __tablename__ = 'messages'
    id = Column(BigInteger, primary_key=True)
    message_id = Column(Integer)
    from_user_id = Column(Integer)
    date = Column(DateTime)
    chat_id = Column(Integer)
    forward_from_id = Column(Integer)
    forward_date = Column(DateTime)
    TMP_reply_to_message = Column(String)
    text = Column(String)
    TMP_entities = Column(String)
    TMP_audio = Column(String)
    TMP_document = Column(String)
    TMP_photo = Column(String)
    TMP_sticker = Column(String)
    TMP_video = Column(String)
    TMP_voice = Column(String)
    TMP_caption = Column(String)
    TMP_contact = Column(String)
    TMP_location = Column(String)
    TMP_venue = Column(String)
    TMP_from = Column(String)
    TMP_chat = Column(String)
    TMP_forward_from = Column(String)
    
    def __init__(self, message):
        self.id = int(str(message.chat.id)+str(message.message_id))
        self.message_id = message.message_id
        self.date = datetime.fromtimestamp(message.date)
        self.chat_id = message.chat.id
        try:
            self.from_user_id = message.from_user.id
        except:
            self.from_user_id = 0
        try:
            self.forward_from_id = message.forward_from.id
        except:
            self.forward_from_id = 0
        self.forward_date = datetime.fromtimestamp(message.forward_date)
        self.TMP_reply_to_message = str(message.reply_to_message)
        self.text = message.text
        self.TMP_entities = str(message.entities)
        self.TMP_audio = str(message.audio)
        self.TMP_document = str(message.document)
        self.TMP_photo = str(message.photo)
        self.TMP_sticker = str(message.sticker)
        self.TMP_video = str(message.video)
        self.TMP_voice = str(message.voice)
        self.TMP_caption = str(message.caption)
        self.TMP_contact = str(message.contact)
        self.TMP_location = str(message.location)
        self.TMP_venue = str(message.venue)
        self.TMP_from = str(message.from_user)
        self.TMP_chat = str(message.chat)
        self.TMP_forward_from = str(message.forward_from)
'''
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
'''

class SqlUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    messages_count = Column(Integer)
    messages_shared = Column(Integer)
    messages_received = Column(Integer)
    messages_rated = Column(Integer)
    
    def __init__(self, message):
        self.id = message.from_user.id
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
        self.username = message.from_user.username
        self.messages_count = 1
        self.messages_shared = 0
        self.messages_received = 0
        self.messages_rated = 0


class SqlChat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    all_members_are_administrators = Column(String)
    messages_count = Column(Integer)
    state_0 = Column(BigInteger)    #id of message that bot posted in chat (to collect reactions)
    messages_shared = Column(Integer)
    messages_received = Column(Integer)
    messages_rated = Column(Integer)
    
    def __init__(self, message):
        self.id = message.chat.id
        self.type = str(message.chat.type)
        self.title = message.chat.title
        self.username = message.chat.username
        self.first_name = message.chat.first_name
        self.last_name = message.chat.last_name
        self.all_members_are_administrators = str(message.chat.all_members_are_administrators)
        self.messages_count = 1
        self.state_0 = 0
        self.messages_shared = 0
        self.messages_received = 0
        self.messages_rated = 0


class SqlReaction(Base):
    __tablename__ = 'reactions'
    id = Column(BigInteger, primary_key=True)
    origin_message_id = Column(BigInteger)
    from_user_id = Column(Integer)
    chat_id = Column(Integer)
    date = Column(DateTime)
    emoji = Column(String)
    
    def __init__(self, message, state_0):
        self.id = int(str(message.chat.id)+str(message.message_id))
        self.origin_message_id = state_0
        try:
            self.from_user_id = message.from_user.id
        except:
            self.from_user_id = 0
        self.chat_id = message.chat.id
        self.date = datetime.fromtimestamp(message.date)
        self.emoji = demojize(message.text)


class SqlKeyReaction(Base):
    '''
    Работает только в личке, т.к. я пока хз, как в групповом чате получить user_id юзера, тапнувшего кнопку. 
    Сейчас логика идентификации - через chat_id, в котором тапается кнопка.
    '''
    __tablename__ = 'key_reactions'
    id = Column(String, primary_key=True) #На будущее - подумать, какой лучше ключ сделать для этой таблицы
    meme_id = Column(BigInteger)
    reaction_chat_id = Column(Integer)
    reaction_date = Column(DateTime)
    emoji_challengers = Column(String)
    emoji_winner = Column(String)
    
    def __init__(self, meme_id, reaction_chat_id, challengers, winner):
        self.id = str(meme_id)+str(reaction_chat_id)+str(datetime.now())
        self.meme_id = meme_id
        self.reaction_chat_id = reaction_chat_id
        self.reaction_date = datetime.now()
        self.emoji_challengers = challengers
        self.emoji_winner = winner
