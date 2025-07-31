import json
import os

# Load sources from JSON file
def load_sources():
    path = os.path.join(os.path.dirname(__file__), "data", "sources.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    sources = load_sources()
    print(f"Loaded {len(sources)} sources:")
    for source in sources:
        print(f"- {source['name']} ({source['baseUrl']})")

if __name__ == "__main__":
    main()
  
