from Botio import *
from config import cookie


def message(cookie):
    bot = Botio(cookie)
    chats = bot.get_chats()
    message = bot.send_message("Hi!", chats[0]['uuid'])
    print(message)


def create_achat(cookie):
    bot = Botio(cookie)
    chat = bot.create_chats()
    print(chat)

def chats(cookie):
    bot = Botio(cookie)
    conversations = bot.get_chats()
    for conv in conversations:
        print(conv)

