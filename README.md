# omf-io

This package provides a simple interface to read and write OMF files using the [Open Mining Format package (omf)](https://omf.readthedocs.io/en/latest/).

The aim of the package is to "Democratise the OMF format" - reducing the barrier to entry for python users to adopt OMF,
by enabling conversion of existing data into and out of OMF files. This could be for tabular block models, raster files, or any other OMF element.

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
