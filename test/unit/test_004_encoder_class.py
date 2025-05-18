import pytest
from pathlib import Path

from omf_io.spatial_encoding.encoder import SpatialEncoder


@pytest.fixture
def config_dict():
    return {
        "EPSG:4326": {"x_offset": 10000.0, "y_offset": 20000.0, "z_offset": 10.0},
        "EPSG:3857": {"x_offset": 5000.0, "y_offset": 10000.0, "z_offset": 0.0},
    }

@pytest.fixture
def default_config_file(tmp_path, config_dict):
    config_path = tmp_path / "default_offsets.yaml"
    with open(config_path, "w") as f:
        import yaml
        yaml.dump(config_dict, f)
    return config_path

def test_load_config_from_dict(config_dict):
    encoder = SpatialEncoder(config=config_dict, srs_code="EPSG:4326")
    assert encoder.x_offset == 10000.0
    assert encoder.y_offset == 20000.0
    assert encoder.z_offset == 10.0

def test_load_config_from_file(default_config_file):
    encoder = SpatialEncoder(config=default_config_file, srs_code="EPSG:3857")
    assert encoder.x_offset == 5000.0
    assert encoder.y_offset == 10000.0
    assert encoder.z_offset == 0.0

def test_set_offsets_override(config_dict):
    encoder = SpatialEncoder(config=config_dict, srs_code="EPSG:4326")
    encoder.set_offsets({"x_offset": 0.0, "y_offset": 0.0, "z_offset": 0.0})
    assert encoder.x_offset == 0.0
    assert encoder.y_offset == 0.0
    assert encoder.z_offset == 0.0

def test_encode_decode_coordinates_mock(config_dict, mocker):
    mocker.patch("omf_io.spatial_encoding.encoder.encode_coordinates", return_value=12345)
    mocker.patch("omf_io.spatial_encoding.encoder.decode_coordinates", return_value=(10.0, 20.0, 5.0))

    encoder = SpatialEncoder(config=config_dict, srs_code="EPSG:4326")
    encoded = encoder.encode_coordinates(10.0, 20.0, 5.0)
    assert encoded == 12345

    decoded = encoder.decode_coordinates(encoded)
    assert decoded == (10.0, 20.0, 5.0)


def test_round_trip_with_offsets(config_dict):
    encoder = SpatialEncoder(config=config_dict, srs_code="EPSG:4326")

    # Original coordinates
    original_coords = (10010.0, 20020.0, 5.0)

    # Encode the coordinates
    encoded = encoder.encode_coordinates(*original_coords)

    # Decode back to original coordinates
    decoded = encoder.decode_coordinates(encoded)

    # Assert that the decoded coordinates match the original
    assert decoded == original_coords


def test_negative_coords(config_dict):
    encoder = SpatialEncoder(config=None, srs_code="EPSG:4326")

    # Original negative coordinates
    original_coords = (-10.0, -20.0, -5.0)

    # Expect failure when encoding negative coordinates
    with pytest.raises(ValueError, match="Coordinate values must be non-negative."):
        encoder.encode_coordinates(*original_coords)

    # Set offsets to allow negative coordinates
    encoder.set_offsets({"x_offset": 10000.0, "y_offset": 20000.0, "z_offset": 10.0})

    # Encode the coordinates (offsets are applied internally by the class)
    encoded = encoder.encode_coordinates(*original_coords)

    # Decode back to the original coordinates
    decoded = encoder.decode_coordinates(encoded)

    # Assert that the decoded coordinates match the original negative coordinates
    assert decoded == pytest.approx(original_coords)