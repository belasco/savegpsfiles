#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""savecurrentgps.py
Daniel Belasco Rogers dan@planbperformance.net

Wed 15 Jul 2015 17:38:21 CEST

Re-writing ncurses-based script to take back to bare essentials.
Command line only with functions that could then be called by a gui
if I build one later.

"""

import sys
import os
import subprocess
import configparser
import argparse
import gzip
from shutil import copy2, which
from os import path

__version__ = '0.4'


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
    CURYEAR = config.get('core', 'currentyear')
    garminfilelocation = config.get('core', 'garminfilelocation')
    basefilepath = config.get('core', 'basefilepath')
    originaldirname = config.get('core', 'originaldirname')
    preprocessdirname = config.get('core', 'preprocessdirname')
    tempfilelocation = config.get('core', 'tempfilelocation')
    userlist = config.options('users')
    userdict = {}
    for key in userlist:
        userdict[key] = config.get('users', key)

    # if path features tildes, expand these
    basefilepath = os.path.expanduser(basefilepath)
    tempfilelocation = os.path.expanduser(tempfilelocation)

    return garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation, userdict


def getsettingspath():
    """
    find settings in current dir of this script and capture non
    existence- this location may change
    """
    curdir = os.path.dirname(__file__)
    settingspath = os.path.expanduser(os.path.join(curdir, 'settings.cfg'))

    if not os.path.exists(settingspath):
        print("Error: Settings file not found at %s" % settingspath)
        print()
        sys.exit(2)

    return settingspath


def checkgarminmount(garminfilelocation):
    """
    Look for the Garmin mounted at the location set in the settings
    config file and notify the user if it is not there.
    """
    if not os.path.exists(garminfilelocation):
        print("Error:")
        print("No GPS found at %s" % garminfilelocation)
        print()
        print("Check that the GPS is plugged in")
        print("and has finished making GPX file")
        print("then try again.")
        print()
        sys.exit(2)

    return


def asksophdan():
    """
    ask the user whether this is Soph's GPS or Dan's and return the
    answer as 'name'
    """
    name = ""

    while 1:
        name = input("Is this Soph's GPS or Dan's [s/d]? ")
        name = name.lower()
        if name == 's':
            return 'soph'
        elif name == 'd':
            return 'dan'
        elif name == 'q':
            print("You pressed q for Quit... Goodbye")
            print()
            sys.exit()
        else:
            print("Please answer 's' or 'd' for Soph or Dan...")
            print()


def makenewfilename(basefilepath, originaldirname, name, CURYEAR):
    """
    generate a filename and path for the destination GPX file. The
    basename (file name) is then re-used for the preprocessed file
    if it is made.

    """
    # find location of current GPS files on user's machine
    gpxfilepath = os.path.join(basefilepath, name + CURYEAR,
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
    newfilename = "%s-%s-%s.gpx" % (CURYEAR, userchar, newnum)
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


def askyesno(question):
    """
    Ask a yes or no question. Loop until the answer is returned.
    Answering 'q' quits the programme
    """
    while 1:
        answer = input(question).lower()
        if answer in ('y', 'yes'):
            answer = True
        elif answer in ('n', 'no'):
            answer = False
        elif answer == 'q':
            print("You pressed q for Quit... Goodbye")
            print()
            sys.exit()
        return answer

        print('Please answer y or n')
    return


def checkapplication(application):
    """
    Look for an application and inform the user if not found. This
    is run on preprocessGPX and viking. There are slightly
    different comments for the case that each is not found.

    """
    checkapp = which(application)

    if checkapp:
        return checkapp
    else:
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

    return


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
    preprocessout = subprocess.check_output([preprocessbin, tempgpxfile, '-d',
                                             preprocesslocation, '-c'], universal_newlines=True)

    # parse the output into the location of the preprocessed file and return
    preprocessout = parsepreprocessout(preprocessout)

    return preprocessout


def openviking(vikingbin, filetoopen):
    """ask to open the file in viking"""
    ans = askyesno("Open the file in Viking? ")

    if ans:
        print("Opening {!s} in Viking...".format(filetoopen))
        subprocess.Popen([vikingbin, filetoopen])

    return


def main():
    """
    """
    args = parse_arguments()
    settingspath = path.expanduser(args.settingspath)

    # read settings
    garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation,\
        userdict = getsettings(settingspath)
    print()
    print("Loaded settings")
    print(garminfilelocation, CURYEAR, basefilepath,
          originaldirname, preprocessdirname, tempfilelocation, userdict)

    # checkgarminmount(garminfilelocation)
    # print("GPS found")
    # print()

    # # check for the auxiliary programmes this script may need and
    # # inform the user if not found. Return the location of the
    # # found script for later subprocess calls
    # preprocessbin = checkapplication("preprocessGPX")
    # vikingbin = checkapplication("viking")

    # name = asksophdan()

    # # create the new file path using the various settings and
    # # calculated values
    # newfilepath = makenewfilename(basefilepath,
    #                               originaldirname,
    #                               name, CURYEAR)

    # print("Saving GPX file from Garmin as a compressed file in {!s}".format(newfilepath))
    # print()

    # tempgpxfile = copygpxfile(tempfilelocation,
    #                           newfilepath,
    #                           garminfilelocation)

    # savecompress(tempgpxfile, newfilepath)

    # if preprocessbin:
    #     print("Pre-processing and saving a copy in {!s}".format(preprocessdirname))
    #     print()
    #     preprocessout = preprocess(tempgpxfile, newfilepath,
    #                                preprocessdirname, preprocessbin)
    #     if vikingbin:
    #         openviking(vikingbin, preprocessout)

    # elif vikingbin:
    #     openviking(vikingbin, tempgpxfile)

    print("Script ends here - goodbye")
    print()


if __name__ == '__main__':
    sys.exit(main())
