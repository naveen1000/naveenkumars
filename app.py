from proxy_requests import ProxyRequests
import json
import requests
import time
from prefetch import prefetch
import config

from fbPush import fbpush
from fbRdbUpdate import fputOnRdb


#Fetching score main function of this app.

def score():
    try:
        r = ProxyRequests(config.ur)
        r.get()
        a=str(r)
        data=json.loads(a)
        score=int(data["comm_lines"][0]["score"])
        wicket=int(data["comm_lines"][0]["wkts"])
        over=float(data['bat_team']['innings'][0]['overs'])
        detailed_score=data["comm_lines"][0]["score"]+"/"+data["comm_lines"][0]["wkts"]+" "+data['bat_team']['innings'][0]['overs']
        print(detailed_score,end=" ")
        fputOnRdb(detailed_score)
        try:
            bowler=data['bowler'][0]['name']
            print(bowler)
            batname0=data['batsman'][0]['name']
            batname1=data['batsman'][1]['name']
            bat0score=data['batsman'][0]['r']
            bat1score=data['batsman'][1]['r']
            bat0ball=data['batsman'][0]['b']
            bat1ball=data['batsman'][1]['b']
            bowler=data['bowler'][0]['name']
            batters=batname0+"("+bat0score+"-"+bat0ball+")"+batname1+"("+bat1score+"-"+bat1ball+")"
            detailed_score=data["comm_lines"][0]["score"]+"/"+data["comm_lines"][0]["wkts"]+" "+data['bat_team']['innings'][0]['overs']
            print(batters)
        except:
            print("An exception occurred fetching either batters or bowler")
        try:   
            if (over==(config.tover-1.0+0.5)):
                global bow
                bow=bowler
            if over==int(config.tover):
                msg =detailed_score+" " + bow + "\n" + batters +"\n"+ data['prev_overs']
                print(msg)
                notify(msg)
                config.tover=config.tover+1
                fbpush(msg)
                time.sleep(15)
            if wicket==config.twicket:
                msg=series_name+"\n"+"wicket "+str(twicket)+" "+data['last_wkt_name']+" "+data['last_wkt_score']+" B: "+bowler+"\n"+detailed_score
                fbpush(msg)
                notify(msg)
                config.twicket=config.twicket+1
                time.sleep(15)
        except:
            print("An exception occurred while trying to notify")
    except:
        print("An exception occurred fetching score")
    
 #Telegram notification    
def notify(msg):
    #Telegam Bot Url
    #url='https://api.telegram.org/bot879982304:AAHG7ZRyEMWoQB-ToaiJBv_gMvkW-ekJcSg/sendMessage?chat_id=582942300&text='+msg
    #TelegramChannel chatId -1001181667975
    url='https://api.telegram.org/bot879982304:AAHG7ZRyEMWoQB-ToaiJBv_gMvkW-ekJcSg/sendMessage?chat_id=-1001181667975&text='+msg
    requests.get(url)
    print("notified")

def main():   
    #mid=input('Enter mid..\n')
    mid='22645'
    print(mid)
    config.ur='http://mapps.cricbuzz.com/cbzios/match/'+mid+'/leanback.json'
    prefetch()
    while(True):
        score()
        time.sleep(5)

main()






