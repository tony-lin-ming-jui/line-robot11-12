from flask import Flask,render_template,request,redirect,url_for,session
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#from linebot.exceptions import *
from linebot.models import *
#from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
import requests
from bs4 import BeautifulSoup

import base64
from matplotlib.font_manager import FontProperties
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import io
import json
import pandas

import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

import random
import song_crawler
import apple
import movie_crawler
import invoice_pic_crawler
import radar_crawler
import Sticker_random
import rainfall_pic_crawler
import Satellite_pic_crawler
import weather_data
import oil_crawler_n_office
import oil_crawler_tw_new
import work_class_cancel_crawler
import work_class_cancel_crawler_notebook
import PTQS1005
import oil_crawler_of
import power_crawler_office
import reservoir_crawler

import pymysql
import os
import re

from pygame import mixer

import sys
app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)



line_bot_api = LineBotApi('dzMHXFwU0FbiK7Ct+zLK80AgIt3wHV7trwSdsh+EjSKNW8vTir0fhCP6qRsqLWjl/UxiiqECfBK6AfHe0htI/Ksqz0DQLAGBoZZnsLG7lgXlHSvG7gd6yW2LT7K5qbXl4fQ4f3X+YCWlfXPv/vptTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18305b046cb7b77b860f4381569cafd3')
#user_id='U7446a50ce4c8e4c5942a18454bac76a2'
webhook_url="https://2633cdc9.ngrok.io"
db = pymysql.connect("127.0.0.1","root","1qaz1qaz","linesss",charset="utf8" )
cursor = db.cursor()

@app.route("/voice")
def voice():
    #print("aaaaaaaaa",a)
    #if a:
    return render_template('voice.html')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text =="我要加入語音訊息服務":
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        if isinstance(event.source, SourceUser):
            #創數據庫的方式只有第一次要創
            #cursor.execute("create table voice (number Integer NOT NULL AUTO_INCREMENT,userid VARCHAR(35) NOT NULL,name VARCHAR(35), PRIMARY KEY (number))")
            #db.commit()
            profile = line_bot_api.get_profile(event.source.user_id)
            print(profile.display_name)
            print(client)
            cursor.execute("SELECT * FROM voice WHERE name ='"+ str(profile.display_name)+"'")
            A=cursor.fetchall()
            print(A)
            if A:
                mes="名稱已有人使用或你已經加入過了歐"
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/service1.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/service1.m4a')
                    mixer.music.play()                    
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service1.m4a', duration=100000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/service1s.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/service1s.m4a')
                    mixer.music.play()                    
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service1sm4a', duration=100000))

            else:                
                cursor.execute("INSERT INTO voice (userid, name) VALUES ('" + str(client) + "','" + str(profile.display_name) + "')")
                db.commit()
                smes="名稱"+str(profile.display_name)+"成功加入語音訊息服務"
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/service2.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/service2.m4a')
                    mixer.music.play()                    
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service2.m4a', duration=100000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/service2s.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/service2s.m4a')
                    mixer.music.play()                    
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service2s.m4a', duration=100000))
        else:
            fmes="無法取得你的名稱，群組或聊天室無法使用此功能"
            try:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+fmes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/service3.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/service3.m4a')
                mixer.music.play()                    
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=fmes))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service3.m4a', duration=100000))
            except:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+fmes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/service3s.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/service3s.m4a')
                mixer.music.play()                    
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=fmes))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service3s.m4a', duration=100000))
            
    elif re.findall('^傳Line給.*?:[^:]+',event.message.text):
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))

        #print(''.join(re.findall('^傳Line訊息給(.*?):[^:]+',event.message.text)))
        name=''.join(re.findall('^傳Line給(.*?):[^:]+',event.message.text))
        #print(''.join(re.findall('^傳Line訊息給.*?:([^:]+)',event.message.text)))
        mesg=''.join(re.findall('^傳Line給.*?:([^:]+)',event.message.text))
        profile = line_bot_api.get_profile(event.source.user_id)
        print(profile.display_name)
        print(name)
        print(mesg)
        dmesg="來自"+str(profile.display_name)+"的訊息:"+str(mesg)
        smesg="傳送成功"
        cursor.execute("SELECT * FROM voice WHERE name ='"+ str(name)+"'")
        for row in cursor.fetchall():            
            who=row[1]
        #print(who)
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+dmesg+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/service4.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            #stream_urls = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smesg+'&language=zh-tw'
            #rs = requests.get(stream_urls, stream=True)
            #with open('staticsss/service4sss.m4a', 'wb') as f:
            #    try:
            #        for block in rs.iter_content(1024):
            #            f.write(block)
            #        f.close()
            #    except KeyboardInterrupt:
            #        pass
            mixer.init()
            mixer.music.load('static/service4.m4a')
            mixer.music.play()
            #mixer.init()
            #mixer.music.load('staticsss/service4sss.m4a')
            #mixer.music.play()
            #print(who)                    
            line_bot_api.push_message(who,TextSendMessage(text=dmesg))
            line_bot_api.push_message(who,AudioSendMessage(original_content_url=webhook_url+'/static/service4.m4a', duration=100000))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smesg))
            #line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticsss/service4sss.m4a', duration=100000))
            #掛點 QQ
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+dmesg+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/service4s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            #stream_urls = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smesg+'&language=zh-tw'
            #rs = requests.get(stream_urls, stream=True)
            #with open('statica/service4a.m4a', 'wb') as f:
            #    try:
            #        for block in rs.iter_content(1024):
            #            f.write(block)
            #        f.close()
            #    except KeyboardInterrupt:
            #        pass
            #mixer.init()
            #mixer.music.load('statics/service4s.m4a')
            #mixer.music.play()
            #mixer.init()
            #mixer.music.load('statica/service4a.m4a')
            #mixer.music.play()
            print(who)                    
            line_bot_api.push_message(who,TextSendMessage(text=dmesg))
            line_bot_api.push_message(who,AudioSendMessage(original_content_url=webhook_url+'/statics/service4s.m4a', duration=100000))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smesg))
            #line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statica/service4a.m4a', duration=100000))
        
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


   
if __name__ == "__main__":
    app.run(port=9000,debug =True)
