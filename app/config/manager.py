"""
Configuration manager.
"""

from functools import lru_cache

from app.config.loader import load_configuration
from app.config.settings import AppSettings


@lru_cache(maxsize=1)
def get_config() -> AppSettings:
    """
    Return the validated Falcon configuration.

    The configuration is loaded once and cached for
    the lifetime of the application.
    """

    config = load_configuration()

    return AppSettings.model_validate(config)