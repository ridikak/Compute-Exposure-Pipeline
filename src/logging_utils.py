import logging
from .config import CFG

def get_logger(name: str) -> logging.Logger:
    level = getattr(logging, CFG.get("log_level", "INFO").upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    return logging.getLogger(name)
