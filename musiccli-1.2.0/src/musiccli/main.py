from argparse import ArgumentParser

from .crawler import get_list, print_list, download_request, download


async def runner(song_name: str) -> None:
    songs = await get_list(" ".join(song_name))

    if songs is None:
        print("Found nothing : (")
        return
    else:
        print_list(songs)
        print("Choose a number from the list to download the corresponding music.")

    while True:
        num = int(input("Number: ")) - 1

        if num < 0:
            print("Invalid number, please give valid number from the list!")
            continue

        try:
            song = songs[num]
        except IndexError:
            print("Invalid number, please give valid number from the list!")
            continue
        else:
            byte_code = await download_request(song['link'])
            download(song["song"], byte_code)
            return


async def main():
    desc = "MusicCLI is a command-line interface application that allows users to search and download music from a " \
           "variety of online sources. With MusicCLI, users can easily find and download their favorite songs to their" \
           " Desktop folder."
    epilog = "If you find this project useful, we would greatly appreciate it if you could take a moment to give it a " \
             "star on GitHub. Your support helps us to continue improving the project and providing useful tools for " \
             "the community. Thank you for your consideration!😉"
    parser = ArgumentParser(prog="MusicCLI", description=desc, usage="mcli [SONG]", epilog=epilog)
    parser.add_argument('song', type=str, nargs='*', help='Name of the song')
    args = parser.parse_args()

    await runner(args.song)








