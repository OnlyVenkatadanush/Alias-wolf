# scanner.py

import asyncio
import aiohttp
import pandas as pd
import json

with open('data/config.json', 'r') as f:
    sites = json.load(f)
    print("[DEBUG] Sites loaded:", sites)
def getprofilelink(username,platform):
    return f"https://{platform}.com/{username}"

async def check_site(session, site, username):
    try:
        url = site["url"].format(username=username)
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                profile_link = getprofilelink(username, site["name"].lower())
                return {"site": site["name"], "url": url, "status": "Found","Profile link":profile_link}
            elif response.status == 404:
                return {"site": site["name"], "url": url, "status": "Not Found","Profile link":None}
            elif response.status == 429:
                return {"site": site["name"], "url": url, "status": "Too Many Requests","Profile link":None}
            elif response.status == 403:
                return {"site": site["name"], "url": url, "status": "Forbidden","Profile link":None}
            elif response.status == 500:
                return {"site": site["name"], "url": url, "status": "Internal Server Error","Profile link":None}
            elif response.status == 503:
                return {"site": site["name"], "url": url, "status": "Service Unavailable","Profile link":None}
            elif response.status == 301 or response.status == 302:
                return {"site": site["name"], "url": url, "status": "Moved Permanently","Profile link":None}
            elif response.status == 401:
                return {"site": site["name"], "url": url, "status": "Unauthorized","Profile link":None} 
            elif response.status == 408:
                return {"site": site["name"], "url": url, "status": "Request Timeout","Profile link":None}
            else:
                return {"site": site["name"], "url": url, "status": f"Status {response.status}","Profile link":None}
    except Exception:
        return {"site": site["name"], "url": "", "status": "Error"}

async def scan_all(username):
    async with aiohttp.ClientSession() as session:
        tasks = [check_site(session, site, username) for site in sites]
        return await asyncio.gather(*tasks)

def scan_username(username):
    results = asyncio.run(scan_all(username))
    df = pd.DataFrame(results)
    return df
