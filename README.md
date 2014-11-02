# savegpsfiles #

## Save GPX files in specified directory structure ##

Copyright 2014 Daniel Belasco Rogers
Keywords: GPS, GPX, Garmin, file copy, utility

Automate the process of saving new gpx files from a GARMIN etrex.
It checks for the GPS, which should mount at GARMNTPT, looks in the
correct location defined in settings.cfg, finds the number of the
last file, generates a new filename and uses this as the
destination to copy the file from the mount (GARFILEPTH) to the
folder. Then it asks the user if they want to view the file in
viking, if it is on the system.
