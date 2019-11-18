#!/usr/bin/env python
"""
 Wrapper to receive the Twilio webhook and call wxtext.py to generate the response
"""
import cgi
import cgitb
import wxtext


def logmsg(_msg):
    with open("logs/test.log", "a") as logfile:
        logfile.write("{}\n".format(_msg))


cgitb.enable(display=0, logdir="logs/")
logmsg("---start---")

form = cgi.FieldStorage()
for key in form.keys():
    variable = str(key)
    value = str(form.getvalue(variable))
    logmsg("%s: %s" % (variable, value))

location = form.getvalue("Body")
wx = wxtext.wxtext(location)

logmsg("reply: {}".format(wx))

templ = """Content-Type: text/xml;charset=utf-8

<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{}</Message>
</Response>
"""
resp = templ.format(wx)
logmsg(resp)
logmsg("---end---\n")

print(resp)
