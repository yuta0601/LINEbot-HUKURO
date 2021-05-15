import json
import os
from flask import (
    Flask,
    request,
    abort,
)
import re
from re import Match

from linebot import (
    LineBotApi,
    WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FollowEvent,
    ImageMessage,
    AudioMessage,
    FlexSendMessage,
    BubbleContainer,
    CarouselContainer,
)

import datetime
import pytz
import hashlib


app = Flask(__name__)

# 環境変数
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

# API
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

global count
count = 1


@app.route("/")
def hello_world():
    return "hello world!"

# Check REQUEST
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

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # global count
    # count = 1

    if event.message.text == "/user":

        # 個人情報取得(機密情報)
        userId = event.source.user_id
        # profile = line_bot_api.get_profile(userId)
        # display_name = profile.display_name
        # status_message = profile.status_message

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=userId),
        )
    elif event.message.text == "/group":

        # グループ情報を取得
        groupId = event.source.group_id

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=groupId),
        )

    else:
        now_time = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        date_str = now_time.strftime('%Y/%m/%d %H:%M:%S')
        # 2021/05/15 17:30:29

        count += 1

        userId = event.source.user_id
        hashId = userId + date_str
        hashId = hashId[0:6] + hashId[8:14]

        messages = TextSendMessage(text=
            str(count)
            + ":VIPがお送りします"
            + " ID:"
            + hashId
            + "\n"
            + event.message.text
        )

        line_bot_api.broadcast(messages=messages)

        # 匿名チャット用
        # GROUP_ID = "C26ade19153c8f3516e45e8137e6dec14"
        # line_bot_api.push_message(
        #     GROUP_ID,
        #     TextSendMessage(text=event.message.text)
        # )

        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=event.message.text),
        # )

# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image(event):
    # https://qiita.com/Sweetpotato/items/89fef4f816e33968fdda
    # 上記を参考に作成しようとしたがtensorflowがインストールできないため保留


@handler.add(FollowEvent)
def handle_follow(event):
    msg = '友達追加ありがとう'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
