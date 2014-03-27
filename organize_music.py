#!/usr/bin/env python

#Author: Doug Campbell
#Email: ndouglascampbell@gmail.com
#Date: March 05, 2014

#Description:
#Usage:b

###

import os 
import sys
import shutil
import albumart
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3

MUSIC_DIR = '/media/doug/Elements/Media/test_music'
ORG_DIR = '/media/doug/Elements/Media/Org_Music'

#builds out the appropriate directories 
def build_dirs(tags, media_dir, org_dir):

    artist_dir = os.path.join(org_dir, tags['artist'][0].title())
    #builds directory if doesnt exist
    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)
    
    album_dirname = '%s [%s]' % (tags['album'][0].title(), tags['date'][0])
    album_dir = os.path.join(artist_dir, album_dirname)
    if not os.path.exists(album_dir):
        os.makedirs(album_dir)
    
    return album_dir


def find_all_music(media_dir, org_dir):

    for rootdir, dirnames, filenames in os.walk(media_dir):
        for files in filenames:

            #handle mp3s
            if (files[-3:] == 'mp3'):
                try:
                    tags = EasyID3(os.path.join(rootdir, files))
                except Exception, e:
                    print "Error: %s" % (files, e)
             #handle flac
            elif (files[-4:] == 'flac'):
                try:
                    tags = FLAC(os.path.join(rootdir, files))
                    print tags
                except Exception, e:
                    print "Error: %s" % (files, e)

            album_dir = build_dirs(tags, media_dir, org_dir)

            if not os.path.isfile(os.path.join(album_dir, files)):
                shutil.copy(os.path.join(rootdir,files), album_dir)

if __name__ == "__main__":
    #make sure organized directory exists
    if not os.path.exists(ORG_DIR):
        os.makedirs(ORG_DIR)

    print "Moving all music now to %s..." % ORG_DIR
    find_all_music(MUSIC_DIR, ORG_DIR)
    print "Getting Cover Art..."
    albumart.get_cover_art(ORG_DIR)
    print "Done!"



