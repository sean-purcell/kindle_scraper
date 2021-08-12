import bs4
import feedparser
import requests
import time

import scraper.util

FEED_URL = "https://www.royalroad.com/syndication/45534?count=25"

AUTHOR = "Alexander Wales"

def _get_chapters(previous):
    feed = feedparser.parse(FEED_URL)

    return sorted(
        filter(
            lambda x: x[0] > previous,
            [
                (time.mktime(ent.published_parsed), ent.title, ent.link)
                for ent in feed.entries
            ],
        )
    )

def _get_contents(link):
    response = requests.get(link)
    if response.status_code != 200:
        raise RuntimeError(f'Failed to download {link}: {response.status_code}')
    text = response.text
    soup = bs4.BeautifulSoup(text, features="lxml")
    contents = soup.find("div", class_="chapter-content")
    return contents.encode_contents(formatter="html").decode("utf-8")

def scrape(state, _creds):
    previous = state.get("previous", 0)
    chapters = _get_chapters(previous)

    out = []
    for ts, title, link in chapters:
        text = _get_contents(link)
        previous = max(previous, ts)
        out.append((title, scraper.util.format_chapter(title, text, AUTHOR)))
    return (out, {"previous": previous})

