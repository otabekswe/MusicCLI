import os
from asyncio import create_task
from typing import Union

from bs4 import BeautifulSoup, ResultSet
from requests import get, session

bs = BeautifulSoup
session = session()
session.headers.update({'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, '
                        'like Gecko) Chrome/32.0.1667.0 Safari/537.36', 'Accept': '*/*', 'Connection': 'keep-alive'})

path : str
# Finding Path -> Desktop
if os.name == 'nt':
    path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
elif os.name == "posix":
    path = os.path.join(os.path.expanduser('~'), 'Desktop')
else:
    path = os.getcwd()


async def request_to(web: str) -> ResultSet:
    html = get(web).text
    parsed = bs(html, "lxml")
    track_info = None

    if "morsmusic" in web:
        song_tags = parsed.select_one("div", attrs={'class': "track mustoggler", 'data-musmeta': True})
        track_info = song_tags.find_all('div', class_='track-info')
    elif "uzhits" in web:
        song_tags = parsed.select_one("div", claas_="track-item fx-row fx-middle js-item")
        track_info = (song_tags.find_all('div', class_="track-item fx-row fx-middle js-item"), parsed.find('div', class_="navigation"))

    return track_info


async def search_uzhits(tags):
    if tags is None:
        return []
    songs = []
    for tag_data in tags[0]:
        song_name = list(tag_data.children)[1].text
        song_link = list(tag_data.children)[1].a['href']

        if song_link == "":
            continue

        songs.append({
            "song": song_name,
            "link": song_link,
        })
    return songs


async def search_morsmusic(tags):
    if tags is None:
        return []
    songs = []
    for tag_data in tags:
        song_name = tag_data.div.a.text + " - " + " ".join(tag_data.a.text.split())
        song_link = "https://now.morsmusic.org" + tag_data.a['href']

        if song_link == "":
            continue

        songs.append({
            "song": song_name,
            "link": song_link,
        })
    return songs


async def download_request(link: str) -> bytes:
    html = get(link).text
    parsed = bs(html, "lxml")
    if "morsmusic" in link:
        tag = parsed.find('a', class_='__adv_download')
        return get(f"https://now.morsmusic.org{tag['href']}").content

    elif "uzhits" in link:
        tag = parsed.find('a', class_='fbtn fdl')
        return get(tag['href']).content


def print_list(ls: list) -> None:
    num = 1
    for i in ls:
        print(f"{num}.{i['song']}")
        num += 1


async def get_list(name: str) -> Union[list, None]:
    req1 = create_task(request_to(f"https://now.morsmusic.org/search/{name}"))
    req2 = create_task(request_to(f"https://uzhits.net/xfsearch/{name}"))
    mormus = await req1
    uzhit = await req2
    songs = await search_morsmusic(mormus) + await search_uzhits(uzhit)
    if songs == []:
        return None
    return songs


def download(name: str, byte_code: bytes) -> None:
    with open(f"{path}/{name}.mp3", "wb") as music:
        music.write(byte_code)
        os.system("clear" if os.name == "posix" else "cls")
        print("All done!")
