#! /bin/bash

# Create a currentGPS directory structure in location supplied as a
# first argument. Second argument is the year required i.e. the
# current year or next year.

version="0.1"
user1="dan"
user2="soph"

usemessage(){
    # see here for why printf is better than echo
    # http://stackoverflow.com/questions/10576571/how-to-make-echo-interpret-backslash-escapes-and-not-print-a-trailing-newline
    printf "\nCreate a directory structure to save GPX files in\n"
    printf "Usage: $0 path year\n"
    printf "Where path is the directory to make the file structure in\n"
    printf "(currently this is selectedplanbfiles/currentGPS)\n"
    printf "and year is the (current or next) year in question\n\n"
}

if [ "$1" = "-h" ];
then
    usemessage
    exit 1
elif [ "$1" = "-v" ];
then
    printf $version
    printf "\n"
    exit 1
elif [ $# -ne 2 ];
then
    printf "\nError: not enough arguments\n"
    usemessage
    exit 1
fi

makestruct(){
    cd $1
    mkdir 1_original
    mkdir 2_preprocessed
    mkdir 3_cleaned
    cd ../
}

# make the directory structure in the location supplied by the
# first arg
if [ ! -d $1 ];  # only make it if it isn't already there
then
    mkdir $1/currentGPS
fi
cd $1/currentGPS

if [ -d $user1$2 ];  # check we haven't already done this!
then
    printf "\nIt looks like there is already a file structure for this year\n"
    printf "Please check and try again if necessary.\n\n"
    exit 1
fi

# finally make the user folders and the same structure within each
mkdir $user1$2
makestruct $user1$2
mkdir $user2$2
makestruct $user2$2

printf "\nSuccessfully created file structure in $1/currentGPS"
