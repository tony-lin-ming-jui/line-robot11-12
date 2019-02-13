import time
from datetime import datetime
import re
date_now = datetime.now()
print(date_now.strftime('%Y/%m/%d'))
print(date_now.year)
print(date_now.month)
print(date_now.day)
print(date_now.hour)
print(date_now.minute)
print(date_now.second)
#year=''.join(re.findall('([0-9]+)/$',date_now))
#print(year)

