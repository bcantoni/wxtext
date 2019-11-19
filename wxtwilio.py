#!/usr/bin/env python
"""
 Wrapper to receive the Twilio webhook and call wxtext.py to generate the response
"""
import cgi
import os
import requests
import wxtext


def logmsg(_msg):
    with open("logs/test.log", "a") as logfile:
        logfile.write("{}\n".format(_msg))


def send_slack_messages(slack_webhook_url, messages):
    for m in messages:
        req = requests.post(slack_webhook_url, json={'text': m})
        logmsg("Response from Slack webhook: {} {}".format(req.status_code, req.content))
    return


logmsg("---start---")

form = cgi.FieldStorage()
reqkeys = []
for key in form.keys():
    variable = str(key)
    value = str(form.getvalue(variable))
    msg = "{}: {}".format(variable, value)
    logmsg(msg)
    reqkeys.append(msg)

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

send_slack_messages(
    os.environ['SLACK_WEBHOOK'],
    ["\n".join(reqkeys), msg]
)
