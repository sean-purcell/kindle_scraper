import configparser
import importlib
import json
import os.path
import sys
import traceback

import scraper.flags
import scraper.gmail

flags = scraper.flags.get_flags()

def run_module(name, state, creds):
    print(f"Running scraper for {name}")

    try:
        mod = importlib.import_module(f"scraper.modules.{name}")
        return mod.scrape(state, creds)
    except ImportError:
        tb = traceback.format_exc()
        print(f"No scraper found for {name}:\n{tb}")
    except Exception as err:
        tb = traceback.format_exc()
        print(f"Failed to scrape {name}:\n{tb}")
    return [], None

def send_docs(creds, docs):
    if not flags.no_send:
        for name, content in docs:
            print(f"Sending {name}")
            scraper.gmail.send_html(creds, name, content)
    if flags.write_to_file:
        for name, content in docs:
            print(f"Writing to {name}.html")
            with open(f"{name}.html", "w") as out:
                out.write(content)

def get_state():
    state_path = flags.state_file
    if os.path.exists(state_path):
        return json.loads(open(state_path, "r").read())
    else:
        return {}

def store_state(state):
    state_path = flags.state_file
    with open(state_path, "w") as f:
        f.write(json.dumps(state) + "\n")

def main():
    scraper.flags.get_flags()

    creds = scraper.gmail.get_creds(flags.email_token)

    state = get_state()

    mods = flags.modules.split(",")
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

    send_docs(creds, all_docs)

    store_state(new_state)

if __name__ == "__main__":
    main()
