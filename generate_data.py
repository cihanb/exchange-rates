import sys
from urllib.request import urlopen
import datetime
import time

def validate(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

#START HERE
for iyear in range(2013, datetime.datetime.now().year):
    for imonth in range(1,12):
        for iday in range(1,31):
            try:
                idate = str(iyear)+"-"+str(imonth)+"-"+str(iday)
                #validate the date is valid
                validate(idate)
                print ("saving: " + idate)
                if (idate < datetime.datetime.now().strftime("%Y-%m-%d")):
                    content = urlopen("https://exchangeratesapi.io/api/"+ idate +"?base=USD").read()
                    # print (content.decode("utf-8"))
                    f = open('data/'+ idate +'.json',"w+")
                    f.write(content.decode("utf-8"))
                    f.close()
            except:
                # skip date
                #raise "error"
                print ("incorrect date:" + idate)
