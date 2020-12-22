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
    try:
        replied = text_pattern_handler.handle(event)

        if not replied:
            # Default REPLY
            # オウム返し
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

    except Exception:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('エラーです')
        )
        raise

@text_pattern_handler.add(pattern=r'^moodle$')
def reply_moodle(event: MessageEvent, match: Match):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="https://moodle.it-hac-neec.jp/login/index.php")
    )

@text_pattern_handler.add(pattern=r'^is13$')
def reply_moodle(event: MessageEvent, match: Match):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="https://sites.google.com/site/is13hp/home")
    )

@handler.add(FollowEvent)
def handle_follow(event):
    msg = '友達追加ありがとう'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)