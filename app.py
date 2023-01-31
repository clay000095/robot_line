
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)


line_bot_api = LineBotApi('7u4CpY+aTDf9W/RPzni523xbn58K3W1TEWyT0SHqXamCq+JlCDzIAPv+vsmye0xrX/cZrVou2Fvw0X24Bw8FLYZPbKVwQM4r4Mp4m6saMVg/6z5pnuCfGD4DsjzttEQ59j2cwTcVRE1l3LGbthLMJAdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('a11833d3e2e7dded62b45187a02eca39')

line_bot_api.push_message('U7084bc0b820b41725e89e0cc5b4c30fe', TextSendMessage(text='請開始你的表演'))

#callback's Post Request
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
    message = text=event.message.text
    if re.match('你在哪',message):
        # VocieTube：https://tw.voicetube.com/challenges/pronunciation/20210604
        audio_message = AudioSendMessage(
            original_content_url='https://cdn.voicetube.com/everyday_records/5131/1622711427.mp3',
            duration=2000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
