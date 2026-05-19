import typer

from core.parser import parse
from core.generator import generate

app = typer.Typer()

@app.command()
def ask(query: str):
    intent = parse(query)

    command = generate(intent)

    print(f"Intent: {intent}")
    print(f"Command: {command}")

if __name__ == "__main__":
    app()