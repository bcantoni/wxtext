#!/usr/bin/env python

import json
import os
import requests
import urllib
import compass


def geocode(location):
    """From text location description, find lat/lon coordinates"""
    url = "https://geocoder.api.here.com/6.2/geocode.json?app_id={}&app_code={}&searchtext={}&countryfocus={}".format(
        os.environ['HERE_APP_ID'],
        os.environ['HERE_APP_CODE'],
        urllib.quote(location),
        'USA'
    )

    req = requests.get(url)
    dat = json.loads(req.content)
    view = dat['Response']['View'][0]

    return (view['Result'][0]['Location']['Address']['Label'],
            view['Result'][0]['Location']['DisplayPosition']['Latitude'],
            view['Result'][0]['Location']['DisplayPosition']['Longitude'])


def weather(lat, lon):
    """From lat/lon coordinates, find current weather report"""
    url = "https://api.openweathermap.org/data/2.5/weather?APPID={}&lat={}&lon={}&units=imperial".format(
        os.environ['OPENWEATHER_APP_ID'],
        lat,
        lon
    )
    req = requests.get(url)
    dat = json.loads(req.content)
    txt = "{}: {}F, humidity {}%, wind {}mph from {}".format(
        dat['name'],
        int(round(dat['main']['temp'])),
        int(round(dat['main']['humidity'])),
        int(round(dat['wind']['speed'])),
        compass.degrees_direction(dat['wind']['deg'])
    )

    return txt


def wxtext(location):
    """From text location description, find and summarize current weather report"""
    (addr, lat, lon) = geocode(location)
    wx = weather(lat, lon)
    return wx


if __name__ == '__main__':
    tests = [
        'Soda Springs, CA',
        '95129',
        'Joshua Tree',
        'Dublin Ireland'
    ]
    for t in tests:
        print("{} returns: {}".format(t, wxtext(t)))
