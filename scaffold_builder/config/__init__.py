"""
Configuration module for Project Scaffold Builder.
"""

from .settings import (
    APP_TITLE,
    APP_VERSION,
    CONFIG_FILENAME,
    DEFAULT_BASE_DIR,
    DEFAULT_PROJECT_NAME,
    Colors,
    DEFAULT_GITIGNORE,
    DEFAULT_README,
    DEFAULT_MAIN,
)
from .templates import (
    PROJECT_TEMPLATES,
    DEFAULT_TEMPLATE_NAME,
    DEFAULT_STRUCTURE,
)

__all__ = [
    "APP_TITLE",
    "APP_VERSION",
    "CONFIG_FILENAME",
    "DEFAULT_BASE_DIR",
    "DEFAULT_PROJECT_NAME",
    "Colors",
    "DEFAULT_GITIGNORE",
    "DEFAULT_README",
    "DEFAULT_MAIN",
    "PROJECT_TEMPLATES",
    "DEFAULT_TEMPLATE_NAME",
    "DEFAULT_STRUCTURE",
]
