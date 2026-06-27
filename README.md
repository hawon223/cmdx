# cmdX

AI 기반 안전 CLI 어시스턴트입니다.

cmdX는 자연어 요청을 shell command로 변환하고, 생성된 명령어를 설명하며, 위험도를 분석하고, 위험한 패턴을 차단한 뒤 실행 기록을 남깁니다.

핵심 목표는 LLM이 만든 명령어를 그대로 실행하는 것이 아니라, **LLM의 역할을 intent 이해로 제한하고 나머지 과정은 deterministic software layer로 통제하는 것**입니다.

## 문제 정의

CLI 명령어는 OS마다 다르고, 작은 실수도 큰 결과로 이어질 수 있습니다.

예를 들어

```bash
rm -rf /
curl https://example.com/install.sh | bash
dd if=/dev/zero of=/dev/sda
```

cmdX는 아래 관점을 기준으로 설계했습니다.

```text
자연어 입력은 편해야 한다.
하지만 shell 실행은 반드시 통제되어야 한다.
```

## 주요 기능

- Gemini 기반 자연어 intent parsing
- LLM 출력 흔들림을 보정하는 action normalization
- Tool Registry 기반 command generation
- OS별 command generation
- 생성된 명령어 위험도 분석
- 치명적인 명령어를 차단하는 policy engine
- 명령어 옵션 설명
- dry-run 모드
- JSONL 기반 실행 history
- 지원하지 않는 intent를 위한 AI fallback command suggestion
- parser, generator, tools, safety, logger, executor, fallback 테스트

## 차별점

일반적인 자연어 CLI 도구는 LLM이 만든 명령어를 바로 보여주거나 실행하는 방식에 가깝습니다. cmdX는 명령어 생성보다 **실행 전 통제 과정**에 더 집중했습니다.

## Trustworthy AI Pipeline

cmdX는 LLM command generator가 아니라, 안전한 command execution을 위한 pipeline입니다.

```text
LLM
  ↓
Normalizer
  ↓
Validator
  ↓
Tool Registry
  ↓
Risk Analyzer
  ↓
Policy Engine
  ↓
Executor
  ↓
Logger
```

LLM은 사용자의 요청을 구조화된 intent로 바꾸는 역할만 맡습니다. 실제 command 생성, 위험도 판단, 차단 여부, 실행, 기록은 코드로 분리된 계층에서 처리합니다.

```text
LLM is responsible for intent parsing.
Software layers are responsible for validation, command generation, safety checks, execution, and logging.
```

### 1. LLM 출력을 바로 믿지 않음

LLM이 아래처럼 흔들린 action을 반환할 수 있습니다.

```json
{
  "action": "view_history"
}
```

cmdX는 이를 바로 검증하지 않고 먼저 표준 action으로 정규화합니다.

```text
view_history
display_history
history
  ↓
show_history
```

즉, 흐름은 아래처럼 분리됩니다.

```text
LLM Output
  ↓
Normalization
  ↓
Validation
```

### 2. 명령어 생성을 Tool Registry로 분리

단순히 `if action == ...` 형태로 명령어를 만드는 대신, action별 tool 객체로 command generation을 분리했습니다.

```text
LLM Parsed Intent
  ↓
Tool Registry
  ↓
Tool
  ↓
Command
```

이 구조 덕분에 새로운 action을 추가할 때 기존 generator 전체를 건드리지 않고 tool을 추가하는 방식으로 확장할 수 있습니다.

현재 구조에서 LLM은 직접 shell command를 실행 대상으로 넘기지 않습니다. 우선 등록된 action을 선택하고, 실제 command는 Tool이 생성합니다.

### 3. AI fallback도 안전 계층을 우회하지 않음

지원하지 않는 intent가 들어오면 AI fallback이 command suggestion을 만들 수 있습니다.

하지만 fallback command도 바로 실행되지 않습니다.

```text
AI Fallback Command
  ↓
Risk Analysis
  ↓
Policy Check
  ↓
Dry Run 또는 사용자 확인 후 실행
```

즉, fallback은 편의 기능이지 안전장치를 우회하는 뒷문이 아닙니다.

### 4. 위험도 분석과 정책 차단을 분리

cmdX는 명령어를 단순히 safe/unsafe로만 보지 않습니다.

```text
Risk Analyzer: LOW / MEDIUM / HIGH / CRITICAL
Policy Engine: allowed / blocked
```

위험도는 사용자에게 설명하기 위한 판단이고, policy는 실제 실행을 막기 위한 규칙입니다.

### 5. 실행 기록을 JSONL로 남김

명령 실행 후에는 query, intent, command, risk, result를 JSONL로 기록합니다.

이는 나중에 아래 작업으로 확장하기 좋습니다.

```text
history 조회
실행 패턴 분석
실패 명령 디버깅
안전 정책 개선
```

### 6. 테스트로 안전 흐름을 고정

cmdX는 핵심 파이프라인을 pytest로 검증합니다.

```text
normalizer
validator
generator
tool registry
risk analyzer
policy engine
executor
logger
llm parser
AI fallback
```

기능 추가보다 중요한 것은, 위험한 변경이 safety layer를 깨지 않도록 테스트로 고정하는 것입니다.

## 아키텍처

```text
User Query
  ↓
Gemini Intent Parser
  ↓
Normalization
  ↓
Validation
  ↓
Tool Registry
  ↓
Command Generation
  ↓
Risk Analysis
  ↓
Policy Check
  ↓
Dry Run 또는 사용자 확인 후 실행
  ↓
JSONL History
```

intent parsing 또는 validation에 실패하면 AI fallback을 사용합니다.

