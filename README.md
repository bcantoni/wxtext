# wxtext

This is the code which powers my [Weather by Text](http://scooterlabs.com/wx/) service. The backend code is written in Python and uses the following services:

* **Twilio** for text/SMS messaging (requests and responses)
* **Here.com** for geocoding (converting from place names into lat/long coordinates)
* **OpenCageData** for providing weather forecast data from lat/long coordinates

## Setup

The code currently runs on Python 2.7 and up.

You'll need to sign for free developer accounts on Here.com and OpenCageData, then set up these environment variables:

* HERE_APP_ID
* HERE_APP_CODE
* OPENWEATHER_APP_ID

On your webhost:

1. Copy or clone the Python files from this repo into a path reachable from your web server
2. Make the local `./logs` directory and make sure its writeable by the web server process (on my system I just set it to 777 writeable by everyone)
3. Test that everything is set up by running `python wxtext.py`

Finally, in Twilio buy a number (or use one you already have) and configure it to do an HTTP POST to the `wxtwilio.py` file on your own web host.

## To Do

* Improve the forecast response with more details like general conditions (sunny, cloudy, etc)
* Add support for HELP query
* Add better international support including units, look at using city/country code coming with Twilio request to see if those are useful
* Convert to Python 3.8 and add requests caching
* Improve error handling everywhere, especially if location is not found (make sure always respond to a request from user)
* Look at hosting on AWS Lambda w/API Gateway rather than requiring a separate web host
