from pathlib import Path

import yaml


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration file path
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


def load_config():
    """Load the project configuration from config.yaml."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config