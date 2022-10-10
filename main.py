from ast import If
from flask import Flask, request, abort
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot.models import (FollowEvent, UnfollowEvent, MessageEvent,
                            TextMessage, TextSendMessage, PostbackEvent,
                            QuickReply, QuickReplyButton)
from linebot.models.actions import (MessageAction)
import thread_eng as d
import japToZh as jap
import configparser
import json

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))

# 線呈池
executor = ThreadPoolExecutor(10)

RegisteredData_path = './registered_data.json'
with open(RegisteredData_path, 'r', encoding='utf-8') as file:
  registered_data = json.load(file)


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
    print(
      "Invalid signature. Please check your channel access token/channel secret.")
    abort(400)


@handler.add(FollowEvent)  # 加入帳號
def Follow(event):
  user_id = event.source.user_id
  registered_data[user_id] = {}
  registered_data[user_id]['State'] = 'newcome'
  reply = '歡迎使用本linebot，可以選以下功能進行翻譯喔!'
  line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
  with open(RegisteredData_path, 'w', encoding='utf-8') as file:
    json.dump(registered_data, file, ensure_ascii=False, indent=4)


@handler.add(UnfollowEvent)  # 封鎖帳號
def Unfollow(event):
  user_id = event.source.user_id
  try:
    del registered_data[user_id]
    with open(RegisteredData_path, 'w', encoding='utf-8') as file:
      json.dump(registered_data, file, ensure_ascii=False, indent=4)
  except:
    pass
  line_bot_api.unlink_rich_menu_from_user(user_id)


def handle_message_code(event):
  text = event.message.text
  user_id = event.source.user_id
  state = registered_data[user_id]['State']
  reply = "請選擇功能!"
  if text == "英翻中" and state == 'newcome':
    registered_data[user_id]['State'] = 'english'
    reply = '{}'.format('請輸入您想翻譯的英文:')
  elif text == "日翻中" and state == 'newcome':
    registered_data[user_id]['State'] = 'japanese'
    reply = '{}'.format('請輸入您想翻譯的日文:')
  elif state == 'english':
    reply_list, replytime = d.queuethread(text)
    print("完成英文翻譯並開始回傳")
    for i in range(replytime):
      print("傳送第" + str(i + 1) + "則訊息")
      print("傳送訊息:", reply_list[i])
      print(type(reply_list[i]))
      line_bot_api.push_message(user_id, TextSendMessage(text=reply_list[i]))
      # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_list[i]))
    registered_data[user_id]['State'] = 'newcome'
    return
  elif state == 'japanese':
    reply = jap.changeString(text)
    registered_data[user_id]['State'] = 'newcome'
  with open(RegisteredData_path, 'w', encoding='utf-8') as file:
    json.dump(registered_data, file, ensure_ascii=False, indent=4)
  line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  executor.submit(handle_message_code, (event))


if __name__ == "__main__":
  app.run(debug=True)
