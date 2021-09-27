#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  
from os import path
import io

NAME = 'news_scraper'


setup(
    name=NAME,
    version=0.1,
    description=('This is a schedulable console app which scrapes'
        +' the news feed of a given news source, saves the data, '
        +'and updates it with the corresponding timestamp',)
    author='Eren Keşküş',
    author_email='eren01@gmail.com',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    # TODO
    keywords='scrape article magazine',
    packages=find_packages(exclude=['contrib', 'docs']),
    install_requires=[],
    scripts=[],
    test_suite='tests',
)

