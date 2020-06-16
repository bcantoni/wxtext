#!/usr/bin/env python

import argparse
import json
import os
import requests
import urllib.parse
import compass


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def geocode(location, verbose=False):
    """From text location description, find lat/lon coordinates"""
    url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey={}&searchtext={}&countryfocus={}".format(
        os.environ['HERE_APP_CODE'],
        urllib.parse.quote(location),
        'USA'
    )

    req = requests.get(url)
    if verbose:
        print("GEOCODE: {}".format(req.content))
    dat = json.loads(strip_non_ascii(req.content))
    view = dat['Response']['View'][0]

    if verbose:
        print("Full found geolocation: {}".format(
            view['Result'][0]['Location']['Address']['Label']
        ))

    return (view['Result'][0]['Location']['Address']['Label'],
            view['Result'][0]['Location']['DisplayPosition']['Latitude'],
            view['Result'][0]['Location']['DisplayPosition']['Longitude']
            )


def weather_darksky(lat, lon, verbose=False):
    """From lat/lon coordinates, find current weather report"""
    url = "https://api.darksky.net/forecast/{}/{},{}?exclude=minutely,daily,alerts,hourly".format(
        os.environ['DARKSKY_SECRET'],
        lat,
        lon
    )
    req = requests.get(url)
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


def wxtext(location, verbose=False):
    """From text location description, find and summarize current weather report"""
    (addr, lat, lon) = geocode(location, verbose)
    wx = weather_darksky(lat, lon, verbose)
    return "{}: {}".format(addr, wx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test wxtext geo and weather API calls")
    parser.add_argument('--verbose', '-v', action="store_true", help="Verbose mode")
    args = parser.parse_args()

    tests = [
        'Soda Springs, CA',
        '94050',
        '95014',
        'Joshua Tree',
        'Dublin Ireland'
    ]
    for t in tests:
        print("{} returns: {}\n".format(t, wxtext(t, args.verbose)))
