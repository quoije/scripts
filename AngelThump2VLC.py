from bs4 import BeautifulSoup
from requests import post
from requests import get
import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-c", help = "AngelThump channel name")
args = parser.parse_args()

def getAT():
    endpoint = 'https://beta.watchw.me/'
    r = get(endpoint)
    return BeautifulSoup(r.text, 'html.parser')

ogTitle = getAT().body.find('div', attrs={'id':'original-title'}).text
ogStart = getAT().body.find('div', attrs={'id':'start'}).text
ogEnd = getAT().body.find('div', attrs={'id':'end'}).text
ogRuntime = getAT().body.find('div', attrs={'id':'runtime'}).text

def getATTitleYear():
    s = getAT().body.find('div', attrs={'id':'title'}).text 
    return s[s.find('(')+1:s.find(')')]

def getToken():
    print("[+] getting token")
    endpoint = 'https://vigor.angelthump.com/' + args.c + '/token'
    jHeaders =  {"Content-Type": "application/json", "Identifier": "SwnpX0RnA99YdRj0SPqs"}
    r = post(endpoint, headers=jHeaders)
    return json.loads(r.text)["token"]

def getHLS():
    endpoint = 'https://vigor.angelthump.com/hls/' + args.c + '.m3u8?token=' + getToken()
    return endpoint

def playVLC():
    subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe",getHLS()])

if args.c:
    print("[+] channel: % s" % args.c)
    if args.c == "windowsmoviehouse":
        print("[+] getting title")
        print("[+] "+ ogTitle + " - " + getATTitleYear() + " (" + ogRuntime + ")")
        print("[+] Start: "+ ogStart)
        print("[+] End: "+ ogEnd)
    playVLC()
    print("[+] opening VLC")
else:
    print("[+] you need to input a channel name bozo '-c'")
