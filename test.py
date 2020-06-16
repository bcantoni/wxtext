#!/usr/bin/env python

import json
import os
import requests
import time
import urllib.parse
import compass


def geocode(location):
    url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey={}&searchtext={}&countryfocus={}".format(
        os.environ['HERE_APP_CODE'],
        urllib.parse.quote(location),
        'USA'
    )

    req = requests.get(url)
    assert req.status_code == 200, "Error calling geocoder service"
    dat = json.loads(req.content)
    view = dat['Response']['View'][0]
    print("geocode returned {} results".format(len(view['Result'])))

    return (view['Result'][0]['Location']['Address']['Label'],
            view['Result'][0]['Location']['DisplayPosition']['Latitude'],
            view['Result'][0]['Location']['DisplayPosition']['Longitude'])


def weather_open(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?APPID={}&lat={}&lon={}&units=imperial".format(
        os.environ['OPENWEATHER_APP_ID'],
        lat,
        lon
    )
    req = requests.get(url)
    assert req.status_code == 200, "Error calling weather service"
    dat = json.loads(req.content)
    txt = "{}: {} F, humidity {}%, wind {} from {}".format(
        dat['name'],
        dat['main']['temp'],
        dat['main']['humidity'],
        dat['wind']['speed'],
        compass.degrees_direction(dat['wind']['deg'])
    )

    return txt


def weather_darksky(lat, lon, verbose=False):
    """From lat/lon coordinates, find current weather report"""
    url = "https://api.darksky.net/forecast/{}/{},{}?exclude=minutely,daily,alerts,hourly".format(
        os.environ['DARKSKY_SECRET'],
        lat,
        lon
    )
    req = requests.get(url)
    assert req.status_code == 200, "Error calling weather service"
    if verbose:
        print("WEATHER: {}".format(req.content))
    dat = json.loads(req.content)

    summary = dat['currently']['summary']
    temp = int(round(dat['currently']['temperature']))
    humidity = dat['currently']['humidity'] * 100
    wind = int(round(dat['currently']['windSpeed']))
    direction = compass.degrees_direction(dat['currently']['windBearing'])

    txt = "{}F, {}, humidity {}%, wind {}mph from {}".format(
        temp,
        summary,
        humidity,
        wind,
        direction
    )

    return txt


places = [
    '95014',
    '425 W Randolph Chicago',
    'Soda Springs CA',
]

for p in places:
    time.sleep(1)
    (addr, lat, lon) = geocode(p)
    print("{} is at {} / {}".format(addr, lat, lon))
    wx = weather_darksky(lat, lon)
    print("Forecast: {}".format(wx))
