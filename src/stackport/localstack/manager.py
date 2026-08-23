import subprocess
from pathlib import Path


class LocalStackManager:
    def __init__(self):
        self.log_dir = Path.cwd() / ".stackport" / "logs"
        self.stdout_log = self.log_dir / "localstack.log"
        self.stderr_log = self.log_dir / "localstack.error.log"

    def start(self) -> bool:
        if self.is_running():
            print("LocalStack is already running.")
            return True

        self.log_dir.mkdir(parents=True, exist_ok=True)

        try:
            with (
                self.stdout_log.open("a") as stdout,
                self.stderr_log.open("a") as stderr,
            ):
                result = subprocess.run(
                    ["localstack", "start", "-d"],
                    stdout=stdout,
                    stderr=stderr,
                    text=True,
                    check=False,
                )

            if result.returncode != 0:
                raise RuntimeError(
                    "Failed to start LocalStack. "
                    f"Check {self.stderr_log} for details."
                )

            if not self.is_running():
                raise RuntimeError(
                    "LocalStack start command completed, "
                    "but LocalStack is not running."
                )

            print("LocalStack started.")
            return True

        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute LocalStack CLI: {exc}"
            ) from exc

    def stop(self) -> None:
        if not self.is_running():
            print("LocalStack is not running.")
            return

        try:
            result = subprocess.run(
                ["localstack", "stop"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to stop LocalStack: {result.stderr.strip()}"
                )

            print("LocalStack stopped.")

        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute LocalStack CLI: {exc}"
            ) from exc

    def is_running(self) -> bool:
        result = subprocess.run(
            ["localstack", "status"],
            capture_output=True,
            text=True,
            check=False,
        )

        return "running" in result.stdout.lower()

    def status(self) -> str:
        result = subprocess.run(
            ["localstack", "status"],
            capture_output=True,
            text=True,
            check=False,
        )

        output = result.stdout.strip()

        if "running" in output.lower():
            return "RUNNING"

        return "STOPPED"