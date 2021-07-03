import os
import sys
import json

import requests
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

access_token = 'EAADvzeABWHcBAJB86Qvf3qtqmZArjjgf77fcnBA9nw3bZBo5acmZBq4KHv3aEddJmyeyQ7jpKNQ7V3WaHcrmotvdFI6nCyLOIu1ZCaNmtonc0LYI3Q6E0sITwdSI6hg2KguaAs7w3Y8pclLUdaQ3ZAEv7VC9R6fbGlZAkeEZBzlWpEkDs09iaAY'
verify_token = 'handshake'
bot = Bot(access_token)
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])   
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    # data is the payload which is the information needed by the bot to generate response
    payload = data
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    with open('/home/muhammed/Documents/Enigma/Chatbots/Flask and ngrok 2 videos/payload_text_file.txt','a') as f:
            f.write(str(payload))
            f.write('\n')
    if data["object"] == "page":   # make sure this is a page subscription

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                if messaging_event.get("message"):     # someone sent us a message
                    if messaging_event['message'].get('quick_reply'):
                        received_quick_reply(messaging_event)
                    else:
                        received_message(messaging_event)

                elif messaging_event.get("delivery"):  # delivery confirmation
                    pass
                    # received_delivery_confirmation(messaging_event)

                elif messaging_event.get("optin"):     # optin confirmation
                    pass
                    # received_authentication(messaging_event)

                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    received_postback(messaging_event)

                else:    # uknown messaging_event
                    log("Webhook received unknown messaging_event: " + messaging_event)

    return "ok", 200



def received_message(event):

    sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
    
    # could receive text or attachment but not both
    if "text" in event["message"]:
        message_text = event["message"]["text"]

        # parse message_text and give appropriate response   
        if message_text == 'image' or message_text == 'Image':
            send_image_message(sender_id)

        elif message_text == 'file' or message_text == 'File':
            send_file_message(sender_id)

        elif message_text == 'audio' or message_text == 'Audio':
            send_audio_message(sender_id)

        elif message_text == 'video' or message_text == 'Video':
            send_video_message(sender_id)

        elif message_text == 'button' or message_text == 'Button':
            send_button_message(sender_id)

        elif message_text == 'generic' or message_text == 'Generic':
            send_generic_message(sender_id)

        elif message_text == 'share' or message_text == 'Share':
            send_share_message(sender_id)
        elif message_text == 'pymessenger' or message_text == 'Pymessenger':
            send_generic_message_pymessenger(sender_id)
        elif message_text == 'quick_reply' or message_text ==  'Quick reply':
            send_quick_reply_text_message(sender_id)
        else: # default case
            send_text_message(sender_id, "Echo: " + message_text)

    elif "attachments" in event["message"]:
        message_attachments = event["message"]["attachments"]   
        send_text_message(sender_id, "Message with attachment received")


# Message event functions
def send_text_message(recipient_id, message_text):

    # encode('utf-8') included to log emojis to heroku logs
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text.encode('utf-8')))

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    call_send_api(message_data)


def send_generic_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Asylex",
                        "subtitle": "free online legal aid on Swiss asylum law",
                        "item_url": "https://asylex.ch/",               
                        "image_url": "https://media-exp2.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAr8AAAAJDYyNGU1NWM4LTA4NzYtNGU4Yy1hNmY5LTA3MDAzOWRhZWFkNQ.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://asylex.ch/docs/faq_en.pdf",
                            "title": "Open FAQ"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for first bubble",
                        }],
                    }, {
                        "title": "Google",
                        "subtitle": "Find all your answers",
                        "item_url": "https://www.google.com/",               
                        "image_url": "https://www.google.ch/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.google.ch/",
                            "title": "Google Suche"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for second bubble",
                        }]
                    }]
                }
            }
        }
    })

    log("sending template with choices to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)

def send_generic_message_pymessenger(recipient_id):
    #how to define the type of the 
    message_data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Asylex",
                        "subtitle": "free online legal aid on Swiss asylum law",
                        "item_url": "https://asylex.ch/",               
                        "image_url": "https://media-exp2.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAr8AAAAJDYyNGU1NWM4LTA4NzYtNGU4Yy1hNmY5LTA3MDAzOWRhZWFkNQ.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://asylex.ch/docs/faq_en.pdf",
                            "title": "Open FAQ"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for first bubble",
                        }],
                    }, {
                        "title": "Google",
                        "subtitle": "Find all your answers",
                        "item_url": "https://www.google.com/",               
                        "image_url": "https://www.google.ch/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.google.ch/",
                            "title": "Google Suche"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for second bubble",
                        }]
                    }]
                }
            }
        }
    }

    log("sending template with choices to {recipient}: ".format(recipient=recipient_id))

    bot.send_message(recipient_id, message_data['message'])
    

  

