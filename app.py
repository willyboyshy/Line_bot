from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage ,ImageSendMessage 
import json ,os
import od
Save_dir = "./upload/"

app = Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')


@app.route("/", methods=['POST','GET'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):  
    if (event.message.type == 'image'):
        if (event.message.type == "image"):
            SendImage = line_bot_api.get_message_content(event.message.id)
        fileName = event.message.id + ".png"
    elif (event.message.type == 'video'):
        fileName = event.message.id + ".mp4"
    elif (event.message.type == 'file'):
        fileName = json.loads(str(event.message))["fileName"] 
    else :
        fileName = ""

    if (fileName != ""):
        message_content  = line_bot_api.get_message_content(event.message.id)
        with open(Save_dir + fileName , 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(od.upload(fileName))))

if __name__ == "__main__":
    if not os.path.exists(Save_dir):
        os.makedirs(Save_dir)
    app.run(port=8080,debug=True)