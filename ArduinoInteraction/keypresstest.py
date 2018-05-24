from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

while True:
    keyboard.press('a')
    keyboard.release('a')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(1)