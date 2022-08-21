def package_name() -> str:
    # Trim ".lib" from the package name of this module to get the "root" package name
    return __package__[:-4]
