#!/usr/bin/env python
import requests
import json
import time
import sys
from flask import Flask
from flask_ask import Ask, statement, question, session

#global all_rooms


WEBEX_TEAMS_ACCESS_TOKEN="NmZhM2FkYTktMWJjNy00Y2E2LTgxYmItMTU4MzEyMzQ2YTAxMjkzOGE2ODctY2My"

from webexteamssdk import WebexTeamsAPI
api = WebexTeamsAPI(access_token=WEBEX_TEAMS_ACCESS_TOKEN)

all_rooms=api.rooms.list()

def find_roomid(room_name):
    
    #print(all_rooms)
    result_room = [room for room in all_rooms if room_name.lower() in room.title.lower()]

    #print(result_room[0].id)

    room=result_room[0]
    print(room.id)
   
    return room.id

def list_message(room):
    
    URL="https://api.ciscospark.com/v1/messages?roomId="+room+"&max=3"
    print(URL)
    r = requests.get(URL,headers={'Authorization': 'Bearer ' + WEBEX_TEAMS_ACCESS_TOKEN,
        'Content-Type': 'application/json'}).json()

    raw_email_message=[]
    a=0
    for i in r["items"]:
        #print (i["personEmail"])
        #print (i["text"])
        raw_email_message.append("from: "+i["personEmail"]+" "+i["text"])
        
    email_message="<break time=\"0.5s\"/>".join(str(x) for x in raw_email_message)
    print(email_message)
    return email_message

def create_message(room,user_message):
    
    messages_create = api.messages.create(room,text=user_message)
   

    #print(messages_list.text)
    #messages_list.
    #for i in messages_list:
    #   print (i.text)

    #return result_room


#room_name="Test Room v3"
#room=find_roomid(room_name)

#list_message(room)


app = Flask(__name__)

@app.route('/')
def homepage():
    print(requests)
    return "hello world!"

ask = Ask(app, "/webex")

@ask.launch
def start_skill():
    print(requests)
    session.attributes['reply']=0
    #all_rooms = api.rooms.list()
    #try:
    #    all_rooms=api.rooms.list()
    #except:
    #    return statement ("Error encountered on API")
    welcome_message="Hello there, which webex teams room do you like to listen to? Say space then the name of the Webex Teams Space. Example space GVE Enterprise Network"
    return question (welcome_message)

@ask.intent("YesIntent")
def Yes_intent():
    #headlines=get_headlines()
    if session.attributes['reply'] == 0:
        yes_msg="Which webex teams room do you like to listen to? Say space then the name of the Webex Teams Space. Example space GVE Enterprise Network"
    elif session.attributes['reply'] == 1:
        yes_msg="What is your message? Say Reply then your message. Example Reply Hi!"

    return question(yes_msg)


@ask.intent("ListMessageIntent", convert={'room_name': str})
def List_Message_intent(room_name):

    print(room_name)
    try:
        room_id=find_roomid(room_name)

        
        message_text="<speak>These are the latest 3 messages from space "+room_name+"<break time=\"0.5s\"/>"+list_message(room_id)

        ending_text=". Do you want to reply?</speak>"
        session.attributes['reply'] = 1
        session.attributes['room_id'] = room_id

    except:
        message_text="I can't access find "+room_name
        ending_text="What is the webex teams space again? Say space then the name of the Webex Teams Space. Example space GVE Enterprise Network"


    
    return question(message_text+ending_text)

@ask.intent("CreateMessageIntent", convert={'message': str})
def Create_Message_intent(message):
    try:
        user_message=create_message(session.attributes['room_id'],message)
        message_text="Message Successfully sent!"
        ending_text=". Do you want to list messages again?"
        session.attributes['reply'] = 0
       
    except:
        message_text="Something went wrong!"
        ending_text=". Do you want to list messages again?"
    return question(message_text+ending_text) 

@ask.intent("NoIntent")
def No_intent():
    #headlines=get_headlines()
    No_msg="Thank you and I hope you have a wonderful day!"
    return statement(No_msg)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)