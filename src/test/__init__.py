from os import path

def pkg():
    parent_package = path.basename(path.dirname(path.dirname(__file__)))
    my_package = path.basename(path.dirname(__file__))
    return f"{parent_package}.{my_package}"