def send_image_message(recipient_id):
    '''
    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"image",
                "payload":{
                    "url":"https://steamuserimages-a.akamaihd.net/ugc/159156190291189840/D972C569C3D39D33F5F9937B5E534F24D9921CD4/"
                }
            }
        }
    })
    '''
    message_data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"image",
                "payload":{
                    "url":"https://steamuserimages-a.akamaihd.net/ugc/159156190291189840/D972C569C3D39D33F5F9937B5E534F24D9921CD4/"
                }
            }
        }
    }
    print(f'testing the json.dumps is \n {message_data} {type(message_data)}')
    log("sending image to {recipient}: ".format(recipient=recipient_id))

    call_send_api_2(message_data)


def send_file_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"file",
                "payload":{
                    "url":"https://asylex.ch/docs/asylverfahren_en.pdf"
                }
            }
        }
    })

    log("sending file to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)


def send_audio_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"audio",
                "payload":{
                    "url":"http://vochabular.ch/downloads/Audio/Kapitel2/3_Kapitel2_UebungAe_D/1.mp3"
                }
            }
        }
    })

    log("sending audio to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)


def send_video_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"video",
                "payload":{
                    "url":"http://techslides.com/demos/sample-videos/small.mp4"
                }
            }
        }
    })

    log("sending video to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)


def send_button_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://asylex.ch",
                        "title":"Asylex website"
                    },
                    {
                        "type":"postback",
                        "title":"Call Postback",
                        "payload":"Payload for send_button_message()"
                    }
                    ]
                }
            }
        }
    })

    log("sending button to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)



def send_share_message(recipient_id):

    # Share button only works with Generic Template
    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                    {
                        "title":"Asylex link",
                        "subtitle":"free online legal aid on Swiss asylum law",
                        "image_url":"https://media-exp2.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAr8AAAAJDYyNGU1NWM4LTA4NzYtNGU4Yy1hNmY5LTA3MDAzOWRhZWFkNQ.png",
                        "buttons":[
                        {
                            "type":"element_share"
                        }
                        ]
                    }    
                    ]
                }
        
            }
        }
    })

    log("sending share button to {recipient}: ".format(recipient=recipient_id))
    # log us
    call_send_api(message_data)


def send_recipte(recipient_id):
    message = {
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":"Stephane Crozatier",
        "order_number":"12345678902",
        "currency":"USD",
        "payment_method":"Visa 2345",        
        "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
        "timestamp":"1428444852",         
        "address":{
          "street_1":"1 Hacker Way",
          "street_2":"",
          "city":"Menlo Park",
          "postal_code":"94025",
          "state":"CA",
          "country":"US"
        },
        "summary":{
          "subtotal":75.00,
          "shipping_cost":4.95,
          "total_tax":6.19,
          "total_cost":56.14
        },
        "adjustments":[
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"$10 Off Coupon",
            "amount":10
          }
        ],
        "elements":[
          {
            "title":"Classic White T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":2,
            "price":50,
            "currency":"USD",
            "image_url":"http://petersapparel.parseapp.com/img/whiteshirt.png"
          },
          {
            "title":"Classic Gray T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":1,
            "price":25,
            "currency":"USD",
            "image_url":"https://cdn.motor1.com/images/mgl/NeEOn/s1/2012-343195-2014-mercedes-benz-sls-amg-black-series1.jpg"
          }
        ]
      }
    }
    }
    
    bot.send_message(recipient_id, message)

def received_postback(event):

    sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

    # The payload param is a developer-defined field which is set in a postback
    # button for Structured Messages
    payload = event["postback"]["payload"]

    log("received postback from {recipient} with payload {payload}".format(recipient=recipient_id, payload=payload))

    if payload == 'Get Started':
        # Get Started button was pressed
        send_text_message(sender_id, "Welcome to the Asylex bot - Anything you type will be echoed back to you, except for the following keywords: image, file, audio, video, button, generic, share.")
    elif payload == 'Payload for send_button_message()':
        send_text_message(sender_id, "Welcome to the Asylex bot - Postback was called")
    elif payload == 'Payload for first bubble':
        send_text_message(sender_id, 'hear me roar ladies and genetlmens')

    elif payload == 'purchase':
        bot.send_text_message(sender_id, ' hi sender here are your purchases')
        send_recipte(sender_id)
        
    else:

        # Notify sender that postback was successful
        send_text_message(sender_id, "Welcome to the Asylex bot - Anything you type will be echoed back to you, except for the following keywords: image, file, audio, video, button, generic, share.")

