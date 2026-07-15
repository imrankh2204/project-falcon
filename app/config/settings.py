"""
Configuration models for Project Falcon.
"""

from pydantic import BaseModel


class BrokerSettings(BaseModel):
    broker: str
    kite_api_key: str = ""
    kite_api_secret: str = ""
    kite_access_token: str = ""


class DatabaseSettings(BaseModel):
    url: str


class LoggingSettings(BaseModel):
    level: str
    directory: str


class TradingSettings(BaseModel):
    paper_trading: bool
    max_trades_per_day: int
    max_daily_loss: float
    max_open_positions: int


class TelegramSettings(BaseModel):
    enabled: bool
    bot_token: str = ""
    chat_id: str = ""


class AppSettings(BaseModel):
    app_name: str
    app_version: str
    app_env: str
    timezone: str

    broker: BrokerSettings
    database: DatabaseSettings
    logging: LoggingSettings
    trading: TradingSettings
    telegram: TelegramSettings