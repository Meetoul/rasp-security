from gpio_config import GpioConfig

from config import DETECTION_TIMEOUT

import RPi.GPIO as GPIO
from timeit import default_timer as timer

BOUNCETIME = 200 # ms

class TimeoutedCallback:

    def __init__(self, callback):
        self.m_callback = callback
        self.m_last_timepoint = 0

    def __call__(self, *args, **kwargs):
        current_timepoint = timer()
        time_passed = current_timepoint - self.m_last_timepoint

        if time_passed > DETECTION_TIMEOUT:
            self.m_last_timepoint = current_timepoint
            self.m_callback(*args, **kwargs)

    def __eq__(self, other):
        return self.m_callback.__eq__(other)

class GpioSubscription:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.m_listeners = {}
        self.m_detection_timepoints = {}

        for gpio_num in GpioConfig.get_gpios():
            GPIO.setup(gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(gpio_num, GPIO.RISING, bouncetime=BOUNCETIME)
            GPIO.add_event_callback(gpio_num, self)

            self.m_listeners[gpio_num] = []
            self.m_detection_timepoints[gpio_num] = timer()


    def subscribe(self, gpio, listener):
        self.m_listeners[gpio].append(TimeoutedCallback(listener))

    def subscribe_all(self, listener):
        for listeners in self.m_listeners.values():
            listeners.append(TimeoutedCallback(listener))

    def unsubscribe(self, listener):
        for listeners in self.m_listeners.values():
            if listener in listeners:
                listeners.remove(listener)

    def __call__(self, param):
        listeners = self.m_listeners[param]
        area = GpioConfig.gpio_to_area(param)

        for listener in listeners:
            listener(area)
