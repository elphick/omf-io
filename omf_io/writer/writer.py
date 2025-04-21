import numpy as np
import pandas as pd

from omf_io.base import PathLike
from omf_io.reader import OMFReader


class OMFWriter(OMFReader):
    """A class to write elements to an OMF file.
    """

    def __init__(self, filepath: PathLike):
        """Instantiate the OMFPandasWriter object.

        Args:
            filepath (Path): Path to the OMF file.
        """
        OMFReader.__init__(self, filepath)


    def write_raster_from_file(self, raster_file: PathLike, name: str, **kwargs):
        """Load a raster from a file into an OMF GridSurface object.

        Args:
            raster_file (PathLike): Path to the raster file (e.g., GeoTIFF).
            name (str): The name of the raster.
            **kwargs: Additional keyword arguments.
        """
        pass

    def write_raster_from_array(self, array: np.ndarray, name: str, **kwargs):
        """Load a raster from a numpy array into an OMF GridSurface object.

        Args:
            array (np.ndarray): The raster as a numpy array.
            name (str): The name of the raster.
            **kwargs: Additional keyword arguments.
        """
        pass

    def write_blockmodel_from_file(self, blockmodel_file: PathLike, name: str, **kwargs):
        """Load a blockmodel from a file into an OMF BlockModel object.

        Args:
            blockmodel_file (PathLike): Path to the blockmodel file.
            name (str): The name of the blockmodel.
            **kwargs: Additional keyword arguments.
        """
        pass

    def write_blockmodel_from_dataframe(self, df: pd.DataFrame, name: str, **kwargs):
        """Load a blockmodel from a pandas DataFrame into an OMF BlockModel object.

        Args:
            df (pd.DataFrame): The blockmodel as a pandas DataFrame.
            name (str): The name of the blockmodel.
            **kwargs: Additional keyword arguments.
        """
        pass