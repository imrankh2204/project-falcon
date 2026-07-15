from app.config import get_config

config = get_config()

print("=" * 50)
print("Project Falcon Configuration")
print("=" * 50)

print(f"Application : {config.app_name}")
print(f"Version     : {config.app_version}")
print(f"Environment : {config.app_env}")
print(f"Broker      : {config.broker.broker}")
print(f"Database    : {config.database.url}")
print(f"Paper Mode  : {config.trading.paper_trading}")
print(f"Timezone    : {config.timezone}")