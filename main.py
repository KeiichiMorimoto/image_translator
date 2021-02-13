import os
from io import BytesIO

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, MessageEvent, TextMessage, TextSendMessage)

from image_translator import translate_eng_image_to_ja
 
app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
 
### Webhookからのリクエストをチェックする ###
@app.route("/callback", methods=['POST'])
def callback():
  print("callback() : in")
  # リクエストヘッダーから署名検証のための値を取得します。
  signature = request.headers['X-Line-Signature']
 
  # リクエストボディを取得します。
  body = request.get_data(as_text=True)
  print("body:", body)

  app.logger.info("Request body: " + body)

  # handle webhook body
  # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
  try:
    handler.handle(body, signature)
  # 署名検証で失敗した場合、例外を出す。
  except InvalidSignatureError:
    print("InvalidSignatureError")
    abort(400)
  # handleの処理を終えればOK
  return 'OK'
 
### Text受信時 ###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  print("handle_message:", event)
  text = event.message.text

  messages = [
        TextSendMessage(text=text),
        TextSendMessage(text='英文が書いてある画像を送ってみてね'),
    ]
  
  reply_message(event, messages)
 
### 画像受信時 ###
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
  print("handle_image:", event)
 
  message_id = event.message.id
  image_url = getImageLine(message_id)
  #message_content = line_bot_api.get_message_content(message_id)   # message_idから画像のバイナリデータを取得
  #image = BytesIO(message_content.content)

  print(image_url)

  return
  
  try:
    image_text = translate_eng_image_to_ja(image_url=image_url)
    #image_text = translate_eng_image_to_ja(image=image)
    print(image_text)
  
  except Exception as e:
    print("[Error]エラーが発生しました")
  

def reply_message(event, messages):
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages,
    )

# ポート番号の設定
if __name__ == "__main__":
  port = os.environ.get('PORT', 3333)
  app.run(host="0.0.0.0", port=port)

def getImageLine(id):

  line_url = 'https://api.line.me/v2/bot/message/' + id + '/content/'

  # 画像の取得
  result = requests.get(line_url, headers=header)
  print(result)

  # 画像の保存
  im = Image.open(BytesIO(result.content))
  filename = '/tmp/' + id + '.jpg'
  print(filename)
  im.save(filename)

  return filename

