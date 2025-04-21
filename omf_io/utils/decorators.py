
from ..utils.optional_packages import optional_packages

def requires_package(package_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not optional_packages.get(package_name, False):
                raise ImportError(f"{package_name} is not installed. Please install it using 'poetry install --extras \"{package_name}\"'.")
            return func(*args, **kwargs)
        return wrapper
    return decorator