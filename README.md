# CTF Writeups

Writeups for the web security labs and CTF challenges I've worked through. Each one covers the full run: the setup, the recon, the bug, the exploit, and how the bug should have been fixed.

## Writeups

| Writeup | Platform | Category | Difficulty | Date |
| --- | --- | --- | --- | --- |
| [I Bought a $1,337 Jacket for One Cent](Excessive%20Trust%20in%20Client-side%20controls/Report.md) | PortSwigger Web Security Academy | Business logic | Apprentice | Nov 10, 2026 |

## Repo layout

Each writeup has its own folder, named after the lab or challenge, with the writeup in `Report.md`:

```
ctf-writeups/
├── README.md
└── <Lab or challenge name>/
    └── Report.md
```

## Tools

- [Burp Suite](https://portswigger.net/burp) for intercepting and editing traffic
- Firefox, proxied through Burp

## Disclaimer

Everything here was done on deliberately vulnerable labs and CTF challenges that are built to be attacked. Don't use these techniques on systems you don't have permission to test.
