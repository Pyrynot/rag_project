import os
import requests
import json
import time
import mwparserfromhell

BASE_URL = "https://oldschool.runescape.wiki/api.php"
SAVE_DIR = "wiki"

def fetch_all_pages(limit=50):
    session = requests.Session()
    all_pages = []
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit": limit
    }

    response = session.get(url=BASE_URL, params=params)
    data = response.json()
    all_pages.extend(data["query"]["allpages"])

    return all_pages

def fetch_page_content(page_title):
    session = requests.Session()
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions|info|categories",
        "titles": page_title,
        "rvslots": "*",
        "rvprop": "content|timestamp|ids",
        "inprop": "url"
    }

    response = session.get(url=BASE_URL, params=params)
    data = response.json()

    page_id = next(iter(data["query"]["pages"]))
    page_data = data["query"]["pages"][page_id]

    content = page_data["revisions"][0]["slots"]["main"]["*"]
    timestamp = page_data["revisions"][0]["timestamp"]
    page_url = page_data["fullurl"]
    categories = [cat["title"] for cat in page_data.get("categories", [])]
    page_id = page_data["pageid"]
    revision_id = page_data["revisions"][0]["revid"]

    return {
        "title": page_title,
        "content": content,
        "timestamp": timestamp,
        "url": page_url,
        "categories": categories,
        "page_id": page_id,
        "revision_id": revision_id
    }

def save_to_file(directory, filename, data):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    print("Fetching limited pages...")
    pages = fetch_all_pages(limit=50)
    print(f"Total pages fetched: {len(pages)}")

    all_page_contents = []

    for page in pages:
        title = page['title']
        print(f"Fetching content for: {title}")
        page_content = fetch_page_content(title)
        
        # Skip redirects
        if page_content["content"].startswith("#REDIRECT"):
            print(f"Skipping redirect page: {title}")
            continue
        
        all_page_contents.append(page_content)
        time.sleep(0.5)  # To prevent overloading the server with requests

    save_to_file(SAVE_DIR, "osrs_wiki_contents.json", all_page_contents)
    print(f"All content saved to {os.path.join(SAVE_DIR, 'osrs_wiki_contents.json')}")

if __name__ == "__main__":
    main()
