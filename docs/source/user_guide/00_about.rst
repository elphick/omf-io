About this package
==================

This package is a Python library for reading and writing OMF files. The objective is to to
reduce barrier to entry for users who are not familiar with OMF, and to provide a simple interface
to the OMF file format.

Delivery over perfection
------------------------

The idea is that the conversions into and out of the omf format are delivered by leveraging existing packages,
at least in the first instance.  We will still try to provide the user with a low-dependency pathway with the use of extras.
There is a trade off between the number of dependencies and speed / ease of development.  We will prioritise
functionality over dependency minimisation initially, but can re-balance down the track.

Agility
-------

Let's try to be agile.  We will try to deliver the package in a way that is easy to use and easy to extend.
To this end we will use the python package ``omf==2.0.0a0`` in the first instance.  Once the rust backed
python package ``omf2`` is available we will switch to that.

Documentation
-------------

In this project we will write many of the documentation first, to help define the scope.  Sphinx has
been used to generate the documentation.

Testing
-------

We aim for coverage > 90% using ``pytest``.