import pytest
from pathlib import Path

@pytest.fixture
def copper_deposit_path():
    # Path to the copper_deposit.omf file in the assets directory
    return Path("../assets/copper_deposit.omf")