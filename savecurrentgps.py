#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
savecurrentgpsncurses.py
2013/02/06 21:58:17 Daniel Belasco Rogers dan@planbperformance.net

This is an adaptation of savecurrentgps.py

The script is to automate the process of saving new gpx files.  It
checks for the GPS, which should mount at GARMNTPT, looks in the
user's dropbox location, finds the number of the last file, generates
a new filename and uses this as the destination to copy the file from
the mount (GARFILEPTH) to the dropbox folder. Then it asks the user if
they want to view the file in viking.

TODO
1. Generalise more by adding usernames, location of stored current
gpx files etc. in settings.cfg
2. improve robustness by checking for viking on system.
3. Include options to step back or exit?
"""

import curses
import sys
import os
import subprocess
import ConfigParser
from shutil import copy2
from glob import glob


def makenewfilename(name, CURYEAR):
    """
    generate a filename and path for the destination GPX file
    """
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.expanduser("~/Dropbox/planb/currentGPS/%s%s/" % (name, CURYEAR))

    # look in directory and find latest filename in order to increment
    filelist = glob(gpxfilepath + '*.gpx')
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


def initcurses():
    """
    """
    # start ncurses screen
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    # set offsets for text screens following
    y = 2
    x = 3
    return screen, y, x


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
            return 'soph'
        if answer in [ord('D'), ord('d')]:
            return 'dan'


def exitscreen(screen, y, x):
    """
    last screen
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "Copied data from GPS.")
    screen.addstr(y + 2, x, "After checking the result is what you expected in Viking or similar,")
    screen.addstr(y + 3, x, "you can safely unplug the GPS, turn it on and erase the tracks to clear it.")
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
    Is this an alternative last screen?
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "Do you want to view the file in Viking")
    screen.addstr(y + 1, x, "on exit?")
    screen.addstr(y + 3, x, "Y", curses.A_UNDERLINE)
    screen.addstr(y + 3, x + 1, "es/")
    screen.addstr(y + 3, x + 4, "N", curses.A_UNDERLINE)
    screen.addstr(y + 3, x + 5, "o?")
    screen.refresh()
    while 1:
        answer = screen.getch()
        if answer in [ord('Y'), ord('y')]:
            with open(os.devnull, "w") as fnull:
                subprocess.Popen(['viking', newfilepath], stdout=fnull, stderr=fnull)
            exitscreen(screen, y, x)
        elif answer in [ord('N'), ord('n')]:
            exitscreen(screen, y, x)


def copyscreen(screen, y, x, newfilename):
    """
    """
    screen.clear()
    screen.border(0)
    screen.addstr(y, x, "New file will be called: %s" % newfilename)
    screen.addstr(y + 2, x, "Press any key to copy file")
    screen.refresh()
    screen.getch()
    return


def getsettings(path):
    """
    get settings from an external settings file
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)
    CURYEAR = config.get('core', 'currentyear')
    GARMNTPT = config.get('core', 'garminlocation1')
    garminlocation2 = config.get('core', 'garminlocation2')
    return GARMNTPT, garminlocation2, CURYEAR


def main():
    """
    """
    # get settings
    GARMNTPT, garminlocation2, CURYEAR = getsettings('settings.cfg')
    GARFILEPTH = GARMNTPT + garminlocation2

    # initialise screen
    screen, y, x = initcurses()

    # Check screen
    welcomescreen(screen, y, x)

    # Check gps plugged in
    gpspresent(screen, y, x, GARMNTPT)

    # ask if the GPS is Soph's or Dan's
    name = asksophdan(screen, y, x)

    # silently query relevant dropbox folder for last saved name and
    # make new name, adding one to final number in filename
    newfilename, newfilepath = makenewfilename(name, CURYEAR)
    # copyscreen(screen, y, x, newfilename)

    # copy GPX file from GPS using newfilepath as destination
    copy2(GARFILEPTH, newfilepath)

    # offer the user the option of opening file in Viking
    vikingoption(screen, y, x, newfilepath)

    # exit, advising user to check GPX file in Viking and then erase
    # the data from the GPS
    exitscreen(screen, y, x)

if __name__ == '__main__':
    curses.wrapper(main())
