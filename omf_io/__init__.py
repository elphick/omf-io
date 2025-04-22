from importlib import metadata

try:
    __version__ = metadata.version('omf_io')
except metadata.PackageNotFoundError:
    # Package is not installed
    pass
