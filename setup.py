#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  
from os import path
import io

NAME = 'news_scraper'


setup(
    name=NAME,
    version=0.1,

    # TODO
    description='',

    # Author details
    author='',
    author_email='',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    # TODO
    keywords='',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs']),

    install_requires=[],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest', 'nose'],
        'test': ['coverage', 'nose'],
    },
    # TODO
    # entry_points={
    #     'console_scripts': [
    #         ' =  '
    #     ]
    # },
    # TODO 
    scripts=[],
    test_suite='tests',
)

