from bs4 import BeautifulSoup
from requests import post
from requests import get
import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-c", help = "[+] AngelThump channel name")
parser.add_argument("-t", help = "[+] getting title for windowsmoviehouse channel", action='store_true')
args = parser.parse_args()

def getAT():
    endpoint = 'https://beta.watchw.me/'
    r = get(endpoint)
    return BeautifulSoup(r.text, 'html.parser')

ogTitle = getAT().body.find('div', attrs={'id':'original-title'}).text
ogStart = getAT().body.find('div', attrs={'id':'start'}).text
ogEnd = getAT().body.find('div', attrs={'id':'end'}).text
ogRuntime = getAT().body.find('div', attrs={'id':'runtime'}).text
ogOverview = (getAT().body.find('div', attrs={'id':'overview'}).text)

def getATTitleYear():
    s = getAT().body.find('div', attrs={'id':'title'}).text 
    return s[s.find('(')+1:s.find(')')]

def getToken(channel):
    print("[++] getting token")
    endpoint = 'https://vigor.angelthump.com/' + channel + '/token'
    jHeaders =  {"Content-Type": "application/json", "Identifier": "SwnpX0RnA99YdRj0SPqs"}
    r = post(endpoint, headers=jHeaders)
    return json.loads(r.text)["token"]

def getHLS(channel):
    endpoint = 'https://vigor.angelthump.com/hls/' + channel + '.m3u8?token=' + getToken(channel)
    return endpoint

def playVLC(channel):
    subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe",getHLS(channel), "--qt-minimal-view"])

def ayyLmao():
    print("[+] getting title for windowsmoviehouse channel")
    print("[++] -----------------------")
    print("[++] "+ ogTitle + " - " + getATTitleYear() + " (" + ogRuntime + ")")
    print("[++] Start: "+ ogStart)
    print("[++] End: "+ ogEnd)
    print("[++] Overview: "+ ogOverview)
    print("[++] -----------------------")

if args.c:
    print("[+] channel: % s" % args.c)
    if args.c == "windowsmoviehouse":
       ayyLmao()
    playVLC(args.c)
    print("[++] opening VLC")
elif args.t:
    ayyLmao()
else:
    print("[+] you need to input a channel name bozo '-c'")
    print("[++] ..........................................")
    print("[+] default channels then:")
    choice = input('[+]  (1) windowsmoviehouse / (2) kinokomplex \n[+] Put your input: ')
    if choice == "1":
        ayyLmao()
        playVLC("windowsmoviehouse")
        print("[++] opening VLC")
    elif choice == "2":
        playVLC("kinokomplex")
        print("[++] opening VLC")
    else:
        ayyLmao()
        playVLC("windowsmoviehouse")
        print("[++] opening VLC")