from requests import post
import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-c", help = "AngelThump channel name")
args = parser.parse_args()

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
    playVLC()
    print("[+] opening VLC")
