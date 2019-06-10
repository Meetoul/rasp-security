import telepot
from telepot.loop import MessageLoop

import storage

from config import TELEGRAM_BOT_TOKEN

CHAT_IDS_KEY = 'chat_ids'

class Telegram:

    def __init__(self):
        self.m_chat_ids = []
        self.__load_chat_ids()

    def start(self, msg_handler):
        self.m_handler = msg_handler
        self.m_bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
        MessageLoop(self.m_bot, self.__msg_handler).run_as_thread()

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

        self.m_handler(chat_id, content['text'])

    def send(self, chat_id, text):
        self.m_bot.sendMessage(chat_id, text)

    def send_all(self, text):
        for chat_id in self.m_chat_ids:
            self.send(chat_id, text)

    def send_image(self, chat_id, text, image):
        with open(image, 'rb') as raw_image:
            self.m_bot.sendMessage(chat_id, text)
            self.m_bot.sendPhoto(chat_id, raw_image)

    def send_all_image(self, text, image):
            for chat_id in self.m_chat_ids:
                self.send_image(chat_id, text, image)
