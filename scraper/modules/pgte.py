import feedparser
import time

import scraper.util

FEED_URL = "https://practicalguidetoevil.wordpress.com/feed/"

AUTHOR = "Erratic Errata"

def _get_chapters(previous):
    feed = feedparser.parse(FEED_URL)

    return sorted(
        filter(
            lambda x: x[0] > previous,
            [
                (time.mktime(ent.published_parsed), ent.title, ent.content[0].value)
                for ent in feed.entries
            ],
        )
    )

def scrape(state, _creds):
    previous = state.get("previous", 0)
    chapters = _get_chapters(previous)

    out = []
    for ts, title, text in chapters:
        previous = max(previous, ts)
        out.append((f"{title}.html", scraper.util.format_chapter(title, text, AUTHOR)))
    return (out, {"previous": previous})
