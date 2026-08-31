import typer

from stackport.commands import (
    up as up_command,
    down as down_command,
    status as status_command,
    logs as logs_command,
)

app = typer.Typer()


@app.command()
def up():
    up_command.main()


@app.command()
def down():
    down_command.main()


@app.command()
def status():
    status_command.main()


@app.command()
def logs():
    logs_command.main()


if __name__ == "__main__":
    app()