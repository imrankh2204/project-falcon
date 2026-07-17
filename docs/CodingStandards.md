## Fail Fast Principle

Infrastructure components must detect configuration or initialization errors as early as possible and stop execution with clear diagnostic messages.

Never allow the application to continue running in a partially initialized state.

## Database Access

Only DatabaseManager is permitted to execute raw SQL.

Application components must interact with the database exclusively through the DatabaseManager interface.
