import telepot
from telepot.loop import MessageLoop

import storage

from config import TELEGRAM_BOT_TOKEN

CHAT_IDS_KEY = 'chat_ids'

class Telegram:

    def __init__(self, msg_handler):
        self.m_bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
        MessageLoop(self.m_bot, self.__msg_handler).run_as_thread()

        self.m_handler = msg_handler

        self.m_chat_ids = []

        self.__load_chat_ids()

    def __load_chat_ids(self):
        chat_ids = storage.load(CHAT_IDS_KEY)

        if chat_ids:
            self.m_chat_ids.extend(chat_ids)

    def __save_chat_id(self, chat_id):
        self.m_chat_ids.append(chat_id)
        storage.save(CHAT_IDS_KEY, self.m_chat_ids)

    def __msg_handler(self, content):
        chat_id = content['from']['id']

        if chat_id not in self.m_chat_ids:
            self.__save_chat_id(chat_id)

        self.m_handler(content['text'])

    def send_all(self, text):
        for chat_id in self.m_chat_ids:
            self.m_bot.sendMessage(chat_id, text)