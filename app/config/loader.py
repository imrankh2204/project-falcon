"""
Loads Falcon configuration from .env and YAML.
"""

from pathlib import Path

import os
import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_configuration() -> dict:
    """
    Load environment variables and YAML configuration.

    Returns
    -------
    dict
        Configuration dictionary.
    """

    env_file = PROJECT_ROOT / ".env"

    if env_file.exists():
        load_dotenv(env_file)

    app_env = os.getenv("APP_ENV", "paper")

    yaml_file = PROJECT_ROOT / "configs" / f"{app_env}.yaml"

    if not yaml_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found:\n{yaml_file}"
        )

    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_config = yaml.safe_load(file) or {}

    return {
        "app_name": os.getenv("APP_NAME", "ProjectFalcon"),
        "app_version": os.getenv("APP_VERSION", "0.1.0-alpha"),
        "app_env": app_env,
        "timezone": os.getenv("TIMEZONE", "Asia/Kolkata"),

        "broker": {
            "broker": os.getenv("BROKER", "zerodha"),
            "kite_api_key": os.getenv("KITE_API_KEY", ""),
            "kite_api_secret": os.getenv("KITE_API_SECRET", ""),
            "kite_access_token": os.getenv("KITE_ACCESS_TOKEN", ""),
        },

        "database": {
            "url": os.getenv("DATABASE_URL"),
        },

        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "directory": os.getenv("LOG_DIRECTORY", "logs"),
        },

        "trading": {
            "paper_trading": os.getenv("PAPER_TRADING", "true").lower() == "true",
            "max_trades_per_day": int(os.getenv("MAX_TRADES_PER_DAY", "3")),
            "max_daily_loss": float(os.getenv("MAX_DAILY_LOSS", "3000")),
            "max_open_positions": int(os.getenv("MAX_OPEN_POSITIONS", "1")),
        },

        "telegram": {
            "enabled": os.getenv("TELEGRAM_ENABLED", "false").lower() == "true",
            "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
        },

        "yaml": yaml_config,
    }