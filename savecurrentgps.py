#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""savecurrentgps.py
Daniel Belasco Rogers dan@planbperformance.net

Wed 15 Jul 2015 17:38:21 CEST 

Re-writing ncurses-based script to take back to bare essentials.
Command line only with functions that could then be called by a gui
if I build one later.

"""

import curses
import sys
import os
import subprocess
import ConfigParser
import gzip
from shutil import copy2

__version__ = '0.3'


def vikingoption(screen, y, x, newfilepath):
    """
    Offer the user the option to open the file in Viking.
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "Do you want to edit the")
    screen.addstr(y + 1, x, "processed file in Viking?")
    screen.addstr(y + 3, x, "Y", curses.A_UNDERLINE)
    screen.addstr(y + 3, x + 1, "es/")
    screen.addstr(y + 3, x + 4, "N", curses.A_UNDERLINE)
    screen.addstr(y + 3, x + 5, "o?")
    screen.refresh()
    while 1:
        answer = screen.getch()
        if answer in [ord('Y'), ord('y')]:
            with open(os.devnull, "w") as fnull:
                subprocess.Popen(['viking', newfilepath],
                                 stdout=fnull, stderr=fnull)
            return
        elif answer in [ord('N'), ord('n')]:
            return


def preprocess(newfilepath, preprocesslocation):
    """
    run preprocessGPX on the copied file
    """
    with open(os.devnull, 'w') as fnull:
        subprocess.Popen(['preprocessGPX', newfilepath, '-d',
                          preprocesslocation, '-c'],
                         stdout=fnull, stderr=fnull)
    return


def getsettings(path):
    """
    get settings from the external settings file
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)
    CURYEAR = config.get('core', 'currentyear')
    garminfilelocation = config.get('core', 'garminfilelocation')
    basefilepath = config.get('core', 'basefilepath')
    originaldirname = config.get('core', 'originaldirname')
    preprocessdirname = config.get('core', 'preprocessdirname')
    tempfilelocation = config.get('core', 'tempfilelocation')

    # if path features tildes, expand these
    basefilepath = os.path.expanduser(basefilepath)
    tempfilelocation = os.path.expanduser(tempfilelocation)

    return garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation


def getsettingspath():
    """
    find settings in current dir of this script and capture non
    existence- this location may change
    """
    curdir = os.path.dirname(__file__)
    settingspath = os.path.expanduser(os.path.join(curdir, 'settings.cfg'))

    if not os.path.exists(settingspath):
        print "Error: Settings file not found at %s" % settingspath
        print
        sys.exit(2)

    print "Loaded settings"
    print

    return settingspath


def checkgarminmount(garminfilelocation):

    if not os.path.exists(garminfilelocation):
        print "Error:"
        print "No GPS found at %s" % garminfilelocation
        print
        print "Check that the GPS is plugged in"
        print "and has finished making GPX file"
        print "then try again."
        print
        sys.exit(2)

    print "GPS found"
    print

    return


def asksophdan():
    """
    ask the user whether this is Soph's GPS or Dan's and return the
    answer as 'name'
    """
    name = ""

    while 1:
        name = raw_input("Is this Soph's GPS or Dan's [s/d]? ")
        name = name.lower()
        if name == 's':
            return 'soph'
        elif name == 'd':
            return 'dan'
        else:
            print "Please answer 's' or 'd' for Soph or Dan..."
            print


def makenewfilename(basefilepath, originaldirname, name, CURYEAR):
    """
    generate a filename and path for the destination GPX file
    """
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.join(basefilepath, name + CURYEAR,
                               originaldirname)

    # look in directory and find latest filename in order to increment
    filelist = os.listdir(gpxfilepath)

    if filelist == []:
        # it might be a new year and the directory is empty
        newnum = '01'
    else:
        lastfile = sorted(filelist)[-1]
        # split last filename and increment number for filename
        filenum = lastfile[lastfile.rfind('-') + 1:]
        filenum = filenum[:filenum.find('.')]
        newnum = '%02d' % (int(filenum) + 1)

    # make user character for filename generation from answer
    userchar = name[0].upper()

    # put it all together and return filepath
    newfilename = "%s-%s-%s.gpx" % (CURYEAR, userchar, newnum)
    newfilepath = os.path.join(gpxfilepath, newfilename)

    return newfilepath


def copygpxfile(tempfilelocation, newfilepath, garminfilelocation):
    """
    copy the gpx file from garmin to a temp location and return the file path to it
    """
    newfilename = os.path.basename(newfilepath)
    tempgpxfile = os.path.join(tempfilelocation, newfilename)

    copy2(garminfilelocation, tempgpxfile)

    return tempgpxfile


def savecompress(tempgpxfile, newfilepath):
    """
    compress and save this file to location for 'original' files
    """

    with open(tempgpxfile, 'rb') as tempgpxfileobj:
        with gzip.open(newfilepath + '.gz', 'wb') as compressgpxfile:
            compressgpxfile.writelines(tempgpxfileobj)


def main():
    """
    """
    settingspath = getsettingspath()

    # read settings
    garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation\
        = getsettings(settingspath)

    # check to see if the garmin is mounted at the expected
    # location (see settings)
    checkgarminmount(garminfilelocation)

    # ask if the GPS is Soph's or Dan's
    name = asksophdan()

    # create the new file path using the various settings and
    # calculated values
    newfilepath = makenewfilename(basefilepath,
                                  originaldirname,
                                  name, CURYEAR)

    # copy the raw GPX file from the Garmin device to a temporary
    # folder
    tempgpxfile = copygpxfile(tempfilelocation,
                              newfilepath,
                              garminfilelocation)

    print "Saving GPX file from Garmin as a compressed file in %s" % newfilepath
    savecompress(tempgpxfile, newfilepath)

    # # evoke preprocessGPX on copied file, make file paths and tell
    # # user
    # preprocesslocation = os.path.join(os.path.dirname
    #                                   (os.path.dirname(newfilepath)),
    #                                   preprocessdirname)
    # preprocess(tempgpxfile, preprocesslocation)
    # processedfilepath = os.path.join(preprocesslocation,
    #                                  os.path.basename(newfilepath))
    # processedfilepath = "%s_pp.gpx" % (os.path.splitext(processedfilepath)[0])

    # # offer the user the option of opening file in Viking
    # vikingoption(screen, y, x, processedfilepath)

    # exitscreen(screen, y, x)

if __name__ == '__main__':
    sys.exit(main())
