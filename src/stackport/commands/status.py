from pathlib import Path

from stackport.runtime.state import State
from stackport.localstack.manager import LocalStackManager


def main():
    state = State()
    current_state = state.load()

    if current_state is None:
        print("Application: STOPPED")
        print("LocalStack: STOPPED")
        raise SystemExit


    # -------------------------
    # Application status
    # -------------------------

    app_state = current_state.get("app")

    if app_state is None:
        print("Application: STOPPED")
    else:
        pid = app_state.get("pid")

        if pid and Path(f"/proc/{pid}").exists():
            print(f"Application: RUNNING (PID: {pid})")
        else:
            print("Application: STOPPED")

            if "app" in current_state:
                current_state.pop("app")

                if current_state:
                    state.save(current_state)
                else:
                    state.clear()

    # -------------------------
    # LocalStack status
    # -------------------------

    localstack = LocalStackManager()

    print(f"LocalStack: {localstack.status()}")

if __name__ == "__main__":
    main()