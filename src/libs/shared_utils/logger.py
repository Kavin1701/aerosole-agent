
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / "config" / "logger.env"
load_dotenv(dotenv_path=env_path)

LOG_FILE = os.getenv("LOG_FILE")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app")
