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

app = Flask(__name__)

line_bot_api = LineBotApi('X5sz8cvxRieZR4qPOXPAzFn/6tu++me2oQqOzTvO6vm0eRRcN64Hp04Kx5dUMFvsaKo+sx1BRz5HcSX4JSzx4CfPtPrRjXj6SGiAhH+efsBaupH/cjjUoWJStZJCw5hQpi2SIRza+QDOFmTDcqfKfgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('96bce3564db3a8baa77a253d294a8d89')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()