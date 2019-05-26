#!/usr/bin/python3

from gpio_config import GpioConfig
GpioConfig.init()

from gpio_subscription import GpioSubscription
from telegram import Telegram
from camera import Camera

def msg_handler(message):
    print(message)

subscribtion = GpioSubscription()
camera = Camera()

tg = Telegram(msg_handler)

def telegram_listener(area):
    text = 'There is an intruder in %s' % area
    print(text)
    image = camera.capture()
    tg.send_all_image(text, image)

def main():

    subscribtion.subscribe_all(telegram_listener)

    input('Press any key to exit...')

if __name__ == '__main__':
    main()
