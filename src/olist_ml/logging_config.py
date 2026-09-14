import logging
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Logs directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file
LOG_FILE = LOG_DIR / "olist_ml.log"

def setup_logging():
    """Configure application logging.] to console and file"""

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Show logs in the terminal
            logging.StreamHandler(),

            # Save logs to a file
            logging.FileHandler(LOG_FILE,encoding="utf-8",),
        ],
        force=True,)

    