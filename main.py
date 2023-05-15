import os
from argparse import ArgumentParser

import requests
from crawler import search, _download_link


download_path = os.path.join(os.environ['USERPROFILE'], 'Desktop') if os.name == 'nt' else os.path.join(os.path.expanduser('~'), 'Desktop')


def main() -> None:
    desc = "MusicCLI is a command-line interface application that allows users to search and download music from a " \
           "variety of online sources. With MusicCLI, users can easily find and download their favorite songs to their"\
           " Desktop folder."
    epilog = "If you find this project useful, we would greatly appreciate it if you could take a moment to give it a "\
             "star on GitHub. Your support helps us to continue improving the project and providing useful tools for "\
             "the community. Thank you for your consideration!😉"
    parser = ArgumentParser(prog="MusicCLI", description=desc, usage="mcli [SONG]", epilog=epilog)
    parser.add_argument('song', type=str, nargs='*', help='Name of the song')
    args = parser.parse_args()
    # For searching
    num = 1
    song_list = search(args.song)

    for i in song_list:
        name = f"{num}.{i['artist']} - {i['song']}"
        print(name)
        num += 1

    while True:
        number = int(input("Choose a number from the list to download the corresponding music: ")) - 1
        if number <= 0 or number > len(song_list):
            print("You choose wrong number, please do it again!")
            continue
        else:
            break
    choosen_song = song_list[number]
    with open(f"{download_path}/{choosen_song['artist']} - {choosen_song['song']}.mp3", 'wb') as music:
        music.write(requests.get(_download_link(song_list[number]['link'])).content)

    print("All done!")


if __name__ == "__main__":
    main()