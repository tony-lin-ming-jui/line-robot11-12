from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError,InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

from datetime import datetime
import time
import json

line_bot_api = LineBotApi('dzMHXFwU0FbiK7Ct+zLK80AgIt3wHV7trwSdsh+EjSKNW8vTir0fhCP6qRsqLWjl/UxiiqECfBK6AfHe0htI/Ksqz0DQLAGBoZZnsLG7lgXlHSvG7gd6yW2LT7K5qbXl4fQ4f3X+YCWlfXPv/vptTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18305b046cb7b77b860f4381569cafd3')

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
    if re.findall('記帳.*?',event.message.text):        
        message=event.message.text
        if re.findall('記帳 *?[0-9]+.*?.',message):#其他地方變數禁止使用 money date_now thing
            global client_id
            global thing
            global money
            global date_now
            a=request.get_data(as_text=True)
            #profile = line_bot_api.get_profile(event.source)
            client_id=''.join(re.findall('userId":"(.*?)"',a))
            print("唯一名稱:",client_id)
            #print(type(a))            
            
            x=re.findall('記帳 *?([0-9]+)',message)
            y=re.findall('\D',message)
            money=''.join(x)
            thing=''.join(y).strip("記帳 ")            
            date_now = datetime.now().strftime('%Y/%m/%d')
            date_nows = datetime.now().strftime('%Y-%m-%d')
            print(date_nows)
            if thing == "":
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
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='是否確認增加此花費\n金額:'+ money+'元\n日期:'+date_now+'\n備註:'+thing,
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(label="確認", data="確認")
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(label="取消", data="取消")
                                ),
                                ])))


        else:
            x="歡迎使用ESLAB記帳小幫手請輸入:\n記帳 金額(輸入數字)"#這裡或許可以改成圖片
            line_bot_api.reply_message(event.reply_token,               
                TextSendMessage(text=x))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
@handler.add(PostbackEvent)#只回復postback的訊息
def handle_postback(event):
    if event.postback.data == '取消': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已取消此筆記帳"))
    elif event.postback.data == '確認': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:"+thing+":"+money+"元\n日期:"+date_now))
    elif event.postback.data == '飲食': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:飲食:"+money+"元\n日期:"+date_now))
    elif event.postback.data == '日常': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:日常:"+money+"元\n日期:"+date_now))
    elif event.postback.data == '交通': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:交通:"+money+"元\n日期:"+date_now))
    elif event.postback.data == '娛樂': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:娛樂:"+money+"元\n日期:"+date_now))
    elif event.postback.data == '醫療': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:醫療:"+money+"元\n日期:"+date_now))
    elif event.postback.data == '其他': #這裡可以直接拿money和 date_now       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已記帳:其他:"+money+"元\n日期:"+date_now))

'''
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
