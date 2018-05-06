# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 23:38:57 2017

@author: xahb
"""
def anek_scenario(message, bot):
    import re
    from answers import anekpool
    from poolsearch import pool_search, endcut_base
    from random import random
    
    isthematic = re.search("[Пп]ро \w+", message.text)
    if isthematic:
        theme=isthematic.group(0)[4:]
        aneksfound = pool_search(anekpool, endcut_base(theme))
        if len(aneksfound)>1:
            chosen=aneksfound[round(random()*len(aneksfound))]
            bot.reply_to(message, anekpool[chosen])
            #anek_candidates=aneksfound
        elif len(aneksfound)==1:
            bot.reply_to(message, anekpool[aneksfound[0]])
        else:
            bot.reply_to(message, "Не знаю таких")
    else:
        bot.reply_to(message, anekpool[round(random()*len(anekpool))])
        
        
def movie_scenario(message, bot):
    import os
    import re
    from urllib import parse
    import psycopg2
    from random import random
    
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    
    cur = conn.cursor()
    
    #conditions for query
    conditions = "WHERE 1=1"
    
    #year filter
    isyear = re.search("[0-9]{2,4}", message.text)
    if isyear:
        if re.search("не стар[еш]е|новее|позднее|после|свежее", message.text):
            yearfilter=">= "
        else:
            yearfilter="= "
        year = isyear.group(0)
        conditions += " AND year "+yearfilter+str(year)
    else:
        year="" #for replacement in rating search
    
    #rating filter
    israting = re.search("[Рр]ейтинг", message.text)
    if israting:
        if re.search("не ниже|не меньше|больше|выше|от", message.text):
            ratingfilter=">= "
        else:
            ratingfilter="= "
        rating = re.search("[0-9][.,]?[0-9]?", message.text.replace(year,"")).group(0) #remove year from the string
        conditions += " AND rating_kp "+ratingfilter+str(rating)    
          
    cur.execute('SELECT movie_id from "tomatoes1000" '+conditions)
    movie_candidates = cur.fetchall()
    
    if len(movie_candidates)>0:
        movie_rand = movie_candidates[round(random()*len(movie_candidates))][0]
    
        cur.execute('SELECT name_ru, name_en, year, rating_kp, votes_kp, genres from "tomatoes1000" WHERE movie_id='+str(movie_rand))
        movie = cur.fetchall()
    
        answer= movie[0][0] + " ("+ movie[0][1]+")\n" + "Год: " + str(movie[0][2]) + "\n" + "Рейтинг КП: " + str(movie[0][3]) + "\n" + "Голосов на КП: " + str(movie[0][4]) + "\n" + "Жанр: " + str(movie[0][5])
    else:
        answer= "Сорри, не знаю таких"
    bot.reply_to(message, answer)
