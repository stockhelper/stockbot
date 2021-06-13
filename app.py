# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:41:10 2019

@author: aaaaa
"""

from __future__ import print_function
import time
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import schedule
from pymongo import MongoClient
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup

# Authentication Database認證資料庫
Authdb='Stock_Helper_Database'

line_bot_api = LineBotApi('dxXnzAfehaEFn4wc2QPQ2TshuuvjpVeppPJFCsLVuEFl2Kq82UIgw2eN9byiudwCvjw/iIPvHy6LyQO5XZP34RgH9MF4Yh+ZothnbvUXghY0veC8Snf8YuNJXVzuUrhKiTfABsjQ4GJ0LVQsnjut2QdB04t89/1O/w1cDnyilFU=')
yourid='U0f84a7f70cfdf86b7afa00cd651f5836'
##### 資料庫連接 #####
def constructor():
    client = MongoClient('mongodb+srv://stock_helper_01:<password2021>@cluster0.2el1z.mongodb.net/Stock_Helper_Database?retryWrites=true&w=majority')
    db = client[Authdb]
    return db

# 抓你的股票
def show_user_stock_fountion():  
    db=constructor()
    collect = db['fountion']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel

def job():
    data = show_user_stock_fountion()
    for i in data:
        stock=i['stock']
        bs=i['bs']
        price=i['price']
        
        url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getstock= soup.find('b').text #裡面所有文字內容
        if float(getstock):
            if bs == '<':
                if float(getstock) < price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
            else:
                if float(getstock) > price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
        else:
            line_bot_api.push_message(yourid, TextSendMessage(text='這個有問題'))
second_5_j = schedule.every(10).seconds.do(job)

# 無窮迴圈
while True: 
    schedule.run_pending()
    time.sleep(1)