def received_quick_reply(event):
   
    sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

    # The payload param is a developer-defined field which is set in a postback
    # button for Structured Messages
    payload = event["message"]["quick_reply"]['payload']

    log("received postback from {recipient} with payload {payload}".format(recipient=recipient_id, payload=payload))

    if payload == 'Get Started':
        # Get Started button was pressed
        send_text_message(sender_id, "Welcome to the Asylex bot - Anything you type will be echoed back to you, except for the following keywords: image, file, audio, video, button, generic, share.")
    elif payload == 'Payload for send_button_message()':
        send_text_message(sender_id, "Welcome to the Asylex bot - Postback was called")
    elif payload == 'Payload for first bubble':
        send_text_message(sender_id, 'hear me roar ladies and genetlmens')

    elif payload == 'purchase':
        bot.send_text_message(sender_id, ' hi sender here are your purchases')
        send_recipte(sender_id)
        
    else:

        # Notify sender that postback was successful
        send_text_message(sender_id, "Welcome to the Asylex bot - Anything you type will be echoed back to you, except for the following keywords: image, file, audio, video, button, generic, share.")


def send_quick_reply_text_message(recipient_id):
    message = {
        "text": "Pick a color:",
        "quick_replies":[
        {
            "content_type":"text",
            "title":"Red",
            "payload":"<POSTBACK_PAYLOAD>",
            "image_url":"http://example.com/img/red.png"
        },{
            "content_type":"text",
            "title":"Green",
            "payload":"<POSTBACK_PAYLOAD>",
            "image_url":"http://example.com/img/green.png"
        },
        {
            "content_type":"text",
            "title":"Purchase",
            "payload":"purchase",
            #"image_url":"http://example.com/img/green.png"
        }
        ]
    }
    bot.send_message(recipient_id, message)

def call_send_api(message_data):

    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        #this part responsible for printing the error encountered in the process

def call_send_api_2(message_data):

    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, json=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        #this part responsible for printing the error encountered in the process

def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()

# import os, sys
# from flask import Flask, request
# from utils import wit_response, get_news_elements
# from pymessenger import Bot
# import requests,json

# app = Flask(__name__)

# bot = Bot(os.environ["PAGE_ACCESS_TOKEN"])
# PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')


# @app.route('/', methods=['GET'])
# def verify():
# 	# Webhook verification
#     if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
#         if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
#             return "Verification token mismatch", 403
#         return request.args["hub.challenge"], 200
#     return "Hello world", 200


# @app.route('/', methods=['POST'])
# def webhook():
# 	data = request.get_json()
# 	log(data)

# 	if data['object'] == 'page':
# 		for entry in data['entry']:
# 			for messaging_event in entry['messaging']:

# 				# IDs
# 				sender_id = messaging_event['sender']['id']
# 				recipient_id = messaging_event['recipient']['id']

# 				if messaging_event.get('message'):
# 					# Extracting text message
# 					if 'text' in messaging_event['message']:
# 						messaging_text = messaging_event['message']['text']
# 					else:
# 						messaging_text = 'no text'

# 					# Echo
# 					#response = messaging_text
					
# 					# response = None
# 					# entity, value = wit_response(messaging_text)
					
# 					# if entity == 'newstype':
# 					# 	response = "OK. I will send you {} news".format(str(value))
# 					# elif entity == 'location':
# 					# 	response = "OK. So, you live in {0}. I will send you top headlines from {0}".format(str(value))
					
# 					# if response == None:
# 					# 	response = "Sorry, I didn't understand"

# 					categories = wit_response(messaging_text)
# 					elements = get_news_elements(categories)
# 					bot.send_generic_message(sender_id, elements)
				
# 				elif messaging_event.get('postback'):
# 					# HANDLE POSTBACKS HERE
# 					payload = messaging_event['postback']['payload']
# 					if payload ==  'SHOW_HELP':
# 						bot.send_quickreply(sender_id, HELP_MSG, news_categories)

# 	return "ok", 200

# def set_greeting_text():
# 	headers = {
# 		'Content-Type':'application/json'
# 		}
# 	data = {
# 		"setting_type":"greeting",
# 		"greeting":{
# 			"text":"Hi {{user_first_name}}! I am a news bot"
# 			}
# 		}
# 	ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(PAGE_ACCESS_TOKEN)
# 	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
# 	print(r.content)

# def set_persistent_menu():
# 	headers = {
# 		'Content-Type':'application/json'
# 		}
# 	data = {
# 		"setting_type":"call_to_actions",
# 		"thread_state" : "existing_thread",
# 		"call_to_actions":[
# 			{
# 				"type":"web_url",
# 				"title":"Meet Asylex",
# 				"url":"https://asylex.ch" 
# 			},
# 			{
# 				"type":"postback",
# 				"title":"Help",
# 				"payload":"SHOW_HELP"
# 			}]
# 		}
# 	ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(PAGE_ACCESS_TOKEN)
# 	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
# 	print(r.content)



# def log(message):
# 	print(message)
# 	sys.stdout.flush()

# set_persistent_menu()
# set_greeting_text()

if __name__ == "__main__":
     app.run(threaded = True, port= 5000)