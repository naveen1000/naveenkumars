#https://github.com/olucurious/PyFCM
from pyfcm import FCMNotification
from firebase import firebase 
firebase = firebase.FirebaseApplication('https://crick-notify.firebaseio.com/',None)    
push_service = FCMNotification(api_key="AAAAlwGOB7s:APA91bHTREkY-2Ypjxn6A-L6jplxbctiWTEO64eyP4gTZHVmWDYsiKoMEB07wMlV8Zi5XwTm3v5UlxUeOYTPUpJxtyfemLEVlNt7FV6nUU6O-mhpMeXrm3fta0mb7Rt6HsgimVUeHI0-")
registration_ids=[]
def updateRegIds():
    try:
        global registration_ids
        registration_ids=[]
        result = firebase.get('/users/', '')  
        for i in result:
            registration_ids.append(i)
        print("Updated RegIds")
        print(len(registration_ids))
    except:
        print("An exception occurred while trying to update regIds")


message_title = "CricNotify"
message_icon="firebase-logo.png"
click_action="https://crick-notify.web.app/"

def fbpush(message_body):
    try:
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_body = message_body ,message_icon=message_icon,click_action=click_action)
        print(result)
    except:
        print("An exception occurred while trying to notify firebase")
