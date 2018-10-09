#!/usr/bin/env python
import requests
import json
import time
import sys
from flask import Flask
from flask_ask import Ask, statement, question, session

#import json
#import requests
#import time
#import unidecode

BASE_URL='api.musixmatch.com/ws/1.1/matcher.lyrics'
#ticket="ST-1082-d0KK3EEWCU9n9YsuaV7e-cas"
lyrics_id="53d7601ca5d2d9ecdc04c4b0319b0c5f"
#id="ae19cd21-1b26-4f58-8ccd-d265deabb6c3"


app = Flask(__name__)


@app.route('/')
def homepage():
    print(requests)
    return "hello world!"

ask = Ask(app, "/lyrics")


#https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=jsonp&callback=callback&q_track=easy&q_artist=commodores&apikey=53d7601ca5d2d9ecdc04c4b0319b0c5f

def get_lyrics(BASE_URL,lyrics_id,song_name,song_artist):
    #api = "/network-device"

    FULL_URL = "https://"+BASE_URL+".get?format=jsonp&callback=callback&q_track="+song_name+"&q_artist="+song_artist+"&apikey="+lyrics_id
    print(FULL_URL)
    headers = {"Content-Type":"application/json"}
    response = requests.get(FULL_URL, headers=headers, verify=False)
    #print (json.dumps(response, indent = 4, separators = (",",":")))
    #print (result.text)
   
    A=response.text
    #print(A)
    result=A.replace("callback(","")
    result=result.replace(");","")

    result=json.loads(result)
    #print(result["message"]["body"]["lyrics"]["lyrics_body"])
    raw_lyrics=result["message"]["body"]["lyrics"]["lyrics_body"]
    
    list_lyrics=raw_lyrics.split("*******")
    lyrics=list_lyrics[0].replace("\n", ",")
    print(lyrics)
    return (lyrics)
        

#song_name="easy"
#song_artist="commodores"
#lyrics=get_lyrics(BASE_URL,lyrics_id,song_name,song_artist)
#print(lyrics)


@ask.launch
def start_skill():
    session.attributes['str_title']=None
    session.attributes['str_artist']=None
    print(requests)
    welcome_message="Hello there, would you like me to sing a song?"
    return question (welcome_message)

@ask.intent("YesIntent")
def Yes_intent():
    #headlines=get_headlines()
    song_msg="Which song and which artist? "
    return question(song_msg)

@ask.intent("LyricsIntent", convert={'str_title': str,'str_artist': str,'anonymous':str})
def Lyrics_intent(str_title,str_artist,anonymous):

    print(session.attributes['str_title'])
    print(session.attributes['str_artist'])
    #session.attributes['str_title']=None
    #session.attributes['str_artist']=None
    #session.attributes['str_title'] = str_title
    #session.attributes['str_artist'] = str_artist

    if str_title is not None:
        session.attributes['str_title'] = str_title

    if str_artist is not None:
        session.attributes['str_artist'] = str_artist



    if anonymous is not None:
        if session.attributes['str_title'] is None:
            session.attributes['str_title'] = anonymous
        else:
            session.attributes['str_artist'] = anonymous


    print(anonymous)
    print(session.attributes['str_title'])
    print(session.attributes['str_artist'])


    if session.attributes['str_artist'] is None:
        lyrics_text="From which artist?"
        ending_text=""
    
    else:
        try:
            lyrics_text=get_lyrics(BASE_URL,lyrics_id,session.attributes['str_title'],session.attributes['str_artist'])
            ending_text=". Do you like me to sing again?"
            session.attributes['str_title'] = None
            session.attributes['str_artist'] = None
        except:
            lyrics_text="Sorry I didn't know the song or artist"
            ending_text="Can you repeat again?"
            session.attributes['str_title'] = None
            session.attributes['str_artist'] = None

    
    return question(lyrics_text+ending_text)

@ask.intent("NoIntent")
def No_intent():
    #headlines=get_headlines()
    No_msg="Thank you and I hope you like my singing talent!"
    return statement(No_msg)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)