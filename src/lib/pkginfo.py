def package_name() -> str:
    # Trim ".lib" from the package name
    return __package__[:-4]
