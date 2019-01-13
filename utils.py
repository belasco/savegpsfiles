#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utils.py
2019/01/13 17:57:15


Copyright 2019 Daniel Belasco Rogers dan@planbperformance.net
"""

import sys


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
