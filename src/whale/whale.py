import os
import sys
import json
from pathlib import Path

USER_HOME = Path.home()
WHALE_HOME_DIRECTORY = USER_HOME / 'Library' / 'Application Support' / 'Naver' / 'Whale'
WHALE_BOOKMARK_FILE = WHALE_HOME_DIRECTORY / 'Profile 1' / 'Bookmarks'

ENCODING = 'utf-8'
URL = 'url'
FOLDER = 'folder'

def convert_to(query):
    return query.strip().lower()

query = convert_to(sys.argv[1] if len(sys.argv) > 1 else '')

# 북마크 JSON 파일 로드
with open(WHALE_BOOKMARK_FILE, 'r', encoding=ENCODING) as file:
    bookmark_json = json.load(file)

bookmark_bar = bookmark_json.get('roots', {}).get('bookmark_bar', {})

def search(query, element):
    element_type = element.get('type')

    if element_type == URL:
        return search_url(query, element)
    elif element_type == FOLDER:
        return search_folder(query, element)
    else:
        return []

def search_folder(query, element):
    children = element.get('children', [])
    results = []
    for child in children:
        results.extend(search(query, child))
    return results

def search_url(query, element):
    url = element.get('url', '')
    name = element.get('name', '')

    is_search_target = not query or (query in url.lower() or query in name.lower())

    if is_search_target:
        return [{
            "uid": name,
            "title": name,
            "arg": url
        }]
    return []

filtered_items = search(query, bookmark_bar)

print(json.dumps({"items": filtered_items}, ensure_ascii=False))
