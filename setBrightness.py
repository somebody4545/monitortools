# setBrightness.py

import os
import time
import requests
import asyncio
import dotenv
import screen_brightness_control as sbc
from screeninfo import get_monitors

dotenv.load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")

started = False
current_setting = "not set"
cached_sunrise = None
cached_sunset = None

async def start():
    global started, cached_sunrise, cached_sunset
    started = True

    location = "seattle"
    direction = "east"

    while started:
        if cached_sunrise is None or cached_sunset is None or time.time() > cached_sunset:
            # Fetch the sunrise and sunset times only once per day
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OWM_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            cached_sunrise = data["sys"]["sunrise"]
            cached_sunset = data["sys"]["sunset"]

        now = time.time()

        # Adjust brightness based on time of day
        if cached_sunrise < now < cached_sunset:
            midday = (cached_sunrise + cached_sunset) / 2
            if cached_sunrise < now < midday:
                if direction == "east":
                    brightDay()
                else:
                    dimDay()
            else:
                if direction == "west":
                    brightDay()
                else:
                    dimDay()
        else:
            if now > cached_sunrise - 3600 or now < cached_sunset + 3600:
                barelyNight()
            else:
                midNight()

        await asyncio.sleep(120)  # Non-blocking sleep for 2 minutes

def brightDay():
    global current_setting
    set_brightness_for_monitors(100, "bright day")

def dimDay():
    global current_setting
    set_brightness_for_monitors(50, "dim day")

def barelyNight():
    global current_setting
    set_brightness_for_monitors(35, "barely night")

def midNight():
    global current_setting
    set_brightness_for_monitors(25, "midnight")

def set_brightness_for_monitors(brightness, setting):
    global current_setting
    for monitor in get_monitors():
        sbc.set_brightness(brightness)
    current_setting = setting

async def stop():
    global started, current_setting
    started = False
    current_setting = "not set"

def get_monitors_friendly():
    return sbc.list_monitors()

def get_current_setting():
    return current_setting

def force_set(setting):
    asyncio.run(stop())
    sbc.set_brightness(setting)
