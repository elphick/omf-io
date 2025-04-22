import pandas as pd
import pytest
from pathlib import Path


@pytest.fixture
def copper_deposit_path():
    # Path to the copper_deposit.omf file in the assets directory
    return Path(__file__).resolve().parents[1] / 'assets/copper_deposit.omf'


@pytest.fixture
def pointset_sample_data():
    """Fixture to provide sample point set data."""
    data = pd.DataFrame(
        {
            "attribute1": [10, 20, 30],
            "attribute2": [1.1, 2.2, 3.3],
        },
        index=pd.MultiIndex.from_tuples(
            [(1., 2., 3.), (4., 5., 6.), (7., 8., 9.)], names=["x", "y", "z"]
        ),
    )
    return data
