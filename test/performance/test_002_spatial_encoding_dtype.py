"""
Compare the performance of different data types for spatial encoding.
"""
from timeit import timeit

import numpy as np
from numba import njit


@njit
def _encode_coordinates_unsigned(x: np.array, y: np.array, z: np.array) -> np.ndarray:
    """Encode the coordinates into a 64-bit unsigned integer or an array of 64-bit unsigned integers."""
    mask_24bit = np.uint64(0xFFFFFF)  # Explicitly cast the mask to np.uint64
    mask_16bit = np.uint64(0xFFFF)  # Explicitly cast the mask to np.uint64

    x_int = (x * 10).astype(np.uint64) & mask_24bit  # 24 bits for x
    y_int = (y * 10).astype(np.uint64) & mask_24bit  # 24 bits for y
    z_int = (z * 10).astype(np.uint64) & mask_16bit  # 16 bits for z

    # Cast shift amounts to np.uint64
    encoded = (x_int << np.uint64(40)) | (y_int << np.uint64(16)) | z_int
    return encoded


@njit
def _encode_coordinates_signed(x: np.array, y: np.array, z: np.array) -> np.ndarray:
    """Encode the coordinates into a 64-bit integer or an array of 64-bit integers."""

    x_int = (x * 10).astype(np.int64) & 0xFFFFFF  # 24 bits for x
    y_int = (y * 10).astype(np.int64) & 0xFFFFFF  # 24 bits for y
    z_int = (z * 10).astype(np.int64) & 0xFFFF  # 16 bits for z
    encoded = (x_int << 40) | (y_int << 16) | z_int
    return encoded


def test_encode_coordinates_speed():
    num_points = int(100e6)
    x = np.round(np.random.uniform(0, 16777215, num_points), 1)
    y = np.round(np.random.uniform(0, 16777215, num_points), 1)
    z = np.round(np.random.uniform(0, 65535, num_points), 1)

    # confirm that a signed index can be converted to an unsigned index and match
    # this also warms up the functions

    unsigned_encoded = _encode_coordinates_unsigned(x, y, z)
    signed_encoded = _encode_coordinates_signed(x, y, z)
    # Convert the signed to unsigned
    signed_to_unsigned = signed_encoded.astype(np.uint64)
    # Check if they match
    assert np.array_equal(unsigned_encoded, signed_to_unsigned), "Unsigned and signed encodings do not match!"


    # Measure the time taken for signed encoding
    time_signed = timeit(lambda: _encode_coordinates_signed(x, y, z), number=100)
    print(f"Signed encoding time: {time_signed:.6f} seconds")

    # Measure the time taken for unsigned encoding
    time_unsigned = timeit(lambda: _encode_coordinates_unsigned(x, y, z), number=100)
    print(f"Unsigned encoding time: {time_unsigned:.6f} seconds")

    print(f"Speedup: {time_signed / time_unsigned:.2f}x")


