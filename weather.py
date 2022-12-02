# import modules
import requests, json
import light_notify

from lifxlan import LifxLAN
from light_notify import white, red, orange, yellow, cyan, blue
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


#The majority of the weather() function was found here:
#https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/

# Light settings
DEF_kelvin = 3500
DEF_period = 1
DEF_bright = 0.75
Max_bright = 0.75


def setfromrange(val, oldMin, oldMax, newMin, newMax):
    val = math.min(val, oldMax)
    val = math.max(val, oldMin)
    tmp = (val - oldMin) / oldMax
    result = int(newMin + tmp * (newMax - newMin))
    result = math.min(result, newMax)
    result = math.max(result, newMin)
    return result


def timeofday(time):
    str_parts = time.split()
    mil_time = str_parts[1].split(':')[0]

    if (time[-2:] == "PM"):
        mil_time += 12

    print("time:", mil_time)

    kelvin = DEF_kelvin
    period = DEF_period
    bright = DEF_bright
    light_notify.notify(red, kelvin, period, bright)


def cloudcover(cover):
    print("cover:", cover)
    kelvin = DEF_kelvin
    period = DEF_period
    bright = DEF_bright
    light_notify.notify(white, kelvin, period, bright)


def temperature(temp):
    print("temp:", temp)

    kelvin = setfromrange(temp, 0, 100, 2500, 9000)
    period = 2 - setfromrange(temp, 0, 100, 0, 1.75)
    bright = setfromrange(temp, 0, 100, 0.5*Max_bright, Max_bright)
    light_notify.notify(white, kelvin, period, bright)


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
