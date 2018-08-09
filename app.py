import ast 
import base64
import io
import telegram
import mimetypes
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
from flask import request
from datetime import datetime

#### BOT STUFF

def info(bot, update):
    update.message.reply_text('This is some info')

def hello(bot, update):
    update.message.reply_text('Hello!')

TOKEN='YOURTOKEN'
bot = telegram.Bot(token=TOKEN)
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("/info", info))
dp.add_handler(CommandHandler("/hello", hello))
updater.start_webhook(listen='0.0.0.0',
                      port=8443,
                      url_path=TOKEN,
                      key='private.key',
                      cert='cert.pem',
                      webhook_url='WEBHOOKURL'+TOKEN)
######
chat = -1001127462648
app = Flask(__name__)
######
@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello Connor!</h1>
    <p>It is currently {time}.</p>

    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTivnbcZ123a7iSn6jWrlcDsS4Lao8UTfNEYU2xCHrNRcDcP0SM">
    """.format(time=the_time)

@app.route('/', methods=['POST'])
def webhook():
    print(request)
    if request.method == 'POST':
        print(request.data)
        file = open('temp.txt','w')
        file.write(str(request.data))
        file.close()
        parsed = ast.literal_eval((request.data).decode("utf-8"))
        if parsed["type"] == "image":
            print("image :))")
            path = "temp."+parsed["extension"]
            fh = open(path, "wb")
            fh.write(base64.decodebytes(bytes(parsed['data'], 'utf8')))
            fh.close()
            bot.send_photo(chat_id=chat, photo=open(path, 'rb'))
            return '', 20
        elif parsed["type"] == "audio":
            print("audio :))")
            path = "temp."+parsed["extension"]
            fh = open(path, "wb")
            fh.write(base64.decodebytes(parsed['data']))
            fh.close()
            bot.send_audio(chat_id=chat, audio=open(path, 'rb'))
            return "it's an audio!", 200
        elif parsed["type"] == "text": 
            bot.send_message(chat_id=chat, text=parsed["data"])
            print(parsed["data"])
            return "here's a text message\n", 200
        else:
            return 'oh shit\nidk what this is', 200
            warningLog =  open('{date}.txt'.format(date=datetime.date.today().strftime("%Y%m%d")),'w')
            warningLog.write(str(request.data))
            warningLog.close()
    else:
        abort(400)

 
bot.send_message(chat_id=chat, text="Live at {time}!"
    .format(time=datetime.now().strftime("%A, %d %b %Y %l:%M %p")))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

