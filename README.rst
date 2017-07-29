xmlparser
---------

Installation:
=============

``python setup.py install``

Usage:
======

``xmlparser generate`` command creates zip-archives (50 by default)
with xml files (100 per archive by default).


``xmlparser generate ~/sample-dir``

``xmlparser parse`` command processes given directory: opens zip-archives
and parses xml-files. The information obtained will be stored in .csv files
(./id_level.csv and ./id_objects.csv by default).


``xmlparser parse ~/sample-dir``

More information about CLI:
===========================

``xmlparser <command> --help``

