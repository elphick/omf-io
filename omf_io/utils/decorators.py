
def requires_dependency(library_name: str, library: object):
    """
    A decorator to check if an optional library is installed.

    Args:
        library_name (str): The name of the library (for error messages).
        library (object): The library object (e.g., `gpd` or `Point`).

    Returns:
        Callable: The wrapped function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if library is None:
                raise ImportError(f"{library_name} is not installed. Please install it to use this function.")
            return func(*args, **kwargs)
        return wrapper
    return decorator