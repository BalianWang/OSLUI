import os


def get_environment_variable(variable_name):
    try:
        value = os.environ[variable_name]
        return value
    except KeyError:
        raise Exception(f"environment variable {variable_name} does not exist")
