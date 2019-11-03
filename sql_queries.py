# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:59:10 2019

@author: Lenovo
"""

from sqlalchemy import Column, Integer, String#, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class SqlMessage(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    from_user_id = Column(String)
    #date = Column(DateTime)
    chat_id = Column(Integer)
    '''
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
    '''
    def __init__(self, message):
        self.message_id = message.id
        self.from_user_id = message.from_user.id
        #self.date = Column(DateTime)
        self.chat_id = message.chat.id
        self.id = int(str(self.chat_id)+str(self.message_id))
'''
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)


class SqlUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
'''




insert_memes='''INSERT INTO public.memes (message_id, from_user_id, date, chat_id, forward_from_id, forward_date, reply_to_message_id, ) 
                 VALUES (%s, %s, %s, %s, %s);'''


insert_users="INSERT INTO public.users (user_id, user_first_name, user_last_name, username, ) VALUES (%s, %s, %s, %s, %s);" 