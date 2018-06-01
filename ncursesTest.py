#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ncursesTest.py
2018/06/01 12:30:21

Testing aspects of ncurses for info and warning screens to use in savecurrentUI
when they work.

Copyright 2018 Daniel Belasco Rogers dan@planbperformance.net
"""

import textwrap
import curses
from time import sleep
from savecurrentUI import Info, Menu, initscreen


def dummyprocess():
    """Just something to keep the programme waiting a while"""
    sleep(5)
    return


class Nowait(Info):
    """Although this is actually a new version of Info, this feels like
    the base class to me"""

    def display(self):
        line = 2
        margin = 4

        for idx, item in enumerate(self.msg):
            self.window.addstr(line + idx, margin, item)

        self.window.refresh()


def main(myscreen):
    """
    """
    initscreen(myscreen)
    maxyx = myscreen.getmaxyx()

    nowait = Nowait(maxyx, "Starting some process, please wait...")
    nowait.display()
    dummyprocess()

    info = Info(maxyx, "Process has finished")
    info.display()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Got KeyboardInterrupt exception. Exiting...")
        exit()
