{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#載入LineBot所需要的套件\n",
    "from flask import Flask, request, abort\n",
    "\n",
    "from linebot import (\n",
    "    LineBotApi, WebhookHandler\n",
    ")\n",
    "from linebot.exceptions import (\n",
    "    InvalidSignatureError\n",
    ")\n",
    "from linebot.models import *\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# 必須放上自己的Channel Access Token\n",
    "line_bot_api = LineBotApi('dxXnzAfehaEFn4wc2QPQ2TshuuvjpVeppPJFCsLVuEFl2Kq82UIgw2eN9byiudwCvjw/iIPvHy6LyQO5XZP34RgH9MF4Yh+ZothnbvUXghY0veC8Snf8YuNJXVzuUrhKiTfABsjQ4GJ0LVQsnjut2QdB04t89/1O/w1cDnyilFU=')\n",
    "# 必須放上自己的Channel Secret\n",
    "handler = WebhookHandler('a218e7c2b920e92b4d528d268b830d38')\n",
    "\n",
    "line_bot_api.push_message('U0f84a7f70cfdf86b7afa00cd651f5836', TextSendMessage(text='你可以開始了'))\n",
    "\n",
    "# 監聽所有來自 /callback 的 Post Request\n",
    "@app.route(\"/callback\", methods=['POST'])\n",
    "def callback():\n",
    "    # get X-Line-Signature header value\n",
    "    signature = request.headers['X-Line-Signature']\n",
    "\n",
    "    # get request body as text\n",
    "    body = request.get_data(as_text=True)\n",
    "    app.logger.info(\"Request body: \" + body)\n",
    "\n",
    "    # handle webhook body\n",
    "    try:\n",
    "        handler.handle(body, signature)\n",
    "    except InvalidSignatureError:\n",
    "        abort(400)\n",
    "\n",
    "    return 'OK'\n",
    "\n",
    "#訊息傳遞區塊\n",
    "@handler.add(MessageEvent, message=TextMessage)\n",
    "def handle_message(event):\n",
    "    message = TextSendMessage(text=event.message.text)\n",
    "    line_bot_api.reply_message(event.reply_token,message)\n",
    "\n",
    "#主程式\n",
    "import os\n",
    "if __name__ == \"__main__\":\n",
    "    port = int(os.environ.get('PORT', 5000))\n",
    "    app.run(host='0.0.0.0', port=port)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
