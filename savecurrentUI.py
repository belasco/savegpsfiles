#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
savecurrentUI.py
2017/12/24 13:47:20

A curses User Interface (UI) for savecurrentgps

Copyright 2017 Daniel Belasco Rogers dan@planbperformance.net
"""

import curses
import textwrap
import subprocess
from distutils.spawn import find_executable
from savecurrentgps import parse_arguments, getsettings,\
     checkgarminmount, makenewfilename, copygpxfile, \
     savecompress, writedatefile, preprocess


class Info(object):
    """Put a string in a window for the user. Do not wait for key
    press"""

    def __init__(self, maxyx, title):
        margin = 4
        self.height = maxyx[0] - margin * 2
        self.width = maxyx[1] - margin * 2
        self.window = curses.newwin(self.height,
                                    self.width,
                                    margin, margin)
        self.window.box()
        self.window.keypad(1)
        self.msg = textwrap.wrap(title, self.width - margin * 2)

    def display(self):
        line = 2
        margin = 4

        for idx, item in enumerate(self.msg):
            self.window.addstr(line + idx, margin, item)

        self.window.refresh()


class InfoPress(Info):
    """Modify Info with a press any key message and getch to wait on
    screen for user press"""

    def display(self):
        line = 2
        margin = 4

        for idx, item in enumerate(self.msg):
            self.window.addstr(line + idx, margin, item)

        line += len(self.msg)
        self.window.addstr(line + 2, margin, "Press any key to continue ")

        self.window.getch()

        self.window.clear()
        curses.doupdate()


class Menu(object):
    """Populate choices (items as a list) for the user to cycle through.

    After instantiating the object, display it with the object's display
    function. The answer is the answer property of the Menu object ie.
    Menuname.answer. maxyx is a screen property which gives a width and
    height for the window.
    """
    def __init__(self, items, maxyx, title):
        self.margin = 4
        self.window = curses.newwin(maxyx[0] - self.margin * 2,
                                    maxyx[1] - self.margin * 2,
                                    self.margin, self.margin)
        self.window.box()
        self.window.keypad(1)
        self.position = 0
        self.title = title
        self.items = items

    def display(self):
        line = 2  # running total of what line we're on for layout
        margin = 4

        self.window.addstr(line, margin, self.title)

        line += 2
        tab = margin + 4

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                self.window.addstr(line + index, tab, item, mode)

            # get user input
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                # the user has chosen the current position. Because we actually
                # want the user_uid index for the userdict dictionary, plus 1 to
                # position
                self.answer = self.items[self.position]
                break

            elif key in [curses.KEY_UP, curses.KEY_LEFT, ord('p')]:
                # navigate(-1)
                self.position = self.position - 1

            elif key in [curses.KEY_DOWN, curses.KEY_RIGHT, ord('n')]:
                # navigate(1)
                self.position = self.position + 1

            # Modulo the dictionary length as a way of wrapping the menu round i.e.
            # if under 0, go to max, if over max, go to 0 etc.
            self.position = self.position % len(self.items)

        self.window.clear()
        curses.doupdate()


def getuser(userdict, maxyx):
    "Loop through asking for the user until confirmed"

    while 1:
        # first question to find out user
        title = "Please choose who this GPS belongs to from the list below:"
        userlist = list(userdict.values())
        usermenu = Menu(userlist, maxyx, title)
        usermenu.display()
        chosenuser = usermenu.answer

        # confirm
        title = "You chose {}, is this correct?".format(chosenuser)
        usermenu = Menu(['Yes', 'No'], maxyx, title)
        usermenu.display()

        # only break out of this while loop when Yes is returned, otherwise ask
        # first question again
        if usermenu.answer == 'Yes':
            return chosenuser


def initscreen(myscreen):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)

    myscreen.bkgd(curses.color_pair(1))
    myscreen.border(0)
    curses.curs_set(0)
    myscreen.refresh()


def main(myscreen):
    """
    """
    initscreen(myscreen)
    maxyx = myscreen.getmaxyx()

    args = parse_arguments()

    # read settings
    garminfilelocation, curyear, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation,\
        userdict = getsettings(args.settingspath)

    # check if the garmin is mounted to the location specified in settings
    garminfilelocation = checkgarminmount(garminfilelocation)

    if not garminfilelocation:
        msg = "No Garmin found. Please plug in, wait for it "
        msg += "to produce a GPX file and try again"
        info = InfoPress(maxyx, msg)
        info.display()
        exit(2)
    else:
        info = InfoPress(maxyx, 'Garmin found, ready for import')
        info.display()

    # check for the auxiliary programmes this script may need and
    # inform the user if not found. Return the location of the
    # found script for later subprocess calls
    preprocessbin = find_executable("preprocessGPX")
    if not preprocessbin:
        msg = "The programme preprocessGPX was not found. "
        msg += "You will be able to save a compressed file, "
        msg += "but you will not be able to pre-process the file. "
        msg += "If you know you have it installed, you may "
        msg += "have a PATH problem because WHICH can't find it."
        info = InfoPress(maxyx, msg)
        info.display()
    vikingbin = find_executable("viking")
    if not vikingbin:
        msg = "Viking was not found on this system. "
        msg += "You will not be able to view or edit GPX files."
        info = InfoPress(maxyx, msg)
        info.display()

    # get and confirm user
    name = getuser(userdict, maxyx)

    msg = "Copying file to temporary location."
    info = Info(maxyx, msg)
    info.display()

    # create the new file path using the various settings and
    # calculated values
    newfilepath = makenewfilename(basefilepath,
                                  originaldirname,
                                  name, curyear)

    # copy gpx file from Garmin to temporary location set by settings
    tempgpxfile = copygpxfile(tempfilelocation,
                              newfilepath,
                              garminfilelocation)

    # use gzip to compress that file and save it in the 'original' folder
    savecompress(tempgpxfile, newfilepath)

    msg = "Saved GPX file as a compressed file "
    msg += "{}.gz ".format(newfilepath)
    info = Info(maxyx, msg)
    info.display()

    timefilepath = writedatefile(basefilepath, name)
    msg = "Wrote current time to {} ".format(timefilepath)
    info = Info(maxyx, msg)
    info.display

    if preprocessbin:
        msg = "Pre-processing and saving a copy in {}".format(preprocessdirname)
        info = Info(maxyx, msg)
        info.display
        preprocessout = preprocess(tempgpxfile, newfilepath,
                                   preprocessdirname, preprocessbin)

    if vikingbin:
        title = "Open the file in Viking?"
        vikingmenu = Menu(['Yes', 'No'], maxyx, title)
        vikingmenu.display()
        if vikingmenu.answer == 'Yes':
            subprocess.Popen([vikingbin, preprocessout])


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Exiting...")
        exit()
