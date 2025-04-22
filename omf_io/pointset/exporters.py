import struct

import pandas as pd

import omf
from pathlib import Path

from omf_io.pointset.utils import construct_struct_format
from omf_io.utils.attributes import generate_omf_attributes
from omf_io.utils.decorators import requires_dependency
from omf_io.utils.file import write_omf_element

try:
    import geopandas as gpd
    from shapely.geometry import Point
    import pyvista as pv
except ImportError:
    gpd = None
    Point = None
    pv = None

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import geopandas as gpd  # For type hinting only
    import pyvista as pv


def export_to_csv(data: pd.DataFrame, output_file: Path):
    data.to_csv(output_file, index=True)


def export_to_omf(data: pd.DataFrame, element_name: str, output_file: Path = None) -> Union[Path, omf.PointSet]:
    point_set = omf.PointSet(
        name=element_name,
        vertices=data.index.to_frame(index=False).values
    )
    point_set.attributes = generate_omf_attributes(data)

    if output_file:
        point_set.validate()
        write_omf_element(point_set, output_file, overwrite=True)
        return output_file
    else:
        return point_set


@requires_dependency("GeoPandas", gpd)
def export_to_geopandas(data: pd.DataFrame) -> "gpd.GeoDataFrame":
    """
    Convert a DataFrame with a MultiIndex (x, y, z) to a GeoDataFrame with Point geometries.

    Args:
        data (pandas.DataFrame): The input DataFrame with a MultiIndex (x, y, z).

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame with Point geometries.
    """
    points = [Point(x, y, z) for x, y, z in data.index]
    gdf = gpd.GeoDataFrame(data.reset_index(drop=True), geometry=points)

    return gdf


def export_to_ply(data: pd.DataFrame, output_file: Path, binary: bool = False) -> Path:
    """
    Export points to a PLY file (ASCII or binary).

    Args:
        data (pd.DataFrame): The input DataFrame with a MultiIndex (x, y, z).
        output_file (Path): The output PLY file path.
        binary (bool): Whether to export in binary format. Defaults to False (ASCII).
    """
    if not isinstance(data.index, pd.MultiIndex) or data.index.names != ['x', 'y', 'z']:
        raise ValueError("DataFrame must have a MultiIndex with names ['x', 'y', 'z'].")

    vertices = data.index.to_frame(index=False).values
    attributes = data.reset_index(drop=True)

    with open(output_file, 'wb' if binary else 'w') as f:
        # Write PLY header
        if binary:
            f.write(b"ply\n")
            f.write(b"format binary_little_endian 1.0\n")
            f.write(f"element vertex {len(vertices)}\n".encode())
            f.write(b"property float x\nproperty float y\nproperty float z\n")
            for column in attributes.columns:
                f.write(f"property {attributes[column].dtype.name} {column}\n".encode())
            f.write(b"end_header\n")
        else:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(vertices)}\n")
            f.write("property float x\nproperty float y\nproperty float z\n")
            for column in attributes.columns:
                f.write(f"property {attributes[column].dtype.name} {column}\n")
            f.write("end_header\n")

        # Write vertex data
        if binary:
            struct_format = construct_struct_format(
                {'x': 'float', 'y': 'float', 'z': 'float', **attributes.dtypes.to_dict()})
            for vertex, row in zip(vertices, attributes.itertuples(index=False)):
                f.write(struct.pack(struct_format, *vertex, *row))
        else:
            for vertex, row in zip(vertices, attributes.itertuples(index=False)):
                f.write(" ".join(map(str, vertex)) + " " + " ".join(map(str, row)) + "\n")

    return output_file


@requires_dependency("pyvista", "pv")
def export_to_pyvista(data: pd.DataFrame) -> "pv.PolyData":
    """
    Convert a pandas DataFrame with a MultiIndex to a PyVista PolyData object.

    Args:
        data (pd.DataFrame): The input DataFrame with a MultiIndex (x, y, z).

    Returns:
        pv.PolyData: A PyVista PolyData object representing the point cloud.
    """
    if not isinstance(data.index, pd.MultiIndex) or data.index.names != ["x", "y", "z"]:
        raise ValueError("DataFrame must have a MultiIndex with levels ['x', 'y', 'z'].")

    # Extract coordinates from the MultiIndex
    points = data.index.to_frame(index=False).values

    # Create a PyVista PolyData object
    polydata = pv.PolyData(points)

    # Add attributes as point data
    for column in data.columns:
        # Check if the column contains tuples and convert them to strings
        if data[column].apply(lambda x: isinstance(x, tuple)).any():
            polydata.point_data[column] = data[column].apply(str).values
        else:
            polydata.point_data[column] = data[column].values
    return polydata
