import collections
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def is_valid(word):
    if len(word) < 5:
        return False
    return "[" not in word and "]" not in word
def extract_lyrics(url):
    print(f"Fetching lyrics... {url}")
    r = requests.get(url)
    if r.status_code != 200:
        print("Page imposible a recuperer")
        return []

    soup = BeautifulSoup(r.content, 'html.parser')
    lyrics = soup.find("div", class_="PageGriddesktop-a6v82w-0 SongPageGriddesktop-sc-1px5b71-0 Lyrics__Root-sc-1ynbvzw-0 iEyyHq")
    if not lyrics :
        return extract_lyrics(url)

    all_words = []
    for sentence in lyrics.stripped_strings :
        sentence_words = [word.strip(".").strip(",").lower() for word in sentence.split() if is_valid(word)]
        all_words.extend(sentence_words)

    return all_words


def get_all_urls():
    page_number=1
    links = []
    while True :
        r = requests.get(f"https://genius.com/api/artists/29743/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            print(f"Fetching page {page_number}")
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")
            links.extend([song.get("url") for song in songs])

            page_number+=1
            if not next_page :
                print("No more page to fetch")
                break
    return links


def get_all_words():
    urls = get_all_urls()

    words = []
    for url in urls:
        lyrics = extract_lyrics(url=url)
        words.extend(lyrics)

    with open ("data.json","w") as f:
        json.dump(words, f,indent=4)


    counter = collections.Counter(words)
    most_common_words = counter.most_common(15)
    pprint(most_common_words)


get_all_urls()
get_all_words()