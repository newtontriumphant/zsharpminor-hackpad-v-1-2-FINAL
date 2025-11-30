import board
# zsharpminor's HackPad v1.2, FINAL.

# THIS CODE IS PRELIMINARY!!!
# I have little experience with KMK, so 
# the code here is my best guess according
# to Google and the KMK wiki. Once board
# is assembled, I will experiment around with
# it until it works. All pinouts should
# be correct.

import time
import random
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB

keyboard = KMKKeyboard()

PINS = [board.GP7, board.GP27, board.GP29, board.GP28, board.GP6, board.GP1]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

encoder = EncoderHandler()
encoder.pins = ((board.GP26, board.GP3, board.GP2, False),)
encoder.map = [
    [KC.VOLD, KC.VOLU]
]
keyboard.modules.append(encoder)

keyboard.rgb_pixel_pin = board.GP4
keyboard.rgb_num_pixel = 1

rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixel)
keyboard.extensions.append(rgb)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def fade_color(start_color, end_color, duration=0.5, steps=20):
    for i in range(steps + 1):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / steps)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / steps)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / steps)
        rgb.pixels.fill((r, g, b))
        rgb.pixels.show()
        time.sleep(duration / steps)

old_process_key = keyboard.process_key

def new_process_key(key, pressed):
    if pressed and key in keyboard.matrix.keys:
        color = random_color()
        fade_color((0, 0, 0), color, 0.5)
        time.sleep(0.5)
        fade_color(color, (0, 0, 0), 0.5)
    return old_process_key(key, pressed)

keyboard.process_key = new_process_key

# PLACEHOLDER KEYS 1-6, WILL ADJUST ONCE BOARD IN HAND.

keyboard.keymap = [
    [KC.KP_1, KC.KP_2, KC.KP_3, KC.KP_4, KC.KP_5, KC.KP_6]
]

if __name__ == "__main__":
    keyboard.go()
