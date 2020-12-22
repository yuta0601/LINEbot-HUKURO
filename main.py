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

# payload = {
#   "type": "bubble",
#   "hero": {
#     "type": "image",
#     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png",
#     "size": "full",
#     "aspectRatio": "20:13",
#     "aspectMode": "cover"
#   },
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "spacing": "sm",
#     "contents": [
#       {
#         "type": "text",
#         "text": "Arm Chair, White",
#         "weight": "bold",
#         "size": "xl",
#         "wrap": true,
#         "contents": []
#       },
#       {
#         "type": "box",
#         "layout": "baseline",
#         "contents": [
#           {
#             "type": "text",
#             "text": "$49",
#             "weight": "bold",
#             "size": "xl",
#             "flex": 0,
#             "wrap": true,
#             "contents": []
#           },
#           {
#             "type": "text",
#             "text": ".99",
#             "weight": "bold",
#             "size": "sm",
#             "flex": 0,
#             "wrap": true,
#             "contents": []
#           }
#         ]
#       }
#     ]
#   },
#   "footer": {
#     "type": "box",
#     "layout": "vertical",
#     "spacing": "sm",
#     "contents": [
#       {
#         "type": "button",
#         "action": {
#           "type": "uri",
#           "label": "Add to Cart",
#           "uri": "https://linecorp.com"
#         },
#         "style": "primary"
#       },
#       {
#         "type": "button",
#         "action": {
#           "type": "uri",
#           "label": "Add to wishlist",
#           "uri": "https://linecorp.com"
#         }
#       }
#     ]
#   }
# }

# container_obj = FlexSendMessage.new_from_json_dict(payload)

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

    if event.message.text == "moodle":
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text="https://moodle.it-hac-neec.jp/login/index.php"),
        )

    elif event.message.text == "is13":
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text="https://sites.google.com/site/is13hp/home"),
        )
    
    # elif event.message.text = "test":
    #     line_bot_api.reply_message(
    #         event.reply_token, 
    #         TextSendMessage(text=container_obj),
    #     )

    else:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=event.message.text),
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