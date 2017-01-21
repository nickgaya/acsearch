#! /usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='acsearch',
    version='1.0',
    description="Aho-Corasick search implementation",
    author="Nicholas Gaya",
    url="nickgaya.wordpress.com",
    packages=find_packages(),
    setup_requires=[
        'nose>=1.0',
    ],
    test_suite='nose.collector',
)
