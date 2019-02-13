import re
import pymysql
#db = pymysql.connect("127.0.0.1","root","1qaz1qaz","linesss",charset="utf8" )
#cursor = db.cursor()

#db = pymysql.connect("127.0.0.1","root","1qaz1qaz","line_db",charset="utf8" )
#cursor = db.cursor()
#cursor.execute("create table voice (number Integer NOT NULL AUTO_INCREMENT,userid VARCHAR(35) NOT NULL,name VARCHAR(35), PRIMARY KEY (number))")
#db.commit()
'''
[^;] 代表不是 ; 的所有東西
[^;]+ 代表 1 個以上不是 ; 的所有東西
最後的 $ 代表後面不能再接其他東西
'''
#x="傳Line給叡:嗨"

#y=re.findall('^傳Line給(.*?):[^:]+',x)
x="確認 80 雞123腿"
y=re.findall('^確認 *?([0-9]+)',x)
#z=re.findall('\D',x)
#zz=''.join(z).strip("確認 ")
#print(zz)
print(y)
