from proxy_requests import ProxyRequests
import json
import requests
import time
from prefetch import prefetch,listofMatches
import config

from fbPush import fbpush,updateRedIds
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
        detailed_score=config.bat_team_name+" "+data["comm_lines"][0]["score"]+"/"+data["comm_lines"][0]["wkts"]+" "+data['bat_team']['innings'][0]['overs']
        print(detailed_score,end=" ")
        
        try:
            bowler=data['bowler'][0]['name']
            print("B:"+bowler)
            batname0=data['batsman'][0]['name']
            batname1=data['batsman'][1]['name']
            bat0score=data['batsman'][0]['r']
            bat1score=data['batsman'][1]['r']
            bat0ball=data['batsman'][0]['b']
            bat1ball=data['batsman'][1]['b']
            bowler=data['bowler'][0]['name']
            batters=batname0+"*("+bat0score+"-"+bat0ball+") "+batname1+"("+bat1score+"-"+bat1ball+")"
            print(batters)
            fputOnRdb(detailed_score + "     B: "+bowler+"\n"+batters+"\nRecent:\n"+data['prev_overs'])
        except:
            print("An exception occurred fetching either batters or bowler")
        try:   
            if (over==(config.tover-1.0+0.5)):
                global bow
                bow=bowler
            if over==config.tover:
                prev_overs=data['prev_overs']
                prev_over=prev_overs.split('|')
                msg =detailed_score+" B:" + bow + "\n" + batters +"\n"+ prev_over[-1]
                print(msg)
                notify(msg)
                config.tover=config.tover+1
                fbpush(msg)
                updateRedIds()
                time.sleep(10)
            if wicket==config.twicket:
                msg="wicket "+str(config.twicket)+" "+data['last_wkt_name']+" "+data['last_wkt_score']+" B: "+bowler+"\n"+detailed_score
                fbpush(msg)
                notify(msg)
                config.twicket=config.twicket+1
                time.sleep(15)
            if (int(over+1)!=config.tover):
                updateRedIds()
                prefetch()
            if ((wicket+1)!=config.twicket):
                updateRedIds()
                prefetch()
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
    mid=listofMatches()
    print(mid)
    config.ur='http://mapps.cricbuzz.com/cbzios/match/'+mid+'/leanback.json'
    prefetch()
    updateRedIds()
    while(True):
        score()
        time.sleep(5)

main()






