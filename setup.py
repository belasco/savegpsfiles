#!/usr/bin/env python2
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

from savecurrentgps import __version__


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(name='savecurrentgps',
      description='savecurrentgps',
      long_description=readme(),
      author='Daniel Belasco Rogers',
      author_email='danbelasco@yahoo.co.uk',
      # url='https://github.com/belasco/savecurrentgps',
      # download_url='https://github.com/ptrv/gpx2spatialite',
      version=__version__,
      py_modules=['savecurrentgps'],
      install_requires=['viking', 'preprocessGPX'],
      license='GPLv3')
