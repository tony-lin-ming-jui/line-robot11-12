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
import work_class_cancel_crawler
import PTQS1005
import oil_crawler_of
import power_crawler_office
import reservoir_crawler

app = Flask(__name__)

line_bot_api = LineBotApi('dzMHXFwU0FbiK7Ct+zLK80AgIt3wHV7trwSdsh+EjSKNW8vTir0fhCP6qRsqLWjl/UxiiqECfBK6AfHe0htI/Ksqz0DQLAGBoZZnsLG7lgXlHSvG7gd6yW2LT7K5qbXl4fQ4f3X+YCWlfXPv/vptTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18305b046cb7b77b860f4381569cafd3')
user_id='U7446a50ce4c8e4c5942a18454bac76a2'

scheduler = BlockingScheduler()


@app.route('/plots')  
def oilweb():
    img = io.BytesIO()
    oilof=oil_crawler_of.oilof()
    #oilof=oilof()
    print(oilof)
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
    line_bot_api.push_message(user_id,TextSendMessage(text='Hello World! :)'))
    #這裡會主動會訊息
def t1():
    cancel=work_class_cancel_crawler.wkncls()
    line_bot_api.push_message(user_id,TextSendMessage(text=cancel[0]+"\n"+cancel[1]))
    #line_bot_api.push_message(user_id,TextSendMessage(text='Hello World! :)'))


