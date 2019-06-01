import time
import requests
from proxy_requests import ProxyRequests
import json
#prefetch wicket and over inorder to notify.
import config
def listofMatches():
    url='http://mapps.cricbuzz.com/cbzios/match/livematches'
    r = ProxyRequests(url)
    r.get()
    a=str(r)
    data=json.loads(a)
    matches=[]
    match_id=[]
    for i in data['matches']:
        matches.append(i)
    for i in matches:
        t= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i['header']['start_time'])))
        match_id.append(i['match_id'])
        print(i['match_id']+' '+ t +' '+i['series_name'])
    return match_id[0]    


def prefetch():
    try:
        print("Pre-fetching")
        print(config.ur)
        r = ProxyRequests(config.ur)
        r.get()
        a=str(r)
        data=json.loads(a)
        config.series_name = data["series_name"]
        config.bat_team_name=data['bat_team']['name']
        config.twicket=int(data["comm_lines"][0]["wkts"])
        config.twicket=config.twicket+1
        config.tover=int(float(data['bat_team']['innings'][0]['overs']))
        config.tover=config.tover+1
        config.series_name="--"+config.series_name+"--"
        print(config.series_name+'\n'+config.bat_team_name)
    except:
        print("An exception occurred prefetching")
        time.sleep(5)
        prefetch()