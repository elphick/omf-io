from importlib import metadata
from .utils.optional_packages import optional_packages

try:
    __version__ = metadata.version('omf_io')
except metadata.PackageNotFoundError:
    # Package is not installed
    pass
