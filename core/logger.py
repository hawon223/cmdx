from datetime import datetime
import os


def log_command(
    query,
    intent,
    command,
    risk
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_text = f"""
[{timestamp}]

Query:
{query}

Intent:
{intent.action}

Command:
{command}

Risk:
{risk}

-----------------------------------
"""

    os.makedirs("logs", exist_ok=True)

    with open(
        "logs/history.log",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(log_text)

    return True
