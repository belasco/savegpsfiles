#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
archive_makefolders.py
2019/01/12 20:51:22

At the start of a new year, move the old GPS files to the
archive location and recreate an empty folder structure
for the new GPS files. Also checks for config file, makes
one if not and checks that the current year is in existing
file.

Based on createFiles.py

NB use shutil.move (preserves create times and ownership)
Use configparser to create config file. NOT like in createFiles.py

Copyright 2019 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys
import os
import argparse
from datetime import datetime


__version__ = '0.1'


def parseargs():

    desc = "At the start of a new year, move the old GPS files to the "
    desc += "archive location and recreate an empty folder structure "
    desc += "for the new GPS files. Also checks for config file, makes "
    desc += "one if not and checks that the current year is in existing "
    desc += "file. Version={}".format(__version__)

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('basefilepath',
                        help="A path to make the directory structure in.")

    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {}".format(__version__))

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


def main():
    """
    """
    # get args
    # get previous year from folder names
    # make new year folder in archive location
    # move directories from current to archive location
    # update year in config file (create if not found)
    # set up new directory structure


if __name__ == '__main__':
    sys.exit(main())
