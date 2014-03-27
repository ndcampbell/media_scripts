import os
import sys
import urllib
import pylast #a python interface to last.fm api
from mutagen.easyid3 import EasyID3


def get_cover_art(mediadir):
    count = 0
    API_KEY = "11c7a5d7826cfa032c53e02ae058f24d"
    API_SECRET = "0dc369783d5069fb6a2087b6f5b597d0"
    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET) #no authentication required since no writing.

    for rootdir, dirnames, filenames in os.walk(mediadir):
        if "cover.jpg" in filenames or "cover.png" in filenames: #checks if cover.jpg is already present in the directory
            continue
        for files in filenames:
            if (files[-3:] == "mp3"):
                try:
                    audiofile = EasyID3(os.path.join(rootdir, files))
                    metadata= audiofile["artist"] + audiofile["album"]
                    album = network.get_album(metadata[0], metadata[1])
                    album_cover = album.get_cover_image(3) #the param is the size. 1 for small, 2 for medium, 3 for large (300x300)
                    cover_name = "cover.%s" % album_cover[-3:]
                    urllib.urlretrieve(album_cover, rootdir + os.sep + cover_name) #os.sep adds the directory separator. \ or / depending on OS
                    count +=1
                    break
                except: #if no album cover is found or issue with id3 tag. Will fix this in the future.
                    continue
    print "%d covers downloaded" % count

            

def fix_tags(): #future fix tags functions.
    return 0

if __name__ == "__main__":
    full_mediadir = sys.argv[1]
    get_cover_art(full_mediadir)


