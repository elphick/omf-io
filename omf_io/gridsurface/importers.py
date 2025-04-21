import xarray as xr
from pathlib import Path


def load_raster_with_rioxarray(raster_file: Path):
    """Load a raster file using rioxarray.

    .. todo:: Implement the load_raster_with_rioxarray function

    Args:
        raster_file (Path): The input raster file path.

    Returns:
        xarray.DataArray: The raster data with geospatial metadata.
    """
    try:
        import rioxarray  # Ensure rioxarray is available
    except ImportError:
        raise ImportError("rioxarray is not installed. Install it with `pip install rioxarray`.")

    # Open the raster file as an xarray.DataArray
    raster = rioxarray.open_rasterio(raster_file)
    return raster


def import_raster_as_grid_surface(raster_file: Path, **kwargs) -> xr.DataArray:
    """Import a raster file as a grid surface.

    Args:
        raster_file (Path): The input raster file path.
        **kwargs: Additional keyword arguments for rioxarray.

    Returns:
        xarray.DataArray: The imported grid surface data.
    """
    raster = load_raster_with_rioxarray(raster_file)
    # Apply any additional processing or transformations here
    return raster
