import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.agent import run_agent
from core.llm_parser import parse_with_gemini
from core.fallback import suggest_command_with_gemini
from core.generator import generate
from core.risk_analyzer import analyze
from core.executor import execute
from core.validator import validate_intent
from core.explainer import explain
from core.policy import check_policy
from core.logger import log_command, read_history

app = typer.Typer()
console = Console()


@app.command()
def history(
    limit: int = typer.Option(
        10,
        "--limit",
        "-n",
        help="Number of history entries to show."
    )
):
    entries = read_history(limit=limit)

    if not entries:
        console.print("[bold yellow]No history found[/bold yellow]")
        return

    table = Table(title="Command History")
    table.add_column("#", justify="right", style="bold cyan")
    table.add_column("Time", style="white")
    table.add_column("Risk", style="magenta")
    table.add_column("Success", style="green")
    table.add_column("Command", style="white")

    for index, entry in enumerate(entries, start=1):
        result = entry.get("result", {})
        success = result.get("success")

        if success is True:
            success_text = "yes"
        elif success is False:
            success_text = "no"
        else:
            success_text = "-"

        table.add_row(
            str(index),
            entry.get("timestamp", ""),
            entry.get("risk", ""),
            success_text,
            entry.get("command", "")
        )

    console.print(table)


@app.command()
def agent(
    query: str,
    execute_steps: bool = typer.Option(
        False,
        "--execute",
        help="Execute each safe planned step. Defaults to dry-run."
    ),
    max_steps: int = typer.Option(
        3,
        "--max-steps",
        help="Maximum number of plan steps to process."
    )
):
    try:
        result = run_agent(
            query=query,
            dry_run=not execute_steps,
            max_steps=max_steps
        )
    except Exception as e:
        console.print(
            Panel(
                Text(str(e), style="bold white"),
                title="Agent Error",
                border_style="red",
            )
        )
        return

    summary = Table.grid(padding=(0, 1), expand=True)
    summary.add_column("Field", style="bold blue")
    summary.add_column("Value", style="white")
    summary.add_row("Goal", result.goal)
    summary.add_row("Mode", "execute" if execute_steps else "dry-run")
    summary.add_row("Completed", str(result.completed))
    if result.stopped_reason:
        summary.add_row("Stopped Reason", result.stopped_reason)
    console.print(Panel(summary, title="Agent Plan", border_style="blue"))

    table = Table(title="Agent Steps")
    table.add_column("#", justify="right", style="bold cyan")
    table.add_column("Action", style="white")
    table.add_column("Status", style="magenta")
    table.add_column("Risk", style="yellow")
    table.add_column("Command", style="white")

    for step in result.steps:
        table.add_row(
            str(step.step_index),
            step.action,
            step.status,
            step.risk,
            step.command
        )

    console.print(table)

    for step in result.steps:
        if step.observation:
            console.print(
                Panel(
                    step.observation.summary,
                    title=f"Observation #{step.step_index}",
                    border_style="green" if step.observation.success else "red"
                )
            )

@app.command()
def ask(
    query: str,
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show the generated command without executing it."
    )
):
    fallback_used = False

    try:
        intent = parse_with_gemini(query)
        validate_intent(intent)
        command = generate(intent)
    except Exception as e:
        try:
            command = suggest_command_with_gemini(query)
            fallback_used = True
            intent = {
                "action": "ai_fallback",
                "reason": str(e)
            }
        except Exception as fallback_error:
            error_message = (
                f"Intent error: {e}\n\n"
                f"Fallback error: {fallback_error}"
            )
            console.print(
                Panel(
                    Text(error_message, style="bold white"),
                    title="Intent Validation Error",
                    border_style="red",
                )
            )
            return


    risk_result = analyze(command)

    intent_table = Table.grid(padding=(0, 1), expand=True)
    intent_table.add_column("Field", style="bold blue")
    intent_table.add_column("Value", style="white")
    if fallback_used:
        intent_table.add_row("Action", intent["action"])
        intent_table.add_row("Reason", intent["reason"])
        intent_table.add_row("Source", "AI Fallback")
    else:
        intent_table.add_row("Action", intent.action)
        intent_table.add_row("Target", str(intent.target))
        intent_table.add_row("Recursive", str(intent.recursive))
    console.print(
        Panel(
            intent_table,
            title="Fallback Intent" if fallback_used else "Intent",
            border_style="blue"
        )
    )

    risk_styles = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "bold red",
        "CRITICAL": "bold white on red"
    }
    risk_text = (
        f"[{risk_styles[risk_result['risk']]}]"
        f"{risk_result['risk']}"
        f"[/{risk_styles[risk_result['risk']]}]"
    )

    summary = Table.grid(padding=(0, 1), expand=True)
    summary.add_column("Field", style="bold magenta")
    summary.add_column("Value", style="white")
    summary.add_row("Command", command)
    summary.add_row("Risk", risk_text)
    summary.add_row("Reason", risk_result["reason"])
    console.print(Panel(summary, title="Analysis", border_style="yellow"))

    explanations = explain(command)
    if explanations:
        explain_table = Table.grid(padding=(0, 2))
        explain_table.add_column(style="bold cyan")
        explain_table.add_column(style="white")
        for option, desc in explanations.items():
            explain_table.add_row(option, desc)
        console.print(
            Panel.fit(
                explain_table,
                title="Command Explanation",
                border_style="green"
            )
        )

    policy_result = check_policy(command)
    if not policy_result["allowed"]:
        blocked_message = (
            f"Command: {command}\n\n"
            f"Reason:\n{policy_result['reason']}"
        )
        console.print(
            Panel(
                Text(blocked_message, style="bold white"),
                title="Policy Blocked",
                border_style="red",
            )
        )
        return

    if risk_result["risk"] in ["HIGH", "CRITICAL"]:
        blocked_message = (
            f"Command: {command}\n\n"
            f"Reason:\n{risk_result['reason']}"
        )
        console.print(
            Panel(
                Text(blocked_message, style="bold white"),
                title="Blocked",
                border_style="red",
            )
        )
        return

    if dry_run:
        console.print(
            Panel(
                Text(command, style="bold white"),
                title="Dry Run",
                border_style="cyan",
            )
        )
        return

    confirm = console.input("\n[bold green]실행하시겠습니까? (y/n): [/bold green]")

    if confirm.lower() != "y":
        console.print("[bold yellow]실행 취소[/bold yellow]")
        return

    result = execute(command)
    log_command(
        query=query,
        intent=intent,
        command=command,
        risk=risk_result["risk"],
        result=result
    )

    console.print(Panel(Text("Execution Result", style="bold white"), border_style="green"))

    if result["success"]:
        if result["stdout"]:
            console.print(Panel(result["stdout"], title="stdout", border_style="green"))
        if result["stderr"]:
            console.print(Panel(result["stderr"], title="stderr", border_style="red"))
    elif result["stderr"]:
        console.print(Panel(result["stderr"], title="stderr", border_style="red"))
    else:
        error_message = result["error"] or (
            f"Command failed with return code {result['returncode']}"
        )
        console.print(Panel(error_message, title="Error", border_style="red"))

if __name__ == "__main__":
    app()
