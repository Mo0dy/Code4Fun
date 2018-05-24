import sys
import serial
import time
# import os
from pynput.keyboard import Key, Controller
from time import sleep

# os.environ["SDL_VIDEODRIVER"] = "dummy"

keyboard = Controller()

refresh_rate = 20
baudrate = 115200
ports = [5, 6, 4, 3]

sers = [serial.Serial('COM' + str(p), baudrate, timeout=1 / refresh_rate) for p in ports]


def my_quit():
    global loop
    loop = False


def write_number(n):
    keyboard.type(n)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


loop = True
while loop:

    inputs = [str(s.readline().decode().strip()) for s in sers]
    # print_str = str(ser.readline().decode().strip())

    # if print_str:
    #     write_number(print_str)

    for i in inputs:
        if i:
            write_number(i)

for s in sers:
    s.close()
