# Commands
help = "/ss <url> to take sceenshot..\n(example: /ss https://www.google.com)"
start = "Welcome!\nLet's get start... \n\nowener: @jabir52"

def bot_ai(message):
    message = message.lower()
    is_tag_user = "y"
    if "/help" in message:
        is_tag_user = "n"
        text = help
        return help, is_tag_user
    elif "/start" in message:
        is_tag_user = "n"
        text = start
        return text, is_tag_user
    return "Invalid commads...\n\n/help for any help", is_tag_user