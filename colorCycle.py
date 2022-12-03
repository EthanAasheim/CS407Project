# import modules
import time
import random
import requests, json
import light_notify

from lifxlan import LifxLAN
from light_notify import white, red, orange, yellow, green, cyan, blue, purple, pink


def main():
    colors = [white, red, orange, yellow, green, cyan, blue, purple, pink]
    while True:
        i = int(random.randrange(len(colors)))
        light_notify.notify(colors[i], end=3)
        time.sleep(0.1)

if __name__=="__main__":
    main()
