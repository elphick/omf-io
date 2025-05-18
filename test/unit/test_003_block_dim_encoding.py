import pytest
import numpy as np

from omf_io.spatial_encoding.encoder import encode_dimensions, decode_dimensions, MAX_DIM_VALUE


def test_encode_decode_float_dimensions():
    dx, dy, dz = 12.3, 56.7, 90.1
    encoded = encode_dimensions(dx, dy, dz)
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions(encoded)
    assert pytest.approx(decoded_dx, 1e-06) == dx
    assert pytest.approx(decoded_dy, 1e-06) == dy
    assert pytest.approx(decoded_dz, 1e-06) == dz


def test_encode_decode_array_dimensions():
    dx = np.array([12.3, 23.4, 34.5])
    dy = np.array([56.7, 67.8, 78.9])
    dz = np.array([90.1, 12.3, 23.4])
    encoded = encode_dimensions(dx, dy, dz)
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions(encoded)
    np.testing.assert_almost_equal(decoded_dx, dx, decimal=6)
    np.testing.assert_almost_equal(decoded_dy, dy, decimal=6)
    np.testing.assert_almost_equal(decoded_dz, dz, decimal=6)


def test_max_values_dimensions():
    dx, dy, dz = MAX_DIM_VALUE, MAX_DIM_VALUE, MAX_DIM_VALUE
    encoded = encode_dimensions(dx, dy, dz)
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions(encoded)
    assert pytest.approx(decoded_dx, 1e-06) == dx
    assert pytest.approx(decoded_dy, 1e-06) == dy
    assert pytest.approx(decoded_dz, 1e-06) == dz


def test_exceed_max_values_dimensions():
    with pytest.raises(ValueError, match=f"exceeds the maximum supported value"):
        encode_dimensions(MAX_DIM_VALUE + 0.1, 0, 0)
    with pytest.raises(ValueError, match=f"exceeds the maximum supported value"):
        encode_dimensions(0, MAX_DIM_VALUE + 0.1, 0)
    with pytest.raises(ValueError, match=f"exceeds the maximum supported value"):
        encode_dimensions(0, 0, MAX_DIM_VALUE + 0.1)


def test_more_than_one_decimal_place_dimensions():
    with pytest.raises(ValueError, match="has more than 1 decimal place"):
        encode_dimensions(12.345, 0, 0)
    with pytest.raises(ValueError, match="has more than 1 decimal place"):
        encode_dimensions(0, 56.789, 0)
    with pytest.raises(ValueError, match="has more than 1 decimal place"):
        encode_dimensions(0, 0, 90.123)


def test_random_values_dimensions():
    num_points: int = int(1e06)
    dx = np.round(np.random.uniform(0, MAX_DIM_VALUE, num_points), 1)
    dy = np.round(np.random.uniform(0, MAX_DIM_VALUE, num_points), 1)
    dz = np.round(np.random.uniform(0, MAX_DIM_VALUE, num_points), 1)
    encoded = encode_dimensions(dx, dy, dz)
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions(encoded)
    np.testing.assert_almost_equal(decoded_dx, dx, decimal=6)
    np.testing.assert_almost_equal(decoded_dy, dy, decimal=6)
    np.testing.assert_almost_equal(decoded_dz, dz, decimal=6)
