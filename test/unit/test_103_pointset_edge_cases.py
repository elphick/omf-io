import pandas as pd
import pytest
from pathlib import Path
from omf_io.pointset.point_set import PointSetIO


def test_from_omf_missing_pointset(copper_deposit_path):
    # Ensure the file exists
    assert copper_deposit_path.exists(), "The copper_deposit.omf file is missing."

    # Attempt to load a non-existent PointSet
    with pytest.raises(ValueError, match="PointSet with name 'non_existent' not found in the OMF project."):
        PointSetIO.from_omf(copper_deposit_path, "non_existent")


def test_from_csv_invalid_file(tmp_path):
    # Create an invalid CSV file
    invalid_csv = tmp_path / "invalid.csv"
    pd.DataFrame({"a": [1], "b": [2]}).to_csv(invalid_csv, index=False)

    # Attempt to load the invalid CSV
    with pytest.raises(ValueError, match="CSV file must have at least three columns for x, y, and z coordinates."):
        PointSetIO.from_csv(invalid_csv)


def test_empty_pointset():
    empty_data = pd.DataFrame(columns=["x", "y", "z"]).set_index(["x", "y", "z"])
    pointset = PointSetIO(empty_data)

    # Validate that the points DataFrame is empty
    assert pointset.data.empty, "The PointSet should be empty."