def weather():#先不弄 主動推播天氣
    weather=weather_data.weather()
    weathers=''.join(weather)
    line_bot_api.push_message(user_id,TextSendMessage(text=weathers))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == '我是誰':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='line的名稱: ' + profile.display_name),
                    TextSendMessage(text='line的自我介紹: ' + profile.status_message)
                ])
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif event.message.text == '滾':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='離開群組'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='離開群組'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="我無法從1:1聊天室滾出去"))
    elif event.message.text == "你好":        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你好"))
    elif event.message.text =="貼圖":
       sticker=Sticker_random.sticker()
       line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=sticker[0], sticker_id=sticker[1]))
    elif event.message.text =="時間":
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=time_now))
    elif event.message.text == "發票":
        invoice=invoice_pic_crawler.invoice()
        print("invoice",invoice)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=invoice[0], preview_image_url=invoice[0]))
    elif event.message.text == "油價":
        oil=oil_crawler_n_office.oil()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=oil))
    elif event.message.text == "國際油價":
        oilof=oil_crawler_of.oilof()
        m="今天國際油價:\n西德州:"+str(oilof[-3])+"美元\桶\n北海布蘭特:"+str(oilof[-2])+"美元\桶\n杜拜:"+str(oilof[-1])+"美元\桶\n"
        u="參考資料:https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
        print(m+u)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url="https://b9e1f9cb.ngrok.io/static/oil.jpg", preview_image_url="https://b9e1f9cb.ngrok.io/static/oil.jpg"))
        line_bot_api.push_message(user_id,TextSendMessage(text=m+u))
    elif event.message.text == "電":
        power=power_crawler_office.power()
        powers='\n'.join(power)
        print(type(powers))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=powers))
    elif event.message.text == "水庫":
        reservoir=reservoir_crawler.dam()
        print(type(reservoir))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reservoir))
    elif event.message.text == "天氣":
        cancel=work_class_cancel_crawler.wkncls()
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
                        text='今日紫外線、今日紫外線最大值、累積雨量',
                        actions=[
                            MessageAction(label='今日紫外線',text='紫外線'),                            
                            MessageAction(label='今日紫外線最大值',text='紫外線最大值'),
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
        line_bot_api.push_message(user_id,TextSendMessage(text=cancel[0]+"\n"+cancel[1]))
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
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
    elif event.message.text == "紫外線最大值":
        url='https://www.cwb.gov.tw/V7/observe/UVI/Data/UVI_Max.png'
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
                    text='各縣市天氣資料',
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
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]))
    elif event.message.text =="台北天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[1]))
    elif event.message.text =="新北天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[2]))
    elif event.message.text =="北北基天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[0]+weather[1]+weather[2]))    
    elif event.message.text =="桃園天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]))
    elif event.message.text =="新竹天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[4]+weather[5]))
    elif event.message.text =="苗栗天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[6]))        
    elif event.message.text =="桃竹苗天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[3]+weather[4]+weather[5]+weather[6]))
    elif event.message.text =="台中天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[7]))
    elif event.message.text =="彰化天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[8]))
    elif event.message.text =="南投天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[9]))
    elif event.message.text =="雲林天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[10]))
    elif event.message.text =="嘉義天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[11]+weather[12]))
    elif event.message.text =="宜蘭天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[13]))
    elif event.message.text =="花蓮天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]))
    elif event.message.text =="台東天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[15]))
    elif event.message.text =="花東天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[14]+weather[15]))
    elif event.message.text =="台南天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[16]))
    elif event.message.text =="高雄天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[17]))
    elif event.message.text =="屏東天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[18]))
    elif event.message.text =="連江天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]))
    elif event.message.text =="金門天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[20]))
    elif event.message.text =="澎湖天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[21]))
    elif event.message.text =="外島天氣":
        weather=weather_data.weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weather[19]+weather[20]+weather[21]))
    elif event.message.text =="停班停課":
        cancel=work_class_cancel_crawler.wkncls()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cancel[0]+"\n"+cancel[1]))        
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

    elif event.message.text == "Image Carousel":
        print("Image Carousel")       
        Image_Carousel = TemplateSendMessage(
        alt_text='目錄template',
        template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://img.appledaily.com.tw/images/thumbnail/other/ab363fdc78bc795e202b810c231752fd.jpg',
                action=PostbackTemplateAction(label='postback1',text='postback text1',data='action=buy&itemid=1')
                ),
            ImageCarouselColumn(
                image_url='https://img.bluezz.tw/invoice/107/0304.jpg',
                action=PostbackTemplateAction(label='postback2',text='postback text2',data='action=buy&itemid=2')
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token,Image_Carousel)
    elif event.message.text == "新聞":
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
        dictionary = dict(zip(x,news_group))
        p=random.sample(range(12),10)    
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
                image_url=dictionary['link2'][p[2]],
                action=URITemplateAction(
                    uri=dictionary['link'][p[2]],
                    label=dictionary['title'][p[2]][0:11]
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
    elif event.message.text == "電影":
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
    elif event.message.text == "功能":
        message="ESLAB有以下功能\n0.功能:\n  輸入後可查詢功能\n1.貼圖\n2.時間\n3.發票\n4.油價\n5.國際油價\n6.電\n7.水庫\n8.天氣\n9.停班停課\n10.歌曲排行\n11.新聞\n12.電影\n13.主動傳訊息(每10秒)\n14.實驗室"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))


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
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='主動訊息開啟'))
        scheduler.add_job(t1, 'interval', seconds=10,id='t1')#這裡設定時間，只有在第一次傳送訊息後 才會開始主動回訊息hour='0-9', minute="*"
        scheduler.start()#scheduler.add_job(要執行的程式, 'interval', seconds=10,id='t1')
    elif event.message.text == "主動傳Hello World": 
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
    else:
        google_url = 'https://www.google.com.tw/search'
        # 查詢參數
        my_params = {'q': event.message.text}
        # 下載 Google 搜尋結果
        r = requests.get(google_url, params = my_params)
        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 原始碼
            soup = BeautifulSoup(r.text, 'html.parser')
              # 觀察 HTML 原始碼
              # print(soup.prettify())

              # 以 CSS 的選擇器來抓取 Google 的搜尋結果
            items = soup.select('div.g > h3.r > a[href^="/url"]')
            #print(items)
            list_google=[]
            for i in items:        
            
                # 標題
                #print("標題：" + i.text)
                title="標題：" + i.text
                list_google.append(title)
                # 網址
                #print("網址：" + i.get('href'))
                url="網址：" + i.get('href').strip("/url?q=")
                list_google.append(url)
                
            #print(title)
            #print(url)
            #print(list_google)
            google='\n'.join(list_google)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以下是我幫你蒐集到的資料:\n"+google))
            

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
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[0]))
    elif event.postback.data == '揮發性有機物':
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[1]))
    elif event.postback.data == '甲醛':
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[2]))
    elif event.postback.data == '二氧化碳':
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[3]))
    elif event.postback.data == '溫度':
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[4]))
    elif event.postback.data == '相對濕度':
        PTQS=PTQS1005.ptq()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PTQS[5]))

@handler.add(FollowEvent)
def handle_follow(event):#剛加入好友會跳出的功能
    print("加入追蹤")
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
                        text='停班停課、新聞、電影',
                        actions=[
                            MessageAction(label='停班停課',text='停班停課'),
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
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/xOrDUep.jpg',
                        title='功能',
                        text='歌曲排行、實驗室、功能',
                        actions=[
                            MessageAction(label='歌曲排行',text='歌曲排行'),
                            MessageAction(label='實驗室',text='實驗室'),
                            MessageAction(label='功能',text='功能')
                        ]
                    )
                ]
            )
        )        
    line_bot_api.reply_message(event.reply_token, carousel_template_message)
@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("退出追蹤")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='加入 ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("離開群組/聊天室")
    
if __name__ == "__main__":
    app.run(port=9000,debug =True)

    


