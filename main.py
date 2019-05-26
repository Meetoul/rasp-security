#!/usr/bin/python3

from gpio_config import GpioConfig
GpioConfig.init()

from gpio_subscription import GpioSubscription
from telegram import Telegram

def msg_handler(message):
    print(message)

subscribtion = GpioSubscription()
tg = Telegram(msg_handler)

def telegram_listener(area):
    text = 'There is an intruder in %s' % area
    print(text)
    tg.send_all(text)

def main():

    subscribtion.subscribe_all(telegram_listener)

    input('Press any key to exit...')

if __name__ == '__main__':
    main()
