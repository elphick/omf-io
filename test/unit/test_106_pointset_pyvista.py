import pytest
import pandas as pd
import numpy as np

from omf_io.pointset.importers import import_from_pyvista
from omf_io.pointset.exporters import export_to_pyvista
from omf_io.pointset import PointSetIO

pytest.importorskip("pyvista")
import pyvista as pv


@pytest.fixture
def sample_polydata():
    # Create a sample PyVista PolyData object
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    polydata = pv.PolyData(points)
    polydata.point_data["attribute1"] = [10, 20, 30]
    return polydata


@pytest.fixture
def sample_dataframe():
    # Create a sample pandas DataFrame with a MultiIndex
    index = pd.MultiIndex.from_tuples(
        [(0, 0, 0), (1, 1, 1), (2, 2, 2)], names=["x", "y", "z"]
    )
    data = pd.DataFrame({"attribute1": [10, 20, 30]}, index=index)
    return data


def test_import_from_pyvista(sample_polydata):
    # Test importing from PyVista PolyData
    df = import_from_pyvista(sample_polydata)
    assert isinstance(df, pd.DataFrame)
    assert list(df.index.names) == ["x", "y", "z"]
    assert "attribute1" in df.columns
    assert df.shape == (3, 1)
    assert df["attribute1"].tolist() == [10, 20, 30]


def test_export_to_pyvista(sample_dataframe):
    # Test exporting to PyVista PolyData
    polydata = export_to_pyvista(sample_dataframe)
    assert isinstance(polydata, pv.PolyData)
    assert polydata.n_points == 3
    assert "attribute1" in polydata.point_data
    assert polydata.point_data["attribute1"].tolist() == [10, 20, 30]


def test_pointsetio_from_pyvista(sample_polydata):
    # Test PointSetIO.from_pyvista
    pointset = PointSetIO.from_pyvista(sample_polydata)
    assert isinstance(pointset, PointSetIO)
    assert list(pointset.data.index.names) == ["x", "y", "z"]
    assert "attribute1" in pointset.data.columns
    assert pointset.data.shape == (3, 1)


def test_pointsetio_to_pyvista(sample_dataframe):
    # Test PointSetIO.to_pyvista
    pointset = PointSetIO(sample_dataframe)
    polydata = pointset.to_pyvista()
    assert isinstance(polydata, pv.PolyData)
    assert polydata.n_points == 3
    assert "attribute1" in polydata.point_data
    assert polydata.point_data["attribute1"].tolist() == [10, 20, 30]