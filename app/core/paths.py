"""
Common filesystem paths used throughout Falcon.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_ROOT / "app"
CONFIGS_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"

DATABASE_DIR = DATA_DIR / "database"
HISTORICAL_DIR = DATA_DIR / "historical"
INSTRUMENTS_DIR = DATA_DIR / "instruments"
CACHE_DIR = DATA_DIR / "cache"
PAPER_TRADES_DIR = DATA_DIR / "paper_trades"

LOGS_DIR = PROJECT_ROOT / "logs"

RESOURCES_DIR = APP_DIR / "resources"