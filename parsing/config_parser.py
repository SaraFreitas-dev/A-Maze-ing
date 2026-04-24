import sys
from typing import Any


class ConfigError(Exception):
    """
    Custom exception for config
    """
    pass


def get_config_path() -> str:
    """
    Get the config file_name
    If no configuration is given as an argument,
    Use the default_config.txt as default
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "config/default_config.txt"


def check_mandatory_keys(config_keys: dict[str, Any]) -> None:
    """
    Check if all the mandatory keys are present and uncommented
    From the config file
    If not: raise an error - The maze can't be generated
    """
    required_k = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_k - config_keys.keys()

    if missing:
        raise ConfigError(
            f"Missing required key(s): {', '.join(missing)}"
        )


def parse_config(file_path: str) -> dict[str, Any]:
    """
    Read and transform the values of config.txt into a dict
    """
    config: dict[str, Any] = {}

    try:
        with open(file_path, "r") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith('#'):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Invalid format on line {i}.")

                key, value = line.split("=", 1)  # maxsplit=1
                key = key.strip()  # Remove extra spaces
                value = value.strip()

                if key in config:
                    raise ConfigError(f"Duplicate key '{key}' on line {i}.")

                config[key] = value
        check_mandatory_keys(config)
        return config

    except FileNotFoundError:
        raise ConfigError(f"File '{file_path}' was not found.")


if __name__ == "__main__":
    try:
        config = parse_config(get_config_path())
        print(config)
    except ConfigError as e:
        print(e)
