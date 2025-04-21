import asyncio
import aiohttp
import json


async def check_username(session, platform, url_template, username):
    url = url_template.replace("{username}", username)
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                return (platform, "FOUND", url)
            elif resp.status == 404:
                return (platform, "NOT FOUND", url)
            elif resp.status == 429:
                return (platform, "(429 Too Many Requests)", url)
            else:
                return (platform, f"ERROR ({resp.status})", url)
    except Exception as e:
        return (platform, f"ERROR ({str(e)})", url)

async def scan_user(username, config):
    results = []
    '''user_agents=[
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    ]'''
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for platform, url_template in config["platforms"].items():
            tasks.append(check_username(session, platform, url_template, username))
        results = await asyncio.gather(*tasks)
    return results
