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
import gzip
from shutil import copy2, which

__version__ = '0.3'


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

    # if path features tildes, expand these
    basefilepath = os.path.expanduser(basefilepath)
    tempfilelocation = os.path.expanduser(tempfilelocation)

    return garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation


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


def preprocess(tempgpxfile, newfilepath, preprocessdirname):
    """
    run preprocessGPX on the copied file
    """
    preprocesslocation = os.path.join(os.path.dirname
                                      (os.path.dirname(newfilepath)),
                                      preprocessdirname)
    processedfilepath = os.path.join(preprocesslocation,
                                     os.path.basename(newfilepath))
    processedfilepath = "{!s}_pp.gpx".format(os.path.splitext(processedfilepath)[0])


    subprocess.Popen(['preprocessGPX', tempgpxfile, '-d',
                      preprocesslocation, '-c'])

    return


def main():
    """
    """
    settingspath = getsettingspath()
    print()
    print("Loaded settings")

    # read settings
    garminfilelocation, CURYEAR, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation\
        = getsettings(settingspath)

    # checkgarminmount(garminfilelocation)
    print("GPS found")
    print()

    # check for the auxiliary programmes this script may need and
    # inform the user if not found. Return the location of the
    # found script for later subprocess calls
    preprocessbin = checkapplication("preprocessGPX")
    vikingbin = checkapplication("viking")

    name = asksophdan()

    # create the new file path using the various settings and
    # calculated values
    newfilepath = makenewfilename(basefilepath,
                                  originaldirname,
                                  name, CURYEAR)

    # copy the raw GPX file from the Garmin device to a temporary
    # folder
    tempgpxfile = copygpxfile(tempfilelocation,
                              newfilepath,
                              garminfilelocation)

    print()
    print("Saving GPX file from Garmin as a compressed file in {!s}".format(newfilepath))
    savecompress(tempgpxfile, newfilepath)

    if preprocessbin:
        preprocess(tempgpxfile, newfilepath, preprocessdirname)

    # # offer the user the option of opening file in Viking
    # vikingoption(screen, y, x, processedfilepath)


if __name__ == '__main__':
    sys.exit(main())
