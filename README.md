# omf-io

This package provides a simple interface to read and write OMF files using the [Open Mining Format package (omf)](https://omf.readthedocs.io/en/latest/).

The aim of the package is to **Enable OMF adoption in the Python ecosystem** - reducing the barrier to entry for Python users to adopt OMF.

OMF-IO enables conversion of existing data into and out of OMF files. This could be for tabular block models, raster files, or any other OMF element.

Use cases include:

- **OMF Creation**: OMF-IO can be used to create OMF files from existing data. This is useful for users who want to create OMF files from scratch or for users who want to convert existing data into OMF format.
- **Export from OMF**: OMF-IO can be used to export OMF files into other formats. This is useful for users who want to share their OMF data with others who may not be using OMF, or for users who want to convert their OMF data into a different format for use in other applications.
- **Adhoc Conversion**: OMF-IO can be used to convert data between different formats. This is useful for users who want to convert their data into a different format for use in other applications, which need not be OMF.

![OMF-IO Animation](https://raw.githubusercontent.com/elphick/omf-io/4-document-supported-formats/docs/source/_static/omf_io_animation.gif)

## Installation

```bash
pip install omf-io
```

## Usage

```python
from pathlib import Path
from omf_io.gridsurface.grid_surface import GridSurfaceIO

# Importing data
grid_surface = GridSurfaceIO.from_raster(Path("input_raster.tif"))

# Exporting data
grid_surface.to_raster(Path("output_raster.tif"))
```
