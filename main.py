import typer

from core.llm_parser import parse_with_gemini
from core.generator import generate
from core.risk_analyzer import analyze
from core.executor import execute

app = typer.Typer()


@app.command()
def ask(query: str):

    intent = parse_with_gemini(query)

    command = generate(intent)

    risk_result = analyze(command)

    print(f"\nIntent: {intent}")
    print(f"Command: {command}")
    print(f"Risk: {risk_result['risk']}")
    print(f"Reason: {risk_result['reason']}")

    if risk_result["risk"] == "HIGH":
        print("\nHIGH RISK COMMAND 차단됨")
        return

    confirm = input("\n실행하시겠습니까? (y/n): ")

    if confirm.lower() != "y":
        print("실행 취소")
        return

    result = execute(command)

    print("\n=== RESULT ===")

    if result["success"]:

        print(result["stdout"])

        if result["stderr"]:
            print(result["stderr"])

    else:
        print(result["error"])


if __name__ == "__main__":
    app()