import requests
import re
from bot_ai import *

api = 'https://api.telegram.org/bot2070925065:AAGEyOVjNlAOfuZ6E4C2Xa4_56wPQ_GeZdo'


def read_message(offset):
    data = {
        "offset": offset
    }
    res = requests.get(api+"/getUpdates", data=data)
    data = res.json()
    print(data)

    try:
        for result in data["result"]:

            chat_id = result["message"]["chat"]["id"]
            message = result["message"]["text"]     # Message from user
            message_id = result["message"]["message_id"]

            url, is_urlfound = find(message)

            if is_urlfound == "y":
                link = make_url(url)
                ss(chat_id, message_id, link)
            elif "/help" == message:
                help = "Send me any valid link to get webcapture..[to take screenshot]\nFor any problem contact with owner..\nOwner: @jabir52"
                send_message(chat_id, message_id, help, "y")
            elif "/start" == message:
                start = "Welcome!\nLet's get start... \n\nowener: @jabir52"
                send_message(chat_id, message_id, start, "y")
            else:
                pass
    except:
        pass

    if data["result"]:
        updated_id = data['result'][-1]["update_id"]+1
        return updated_id


def send_message(chat_id, message_id,  text, is_tag_user):
    data1 = {
        "chat_id": chat_id,
        "text": text,           # Without tagging
    }
    data2 = {
        "chat_id": chat_id,
        "text": text,
        "reply_to_message_id": message_id   # For tagging
    }
    if is_tag_user == "y":
        requests.get(api+"/sendMessage", data=data2)
    else:
        requests.get(api + "/sendMessage", data=data1)


def ss(chat_id, message_id, link):

    print(link)
    def capture():
        BASE = 'https://render-tron.appspot.com/screenshot/'
        url = link
        print(link)
        path = 'ss.jpg'
        response = requests.get(BASE + url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
    capture()

    data1 = {
        "chat_id": chat_id,
        "reply_to_message_id": message_id

    }
    files = {"photo": open("ss.jpg", "rb")}

    requests.post(api + "/sendPhoto", data=data1, files=files)

def find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    if len(url) != 0:
        return [x[0] for x in url], "y"

    else:
        return [x[0] for x in url], "n"

def make_url(url):

    try:

        for b in url:
            n = url
            try:
                c = b.replace("https://", "http://")
                n = b.replace("http://", "")
            except:
                pass
            c =  n
            print(c)
            r = requests.get(c)
            r = r.url
            print(r[0:5])
            if r[0:5] == "https":
                url = n.replace(n[0:8], "https://")
                print(url)
                return url
            elif r[0:5] != "https" and r[0:4] == "http":
                url = n.replace(n[0:9], "http://")
                print(url)
                return url
            else:
                return "errora"
                pass
    except:
        return "error"
        pass

offset = 0
while True:
    offset = read_message(offset)
    print("sent\n")
