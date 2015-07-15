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
from glob import glob

__version__ = '0.3'


def makenewfilename(dropboxlocation, dropboxoriginal, name, CURYEAR):
    """
    generate a filename and path for the destination GPX file
    """
    name = name.lower()
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.join(dropboxlocation, name + CURYEAR,
                               dropboxoriginal)

    # look in directory and find latest filename in order to increment
    filelist = glob(os.path.join(gpxfilepath, '*.*'))
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

    return newfilename, newfilepath


def welcomescreen(screen, y, x):
    """
    start the programme with a reminder to plug gps in
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "Make sure your GPS is plugged in")
    screen.addstr(y + 1, x, "and has finished making the GPX file")
    screen.addstr(y + 3, x, "Then press any key to continue")
    screen.refresh()
    screen.getch()
    return


def gpspresent(screen, y, x, GARMNTPT):
    """
    if GPS not plugged in, end script giving user instructions
    """
    if not os.path.exists(GARMNTPT):
        screen.clear()
        screen.border(0)
        screen.addstr(y, x, ("Error: GPS not found at %s" % GARMNTPT))
        screen.addstr(y + 2, x, "Please plug in GPS and wait for it to finish saving data as GPX")
        screen.addstr(y + 3, x, "Then run this script again")
        screen.addstr(y + 5, x, "Press any key to exit")
        screen.refresh()
        curses.beep()
        screen.getch()
        curses.endwin()
        sys.exit(2)
    return


def asksophdan(screen, y, x):
    """
    ask the user whether this is Soph's GPS or Dans and return answer
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, 2, "GPS found")
    screen.addstr(y + 1, 2, "Is this Soph's GPS or Dan's?...")
    screen.addstr(y + 3, x + 2, "S", curses.A_UNDERLINE)
    screen.addstr(y + 3, x + 3, "oph's GPS")
    screen.addstr(y + 4, x + 2, "D", curses.A_UNDERLINE)
    screen.addstr(y + 4, x + 3, "an's GPS")
    screen.addstr(y + 6, x + 2, "(Press 'D' or 'S')")
    screen.refresh()
    while 1:
        answer = screen.getch()
        if answer in [ord('S'), ord('s')]:
            return 'Soph'
        if answer in [ord('D'), ord('d')]:
            return 'Dan'


def checksophdan(screen, y, x, name):
    """
    confirm the answer to the asksophdan question
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "You said that it is %s's GPS" % (name))
    screen.addstr(y + 3, x, "Is this correct?")
    screen.addstr(y + 5, x, "Y", curses.A_UNDERLINE)
    screen.addstr(y + 5, x + 1, "es/")
    screen.addstr(y + 5, x + 4, "N", curses.A_UNDERLINE)
    screen.addstr(y + 5, x + 5, "o?")
    screen.refresh()
    while 1:
        answer = screen.getch()
        if answer in [ord('Y'), ord('y')]:
            return True
        elif answer in [ord('N'), ord('n')]:
            return False


def exitscreen(screen, y, x):
    """
    last screen
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "Copied data from GPS and created a preprocessed file")
    screen.addstr(y + 2, x, "Script ends successfully here")
    screen.addstr(y + 5, x, "Press any key to exit")
    screen.refresh()
    screen.getch()
    curses.endwin()
    sys.exit()


def noviking(screen, y, x):
    """
    Report to the user that Viking isn't on the current system
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "You don't seem to have Viking installed on your system")
    screen.addstr(y + 1, x, "Try sudo apt-get install viking")
    screen.addstr(y + 5, x, "Press any key to exit")
    screen.refresh()
    screen.getch
    return


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


def checksettings(settingspath, screen, y, x):
    """
    Check the user has the settings file installed and advise
    """
    if not os.path.exists(settingspath):
        screen.clear()
        screen.border(0)
        screen.addstr(y, x, ("Error: Settings file not found at %s"
                             % settingspath))
        screen.addstr(y + 2, x, "Please link to the settings file")
        screen.addstr(y + 3, x, "from the directory this script is run in")
        screen.addstr(y + 4, x, "and try again")
        screen.addstr(y + 6, x, "Press any key to exit")
        screen.refresh()
        curses.beep()
        screen.getch()
        curses.endwin()
        sys.exit(2)
    return


def getsettings(path):
    """
    get settings from an external settings file
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)
    CURYEAR = config.get('core', 'currentyear')
    garminfilelocation = config.get('core', 'garminfilelocation')
    dropboxlocation = config.get('core', 'dropboxlocation')
    dropboxoriginal = config.get('core', 'dropboxoriginal')
    dropboxpreprocessed = config.get('core', 'dropboxpreprocessed')
    tempfilelocation = config.get('core', 'tempfilelocation')
    return garminfilelocation, CURYEAR, dropboxlocation,\
        dropboxoriginal, dropboxpreprocessed, tempfilelocation


def main(screen):
    """
    """
    # offsets for text
    y = 2
    x = 3

    # current directory of script to find settings
    curdir = os.path.dirname(__file__)
    settingspath = os.path.expanduser(os.path.join(curdir, 'settings.cfg'))
    checksettings(settingspath, screen, y, x)
    # load settings
    garminfilelocation, CURYEAR, dropboxlocation,\
        dropboxoriginal, dropboxpreprocessed, tempfilelocation\
        = getsettings(settingspath)

    dropboxlocation = os.path.expanduser(dropboxlocation)
    tempfilelocation = os.path.expanduser(tempfilelocation)

    welcomescreen(screen, y, x)

    gpspresent(screen, y, x, garminfilelocation)

    # ask if the GPS is Soph's or Dan's
    while 1:
        name = asksophdan(screen, y, x)
        confirm = checksophdan(screen, y, x, name)
        if confirm:
            break

    # silently query relevant dropbox folder for last saved name and
    # make new name, adding one to final number in filename
    newfilename, newfilepath = makenewfilename(dropboxlocation,
                                               dropboxoriginal,
                                               name, CURYEAR)

    # copy GPX file from GPS using newfilepath as destination
    tempgpxfile = os.path.join(tempfilelocation, newfilename)
    copy2(garminfilelocation, tempgpxfile)

    # compress and save this file to location for 'original' files
    with open(tempgpxfile, 'rb') as tempgpxfileobj:
        with gzip.open(newfilepath + '.gz', 'wb') as compressgpxfile:
            compressgpxfile.writelines(tempgpxfileobj)

    # evoke preprocessGPX on copied file, make file paths and tell
    # user
    preprocesslocation = os.path.join(os.path.dirname
                                      (os.path.dirname(newfilepath)),
                                      dropboxpreprocessed)
    preprocess(tempgpxfile, preprocesslocation)
    processedfilepath = os.path.join(preprocesslocation,
                                     os.path.basename(newfilepath))
    processedfilepath = "%s_pp.gpx" % (os.path.splitext(processedfilepath)[0])

    # offer the user the option of opening file in Viking
    vikingoption(screen, y, x, processedfilepath)

    exitscreen(screen, y, x)

if __name__ == '__main__':
    curses.wrapper(main)
