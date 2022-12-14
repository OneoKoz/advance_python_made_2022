from dataclasses import dataclass
import yaml

CONF_FILE_PATH = "../conf/conf.yaml"


@dataclass
class Config:
    host: str
    port: int
    encoding: str
    timeout: int


def get_data() -> Config:
    with open(CONF_FILE_PATH, "r", encoding='utf-8') as stream:
        try:
            return Config(**yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    return None
