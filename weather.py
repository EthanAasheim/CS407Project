# import modules
import requests, json
import light_notify

from lifxlan import LifxLAN
from light_notify import white, red, orange, yellow, cyan, blue
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


# Default light settings
DEFAULT_KELVIN = 3500
DEFAULT_PERIOD = 2
DEFAULT_BRIGHT = 0.75
MAX_BRIGHT = 0.75


def setfromrange(val, oldMin, oldMax, newMin, newMax):
    val = min(val, oldMax)
    val = max(val, oldMin)
    tmp = (val - oldMin) / (oldMax - oldMin)
    result = int(newMin + tmp * (newMax - newMin))
    result = min(result, newMax)
    result = max(result, newMin)
    return result


def timeofday(time):
    str_parts = time.split()
    mil_time = int(str_parts[1].split(':')[0])

    # Need military time
    if (time[-2:] == "PM"):
        mil_time += 12

    print("time:", mil_time)

    # Default colors
    color = yellow
    hue = 58275

    # Midnight to 6 AM -> blue to cyan
    if mil_time < 6:
        hue = 43634 - setfromrange(mil_time, 0, 6, 0, 43634 - 29814)
    # 6 AM to 9 AM -> cyan to yellow
    elif mil_time < 9:
        hue = 29814 - setfromrange(mil_time, 6, 9, 0, 29814 - 9000)
    # 9 AM to Noon -> yellow to white
    elif mil_time < 12:
        color = (color[0], color[1], setfromrange(mil_time, 9, 12, 0, 255))
        hue = None
    # Noon to 3 PM -> white to orange
    elif mil_time < 15:
        color = (color[0], color[1], setfromrange(mil_time, 9, 12, 0, 255))
        hue = None
    # 3 PM to 6 PM -> orange to red
    elif mil_time < 18:
        hue = 6500 - setfromrange(mil_time, 15, 18, 0, 6500)
    # 6 PM to Midnight -> red to blue
    else:
        hue = 65535 - setfromrange(mil_time, 18, 24, 0, 65535 - 43634)

    # Faster and brighter the closer to noon
    kelvin = DEFAULT_KELVIN
    if mil_time < 12:
        bright = setfromrange(mil_time, 0, 12, 0.25*MAX_BRIGHT, MAX_BRIGHT)
        period = 2*DEFAULT_PERIOD - setfromrange(mil_time, 0, 12, 0, (2 - 0.5)*DEFAULT_PERIOD)
    else:
        bright = MAX_BRIGHT - setfromrange(mil_time, 12, 24, 0, 0.75*MAX_BRIGHT)
        period = setfromrange(mil_time, 12, 24, 0.5*DEFAULT_PERIOD, DEFAULT_PERIOD)
    light_notify.notify(color, period, bright, kelvin, hue)


def cloudcover(cover):
    print("cover:", cover)

    color = yellow
    if cover == "Clear" or "Sunny":
        color = yellow
    if cover == "Mostly Clear" or "Mostly Sunny":
        color = (255, 255, 128)
    if cover == "Partly Cloudy" or "Partly Sunny":
        color = white
    if cover == "Mostly Cloudy":
        color = cyan
    if cover == "Cloudy":
        color = blue

    kelvin = DEFAULT_KELVIN
    period = DEFAULT_PERIOD
    bright = DEFAULT_BRIGHT
    light_notify.notify(color, period, bright, kelvin)


def temperature(temp):
    temp = int(temp)

    # Use a range of 0°C to 60°C to determine warmth of white color
    # Warmer and faster the closer to noon
    kelvin = 9000 - setfromrange(temp, 0, 60, 0, 9000 - 2500)
    period = 2*DEFAULT_PERIOD - setfromrange(temp, 0, 60, 0, (2 - 0.5)*DEFAULT_PERIOD)
    bright = setfromrange(temp, 0, 60, 0.5*MAX_BRIGHT, MAX_BRIGHT)
    print("temp:", temp)
    print("kelvin:", kelvin)
    light_notify.notify(white, period, bright, kelvin)


def weather(city, factor):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location)
    print(time)
    print(info)
    print(weather+"°C")

    # Send result to control light
    if (factor == "time" or factor == "t"):
        timeofday(time)
    if (factor == "cover" or factor == "c"):
        cloudcover(info)
    if (factor == "temp" or factor == "k"):
        temperature(weather)


def main():
    city = input("Enter city name: ")
    city = city+" weather"

    factor = input("Enter factor (time, cover, temp): ")
    weather(city, factor)


if __name__=="__main__":
    main()
