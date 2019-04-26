import asyncio
import aiohttp
import bs4

import scraper.util

BASEURL = "https://archiveofourown.org/works/11478249"

AUTHOR = "cthuluraejepsen"

async def _scrape_index(session):
    async with session.get(BASEURL, timeout=60) as resp:
        def idx(name):
            return int(name[: name.find(".")])
        text = await resp.text()
        soup = bs4.BeautifulSoup(text, features="lxml")
        options = soup.find("select", id="selected_id").find_all("option")
        return [(idx(o.text), o.text, o.attrs["value"]) for o in options]

async def _scrape_page(session, key):
    async with session.get(f"{BASEURL}/chapters/{key}") as resp:
        return await resp.text()

def _parse_chapter(text):
    soup = bs4.BeautifulSoup(text, features="lxml")
    return str(soup.find("div", "chapter"))

async def _get_after(prev_idx):
    async with aiohttp.ClientSession() as session:
        print(f"Getting index")
        chaps = await _scrape_index(session)
        chaps = [(idx, name, key) for (idx, name, key) in chaps if idx > prev_idx]
        async def _get_texts(idx, name, key):
            return (idx, name, await _scrape_page(session, key))
        print(f"Downloading {len(chaps)} pages")
        chaps = await asyncio.gather(*(_get_texts(*chap) for chap in chaps))

        print(f"Formatting {len(chaps)} pages")
        return [(idx, name, _parse_chapter(text)) for (idx, name, text) in chaps]

def scrape(state, _creds):
    min_idx = state.get("idx", 0)

    loop = asyncio.get_event_loop()
    chapters = loop.run_until_complete(_get_after(min_idx))

    return (
        [
            (name, scraper.util.format_chapter(name, content, AUTHOR))
            for (_, name, content) in chapters
        ],
        {"idx": max(0, min_idx, *[idx for (idx, _, _) in chapters])},
    )
