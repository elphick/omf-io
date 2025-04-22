from pathlib import Path

from ydata_profiling.controller.pandas_decorator import profile_report

from omf_io.base import OMFIO, PathLike
from omf_io.utils.decorators import requires_dependency


class OMFReader(OMFIO):
    """A class limited to reading an OMF file.
    """

    def __init__(self, filepath: PathLike):
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File does not exist: {filepath}")
        super().__init__(filepath)

    def export_surface_to_raster_file(self, surface_name: str, output_file: PathLike):
        """Convert a surface to a raster file.

        Example use case is converting an elevation surface to a GeoTIFF.

        Args:
            surface_name (str): The name of the surface to convert.
            output_file (PathLike): The output raster file path.
        """
        pass

    def export_image_to_file(self, image_name: str, output_file: PathLike):
        """Convert an image to a file.

        Example use case is converting an ortho-image to a jpg

        Args:
            image_name (str): The name of the image to convert.
            output_file (PathLike): The output file path.
        """
        pass

    def export_blockmodel_to_file(self, blockmodel_name: str, output_file: PathLike):
        """Convert a blockmodel to a file.

        Args:
            blockmodel_name (str): The name of the blockmodel to convert.
            output_file (PathLike): The output file path.
        """
        pass

    @requires_dependency('ydata_profiling', profile_report)
    def export_blockmodel_profile_report(self, blockmodel_name: str, output_file: PathLike):
        """Generate a profile report for a blockmodel.

        Args:
            blockmodel_name (str): The name of the blockmodel to profile.
            output_file (PathLike): The output file path.
        """
        pass