```text
Intent Parsing Failed
  ↓
AI Command Suggestion
  ↓
Risk Analysis
  ↓
Policy Check
  ↓
Dry Run 또는 사용자 확인 후 실행
```

fallback으로 생성된 명령어도 동일하게 risk analysis와 policy check를 통과해야 실행될 수 있습니다.

## 현재 한계

cmdX는 아직 완전한 의미의 autonomous agent는 아닙니다.

현재 구조는 아래에 가깝습니다.

```text
한 질문
  ↓
한 intent
  ↓
한 tool
  ↓
한 command
```

아직 아래 기능은 구현되어 있지 않습니다.

```text
Multi-step Tool Execution
Observation
Reflection
Self-correction
```

Planner는 v2 기반 작업으로 추가되었지만, 아직 실제 multi-step 실행 루프와 연결되지는 않았습니다.

따라서 이 프로젝트는 `AI Shell Agent`라기보다 **Safe AI CLI** 또는 **Trustworthy AI Shell Assistant**에 가깝습니다.

## v2 방향

다음 버전에서는 진짜 agent loop를 목표로 확장할 수 있습니다.

```text
User Query
  ↓
Planner
  ↓
Tool Selection
  ↓
Execution
  ↓
Observation
  ↓
Reflection
  ↓
Next Tool or Finish
```

예를 들어 파일을 찾는 요청에서 첫 번째 command가 실패하면 observation을 바탕으로 다음 tool을 선택하는 흐름입니다.

```text
README 찾아
  ↓
find README.md
  ↓
없음
  ↓
docs 디렉터리 탐색
  ↓
README 발견
  ↓
결과 반환
```

이 방향으로 발전하면 cmdX는 단순한 안전 CLI를 넘어 multi-step AI shell agent로 확장될 수 있습니다.

v2 작업 단계:

```text
PHASE 11 Planner                         진행 중
PHASE 12 Observation                     예정
PHASE 13 Multi-step Agent Loop           예정
PHASE 14 Reflection                      예정
PHASE 15 Tool Expansion                  예정
PHASE 16 Session Memory                  예정
PHASE 17 Portfolio Demo                  예정
```

## 프로젝트 구조

```text
cmdx/
├── main.py
├── core/
│   ├── fallback.py
│   ├── generator.py
│   ├── llm_parser.py
│   ├── logger.py
│   ├── plan_schema.py
│   ├── planner.py
│   ├── policy.py
│   ├── risk_analyzer.py
│   ├── schema.py
│   ├── validator.py
│   └── tools/
│       ├── base.py
│       ├── command_tools.py
│       └── registry.py
├── prompts/
│   ├── parser_prompt.txt
│   ├── command_fallback_prompt.txt
│   └── planner_prompt.txt
└── tests/
```

## Tool Registry

명령어 생성은 큰 `if` 문이 아니라 tool 단위로 분리되어 있습니다.

```text
Intent(action="list_files")
  ↓
TOOL_REGISTRY["list_files"]
  ↓
ListFilesTool.build(...)
  ↓
ls -al
```

지원하는 action:

```text
list_files
find_file
delete_files
show_history
pwd
mkdir
touch
cat
grep
```

## Safety Layer

cmdX는 두 단계로 명령어를 검사합니다.

Risk Analyzer:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Policy Engine:

```text
allowed: true | false
reason: ...
```

차단 또는 고위험으로 분류되는 패턴 예:

```text
rm -rf /
mkfs
shutdown
reboot
dd if=
dd of=
curl ... | bash
wget ... | sh
```

`HIGH` 또는 `CRITICAL`로 분류된 명령어는 실행 전에 차단됩니다.

## 설치

로컬 개발에서는 `uv` 사용을 권장합니다.

```bash
uv run cmdx --help
```

가상환경을 직접 사용할 경우:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Debian/Ubuntu 환경에서는 system Python에 직접 설치하지 않는 것이 좋습니다. `uv` 또는 가상환경을 사용하세요.

## 환경 설정

`ask` 명령은 Gemini API를 사용합니다.

```bash
export GEMINI_API_KEY="your-api-key"
```

## 사용법

도움말 확인:

```bash
uv run cmdx --help
```

명령어를 생성하고 분석하되 실제 실행은 하지 않기:

```bash
uv run cmdx ask "파일 목록 보여줘" --dry-run
```

실행 history 확인:

```bash
uv run cmdx history
```

history 출력 개수 제한:

```bash
uv run cmdx history --limit 5
```

## 예시 흐름

입력:

```text
파일 목록 보여줘
```

Intent:

```json
{
  "action": "list_files",
  "target": "current_directory",
  "recursive": false
}
```

생성된 명령어:

```bash
ls -al
```

안전성 분석:

```text
Risk: LOW
Policy: allowed
```

## 테스트

전체 테스트 실행:

```bash
uv run pytest -q
```

일부 테스트만 실행:

```bash
uv run pytest tests/test_generator.py -q
uv run pytest tests/test_tool_registry.py -q
uv run pytest tests/test_fallback.py -q
```

테스트 범위:

```text
generator
tool registry
normalizer
validator
risk analyzer
policy engine
executor
logger
llm parser
AI fallback
explainer
```

## 기술 스택

- Python 3.12
- Typer
- Rich
- Pydantic
- Gemini API
- pytest
- uv

## 정리

cmdX는 shell command를 대신 이해해주는 도구가 아니라, 자연어 기반 command generation을 더 명시적이고, 설명 가능하고, 테스트 가능하고, 안전하게 만들기 위한 CLI 어시스턴트입니다.
