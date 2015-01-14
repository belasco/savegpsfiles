# savegpsfiles #

## Save GPX files in specified directory structure ##

Copyright 2014 Daniel Belasco Rogers
Keywords: GPS, GPX, Garmin, file copy, utility

Automate the process of saving new gpx files from a GARMIN etrex
using a simple ncurses interface.

Using settings from the file settings.cfg, the script checks for
the GPS, which should mount at GARMNTPT, finds the number of the
last file (location also defined in settings.cfg), generates a new
filename and uses this as the destination to copy the file from the
mount (GARFILEPTH) to the folder. In the background it copies the
gpx file from the Garmin device to a temporary folder and zips it
before moving it into the correct (1_original) directory.

Then it asks the user if they want to view/edit the file in viking,
if it is on the system.

The utility script GPSfilestruct.sh creates the expected file
structure using our defaults of two users ('dan' and 'soph') having
three subfolders in each user folder as follows, where YYYY is the
year in four figures (i.e. 2015):
<pre>
currentGPS/
├──   dan2015
│   ├──   1_original
│   │   └──   2015-D-01.gpx.gz
│   ├──   2_preprocessed
│   │   └──   2015-D-01_pp.gpx
│   └──   3_cleaned
└──   soph2015
    ├──   1_original
    ├──   2_preprocessed
    └──   3_cleaned
</pre>
