import numpy as np
from typing import Tuple, Union

Point = Tuple[float, float, float]
BlockDimension = Tuple[float, float, float]
ArrayOrFloat = Union[np.ndarray, float]

MAX_XY_VALUE = 1677721.5  # Maximum value for x and y (2^24 - 1) / 10
MAX_Z_VALUE = 6553.5      # Maximum value for z (2^16 - 1) / 10
MAX_DIM_VALUE = 102.3  # Maximum value for dx, dy, dz

def encode_coordinates(x: ArrayOrFloat, y: ArrayOrFloat, z: ArrayOrFloat) -> Union[np.ndarray, int]:
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

def decode_coordinates(encoded: Union[np.ndarray, int]) -> Union[Tuple[np.ndarray, np.ndarray, np.ndarray], Point]:
    """Decode the 64-bit integer or array of 64-bit integers back to the original coordinates."""
    x_int = (encoded >> 40) & 0xFFFFFF
    y_int = (encoded >> 16) & 0xFFFFFF
    z_int = encoded & 0xFFFF
    x = x_int / 10.0
    y = y_int / 10.0
    z = z_int / 10.0
    return x, y, z

def encode_dimensions(dx: ArrayOrFloat, dy: ArrayOrFloat, dz: ArrayOrFloat) -> Union[np.ndarray, int]:
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

def decode_dimensions(encoded: Union[np.ndarray, int]) -> Union[Tuple[np.ndarray, np.ndarray, np.ndarray], BlockDimension]:
    """Decode the 32-bit integer or array of 32-bit integers back to the original block dimensions."""
    dx_int = (encoded >> 20) & 0x3FF
    dy_int = (encoded >> 10) & 0x3FF
    dz_int = encoded & 0x3FF
    dx = dx_int / 10.0
    dy = dy_int / 10.0
    dz = dz_int / 10.0
    return dx, dy, dz