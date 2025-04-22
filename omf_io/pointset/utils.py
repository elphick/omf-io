import struct

# Shared property formats for encoding/decoding
PROPERTY_FORMATS = {
    'float': 'f', 'float32': 'f', 'float64': 'd',
    'int': 'i', 'int32': 'i', 'int64': 'q',
    'uchar': 'B', 'uint8': 'B',
    'double': 'd', 'uint16': 'H'
}

def construct_struct_format(properties):
    """
    Construct a struct format string based on the properties dictionary.

    Args:
        properties (dict): A dictionary where keys are property names and values are data types.

    Returns:
        str: The struct format string.
    """
    try:
        return ''.join(PROPERTY_FORMATS[str(prop)] for prop in properties.values())
    except KeyError as e:
        raise ValueError(f"Unsupported data type: {e}")

def calculate_struct_size(struct_format):
    """
    Calculate the size of a struct based on the format string.

    Args:
        struct_format (str): The struct format string.

    Returns:
        int: The size of the struct.
    """
    return struct.calcsize(struct_format)