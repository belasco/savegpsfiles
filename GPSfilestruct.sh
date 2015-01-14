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
    printf "Usage: $0 location year\n"
    printf "Where location is the directory to make the file structure in\n"
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
mkdir $1/currentGPS
cd $1/currentGPS
mkdir $user1$2
mkdir $user2$2
makestruct $user1$2
makestruct $user2$2
