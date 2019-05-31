import time
import requests
from proxy_requests import ProxyRequests
import json
#prefetch wicket and over inorder to notify.
import config
def prefetch():
    try:
        print("Pre-fetching")
        print(config.ur)
        r = ProxyRequests(config.ur)
        r.get()
        a=str(r)
        data=json.loads(a)
        series_name = data["series_name"]
        config.twicket=int(data["comm_lines"][0]["wkts"])
        config.twicket=config.twicket+1
        config.tover=int(float(data['bat_team']['innings'][0]['overs']))
        config.tover=config.tover+1
        series_name="--"+series_name+"--"
        print(series_name)
    except:
        print("An exception occurred prefetching")
        time.sleep(5)
        prefetch()