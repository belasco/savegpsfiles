#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
createFiles.py
2017/04/01 21:52:14
modified Sat 02 Jun 2018 15:59:06 CEST

A utility script to create the settings files in the right place
(~/.config/savecurrentgps/) and the base file structure for savecurrentgps

Copyright 2017 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys
import os
import argparse
from datetime import datetime

__version = '0.2'
# folder names (see savecurrent for details)
ORIGINAL = '1_original'  # name for the folder for original files
PROCESSED = '2_preprocessed'  # name for the folder for processed files
CLEANED = '3_cleaned'  # cleaned folder name


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


def makesettings(configpath, year, basefilepath, tempfile, userlist):
    """"""
    EOL = "\n"
    configfile = "[core]" + EOL
    configfile += "currentyear={}{}".format(year, EOL)
    configfile += "# Mount point after the username" + EOL
    configfile += "garminfilelocation=GARMIN/Garmin/GPX/Current/Current.gpx" + EOL
    configfile += "basefilepath={}{}".format(basefilepath, EOL)
    configfile += "originaldirname={}{}".format(ORIGINAL, EOL)
    configfile += "preprocessdirname={}{}".format(PROCESSED, EOL)
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


def makefilestructure(basefilepath, year, userlist):

    os.mkdir(basefilepath)

    for user in userlist:
        userdir = user + str(year)
        userdir = os.path.join(basefilepath, userdir)
        os.mkdir(userdir)
        os.mkdir(os.path.join(userdir, ORIGINAL))
        os.mkdir(os.path.join(userdir, PROCESSED))
        os.mkdir(os.path.join(userdir, CLEANED))

    return


def main():
    """
    """
    args = parseargs()

    tempfile = checkdir(args.tempfile)
    configpath = checkdir(args.configpath)
    configpath = os.path.join(os.path.expanduser(args.configpath), 'settings.cfg')

    # get current year if not provided
    if not args.year:
        year = datetime.now().year
    else:
        year = args.year

    # make the file structure if not there
    if os.path.isdir(args.basefilepath):
        print('Already have a file structure to save the gpx files.')
    else:
        makefilestructure(args.basefilepath, year, args.userlist)
        print('Made a file structure at {}'.format(args.basefilepath))

    # make and save the config file
    if os.path.isfile(configpath):
        print("You already have a config file at {}".format(configpath))
        print("No further action for this script.")
    else:
        configfile = makesettings(configpath, year, args.basefilepath, tempfile, args.userlist)
        with open(configpath, 'w') as f:
            f.write(configfile)
        print("Wrote new config file to {}".format(configpath))
        print("Please open in a text editor and customise, ")
        print("if necessary.")


if __name__ == '__main__':
    sys.exit(main())
