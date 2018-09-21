import os
import sys
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('sensai.config')

db = SQLAlchemy(app)
from sensai.views import get_menus

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

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
        abort(400)

    return {'statusCode': 200, 'body': '{}'}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    menus = get_menus()
    menu = menus[0].name
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=menu))
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
        '''


if __name__ == "__main__":
    app.run()
