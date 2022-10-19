from xml.sax import handler
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
    "content-type": "application/json",
}
haResponse = get(haUrl, headers=haHeaders)
haData = loads(haResponse.text)
haLightColor = haData['attributes']['rgb_color']
gsAddress = "http://127.0.0.1:50786"
gsGame = "HA_LIGHT_SYNC"
gsEvent = "SYNC"

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

def removeGameEvent():
        """Removes a lighting event from Engine."""
        print("[+] removeGameEvent()")
        endpoint = f'{gsAddress}/remove_game_event'
        payload = {
            "game" : gsGame,
            "event" : gsEvent
        }
        post(endpoint, json=payload)

def bindGameEvent():
        """Binds a lighting event to Engine."""
        print("[+] bindGameEvent()")
        endpoint = f'{gsAddress}/register_game_event'
        payload = {
            "game" : gsGame,
            "event": gsEvent,
            "handlers" : 
                {
                "device-type": "rgb-zoned-device",
                "zone": "two",
                "color": {"red": 0, "green": 255, "blue": 0},
                "mode": "color"
            }
        }
        post(endpoint, json=payload)    

def sendGameEvent(event, kill_switch):
        """Sends a lighting event/frame to Engine."""
        print("[+] sendGameEvent(kill_switch)")

        if event == "init":
            print("ayyy")
        elif event == gsEvent:
            endpoint = f'{gsAddress}/game_event'
            payload = {
                "game": gsGame,
                "event": gsEvent,
                "data": {
                    "value" : 50
                }
            }
            with Session() as s:
                while kill_switch == 0:
                    print("[+] loopyloop")                
                    s.post(endpoint, json=payload)
                    if kill_switch == 1: break
                    sleep(0.01)


bindGameEvent()
sendGameEvent(gsEvent, 0)
