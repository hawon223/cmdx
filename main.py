import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.llm_parser import parse_with_gemini
from core.generator import generate
from core.risk_analyzer import analyze
from core.executor import execute
from core.validator import validate_intent

app = typer.Typer()
console = Console()

@app.command()
def ask(query: str):
    
    try:
        intent = parse_with_gemini(query)
        validate_intent(intent)
    except Exception as e:
        console.print(
            Panel(
                Text(str(e), style="bold white"),
                title="Intent Validation Error",
                border_style="red",
            )
        )
        return


    command = generate(intent)
    risk_result = analyze(command)

    intent_table = Table.grid(padding=(0, 1), expand=True)
    intent_table.add_column("Field", style="bold blue")
    intent_table.add_column("Value", style="white")
    intent_table.add_row("Action", intent.action)
    intent_table.add_row("Target", str(intent.target))
    intent_table.add_row("Recursive", str(intent.recursive))
    console.print(Panel(intent_table, title="Intent", border_style="blue"))

    summary = Table.grid(padding=(0, 1), expand=True)
    summary.add_column("Field", style="bold magenta")
    summary.add_column("Value", style="white")
    summary.add_row("Command", command)
    summary.add_row("Risk", risk_result["risk"])
    summary.add_row("Reason", risk_result["reason"])
    console.print(Panel(summary, title="Analysis", border_style="yellow"))

    if risk_result["risk"] == "HIGH":
        console.print(
            Panel(
                Text("HIGH RISK COMMAND 차단됨", style="bold white"),
                title="Blocked",
                border_style="red",
            )
        )
        return

    confirm = console.input("\n[bold green]실행하시겠습니까? (y/n): [/bold green]")

    if confirm.lower() != "y":
        console.print("[bold yellow]실행 취소[/bold yellow]")
        return

    result = execute(command)

    # console.print(Panel(Text("RESULT", style="bold white"), border_style="green"))

    if result["success"]:

        if result["stdout"]:
            console.print(Panel(result["stdout"], title="stdout", border_style="green"))

        if result["stderr"]:
            console.print(Panel(result["stderr"], title="stderr", border_style="red"))

    else:
        console.print(Panel(result["error"], title="Error", border_style="red"))


if __name__ == "__main__":
    app()