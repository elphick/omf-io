from typing import Literal

import pandas as pd

def validate_block_model_data(block_data: pd.DataFrame, model_type: Literal['regular', 'tensor']):
    """Validate the block model data.

    Args:
        block_data (pandas.DataFrame): The block model data.

    Raises:
        ValueError: If the data is invalid.
    """
    # Placeholder implementation
    if block_data.empty:
        raise ValueError("Block model data cannot be empty.")