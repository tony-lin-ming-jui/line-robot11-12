from flask import Flask,render_template,request,redirect,url_for,session,g,escape,Markup
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


#ESLAB小幫手
line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')
#ESlab
#line_bot_api = LineBotApi('Channel access token')
#handler = WebhookHandler('Channel secret')

webhook_url="https://3593230f.ngrok.io"
scheduler = BlockingScheduler()


#db = pymysql.connect("127.0.0.1","root","1qaz1qaz","linesss",charset="utf8" )
db = pymysql.connect("127.0.0.1","root","1qaz1qaz","line_db",charset="utf8" )
cursor = db.cursor()

@app.route("/voice")
def voice():
    #print("aaaaaaaaa",a)
    #if a:
    return render_template('voice.html')

@app.route("/account",methods=['GET','POST'])#解決不了session
def account():
    #client_id=z
    client_id=session.get('session_name')
    print(client_id)
    cursor.execute("SELECT * FROM "+client_id+"")
    listnumber=[]
    listmoney=[]
    listthing=[]
    listdate=[]
    for row in cursor.fetchall():            
        listnumber.append(int(row[0]))
        listmoney.append(int(row[1]))
        listthing.append(row[2])
        listdate.append(row[3].strftime('%Y/%m/%d'))
   
    mes=[]
        
    for i in range(0,len(listnumber)):
        mes.append("編號"+str(listnumber[i])+" "+str(listthing[i])+":"+str(listmoney[i])+"元 日期:"+str(listdate[i]))        
        #mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i])+"編號"+str(listnumber[i]))
        #mesg='\n'.join(mes)
    #print(mesg)
    return render_template('account.html',mes=mes)


@app.route('/plots')  
def oilweb():
    #if a:
    return render_template('oilweb.html')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    #sched = BlockingScheduler()
    #sched.add_job(t1, 'interval', seconds=10)#這裡設定時間，只有在第一次傳送訊息後 才會開始主動回訊息
    #sched.start()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def t2():

    line_bot_api.push_message(c2,TextSendMessage(text='Hello World! :)'))
    #這裡會主動會訊息
