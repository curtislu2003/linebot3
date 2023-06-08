from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import pandas as pd
def work():

   url='https://docs.google.com/spreadsheets/d/e/2PACX-1vSveRQbLbdsOw-4uh_60nAyrztHHxKoYnuT4eL6KeM4ZZRfK2dwl4zwYZgN0OKJfAuVP1-wv_TM2GZj/pub?gid=1258066858&single=true&output=csv'
   df = pd.read_csv(url)
   df1 = df[['周别', '机台编号', '生产效率', '实际重量/KG', '损耗']]
   df1= df[df['周别'] ==31]
   df2 = df1.groupby('机台编号')['实际重量/KG'].sum().reset_index()
   df3 = df1.groupby('机台编号')['损耗'].mean()
   df4 = df1.groupby('机台编号')['生产效率'].mean()
   df5 = pd.merge(df2,df3, on='机台编号')
   df6 = pd.merge(df5,df4, on='机台编号')

   return df6

app = Flask(__name__)

line_bot_api = LineBotApi('D3bAHNtDhBY0qwOHUNxl3jHIeoFWOcvEMMYeOiqi70dT+1syMyxXDKtLSyi/OFO/GAcgrCW8Be4Pumq7AhszmEn8al5o0VN3GChVolIEJoqX2d7dIqlxGgYg/vAYbKoxnEdG+JlnoK41dGQ9Ah8oZQdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('U0c2ff020ebdb9b4cb829964f35c87a02')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=work(event.message.text)))


if __name__ == "__main__":
    app.run()
