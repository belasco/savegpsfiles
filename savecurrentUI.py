#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
savecurrentUI.py
2017/12/24 13:47:20

An attempt to build an ncurses UI for savecurrentgps

Copyright 2017 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys
import curses
from savecurrentgps import parse_arguments, getsettings


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


def chooseuser(userdict, maxyx):
    """
    using the user dictionary from the settings file, ask who's GPS
    this is
    """
    margin = 4  # padding all round window
    userwin = curses.newwin(maxyx[0] - margin * 2,
                            maxyx[1] - margin * 2, margin, margin)
    userwin.box()

    line = 2  # running total of what line we're on
    msg = "Please choose who this GPS belongs to from the list below:"
    userwin.addstr(line, margin, msg)

    line += 2
    tab = margin + 4
    for idx, key in enumerate(sorted(userdict.keys())):
        msg = "{}:  {}".format(key, userdict[key])
        userwin.addstr(line, tab, msg)
        line += 1

    msg = "Enter a number from 1 to {} > ".format(len(userdict))
    line += 1
    userwin.addstr(line, margin, msg)

    userwin.refresh()

    while 1:
        user_uid = userwin.getch()
        line += 1
        if user_uid == ord('q'):
            curses.endwin()
            print("User entered Q for Quit. Script ends here.")
            sys.exit()
        elif user_uid not in userdict.keys():
            msg = "That number is not in use. Please enter another. "
            userwin.addstr(line, margin, msg)
            

        # user_uid = input("Enter a number from 1 to {} > ".format(len(userdict)))
        # user_uid = int(user_uid)
        # if user_uid in userdict.keys():
        #     # confirm the selection
        #     print()
        #     ans = askyesno('You selected {}. Is this correct? '.format(userdict[user_uid]))
        #     if ans:
        #         return user_uid
        #     else:
        #         print('Please run the script again to select the correct user')
        #         print('Script ends here\n')
        #         sys.exit()

        # elif user_uid.lower() == 'q':
        #     print("You pressed q for Quit... Goodbye")
        #     print
        #     sys.exit()

        # print('Your entry was not valid. Please try again.')


def initscreen(myscreen):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)

    myscreen.bkgd(curses.color_pair(1))
    myscreen.border(0)
    myscreen.refresh()


def main(myscreen):
    """
    """
    initscreen(myscreen)
    maxyx = myscreen.getmaxyx()

    args = parse_arguments()

    # read settings
    garminfilelocation, curyear, basefilepath,\
        originaldirname, preprocessdirname, tempfilelocation,\
        userdict = getsettings(args.settingspath)

    # get user from dict derived from settings
    user_uid = chooseuser(userdict, maxyx)
    name = userdict[user_uid]


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Got KeyboardInterrupt exception. Exiting...")
        exit()
