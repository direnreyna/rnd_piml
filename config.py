# config.py

"""
Configuration module for determining runtime environment and settings.
"""

from typing import Literal

EnvironmentType = Literal["colab", "local"]

def get_environment() -> EnvironmentType:
    """
    Determines the execution environment based on available modules.

    Returns:
        EnvironmentType: Either "colab" or "local".
    """
    try:
        import google.colab  # type: ignore
        return "colab"
    except ImportError:
        return "local"
