# WebexTeamsHandsFree
WebexTeamsHandsFree

Summary: This application will allow the user to listen and reply to Webex Teams Messages using Alexa.

Requirements:
1. Webex Teams
2. Webex Teams token
3. Alexa Echo
4. Alexa Skills Creation

Optional but recommended: Heroku PaaS Cloud

Guide:

1. Replace the "XXXX" value of WEBEX_TEAMS_ACCESS_TOKEN with your token
WEBEX_TEAMS_ACCESS_TOKEN="XXXX"

2. Deploy using Heroku Paas Cloud or run using NGROK

3. Alexa Skills Creation
a. Create Alexa Skill Invocation Name
b. Add the Appendix A in JSON editor (change the invocation name to you created alexa skill invocation name)

4. Add the created Alexa Skill in Alexa App



Appendix A - Alexa JSON
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "webex hands free",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": [
                        "Exit"
                    ]
                },
                {
                    "name": "ListMessageIntent",
                    "slots": [
                        {
                            "name": "room_name",
                            "type": "AMAZON.CreativeWorkType"
                        }
                    ],
                    "samples": [
                        "space {room_name}",
                        "I would like to listen to {room_name}",
                        "I want to listen to {room_name}"
                    ]
                },
                {
                    "name": "YesIntent",
                    "slots": [],
                    "samples": [
                        "yes"
                    ]
                },
                {
                    "name": "NoIntent",
                    "slots": [],
                    "samples": [
                        "stop",
                        "thank you",
                        "no"
                    ]
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "CreateMessageIntent",
                    "slots": [
                        {
                            "name": "message",
                            "type": "AMAZON.WrittenCreativeWorkType"
                        }
                    ],
                    "samples": [
                        "message {message}",
                        "reply {message}"
                    ]
                }
            ],
            "types": []
        }
    }
}
