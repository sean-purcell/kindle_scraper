import importlib
import sys
import traceback

def run_module_ebook(name):
    print(f"Running ebook scraper for {name}")

    try:
        mod = importlib.import_module(f"scraper.modules.{name}")
        return mod.scrape_ebook()
    except ImportError:
        print(f"No scraper found for {name}")
    except Exception as err:
        tb = traceback.format_exc()
        print(f"Failed to scrape {name}:\n{tb}")
    return None

def generate_ebook(name):
    ebook = run_module_ebook(name)
    if ebook:
        print(f"Writing to {name}.html")
        with open(f"{name}.html", "w") as out:
            out.write(ebook)

def main():
    generate_ebook(sys.argv[1])

if __name__ == "__main__":
    main()
