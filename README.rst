acsearch
========

Python implementation of the Aho-Corasick string search algorithm.

Usage
-----

Build a dictionary from a list of words::

    >>> from acsearch import ACDictionary
    >>> acd = ACDictionary(["foo", "bar", "aria"])

Find all dictionary matches in a given string in linear time::

    >>> acd.findall("barbarian")
    ['bar', 'bar', 'aria']

Testing
-------

To run the tests, install ``nose`` and then run::

    nosetests acsearch
