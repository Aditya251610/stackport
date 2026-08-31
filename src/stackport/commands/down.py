import os
import signal
from pathlib import Path

from stackport.runtime.state import State
from stackport.localstack.manager import LocalStackManager


def main():
    state = State(Path(".stackport/state.json"))
    current_state = state.load()

    if current_state is None:
        print("No application state found.")
        raise SystemExit


    # -------------------------
    # Stop application
    # -------------------------

    app_state = current_state.get("app")

    if app_state is not None:
        pid = app_state.get("pid")

        if pid is not None:
            try:
                if Path(f"/proc/{pid}").exists():
                    print(f"Stopping application with PID: {pid}")

                    os.kill(pid, signal.SIGTERM)

                    print("Application stopped.")

                else:
                    print(f"Process {pid} is no longer running.")

            except ProcessLookupError:
                print(f"Process {pid} is no longer running.")

            except PermissionError:
                print(f"Permission denied while stopping process {pid}.")

            except Exception as exc:
                print(f"Error stopping application: {exc}")


    # -------------------------
    # Stop LocalStack
    # -------------------------

    localstack_state = current_state.get("localstack")

    if localstack_state is not None:
        try:
            localstack = LocalStackManager()

            if localstack.status() == "RUNNING":
                localstack.stop()
            else:
                print("LocalStack is not running.")

        except Exception as exc:
            print(f"Error stopping LocalStack: {exc}")


    # -------------------------
    # Clear state
    # -------------------------

    state.clear()

    print("Stackport stopped.")

if __name__ == "__main__":
    main()