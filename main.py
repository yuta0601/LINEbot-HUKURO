import os
from flask import Flask, request, abort
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
    received_message = event.message.text
    msg = received_message

    if received_message == "moodle":
        msg = "https://moodle.it-hac-neec.jp/login/index.php"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    elif received_message == "is13":
        msg = "https://sites.google.com/site/is13hp/home"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )

@handler.add(FollowEvent)
def handle_follow(event):
    msg = '友達追加ありがとう'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )


def createRichmenu():
    result = False
    try:
        # define a new richmenu
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=1200, height=405),
            selected = True,
            name = 'richmenu for randomchat',
            chat_bar_text = 'TAP HERE',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=480, height=405),
                    action=MessageAction(text=config.REMOVE)
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=480, y=0, width=720, height=405),
                    action=MessageAction(text=config.NEXT)
                )
            ]
        )
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

        # upload an image for rich menu
        path = 'image'

        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

        # set the default rich menu
        line_bot_api.set_default_rich_menu(richMenuId)

        result = True

    except Exception:
        result = False

    return result


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)