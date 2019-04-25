import configparser
import importlib
import json
import os.path
import sys
import traceback

from scraper import gmail

def run_module(name, state, creds):
    print(f"Running scraper for {name}")

    try:
        mod = importlib.import_module(f"scraper.modules.{name}")
        return mod.scrape(state, creds)
    except ImportError:
        print(f"No scraper found for {name}")
    except Exception as err:
        tb = traceback.format_exc()
        print(f"Failed to scrape {name}:\n{tb}")
    return [], None

def send_docs(cfg, creds, docs):
    for name, content in docs:
        gmail.send_html(cfg, creds, name, content)

def get_state(cfg):
    state_path = cfg["scraping"]["state"]
    if os.path.exists(state_path):
        return json.loads(open(state_path, "r").read())
    else:
        return {}

def store_state(cfg, state):
    state_path = cfg["scraping"]["state"]
    with open(state_path, "w") as f:
        f.write(json.dumps(state) + "\n")

def main():
    cfg = configparser.ConfigParser()
    cfg.read("CONFIG")

    creds = gmail.get_creds(cfg["email"]["token"])

    state = get_state(cfg)

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

    send_docs(cfg, creds, all_docs)

    store_state(cfg, new_state)

if __name__ == "__main__":
    main()
