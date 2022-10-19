from logging import handlers
from requests import get
from requests import post
from json import loads
from time import sleep
from requests import Session, post

# https://github.com/slattery-mark/SteelSeries-CKL-App
# author: slattery-mark
# modified by quoije

haAddress = "192.168.0.42"
haLight = "light.sb50_l4"
haUrl = "http://" + haAddress + ":8123/api/states/" + haLight
haHeaders = {
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0ZmQ4MzQxNTZjNjg0YThlYTFjY2NiYmNkNWEzYTI4OSIsImlhdCI6MTY2NjExMDcwMiwiZXhwIjoxOTgxNDcwNzAyfQ.5KVla7Y72yKFrWhF01EupQpSHX0Rbr0CQ-LMLW6v6VU",
                "content-type": "application/json"
            }
gsAddress = "http://127.0.0.1:50786"
gsGame = "HA_LIGHT_SYNC"
gsEvent = "SYNC"
redRGB = 0
greenRGB = 0
blueRGB = 0

def checkLight():
        """ Check HA light color """
        haResponse = get(haUrl, headers=haHeaders)
        haData = loads(haResponse.text)
        return haData['attributes']['rgb_color']

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
                        "device-type": "keyboard",
                        "zone": "all",
                        "context-frame-key": "zone-all-color"
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
                    "zone-all-color": {
                        "color": {"red": redRGB,"green": greenRGB,"blue": blueRGB}
                    }
                }
            }
        }

        with Session() as s:
            while kill_switch == 0:

                """ DEBUG """
                print("[+] loopyloop")
                """ DEBUG """       
                print("[+] sendGameEvent(kill_switch)")
                print("[+] update light RGB state")
                updateLight()
                r = s.post(endpoint, json=payload)
                print(r.text)

                if kill_switch == 1: break

                """ DEBUG """
                print("[+] HA RGB: " + str(checkLight()[0]) + " " + str(checkLight()[1]) + " " + str(checkLight()[2]))
                """ DEBUG """

                sleep(1.01)

print("[+] removing game event for debug")
removeGameEvent()
print("[+] removing game for debug")
removeGame()
print("[+] register game for debug")
registerGame()
print("[+] bind game for debug")
bindGameEvent()
print("[+] send game for debug")
sendGameEvent(0)