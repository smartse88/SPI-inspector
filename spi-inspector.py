#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 23:01:37 2018

@author: simon
"""

from spifetch import fetchspi
import cgi

#answer = fetchspi('https://en.wikipedia.org/wiki/Wikipedia:Sockpuppet_investigations/Anatha_Gulati')

def printFooter():
    print ("""<hr>
    <small>Made by <a href="http://en.wikipedia.org/wiki/User:Smartse">Smartse</a> with front-end copied from <a href="http://en.wikipedia.org/wiki/User:Apoc2400">Apoc2400</a> . Send feedback to smartsewiki (at) gmail.com or <a href="http://en.wikipedia.org/wiki/User_talk:Smartse">my talk page</a>.</small>
    """)
    print ("</body></html>")

def error(message):
    print ('<span id="citespan"><hr><font color="red">', cgi.escape(message, 1), "</font></span>")
    printFooter()
    exit()

def main():
    print ('Content-Type: text/html; charset=utf-8')
    print ('')
    print ("""<!DOCTYPE html><html><head>
             <title>Wikipedia sockpuppet investigator</title>
        <link rel="shortcut icon" href="/favicon.ico" />
        </head><body style="font-family: sans-serif; font-size:0.79375em">
        <h1><a href="/doiweb.py" style="text-decoration: none; color: black">Generates lists of users and created articles from an sockpuppet investigation</a></h1>
        """)

    form = cgi.FieldStorage()
    spi = ''
    if form.has_key("spi"):
        spi = form["spi"].value

    print ("""<hr><form action="" method="get">
        <label for="spi">SPI:</label>
        <input type="text" size="80" name="spi" id="spi" tabindex=1 value="%s">
        <input type="submit" value="Load" tabindex=1>
        </form>""" % (cgi.escape(spi, 1)))

    if not form.has_key("spi"):
        print ("""Example DOI (copy and paste above): 10.1111/j.1600-0404.1986.tb04634.x
        <p>Try also: <a href="/">Wikipedia citation tool for Google Books</a> or <a href="/nytweb.py">The New York Times</a></p>""")
        printFooter()
        return

    print(fetchspi(spi))
        
    print ("""<hr><font color="DarkOliveGreen">Below is the complete reference tag. Copy and paste it into the Wikipedia article.</font><br />
    <textarea rows="5" cols="100" style="width: 99%" id="fullcite" tabindex=1>""")

    print ('</textarea>')

    printFooter()



if __name__ == "__main__":
    main()