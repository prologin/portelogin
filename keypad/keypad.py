#! /usr/bin/python2

import Adafruit_BBIO.GPIO as GPIO
import requests

class Keypad:
    def __init__(self):
        pins = ["P8_7",
                "P8_8",
                "P8_14",
                "P8_13",
                "P8_11",
                "P8_12",
                "P8_9",
                "P8_10"]

        self.rows = [pins[0], pins[1], pins[7], pins[6]]
        self.columns = [pins[2], pins[3], pins[4], pins[5]]
        self.led_in = "P9_11"
        self.led_ok = "P9_12"
        GPIO.setup(self.led_in, GPIO.OUT)
        GPIO.setup(self.led_ok, GPIO.OUT)

        self.keys = [['1', '2', '3', 'A'],
                     ['4', '5', '6', 'B'],
                     ['7', '8', '9', 'C'],
                     ['*', '0', '#', '.']]
        self.init_gpio()

    def find_key(self, l, val):
        try:
            return l.index(next((x for x in l if GPIO.input(x) == val), ""))
        except ValueError:
            return None

    def init_gpio(self):
        for i in self.rows:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

        for i in self.columns:
            GPIO.setup(i, GPIO.IN)



    def get_key(self):
        c = self.find_key(self.columns, 1)
        if c == None:
            return None

        for i in self.rows:
            GPIO.setup(i, GPIO.IN)

        for i in self.columns:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

        r = self.find_key(self.rows, 0)

        self.init_gpio()
        if r == None:
            return None
        else:
            return self.keys[r][c]

    def poll_key(self):
        k = None
        while k == None:
            k = self.get_key()
        GPIO.output(self.led_in, GPIO.HIGH)
        r = k
        while k != None:
            k = self.get_key()
        GPIO.output(self.led_in, GPIO.LOW)
        return r


if __name__ == '__main__':
    kp = Keypad()
    login = ""
    passwd = ""
    while True:
        k = kp.poll_key()
        if k == '#':
            payload = {"login" : login, "passwd" : passwd}
            GPIO.output(kp.led_ok, GPIO.HIGH)
            requests.get("http://192.168.1.100/check/%s/%s" % (login,
                passwd))
            #requests.get("http://192.168.103.156:8000/check/%s/%s" % (login,
            #    passwd))
            GPIO.output(kp.led_ok, GPIO.LOW)
            login, passwd = passwd, ""
        else:
            passwd += k
