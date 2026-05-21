# josn, DB, vector search로 확장 가능

EXPLANATIONS = {

    "ls": {
        "-a": "숨김 파일 포함",
        "-l": "상세 정보 출력"
    },

    "rm": {
        "-r": "하위 디렉토리 포함 삭제",
        "-f": "강제 삭제"
    },

    "find": {
        "-name": "파일 이름 기준 검색"
    }
}

def explain(command: str):

    tokens = command.split()

    if not tokens:
        return {}

    base_command = tokens[0]

    if base_command not in EXPLANATIONS:
        return {}

    explanations = {}

    for token in tokens[1:]:

        # short option bundle 처리
        # 예: -al -> -a, -l

        if token.startswith("-") and not token.startswith("--"):

            if len(token) > 2:

                for char in token[1:]:

                    short_option = f"-{char}"

                    if short_option in EXPLANATIONS[base_command]:

                        explanations[short_option] = (
                            EXPLANATIONS[base_command][short_option]
                        )

                continue

        # 일반 옵션 처리

        if token in EXPLANATIONS[base_command]:

            explanations[token] = (
                EXPLANATIONS[base_command][token]
            )

    return explanations