Points
======

Points are managed in OMF by the ``PointSet`` class.  A ``PointSet`` is a collection of points, each of which
has associated attributes.

In the mining context, points are often used to represent hole collars.  A collection of hole collars
is represented by a ``PointSet``.  An attribute for a hole collar pointset might be the hole name, or the
depth of the hole.

The ``PointSetIO`` class helps manage conversions between formats, including to and from OMF.

.. code-block:: python
   :linenos:

   from omf_io.pointset import PointSetIO

   # Read a PointSet from an OMF file
   pointset_io: PointSetIO = PointSetIO.from_omf("example.omf", "my_pointset")

   # Read a Pointset from a csv file
   pointset_io: PointSetIO = PointSetIO.from_csv("example.csv", "my_pointset")

   # Write a PointSet to an OMF file
   PointSetIO.to_omf(pointset_io, "example.omf", "my_pointset")

   # Write a PointSet to a csv file
   PointSetIO.to_csv(pointset_io, "example.csv", "my_pointset")