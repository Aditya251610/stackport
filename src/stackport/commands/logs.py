from pathlib import Path


LOG_FILE = Path(".stackport/logs/app.log")


def main() -> None:
    if not LOG_FILE.exists():
        print("No application logs found.")
        return

    print(f"File: {LOG_FILE}")
    print()

    with LOG_FILE.open("r") as log_file:
        content = log_file.read()

    if content:
        print(content, end="")
    else:
        print("No logs available.")


if __name__ == "__main__":
    main()