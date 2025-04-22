import xarray as xr
from pathlib import Path
from .validation import validate_grid_surface_data
from .importers import import_raster_as_grid_surface
from .exporters import export_grid_surface_to_raster


class GridSurfaceIO:
    """
    Handles the creation and consumption of grid surface (raster) objects.
    """

    def __init__(self, surface_data: xr.DataArray):
        """
        Initialize the GridSurfaceIO instance.

        Args:
            surface_data (xarray.DataArray): The grid surface data.
        """
        validate_grid_surface_data(surface_data)
        self.surface_data = surface_data

    @classmethod
    def from_raster(cls, raster_file: Path, **kwargs):
        """
        Create a GridSurfaceIO instance from a raster file.

        Args:
            raster_file (Path): The input raster file path.
            **kwargs: Additional arguments for the import function.

        Returns:
            GridSurfaceIO: An instance of the class.
        """
        surface_data = import_raster_as_grid_surface(raster_file, **kwargs)
        return cls(surface_data)

    def to_raster(self, output_file: Path, format: str = "GeoTIFF", **kwargs):
        """
        Prepare the grid surface data for export to a raster file.

        Args:
            output_file (Path): The output raster file path.
            format (str): The format of the output raster file. Default is "GeoTIFF".
            **kwargs: Additional arguments for the export function.
        """
        export_grid_surface_to_raster(self.surface_data, output_file, format=format, **kwargs)