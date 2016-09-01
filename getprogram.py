#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re

import sys

import youtube_dl

import subprocess

class CeskaTelevize():

    def __init__(self):
        self.urls = []
        self.titles = []
        self.ydl = youtube_dl.YoutubeDL()

    def get_program_title(self,link):
       m = re.search('>(.+?)<', link)
       if m:
           title = m.group(1)
       else:
           return ""

       return title


    def get_program_url(self,link):
       m = re.search('href=\"(.+?)\"', link)
       if m:
           url = m.group(1)
       else:
           return ""

       return url

    def get_link(self,tag):
        if len(tag) != 1:
            return ""
        link = str(tag[0])

        if "ivysilani" in link or "porady" in link:
            if "sledovat živě" not in link:
                title = self.get_program_title(link)
                url = self.get_program_url(link)
                if title != "" and url != "":
                    self.titles.append(title)
                    self.urls.append(url)
                return True
        return False

    def download_links(self):
        # Download program page
        response = urllib.request.urlopen("http://www.ceskatelevize.cz/tv-program/")
        data = response.read()
        page = data.decode('utf-8')

        html = BeautifulSoup(page,"lxml")

        for incident in html('li', {"class": "current"}):
            programmetitle = incident('a',{"class":"programmeTitle"})
            videolink = incident('a',{"class":"videoLink"})
            self.get_link(programmetitle)
            self.get_link(videolink)

        if len(self.titles) != len(self.urls):
            return False

        if len(self.titles) == 0:
            return False

        return True

    def select_program(self):
        i = 1

        print ("Vyberte si pořad:")

        for title in self.titles:

           print ("\t"+str(i)+". "+title)
           i += 1

        print ("Zadejte číslo pořadu:")
        userinput = sys.stdin.readline().rstrip('\n')

        try:
            number = int(userinput)
        except:
            print (userinput+" neni cislo, prosim, zvolte cislo.")
            return 0

        if number <= 0 or number > len(self.titles):
            print (str(number)+" neni v rozsahu moznych programu! Zvolte jine cislo")
            return 0

        return number

    def get_url_from_index(self,number):
        index = number - 1
        print("Zvolil jste "+str(number)+": "+self.titles[index])

        return "http://www.ceskatelevize.cz"+self.urls[index]

    def get_stream_url(self,url):
        print("getting stream for "+url)

        info_dict = self.ydl.extract_info(url, download=False)

        video_url = info_dict["entries"][0]["url"]

        print (video_url)

        return video_url

    def play(self,stream):
        self.play_mplayer(stream)
        pass

    def play_mplayer(self,stream):
        args = [ "mplayer", stream]
        subprocess.Popen(args)

    def play_vlc(self,stream):
        args = [ "vlc", stream]
        subprocess.Popen(args)

    def run(self):

        if not self.download_links():
            print ("Zadne porady se nepodarilo najit. Prosim, zkuste to znovu pozdeji.")
            return False

        program = 0
        while program == 0:
            program = self.select_program()

        url = self.get_url_from_index(program)

        stream = self.get_stream_url(url)

        self.play(stream)


ceskatelevize = CeskaTelevize()
ceskatelevize.run()
