import ast
import struct
from typing import Union

import pandas as pd
import omf
from pathlib import Path

from omf_io.pointset.utils import construct_struct_format, calculate_struct_size
from omf_io.utils.decorators import requires_dependency

try:
    import geopandas as gpd
except ImportError:
    gpd = None

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd  # For type hinting only


def import_from_csv(file_path: Path) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path, index_col=[0, 1, 2])
    except IndexError:
        raise ValueError("CSV file must have at least three columns for x, y, and z coordinates.")
    data.index.names = ['x', 'y', 'z']
    if 'holeid_color' in data.columns:
        data['holeid_color'] = data['holeid_color'].apply(ast.literal_eval)
    return data


def import_from_omf(omf_input: Union[Path, omf.Project], pointset_name: str) -> pd.DataFrame:
    if isinstance(omf_input, Path):
        project = omf.load(str(omf_input))
    elif isinstance(omf_input, omf.Project):
        project = omf_input
    else:
        raise TypeError("omf_input must be a Path or an omf.Project object.")

    pointset = next(
        (element for element in project.elements if
         element.name == pointset_name and isinstance(element, omf.PointSet)),
        None
    )
    if not pointset:
        raise ValueError(f"PointSet with name '{pointset_name}' not found in the OMF project.")

    vertices = pd.DataFrame(pointset.vertices.array, columns=['x', 'y', 'z'])
    vertices.set_index(['x', 'y', 'z'], inplace=True)

    for attr in pointset.attributes:
        if isinstance(attr, omf.attribute.CategoryAttribute):
            vertices[attr.name] = attr.categories.values
            vertices[f"{attr.name}_color"] = attr.categories.colors
        else:
            raise NotImplementedError(f"Attribute '{attr}' not implemented.")

    return vertices


@requires_dependency("GeoPandas", gpd)
def import_from_geopandas(gdf: "gpd.GeoDataFrame") -> pd.DataFrame:
    """
    Convert a GeoDataFrame with Point geometries to a DataFrame with a MultiIndex.

    Args:
        gdf (geopandas.GeoDataFrame): The input GeoDataFrame with Point geometries.

    Returns:
        pandas.DataFrame: A DataFrame with a MultiIndex (x, y, z) and attribute columns.
    """
    if not all(gdf.geometry.type == "Point"):
        raise ValueError("GeoDataFrame must contain only Point geometries.")

    coords = gdf.geometry.apply(lambda geom: (geom.x, geom.y, geom.z if geom.has_z else 0))
    data = gdf.drop(columns="geometry")
    data.index = pd.MultiIndex.from_tuples(coords, names=["x", "y", "z"])

    return data


def import_from_ply(input_file: Path) -> pd.DataFrame:
    """
    Import points from a PLY file (ASCII or binary).

    Args:
        input_file (Path): The input PLY file path.

    Returns:
        pd.DataFrame: A DataFrame with a MultiIndex (x, y, z).
    """
    with open(input_file, 'rb') as f:
        header = []
        while True:
            line = f.readline().decode().strip()
            header.append(line)
            if line == "end_header":
                break

        # Determine format
        format_line = next(line for line in header if line.startswith("format"))
        if "ascii" in format_line:
            return _import_points_from_ply_ascii(f, header)
        elif "binary" in format_line:
            return _import_points_from_ply_binary(f, header)
        else:
            raise ValueError("Unsupported PLY format.")


def _parse_ply_header(header: list[str]) -> dict:
    """
    Parse the PLY header to extract property names and their data types.

    Args:
        header (list[str]): The PLY header lines.

    Returns:
        dict: A dictionary where keys are property names and values are their data types.
    """
    properties = {}
    for line in header:
        if line.startswith("property"):
            parts = line.split()
            dtype = parts[1]
            name = parts[2]
            properties[name] = dtype
    return properties


def _import_points_from_ply_ascii(file_obj, header) -> pd.DataFrame:
    properties = _parse_ply_header(header)
    columns = list(properties.keys())
    dtypes = {name: (float if dtype.startswith("float") else int if dtype.startswith("int") else str)
              for name, dtype in properties.items()}
    points = []
    for line in file_obj:
        parts = line.decode().strip().split()
        points.append([dtypes[col](val) for col, val in zip(columns, parts)])

    df = pd.DataFrame(points, columns=columns)
    df.set_index(['x', 'y', 'z'], inplace=True)
    return df


def _import_points_from_ply_binary(file_obj, header) -> pd.DataFrame:
    properties = _parse_ply_header(header)
    columns = list(properties.keys())

    # Construct struct format and size
    struct_format = construct_struct_format(properties)
    struct_size = calculate_struct_size(struct_format)

    # Parse the vertex count from the header
    vertex_count = next(int(line.split()[-1]) for line in header if line.startswith("element vertex"))

    points = []
    for _ in range(vertex_count):
        vertex_data = file_obj.read(struct_size)
        points.append(struct.unpack(struct_format, vertex_data))

    df = pd.DataFrame(points, columns=columns)
    df.set_index(['x', 'y', 'z'], inplace=True)
    return df