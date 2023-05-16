import requests
from bs4 import BeautifulSoup as bs

session = requests.session()
session.headers.update({'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/32.0.1667.0 Safari/537.36', 'Accept': '*/*', 'Connection':
                                      'keep-alive', 'origin': 'https://now.morsmusic.org'})


def search(song: str) -> list:
    '''
    Searches for a song on webiste and returns a list of dictionaries containing information about each song.

    Args:
        song (str): The name of the song to search for.

    Returns:
        list: A list of dictionaries containing information about each song found in the search results.
        Each dictionary contains the following keys:
            - "artist": Name of the artist who performs the song.
            - "song": Name of the song.
            - "link": URL of the page where the song can be played or downloaded.
    '''
    url = f"https://now.morsmusic.org/search/{song}"
    html = requests.get(url)
    parsed = bs(html.text, 'lxml')
    songs = []
    all_tags = parsed.select_one("div", attrs={'class':"track mustoggler", 'data-musmeta':True})

    for i in all_tags.find_all('div', attrs={'class': 'track-info'}):
        song_name = i.a.text.strip()
        artist = i.div.a.text
        link = "https://now.morsmusic.org" + i.a['href']
        songs.append({
            "artist" : artist,
            "song": song_name,
            "link": link
        })
    return songs


def _download_link(link: str) -> str:
    html = requests.get(link)
    parser = bs(html.text, 'lxml')
    href = parser.find('div', class_='track-control-item track-download').a['href']
    return f"https://now.morsmusic.org{href}"







