from loguru import logger
from utils import BASE_PATH, Config

log = logger.bind(name="game")

log.add(
    BASE_PATH / ".logs" / "game.log",
    format="{time} | {level} | {message}",
    level=Config.log_level.upper(),
    rotation="10 MB",
    compression="zip",
    filter=lambda record: record["extra"].get("name") == "game",
)
