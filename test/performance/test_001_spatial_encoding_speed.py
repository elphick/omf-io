import time
from typing import Union, Tuple

import numpy as np
import matplotlib.pyplot as plt

from omf_io.spatial_encoding.encoder import encode_coordinates, decode_coordinates, Point, ArrayOrFloat, \
    encode_dimensions, BlockDimension, decode_dimensions, MAX_XY_VALUE, MAX_Z_VALUE, MAX_DIM_VALUE


def encode_coordinates_original(x: ArrayOrFloat, y: ArrayOrFloat, z: ArrayOrFloat) -> Union[np.ndarray, int]:
    """Encode the coordinates into a 64-bit integer or an array of 64-bit integers."""

    def check_value(value, max_value):
        if value > max_value:
            raise ValueError(f"Value {value} exceeds the maximum supported value of {max_value}")
        if not (value * 10).is_integer():
            raise ValueError(f"Value {value} has more than 1 decimal place")
        return value

    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray) and isinstance(z, np.ndarray):
        x = np.vectorize(check_value)(x, MAX_XY_VALUE)
        y = np.vectorize(check_value)(y, MAX_XY_VALUE)
        z = np.vectorize(check_value)(z, MAX_Z_VALUE)
        x_int = (x * 10).astype(np.int64) & 0xFFFFFF
        y_int = (y * 10).astype(np.int64) & 0xFFFFFF
        z_int = (z * 10).astype(np.int64) & 0xFFFF
        encoded = (x_int << 40) | (y_int << 16) | z_int
        return encoded
    else:
        x = check_value(x, MAX_XY_VALUE)
        y = check_value(y, MAX_XY_VALUE)
        z = check_value(z, MAX_Z_VALUE)
        x_int = int(x * 10) & 0xFFFFFF
        y_int = int(y * 10) & 0xFFFFFF
        z_int = int(z * 10) & 0xFFFF
        encoded = (x_int << 40) | (y_int << 16) | z_int
        return encoded


def decode_coordinates_original(encoded: Union[np.ndarray, int]) -> Union[
    Tuple[np.ndarray, np.ndarray, np.ndarray], Point]:
    """Decode the 64-bit integer or array of 64-bit integers back to the original coordinates."""
    x_int = (encoded >> 40) & 0xFFFFFF
    y_int = (encoded >> 16) & 0xFFFFFF
    z_int = encoded & 0xFFFF
    x = x_int / 10.0
    y = y_int / 10.0
    z = z_int / 10.0
    return x, y, z


def encode_dimensions_orig(dx: ArrayOrFloat, dy: ArrayOrFloat, dz: ArrayOrFloat) -> Union[np.ndarray, int]:
    """Encode the block dimensions into a 32-bit integer or an array of 32-bit integers."""

    def check_value(value, max_value):
        if value > max_value:
            raise ValueError(f"Value {value} exceeds the maximum supported value of {max_value}")
        if not (value * 10).is_integer():
            raise ValueError(f"Value {value} has more than 1 decimal place")
        return value

    if isinstance(dx, np.ndarray) and isinstance(dy, np.ndarray) and isinstance(dz, np.ndarray):
        dx = np.vectorize(check_value)(dx, MAX_DIM_VALUE)
        dy = np.vectorize(check_value)(dy, MAX_DIM_VALUE)
        dz = np.vectorize(check_value)(dz, MAX_DIM_VALUE)
        dx_int = (dx * 10).astype(np.int32) & 0x3FF  # 10 bits for dx
        dy_int = (dy * 10).astype(np.int32) & 0x3FF  # 10 bits for dy
        dz_int = (dz * 10).astype(np.int32) & 0x3FF  # 10 bits for dz
        encoded = (dx_int << 20) | (dy_int << 10) | dz_int
        return encoded
    else:
        dx = check_value(dx, MAX_DIM_VALUE)
        dy = check_value(dy, MAX_DIM_VALUE)
        dz = check_value(dz, MAX_DIM_VALUE)
        dx_int = int(dx * 10) & 0x3FF
        dy_int = int(dy * 10) & 0x3FF
        dz_int = int(dz * 10) & 0x3FF
        encoded = (dx_int << 20) | (dy_int << 10) | dz_int
        return encoded


def decode_dimensions_orig(encoded: Union[np.ndarray, int]) -> Union[
    Tuple[np.ndarray, np.ndarray, np.ndarray], BlockDimension]:
    """Decode the 32-bit integer or array of 32-bit integers back to the original block dimensions."""
    dx_int = (encoded >> 20) & 0x3FF
    dy_int = (encoded >> 10) & 0x3FF
    dz_int = encoded & 0x3FF
    dx = dx_int / 10.0
    dy = dy_int / 10.0
    dz = dz_int / 10.0
    return dx, dy, dz


