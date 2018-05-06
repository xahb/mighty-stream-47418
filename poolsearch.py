#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 23:02:01 2017

@author: xahb
"""

def endcut_base(word):
    
    endings1 = {'а','я','ы','и','е','у','ю','о','ь'}
    endings2 = {'ий','ый','ая','яя','ое','ее','ой','ей','ую','юю','ею','ом','ем','ью','им','ым','ов','ам','ям','ах',
                'ях','ые','ие','ых','их','ым','им', 'ов', 'ев', 'ек', 'ки'}
    endings3 = {'ого','его','ому','ему','ами','ями','ыми','ими'}

    if len(word)>3:
        if word[-3:] in endings3:
            newword=word[:-3]
        elif word[-2:] in endings2:
            newword=word[:-2]
        elif word[-1:] in endings1:
            newword=word[:-1]
        else:
            newword = word
    else:
        newword=word

    return newword


def pool_search(pool, word):
    wordbase = endcut_base(word)
    matches = []
    
    for i in range(len(pool)):
        if pool[i].find(wordbase)>-1:
            matches.append(i)
            
    return matches
