Block Models
============

Block Models are a way to represent 3D data in a grid format and can be represented by various types.

The simplest type is the ``RegularBlockModel``, which is a regular grid of blocks.

.. todo:: Build out the documentation for the blockmodel classes and io

Tabular Block Models
--------------------

While block models are typically represented in a 3D grid format, they can also be represented in a tabular format.
Each row in the table represents a block, and the columns represent the properties of that block.
Packages like ``pandas`` are well suited to this type of representation.

The ``polars`` package is also a good option for this type of representation, particularly for larger datasets.

Persistence of tabular data (outside the omf format) is typically done using the ``parquet`` format.
This format is efficient for both storage and retrieval, and is well supported by both ``pandas`` and ``polars``.
In fact, parquet is the underlying format for ``omf2``.