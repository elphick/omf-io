import pandas as pd
import pytest
from pathlib import Path
from omf_io.pointset.point_set import PointSetIO


def test_round_trip_from_omf_to_csv_and_back(copper_deposit_path, tmp_path):
    # Ensure the file exists
    assert copper_deposit_path.exists(), "The copper_deposit.omf file is missing."

    # Load the PointSet from the OMF file
    pointset_name = "collar"  # Replace with the actual PointSet name in the file
    pointset = PointSetIO.from_omf(copper_deposit_path, pointset_name)

    # Export to CSV
    csv_file = tmp_path / "round_trip_test.csv"
    pointset.to_csv(csv_file)
    assert csv_file.exists(), "The CSV file was not created."

    # Re-import from CSV
    reimported_pointset = PointSetIO.from_csv(csv_file)

    # Assert that the data is consistent
    pd.testing.assert_frame_equal(pointset.data, reimported_pointset.data)
