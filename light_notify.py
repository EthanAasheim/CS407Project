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
DEFAULT_BRIGHT = 0.75

devices = None


#============================== Light settings ================================

def rgb_to_hsbk(rgb, kelvin=3500):
    hsbk = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hue = int(65535 * hsbk[0])
    sat = int(65535 * hsbk[1])
    bright = int(65535 * hsbk[2] / 255)
    return [hue, sat , bright, kelvin]


def setLight(rgb_color, period, bright, kelvin=3500, hue=None):
    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.

    color = rgb_to_hsbk(rgb_color, kelvin)
    color[2] = int(65535 * bright)
    if hue != None:
            color[0] = hue
    rapid = True if period < 0.5 else False

    # Set light color and brightness
    for light in devices:
        try:
            #original_power = light.get_power()
            #original_color = light.get_color()
            light.set_power("on")
            light.set_color(color, period, rapid)
        except:
            pass


#============================== Light settings ================================

def notify(color=white, duration_secs=2, brightMax=DEFAULT_BRIGHT, kelvin=3500, hue=None, end=-1):

    # Get lights
    lifx = LifxLAN(2)
    global devices
    devices = lifx.get_lights()

    # Convert to milliseconds
    transition_time_ms = duration_secs * 1000

    # Get brightness for fading
    if brightMax == None:
        brightMax = DEFAULT_BRIGHT
    bright = brightMax

    running = True
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

        setLight(color, transition_time_ms, bright, kelvin, hue)
        time.sleep(0.1)
        if bright == brightMax:
            bright = 0.5*brightMax
        else:
            bright = brightMax

        if end > 0:
            end -= 1
        if end == 0:
            running = False
            break

    if end < 0:
        for light in devices:
            try:
                light.set_power("off")
            except:
                pass



def main():
    notify(white)


if __name__=="__main__":
    main()
