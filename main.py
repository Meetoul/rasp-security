#!/usr/bin/python3

from gpio_config import GpioConfig
GpioConfig.init()

from config import CAMERA_DEVICE

from gpio_subscription import GpioSubscription
from telegram import Telegram
from camera import Camera

from logger import LOGI

def msg_handler(message):
    print(message)

subscribtion = GpioSubscription()
camera = Camera(CAMERA_DEVICE)

tg = Telegram(msg_handler)

def telegram_listener(area):
    text = 'There is an intruder in %s' % area
    LOGI(text)
    image = camera.capture()
    tg.send_all_image(text, image)

def camera_listener(area):
    LOGI('Capturing video from area %s' % area)
    camera.start_stream()

def main():

    subscribtion.subscribe_all(telegram_listener)
    subscribtion.subscribe_all(camera_listener)

    input('Press any key to exit...')

if __name__ == '__main__':
    main()
