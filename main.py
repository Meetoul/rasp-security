#!/usr/bin/python3

from gpio_config import GpioConfig
GpioConfig.init()

from config import CAMERA_DEVICE, GSM_SERIAL, SMS_CENTER_NUMBER, SMS_NUMBERS

from gpio_subscription import GpioSubscription
from telegram import Telegram
from camera import Camera
from at_serial import AtSerial

from logger import LOGI, LOGE

subscribtion = GpioSubscription()
camera = Camera(CAMERA_DEVICE)
tg = Telegram()
at = AtSerial(GSM_SERIAL, SMS_CENTER_NUMBER)


def msg_handler(chat_id, message):
    if not message.startswith('/'):
        LOGE("Received message %s isn't a command" % message)
        return

    command = message[1:]

    if command == 'enable':
        subscribtion.set_enabled(True)
        LOGI('Security system enabled')
        tg.send(chat_id, 'enabled')
    elif command == 'disable':
        subscribtion.set_enabled(False)
        LOGI('Security system disabled')
        tg.send(chat_id, 'disabled')
    else:
        LOGE('Unrecognized command %s received' % command)

def telegram_listener(area):
    text = 'There is an intruder in %s' % area
    LOGI(text)
    image = camera.capture()
    tg.send_all_image(text, image)

def camera_listener(area):
    LOGI('Capturing video from area %s' % area)
    camera.start_stream()

def sms_listener(area):
    text = 'There is an intruder in %s' % area
    LOGI('SMS: ' + text)
    for number in SMS_NUMBERS:
        at.send_sms(number, text)

def main():
    tg.start(msg_handler)

    subscribtion.subscribe_all(telegram_listener)
    subscribtion.subscribe_all(camera_listener)
    subscribtion.subscribe_all(sms_listener)
    subscribtion.set_enabled(True)

    input('Press any key to exit...')

if __name__ == '__main__':
    main()
