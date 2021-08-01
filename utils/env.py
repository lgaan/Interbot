import os
from typing import Any

import toml


class TomlConfig:
    def __init__(self, json: dict) -> None:
        for k, v in json.items():
            setattr(self, k, v)

    def __getattr__(self, item: Any) -> Any:
        return getattr(self, item)


class TomlReader:
    def __init__(self) -> None:
        self.prod_type = os.getenv("PROD_TYPE", "DEV")

    def read(self, fp: str) -> TomlConfig:
        """Read and return a config from a toml file"""
        contents = toml.load(fp)

        return TomlConfig(contents[self.prod_type])


def load_env(fp: str) -> TomlConfig:
    """Load the environment"""
    return TomlReader().read(fp)
