"""

Module that sets light color, fade duration, and brightness

"""


import sys
import time
import colorsys

from pynput.keyboard import Key, Controller
from lifxlan import LifxLAN
#from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW


def rgb_to_hsbk(rgb):
    hsbk = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hue = int(65535 * hsbk[0])
    sat = int(65535 * hsbk[1])
    bright = int(65535 * hsbk[2] / 255)
    kelvin = 3500
    return [hue, sat , bright, kelvin]


def notify(rgb_color, period, bright):
    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.

    color = rgb_to_hsbk(rgb_color)
    color[2] = int(65535 * bright)
    rapid = True if period < 0.5 else False
    print("bright: ", bright)
    print("color: ", color)

    #print("Discovering lights...")
    lifx = LifxLAN(2)
    devices = lifx.get_lights()
    #print("\nFound {} light(s):\n".format(len(devices)))

    print("setting light to: ", rgb_color)

    # Set light color and brightness
    running = True
    for light in devices:
        try:
            #original_power = light.get_power()
            #original_color = light.get_color()
            #light.set_power("on")
            light.set_color(color, period, rapid)
        except:
            pass


def main():
    red = (255, 0, 0)
    orange = (255, 150, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    purple = (150, 0, 255)
    pink = (255, 0, 255)
    brightMax = 0.5
    bright = brightMax

    duration_secs = 0.5
    transition_time_ms = duration_secs * 1000

    #keyboard = Controller()
    running = True
    while running:
        user_input = input("")
        if user_input == 'r':
            color = red
        if user_input == 'o':
            color = orange
        if user_input == 'y':
            color = yellow
        if user_input == 'g':
            color = green
        if user_input == 'c':
            color = cyan
        if user_input == 'b':
            color = blue
        if user_input == 'p':
            color = purple
        if user_input == 'k':
            color = pink
        if user_input == 'q':
            running = False
            break

        notify(color, transition_time_ms, bright)
        time.sleep(2*duration_secs)
        if bright == brightMax:
            bright = 0
        else:
            bright = brightMax
        print("bright:", bright)


if __name__=="__main__":
    main()
