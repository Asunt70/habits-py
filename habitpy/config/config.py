"""Global variables"""

from platformdirs import user_config_dir, user_data_dir
from pathlib import Path


def get_config_dir():
    return Path(user_config_dir("habitpy"))


def get_data_dir():
    return Path(user_data_dir("habitpy"))


def get_config_path():
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def get_db_path():
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "user.db"


def get_export_path():
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "exported.csv"


# Database
DATABASE_PATH = get_db_path()

# Config
CONFIG_PATH = get_config_path()

EXPORT_PATH = get_export_path()
