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
import configparser
from datetime import datetime
from shutil import move
from __init__ import CONFIGPATH, FILESTRUCTHELPER
from utils import askyesno

# folder names (if no config file is found and a new one has to be made)
ORIGINAL = '1_original'  # name for the folder for original files
PROCESSED = '2_preprocessed'  # name for the folder for processed files
CLEANED = '3_cleaned'  # cleaned folder name
TEMP = '/tmp' # temp folder name
ARCHIVE = '~/gps_projects/GPS'

__version__ = '0.1'


def parseargs():

    desc = "At the start of a new year, move the old GPS files to the "
    desc += "archive location and recreate an empty folder structure "
    desc += "for the new GPS files. Also checks for config file, makes "
    desc += "one if not and checks that the current year is in existing "
    desc += "file. Version={}".format(__version__)

    parser = argparse.ArgumentParser(description=desc)

    # parser.add_argument('basefilepath',
    #                     help="A path to make the directory structure in. \
    #                           e.g. '~/selectedplanbfiles/currentGPS'")

    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {}".format(__version__))

    parser.add_argument('-c', '--configpath',
                        default=CONFIGPATH,
                        help="Define an alternate path for the config file. \
                              Default: '%(default)s'")

    parser.add_argument('-y', '--year',
                        default=None,
                        help="Specify the year for the directory names. \
                              Default is current year.")

    parser.add_argument('-u', '--userlist',
                        default=['Dan', 'Soph'],
                        nargs='+',
                        help="Specify a list of users (can be a list of one!). \
                              Default:'%(default)s'")

    return parser.parse_args()


def makeconfigfile(configpath, year, basefilepath, userlist):
    config = configparser.ConfigParser()
    garminfilelocation = os.path.join('GARMIN', 'Garmin',
                                      'GPX', 'Current',
                                      'Current.gpx')
    config['core'] = {'currentyear': year,
                      'garminfilelocation': garminfilelocation,
                      'basefilepath': basefilepath,
                      'originaldirname': ORIGINAL,
                      'preprocessdirname': PROCESSED,
                      'cleaneddirname': CLEANED,
                      'tempfilelocation': TEMP,
                      'archivelocation': ARCHIVE}
    config['users'] = {}
    for idx, user in enumerate(userlist):
        config['users'][user] = str(idx + 1)

    with open(configpath, 'w') as f:
        config.write(f)

    return


def askbasefilepath():
    """Get a location to make empty file structure from user and check"""
    while 1:
        basefilepath = input('Path: ')
        basefilepath = os.path.expanduser(basefilepath)
        if not os.path.isdir(basefilepath):
            if os.path.isfile(basefilepath):
                print('You entered a file for the base filepath')
                print('Please select a valid root directory')
                print('e.g. ~/selectedplanbfiles/currentGPS')
                sys.exit(2)
            else:
                print(basefilepath)
                print('I do not understand what you entered as a ')
                print('path to a directory on your file system.')
                print('Please check and try again.')
                sys.exit(2)
        # it should be a directory. Confirm selection
        msg = 'You selected {}. Is this correct? '.format(basefilepath)
        ans = askyesno(msg)
        if ans:
            msg = 'Thank you. '
            msg += 'Will write {} to config'.format(basefilepath)
            print(msg)
            return basefilepath
        else:
            print('OK Script will end here')
            sys.exit()


def main():
    """
    """
    # get args
    args = parseargs()
    configpath = os.path.expanduser(args.configpath)

    # year is current year if not passed by user as argument
    if not args.year:
        year = datetime.now().year
    else:
        year = args.year

    # check for config file
    if not os.path.isfile(configpath):
        if os.path.isdir(configpath):
            print('Please specify a file to create new config')
            print('Not a directory')
            sys.exit(2)
        # make config file if not present
        print('Config file not found. Please enter a valid ')
        print('location for the file structure (basefilepath)')
        basefilepath = askbasefilepath()
        makeconfigfile(configpath, year, basefilepath, args.userlist)
        print('Wrote a new config file to {}'.format(configpath))

    # get users, year and locations from config file
    settings = configparser.ConfigParser()
    settings.read(configpath)

    # check there are files in basefile location
    currentyear = settings['core']['currentyear']
    basefilepath = os.path.expanduser(settings['core']['basefilepath'])
    checkdir = settings.options('users')[0] + currentyear
    checkdir = os.path.join(basefilepath, checkdir)

    if not os.path.isdir(checkdir):
        print('Cannot find files under {}'.format(basefilepath))
        print('Will not archive current files')
        print('Script ends here')
        sys.exit()
    else:

    # move directories from current to archive location
        archivelocation = os.path.expanduser(settings['core']['archivelocation'])
        archivelocation = os.path.join(archivelocation, currentyear)
        # create folder to hold current gps folders
        try:
            os.mkdir(archivelocation)
        except FileExistsError:
            print('Archive location {} already exists'.format(archivelocation))
            print('Check manually. Script ends here')
            sys.exit()

        # move folders to archive location
        move(basefilepath, archivelocation)
        
    # update year in config file (create if not found)
    # set up new directory structure


if __name__ == '__main__':
    sys.exit(main())
