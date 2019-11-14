#!/usr/bin/env python

import json
import requests
import time
import urllib
import compass


def geocode(location):
    url = "https://geocoder.api.here.com/6.2/geocode.json?app_id={}&app_code={}&searchtext={}&countryfocus={}".format(
        '3aOY6Lk040Jq7MYdHBRj',
        'a1p7--0yzjDzUVZlxo1g-w',
        urllib.quote(location),
        'USA'
    )

    req = requests.get(url)
    dat = json.loads(req.content)
    view = dat['Response']['View'][0]
    print("geocode returned {} results".format(len(view['Result'])))

    return (view['Result'][0]['Location']['Address']['Label'],
            view['Result'][0]['Location']['DisplayPosition']['Latitude'],
            view['Result'][0]['Location']['DisplayPosition']['Longitude'])


def weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?APPID={}&lat={}&lon={}&units=imperial".format(
        '2d4bf9e3c4df12236bcc3516175eabdc',
        lat,
        lon
    )
    req = requests.get(url)
    dat = json.loads(req.content)
    txt = "{}: {} F, humidity {}%, wind {} from {}".format(
        dat['name'],
        dat['main']['temp'],
        dat['main']['humidity'],
        dat['wind']['speed'],
        compass.wind_direction(dat['wind']['deg'])
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
    wx = weather(lat, lon)
    print("Forecast: {}".format(wx))
