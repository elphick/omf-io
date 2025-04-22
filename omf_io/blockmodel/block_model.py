from pathlib import Path
from typing import Literal
import pandas as pd
from .validation import validate_block_model_data
from .importers import import_block_model_from_csv
from .exporters import export_block_model_to_csv

class BlockModelIO:
    """
    Handles the creation and consumption of block model objects.
    """

    def __init__(self, block_data: pd.DataFrame, model_type: Literal['regular', 'tensor']):
        """
        Initialize the BlockModelIO instance.

        Args:
            block_data (pandas.DataFrame): The block model data.
            model_type (Literal['regular', 'tensor']): The type of block model.
        """
        validate_block_model_data(block_data, model_type)
        self.block_data = block_data
        self.model_type = model_type

    @classmethod
    def from_csv(cls, csv_file: Path, model_type: Literal['regular', 'tensor']):
        """
        Create a BlockModelIO instance from a CSV file.

        Args:
            csv_file (Path): The input CSV file path.
            model_type (Literal['regular', 'tensor']): The type of block model.

        Returns:
            BlockModelIO: An instance of the class.
        """
        block_data = import_block_model_from_csv(csv_file)
        return cls(block_data, model_type)

    @classmethod
    def from_parquet(cls, parquet_file: Path, model_type: Literal['regular', 'tensor']):
        """
        Create a BlockModelIO instance from a Parquet file.

        Args:
            parquet_file (Path): The input Parquet file path.
            model_type (Literal['regular', 'tensor']): The type of block model.

        Returns:
            BlockModelIO: An instance of the class.
        """
        block_data = pd.read_parquet(parquet_file)
        return cls(block_data, model_type)

    def to_csv(self, output_file: Path):
        """
        Export the block model data to a CSV file.

        Args:
            output_file (Path): The output CSV file path.
        """
        export_block_model_to_csv(self.block_data, output_file)

    def to_parquet(self, output_file: Path):
        """
        Export the block model data to a Parquet file.

        Args:
            output_file (Path): The output Parquet file path.
        """
        self.block_data.to_parquet(output_file, index=False)