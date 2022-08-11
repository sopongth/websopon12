from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage
import paho.mqtt.client as mqttClient
import time

channel_secret = "516f3c4270a699099bd6ffe4b5151b68"
channel_access_token = "7oQG7iUu3kLWznQUL1Y3r6YGIe+Mcki7RJXTd3UvsvWJKOsj0twH1aLAGnXMo3N1UkkDEvA95GHHA/kV68jtRmjaEC6fB4rsPxqHR7HMT6R5VXpp+iT6nZ1o/fiDa1oMnPNAMuarZGAIfoFEQwVdsAdB04t89/1O/w1cDnyilFU="
temp = ""
humi = ""

def on_connect(client, userdata, flags, rc): 
    if rc == 0: 
        print("Connected to localhost mqtt broker")
        print("Topic : test")
        global Connected                
        Connected = True             
    else: 
        print("Connection failed")

def on_message(client, userdata, msg):
    global temp,humi
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == '@msg/temp':
        temp = msg.payload.decode('utf-8')
        print(temp)
    if msg.topic == '@msg/humi':
        humi = msg.payload.decode('utf-8')
        print(humi)
        

Connected = False 
broker_address= "mqtt.netpie.io"
port = 1883
user = "cvf4xPBERb9QDrmG8TaNi6gmMhn9jvHW"
password = "mnmp3A04kGHUL(DwkyYvWK0B2!gp(nbz" 
client = mqttClient.Client("09adabca-409b-48c8-a54d-7611665c3c63")               
client.username_pw_set(user, password=password)    
client.on_connect = on_connect
client.on_message = on_message
#client.subscribe("@msg/#", qos=0)

#try:
#    client.connect(broker_address, port=port)
#except:
#    print("Connection failed")

    #client.loop_start()
    #while Connected != True:  
    #    time.sleep(0.1)
    
#


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global temp,humi
    text = event.message.text
    print(text)
    
    try:
        client.connect(broker_address, port=port)
    except:
        print("Connection failed")
    
    if (text=="เปิดไฟ"):
        client.publish("@msg/led","ledon")
        text_out = "เปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="ปิดไฟ"):
        client.publish("@msg/led","ledoff")
        text_out = "ปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีแดง"):
        client.publish("@msg/rgb","red")
        text_out = "เปิดไฟสีแดงเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีเขียว"):
        client.publish("@msg/rgb","green")
        text_out = "เปิดไฟสีเขียวเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีน้ำเงิน"):
        client.publish("@msg/rgb","blue")
        text_out = "เปิดไฟสีน้ำเงินเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="อุณหภูมิและความชื้น"):        
        text_out = "อุณหภูมิ " + temp + " ความชื้น " + humi
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
             
if __name__ == "__main__":          
    app.run()

