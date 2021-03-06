#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""savecurrentgps.py
Daniel Belasco Rogers dan@planbperformance.net

Utility script to copy and compress the current GPX file from an attached
Garmin GPS, produce a pre-processed gpx file and view the result (if Viking is
installed)

Re-writing April 2017 to change location of config file to user's home
directory and implement the saving of a reference file with each download that
tracks the age of the most recent GPX file downloaded.

"""

import sys
import os
import subprocess
import configparser
import argparse
import gzip
from shutil import copy2
from distutils.spawn import find_executable
from os import path, environ
from datetime import datetime
from __init__ import __version__, CONFIGPATH, FILESTRUCTHELPER
from utils import askyesno


def parse_arguments():
    desc = "Utility script to copy and compress the current GPX "
    desc += "file from an attached Garmin GPS, "
    desc += "produce a pre-processed gpx file and "
    desc += "view the result (if Viking is installed)"
    parser = argparse.ArgumentParser(description=desc)

    settingspath = getsettingspath()

    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("-s", "--settingspath",
                        default=settingspath,
                        help="Path to the default settings file or define an alternate")

    return parser.parse_args()


def getsettings(path):
    """
    get settings from the external settings file
    """
    config = configparser.RawConfigParser()
    config.read(path)
    curyear = config.get('core', 'currentyear')
    garminfilelocation = config.get('core', 'garminfilelocation')
    basefilepath = config.get('core', 'basefilepath')
    originaldirname = config.get('core', 'originaldirname')
    preprocessdirname = config.get('core', 'preprocessdirname')
    tempfilelocation = config.get('core', 'tempfilelocation')

    userlist = config.options('users')
    userdict = {}
    for idx, user in enumerate(userlist):
        userdict[idx + 1] = user

    basefilepath = os.path.expanduser(basefilepath)
    tempfilelocation = os.path.expanduser(tempfilelocation)

    return garminfilelocation, curyear, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation, userdict


def getsettingspath():
    """
    find settings in current dir of this script and capture non
    existence- this location may change
    """

    settingspath = os.path.expanduser(CONFIGPATH)

    if not os.path.isfile(settingspath):
        print("Error: Settings file not found at {}".format(settingspath))
        print("Run createFiles.py and edit to make the file")
        print("in the correct location\n")
        sys.exit(2)

    return settingspath


def checkgarminmount(garminsettinglocation):
    """
    Look for the Garmin mounted at the location set in the settings
    config file, cycling through the usual arch and debian mount points
    and notify the user if it is not there.
    """
    user = environ.get('USER')
    archprefix = path.join('/run/media', user)
    mountprefix = path.join('/media', user)
    garminlocation = path.join(mountprefix, garminsettinglocation)
    if not path.exists(garminlocation):
        garminlocation = path.join(archprefix, garminsettinglocation)
        if not path.exists(garminlocation):
            garminlocation = False

    return garminlocation


def nogarmin():
    """Notify user that Garmin was not found and exit"""

    msg = """Error:
No GPS found.

