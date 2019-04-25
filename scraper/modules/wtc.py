import requests
import bs4

import scraper.util

BASEURL = "https://archiveofourown.org/works/11478249"

AUTHOR = "cthuluraejepsen"

def _scrape_index():
    def idx(name):
        return int(name[: name.find(".")])
    req = requests.get(BASEURL)
    soup = bs4.BeautifulSoup(req.text, features="html5lib")
    options = soup.find("select", id="selected_id").find_all("option")
    return [(idx(o.text), o.text, o.attrs["value"]) for o in options]

def _scrape_chapter(key):
    req = requests.get(f"{BASEURL}/chapters/{key}")
    soup = bs4.BeautifulSoup(req.text, features="html5lib")
    return str(soup.find("div", "chapter"))

def _get_after(prev_idx):
    chaps = [(idx, name, key) for (idx, name, key) in _scrape_index() if idx > prev_idx]

    return [(idx, name, _scrape_chapter(key)) for (idx, name, key) in chaps]

def scrape(state, _creds):
    min_idx = state.get("idx", 0)
    chapters = _get_after(min_idx)

    return (
        [
            (name, scraper.util.format_chapter(name, content, AUTHOR))
            for (_, name, content) in chapters
        ],
        {"idx": max(0, min_idx, *[idx for (idx, _, _) in chapters])},
    )
