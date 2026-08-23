import shlex
import subprocess
from pathlib import Path


class ProcessManager:
    def __init__(self, command: str):
        self.command = command
        self._process: subprocess.Popen | None = None

        self.log_dir = Path.cwd() / ".stackport" / "logs"
        self.stdout_log = self.log_dir / "app.log"
        self.stderr_log = self.log_dir / "app.error.log"

    def start(self) -> int | None:
        if self.is_running():
            print("Application is already running.")
            return self._process.pid if self._process else None

        self.log_dir.mkdir(parents=True, exist_ok=True)

        try:
            stdout = self.stdout_log.open("a")
            stderr = self.stderr_log.open("a")

            self._process = subprocess.Popen(
                shlex.split(self.command),
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
                text=True,
            )

            print(f"Application started. PID: {self._process.pid}")
            return self._process.pid

        except (OSError, ValueError) as exc:
            self._process = None
            raise RuntimeError(
                f"Failed to start application: {exc}"
            ) from exc

    def stop(self) -> None:
        if not self.is_running():
            print("No active application process.")
            return

        assert self._process is not None

        print("Stopping application...")

        self._process.terminate()

        try:
            self._process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Graceful shutdown failed. Forcing termination...")
            self._process.kill()
            self._process.wait()

        self._process = None
        print("Application stopped.")

    def is_running(self) -> bool:
        return (
            self._process is not None
            and self._process.poll() is None
        )

    def status(self) -> str:
        if self.is_running():
            assert self._process is not None
            return f"RUNNING (PID: {self._process.pid})"

        return "STOPPED"