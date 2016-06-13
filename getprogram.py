#!/bin/env python

import urllib2
from bs4 import BeautifulSoup

page = urllib2.urlopen("http://www.ceskatelevize.cz/tv-program/")
soup = BeautifulSoup(page)

for incident in soup('li', {"class": "current"}):
    #print incident
    #item = BeautifulSoup(incident)
    print incident('a',{"class":"programmeTitle"})
    print "---"
    print incident('a',{"class":"videoLink"})
    print "--------"
    #    where, linebreak, what = incident.contents[:3]
    #        print where.strip()
    #            print what.strip()
    #                print
