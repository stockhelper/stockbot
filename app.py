#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *



import tempfile, os
import datetime
import time


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('dxXnzAfehaEFn4wc2QPQ2TshuuvjpVeppPJFCsLVuEFl2Kq82UIgw2eN9byiudwCvjw/iIPvHy6LyQO5XZP34RgH9MF4Yh+ZothnbvUXghY0veC8Snf8YuNJXVzuUrhKiTfABsjQ4GJ0LVQsnjut2QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('a218e7c2b920e92b4d528d268b830d38')

line_bot_api.push_message('U0f84a7f70cfdf86b7afa00cd651f5836', TextSendMessage(text='請輸入指令'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
