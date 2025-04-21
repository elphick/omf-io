import xarray as xr
from pathlib import Path
from .validation import validate_surface_data
from .importers import import_surface_from_obj, import_surface_from_ply_ascii, import_surface_from_ply_binary
from .exporters import export_surface_to_obj, export_surface_to_ply_ascii, export_surface_to_ply_binary


class SurfaceIO:
    """
    Handles the creation and consumption of surface (wireframe) objects.
    """

    def __init__(self, surface_data: dict):
        """
        Initialize the SurfaceIO instance.

        Args:
            surface_data (dict): The surface data containing 'vertices' and 'faces'.
        """
        validate_surface_data(surface_data)
        self.surface_data = surface_data

    @classmethod
    def from_obj(cls, obj_file: Path):
        """
        Create a SurfaceIO instance from an OBJ file.

        Args:
            obj_file (Path): The input OBJ file path.

        Returns:
            SurfaceIO: An instance of the class.
        """
        surface_data = import_surface_from_obj(obj_file)
        return cls(surface_data)

    @classmethod
    def from_ply_ascii(cls, ply_file: Path):
        """
        Create a SurfaceIO instance from an ASCII PLY file.

        Args:
            ply_file (Path): The input PLY file path.

        Returns:
            SurfaceIO: An instance of the class.
        """
        surface_data = import_surface_from_ply_ascii(ply_file)
        return cls(surface_data)

    @classmethod
    def from_ply_binary(cls, ply_file: Path):
        """
        Create a SurfaceIO instance from a binary PLY file.

        Args:
            ply_file (Path): The input PLY file path.

        Returns:
            SurfaceIO: An instance of the class.
        """
        surface_data = import_surface_from_ply_binary(ply_file)
        return cls(surface_data)

    def to_obj(self, output_file: Path):
        """
        Export the surface data to an OBJ file.

        Args:
            output_file (Path): The output OBJ file path.
        """
        export_surface_to_obj(self.surface_data, output_file)

    def to_ply_ascii(self, output_file: Path):
        """
        Export the surface data to an ASCII PLY file.

        Args:
            output_file (Path): The output PLY file path.
        """
        export_surface_to_ply_ascii(self.surface_data, output_file)

    def to_ply_binary(self, output_file: Path):
        """
        Export the surface data to a binary PLY file.

        Args:
            output_file (Path): The output PLY file path.
        """
        export_surface_to_ply_binary(self.surface_data, output_file)