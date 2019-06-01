from pyfcm import FCMNotification
from firebase import firebase 
firebase = firebase.FirebaseApplication('https://naveen-kumar-simma.firebaseio.com/',None)    
push_service = FCMNotification(api_key="AAAALXgG6s8:APA91bHaUoZ9MwS78rdihRMc7GsN-NQ8oNDSEjEZcDMeU7DyAr_8EJRHCB_o13ydJXpGYLu4Nl3sA5rpNW6pPdK5Q9Fa50R6zdO6fiQnDU8OG7ZC7hieVYdTn_NeeBTY-XIRwowDh0KA")
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


message_title = "CricNotify"
message_icon="firebase-logo.png"

def fbpush(message_body):
    try:
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_body = message_body ,message_icon=message_icon)
        print(result)
    except:
        print("An exception occurred while trying to notify firebase")
