# cmdX

AI 기반 CLI 어시스턴트

## Problem

OS마다 명령어가 다르고,
위험한 명령어 실행 실수가 발생할 수 있다.

## Goal

자연어를 기반으로 안전한 CLI 명령어를 생성하고,
위험도를 분석하여 실행을 보조한다.

## Features

- Natural Language → CLI
- OS-specific command generation
- Risk analysis
- Command explanation

## Installation

Recommended for local development:

```bash
uv run cmdx --help
```

If you prefer a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
uv run cmdx ask "파일 목록 보여줘" --dry-run
uv run cmdx history
```

`ask` uses the Gemini API, so set `GEMINI_API_KEY` before running it.

```bash
export GEMINI_API_KEY="your-api-key"
```

## Tech Stack

- Python
- Typer
- Gemini API
- Rich

## Architecture

Input
→ Intent Parsing
→ Command Generation
→ Validation
→ Risk Analysis
→ Execution
