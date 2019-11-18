# wxtext

This is the code which powers my [Weather by Text](http://scooterlabs.com/wx/) service. The backend code is written in Python and uses the following services:

* **Twilio** for text/SMS messaging (requests and responses)
* **Here.com** for geocoding (converting from place names into lat/long coordinates)
* **OpenWeather** for providing weather forecast data from lat/long coordinates

Image credit: [Flickr](https://flickr.com/photos/18378305@N00/48068931826/)

## Setup

The code currently runs on Python 2.7. I'm running on a shared web host where I don't have sudo, so I'm not using any libraries beyond what's normally present in a 2.7 system.

You'll need to sign for free developer accounts on Here.com and OpenWeather, then set up these environment variables:

* HERE_APP_ID
* HERE_APP_CODE
* OPENWEATHER_APP_ID

On your webhost:

1. Copy or clone the Python files from this repo into a path reachable from your web server
2. Make the local `./logs` directory and make sure its writeable by the web server process (on my system I just set it to 777 writeable by everyone)
3. Test that everything is set up by running `python wxtext.py` - this will run a few locations through both the geocoding and weather APIs

Finally, in Twilio buy a number (or use one you already have) and configure it to do an HTTP POST to the `wxtwilio.py` file on your own web host for any incoming messages.

## To Do

* Improve the forecast response with more details like general conditions (sunny, cloudy, etc)
* Add support for HELP query
* Add better international support including units, look at using city/country code coming with Twilio request to see if those are useful
* Convert to Python 3.8 and add requests caching
* Improve error handling everywhere, especially if location is not found (make sure always respond to a request from user)
* Look at hosting on AWS Lambda w/API Gateway rather than requiring a separate web host
* Better handling for cases where >1 location may be found, give user a choice
