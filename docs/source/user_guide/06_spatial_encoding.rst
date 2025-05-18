Spatial Encoding
================

Spatial encoding of coordinates and dimensions allows encoding a coordinate ``(x, y, z)`` or a
dimension ``(dx, dy, dz)`` into a single value. This is useful is cases where a unique id is required that
can be decodes to the original coordinates or dimensions.

.. note::
   This is not part of the OMF specification, but a convention adopted by this package to make it easier to
   work with coordinates and dimensions.

The encoding is done using bitwise operations to pack the coordinates or dimensions into a single integer.

Coordinate encoding
-------------------

Coordinate encoding generates a 64 bit integer with the following formula:

``encoded_coordinate_value = (x << 40) | (y << 16) | z``

The values are shifted to the left by the number of bits required to represent the other values.
For example, if ``x`` and ``y`` are both 24 bits, then ``x`` is shifted by 40 bits (24 + 16),
``y`` is shifted by 16 bits and ``z`` is not shifted.

The allocation of bits is as follows:

- 24 bits for ``x``
- 24 bits for ``y``
- 16 bits for ``z``

By limiting floating point values to a limited number of decimal places, we can increase the
maximum value for each coordinate.  This implementation limits the number of decimal places to 1.

For x and y coordinates, the maximum value is 16,777,215 (2^24 - 1), which corresponds to
1,677,721.5 in floating point ((2^24 - 1) / 10).

For z coordinates, the maximum value is 65,535 (2^16 - 1), which corresponds to 6,553.5 in floating
point ((2^16 - 1) / 10).

The specification can be summarised as follows:

.. list-table:: Coordinate Encoding Specification
   :header-rows: 1

   * - Coordinate
     - Bits
     - Minimum
     - Maximum
     - Decimal Places
   * - x
     - 24
     - 0
     - 1,677,721.5
     - 1
   * - y
     - 24
     - 0
     - 1,677,721.5
     - 1
   * - z
     - 16
     - 0
     - 6,553.5
     - 1

This result in a 64 bit integer, which when decoded will be converted back to the original
coordinates.

Dimension encoding
------------------

Dimension encoding creates a 32 bit integer with the following formula:

``encoded_dimension_value = (dx << 20) | (dy << 10) | dz``

.. list-table:: Dimension Encoding Specification
   :header-rows: 1

   * - Dimension
     - Bits
     - Minimum
     - Maximum
     - Decimal Places
   * - dx
     - 10
     - 0
     - 102.3
     - 1
   * - dy
     - 10
     - 0
     - 102.3
     - 1
   * - dz
     - 10
     - 0
     - 102.3
     - 1

The result is a 32 bit integer, which when decoded will be converted back to the original
dimensions.

Out of Range Coordinates
------------------------

The specification does not allow for negative coordinates or dimensions.  If a coordinate or dimension is out of range,
the encoding will fail with a ``ValueError``.  This is to prevent the encoding of invalid values.

It is unlikely that a block dimension will be out of range, but it is possible that a coordinate can be out of range.
This can happen when using coordinate systems that cover large areas.  While the typical use case for a mining
operator will be to use a local coordinate system, it is possible that a coordinate system
is used that covers a large area.  In this case, the coordinate system will be out of range.

We deal with out of range coordinates using offsets.  The offset is added to the coordinate before encoding.
This allows the encoding to succeed, but the offset must be subtracted from the coordinate after decoding.

To assist with this, the ``CoordinateEncoding`` class has an ``offset`` property that can be used to set the offset.
The class is supported by a configuration file that can be used to set the offset.
