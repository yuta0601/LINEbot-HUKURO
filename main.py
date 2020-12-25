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

# flex_message_json_string = """
# {
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
# """

# flex_message_json_string="""
# {  
#   type: bubble,
#   altText: Flex Message,
#   contents: {
#     type: bubble,
#     direction: ltr,
#     header: {
#       type: box,
#       layout: vertical,
#       contents: [
#         {
#           type: text,
#           text: ,
#           align: center
#         }
#       ]
#     },
#     hero: {
#       type: image,
#       url: https://images-na.ssl-images-amazon.com/images/I/81dkWPlc-AL._SX522_.jpg,
#       size: full,
#       aspectRatio: 1.51:1,
#       aspectMode: fit
#     },
#     footer: {
#       type: box,
#       layout: horizontal,
#       contents: [
#         {
#           type: button,
#           action: {
#             type: uri,
#             label: 購入,
#             uri: https://www.amazon.co.jp/天然水-【Amazon-co-jp-限定】サントリー-南アルプスの天然水-2L×9本/dp/B07F1CCSJZ/ref=sr_1_1_sspa?__mk_ja_JP=カタカナ&keywords=水&qid=1563628084&s=gateway&sr=8-1-spons&psc=1
#           }
#         }
#       ]
#     }
#   }
# }
# """
# flex_message_json_dict = json.loads(flex_message_json_string)

# payload = """
# {
#   "type": "flex",
#   "altText": "Flex Message",
#   "contents": {
#     "type": "bubble",
#     "hero": {
#       "type": "image",
#       "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
#       "size": "full",
#       "aspectRatio": "20:13",
#       "aspectMode": "cover",
#       "action": {
#         "type": "uri",
#         "label": "Line",
#         "uri": "https://linecorp.com/"
#       }
#     },
#     "body": {
#       "type": "box",
#       "layout": "vertical",
#       "contents": [
#         {
#           "type": "text",
#           "text": "Brown Cafe",
#           "size": "xl",
#           "weight": "bold"
#         },
#         {
#           "type": "box",
#           "layout": "baseline",
#           "margin": "md",
#           "contents": [
#             {
#               "type": "icon",
#               "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
#               "size": "sm"
#             },
#             {
#               "type": "icon",
#               "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
#               "size": "sm"
#             },
#             {
#               "type": "icon",
#               "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
#               "size": "sm"
#             },
#             {
#               "type": "icon",
#               "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
#               "size": "sm"
#             },
#             {
#               "type": "icon",
#               "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
#               "size": "sm"
#             },
#             {
#               "type": "text",
#               "text": "4.0",
#               "flex": 0,
#               "margin": "md",
#               "size": "sm",
#               "color": "#999999"
#             }
#           ]
#         },
#         {
#           "type": "box",
#           "layout": "vertical",
#           "spacing": "sm",
#           "margin": "lg",
#           "contents": [
#             {
#               "type": "box",
#               "layout": "baseline",
#               "spacing": "sm",
#               "contents": [
#                 {
#                   "type": "text",
#                   "text": "Place",
#                   "flex": 1,
#                   "size": "sm",
#                   "color": "#AAAAAA"
#                 },
#                 {
#                   "type": "text",
#                   "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
#                   "flex": 5,
#                   "size": "sm",
#                   "color": "#666666",
#                   "wrap": True
#                 }
#               ]
#             },
#             {
#               "type": "box",
#               "layout": "baseline",
#               "spacing": "sm",
#               "contents": [
#                 {
#                   "type": "text",
#                   "text": "Time",
#                   "flex": 1,
#                   "size": "sm",
#                   "color": "#AAAAAA"
#                 },
#                 {
#                   "type": "text",
#                   "text": "10:00 - 23:00",
#                   "flex": 5,
#                   "size": "sm",
#                   "color": "#666666",
#                   "wrap": True
#                 }
#               ]
#             }
#           ]
#         }
#       ]
#     },
#     "footer": {
#       "type": "box",
#       "layout": "vertical",
#       "flex": 0,
#       "spacing": "sm",
#       "contents": [
#         {
#           "type": "button",
#           "action": {
#             "type": "uri",
#             "label": "CALL",
#             "uri": "https://linecorp.com"
#           },
#           "height": "sm",
#           "style": "link"
#         },
#         {
#           "type": "button",
#           "action": {
#             "type": "uri",
#             "label": "WEBSITE",
#             "uri": "https://linecorp.com"
#           },
#           "height": "sm",
#           "style": "link"
#         },
#         {
#           "type": "spacer",
#           "size": "sm"
#         }
#       ]
#     }
#   }
# }
# """

# # container_obj = FlexSendMessage.new_from_json_dict(payload)
# container_obj = json.loads(payload)

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
    
    # elif event.message.text == "test":
    #     line_bot_api.reply_message(
    #         event.reply_token, 
    #         FlexSendMessage(
    #           alt_text='test',
    #           messages=container_obj,
    #         ),
    #     )
    elif event.message.text == "test":
        line_bot_api.reply_message(
            event.reply_token, 
            # TextSendMessage(text="https://sites.google.com/site/is13hp/home"),
            FlexSendMessage(
                alt_text="test",
                # contents=flex_message_json_dict,
                contents={
                    'type': 'bubble',
                    'direction': 'ltr',
                    'hero': {
                        'type': 'image',
                        'url': 'https://example.com/cafe.jpg',
                        'size': 'full',
                        'aspectRatio': '20:13',
                        'aspectMode': 'cover',
                        'action': { 'type': 'uri', 'uri': 'http://example.com', 'label': 'label' }
                    }
                }
            )
        )
    
    # elif event.message.test == "test":
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         FlexSendMessage(
    #             # alt_text="test",
    #             contents=flex_message_json_dict
    #         ),
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