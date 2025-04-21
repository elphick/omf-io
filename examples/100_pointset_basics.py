"""
PointSetIO Basics
=================

This example demonstrates the basic usage of the PointSetIO class.

"""

import tempfile
from pathlib import Path

import pandas as pd

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
# Persist a PointSet
# ------------------
# Persist the head of the point set to various file formats.

point_data: pd.DataFrame = pointset_io.data.head(10)
out_filepath: Path = Path(tempfile.gettempdir()) / 'pointset_data.csv'
PointSetIO(data=point_data).to_csv(out_filepath)

# %%
PointSetIO(data=point_data).to_omf(element_name='collar_top_10',
                                   output_file=out_filepath.with_suffix('.omf'))

# %%
# View the OMF elements
# ---------------------

omfr: OMFReader = OMFReader(filepath=out_filepath.with_suffix('.omf'))
omfr.element_types
