import numpy as np
from typing import Tuple, Union, Optional

from numba import njit

Point = Tuple[float, float, float]
BlockDimension = Tuple[float, float, float]
ArrayOrFloat = Union[np.ndarray, float]

# MAX_XY_VALUE = 1677721.5  # Maximum value for x and y (2^24 - 1) / 10
# MAX_Z_VALUE = 6553.5  # Maximum value for z (2^16 - 1) / 10
MAX_XY_VALUE = (0xFFFFFF - 1) / 10  # Slightly reduced to avoid overflow
MAX_Z_VALUE = (0xFFFF - 1) / 10  # Slightly reduced to avoid overflow
MAX_DIM_VALUE = 102.3  # Maximum value for dx, dy, dz (10 bits each)

import yaml
from pathlib import Path
from typing import Union, Dict
import numpy as np


class SpatialEncoder:
    def __init__(self, config: Optional[Union[Path, str, Dict]] = None,
                 srs_code: Optional[str] = None):
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0
        self.config: dict = self.load_config(config)

        if srs_code:
            self.set_offsets_from_srs(srs_code)

    @staticmethod
    def load_config(config: Optional[Union[Path, str, Dict]] = None) -> Dict:
        """Load the configuration from a file or use the provided dictionary."""
        default_config_path = Path(__file__).parent / "spatial_encoder_config.yaml"

        if config is None:
            config = default_config_path

        if isinstance(config, dict):
            return config
        elif isinstance(config, (Path, str)):
            try:
                with open(config, "r") as file:
                    return yaml.safe_load(file)
            except FileNotFoundError:
                raise FileNotFoundError(f"Configuration file '{config}' not found.")
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file: {e}")
        else:
            raise TypeError("Config must be a file path, a dictionary, or None.")

    def set_offsets_from_srs(self, srs_code: str):
        """Set offsets based on the SRS code from the configuration."""
        if srs_code not in self.config:
            raise ValueError(f"SRS code '{srs_code}' not found in configuration.")
        offsets = self.config[srs_code]
        self.x_offset = offsets.get("x_offset", 0.0)
        self.y_offset = offsets.get("y_offset", 0.0)
        self.z_offset = offsets.get("z_offset", 0.0)

    def set_offsets(self, offsets: Dict[str, float]):
        """Override offsets with a dictionary."""
        self.x_offset = offsets.get("x_offset", self.x_offset)
        self.y_offset = offsets.get("y_offset", self.y_offset)
        self.z_offset = offsets.get("z_offset", self.z_offset)

    def encode_coordinates(self, x: Union[int, float, np.ndarray], y: Union[int, float, np.ndarray],
                           z: Union[int, float, np.ndarray]) -> Union[np.ndarray, int]:
        """Encode coordinates with offsets applied.

        The offsets are added to the coordinates before encoding.
        """
        x = np.array(x) + self.x_offset
        y = np.array(y) + self.y_offset
        z = np.array(z) + self.z_offset
        return encode_coordinates(x, y, z)

    def decode_coordinates(self, encoded: Union[int, np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Decode coordinates and apply offsets.

        The offsets are subtracted from the decoded coordinates.
        """
        x, y, z = decode_coordinates(encoded)
        x -= self.x_offset
        y -= self.y_offset
        z -= self.z_offset
        return x, y, z


def encode_coordinates(x: Union[int, float, np.array], y: Union[int, float, np.array],
                       z: Union[int, float, np.array]) -> Union[np.ndarray, int]:
    if isinstance(x, (float, int)):
        x, y, z = np.array([x]), np.array([y]), np.array([z])
    elif not isinstance(x, np.ndarray):
        raise TypeError("Inputs must be floats or numpy arrays.")

    # Vectorized checks for value constraints
    if np.any(x < 0) or np.any(y < 0) or np.any(z < 0):
        raise ValueError("Coordinate values must be non-negative. Consider using offsets.")
    if np.any(x > MAX_XY_VALUE) or np.any(y > MAX_XY_VALUE) or np.any(z > MAX_Z_VALUE):
        raise ValueError(
            f"Coordinate values exceed the maximum supported value: {MAX_XY_VALUE} for x and y, {MAX_Z_VALUE} for z.")
    if np.any((x * 10) % 1 != 0) or np.any((y * 10) % 1 != 0) or np.any((z * 10) % 1 != 0):
        raise ValueError("Coordinate values must have at most 1 decimal place.")

    # Perform encoding
    encoded = _encode_coordinates_numba(x, y, z)

    # Ensure encoded values are within valid range
    MIN_ENCODED_VALUE = 0
    MAX_ENCODED_VALUE = (0xFFFFFF << 40) | (0xFFFFFF << 16) | 0xFFFF
    if np.any((encoded < MIN_ENCODED_VALUE) | (encoded > MAX_ENCODED_VALUE)):
        raise ValueError("Encoded value is out of valid range.")

    if x.size == 1:
        return encoded[0]
    return encoded


@njit
def _encode_coordinates_numba(x: np.array, y: np.array, z: np.array) -> np.ndarray:
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
def _encode_coordinates_numba_unsigned(x: np.array, y: np.array, z: np.array) -> np.ndarray:
    """Encode the coordinates into a 64-bit integer or an array of 64-bit integers."""

    x_int = (x * 10).astype(np.int64) & 0xFFFFFF  # 24 bits for x
    y_int = (y * 10).astype(np.int64) & 0xFFFFFF  # 24 bits for y
    z_int = (z * 10).astype(np.int64) & 0xFFFF  # 16 bits for z
    encoded = (x_int << 40) | (y_int << 16) | z_int
    return encoded

def decode_coordinates(encoded: Union[int, np.ndarray]) -> Union[
    Tuple[np.ndarray, np.ndarray, np.ndarray], Point]:
    # Define valid range for encoded values
    MIN_ENCODED_VALUE = 0
    MAX_ENCODED_VALUE = (0xFFFFFF << 40) | (0xFFFFFF << 16) | 0xFFFF  # Max for x, y, z combined

    if isinstance(encoded, np.int64):
        if not (MIN_ENCODED_VALUE <= encoded <= MAX_ENCODED_VALUE):
            raise ValueError(f"Encoded value {encoded} is out of valid range.")
        encoded = np.array([encoded], dtype=np.int64)
    elif isinstance(encoded, np.ndarray):
        if np.any((encoded < MIN_ENCODED_VALUE) | (encoded > MAX_ENCODED_VALUE)):
            raise ValueError("One or more encoded values are out of valid range.")
    else:
        raise TypeError("Input must be an integer or a numpy array.")

    if encoded.size == 1:
        return _decode_coordinates_numba(encoded[0])
    return _decode_coordinates_numba(encoded)


@njit
def _decode_coordinates_numba(encoded: np.ndarray) -> Union[
    Tuple[np.ndarray, np.ndarray, np.ndarray], Point]:
    """Decode the 64-bit integer or array of 64-bit integers back to the original coordinates."""
    x_int = (encoded >> 40) & 0xFFFFFF
    y_int = (encoded >> 16) & 0xFFFFFF
    z_int = encoded & 0xFFFF
    x = x_int / 10.0
    y = y_int / 10.0
    z = z_int / 10.0
    return x, y, z


def encode_dimensions(dx: Union[int, float, np.array], dy: Union[int, float, np.array],
                      dz: Union[int, float, np.array]) -> Union[int, np.ndarray]:
    if isinstance(dx, (float, int)):
        dx, dy, dz = np.array([dx]), np.array([dy]), np.array([dz])
    elif not isinstance(dx, np.ndarray):
        raise TypeError("Inputs must be floats or numpy arrays.")
    if dx.size == 1:
        return _encode_dimensions_numba(dx, dy, dz)[0]
    return _encode_dimensions_numba(dx, dy, dz)


@njit
def _encode_dimensions_numba(dx: np.array, dy: np.array, dz: np.array) -> np.ndarray:
    """Encode the dimensions into a 64-bit integer or an array of 64-bit integers."""

    def check_value(value, max_value):
        if value > max_value:
            raise ValueError(f"Value {value} exceeds the maximum supported value of {max_value}")
        if (value * 10) % 1 != 0:
            raise ValueError(f"Value {value} has more than 1 decimal place")
        return value

    # Assume inputs are arrays
    dx_checked = np.empty_like(dx)
    dy_checked = np.empty_like(dy)
    dz_checked = np.empty_like(dz)
    for i in range(len(dx)):
        dx_checked[i] = check_value(dx[i], 102.3)
        dy_checked[i] = check_value(dy[i], 102.3)
        dz_checked[i] = check_value(dz[i], 102.3)

    dx_int = (dx_checked * 10).astype(np.int64) & 0x3FF  # 10 bits for dx
    dy_int = (dy_checked * 10).astype(np.int64) & 0x3FF  # 10 bits for dx
    dz_int = (dz_checked * 10).astype(np.int64) & 0x3FF  # 10 bits for dx
    encoded = (dx_int << 20) | (dy_int << 10) | dz_int
    return encoded


def decode_dimensions(encoded: Union[int, np.ndarray]) -> Union[np.array, BlockDimension]:
    if isinstance(encoded, np.int64):
        encoded = np.array([encoded], dtype=np.int64)
    elif not isinstance(encoded, np.ndarray):
        raise TypeError("Input must be an integer or a numpy array.")
    if encoded.size == 1:
        return _decode_dimensions_numba(encoded[0])
    return _decode_dimensions_numba(encoded)


@njit
def _decode_dimensions_numba(encoded: Union[int, np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Decode the 32-bit integer or array of 32-bit integers back to the original block dimensions."""
    dx_int = (encoded >> 20) & 0x3FF
    dy_int = (encoded >> 10) & 0x3FF
    dz_int = encoded & 0x3FF
    dx = dx_int / 10.0
    dy = dy_int / 10.0
    dz = dz_int / 10.0
    return dx, dy, dz
