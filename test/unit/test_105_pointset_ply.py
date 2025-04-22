import tempfile
from pathlib import Path
import pandas as pd
import pytest
from omf_io.pointset.point_set import PointSetIO



def test_to_ply_ascii(pointset_sample_data):
    """Test exporting PointSetIO to an ASCII PLY file."""
    pointset = PointSetIO(pointset_sample_data)

    with tempfile.NamedTemporaryFile(suffix=".ply", delete=False) as temp_file:
        pointset.to_ply(Path(temp_file.name), binary=False)
        assert Path(temp_file.name).exists(), "The ASCII PLY file was not created."


def test_to_ply_binary(pointset_sample_data):
    """Test exporting PointSetIO to a binary PLY file."""
    pointset = PointSetIO(pointset_sample_data)

    with tempfile.NamedTemporaryFile(suffix=".ply", delete=False) as temp_file:
        pointset.to_ply(Path(temp_file.name), binary=True)
        assert Path(temp_file.name).exists(), "The binary PLY file was not created."


def test_from_ply_ascii(pointset_sample_data):
    """Test importing PointSetIO from an ASCII PLY file."""
    pointset = PointSetIO(pointset_sample_data)

    with tempfile.NamedTemporaryFile(suffix=".ply", delete=False) as temp_file:
        pointset.to_ply(Path(temp_file.name), binary=False)
        imported_pointset = PointSetIO.from_ply(Path(temp_file.name))
        pd.testing.assert_frame_equal(imported_pointset.data, pointset_sample_data)


def test_from_ply_binary(pointset_sample_data):
    """Test importing PointSetIO from a binary PLY file."""
    pointset = PointSetIO(pointset_sample_data)

    with tempfile.NamedTemporaryFile(suffix=".ply", delete=False) as temp_file:
        pointset.to_ply(Path(temp_file.name), binary=True)
        imported_pointset = PointSetIO.from_ply(Path(temp_file.name))
        pd.testing.assert_frame_equal(imported_pointset.data, pointset_sample_data)
