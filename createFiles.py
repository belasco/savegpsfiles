#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
createFiles.py
2017/04/01 21:52:14

A utility script to create the settings files in the right place
(~/.config/savecurrentgps/)

Copyright 2017 Daniel Belasco Rogers danbelasco@yahoo.co.uk
"""

import sys
import os
import argparse
from shutil import copy2

__version = '0.2'


def parseargs():

    desc = "A utility script for savecurrentgps which makes sure "
    desc += "the settings file is in the right place, copying from "
    desc += "the skeleton file in the distribution to a config file "
    desc += "in the users home directory. Also makes a structure to "
    desc += "receive the GPS files that savecurrentgps expects"

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {}".format(__version))
    parser.add_argument('-c', '--configpath',
                        default='~/.config/savecurrentgps',
                        help="Define an alternate path for the config file. Default is ~/.config/savecurrentgps")

    return parser.parse_args()


def copyskeleton(configpath):

    settingsname = 'settings.cfg'
    curdir = os.path.dirname(__file__)
    skeletonpath = os.path.expanduser(os.path.join(curdir, settingsname))
    os.mkdir(configpath)
    newconfigfile = os.path.join(configpath, settingsname)
    copy2(skeletonpath, newconfigfile)
    return


def main():
    """
    """
    args = parseargs()
    configpath = os.path.expanduser(args.configpath)

    if os.path.isdir(configpath):
        print("You already have the config files in the right place.")
    else:
        copyskeleton(configpath)
        print("Copied blank config file to {}".format(configpath))
        print("Please open in a text editor and customise, ")
        print("before running createDirs to make the right folder structure")
        print("if necessary.")


if __name__ == '__main__':
    sys.exit(main())
