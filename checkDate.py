#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
checkDate.py
2018/07/18 11:04:56

Look for the most recent files in the currentGPS folder for each user and check
whether danlast and sophlast need to be updated. Scenario: Sophia has
downloaded her GPS on her laptop using another version of savecurrentgps.py
which does not write to these files.

Copyright 2018 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys
from os import path
from glob import glob

from savecurrentgps import getsettings
from __init__ import CONFIGPATH


def getlastfiledates(basefilepath, curyear, originaldirname, userdict):

    for user in userdict:
        filepath = path.join(basefilepath, userdict[user] + curyear, originaldirname)
        filepath = "{}/*".format(filepath)
        filelist = glob(filepath)
        print(max(filelist, key=path.getctime))
        # print(path.join(basefilepath, userdict[user] + curyear, originaldirname))

    danlastfiledate = ""
    sophlastfiledate = ""

    return danlastfiledate, sophlastfiledate


def main():
    """
    """

    # Load location of settings.cfg file 
    settingspath = path.expanduser(CONFIGPATH)

    # Load information from the settings file
    garminfilelocation, curyear, basefilepath,\
    originaldirname, preprocessdirname, tempfilelocation,\
    userdict = getsettings(settingspath)

    print("")
    print("Loaded settings {}".format(settingspath))
    print("")

    # location of the relevant last date files
    danlastpath = path.join(basefilepath, 'danlast')
    sophlastpath = path.join(basefilepath, 'sophlast')

    # get modification (saved) dates of last files in relevant directories
    danlastfiledate, sophlastfiledate = getlastfiledates(basefilepath, curyear, originaldirname, userdict)


if __name__ == '__main__':
    sys.exit(main())
