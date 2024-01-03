from loguru import logger

from .config import Config
from .path import BASE_PATH

log = logger.bind(name="utils")

log.add(
    BASE_PATH / ".logs" / "utils.log",
    format="{time} | {level} | {message}",
    level=Config.log_level.upper(),
    rotation="10 MB",
    compression="zip",
    filter=lambda record: record["extra"].get("name") == "utils",
)
