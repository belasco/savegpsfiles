#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
createFiles.py
2017/04/01 21:52:14
modified Sat 02 Jun 2018 15:59:06 CEST

A utility script to create the settings files in the right place
(~/.config/savecurrentgps/)

Copyright 2017 Daniel Belasco Rogers danbelasco@yahoo.co.uk
"""

import sys
import os
import argparse
from datetime import datetime
from shutil import copy2

__version = '0.2'


def parseargs():

    desc = "A utility script for savecurrentgps which creates "
    desc += "the settings file is in the right place, "
    desc += "in the users home directory. Also makes a structure to "
    desc += "receive the GPS files that savecurrentgps expects. "
    desc += "Argument is the directory in which to create the file "
    desc += "structure. Options listed in help. Version={}".format(__version)

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('basefilepath',
                        help="A path to make the directory structure in.")

    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {}".format(__version))

    parser.add_argument('-c', '--configpath',
                        default='~/.config/savecurrentgps',
                        help="Define an alternate path for the config file. Default: '%(default)s'")

    parser.add_argument('-y', '--year',
                        default=None,
                        help="Specify the year for the directory names. Default is current year.")

    parser.add_argument('-u', '--userlist',
                        default=['dan', 'soph'],
                        nargs='+',
                        help="Specify a list of users (can be a list of one!). Default:'%(default)s'")

    parser.add_argument('-t', '--tempfile',
                        default='/tmp',
                        help="Define an alternate path for temporary files. Default:'%(default)s'")

    return parser.parse_args()


def copyskeleton(configpath):

    settingsname = 'settings.cfg'
    curdir = os.path.dirname(__file__)
    skeletonpath = os.path.expanduser(os.path.join(curdir, settingsname))
    os.mkdir(configpath)
    newconfigfile = os.path.join(configpath, settingsname)
    copy2(skeletonpath, newconfigfile)
    return


def makesettings(configpath, year, basefilepath, tempfile, userlist):
    """"""
    EOL = "\n"
    configfile = "[core]" + EOL
    configfile += "currentyear={}{}".format(year, EOL)
    configfile += "# Mount point after the username" + EOL
    configfile += "garminfilelocation=GARMIN/Garmin/GPX/Current/Current.gpx" + EOL
    configfile += "basefilepath={}{}".format(basefilepath, EOL)
    configfile += "originaldirname=1_original" + EOL
    configfile += "preprocessdirname=2_preprocessed" + EOL
    configfile += "tempfilelocation={}{}".format(tempfile, EOL)
    configfile += "[users]" + EOL

    for user in userlist:
        configfile += user + EOL

    return configfile


def checkdir(path):
    "Check directory and exit if doesn't exist"

    path = os.path.expanduser(path)

    if os.path.isdir(path):
        return path
    else:
        print("The directory {} does not exist. Please check and try again".format(path))
        sys.exit(2)


def main():
    """
    """
    args = parseargs()

    basefilepath = checkdir(args.basefilepath)
    tempfile = checkdir(args.tempfile)
    configpath = checkdir(args.configpath)
    configpath = os.path.join(os.path.expanduser(args.configpath), 'settings.cfg')

    if not args.year:
        year = datetime.now().year
    else:
        year = args.year

    if os.path.isfile(configpath):
        print("You already have a config file at {}".format(configpath))
        print("No further action for this script.")
    else:
        configfile = makesettings(configpath, year, basefilepath, tempfile, args.userlist)
        with open(configpath, 'w') as f:
            f.write(configfile)
        print("Wrote new config file to {}".format(configpath))
        print("Please open in a text editor and customise, ")
        print("if necessary.")


if __name__ == '__main__':
    sys.exit(main())
