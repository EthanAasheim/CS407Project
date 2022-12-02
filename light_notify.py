"""

Module that sets light color, fade duration, and brightness

"""


import sys
import os
import argparse

import time
import select

import colorsys
from lifxlan import LifxLAN
#from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW


white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 200, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
purple = (150, 0, 255)
pink = (255, 0, 255)
brightMax = 1
bright = brightMax

running = True


#============================== Light settings ================================

def rgb_to_hsbk(rgb, kelvin=3500):
    hsbk = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hue = int(65535 * hsbk[0])
    sat = int(65535 * hsbk[1])
    bright = int(65535 * hsbk[2] / 255)
    return [hue, sat , bright, kelvin]


def notify(rgb_color, kelvin, period, bright):
    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.

    color = rgb_to_hsbk(rgb_color, kelvin)
    color[2] = int(65535 * bright)
    rapid = True if period < 0.5 else False
    #print("bright: ", bright)
    #print("color: ", color)

    #print("Discovering lights...")
    lifx = LifxLAN(2)
    devices = lifx.get_lights()
    #print("\nFound {} light(s):\n".format(len(devices)))

    #print("setting light to: ", rgb_color)

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


#============================== Light settings ================================

def main():
    duration_secs = 1
    transition_time_ms = duration_secs * 1000

    #keyboard = Controller()
    color = white
    global running

    while (running == True):
        input = select.select([sys.stdin], [], [], 1)[0]
        if input:
            value = sys.stdin.readline().rstrip()

            if (value == 'w'):
                color = white
            if (value == 'r'):
                color = red
            if (value == 'o'):
                color = orange
            if (value == 'y'):
                color = yellow
            if (value == 'g'):
                color = green
            if (value == 'c'):
                color = cyan
            if (value == 'b'):
                color = blue
            if (value == 'p'):
                color = purple
            if (value == 'k'):
                color = pink
            if (value == "q"):
                running = False
                break

        global bright
        kelvin = 3500
        notify(color, kelvin, transition_time_ms, bright)
        time.sleep(0.1)
        if bright == brightMax:
            bright = 0.25
        else:
            bright = brightMax


if __name__=="__main__":
    main()
