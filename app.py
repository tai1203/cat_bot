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


app = Flask(__name__)

line_bot_api = LineBotApi('h1FJ4YvejcImlsyth6H0qqcsCUvrF4YsF/J0pJeh02DnESHAGrDa1ElreOtBsrYAWFjrEa6M85GmPr9KAM3zVMlmLT1IgUoHmyYEksXAFEw+mNdaG1zTVTjTih0obaLDm0B7YuRMtxZ2Fmg3jzh1mAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0d463d094be0b7ab593202cf9d8d1cd8')


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

# def random_cat_url():
#     r = requests.get("https://api.thecatapi.com/v1/images/search", allow_redirects=True)
#     print(f"random_cat_url: {r.status_code}")

#     json = r.json()
#     cat_url = json[0]["url"]
#     print(type(cat_url))
#     print(cat_url)
#     return cat_url

# def random_dog_url():
#     r = requests.get("https://api.thedogapi.com/v1/images/search", allow_redirects=True)
#     print(f"random_dog_url: {r.status_code}")
    
#     json = r.json()
#     dog_url = json[0]["url"]
#     print(type(dog_url))
#     print(dog_url)
#     return dog_url
 
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     cat_url = random_cat_url()
#     dog_url = random_dog_url()
#     message = event.message.text
#     if message == '喵':
#         try:
#             line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= cat_url, preview_image_url= cat_url))
#         except:
#             line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'error'))
#     elif message == '汪':
#         try:
#             line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= dog_url, preview_image_url= dog_url))
#         except:
#             line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'error'))
#     elif message == 'help':
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text= '需要貓貓時請說喵 要狗狗時請說汪'))
            
  
  
# @handler.add(FollowEvent)
# def handle_follow_event(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text= '嗨嗨尼好 需要貓貓時請說喵 要狗狗時請說汪')
#     )

# openapi: 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
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=environ.get('PORT'))
