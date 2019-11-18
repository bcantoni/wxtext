#!/usr/bin/env python
"""
 Wrapper to receive the Twilio webhook and call wxtext.py to generate the response
"""
import cgi
import wxtext


def logmsg(_msg):
    with open("logs/test.log", "a") as logfile:
        logfile.write("{}\n".format(_msg))


logmsg("---start---")

form = cgi.FieldStorage()
for key in form.keys():
    variable = str(key)
    value = str(form.getvalue(variable))
    logmsg("%s: %s" % (variable, value))

location = form.getvalue("Body")
if location.upper() == 'HELP':
    msg = "Welcome to Scooterlabs Weather by Text - to receive the current weather, reply with your city, state or zip/postal code. Powered by DarkSky https://darksky.net/poweredby/"
else:
    msg = wxtext.wxtext(location)

templ = """Content-Type: text/xml;charset=utf-8
Cache-Control: max-age=300, public

<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{}</Message>
</Response>
"""
resp = templ.format(msg)
logmsg(resp)
logmsg("---end---\n")

print(resp)
