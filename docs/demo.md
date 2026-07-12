# cmdX Demo

핵심 메시지는 단순합니다.

```text
LLM이 shell command를 직접 실행하지 않는다.
LLM은 intent를 고르고, cmdX의 deterministic layer가 검증/생성/분석/실행한다.
```

## 1. 기본 명령어 생성

자연어 요청을 안전한 command 후보로 바꿉니다.

```bash
uv run cmdx ask "파일 목록 보여줘" --dry-run
```

예상 흐름은 아래와 같다

```text
User Query
  ↓
Intent(action="list_files")
  ↓
Tool Registry
  ↓
ls -al
  ↓
Risk: LOW
```

이 시나리오에서 보여줄 점

- LLM 출력은 바로 실행되지 않음
- intent validation 이후 등록된 tool이 command를 생성함
- dry-run으로 실제 실행 전에 결과를 확인할 수 있음

## 2. Multi-step Agent

Planner가 하나의 요청을 여러 step으로 나눕니다.

```bash
uv run cmdx agent "README 찾아서 보여줘"
```

예상 흐름은 아래와 같다.

```text
User Query
  ↓
Plan
  ↓
find_file README.md
  ↓
cat README.md
```

이 시나리오에서 보여줄 점

- 한 요청이 여러 tool step으로 분리됨
- 각 step마다 risk와 policy check가 적용됨
- 실행 결과는 Observation으로 구조화됨

## 3. Git Workflow

```bash
uv run cmdx agent "현재 브랜치와 변경사항 요약 보여줘"
```

예상 step:

```text
git_branch
  ↓
git branch --show-current

git_diff
  ↓
git diff --stat
```

이 시나리오에서 보여줄 점

- git 관련 요청도 shell command 문자열이 아니라 tool action으로 표현됨
- `git_branch`, `git_diff` 같은 작은 tool을 조합해 확장 가능함

## 4. File Inspection

파일을 전부 출력하지 않고 필요한 일부만 확인합니다.

```bash
uv run cmdx agent "README 앞부분을 보고 줄 수도 세줘"
```

예상 step

```text
head README.md
  ↓
head -n 10 README.md

wc README.md
  ↓
wc -l README.md
```

이 시나리오에서 보여줄 점

- 작은 단위의 read-only tool을 조합함
- 파일 탐색/검토 작업에 안전하게 사용할 수 있음

## 5. Safety Blocking

위험한 명령어는 policy layer에서 차단됩니다.

```bash
uv run cmdx ask "루트 디렉토리 전부 삭제해줘" --dry-run
```

예상 흐름

```text
Dangerous command candidate
  ↓
Risk Analyzer
  ↓
Risk: HIGH or CRITICAL
  ↓
Policy Engine
  ↓
BLOCKED
```

이 시나리오에서 보여줄 점

- safety layer가 LLM 결과보다 뒤에 항상 존재함
- 위험도 분석과 policy decision이 분리되어 있음
- 실행 전에 차단 이유를 설명할 수 있음

## 6. Session Memory

실행 중 만들어진 Observation은 Session Memory에 누적됩니다.

```text
Step 1 Observation
  ↓
Session Memory
  ↓
Reflection Prompt Context
```

이 시나리오에서 보여줄 점

- 실패한 step 하나만 보는 것이 아니라 이전 실행 맥락을 함께 볼 수 있음
- reflection이 다음 행동을 판단할 때 최근 observation summary를 참고할 수 있음

## 7. Self-correction Loop

실패한 step에 대해 reflection이 `retry`와 `next_step`을 반환하면, agent는 해당 step을 실행 큐에 다시 넣습니다.

```text
Step failed
  ↓
Observation
  ↓
Reflection(status="retry", next_step=...)
  ↓
Retry next_step
```

이 시나리오에서 보여줄 점

- 실패가 곧바로 종료로 이어지지 않음
- reflection 결과가 실제 다음 실행으로 연결됨
- `max_steps` 안에서 retry loop가 통제됨

## 8. Agent Result UX

agent 실행 결과는 step 목록뿐 아니라 retry 횟수와 Session Memory 요약도 함께 보여줍니다.

```text
Agent Plan
- Goal
- Mode
- Completed
- Steps
- Retries

Agent Steps
- action
- status
- risk
- command

Session Memory
- recent observation summaries
```

이 시나리오에서 보여줄 점

- multi-step 실행 결과를 한눈에 볼 수 있음
- retry가 발생했는지 확인할 수 있음
- observation context가 사용자에게도 노출됨

```text
cmdX는 LLM에게 command 실행 권한을 직접 주지 않고, intent parsing과 planning만 맡긴 뒤 deterministic safety pipeline과 self-correction loop를 통해 실행 가능성을 판단하는 Safe AI CLI입니다.
```
