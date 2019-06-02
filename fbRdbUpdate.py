#https://www.c-sharpcorner.com/article/firebase-crud-operations-using-python/
from firebase import firebase 
firebase = firebase.FirebaseApplication('https://crick-notify.firebaseio.com/',None)    
 
def fputOnRdb(detailed_score):
    try:
        firebase.put('/','object',detailed_score)
    except:
        print("An exception occurred updating Fdb")
