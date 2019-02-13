from flask import Flask,render_template,request,redirect,url_for,session

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError,InvalidSignatureError
)
from linebot.models import *
import re


from datetime import datetime
import time

import pymysql
import os


app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)




line_bot_api = LineBotApi('dzMHXFwU0FbiK7Ct+zLK80AgIt3wHV7trwSdsh+EjSKNW8vTir0fhCP6qRsqLWjl/UxiiqECfBK6AfHe0htI/Ksqz0DQLAGBoZZnsLG7lgXlHSvG7gd6yW2LT7K5qbXl4fQ4f3X+YCWlfXPv/vptTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18305b046cb7b77b860f4381569cafd3')
user_id='U7446a50ce4c8e4c5942a18454bac76a2'

db = pymysql.connect("127.0.0.1","root","1qaz1qaz","linesss",charset="utf8")
cursor = db.cursor()

@app.route("/account")
def account():
    

    client_id=z
  

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
        #mesg='\n'.join(mes)
    #print(mesg)
    return render_template('account.html',mes=mes)

@app.route("/callback", methods=['POST'])
def callback():
    #global body
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
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if re.findall('^記帳.*?',event.message.text):        
        message=event.message.text
        
        global z
        b=request.get_data(as_text=True)            
        #profile = line_bot_api.get_profile(event.source)
        if re.findall('roomId":"(.*?)"',b):
            client=''.join(re.findall('roomId":"(.*?)"',b))
        elif re.findall('groupId":"(.*?)"',b):
            client=''.join(re.findall('groupId":"(.*?)"',b))     
        else:
            client=''.join(re.findall('userId":"(.*?)"',b))
        
        z=client
        print("z",z)
        #####
        session['session_name']=client
        print("唯一名稱:",client)
        if message =='記帳方式':
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='輸入方式:\n記帳 80 雞排\n記帳 80\n刪除:\n刪除記帳 編號\n修改:\n修改金額 編號 新金額 \n修改項目 編號 新項目'))    
        elif re.findall('^記帳 *?[0-9]+.*?',message):#其他地方變數禁止使用 money date_now thing   z
            print("message",message) 
            global month
            #global thing
            #global money
            global date_now
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
                                action=PostbackAction(label="飲食", data="飲食 "+str(money))
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
            carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        
                        title='歡迎使用ESLAB記帳小幫手',
                        text='初次使用請觀看下方說明\n群組或聊天室請輸入:記帳方式  觀看說明',
                        actions=[
                            MessageAction(label='本月消費(顯示全部消費)', text='本月消費'),                            
                            MessageAction(label='本月花費(顯示本月金額)', text='本月花費'),
                            URIAction(label='查詢所有記帳(含編號)', uri='https://342779d8.ngrok.io/account')
                        ]
                    ),
                    CarouselColumn(
                        
                        title='歡迎使用ESLAB記帳小幫手',
                        text='初次使用請觀看下方說明\n群組或聊天室請輸入:記帳方式  觀看說明',
                        actions=[
                            MessageAction(label='查詢編號(最後5個)', text='查詢編號'),                            
                            MessageAction(label='刪除最後一筆記帳', text='刪除最後一筆記帳'),
                            MessageAction(label='修改記帳', text='修改記帳方式請輸入:\n修改金額 編號 新金額 \n修改項目 編號 新項目')
                        ]
                    )
                ]))
                    
            
            
            #line_bot_api.reply_message(event.reply_token, buttons_template_message)
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
            line_bot_api.push_message(user_id,TextSendMessage(text='輸入方式:\n記帳 80 雞排\n記帳 80\n刪除:\n刪除記帳 編號\n修改:\n修改金額 編號 新金額 \n修改項目 編號 新項目'))
            #x="歡迎使用ESLAB記帳小幫手請輸入:\n記帳 80 雞排"#這裡改按鈕刪除最後一筆記帳 查詢編號(最後5個) 查詢所有編號 本月消費#mounth=.strftime('%Y-%m-%d')
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=x))
            

    elif re.findall('^刪除記帳 [0-9]+',event.message.text):
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a)) 
        client_id=''.join(re.findall('userId":"(.*?)"',a))
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

        
    elif event.message.text == '本月消費':
        a=request.get_data(as_text=True)            
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        date_now = datetime.now().strftime('%Y/%m/%d')
        month=''.join(re.findall('/([0-9]+)/',date_now))#抓月份

        cursor.execute("SELECT * FROM "+client_id+" WHERE month ="+ str(month)+"")
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
            print(a)
            #mes.append(listmoney[i]+listthing[i]+listdate[i]+"\n")
        #print(mes)
        print('總金額',a)
        mesg='\n'.join(mes)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(month)+"月總消費\n金額:"+str(a)+"元\n清單如下:\n"+mesg))
    elif event.message.text == '查詢編號':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))        
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
        else:
            for i in range(0,len(listnumber)):
                #mes.append("金額:"+str(listmoney[i])+"date:"+str(listdate[i])+" 項目:"+str(listthing[i]))
                mes.append(str(listthing[i])+":"+str(listmoney[i])+"元"+str(listdate[i])+"編號"+str(listnumber[i]))
            mesg='\n\n'.join(mes)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=mesg))

    elif event.message.text == '本月花費':
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        
        date_now = datetime.now().strftime('%Y/%m/%d')
        month=''.join(re.findall('/([0-9]+)/',date_now))#抓月份

        cursor.execute("SELECT * FROM "+client_id+" WHERE month ="+ str(month)+"")
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
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(month)+"月總消費\n金額:"+str(a)+"元"))

    
   
        
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))



        
@handler.add(PostbackEvent)#只回復postback的訊息
def handle_postback(event):
    if event.postback.data == '取消': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已取消此筆記帳"))
    elif re.findall('^確認 [0-9]+ \D+',event.postback.data):
    #elif event.postback.data == '確認': #這裡可以直接拿money和 date_now
        
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        money= ''.join(re.findall('^確認 ([0-9]+)',event.postback.data))
        y=re.findall('\D',event.postback.data)            
        thing=''.join(y).strip("確認 ")
        print(money)
        print(thing)
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '" + str(thing) + "','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))


        buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                #title='已記帳:'+thing+':'+money+'元',text='', actions=[
                title='已記帳:', text=thing+":"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新金額'),                       
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
                    ]))
        
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        db.close
        
    elif re.findall('^飲食 [0-9]+',event.postback.data):
    #elif event.postback.data == '飲食': #這裡可以直接拿money和 date_now
        print(event.postback.data)
        a=request.get_data(as_text=True)
        if re.findall('roomId":"(.*?)"',a):
            client_id=''.join(re.findall('roomId":"(.*?)"',a))
        elif re.findall('groupId":"(.*?)"',a):
            client_id=''.join(re.findall('groupId":"(.*?)"',a))     
        else:
            client_id=''.join(re.findall('userId":"(.*?)"',a))
        money= ''.join(re.findall('^飲食 ([0-9]+)',event.postback.data))
        print(money)   
        print(client_id)    
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '飲食','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #這裡改POST 要修改項目會金額 難寫囉
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="飲食:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^生活 ([0-9]+)',event.postback.data))        
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '生活','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage( #這裡改POST 要修改項目會金額 難寫囉
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="生活:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^交通 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '交通','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #這裡改POST 要修改項目會金額 難寫囉
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="交通:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^娛樂 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '娛樂','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        
        buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="娛樂:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^醫療 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '醫療','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="醫療:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^住宿 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '住宿','" + str(date_now) + "'," + str(month) + ")")
        db.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
            alt_text='Buttons alt text',
            template=ButtonsTemplate(
                title='已記帳:', text="住宿:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
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
        money= ''.join(re.findall('^其他 ([0-9]+)',event.postback.data))
        cursor.execute("create table if not exists "+client_id+" (number Integer NOT NULL AUTO_INCREMENT,money INT,thing VARCHAR(20) NOT NULL,date DATE,month INT, PRIMARY KEY (number))")
        cursor.execute("INSERT INTO "+client_id+" (money, thing, date,month) VALUES (" + str(money) + ", '其他','" + str(date_now) + "'," + str(month) + ")")
        db.commit() 
        cursor.execute("SELECT LAST_INSERT_ID()")
        for row in cursor.fetchall():
            number=row[0]  
        print("number",number)
        print(type(number))

        buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
            alt_text='Buttons alt text',
                template=ButtonsTemplate(
                    title='已記帳:', text="其他:"+money+"元\n日期:"+date_now+"\n編號:"+ str(number), actions=[
                    MessageAction(label='修改項目', text='請輸入:\n修改項目 '+ str(number)+' 新的項目'),
                    MessageAction(label='修改金額', text='請輸入:\n修改金額 '+ str(number)+' 新的金額'),                        
                    MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
                    MessageAction(label='本月花費', text='本月花費')
                        ]))
        db.close
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        

