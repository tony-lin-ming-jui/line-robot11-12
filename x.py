import oil_crawler_of
oilof=oil_crawler_of.oilof()
m="今天國際油價:\n西德州:"+str(oilof[-3])+"美元\桶\n北海布蘭特:"+str(oilof[-2])+"美元\桶\n杜拜:"+str(oilof[-1])+"美元\桶\n"
u="參考資料:https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
print(m+u)

'''
import reservoir_crawler
reservoir=reservoir_crawler.dam()
print(reservoir)
print(type(reservoir))


import PTQS1005
PTQS=PTQS1005.ptq()
print(PTQS[0])
print(type(PTQS[0]))
'''
'''
import weather_data
weather=weather_data.weather()
weathers=''.join(weather)

#print(weather[5:10])
#各縣市天氣
print(weather[21])
#print(len(weather))
'''
'''
i=0
j=5
while i<len(weather)-6:
    #print("i",i,"j",j)
    print(weather[i:j])
    i=i+5
    j=j+5
    
    
    #print("i",i,"j",j)

'''
'''
for i in range(0,len(weather),4):
    for j in range(4,len(weather),4):
        print("i",i,"j",j)
        #print(weather[i:j])
        
''' 

'''
import Sticker_random
sticker=Sticker_random.sticker()
print(sticker)
print(sticker[0])
print(sticker[1])
'''
'''
import radar_crawler
#global str
#print(radar_crawler)
rd=radar_crawler.radar()
print(rd)
'''
'''
import song_crawler  

rank=song_crawler.ranking()

rankCh='\n'.join(rank[:11])
rankwestern='\n'.join(rank[11:22])
rankNEA='\n'.join(rank[-11:])
print(rankNEA)
'''
'''
 stkid={1:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,21,100,101,102,103,104,105,
                    106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,
                    123,124,125,126,127,128,129130,131,132,133,134,135,136,137,138,139,
                    401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,
                    418,419,420,421,422,423,424,425,426,4227,428,429,430],
                    2:[18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                       41,42,43,44,45,46,47,140,141,142,143,144,145,146,147,148,149,150,
                       151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,
                       167,168,169,170,171,172,173,174,175,176,177,178,179,501,502,503,
                       504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,
                       520,521,522,523,524,525,526,527],
                   3:[180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,
                      197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,
                      214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,
                      231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,
                      248,249,250,251,252,253,254,255,256,257,258,259],
                   4:[260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,
                      277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,
                      294,295,296,297,298,299,300,301,302,303,304,305,306,307,601,602,603,
                      604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,
                      620,621,622,623,624,625,626,627,628,629,630,631,632]}            
        a=random.choice(range(1,5))

        if a==1:    
            p=random.sample(range(88),1)    
            c_stkid=stkid[1][p[0]]
            line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=a, sticker_id=c_stkid))                
        if a==2:    
            p=random.sample(range(97),1)    
            c_stkid=stkid[2][p[0]]
            line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=a, sticker_id=c_stkid))      
                
        if a==3:    
            p=random.sample(range(81),1)    
            c_stkid=stkid[3][p[0]]
            line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=a, sticker_id=c_stkid))
        if a==4:    
            p=random.sample(range(81),1)    
            c_stkid=stkid[4][p[0]]
            line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=a, sticker_id=c_stkid))
'''
