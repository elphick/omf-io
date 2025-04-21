import ast
from typing import Union

import omf
import pandas as pd
from pathlib import Path

from omf_io.utils.attributes import generate_omf_attributes
from omf_io.utils.file import write_omf_element


class PointSetIO:
    """
    Handles the creation and consumption of PointSet objects with attributes.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the PointSetIO instance.

        Args:
            data (pandas.DataFrame): The point set data with a MultiIndex (x, y, z) and attribute columns.
        """
        if not isinstance(data.index, pd.MultiIndex) or data.index.names != ['x', 'y', 'z']:
            raise ValueError("Data must have a MultiIndex with levels ['x', 'y', 'z'].")
        self.data = data

    @classmethod
    def from_csv(cls, file_path: Path) -> "PointSetIO":
        """
        Load a PointSetIO instance from a CSV file.

        Args:
            file_path (Path): The path to the CSV file.

        Returns:
            PointSetIO: An instance of the class.
        """

        try:
            data = pd.read_csv(file_path, index_col=[0, 1, 2])
        except IndexError:
            raise ValueError("CSV file must contain three columns for x, y, z coordinates.")
        data.index.names = ['x', 'y', 'z']

        # Convert stringified tuples back to tuples in the 'holeid_color' column
        if 'holeid_color' in data.columns:
            data['holeid_color'] = data['holeid_color'].apply(ast.literal_eval)

        return cls(data)

    @classmethod
    def from_omf(cls, omf_input: Union[Path, omf.Project], pointset_name: str) -> "PointSetIO":
        """
        Create a PointSetIO instance from an OMF file or project object.

        Args:
            omf_input (Union[Path, omf.Project]): The input OMF file path or project object.
            pointset_name (str): The name of the PointSet element to extract.

        Returns:
            PointSetIO: An instance of the class.
        """
        if isinstance(omf_input, Path):
            project = omf.load(str(omf_input))
        elif isinstance(omf_input, omf.Project):
            project = omf_input
        else:
            raise TypeError("omf_input must be a Path or an omf.Project object.")

        pointset = next(
            (element for element in project.elements if
             element.name == pointset_name and isinstance(element, omf.PointSet)),
            None
        )
        if not pointset:
            raise ValueError(f"PointSet with name '{pointset_name}' not found in the OMF project.")

        # Create a DataFrame with vertices as the MultiIndex
        vertices = pd.DataFrame(pointset.vertices.array, columns=['x', 'y', 'z'])
        vertices.set_index(['x', 'y', 'z'], inplace=True)

        # Add attributes as columns
        for attr in pointset.attributes:
            if isinstance(attr, omf.attribute.CategoryAttribute):
                vertices[attr.name] = attr.categories.values
                vertices[f"{attr.name}_color"] = attr.categories.colors
            else:
                raise NotImplementedError(f"Attribute '{attr}' not implemented.")


        return cls(vertices)

    def to_csv(self, output_file: Path):
        """
        Export the PointSet data to a CSV file.

        Args:
            output_file (Path): The output CSV file path.
        """
        self.data.to_csv(output_file, index=True)

    def to_omf(self, element_name: str = 'point_set', output_file: Path = None) -> omf.PointSet:
        """
        Convert the PointSet data to an OMF PointSet, including attributes.

        Args:
            element_name (str): The name of the PointSet element.
            output_file (Path, optional): The file path to save the OMF PointSet.

        Returns:
            omf.PointSet: The OMF PointSet object (if output_file is not provided).
        """
        point_set = omf.PointSet(
            name=element_name,
            vertices=self.data.index.to_frame(index=False).values
        )

        # Add attributes
        point_set.attributes = generate_omf_attributes(self.data)

        if output_file:
            # Validate and write to file
            point_set.validate()
            write_omf_element(point_set, output_file, overwrite=True)

        return point_set
