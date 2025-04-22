from typing import Union

import omf
import pandas as pd
from pathlib import Path

from omf_io.pointset.importers import import_from_csv, import_from_omf
from omf_io.pointset.exporters import export_to_csv, export_to_omf

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd  # For type hinting only


class PointSetIO:
    """
    Handles the creation and consumption of PointSet objects with attributes.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the PointSetIO instance.

        Args:
            data (pandas.DataFrame): The point set data with a MultiIndex (x, y, z) and attribute columns.
        """
        if not isinstance(data.index, pd.MultiIndex) or data.index.names != ['x', 'y', 'z']:
            raise ValueError("Data must have a MultiIndex with levels ['x', 'y', 'z'].")
        self.data = data

    @classmethod
    def from_csv(cls, file_path: Path) -> "PointSetIO":
        """
        Load a PointSetIO instance from a CSV file.

        Args:
            file_path (Path): The path to the CSV file.

        Returns:
            PointSetIO: An instance of the class.
        """

        data = import_from_csv(file_path)
        return cls(data)

    @classmethod
    def from_omf(cls, omf_input: Union[Path, omf.Project], pointset_name: str) -> "PointSetIO":
        """
        Create a PointSetIO instance from an OMF file or project object.

        Args:
            omf_input (Union[Path, omf.Project]): The input OMF file path or project object.
            pointset_name (str): The name of the PointSet element to extract.

        Returns:
            PointSetIO: An instance of the class.
        """
        data = import_from_omf(omf_input, pointset_name)
        return cls(data)

    @classmethod
    def from_geopandas(cls, gdf: "gpd.GeoDataFrame") -> "PointSetIO":
        """
        Create a PointSetIO instance from a GeoDataFrame.

        Args:
            gdf (geopandas.GeoDataFrame): The input GeoDataFrame with Point geometries.

        Returns:
            PointSetIO: An instance of the class.
        """
        from omf_io.pointset.importers import import_from_geopandas
        data = import_from_geopandas(gdf)
        return cls(data)

    @classmethod
    def from_ply(cls, input_file: Path) -> "PointSetIO":
        """
        Create a PointSetIO instance from a PLY file.

        Args:
            input_file (Path): The input PLY file path.

        Returns:
            PointSetIO: An instance of the class.
        """
        from omf_io.pointset.importers import import_from_ply
        data = import_from_ply(input_file)
        return cls(data)

    def to_csv(self, output_file: Path) -> Path:
        """
        Export the PointSet data to a CSV file.

        Args:
            output_file (Path): The output CSV file path.
        """
        export_to_csv(self.data, output_file)
        return output_file

    def to_omf(self, element_name: str = 'point_set', output_file: Path = None) -> Union[Path, omf.PointSet]:
        """
        Convert the PointSet data to an OMF PointSet, including attributes.

        Args:
            element_name (str): The name of the PointSet element.
            output_file (Path, optional): The file path to save the OMF PointSet.

        Returns:
            omf.PointSet: The OMF PointSet object (if output_file is not provided).
        """
        return export_to_omf(self.data, element_name, output_file)

    def to_geopandas(self) -> "gpd.GeoDataFrame":
        """
        Convert the PointSetIO data to a GeoDataFrame.

        Returns:
            geopandas.GeoDataFrame: A GeoDataFrame with Point geometries.
        """
        from omf_io.pointset.exporters import export_to_geopandas
        return export_to_geopandas(self.data)

    def to_ply(self, output_file: Path, binary: bool = False) -> Path:
        """
        Export the PointSet data to a PLY file.

        Args:
            output_file (Path): The output PLY file path.
            binary (bool): Whether to export in binary format. Defaults to False (ASCII).
        """
        from omf_io.pointset.exporters import export_to_ply
        return export_to_ply(self.data, output_file, binary)
