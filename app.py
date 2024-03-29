from typing import Text
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FollowEvent, JoinEvent
)
from os import environ

import requests
import os
import openai
#API token:
line_bot_api = LineBotApi('')
handler = WebhookHandler('')
openai.organization = ""
openai.api_key = ""
openai.Model.list()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def random_cat_url():
    r = requests.get("https://api.thecatapi.com/v1/images/search", allow_redirects=True)
    print(f"random_cat_url: {r.status_code}")

    json = r.json()
    cat_url = json[0]["url"]
    print(type(cat_url))
    print(cat_url)
    return cat_url

def random_dog_url():
    r = requests.get("https://api.thedogapi.com/v1/images/search", allow_redirects=True)
    print(f"random_dog_url: {r.status_code}")
    
    json = r.json()
    dog_url = json[0]["url"]
    print(type(dog_url))
    print(dog_url)
    return dog_url
 
def hi_chat_ai(event):
    message = event.message.text
    reply_msg = ''
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt=message,
        max_tokens=256,
        temperature=0.5,
    )
        # 接收到回覆訊息後，移除換行符號
    reply_msg = response["choices"][0]["text"].replace('\n','')
    print(reply_msg)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text= reply_msg))
    return 'OK'
 
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == '喵':
        cat_url = random_cat_url()
        try:
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= cat_url, preview_image_url= cat_url))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'error1'))
    elif message == '汪':
        dog_url = random_dog_url()
        try:
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= dog_url, preview_image_url= dog_url)) 
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'error2'))
    elif message == 'help':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text= '嗨嗨尼好 需要貓貓時請說喵 要狗狗時請說汪 若都不要只想跟ai 聊天，就直接打字即可'))
    else:
        try:
            hi_chat_ai(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'error3'))            
  
  
@handler.add(FollowEvent)
def handle_follow_event(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= '嗨嗨尼好 需要貓貓時請說喵 要狗狗時請說汪 若都不要只想跟ai 聊天，就直接打字即可')
    )

# openapi: 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
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=environ.get('PORT'))
