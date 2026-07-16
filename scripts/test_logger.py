from app.core.logger import get_logger

logger = get_logger("startup")

logger.info("Falcon logger initialized.")

logger.warning("This is a warning example.")

logger.error("This is an error example.")