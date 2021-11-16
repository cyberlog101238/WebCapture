import requests
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

            if "/ss" in message:
                link = message.replace("/ss","")
                ss(chat_id, link)

            else:
                text, is_tag_user = bot_ai(message)
                send_message(chat_id, message_id, text, is_tag_user)
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


def ss(chat_id, link):

    def capture():
        BASE = 'https://render-tron.appspot.com/screenshot/'
        url = link
        path = 'ss.jpg'
        response = requests.get(BASE + url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
    capture()

    data1 = {
        "chat_id": chat_id,

    }
    files = {"photo": open("ss.jpg", "rb")}

    requests.post(api + "/sendPhoto", data=data1, files=files)

offset = 0
while True:
    offset = read_message(offset)
    print("sent\n")
