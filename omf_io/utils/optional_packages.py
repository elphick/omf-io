# Optional imports
optional_packages = {
    'ydata_profiling': False,
    'pandera': False
}

try:
    import ydata_profiling

    optional_packages['ydata_profiling'] = True
except ImportError:
    pass

try:
    import pandera

    optional_packages['pandera'] = True
except ImportError:
    pass
