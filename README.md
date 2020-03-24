# savegpsfiles #

## Save GPX files in specified directory structure ##

Copyright 2014, 2020 Daniel Belasco Rogers
Keywords: GPS, GPX, Garmin, file copy, utility

Automate the process of saving new gpx files from a GARMIN etrex
using a simple ncurses interface.

The main script is `savecurrentUI.py` which is an ncurses wrapper
around `savecurrentgps.py` I symlink this in my `~/bin` directory
which is in my PATH. savecurrentgps loads settings from the file
`settings.cfg` This file contains the locations to look for where
the GPS is mounted to and the folders to expect to save files to.
If this settings file is missing, running `archive_makefolders.py`
will create it. See the global variable CONFIGPATH in `__init__.py`
which defines the default location for this.

The main script checks for the GPS, which should have been mounted
at GARMNTPT by the system, finds the number of the last file
(usually in `1_original` defined in settings.cfg), generates a new
filename and uses this as the destination to copy the file from the
mount (GARFILEPTH) to the folder. In the background it compresses
this original file straight off the GPS by copying the gpx file
from the Garmin device to a temporary folder and zipping it (with
gzip) before moving it into the archive (`1_original`) directory.

It also uses the related script
[gpxprocessing](https://github.com/belasco/gpxprocessing) if
present on the system, to save a stripped down version of the
original file to the `2_preprocessed` directory. See that script
for details. Then it asks the user if they want to view/edit the
file in [viking](https://sourceforge.net/projects/viking/), if it
is on the system.

The utility script `archive_makefolders.py` with no arguments moves
the current lot of GPS files into an archive location and creates a
new structure using our defaults of two users ('dan' and 'soph') having
three sub-folders in each user folder as follows:
```
currentGPS/
├──   dan2015
│   ├──   1_original
│   ├──   2_preprocessed
│   └──   3_cleaned
└──   soph2015
    ├──   1_original
    ├──   2_preprocessed
    └──   3_cleaned
```
