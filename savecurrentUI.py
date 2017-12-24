#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
savecurrentUI.py
2017/12/24 13:47:20

An attempt to build an ncurses UI for savecurrentgps

Copyright 2017 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys
import curses
from savecurrentgps import *


def main():
    """
    """
    args = parse_arguments()

    # read settings
    garminfilelocation, curyear, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation,\
        userdict = getsettings(args.settingspath)


if __name__ == '__main__':
    sys.exit(main())
