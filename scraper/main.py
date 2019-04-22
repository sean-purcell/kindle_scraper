import configparser
import importlib
import json
import os.path

from scraper import gmail

def run_module(name, state, creds):
    print(f"Running scraper for {name}")

    try:
        mod = importlib.__import__(f"scraper.modules.{name}")
        return mod.scrape(state, creds)
    except Exception as err:
        print(f"Failed to scrape {name}: {err}")
    return [], None

def main():
    cfg = configparser.ConfigParser()
    cfg.read("CONFIG")

    state_path = cfg["scraping"]["state"]
    if os.path.exists(state_path):
        state = json.loads(open(state_path, "rb").read())
    else:
        state = {}

    creds = gmail.get_creds(cfg["email"]["token"])

    mods = cfg["scraping"]["modules"].split(",")
    print(state)
    print(mods)

    new_state = state

    all_docs = []
    for name in mods:
        docs, ns = run_module(name, state.get(name, {}), creds)
        if ns is not None:
            new_state[name] = ns
        all_docs += docs
    print(f"Obtained {len(all_docs)} documents")

if __name__ == "__main__":
    main()