Check that the GPS is plugged in, mounted,
and has finished making a GPX file,
then try again.
"""
    print(msg)
    sys.exit(2)


def chooseuser(userdict):
    """
    using the user dictionary from the settings file, ask who's GPS
    this is
    """
    print("Please choose who this GPS belongs to from the list below:")

    for key in sorted(userdict.keys()):
        print("{}:  {}".format(key, userdict[key]))

    while 1:
        user_uid = input("Enter a number from 1 to {} > ".format(len(userdict)))
        user_uid = int(user_uid)
        if user_uid in userdict.keys():
            # confirm the selection
            print()
            ans = askyesno('You selected {}. Is this correct? '.format(userdict[user_uid]))
            if ans:
                return user_uid
            else:
                print('Please run the script again to select the correct user')
                print('Script ends here\n')
                sys.exit()

        elif user_uid.lower() == 'q':
            print("You pressed q for Quit... Goodbye")
            print
            sys.exit()

        print('Your entry was not valid. Please try again.')


def checkfilestruct(basefilepath, curyear):
    """"""
    # gpxfilepath = os.path.join(basefilepath, name + curyear)

    if not os.path.isdir(basefilepath):
        print("Folder structure to save GPX files not found.")
        print("Please run {}\n".format(FILESTRUCTHELPER))
        sys.exit()
    from datetime import date
    yearnow = date.today().year
    if str(yearnow) != curyear:
        print("The year in the settings file: {}".format(curyear))
        print("does not match the current year: {}".format(yearnow))
        print("Please edit your settings file and try again.\n")
        sys.exit()

    return


def makenewfilename(basefilepath, originaldirname, name, curyear):
    """
    generate a filename and path forn the destination GPX file. The
    basename (file name) is then re-used for the preprocessed file
    if it is made.

    """
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.join(basefilepath, name + curyear,
                               originaldirname)

    # look in directory and find latest filename in order to increment
    filelist = os.listdir(gpxfilepath)

    if filelist == []:
        # it might be a new year and the directory is empty
        newnum = '01'
    else:
        lastfile = sorted(filelist)[-1]
        # split last filename and increment number for filename
        filenum = lastfile[lastfile.rfind('-') + 1:]
        filenum = filenum[:filenum.find('.')]
        newnum = '%02d' % (int(filenum) + 1)

    # make user character for filename generation from answer
    userchar = name[0].upper()

    # put it all together and return filepath
    newfilename = "%s-%s-%s.gpx" % (curyear, userchar, newnum)
    newfilepath = os.path.join(gpxfilepath, newfilename)

    return newfilepath


def copygpxfile(tempfilelocation, newfilepath, garminfilelocation):
    """
    copy the gpx file from garmin to a temp location and return the
    file path to it
    """
    newfilename = os.path.basename(newfilepath)
    tempgpxfile = os.path.join(tempfilelocation, newfilename)

    copy2(garminfilelocation, tempgpxfile)

    return tempgpxfile


def savecompress(tempgpxfile, newfilepath):
    """
    compress and save this file to location for 'original' files
    """

    with open(tempgpxfile, 'rb') as tempgpxfileobj:
        with gzip.open(newfilepath + '.gz', 'wb') as compressgpxfile:
            compressgpxfile.writelines(tempgpxfileobj)
    return


def writedatefile(settingspath, name):
    """Write a file with the date

    Stored in human readable format in the 'basefilepath' from settings
    """
    writefilename = name + 'last'
    writefilepath = path.join(settingspath, writefilename)

    with open(writefilepath, 'w') as f:
        f.write("{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    return writefilepath


def appwarn(application):
    """Warn user if there are missing applications"""

    print("**[Warning]**")
    print("An application that this script needs:")
    print(application)
    print("...was not found on your system")
    print()
    print("You will be able to save a compressed copy of the GPX file,")
    if application == "preprocessGPX":
        print("but you will not be able to produce a preprocessed version.")
        print("If you know you have {!s} installed, you may have a PATH".format(application))
        print("problem in the shell you launched from.")
    elif application == "viking":
        print("but you will not be able to view or edit the GPX file.")
    print()

    answer = askyesno("Do you want to continue? [y/n] ")
    if answer:
        return
    else:
        print("Fair enough. Goodbye")
        print()
        sys.exit(0)


def parsepreprocessout(preprocessout):
    """
    strip the output of preprocessGPX, looking for the location of
    the preprocessed file and return it so that viking can open
    this
    """
    preprocessout = preprocessout.split()

    for i in preprocessout:
        if i.endswith('.gpx'):
            return i

    return None


def preprocess(tempgpxfile, newfilepath, preprocessdirname, preprocessbin):
    """
    run preprocessGPX on the copied file
    """
    # prepare the file path for the preprocessed file, this looks
    # elaborate because the '1_original' part of the newfilepath
    # has to be removed before the '2_preprocessed' part can be
    # added
    preprocesslocation = os.path.join(os.path.dirname(os.path.dirname(newfilepath)),
                                      preprocessdirname)

    # capture the output from preprocessGPX
    preprocessout = subprocess.check_output(['python', preprocessbin, tempgpxfile, '-d',
                                             preprocesslocation, '-c'], universal_newlines=True)

    # parse the output into the location of the preprocessed file and return
    preprocessout = parsepreprocessout(preprocessout)

    return preprocessout


def main():
    """
    """
    args = parse_arguments()
    settingspath = path.expanduser(args.settingspath)

    # read settings
    garminfilelocation, curyear, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation,\
        userdict = getsettings(settingspath)
    print()
    print("Loaded settings {}".format(settingspath))
    print()

    # check whether the user has the correct file structure
    checkfilestruct(basefilepath, curyear)

    # get user from dict derived from settings
    user_uid = chooseuser(userdict)
    name = userdict[user_uid]

    garminfilelocation = checkgarminmount(garminfilelocation)
    if not garminfilelocation:
        nogarmin()
    else:
        print("GPS found")
        print()

    # check for the auxiliary programmes this script may need and
    # inform the user if not found. Return the location of the
    # found script for later subprocess calls
    preprocessbin = find_executable("preprocessGPX")
    if not preprocessbin:
        appwarn('preprocessGPX')

    vikingbin = find_executable("viking")
    if not vikingbin:
        appwarn('viking')

    # create the new file path using the various settings and
    # calculated values
    newfilepath = makenewfilename(basefilepath,
                                  originaldirname,
                                  name, curyear)

    print("Saving GPX file from Garmin as a compressed file in {}".format(newfilepath))
    tempgpxfile = copygpxfile(tempfilelocation,
                              newfilepath,
                              garminfilelocation)
    savecompress(tempgpxfile, newfilepath)

    timefilepath = writedatefile(basefilepath, name)
    print("Wrote current time to {}".format(timefilepath))

    if preprocessbin:
        print("Pre-processing and saving a copy in {}".format(preprocessdirname))
        preprocessout = preprocess(tempgpxfile, newfilepath,
                                   preprocessdirname, preprocessbin)

    if vikingbin:
        ans = askyesno("Open the file in Viking? ")
        if ans:
            print("Opening {!s} in Viking...".format(preprocessout))
            subprocess.Popen([vikingbin, preprocessout])

    print("Script ends here - goodbye\n")


if __name__ == '__main__':
    sys.exit(main())
