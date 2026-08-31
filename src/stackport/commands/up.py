from stackport.config.loader import yaml_validator
from stackport.localstack.manager import LocalStackManager
from stackport.runtime.process import ProcessManager
from stackport.runtime.state import State

def main():
    config = yaml_validator()

    if config is not None:
        state = State()

        # Start LocalStack
        localstack = LocalStackManager()
        localstack.start()

        # Start application
        process = ProcessManager(config.app.command)
        pid = process.start()

        if pid is not None:
            state.save({
                "app": {
                    "pid": pid,
                    "status": "running",
                },
                "localstack": {
                    "status": localstack.status().lower(),
                },
            })

if __name__ == "__main__":
    main()