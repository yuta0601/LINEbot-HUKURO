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
    FlexSendMessage,
    BubbleContainer,
    CarouselContainer,
    FollowEvent,
    ImageMessage,
    AudioMessage,
)


app = Flask(__name__)

# 環境変数
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

# API
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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

    if event.message.text == "user":

        # 個人情報取得(機密情報)
        userId = event.source.user_id
        profile = line_bot_api.get_profile(userId)
        display_name = profile.display_name
        image_url = profile.image_url
        status_message = profile.status_message

        # グループ情報を取得
        groupID = event.sorce.group_id


        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=groupID),
        )


    elif event.message.text == "foo":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hogefoo"),
        )

    elif event.message.text == "test":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="test",
                contents={
                    "type": "bubble",
                    "direction": "ltr",
                    "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "https://sites.google.com",
                            "label": "label"
                        }
                    },
                }
            )
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text),
        )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
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