'''
                buttons_template_message=TemplateSendMessage(  #本月消費 還要加總額
                alt_text='Buttons alt text',
                template=ButtonsTemplate(
                    title='歡迎使用ESLAB記帳小幫手', text='初次使用請觀看下方說明', actions=[
                        MessageAction(label='本月消費(顯示全部消費)', text='本月消費'),
                        URIAction(label='查詢所有記帳(含編號)', uri='https://342779d8.ngrok.io/account'),
                        #MessageAction(label='查詢所有記帳(含編號)', text='查詢所有記帳'),
                        MessageAction(label='查詢編號(最後5個)', text='查詢編號'),
                        MessageAction(label='刪除最後一筆記帳', text='刪除最後一筆記帳')
                        ]))

        
        confirm_template = ConfirmTemplate(text='已記帳:'+thing+":"+money+"元", actions=[
            MessageAction(label='修改', text='修改記帳 '+ str(number)),#這裡改POST 要修改項目會金額 難寫囉
            MessageAction(label='刪除', text='刪除記帳 '+ str(number)),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        db.close
        line_bot_api.reply_message(event.reply_token, template_message)


        

            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    text='Confirm alt text',
                    confirm_template = ConfirmTemplate(text='Do it?', actions=[
                        PostbackAction(label='Yes', text='Yes!'),
                        PostbackAction(label='No', text='No!'),
                        ])

            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='測試'))

            money=''.join(x)
            date_now = datetime.now().strftime('%Y/%m/%d')
            print(money)#這裡可以用        
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='已增加此花費\n金額:'+money+'元，請選擇分類',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="取消", data="取消")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="飲食", data="飲食")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="日常", data="日常")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="交通", data="交通")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="娛樂", data="娛樂")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="醫療", data="醫療")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="其他", data="其他")
                            ),
                            ])))


            confirm_template = ConfirmTemplate(text='Do it?', actions=[
                MessageAction(label='Yes', text='Yes!'),
                MessageAction(label='No', text='No!'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)
'''
   
if __name__ == "__main__":
    app.run(port=9000,debug =True)
