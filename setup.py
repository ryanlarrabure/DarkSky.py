#!/usr/bin/env python

from distutils.core import setup

setup(
    name='DarkSky',
    version='0.1',
    author='Ryan Larrabure',
    author_email='ryan@larrabure.org',
    url='http://www.github.com/ryan/DarkSky.py/',
    packages=['darksky', 'darksky.abstract_io'],
    package_dir= {'darksky': 'src/darksky'},
    install_requires=['requests']
)
        
