"""
PointSetIO Basics
=================

This example demonstrates the basic usage of the PointSetIO class.

"""

import tempfile
from pathlib import Path

import pandas as pd
import geopandas as gpd

from omf_io.pointset import PointSetIO
from omf_io.reader import OMFReader

# %%
# Load a PointSet
# ---------------
# Load a point set from a OMF file

pointset_io: PointSetIO = PointSetIO.from_omf(omf_input=Path('../assets/copper_deposit.omf'),
                                              pointset_name='collar')

pointset_io.data.head(10)

# %%
# Demonstrate conversions
# -----------------------
# Exercise the PointSetIO class with various conversions

# %%
# CSV file
# ~~~~~~~~

point_data: pd.DataFrame = pointset_io.data.head(10)
out_filepath: Path = Path(tempfile.gettempdir()) / 'pointset_data.csv'
csv_filepath: Path = PointSetIO(data=point_data).to_csv(out_filepath)

# read and print the csv
csv_point_data = pd.read_csv(csv_filepath)
csv_point_data

# %%
# Geodataframe object
# ~~~~~~~~~~~~~~~~~~~

gdf: gpd.geodataframe = PointSetIO(data=point_data).to_geopandas()
gdf

# %%
# PLY file
# ~~~~~~~~

ply_filepath: Path = PointSetIO(data=point_data).to_ply(out_filepath.with_suffix('.ply'), binary=False)

# read and print the PLY using file.open
with ply_filepath.open('r') as f:
    ply_data = f.readlines()
print(''.join(ply_data))

# %%
# OMF file
# ~~~~~~~~

omf_filepath: Path = PointSetIO(data=point_data).to_omf(element_name='collar_top_10',
                                                        output_file=out_filepath.with_suffix('.omf'))
# %%
# View the OMF elements

omfr: OMFReader = OMFReader(filepath=out_filepath.with_suffix('.omf'))
omfr.element_types
