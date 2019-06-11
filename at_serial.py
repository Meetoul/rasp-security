import time
import serial
import RPi.GPIO as GPIO

class AtSerial:
    def __init__(self, dev, serv):
        self.port = serial.Serial(dev, baudrate=115200, timeout=1)
        self.sms_text_mode = False
        self.serv = serv

    # Check if module is ready to receive AT commands
    def at_ready(self):
        self.write_serial('AT')
        self.read_serial()
        return rcv

    # Check if simcard is ready to operate
    def sim_ready(self):
        self.write_serial('AT+CPIN?')
        rcv = self.read_serial()
        return rcv

    # Enalbe SMS text mode
    def set_sms_mode_text(self):
        self.write_serial('AT+CMGF=1')
        rcv = self.read_serial()
        self.sms_text_mode = True
        return rcv

    # Send SMS to a specific number through specific SMS-server
    def send_sms(self, num, text):
        if not self.sms_text_mode:
            self.set_sms_mode_text()

        self.write_serial('AT+CSCA="{}"'.format(self.serv))
        rcv = self.read_serial()
        self.write_serial('AT+CMGS="{}"'.format(num))
        rcv = self.read_serial()
        self.write_serial(text)
        rcv = self.read_serial()
        self.port.write('\x1A'.encode())
        rcv = self.read_serial()

    # Call to a specific number
    def call(self, num):
        self.write_serial('ATD{};'.format(num))
        rcv = self.read_serial()
        return rcv

    # Write string to serial port
    def write_serial(self, msg):
        self.port.write((msg + '\r\n').encode())

    # Read string from serial port
    def read_serial(self):
        return self.port.read(100).decode().strip()
