# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup

setup(name="mouselog",
      version="0.1.0",
      description="Record how far your mouse has travelled, or log movement",
      url="https://github.com/xyproto/mouselog",
      author="Alexander F. Rødseth",
      author_email="xyproto@archlinux.org",
      license="GPLv2",
      py_modules=["mouselog"],
      entry_points={
        "console_scripts" : [
            "mouselog = mouselog:main",
        ]
      },
      classifiers=[
          "Environment :: Console",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Programming Language :: Python",
          "Topic :: System :: Shells",
          "Topic :: Utilities",
      ]
)
