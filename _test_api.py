import asyncio
import os
import aiohttp
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
URL = "https://terasharefile.com/s/1VoUQWBM5KF8emN-cDXnRSA"
HASH = "1VoUQWBM5KF8emN-cDXnRSA"
API2 = "https://gold-newt-367030.hostingersite.com/tera.php?url=" + quote_plus(f"https://1024terabox.com/s/{HASH}")


async def test():
    async with aiohttp.ClientSession() as s:
        print("=== API2 ===")
        print(API2)
        async with s.get(API2, timeout=aiohttp.ClientTimeout(total=30)) as r:
            print("status", r.status)
            print((await r.text())[:800])

        print("\n=== XVERSE (terasharefile URL) ===")
        key = os.getenv("XVERSE_API_KEY", "")
        async with s.post(
            "https://xapiverse.com/api/terabox",
            json={"url": URL},
            headers={"Content-Type": "application/json", "xAPIverse-Key": key},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as r:
            print("status", r.status)
            print((await r.text())[:800])

        print("\n=== XVERSE (1024terabox URL) ===")
        async with s.post(
            "https://xapiverse.com/api/terabox",
            json={"url": f"https://1024terabox.com/s/{HASH}"},
            headers={"Content-Type": "application/json", "xAPIverse-Key": key},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as r:
            print("status", r.status)
            print((await r.text())[:800])


asyncio.run(test())
