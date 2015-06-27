#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py
2014/04/10 20:17:29

Copyright 2014 Daniel Belasco Rogers danbelasco@yahoo.co.uk
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(name='savecurrentgps',
      author='Daniel Belasco Rogers',
      author_email='danbelasco@yahoo.co.uk',
      version='1.0',
      py_modules=['savecurrentgps'],
      long_description=readme(),
      description='Copy the current gpx file from a Garmin Etrex \
into the directory in settings.cfg',
      license='GPLv3')
