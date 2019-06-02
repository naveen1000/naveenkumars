from firebase import firebase 
from pyfcm import FCMNotification
push_service = FCMNotification(api_key="AAAAlwGOB7s:APA91bHTREkY-2Ypjxn6A-L6jplxbctiWTEO64eyP4gTZHVmWDYsiKoMEB07wMlV8Zi5XwTm3v5UlxUeOYTPUpJxtyfemLEVlNt7FV6nUU6O-mhpMeXrm3fta0mb7Rt6HsgimVUeHI0-")

firebase = firebase.FirebaseApplication('https://crick-notify.firebaseio.com/',None)    

message_title = "crickNotify"
message_body = "Testing you are a valid user or not"

registration_ids=[]
def updateRedIds():
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

def fbDeletetToken(token):
    try: 
        firebase.delete('/users/', token)  
        print('Deleted')
    except:
        print("An exception occurred deleting Tokens")
def main():
    global registration_ids
    print('Testing')
    for reg_id in registration_ids:
        print(reg_id)
        result = push_service.notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)
        if(result['failure']==1):
            print('failed once')
            result = push_service.notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)
            if(result['failure']==1):
                fbDeletetToken(reg_id)   


