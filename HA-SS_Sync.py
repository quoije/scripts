from os import getenv
from requests import get
from requests import post
from json import loads
from json import load
from time import sleep

# https://github.com/slattery-mark/SteelSeries-CKL-App
# author: slattery-mark
# modified by quoije
# work with steelseries apex 3 keyboard, 10 zones
#
# change haAddress to your hass server, change haLight to your light entity
# change gsGame, gsEvent to desired steelseries engine name
# change sleepTime to desired time of sleep between post request to ss engine

haAddress = "192.168.0.42"
haLight = "light.sb50_l4"
haUrl = "http://" + haAddress + ":8123/api/states/" + haLight
haHeaders = {
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0ZmQ4MzQxNTZjNjg0YThlYTFjY2NiYmNkNWEzYTI4OSIsImlhdCI6MTY2NjExMDcwMiwiZXhwIjoxOTgxNDcwNzAyfQ.5KVla7Y72yKFrWhF01EupQpSHX0Rbr0CQ-LMLW6v6VU",
                "content-type": "application/json"
            }
gsCorePropsPath = getenv('PROGRAMDATA') + "\SteelSeries\SteelSeries Engine 3\coreProps.json" 
gsAddress = f'http://{load(open(gsCorePropsPath))["address"]}'
gsGame = "HA_LIGHT_SYNC"
gsEvent = "SYNC"
sleepTime = 1.00

def checkLight():
        """ Check HA light color """
        haResponse = get(haUrl, headers=haHeaders)
        haData = loads(haResponse.text)
        return haData['attributes']['rgb_color']

redRGB = 0
greenRGB = 0
blueRGB = 0

def updateLight():
    global redRGB
    global greenRGB
    global blueRGB
    redRGB = checkLight()[0]
    greenRGB = checkLight()[1]
    blueRGB = checkLight()[2]
    print("[+] RED: "+ str(redRGB))
    print("[+] GREEN: "+ str(greenRGB))
    print("[+] BLUE: "+ str(blueRGB))


def registerGame():
        """Registers this application to Engine."""
        print("[+] registerGame()")
        endpoint = f'{gsAddress}/game_metadata'
        payload = {
            "game" : gsGame,
            "game_display_name" : gsGame,
            "developer" : "quoije"
        }
        r = post(endpoint, json=payload)
        print(r.text) 

def removeGame():
        """Removes this application from Engine."""
        endpoint = f'{gsAddress}/remove_game'
        payload = {
            "game": gsGame
        }
        r = post(endpoint, json=payload)
        print(r.text) 

def removeGameEvent():
        """Removes a lighting event from Engine."""
        print("[+] removeGameEvent()")
        endpoint = f'{gsAddress}/remove_game_event'
        payload = {
            "game" : gsGame,
            "event" : gsEvent
        }
        r = post(endpoint, json=payload)
        print(r.text) 

def bindGameEvent():
        """Binds a lighting event to Engine."""
        print("[+] bindGameEvent()")
        endpoint = f'{gsAddress}/bind_game_event'
        payload = {
            "game": gsGame,
            "event": gsEvent,
            "handlers": [{
                        "mode": "context-color",
                        "device-type": "rgb-zoned-device",
                        "zone": "one",
                        "context-frame-key": "zone-color"
                        }]
                    }
        r = post(endpoint, json=payload)
        print(r.text)

def sendGameEvent(kill_switch):
        """Sends a lighting event/frame to Engine."""
        endpoint = f'{gsAddress}/game_event'
        payload = {
            "game": gsGame,
            "event": gsEvent,
            "data" : {
                "frame": {
                    "zone-color": {
                        "red": 0,"green": 0,"blue": 0
                    }
                }
            }
        }

        while kill_switch == 0:

                """ DEBUG """
                print("[+] loopyloop")
                """ DEBUG """       
                
                print("[+] update light RGB state")
                updateLight()
                payload['data']['frame']['zone-color'] = {"red": redRGB,"green": greenRGB,"blue": blueRGB}
                print("[+] sendGameEvent(kill_switch)")
                r = post(endpoint, json=payload)
                print(r.text)
                if kill_switch == 1: break

                """ DEBUG """
                print("[+] HA RGB: " + str(checkLight()[0]) + " " + str(checkLight()[1]) + " " + str(checkLight()[2]))
                """ DEBUG """

                sleep(sleepTime)

print("[+] removing game event")
removeGameEvent()
print("[+] removing game")
removeGame()
print("[+] register game")
registerGame()
print("[+] bind game")
bindGameEvent()
print("[+] send game")
sendGameEvent(0)