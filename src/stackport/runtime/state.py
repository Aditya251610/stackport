import json
from pathlib import Path


class State:
    def __init__(self, state_file: Path | None = None):
        self.state_file = state_file or (Path.cwd() / ".stackport" / "state.json")

    def save(self, state_data: dict) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        with self.state_file.open("w") as f:
            json.dump(state_data, f, indent=4)

    def load(self) -> dict | None:
        if not self.state_file.exists():
            return None

        with self.state_file.open("r") as f:
            return json.load(f)

    def update(self, key: str, value) -> None:
        state_data = self.load() or {}
        state_data[key] = value
        self.save(state_data)

    def clear(self) -> None:
        if self.state_file.exists():
            self.state_file.unlink()