import numpy as np
import omf
import pandas as pd
import pytest
from omf_io.pointset.point_set import PointSetIO


def test_from_omf_with_real_asset(copper_deposit_path):
    # Ensure the file exists
    assert copper_deposit_path.exists(), "The copper_deposit.omf file is missing."

    # Load the PointSet from the OMF file
    pointset_name = "collar"  # Replace with the actual PointSet name in the file
    pointset = PointSetIO.from_omf(copper_deposit_path, pointset_name)

    # Validate the loaded data
    assert not pointset.data.empty, "The PointSet data should not be empty."
    assert pointset.data.index.names == ['x', 'y', 'z'], "The MultiIndex must have names 'x', 'y', and 'z'."
    assert {'holeid', 'holeid_color'}.issubset(
        pointset.data.columns), "The columns must include 'holeid' and 'holeid_color'."


def test_from_omf_with_project_instance(copper_deposit_path):
    # Load the OMF project from the real file
    project = omf.load(str(copper_deposit_path))

    # Assert that the project is an instance of omf.Project
    assert isinstance(project, omf.Project)

    # Call the from_omf method with the project instance
    pointset_name = "collar"  # Replace with the actual PointSet name in the file
    pointset = PointSetIO.from_omf(project, pointset_name)

    # Validate the loaded data
    assert not pointset.data.empty, "The PointSet data should not be empty."
    assert pointset.data.index.names == ['x', 'y', 'z'], "The MultiIndex must have names 'x', 'y', and 'z'."
    assert {'holeid', 'holeid_color'}.issubset(
        pointset.data.columns), "The columns must include 'holeid' and 'holeid_color'."


def test_from_omf_invalid_input_type():
    # Pass an invalid type (e.g., an integer) to the from_omf method
    with pytest.raises(TypeError, match="omf_input must be a Path or an omf.Project object."):
        PointSetIO.from_omf(123, "collar")


def test_to_omf():
    # Create a sample DataFrame with point data
    points_data = pd.DataFrame({
        'x': [1.0, 2.0, 3.0],
        'y': [4.0, 5.0, 6.0],
        'z': [7.0, 8.0, 9.0]
    }).set_index(['x', 'y', 'z'])

    # Initialize a PointSetIO instance
    pointset_io = PointSetIO(points_data)

    # Convert to OMF PointSet
    element_name = "test_point_set"
    omf_pointset = pointset_io.to_omf(element_name)

    # Assert the OMF PointSet has the correct name and vertices
    assert omf_pointset.name == element_name, "The PointSet name is incorrect."
    assert omf_pointset.vertices.shape == list((3, 3)), "The vertices shape is incorrect."
    assert pointset_io.data.index.names == ['x', 'y', 'z'], "The MultiIndex must have names 'x', 'y', and 'z'."
    # Assert the vertices data matches
    assert np.array_equal(
        pointset_io.data.index.to_frame(index=False).values,
        omf_pointset.vertices
    ), "The vertices data is incorrect."
