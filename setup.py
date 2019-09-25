#!/usr/bin/env python

from distutils.core import setup

setup(name='Git Migrator',
      version='1.0',
      description='Simple Chat Server and Client',
      author='Ryan Thompson',
      author_email='ryan.thompson@foghornconsulting.com',
      url='',
      packages=['migrator'],
      entry_points={
          'console_scripts': ['migrator=migrator.command_line:main'],
      }
      )
