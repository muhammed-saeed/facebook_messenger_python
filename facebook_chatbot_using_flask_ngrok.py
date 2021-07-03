from flask import Flask, request
from pymessenger import Bot
from werkzeug.wrappers import response
'''
steps:
1- create facebook shell called flask to take-care about the https request and respond
'''

app = Flask(__name__)
#Find resources on the filesystem
#Used by extensions to improve debugging information

verify_token = 'handshake with the facebook messenger'
page_access_token = 'EAAETyMGKxZBcBAG6QiC9cvKly0LPrnXLbDX570rvVZAUtqZCLCGZA0lyicZCyt5h4Blr3OoqZBOcUmMX1keMTerQNlXK0luWbgduen6xQAZA6CHfTFyijaqpuJDBJRfxGg4K3hlCsulvkM8DmoVZAq4tfYsLTPnH8R1qngEIJfnyZBrxASiKkp8fR'

bot = Bot(page_access_token)

def process_message(text):
    formatted_message = text.lower()
    if formatted_message == 'test':
        response = 'Test Successfull!!!'
        
    elif formatted_message == 'what are your hours ?':
        response = 'We are working on these days and for those hours'
    else:
        response = 'send image'
    
    return response

@app.route('/', methods = ['GET', 'POST'])
def webhook():
    #for facebook to connect to your website or app and verify the message
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == verify_token:
            # request.args is bringing a "dictionary" object for you. 
            # The "dictionary" object is similar to other collection-type of objects in Python,
            # in that it can store many elements in one single object. Therefore the answer to your question
            return request.args.get('hub.challenge')
            #communicate and make sure they are the same
        else:
            return "hello youtube we are not connected to facebook!!"
    
    elif request.method == 'POST':
        payload = request.json
        #note the payload defines the actions taken by the bot depending on the users input
        event = payload['entry'][0]['messaging']
        with open('/home/muhammed/Documents/Enigma/Chatbots/Flask and ngrok 2 videos/payload_text_file.txt','a') as f:
            f.write(str(payload))
            f.write('\n')

        for msg in event:
            print(f'the shape of the payload is {payload} and its length is {len(payload)}')
            text = msg['message']['text']
            sender_id = msg['sender']['id']
            response = process_message(text)
            if response == 'send image':
                bot.send_image_url(sender_id, 'data:image/jpeg;base64,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' )
            else:
                bot.send_text_message(sender_id, response)
            
            return 'Message recieved!!!'

    
    else:
        print(request.data)
        return "200"
        #in case there is no get at all

#if __name__ == '__main__':
#    webhook()

if __name__ == '__main__':
    app.run(threaded = True, port = 5000)