def test_encode_decode_point_large_array():
    number_of_elements = int(1e6)
    x = np.random.uniform(0, MAX_XY_VALUE, size=number_of_elements).round(1)
    y = np.random.uniform(0, MAX_XY_VALUE, size=number_of_elements).round(1)
    z = np.random.uniform(0, MAX_Z_VALUE, size=number_of_elements).round(1)

    start_time = time.time()
    encoded = encode_coordinates_original(x, y, z)
    encoding_time_original = time.time() - start_time
    print(f"Original Encoding time for {number_of_elements:,} elements: {encoding_time_original:.6f} seconds")

    start_time = time.time()
    encoded = encode_coordinates(x, y, z)
    encoding_time_numba = time.time() - start_time
    print(f"Numba encoding time for {number_of_elements:,} elements: {encoding_time_numba:.6f} seconds")

    print(
        f"Numba is {encoding_time_original / encoding_time_numba:.2f} times faster than the original encoding function.")

    start_time = time.time()
    decoded_x, decoded_y, decoded_z = decode_coordinates_original(encoded)
    decoding_time_original = time.time() - start_time
    print(f"Decoding time for {number_of_elements:,} elements: {decoding_time_original:.6f} seconds")

    start_time = time.time()
    decoded_x, decoded_y, decoded_z = decode_coordinates(encoded)
    decoding_time_numba = time.time() - start_time
    print(f"Numba decoding time for {number_of_elements:,} elements: {decoding_time_numba:.6f} seconds")

    print(
        f"Numba is {decoding_time_original / decoding_time_numba:.2f} times faster than the original decoding function.")

    np.testing.assert_almost_equal(decoded_x, x, decimal=6)
    np.testing.assert_almost_equal(decoded_y, y, decimal=6)
    np.testing.assert_almost_equal(decoded_z, z, decimal=6)


def test_encode_decode_dims_large_array():
    number_of_elements = int(1e6)
    dx = np.random.uniform(0, MAX_DIM_VALUE, size=number_of_elements).round(1)
    dy = np.random.uniform(0, MAX_DIM_VALUE, size=number_of_elements).round(1)
    dz = np.random.uniform(0, MAX_DIM_VALUE, size=number_of_elements).round(1)

    start_time = time.time()
    encoded = encode_dimensions_orig(dx, dy, dz)
    encoding_time_original = time.time() - start_time
    print(f"Original Encoding time for {number_of_elements:,} elements: {encoding_time_original:.6f} seconds")

    start_time = time.time()
    encoded = encode_dimensions(dx, dy, dz)
    encoding_time_numba = time.time() - start_time
    print(f"Numba encoding time for {number_of_elements:,} elements: {encoding_time_numba:.6f} seconds")

    print(
        f"Numba is {encoding_time_original / encoding_time_numba:.2f} times faster than the original encoding function.")

    start_time = time.time()
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions_orig(encoded)
    decoding_time_original = time.time() - start_time
    print(f"Decoding time for {number_of_elements:,} elements: {decoding_time_original:.6f} seconds")

    start_time = time.time()
    decoded_dx, decoded_dy, decoded_dz = decode_dimensions(encoded)
    decoding_time_numba = time.time() - start_time
    print(f"Numba decoding time for {number_of_elements:,} elements: {decoding_time_numba:.6f} seconds")

    print(
        f"Numba is {decoding_time_original / decoding_time_numba:.2f} times faster than the original decoding function.")

    np.testing.assert_almost_equal(decoded_dx, dx, decimal=6)
    np.testing.assert_almost_equal(decoded_dy, dy, decimal=6)
    np.testing.assert_almost_equal(decoded_dz, dz, decimal=6)


def test_encoding_speedup_plot():
    "Plot the speedup of Numba vs. original encoding based on array size"

    sizes = []
    speedups = []
    number_of_elements = int(1e6)  # Start with 1 million elements

    while number_of_elements > 1:
        sizes.append(number_of_elements)

        x = np.random.uniform(0, MAX_XY_VALUE, size=number_of_elements).round(1)
        y = np.random.uniform(0, MAX_XY_VALUE, size=number_of_elements).round(1)
        z = np.random.uniform(0, MAX_Z_VALUE, size=number_of_elements).round(1)

        start_time = time.time()
        encode_coordinates_original(x, y, z)
        encoding_time_original = time.time() - start_time

        start_time = time.time()
        encode_coordinates(x, y, z)
        encoding_time_numba = time.time() - start_time

        if encoding_time_numba > 0:
            speedups.append(encoding_time_original / encoding_time_numba)
        else:
            speedups.append(float('inf'))  # Assign infinity to indicate extremely high speedup

        # Adjust granularity below 100,000
        if number_of_elements > 100_000:
            number_of_elements = int(number_of_elements / 2)
        else:
            number_of_elements = int(number_of_elements / 1.5)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, speedups, marker='o', label='Speedup (Original / Numba)')
    plt.xscale('log')
    plt.xlabel('Array Size (log scale)')
    plt.ylabel('Speedup')
    plt.title('Speedup of Numba vs. Original Encoding')
    plt.grid(True)
    plt.legend()
    plt.show()
