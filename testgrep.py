#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
testgrep.py
2014/02/19 11:04:45 Daniel Belasco Rogers danbelasco@yahoo.co.uk


"""

import sys
import os
import ConfigParser
from glob import glob


def makenewfilename(dropboxlocation, dropboxoriginal, name, CURYEAR):
    """
    generate a filename and path for the destination GPX file
    """
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.join(dropboxlocation, name + CURYEAR,
                               dropboxoriginal)

    # look in directory and find latest filename in order to increment
    filelist = glob(os.path.join(gpxfilepath, '*.gpx'))

    if filelist == []:
        # it might be a new year and the directory is empty
        newnum = '01'
    else:
        lastfile = sorted(filelist)[-1]
        # split last filename and increment number for filename
        lastfile = os.path.splitext(lastfile)[0]
        filenum = lastfile[lastfile.rfind('-') + 1:]
        newnum = '%02d' % (int(filenum) + 1)

    # make user character for filename generation from answer
    userchar = name[0].upper()

    # put it all together and return filepath
    newfilename = "%s-%s-%s.gpx" % (CURYEAR, userchar, newnum)
    newfilepath = os.path.join(gpxfilepath, newfilename)

    return newfilename, newfilepath


def getsettings(path):
    """
    get settings from an external settings file
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)
    CURYEAR = config.get('core', 'currentyear')
    GARMNTPT = config.get('core', 'garminmountpoint')
    garminfilelocation = config.get('core', 'garminfilelocation')
    dropboxlocation = config.get('core', 'dropboxlocation')
    dropboxoriginal = config.get('core', 'dropboxoriginal')
    dropboxpreprocessed = config.get('core', 'dropboxpreprocessed')
    return GARMNTPT, garminfilelocation, CURYEAR, dropboxlocation,\
        dropboxoriginal, dropboxpreprocessed


def main():
    """
    """
    # check settings
    settingspath = os.path.expanduser('~/bin/settings.cfg')

    # load settings
    GARMNTPT, garminfilelocation, CURYEAR, dropboxlocation,\
        dropboxoriginal, dropboxpreprocessed = getsettings(settingspath)

    dropboxlocation = os.path.expanduser(dropboxlocation)
    print 'dropboxlocation', dropboxlocation

    name = 'dan'

    # silently query relevant dropbox folder for last saved name and
    # make new name, adding one to final number in filename
    newfilename, newfilepath = makenewfilename(dropboxlocation,
                                               dropboxoriginal,
                                               name, CURYEAR)
    print 'newfilename', newfilename


if __name__ == '__main__':
    sys.exit(main())
