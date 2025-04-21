import logging
import os
from abc import ABC
from pathlib import Path
from typing import Union, Optional, Any

import omf
from omf import Project

PathLike = Union[str, Path, os.PathLike]


class OMFIO(ABC):

    def __init__(self, filepath: PathLike):
        """Instantiate the OMFPandas object.

        Args:
            filepath (Path): Path to the OMF file.

        Raises:
            FileNotFoundError: If the OMF file does not exist.
            ValueError: If the file is not an OMF file.
        """
        self._logger = logging.getLogger(__class__.__name__)

        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if not filepath.suffix == '.omf':
            raise ValueError(f'File is not an OMF file: {filepath}')
        self.filepath: Path = filepath
        self.project: Optional[Project] = None
        if filepath.exists():
            self.project = omf.load(str(filepath))

    def __repr__(self):
        res: str = f"OMF file({self.filepath})"
        res += f"\nElements: {self.element_types}"
        return res

    def __str__(self):
        res: str = f"OMF file({self.filepath})"
        res += f"\nElements: {self.element_types}"
        return res

    @property
    def element_types(self) -> Optional[dict[str, Any]]:
        """Dictionary of elements keyed by name

        In the special case of a composite element, the key will be the composite name and
        the value will be a dictionary of child elements keyed by name.

        """
        _elements = self.project.elements if self.project else []
        if _elements:
            element_dict = {}
            for e in _elements:
                if hasattr(e, 'elements') and e.elements:
                    element_dict[e.name] = {child.name: child.__class__.__name__ for child in e.elements}
                else:
                    element_dict[e.name] = e.__class__.__name__
            return element_dict
        else:
            return {}
