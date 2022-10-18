from requests import get
from requests import post
import json
# Reference
# https://github.com/slattery-mark/SteelSeries-CKL-App

haAddress = "192.168.0.42"
haLight = "light.sb50_l4"
haUrl = "http://" + haAddress + ":8123/api/states/" + haLight
haHeaders = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0ZmQ4MzQxNTZjNjg0YThlYTFjY2NiYmNkNWEzYTI4OSIsImlhdCI6MTY2NjExMDcwMiwiZXhwIjoxOTgxNDcwNzAyfQ.5KVla7Y72yKFrWhF01EupQpSHX0Rbr0CQ-LMLW6v6VU",
    "content-type": "application/json",
}
haResponse = get(haUrl, headers=haHeaders)
haData = json.loads(haResponse.text)
haLightColor = haData['attributes']['rgb_color']
gsAddress = "http://127.0.0.1:50786"
gsGame = "HA_LIGHT_SYNC"

def registerGame():
        """Registers this application to Engine."""
        endpoint = f'{gsAddress}/game_metadata'
        payload = {
            "game" : gsGame,
            "game_display_name" : gsGame,
            "developer" : "quoije"
        }
        r = post(endpoint, json=payload)
        print(r.text)


def sendGameEvent():
        """Sends a lighting event/frame to Engine."""
        endpoint = f'{gsAddress}/game_event'
        payload = {"game": gsGame,
            "event": "SYNC",
            "handlers": [{
                "device-type": "keyboard",
                "zone": "all",
                "color": {"red": haLightColor[0],"green": haLightColor[1],"blue": haLightColor[2]}
                }]}
        r = post(endpoint, json=payload)
        print(r.text)

sendGameEvent()