def t1():
    cancel=work_class_cancel_crawler_notebook.wkncls()
    
    line_bot_api.push_message(c1,TextSendMessage(text=cancel[0]+"\n"+cancel[1]+cancel[2]))
    #line_bot_api.push_message(user_id,TextSendMessage(text='Hello World! :)'))




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    #global a
    #a=event.message.text
    if event.message.text == '我是誰':
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            print(profile.display_name)
            try:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"你是"+profile.display_name+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/who.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/who.m4a')
                mixer.music.play()
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text='line的名稱: ' + str(profile.display_name)),
                        TextSendMessage(text='line的自我介紹: ' + str(profile.status_message))
                    ])
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/who.m4a', duration=300000))
            except:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"你是"+profile.display_name+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/whos.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/whos.m4a')
                mixer.music.play()
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text='line的名稱: ' + str(profile.display_name)),
                        TextSendMessage(text='line的自我介紹: ' + str(profile.status_message))
                    ])
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/whos.m4a', duration=300000))

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif event.message.text == '滾':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='離開群組囉! QQ'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='離開聊天室囉! QQ'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="我無法從1:1聊天室滾出去"))
    elif event.message.text =="我要加入代傳訊息服務":
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
                mes="名稱已有人使用或你已經加入過了歐,使用方法請輸入或語音輸入:\n傳Line給小明:你好嗎\n即可傳送訊息給小明"
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
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service1.m4a', duration=300000))
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
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service1sm4a', duration=300000))

            else:                
                cursor.execute("INSERT INTO voice (userid, name) VALUES ('" + str(client) + "','" + str(profile.display_name) + "')")
                db.commit()
                smes="名稱"+str(profile.display_name)+"成功加入代傳訊息服務"
                kmes="使用方法:請輸入或語音輸入\n傳Line給小明:你好嗎\n即可傳送訊息給小明"
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smes+kmes+'&language=zh-tw'
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
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service2.m4a', duration=300000))
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+smes+kmes+'&language=zh-tw'
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
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smes+"\n"+kmes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service2s.m4a', duration=300000))
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
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service3.m4a', duration=300000))
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
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service3s.m4a', duration=300000))
            
    elif re.findall('^傳Line',event.message.text):
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        if re.findall('^傳Line給.*?:[^:]+',event.message.text):
            cursor.execute("SELECT * FROM voice WHERE userid ='"+ str(client)+"'")
            A=cursor.fetchall()
            if A:

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
                cursor.execute("SELECT * FROM voice WHERE name ='"+ str(name)+"'")#這裡應該可以改成select userid from voice where name = '"+ str(name)+"'
                A=cursor.fetchall()
                if A:
                    for row in A:            
                        who=row[1]
                    print(who)
                    whoss=who
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

                        mixer.init()
                        mixer.music.load('static/service4.m4a')
                        mixer.music.play()
                    
                        line_bot_api.push_message(whoss,TextSendMessage(text=dmesg))
                        line_bot_api.push_message(whoss,AudioSendMessage(original_content_url=webhook_url+'/static/service4.m4a', duration=800000))
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

                        mixer.init()
                        mixer.music.load('statics/service4s.m4a')
                        mixer.music.play()

                        print(who)                    
                        line_bot_api.push_message(whoss,TextSendMessage(text=dmesg))
                        line_bot_api.push_message(whoss,AudioSendMessage(original_content_url=webhook_url+'/statics/service4s.m4a', duration=800000))
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=smesg))
                        #line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statica/service4a.m4a', duration=100000))

                else:
                    xmes=name+"這個人未加入代傳訊息服務"               
                    try:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+xmes+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/service6.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('static/service6.m4a')
                        mixer.music.play()                
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=xmes))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service6.m4a', duration=800000))
                        
                    except:
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+xmes+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/service6s.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                        mixer.init()
                        mixer.music.load('statics/service6s.m4a')
                        mixer.music.play()                
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=xmes))
                        line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service6s.m4a', duration=800000))
            else:
                nomes="必須加入代傳訊息服務才能使用此功能,\n如果想加入請點擊功能選單中的'我要加入代傳訊息服務',\n群組或聊天室無法使用此功能"
                try:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+nomes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/service8.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/service8.m4a')
                    mixer.music.play()                
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=nomes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service8.m4a', duration=100000))                 
                except:
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+nomes+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statics/service8s.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statics/service8s.m4a')
                    mixer.music.play()                
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=nomes))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service8s.m4a', duration=100000))
        else:
            b=request.get_data(as_text=True)       
            if re.findall('roomId":"(.*?)"',b):
                client=''.join(re.findall('roomId":"(.*?)"',b))
            elif re.findall('groupId":"(.*?)"',b):
                client=''.join(re.findall('groupId":"(.*?)"',b))     
            else:
                client=''.join(re.findall('userId":"(.*?)"',b))

            remind="輸入方式:\n傳Line給小明:你好嗎"
            reminds="輸入方式:\n傳Line給小明冒號你好嗎"
            cursor.execute("SELECT * FROM voice")
            list_name=[]
            for row in cursor.fetchall():            
                #print(row[2])
                list_name.append("名稱:"+row[2]+"\n")
            #print(list_name)
            names=''.join(list_name)
            
            print('names',names)
            try:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+reminds+'，加入本服務的用戶有'+names+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/service5.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/service5.m4a')
                mixer.music.play()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=remind+"\n\n加入本服務的用戶有:\n"+names))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service5.m4a', duration=300000))
            except:
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+reminds+'，加入本服務的用戶有'+names+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/service5s.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/service5s.m4a')
                mixer.music.play()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=remind+"\n\n加入本服務的用戶有:\n"+names))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service5s.m4a', duration=300000))

    elif event.message.text =="代傳訊息服務操作":
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        hmes="使用方法:第一，請輸入或語音輸入:我要加入代傳訊息服務\n第二，請輸入或語音輸入:\n傳Line給小明:你好嗎\n即可傳送訊息給小明"
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+hmes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/service7.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/service7.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=hmes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/service7.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+hmes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/service7s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/service7s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=hmes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/service7s.m4a', duration=300000))
        
    elif event.message.text == "你好":
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes="你好我是你的個人助理你也可以把我拉進群組或聊天室 當你群組或聊天室的助理歐"
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/hello.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/hello.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你好我是你的個人助理\n你也可以把我拉進群組/聊天室 當你群組/聊天室的助理歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hello.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/hellos.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/hellos.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你好我是你的個人助理\n你也可以把我拉進群組/聊天室 當你群組/聊天室的助理歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hellos.m4a', duration=300000))

    elif event.message.text =="貼圖":
       sticker=Sticker_random.sticker()
       line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=sticker[0], sticker_id=sticker[1]))
    elif event.message.text =="時間":
        b=request.get_data(as_text=True)     
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        time_now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"現在時間"+time_now+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/timenow.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/timenow.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="現在時間"+time_now))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/timenow.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"現在時間"+time_now+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/timenows.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/timenows.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="現在時間"+time_now))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/timenows.m4a', duration=300000))

    elif event.message.text == "發票":
        invoice=invoice_pic_crawler.invoice()
        print("invoice",invoice)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=invoice[0], preview_image_url=invoice[0]))
    elif event.message.text == "油價":
        b=request.get_data(as_text=True)            
        #profile = line_bot_api.get_profile(event.source)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        oil=oil_crawler_tw_new.oil()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+oil+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oil.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oil.m4a')
            mixer.music.play()
            mes="\n參考資料:https://gas.goodlife.tw/"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=oil+mes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oil.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+oil+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oils.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oils.m4a')
            mixer.music.play()
            mes="\n參考資料:https://gas.goodlife.tw/"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=oil+mes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oils.m4a', duration=300000))

    elif event.message.text == "國際油價":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        #oilof=oil_crawler_of.oilof()
        img = io.BytesIO()
        oilof=oil_crawler_of.oilof()
        #oilof=oilof()
        #print(oilof)
        #print(list_oildate)

        list_oildate=oilof[:31]
        list_oildata=oilof[-93:]

        x=0
        y=3
        list_a=[]
        for i in range(0,31):    
            list_a.append(list_oildata[x:y])
            #print(list_oildata[:x])
            x=x+3
            y=y+3

        #print(list_a)
        jd=json.loads(str(list_a))
        #print("======================================================================================")
        #print(jd)
        
        df=pandas.DataFrame(jd)
        df.columns = ['西德州','北海布蘭特','杜拜']

        list_r=list_oildata[0:93:3]
        list_g=list_oildata[1:93:3]
        list_b=list_oildata[2:93:3]

        #print(list_r)

        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
        plt.rcParams['axes.unicode_minus'] = False
        plt.cla()
        plt.xticks(arange(len(list_oildate)),list_oildate)
        plt.plot(list_r,'o-',color='deeppink', label=u'西德州')
        plt.plot(list_g,'o-',color='#ADFF2F', label=u'北海布蘭特')
        plt.plot(list_b,'o-',color='deepskyblue', label=u'杜拜')
        #將數字顯示在圖上
        c = np.arange( len (list_oildate))
        for x1, y1 in zip(c,list_r ): 
            plt.text(x1, y1 , '%.2f' % y1, ha= 'center' , va= 'bottom' )
        for x2, y2 in zip(c,list_g ): 
            plt.text(x2, y2 , '%.2f' % y2, ha= 'center' , va= 'bottom' )
        for x3, y3 in zip(c,list_b ): 
            plt.text(x3, y3 , '%.2f' % y3, ha= 'center' , va= 'bottom' )

        plt.xlabel(u'月/日')
        plt.ylabel(u'美元/桶')
        plt.legend(loc='upper left')#寫完 label要再加這行才會顯示例
        plt.gcf().set_size_inches(20,10)

        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        image_64_decode = base64.b64decode(plot_url)

        with open('static/oil.jpg', 'wb') as out_file:
            out_file.write(image_64_decode)


        m="今天國際油價:\n西德州:"+str(oilof[-3])+"美元\每桶\n北海布蘭特:"+str(oilof[-2])+"美元\每桶\n杜拜:"+str(oilof[-1])+"美元\每桶\n"
        u="參考資料:https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
        print(m+u)
        #line_bot_api.push_message(user_id,TextSendMessage(text=m+u))
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+m+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/nationoil.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/nationoil.m4a')
            mixer.music.play()
            line_bot_api.push_message(client,ImageSendMessage(original_content_url=webhook_url+"/static/oil.jpg", preview_image_url=webhook_url+"/static/oil.jpg"))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m+u))        
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/nationoil.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+m+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/nationoils.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/nationoils.m4a')
            mixer.music.play()
            line_bot_api.push_message(client,ImageSendMessage(original_content_url=webhook_url+"/static/oil.jpg", preview_image_url=webhook_url+"/static/oil.jpg"))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m+u))        
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/nationoils.m4a', duration=300000))

    elif event.message.text == "電":
        power=power_crawler_office.power()
        powers='\n'.join(power)
        print(type(powers))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=powers))
    elif event.message.text == "水庫":
        reservoir=reservoir_crawler.dam()
        print(type(reservoir))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reservoir))
    elif event.message.text == "天氣":  #原天氣
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather() 
        cancel=work_class_cancel_crawler_notebook.wkncls()
        mes='''這裡提供全台天氣資訊，請使用按鈕點擊，氣溫，濕度，雷達迴波，目前紫外線，未來紫外線預測，累積雨量，衛星雲圖
        各縣市天氣資料，全縣市天氣資料，會立即得到最新資訊'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/weather.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/weather.m4a')
            mixer.music.play()
        
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='氣溫、濕度、雷達迴波',
                            actions=[
                                MessageAction(label='氣溫',text='氣溫'),                            
                                MessageAction(label='濕度',text='濕度'),
                                MessageAction(label='雷達迴波',text='雷達迴波')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='目前紫外線、未來紫外線預測、累積雨量',
                            actions=[
                                MessageAction(label='目前紫外線',text='紫外線'),                            
                                MessageAction(label='未來紫外線預測',text='未來紫外線預測'),
                                MessageAction(label='累積雨量',text='累積雨量')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='衛星雲圖、各縣市天氣資料、',
                            actions=[
                                MessageAction(label='衛星雲圖',text='衛星雲圖'),
                                MessageAction(label='各縣市天氣資料',text='各縣市天氣資料'),
                                MessageAction(label='全縣市天氣資料',text='全縣市天氣資料')
                            ]
                        )
                    ]))
            line_bot_api.push_message(client,TextSendMessage(text=cancel[0]+cancel[1]))
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/weather.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/weathers.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/weathers.m4a')
            mixer.music.play()
        
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='氣溫、濕度、雷達迴波',
                            actions=[
                                MessageAction(label='氣溫',text='氣溫'),                            
                                MessageAction(label='濕度',text='濕度'),
                                MessageAction(label='雷達迴波',text='雷達迴波')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='目前紫外線、未來紫外線預測、累積雨量',
                            actions=[
                                MessageAction(label='目前紫外線',text='紫外線'),                            
                                MessageAction(label='未來紫外線預測',text='未來紫外線預測'),
                                MessageAction(label='累積雨量',text='累積雨量')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fSkXQiA.jpg',
                            title='目前天氣狀況',
                            text='衛星雲圖、各縣市天氣資料、',
                            actions=[
                                MessageAction(label='衛星雲圖',text='衛星雲圖'),
                                MessageAction(label='各縣市天氣資料',text='各縣市天氣資料'),
                                MessageAction(label='全縣市天氣資料',text='全縣市天氣資料')
                            ]
                        )
                    ]))
            line_bot_api.push_message(client,TextSendMessage(text=cancel[0]+cancel[1]))
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/weathers.m4a', duration=300000))
               
    elif event.message.text == "氣溫":
        url='https://www.cwb.gov.tw/V7/observe/real/Data/Real_Image.png?dumm=1536652956'
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif event.message.text == "濕度":
        url='https://www.cwb.gov.tw/V7/observe/real/Data/Real_Humidity.png?dumm=1536653262'
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif event.message.text == "雷達迴波":        
        radar=radar_crawler.radar()   
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=radar, preview_image_url=radar))
    elif event.message.text == "紫外線":
        url='https://www.cwb.gov.tw/V7/observe/UVI/Data/UVI.png'        
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif event.message.text == "未來紫外線預測":
        #url='https://www.cwb.gov.tw/V7/observe/UVI/Data/UVI_Max.png'#今日紫外線最大值
        url='https://www.cwb.gov.tw/V7/forecast/UVI/Data/UVI01.png'# 明日紫外線預計
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif event.message.text == "累積雨量":
        rainfall=rainfall_pic_crawler.rainfall()
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=rainfall, preview_image_url=rainfall))
    elif event.message.text =="衛星雲圖":
        Satellite=Satellite_pic_crawler.Satellite()
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=Satellite, preview_image_url=Satellite))
    elif event.message.text =="全縣市天氣資料":
        weather=weather_data.weather()
        weathers=''.join(weather)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weathers))
    elif event.message.text == '各縣市天氣資料':#快速的button
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='請選擇縣市查詢天氣資料',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="北北基", text="北北基天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="桃竹苗", text="桃竹苗天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="台中天氣", text="台中天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="彰化天氣", text="彰化天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="南投天氣", text="南投天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="雲林天氣", text="雲林天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="嘉義天氣", text="嘉義天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="宜蘭天氣", text="宜蘭天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="花東天氣", text="花東天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="台南天氣", text="台南天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="高雄天氣", text="高雄天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="屏東天氣", text="屏東天氣")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="外島天氣", text="外島天氣")
                            ),
                            
                        ])))
                       
    elif event.message.text =="基隆天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:        
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Keelung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Keelung.m4a')
            mixer.music.play()            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Keelung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Keelungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Keelungs.m4a')
            mixer.music.play()            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Keelungs.m4a', duration=300000))

        #sys.exit()
    elif event.message.text =="台北天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=300000))
        
        
    elif event.message.text =="臺北天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taipeis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taipeis.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taipeis.m4a', duration=300000))


    elif event.message.text =="新北天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))        
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/NTaipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/NTaipei.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/NTaipei.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/NTaipeis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/NTaipeis.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/NTaipeis.m4a', duration=300000))


    elif event.message.text =="北北基天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))        
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+weather[1]+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/PPK.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/PPK.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]+weather[1]+weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PPK.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+weather[1]+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/PPKs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/PPKs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]+weather[1]+weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PPKs.m4a', duration=300000))

    elif event.message.text =="桃園天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taoyuan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taoyuan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taoyuan.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taoyuans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taoyuans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taoyuans.m4a', duration=300000))

    elif event.message.text =="新竹天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Hsinchu.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Hsinchu.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hsinchu.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Hsinchus.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Hsinchus.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hsinchus.m4a', duration=300000))

        
    elif event.message.text =="苗栗天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Miaoli.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Miaoli.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Miaoli.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Miaolis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Miaolism4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Miaolis.m4a', duration=300000))

        
    elif event.message.text =="桃竹苗天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+weather[4]+weather[5]+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/THM.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/THM.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]+weather[4]+weather[5]+weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/THM.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+weather[4]+weather[5]+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/THMs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/THMs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]+weather[4]+weather[5]+weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/THMs.m4a', duration=300000))

    elif event.message.text =="台中天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taichung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taichung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taichung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taichungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taichungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taichungs.m4a', duration=300000))


    elif event.message.text =="臺中天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taichung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taichung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taichung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taichungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taichungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taichungs.m4a', duration=300000))
    
        

    elif event.message.text =="彰化天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Changhua.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Changhua.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Changhua.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Changhuas.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Changhuas.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Changhuas.m4a', duration=300000))
        
        
    elif event.message.text =="南投天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Nantou.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Nantou.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Nantou.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Nantous.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Nantous.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Nantous.m4a', duration=300000))

        
    elif event.message.text =="雲林天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Yunlin.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Yunlin.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yunlin.m4a', duration=300000))
        except:        
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Yunlins.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Yunlins.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yunlins.m4a', duration=300000))

    elif event.message.text =="嘉義天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Chiayi.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Chiayi.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Chiayi.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Chiayis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Chiayis.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Chiayis.m4a', duration=300000))


    elif event.message.text =="宜蘭天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:                
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Yilan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Yilan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yilan.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Yilans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Yilans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yilans.m4a', duration=300000))

    elif event.message.text =="花蓮天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Hualie.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Hualie.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hualie.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Hualies.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Hualies.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hualies.m4a', duration=300000))
      
        
    elif event.message.text =="台東天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taitung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taitung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taitung.m4a', duration=300000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taitungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taitungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taitungs.m4a', duration=300000))        

    elif event.message.text =="臺東天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taitung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taitung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taitung.m4a', duration=300000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taitungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taitungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taitungs.m4a', duration=300000))        

    elif event.message.text =="花東天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Huatung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Huatung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]+weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Huatung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Huatungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Huatungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]+weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Huatungs.m4a', duration=300000))


    elif event.message.text =="台南天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Tainan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Tainan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Tainan.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Tainans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Tainans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Tainans.m4a', duration=300000))


    elif event.message.text =="臺南天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Tainan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Tainan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Tainan.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Tainans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Tainans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Tainans.m4a', duration=300000))
        

    elif event.message.text =="高雄天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Kaohsiung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Kaohsiung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kaohsiung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Kaohsiungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Kaohsiungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Kaohsiungs.m4a', duration=300000))

    elif event.message.text =="屏東天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Pingtung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Pingtung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Pingtung.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Pingtungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Pingtungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Pingtungs.m4a', duration=300000))
                    
    elif event.message.text =="連江天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Lienchiang.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Lienchiang.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Lienchiang.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Lienchiangs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Lienchiangs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Lienchiangs.m4a', duration=300000))

          
    elif event.message.text =="金門天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Kinmen.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Kinmen.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmen.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Kinmens.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Kinmens.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmens.m4a', duration=300000))

        
    elif event.message.text =="澎湖天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Penghu.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Penghu.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Penghu.m4a', duration=300000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Penghus.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Penghus.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Penghus.m4a', duration=300000))        
        
    elif event.message.text =="外島天氣":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+weather[20]+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/outerisland.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/outerisland.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]+weather[20]+weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/outerisland.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+weather[20]+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/outerislands.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/outerislands.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]+weather[20]+weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/outerislands.m4a', duration=300000))
        
    elif event.message.text =="停班停課":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        cancel=work_class_cancel_crawler_notebook.wkncls()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+cancel[0]+cancel[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/classcancel.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/classcancel.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cancel[0]+"\n"+cancel[1]+cancel[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/classcancel.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+cancel[0]+cancel[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/classcancels.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/classcancels.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cancel[0]+"\n"+cancel[1]+cancel[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/classcancels.m4a', duration=300000))

        
    elif event.message.text == "歌曲排行":
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/lQ2AiZb.jpg',
                title='歌曲排行',
                text='中文歌曲排行、西洋歌曲排行、日亞歌曲排行',
                actions=[
                    MessageAction(label='中文歌曲排行',text='中文歌曲排行'),
                    MessageAction(label='西洋歌曲排行',text='西洋歌曲排行'),
                    MessageAction(label='日亞歌曲排行',text='日亞歌曲排行')
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "中文歌曲排行":
        rank=song_crawler.ranking()
        rankCh='\n'.join(rank[:11])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankCh))
    elif event.message.text == "西洋歌曲排行":
        rank=song_crawler.ranking()
        rankwestern='\n'.join(rank[11:22])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankwestern))
    elif event.message.text == "日亞歌曲排行":
        rank=song_crawler.ranking()
        rankNEA='\n'.join(rank[-11:])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankNEA))

    elif event.message.text == "新聞":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        a=apple.apple_news()
        news_title=[]
        news_link=[]
        news_photo=[]    
        for i in range(0,len(a),3):   
            news_title.append(a[i])
            news_link.append(a[i+1])
            news_photo.append(a[i+2])

        news_group=[]    #創一個List
        #將剛剛的三個List加進來
        news_group.append(news_title)
        news_group.append(news_link)
        news_group.append(news_photo)
        #要做為key值的List
        x=['title','link','link2']
        #把兩個做成dictionary
        print("新聞幾個",len(news_title))
        dictionary = dict(zip(x,news_group))
        p=random.sample(range(len(news_title)),len(news_title))
        if len(news_title)>=10:
            try:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]+"第7"+dictionary['title'][p[6]]+"第8"+dictionary['title'][p[7]]+"第9"+dictionary['title'][p[8]]+"第10"+dictionary['title'][p[9]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('static/news.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(10000):
                            if block:
                                f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/news.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[6]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[6]],
                        label=dictionary['title'][p[6]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[7]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[7]],
                        label=dictionary['title'][p[7]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[8]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[8]],
                        label=dictionary['title'][p[8]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[9]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[9]],
                        label=dictionary['title'][p[9]][0:11]
                        )
                    )                
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/news.m4a', duration=300000))
            except:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]+"第7"+dictionary['title'][p[6]]+"第8"+dictionary['title'][p[7]]+"第9"+dictionary['title'][p[8]]+"第10"+dictionary['title'][p[9]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('staticss/newsss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(10000):
                            if block:
                                f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('staticss/newsss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[6]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[6]],
                        label=dictionary['title'][p[6]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[7]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[7]],
                        label=dictionary['title'][p[7]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[8]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[8]],
                        label=dictionary['title'][p[8]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[9]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[9]],
                        label=dictionary['title'][p[9]][0:11]
                        )
                    )                
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticss/newsss.m4a', duration=300000))
        else: #if len(news_title)<10 and len(news_title)>=6: else:
            try:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('statics/newss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(4096):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/newss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    )
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/newss.m4a', duration=300000))
            except:
                mes="今天的新聞第1."+dictionary['title'][p[0]]+"第2."+dictionary['title'][p[1]]+"第3."+dictionary['title'][p[2]]+"第4."+dictionary['title'][p[3]]+"第5."+dictionary['title'][p[4]]
                mess="第6"+dictionary['title'][p[5]]
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                with open('staticsss/newssss.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(4096):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('staticsss/newssss.m4a')
                mixer.music.play()
                Image_Carousel = TemplateSendMessage(
                alt_text='Image_Carousel_Template',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[0]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[0]],
                            label=dictionary['title'][p[0]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[1]],
                        action=URITemplateAction(
                            uri=dictionary['link'][p[1]],
                            label=dictionary['title'][p[1]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[2]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[2]],
                        label=dictionary['title'][p[2]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[3]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[3]],
                        label=dictionary['title'][p[3]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[4]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[4]],
                        label=dictionary['title'][p[4]][0:11]
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=dictionary['link2'][p[5]],
                        action=URITemplateAction(
                        uri=dictionary['link'][p[5]],
                        label=dictionary['title'][p[5]][0:11]
                        )
                    )
                ]))
                line_bot_api.reply_message(event.reply_token,Image_Carousel)
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticsss/newssss.m4a', duration=300000))        
    elif event.message.text == "電影":
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        
        a=movie_crawler.movie()
        movie_title=[]
        movie_link=[]
        movie_img=[]    
        for i in range(0,len(a),3):   
            movie_title.append(a[i])
            movie_link.append(a[i+1])
            movie_img.append(a[i+2])

        movie_group=[]    #創一個List
        #將剛剛的三個List加進來
        movie_group.append(movie_title)
        movie_group.append(movie_link)
        movie_group.append(movie_img)
        #要做為key值的List
        x=['title','link','link2']
        #把兩個做成dictionary
        dictionary = dict(zip(x,movie_group))
        #p=random.sample(range(12),3)
        mes="最新的電影有1."+dictionary['title'][0]+"2."+dictionary['title'][1]+"3."+dictionary['title'][2]+"4."+dictionary['title'][3]+"5."+dictionary['title'][4]
        mess="6."+dictionary['title'][5]+"7."+dictionary['title'][6]+"8."+dictionary['title'][7]+"9."+dictionary['title'][8]+"10."+dictionary['title'][10]
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+mess+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/movie.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/movie.m4a')
            mixer.music.play()
            
            Image_Carousel = TemplateSendMessage(
            alt_text='Image_Carousel_Template',
            template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url=dictionary['link2'][0],
                    action=URITemplateAction(
                        uri=dictionary['link'][0],
                        label=dictionary['title'][0][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][1],
                    action=URITemplateAction(
                        uri=dictionary['link'][1],
                        label=dictionary['title'][1][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][2],
                    action=URITemplateAction(
                        uri=dictionary['link'][2],
                        label=dictionary['title'][2][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][3],
                    action=URITemplateAction(
                        uri=dictionary['link'][3],
                        label=dictionary['title'][3][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][4],
                    action=URITemplateAction(
                        uri=dictionary['link'][4],
                        label=dictionary['title'][4][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][5],
                    action=URITemplateAction(
                        uri=dictionary['link'][5],
                        label=dictionary['title'][5][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][6],
                    action=URITemplateAction(
                        uri=dictionary['link'][6],
                        label=dictionary['title'][6][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][7],
                    action=URITemplateAction(
                        uri=dictionary['link'][7],
                        label=dictionary['title'][7][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][8],
                    action=URITemplateAction(
                    uri=dictionary['link'][8],
                    label=dictionary['title'][8][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][9],
                    action=URITemplateAction(
                    uri=dictionary['link'][9],
                    label=dictionary['title'][9][0:11]
                    )
                )
        
                ]))
            line_bot_api.reply_message(event.reply_token,Image_Carousel)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/movie.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+mess+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/movies.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/movies.m4a')
            mixer.music.play()
            
            Image_Carousel = TemplateSendMessage(
            alt_text='Image_Carousel_Template',
            template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url=dictionary['link2'][0],
                    action=URITemplateAction(
                        uri=dictionary['link'][0],
                        label=dictionary['title'][0][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][1],
                    action=URITemplateAction(
                        uri=dictionary['link'][1],
                        label=dictionary['title'][1][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][2],
                    action=URITemplateAction(
                        uri=dictionary['link'][2],
                        label=dictionary['title'][2][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][3],
                    action=URITemplateAction(
                        uri=dictionary['link'][3],
                        label=dictionary['title'][3][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][4],
                    action=URITemplateAction(
                        uri=dictionary['link'][4],
                        label=dictionary['title'][4][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][5],
                    action=URITemplateAction(
                        uri=dictionary['link'][5],
                        label=dictionary['title'][5][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][6],
                    action=URITemplateAction(
                        uri=dictionary['link'][6],
                        label=dictionary['title'][6][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][7],
                    action=URITemplateAction(
                        uri=dictionary['link'][7],
                        label=dictionary['title'][7][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][8],
                    action=URITemplateAction(
                    uri=dictionary['link'][8],
                    label=dictionary['title'][8][0:11]
                    )
                ),
                ImageCarouselColumn(
                    image_url=dictionary['link2'][9],
                    action=URITemplateAction(
                    uri=dictionary['link'][9],
                    label=dictionary['title'][9][0:11]
                    )
                )
        
                ]))
            line_bot_api.reply_message(event.reply_token,Image_Carousel)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/movies.m4a', duration=300000))

    elif event.message.text == "功能":
        #message="ESLAB有以下功能\n0.功能:\n  輸入後可查詢功能\n1.貼圖\n2.時間\n3.發票\n4.油價\n5.國際油價\n6.電\n7.水庫\n8.天氣\n9.停班停課\n10.歌曲排行\n11.新聞\n12.電影\n13.記帳\n14.主動傳訊息(每10秒)\n15.實驗室"
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，如只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oInstruction.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            
            
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oInstructions.m4a', duration=300000))

    elif event.message.text == "？":
        #message="ESLAB有以下功能\n0.功能:\n  輸入後可查詢功能\n1.貼圖\n2.時間\n3.發票\n4.油價\n5.國際油價\n6.電\n7.水庫\n8.天氣\n9.停班停課\n10.歌曲排行\n11.新聞\n12.電影\n13.記帳\n14.主動傳訊息(每10秒)\n15.實驗室"
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，如只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oInstruction.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

           
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oInstructions.m4a', duration=300000))

    elif event.message.text == "?":
        #message="ESLAB有以下功能\n0.功能:\n  輸入後可查詢功能\n1.貼圖\n2.時間\n3.發票\n4.油價\n5.國際油價\n6.電\n7.水庫\n8.天氣\n9.停班停課\n10.歌曲排行\n11.新聞\n12.電影\n13.記帳\n14.主動傳訊息(每10秒)\n15.實驗室"
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，如只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='代傳訊息操作',text='代傳訊息操作'),
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oInstruction.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我要加入代傳訊息服務、代傳訊息操作、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

           
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oInstructions.m4a', duration=300000))
#第二，手機語音輸入我要加入代傳訊息服務，接著，傳Line給小明冒號你好嗎，即可傳送，


    elif event.message.text == "語音功能":
        mes='''語音功能介紹:第一，請輸入停，即可停止語音，暫停，即可暫停，繼續，即可繼續，第二，手機語音輸入我要加入代傳訊息服務，接著，傳Line給小明冒號你好嗎，即可傳送，
        第三，如想知道天氣請輸入縣市天氣如，台南天氣，第四，輸入實驗室PM 2點5，實驗室揮發性有機物，實驗室甲醛，實驗室二氧化碳，
        實驗室溫度，實驗室相對濕度，即可得室內資訊'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Instruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Instruction.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url=webhook_url+'/static/Instruction.m4a', duration=800000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Instructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(2048):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Instructions.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url=webhook_url+'/statics/Instructions.m4a', duration=800000))


    elif event.message.text == "主動傳訊息":
        carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(                        
                    title='主動傳訊息',text='主動傳停班停課、主動傳Hello World、刪除主動傳訊息',
                    actions=[
                        MessageAction(label='主動傳停班停課',text='主動傳停班停課'),                            
                        MessageAction(label='主動傳Hello World',text='主動傳Hello World'),
                        MessageAction(label='刪除主動傳訊息',text='刪除主動傳訊息')
                        ]
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    elif event.message.text == "主動傳停班停課":
        global c1
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        c1=client
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息開啟'))
        scheduler.add_job(t1, 'interval', seconds=10,id='t1')#這裡設定時間，只有在第一次傳送訊息後 才會開始主動回訊息hour='0-9', minute="*"
        scheduler.start()#scheduler.add_job(要執行的程式, 'interval', seconds=10,id='t1')
    elif event.message.text == "主動傳Hello World":
        global c2
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        c2=client
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息開啟'))
        scheduler.add_job(t2, 'interval', seconds=10,id='t2')#這裡設定時間，只有在第一次傳送訊息後 才會開始主動回訊息hour='0-9', minute="*"
        scheduler.start()#scheduler.add_job(要執行的程式, 'interval', seconds=10,id='t1')
    
    elif event.message.text == "刪除主動傳訊息":
        try:
            scheduler.remove_job('t1')#此功能正確    scheduler.remove_job('這裡放id')
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息關閉'))
        except:
            scheduler.remove_job('t2')
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息關閉'))
    #elif event.message.text == "刪除主動傳訊息":
        #scheduler.remove_job('t1')#此功能正確    scheduler.remove_job('這裡放id')
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息關閉'))




        
    elif event.message.text =="實驗室":
        b=request.get_data(as_text=True)       
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='歡迎來404實驗室點擊PM 2點5，揮發性有機物，甲醛，二氧化碳，溫度，相對濕度，即可得到室內資訊'
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/lab.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/lab.m4a')
            mixer.music.play()

            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                            title='歡迎來到404實驗室',
                            text='PM2.5、揮發性有機物、甲醛',
                            actions=[
                                PostbackAction(label='PM2.5', data='PM2.5'),
                                PostbackAction(label='揮發性有機物', data='揮發性有機物'),
                                PostbackAction(label='甲醛', data='甲醛')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                            title='歡迎來到404實驗室',
                            text='二氧化碳、溫度、濕度',
                            actions=[
                                PostbackAction(label='二氧化碳', data='二氧化碳'),
                                PostbackAction(label='溫度', data='溫度'),
                                PostbackAction(label='相對濕度', data='相對濕度')
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/lab.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/labs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/labs.m4a')
            mixer.music.play()

            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                            title='歡迎來到404實驗室',
                            text='PM2.5、揮發性有機物、甲醛',
                            actions=[
                                PostbackAction(label='PM2.5', data='PM2.5'),
                                PostbackAction(label='揮發性有機物', data='揮發性有機物'),
                                PostbackAction(label='甲醛', data='甲醛')
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                            title='歡迎來到404實驗室',
                            text='二氧化碳、溫度、濕度',
                            actions=[
                                PostbackAction(label='二氧化碳', data='二氧化碳'),
                                PostbackAction(label='溫度', data='溫度'),
                                PostbackAction(label='相對濕度', data='相對濕度')
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/labs.m4a', duration=300000))

    elif event.message.text == '實驗室PM2.5':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/PM25.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/PM25.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PM25.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值 "+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/PM25s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/PM25s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PM25s.m4a', duration=300000))

    elif event.message.text == '實驗室pm2.5':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/PM25.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/PM25.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PM25.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值 "+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/PM25s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/PM25s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PM25s.m4a', duration=300000))

    elif event.message.text == '實驗室PM 2.5':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/PM25.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/PM25.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PM25.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/PM25s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/PM25s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PM25s.m4a', duration=300000))


    elif event.message.text == '實驗室揮發性有機物':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/TVOC.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/TVOC.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/TVOC.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/TVOCs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/TVOCs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/TVOCs.m4a', duration=300000))

    elif event.message.text == '實驗室甲醛':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/HCHO.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/HCHO.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/HCHO.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/HCHOs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/HCHOs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/HCHOs.m4a', duration=300000))

    elif event.message.text == '實驗室二氧化碳':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/CO2.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/CO2.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/CO2.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/CO2s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/CO2s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/CO2s.m4a', duration=300000))

    elif event.message.text == '實驗室溫度':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/tem.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/tem.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/tem.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/tems.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/tems.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/tems.m4a', duration=300000))

    elif event.message.text == '實驗室相對濕度':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/hum.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/hum.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hum.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/hums.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/hums.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hums.m4a', duration=300000))
    elif event.message.text == '實驗室濕度':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/hum.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/hum.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hum.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/hums.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/hums.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hums.m4a', duration=300000))








    elif re.findall('^記帳.*?',event.message.text):        
        message=event.message.text        
        #global z #查ID應該會爆
        b=request.get_data(as_text=True)            
        #profile = line_bot_api.get_profile(event.source)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        
        #z=client
        #print("z",z)
        #####
        #session['session_name']=client
        #print("唯一名稱:",client)
        if message =='記帳方式':
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='輸入方式:\n記帳 80 雞排\n記帳 80\n刪除:\n刪除記帳 編號\n修改:\n修改金額 編號 新金額 \n修改項目 編號 新項目'))    
        
        elif re.findall('^記帳 *?[0-9]+.*?',message):#其他地方變數禁止使用 money date_now thing   z
            print("message",message) 
            #global month
            #global thing
            #global money
            #global date_now
            print(message)
            a=request.get_data(as_text=True)            
            #profile = line_bot_api.get_profile(event.source)
            if re.findall('roomId":"(.*?)"',a):
                client_id=''.join(re.findall('roomId":"(.*?)"',a))
            elif re.findall('groupId":"(.*?)"',a):
                client_id=''.join(re.findall('groupId":"(.*?)"',a))     
            else:
                client_id=''.join(re.findall('userId":"(.*?)"',a))


            print("唯一名稱:",client_id)        
            
            
            x=re.findall('^記帳 *?([0-9]+)',message)
            y=re.findall('\D',message)
            money=''.join(x)
            thing=''.join(y).strip("記帳 ")            
            date_now = datetime.now().strftime('%Y/%m/%d')
            date_nows = datetime.now().strftime('%Y-%m-%d')
            month = ''.join(re.findall('/([0-9]+)/',date_now))
            #print(date_nows)
            if thing == "":
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='已增加此花費\n金額:'+money+'元，請選擇項目',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="取消", data="取消")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="飲食", data="飲食 "+str(money))#+str(money)
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="生活", data="生活 "+str(money))
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="交通", data="交通 "+str(money))
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="娛樂", data="娛樂 "+str(money))
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="醫療", data="醫療 "+str(money))
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="住宿", data="住宿 "+str(money))
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="其他", data="其他 "+str(money))
                            ),
                            ])))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='是否確認增加此花費\n金額:'+ money+'元\n日期:'+date_now+'\n備註:'+thing,
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(label="確認", data="確認 "+str(money)+" "+str(thing))
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(label="取消", data="取消")
                                ),
                                ])))        
        else:
            #global z 
            b=request.get_data(as_text=True)
            if re.findall('roomId":"(.*?)"',b):
                client=''.join(re.findall('roomId":"(.*?)"',b))
            elif re.findall('groupId":"(.*?)"',b):
                client=''.join(re.findall('groupId":"(.*?)"',b))     
            else:
                client=''.join(re.findall('userId":"(.*?)"',b))
                
            #URIAction(label='查詢所有記帳(含編號)', uri=webhook_url+'/account')    
            #print(client)
            #z=client
            session['session_name']=client
            print("唯一名稱:",client)
            carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                        title='歡迎使用ESLAB記帳小幫手(群組記帳與個人記帳為分開)',
                        text='初次使用請觀看下方說明',
                        actions=[
                            MessageAction(label='本月所有消費紀錄', text='本月所有消費紀錄'),                            
                            MessageAction(label='本月花費的總金額', text='本月花費的總金額'),
                            MessageAction(label='查詢所有記帳(含編號)', text='查詢所有記帳')
                            #PostbackAction(label='查詢所有記帳(含編號)', data='查詢所有記帳')                            
                            #URIAction(label='查詢所有記帳(含編號)', uri=url_for('account')
                            #URIAction(label='查詢所有記帳(含編號)', uri=webhook_url+'/account')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                        title='歡迎使用ESLAB記帳小幫手(群組記帳與個人記帳為分開)',
                        text='初次使用請觀看下方說明',
                        actions=[
                            MessageAction(label='查詢編號(最後5個)', text='查詢編號'),                            
                            MessageAction(label='刪除最後一筆記帳', text='刪除最後一筆記帳'),
                            MessageAction(label='修改記帳', text='修改記帳方式請輸入:\n修改金額 編號 新金額 \n修改項目 編號 新項目')
                        ]
                    )
                ]))
                    
            
            
            #line_bot_api.reply_message(event.reply_token, buttons_template_message)
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text='輸入方式:\n記帳 80 雞排\n記帳 80\n刪除:\n刪除記帳 編號\n修改:\n修改金額 編號 新金額 \n修改項目 編號 新項目'))
            #x="歡迎使用ESLAB記帳小幫手請輸入:\n記帳 80 雞排"#這裡改按鈕刪除最後一筆記帳 查詢編號(最後5個) 查詢所有編號 本月所有消費紀錄#mounth=.strftime('%Y-%m-%d')
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=x))
            

    elif re.findall('^刪除記帳 [0-9]+',event.message.text):
        a=request.get_data(as_text=True)
        print("aaaa",a)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
            print("A")
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))
            print("B")
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
            print("C")
        
        print("client_id",client_id)
        message=event.message.text
        x=re.findall('刪除記帳 ([0-9]+)',message)
        #y=re.findall('\D',a)
        #print(x)
        #print(y)
        number=''.join(x)
        #money=''.join(x)
        #thing=''.join(y).strip("記帳 ")
        print(number)
        #print(thing)
        try:
            cursor.execute("SELECT * FROM "+client_id+" WHERE number ="+ str(number)+"")
            for row in cursor.fetchall():            
                moneys=int(row[1])
                things=(row[2])
                dates=(row[3])

            #print(moneys)
            #print(things)
            #print(dates)
            mesg="已刪除:"+str(things)+":"+str(moneys)+"元"+"\n日期:"+str(dates)
            print(mesg)
            cursor.execute("DELETE FROM "+client_id+" WHERE number = "+ str(number)+"")
            db.commit()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))
        except Exception:
            print("此編號不存在")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號"+str(number)+"不存在,請重新確認歐"))
            
    elif event.message.text == '刪除最後一筆記帳':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        
        cursor.execute("SELECT * FROM "+client_id+" order by number desc limit 1")
        listmoney=[]
        listthing=[]
        listdate=[]
        for row in cursor.fetchall():    
            listmoney.append(int(row[1]))
            listthing.append(row[2])
            listdate.append(row[3].strftime('%Y/%m/%d'))
                        
        moneys=(''.join(str(listmoney)).strip("[]"))              
        things=''.join(listthing)
        date_nows=''.join(listdate)
        cursor.execute("DELETE FROM "+client_id+" order by number desc limit 1")
        db.commit()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已刪除:'+things+":"+moneys+"元\n日期:"+date_nows))

    elif re.findall('^修改金額',event.message.text):
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))        
        
        number=''.join(re.findall('^修改金額 ([0-9]+) [0-9]+',event.message.text))
        newmoney=''.join(re.findall('^修改金額 [0-9]+ ([0-9]+)',event.message.text))
        print("編號",number)
        print("新金額:",newmoney)
        listnumber=[]
        listmoney=[]
        listthing=[]
        listdate=[]
        try:
            cursor.execute("SELECT * FROM "+client_id+" WHERE number ="+ str(number)+"")    
            for row in cursor.fetchall():        
                listmoney.append(int(row[1]))
                listthing.append(row[2])
                listdate.append(row[3].strftime('%Y/%m/%d'))
            
            omoney=(''.join(str(listmoney)).strip("[]"))
            things=''.join(listthing)
            date=''.join(listdate)
            print("舊金額",omoney)
            print("項目:",things)
            print("日期",date)
            if omoney=="":
                db.close
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號輸入錯誤"))
                
            else:
                cursor.execute("UPDATE "+client_id+" SET money = "+str(newmoney)+" WHERE number ="+ str(number)+"")
                db.commit()
                mesg="已將編號:\n"+number+":"+things+"\n金額:"+omoney+"元 \n日期:"+date+"\n修改成:\n"+number+":"+things+"\n金額:"+newmoney+"元 \n日期:"+date
                
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))
        except Exception:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入格式錯誤\n修改方式:\n修改金額 編號 新金額"))
            #print("格式不正確")
    elif re.findall('^修改項目',event.message.text):
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        number=''.join(re.findall('^修改項目 ([0-9]+)',event.message.text))
        #x=re.findall('^修改項目 [0-9]+ (\w+)',message)
        #print(x)
        newthing=''.join(re.findall('^修改項目 [0-9]+ (\w+)',event.message.text))
        print("編號",number)
        print("新項目:",newthing)
        listnumber=[]
        listmoney=[]
        listthing=[]
        listdate=[]
        try:
            cursor.execute("SELECT * FROM "+client_id+" WHERE number ="+ str(number)+"")    
            for row in cursor.fetchall():        
                listmoney.append(int(row[1]))
                listthing.append(row[2])
                listdate.append(row[3].strftime('%Y/%m/%d'))
                
            money=(''.join(str(listmoney)).strip("[]"))
            othing=''.join(listthing)
            date=''.join(listdate)
            print("金額",money)
            print("舊項目:",othing)
            print("日期",date)
            if othing=="":
                db.close
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號輸入錯誤"))
            else:
                cursor.execute("UPDATE "+client_id+" SET thing = '"+str(newthing)+"' WHERE number ="+ str(number)+"")
                db.commit()
                print("已將編號:\n"+number+":"+othing+"\n金額:"+money+":"+date+"\n修改成:\n"+number+":"+newthing+"\n金額:"+money+"元 日期:"+date)
                mesg="已將編號:\n"+number+":"+othing+"\n金額:"+money+":"+date+"\n修改成:\n"+number+":"+newthing+"\n金額:"+money+"元 日期:"+date
                db.close
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))
        except Exception:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入格式錯誤\n修改方式:\n修改項目 編號 新項目"))
    
    elif re.findall('請輸入',event.message.text):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="   "))

        
    elif event.message.text == '本月所有消費紀錄':
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        
        cursor.execute("SELECT * FROM "+client_id+" WHERE month ="+ str(month)+" and year = "+ str(year)+"")
        listmoney=[]
        listthing=[]
        listdate=[]
        for row in cursor.fetchall():    
            listmoney.append(int(row[1]))
            listthing.append(row[2])
            listdate.append(row[3].strftime('%Y/%m/%d'))
   
        mes=[]
        a=0
        for i in range(0,len(listmoney)):
            #mes.append("金額:"+str(listmoney[i])+"date:"+str(listdate[i])+" 項目:"+str(listthing[i]))
            mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i]))
            a=a+listmoney[i]
            #print(a)
            #mes.append(listmoney[i]+listthing[i]+listdate[i]+"\n")
        #print(mes)
        print('總金額',a)
        mesg='\n'.join(mes)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(year)+"年"+str(month)+"月總消費\n金額:"+str(a)+"元\n清單如下:\n"+mesg))
    elif event.message.text == '查詢編號':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))        
        
        cursor.execute("SELECT * FROM "+client_id+" order by number desc limit 5")
        listnumber=[]
        listmoney=[]
        listthing=[]
        listdate=[]
        for row in cursor.fetchall():            
            listnumber.append(int(row[0]))
            listmoney.append(int(row[1]))
            listthing.append(row[2])
            listdate.append(row[3].strftime('%Y/%m/%d'))
   
        mes=[]
        if len(listnumber)>5:
            for i in range(0,5):
                #mes.append("金額:"+str(listmoney[i])+"date:"+str(listdate[i])+" 項目:"+str(listthing[i]))
                mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i])+"編號"+str(listnumber[i]))
            mesg='\n\n'.join(mes)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))
        elif len(listnumber)==0:
            nomesg="趕快來記帳吧!!"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=nomesg))
        else:
            for i in range(0,len(listnumber)):
                #mes.append("金額:"+str(listmoney[i])+"date:"+str(listdate[i])+" 項目:"+str(listthing[i]))
                mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i])+"編號"+str(listnumber[i]))
            mesg='\n\n'.join(mes)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))

    elif event.message.text == '本月花費的總金額':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month

        cursor.execute("SELECT * FROM "+client_id+" WHERE month ="+ str(month)+" and year = "+ str(year)+"")
        listmoney=[]
        listthing=[]
        listdate=[]
        for row in cursor.fetchall():    
            listmoney.append(int(row[1]))
            listthing.append(row[2])
            listdate.append(row[3].strftime('%Y/%m/%d'))        
        a=0
        for i in range(0,len(listmoney)):                        
            a=a+listmoney[i]
        print('總金額',a)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(year)+"年"+str(month)+"月總消費\n金額:"+str(a)+"元"))
    elif event.message.text =='查詢所有記帳':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))        

        cursor.execute("SELECT * FROM "+client_id+"")
        listnumber=[]
        listmoney=[]
        listthing=[]
        listdate=[]
        for row in cursor.fetchall():            
            listnumber.append(int(row[0]))
            listmoney.append(int(row[1]))
            listthing.append(row[2])
            listdate.append(row[3].strftime('%Y/%m/%d'))
        
        mes=[]
        for i in range(0,len(listnumber)):
            mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i])+"編號"+str(listnumber[i]))
        mesg='\n\n'.join(mes)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))


    elif event.message.text == '停':
        mixer.music.stop()
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已停止播放"))

    elif event.message.text == '暫停':
        mixer.music.pause()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已暫停播放"))
    elif event.message.text == '繼續':
        mixer.music.unpause()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已繼續播放"))    
    else:
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        
        
        google_url = 'https://www.google.com.tw/search'
        # 查詢參數
        my_params = {'q': event.message.text}
        # 下載 Google 搜尋結果
        r = requests.get(google_url, params = my_params)
        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 原始碼
            soup = BeautifulSoup(r.text, 'html.parser')
            #print(soup)
            # 觀察 HTML 原始碼
            #print(soup.prettify())

            # 以 CSS 的選擇器來抓取 Google 的搜尋結果
            items = soup.select('div.g > h3.r > a[href^="/url"]')
            #print(items)
            list_google=[]
            list_title=[]
            print("item",len(items))
            x=1
            k=[]
            ks=[]
            for i in items:        
                    
                # 標題
                #print("標題：" + i.text)
                title="標題：" + i.text
                list_google.append(title)
                #j=","
                titles=str(x)+","+ str(i.text)
                list_title.append(titles)
                # 網址
                #print("網址：" + i.get('href'))
                url="網址：" + i.get('href').strip("/url?q=")
                list_google.append(url)        
                key=re.findall('(.*?)- 维基百科',i.text)
                keys=re.findall('(.*?)- 維基百科',i.text)                
                k.append(key)
                ks.append(keys)        
                x=x+1
                if x>4:
                    break
                        
                #print(title)
                #print(url)
                #print(list_google)
            google='\n'.join(list_google)
            only_title=','.join(list_title)
            keyword=''.join(str(k)).strip(",' []")
            keywords=''.join(str(ks)).strip(",' []")
            try:
                if keyword!="":
                    try:
                        print("1")
                        term=keyword        
                        print(term)        
                        res = requests.get('https://zh.wikipedia.org/zh-tw/{}'.format(term))
                        soup = BeautifulSoup(res.text, 'lxml')        
                        article = soup.select_one('.mw-parser-output p').text
                        print(article)
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+article[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/goo.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass

                    except:
                        article=""
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('static/goo.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                    mixer.init()
                    mixer.music.load('static/goo.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+article+"\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/goo.m4a', duration=800000))

                elif keywords!="":
                    try:
                        print("2")
                        term=keywords       
                        print(term)        
                        res = requests.get('https://zh.wikipedia.org/zh-tw/{}'.format(term))
                        soup = BeautifulSoup(res.text, 'lxml')        
                        article = soup.select_one('.mw-parser-output p').text
                        print(article)
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+article[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/goos.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass

                    except:
                        article=""
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('statics/goos.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                    mixer.init()
                    mixer.music.load('statics/goos.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+article+"\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/goos.m4a', duration=800000))

                else:
                    print(only_title)
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('static/goo.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('static/goo.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/goo.m4a', duration=800000))
            except:
                if keyword!="":
                    try:
                        print("3")
                        term=keyword        
                        print(term)        
                        res = requests.get('https://zh.wikipedia.org/zh-tw/{}'.format(term))
                        soup = BeautifulSoup(res.text, 'lxml')        
                        article = soup.select_one('.mw-parser-output p').text
                        print(article)
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+article[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('staticss/gooss.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass

                    except:
                        article=""
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('staticss/gooss.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                    mixer.init()
                    mixer.music.load('staticss/gooss.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+article+"\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticss/gooss.m4a', duration=800000))

                elif keywords!="":
                    try:
                        print("4")
                        term=keywords       
                        print(term)        
                        res = requests.get('https://zh.wikipedia.org/zh-tw/{}'.format(term))
                        soup = BeautifulSoup(res.text, 'lxml')        
                        article = soup.select_one('.mw-parser-output p').text
                        print(article)
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+article[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('staticsss/goosss.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass

                    except:
                        article=""
                        print(only_title)
                        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                        r = requests.get(stream_url, stream=True)
                        with open('staticsss/goosss.m4a', 'wb') as f:
                            try:
                                for block in r.iter_content(1024):
                                    f.write(block)
                                f.close()
                            except KeyboardInterrupt:
                                pass
                    mixer.init()
                    mixer.music.load('staticsss/goosss.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+article+"\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/staticsss/goosss.m4a', duration=800000))

                else:
                    print(only_title)
                    stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title[:200]+'&language=zh-tw'
                    r = requests.get(stream_url, stream=True)
                    with open('statica/gooa.m4a', 'wb') as f:
                        try:
                            for block in r.iter_content(1024):
                                f.write(block)
                            f.close()
                        except KeyboardInterrupt:
                            pass
                    mixer.init()
                    mixer.music.load('statica/gooa.m4a')
                    mixer.music.play()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))
                    line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statica/gooa.m4a', duration=800000))
            
                

                        
                #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))

'''                
            try:
                google='\n'.join(list_google)
                only_title=','.join(list_title)
                print(only_title)
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                #x= ['static','statics']
            
                with open('static/goo.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('static/goo.m4a')
                mixer.music.play()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/goo.m4a', duration=100000))

            except:
                google='\n'.join(list_google)
                only_title=','.join(list_title)
                print(only_title)
                stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+only_title+'&language=zh-tw'
                r = requests.get(stream_url, stream=True)
                #x= ['static','statics']

                with open('statics/goos.m4a', 'wb') as f:
                    try:
                        for block in r.iter_content(1024):
                            f.write(block)
                        f.close()
                    except KeyboardInterrupt:
                        pass
                mixer.init()
                mixer.music.load('statics/goos.m4a')
                mixer.music.play()         
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))
                line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/goos.m4a', duration=100000))
'''


            

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    #sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
    #               107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
    #               126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    #index_id = random.randint(0, len(sticker_ids) - 1)
    #sticker_id = str(sticker_ids[index_id])
    #print(index_id)
    sticker_message = StickerSendMessage(
        package_id=event.message.package_id,
        sticker_id=event.message.sticker_id
    )
    
    line_bot_api.reply_message(event.reply_token,sticker_message)

@handler.add(PostbackEvent)#只回復postback的訊息
def handle_postback(event):
    if event.postback.data == 'PM2.5':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/PM25.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/PM25.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/PM25.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內pm2點5數值"+PTQS[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/PM25s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/PM25s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內pm2.5:"+PTQS[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/PM25s.m4a', duration=100000))

    elif event.postback.data == '揮發性有機物':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/TVOC.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/TVOC.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/TVOC.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/TVOCs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/TVOCs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/TVOCs.m4a', duration=100000))
    elif event.postback.data == '甲醛':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/HCHO.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/HCHO.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/HCHO.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/HCHOs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/HCHOs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/HCHOs.m4a', duration=100000))

    elif event.postback.data == '二氧化碳':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/CO2.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/CO2.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/CO2.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/CO2s.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/CO2s.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/CO2s.m4a', duration=100000))
            
    elif event.postback.data == '溫度':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/tem.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/tem.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/tem.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[4]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/tems.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/tems.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[4]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/tems.m4a', duration=100000))

    elif event.postback.data == '相對濕度':
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        PTQS=PTQS1005.ptq()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/hum.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/hum.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/hum.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+"室內"+PTQS[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/hums.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/hums.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("室內"+PTQS[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/hums.m4a', duration=100000))
        

    elif event.postback.data == '取消':        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已取消此筆記帳"))
    elif re.findall('^確認 [0-9]+ \D+',event.postback.data): 
        
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        #print("年份"+str(year)+"月份"+str(month))        
        money= ''.join(re.findall('^確認 ([0-9]+)',event.postback.data))
        y=re.findall('\D',event.postback.data)            
        thing=''.join(y).strip("確認 ")#底下還要多創建一個年份year，不然明年會掛掉
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '" + str(thing) + "','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))


        buttons_template_message=TemplateSendMessage(  #本月所有消費紀錄 還要加總額
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                #title='已記帳:'+thing+':'+money+'元',text='', actions=[
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text=thing+":"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新金額'),                       
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        db.close
        
        
    elif re.findall('^飲食 [0-9]+',event.postback.data):
    #elif event.postback.data == '飲食': 
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^飲食 ([0-9]+)',event.postback.data))
        print(money)   
        print(client_id)    

        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '飲食','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #這裡改POST 要修改項目會金額 難寫囉
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="飲食:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    elif re.findall('^生活 [0-9]+',event.postback.data):
    #elif event.postback.data == '生活': #這裡可以直接拿money和 date_now       
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^生活 ([0-9]+)',event.postback.data))
        
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '生活','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage( #這裡改POST 要修改項目會金額 難寫囉
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="生活:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)


    elif re.findall('^交通 [0-9]+',event.postback.data):          
    #elif event.postback.data == '交通': #這裡可以直接拿money和 date_now
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^交通 ([0-9]+)',event.postback.data))
        
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '交通','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #這裡改POST 要修改項目會金額 難寫囉
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="交通:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close    
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
                    
    elif re.findall('^娛樂 [0-9]+',event.postback.data):
    #elif event.postback.data == '娛樂': #這裡可以直接拿money和 date_now
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^娛樂 ([0-9]+)',event.postback.data))
        
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '娛樂','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        
        buttons_template_message=TemplateSendMessage(  #本月所有消費紀錄 還要加總額
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="娛樂:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)


    elif re.findall('^醫療 [0-9]+',event.postback.data):
    #elif event.postback.data == '醫療': #這裡可以直接拿money和 date_now
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^醫療 ([0-9]+)',event.postback.data))
        
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '醫療','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月所有消費紀錄 還要加總額
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="醫療:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)


    elif re.findall('^住宿 [0-9]+',event.postback.data):
    #elif event.postback.data == '住宿': #這裡可以直接拿money和 date_now
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
            
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^住宿 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '住宿','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月所有消費紀錄 還要加總額
            
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="住宿:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                    ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)        
        
    elif re.findall('^其他 [0-9]+',event.postback.data):
    #elif event.postback.data == '其他': #這裡可以直接拿money和 date_now
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
            
        today = datetime.now()
        date_nows = today.strftime('%Y-%m-%d')
        date_now=today.strftime('%Y/%m/%d')
        year = today.year
        month = today.month
        money= ''.join(re.findall('^其他 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT,year INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month,year) VALUES (" + str(money) + ", '其他','" + str(date_nows) + "'," + str(month) + "," + str(year) + ")")
        db.commit() 
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月所有消費紀錄 還要加總額
           
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/W4XKQ0F.png',
                title='已記帳:(小提醒如果群組或聊天室記帳是群組或聊天室非個人)', text="其他:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                MessageAction(label='修改此項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                MessageAction(label='修改此金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                MessageAction(label='刪除此筆', text='刪除記帳 '+ str(number)),
                MessageAction(label='本月花費的總金額', text='本月花費的總金額')
                ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    #if event.message.address
    if re.findall('基隆',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()        
        try:        
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Keelung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Keelung.m4a')
            mixer.music.play()            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Keelung.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[0]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Keelungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Keelungs.m4a')
            mixer.music.play()            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Keelungs.m4a', duration=100000))
    elif re.findall('台北',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=100000))
    elif re.findall('臺北',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[1]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taipei.m4a')
            mixer.music.play() 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taipei.m4a', duration=100000))
    elif re.findall('新北',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))        
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/NTaipei.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/NTaipei.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/NTaipei.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[2]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/NTaipeis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/NTaipeis.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/NTaipeis.m4a', duration=100000))
    elif re.findall('桃園',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taoyuan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taoyuan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taoyuan.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[3]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taoyuans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taoyuans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taoyuans.m4a', duration=100000))
    elif re.findall('新竹',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Hsinchu.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Hsinchu.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hsinchu.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[4]+weather[5]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Hsinchus.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Hsinchus.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hsinchus.m4a', duration=100000))
    elif re.findall('苗栗',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Miaoli.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Miaoli.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Miaoli.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[6]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Miaolis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Miaolism4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Miaolis.m4a', duration=100000))
    elif re.findall('台中',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taichung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taichung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taichung.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taichungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taichungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taichungs.m4a', duration=100000))
    elif re.findall('臺中',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taichung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taichung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taichung.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[7]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taichungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taichungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taichungs.m4a', duration=100000))
    elif re.findall('彰化',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Changhua.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Changhua.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Changhua.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[8]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Changhuas.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Changhuas.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Changhuas.m4a', duration=100000))
    elif re.findall('南投',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Nantou.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Nantou.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Nantou.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[9]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Nantous.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Nantous.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Nantous.m4a', duration=100000))
    elif re.findall('雲林',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))     
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Yunlin.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Yunlin.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yunlin.m4a', duration=100000))
        except:        
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[10]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Yunlins.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Yunlins.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yunlins.m4a', duration=100000))
    elif re.findall('嘉義',event.message.address):  
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Chiayi.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Chiayi.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Chiayi.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[11]+weather[12]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Chiayis.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Chiayis.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Chiayis.m4a', duration=100000))
    elif re.findall('宜蘭',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()                
        try:                
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Yilan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Yilan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Yilan.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[13]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Yilans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Yilans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Yilans.m4a', duration=100000))
    elif re.findall('花蓮',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Hualie.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Hualie.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Hualie.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[14]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Hualies.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Hualies.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Hualies.m4a', duration=100000))
    elif re.findall('台東',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taitung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taitung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taitung.m4a', duration=100000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taitungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taitungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taitungs.m4a', duration=100000))        
    
    elif re.findall('臺東',event.message.address):    
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Taitung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Taitung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Taitung.m4a', duration=100000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[15]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Taitungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Taitungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Taitungs.m4a', duration=100000))        

    elif re.findall('台南',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Tainan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Tainan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Tainan.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Tainans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Tainans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Tainans.m4a', duration=100000))

    elif re.findall('臺南',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Tainan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Tainan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Tainan.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[16]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Tainans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Tainans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Tainans.m4a', duration=100000))

    elif re.findall('高雄',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Kaohsiung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Kaohsiung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kaohsiung.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[17]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Kaohsiungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Kaohsiungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Kaohsiungs.m4a', duration=100000))

    elif re.findall('屏東',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Pingtung.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Pingtung.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Pingtung.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[18]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Pingtungs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Pingtungs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Pingtungs.m4a', duration=100000))

    elif re.findall('連江',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Lienchiang.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Lienchiang.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Lienchiang.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[19]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Lienchiangs.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Lienchiangs.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Lienchiangs.m4a', duration=100000))

    elif re.findall('金門',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Kinmen.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Kinmen.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmen.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[20]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Kinmens.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Kinmens.m4a')
            mixer.music.play()        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Kinmens.m4a', duration=100000))

    elif re.findall('澎湖',event.message.address):
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        weather=weather_data.weather()
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/Penghu.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/Penghu.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/Penghu.m4a', duration=100000))        
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+weather[21]+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/Penghus.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/Penghus.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/Penghus.m4a', duration=100000))        
    else:
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes="你的位置可能不再台灣歐"
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/not_in_taiwan.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/not_in_taiwan.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/not_in_taiwan.m4a', duration=100000))   
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/not_in_taiwans.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/not_in_taiwans.m4a')
            mixer.music.play()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mes))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/not_in_taiwans.m4a', duration=100000))   
        
    
'''
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.type, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )
'''



@handler.add(FollowEvent)
def handle_follow(event):#剛加入好友會跳出的功能
        print("加入追蹤")
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，如只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/oInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/oInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='請先觀看代傳訊息操作再加入代傳訊息服務、語音功能',
                                actions=[
                                    MessageAction(label='代傳訊息操作',text='代傳訊息操作'),
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/oInstruction.m4a', duration=300000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/oInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/oInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我要加入代傳訊息服務、代傳訊息操作、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )

           
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="傳送地圖給我，我會告訴你當地天氣歐!"))
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/oInstructions.m4a', duration=300000))
#第二，手機語音輸入我要加入代傳訊息服務，接著，傳Line給小明冒號你好嗎，即可傳送，
#"ESLAB有以下功能\n0.功能:\n  輸入後可查詢功能\n1.貼圖\n2.時間\n3.發票\n4.油價\n5.國際油價\n6.電\n7.水庫\n8.天氣\n9.停班停課\n10.歌曲排行\n11.新聞\n12.電影\n13.記帳\n14.主動傳訊息(每10秒)\n15.實驗室"
@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("退出追蹤")


@handler.add(JoinEvent)
def handle_join(event):
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text='加入 ' + event.source.type))
        b=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        mes='''歡迎使用ESLAB功能 請輸入或手機語音輸入縣市天氣 例如 台南天氣 或傳送地圖給我，我會告訴你當地天氣，另外還有發票，
        ，油價，國際油價，停班停課，實驗室，記帳，電，水庫，天氣，新聞，電影，時間，歌曲排行，群組或聊天室請輸入，滾，我就會離開
        如果只想知道語音功能，請說語音功能，我會詳細告訴您'''
        try:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('static/grInstruction.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('static/grInstruction.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我要加入代傳訊息服務、代傳訊息操作、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="群組或聊天室請輸入:滾 我就會離開，傳送地圖給我，我會告訴你當地天氣歐!"))        
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/static/grInstruction.m4a', duration=100000))
        except:
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+mes+'&language=zh-tw'
            r = requests.get(stream_url, stream=True)
            with open('statics/grInstructions.m4a', 'wb') as f:
                try:
                    for block in r.iter_content(1024):
                        f.write(block)
                    f.close()
                except KeyboardInterrupt:
                    pass
            mixer.init()
            mixer.music.load('statics/grInstructions.m4a')
            mixer.music.play()            
            carousel_template_message = TemplateSendMessage(
                    alt_text='Follow Event',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='發票、油價、國際油價',
                                actions=[
                                    MessageAction(label='發票',text='發票'),                            
                                    MessageAction(label='油價',text='油價'),
                                    MessageAction(label='國際油價',text='國際油價')
                                ]
                            ),

                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='停班停課、實驗室、記帳',
                                actions=[
                                    MessageAction(label='停班停課',text='停班停課'),
                                    MessageAction(label='實驗室',text='實驗室'),
                                    MessageAction(label='記帳',text='記帳')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我要加入代傳訊息服務、代傳訊息操作、語音功能',
                                actions=[
                                    MessageAction(label='我要加入代傳訊息服務',text='我要加入代傳訊息服務'),
                                    MessageAction(label='代傳訊息服務操作',text='代傳訊息服務操作'),
                                    MessageAction(label='語音功能',text='語音功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='我是誰可以查詢自己的名稱、傳Line:有教學和查詢好友',
                                actions=[
                                    MessageAction(label='傳Line',text='傳Line'),
                                    MessageAction(label='我是誰',text='我是誰'),
                                    MessageAction(label='功能',text='功能')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='電、水庫、天氣',
                                actions=[
                                    MessageAction(label='電',text='電'),                            
                                    MessageAction(label='水庫',text='水庫'),
                                    MessageAction(label='天氣',text='天氣')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='歌曲排行、新聞、電影',
                                actions=[
                                    MessageAction(label='歌曲排行',text='歌曲排行'),
                                    MessageAction(label='新聞',text='新聞'),
                                    MessageAction(label='電影',text='電影')
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                                title='功能',
                                text='貼圖、時間、主動傳訊息',
                                actions=[
                                    MessageAction(label='貼圖',text='貼圖'),
                                    MessageAction(label='時間',text='時間'),
                                    MessageAction(label='主動傳訊息',text='主動傳訊息')
                                ]
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(client,TextSendMessage(text="群組或聊天室請輸入:滾 我就會離開，傳送地圖給我，我會告訴你當地天氣歐!"))        
            line_bot_api.push_message(client,AudioSendMessage(original_content_url=webhook_url+'/statics/grInstructions.m4a', duration=100000))
            
@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("離開群組/聊天室")

if __name__ == "__main__":
    app.run(port=9000,debug =True)

    


