import yaml
from pathlib import Path
from stackport.models.loader import LoaderConfig

path = Path(__file__).resolve().parents[1] / "stackport.yaml"

with open(path, "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def yaml_validator():
    try:
        loader_config = LoaderConfig(**config)
        print("Validation successful!")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        loader_config = None
    return loader_config
