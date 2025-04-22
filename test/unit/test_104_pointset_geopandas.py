import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, LineString
from omf_io.pointset.point_set import PointSetIO


def test_from_geopandas_valid():
    # Create a valid GeoDataFrame with Point geometries
    data = {
        "attribute1": [10, 20, 30],
        "attribute2": ["A", "B", "C"],
        "geometry": [Point(1, 2, 3), Point(4, 5, 6), Point(7, 8, 9)],
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Convert to PointSetIO
    pointset = PointSetIO.from_geopandas(gdf)

    # Validate the resulting DataFrame
    assert not pointset.data.empty, "The resulting DataFrame should not be empty."
    assert pointset.data.index.names == ["x", "y", "z"], "The MultiIndex must have names 'x', 'y', and 'z'."
    assert {"attribute1", "attribute2"}.issubset(
        pointset.data.columns
    ), "The columns must include 'attribute1' and 'attribute2'."


def test_from_geopandas_invalid_geometry():
    # Create a GeoDataFrame with invalid geometries (e.g., LineString)
    data = {
        "attribute1": [10],
        "geometry": [LineString([(1, 2), (3, 4)])],
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Attempt to convert and expect a ValueError
    with pytest.raises(ValueError, match="GeoDataFrame must contain only Point geometries."):
        PointSetIO.from_geopandas(gdf)


def test_from_geopandas_empty():
    # Create an empty GeoDataFrame
    gdf = gpd.GeoDataFrame(columns=["attribute1", "geometry"], geometry="geometry", crs="EPSG:4326")

    # Convert to PointSetIO
    pointset = PointSetIO.from_geopandas(gdf)

    # Validate the resulting DataFrame is empty
    assert pointset.data.empty, "The resulting DataFrame should be empty."
    assert pointset.data.index.names == ["x", "y", "z"], "The MultiIndex must have names 'x', 'y', and 'z'."


def test_round_trip_from_geopandas():
    # Create a GeoDataFrame with Point geometries
    data = {
        "attribute1": [10, 20, 30],
        "attribute2": ["A", "B", "C"],
        "geometry": [Point(1, 2, 3), Point(4, 5, 6), Point(7, 8, 9)],
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Convert to PointSetIO
    pointset = PointSetIO.from_geopandas(gdf)

    # Convert back to GeoDataFrame
    round_trip_gdf = pointset.to_geopandas()

    # Assert that the original and round-trip GeoDataFrames are equal
    pd.testing.assert_frame_equal(gdf.drop(columns="geometry"), round_trip_gdf.drop(columns="geometry"))
    assert gdf.geometry.equals(round_trip_gdf.geometry), "The geometries should match."
