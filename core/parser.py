def parse(query: str):

    if "현재 위치" in query or "어디" in query:
        return {
            "action": "pwd",
            "target": None,
            "recursive": False
        }

    if "파일 목록" in query:
        return {
            "action": "list_files",
            "target": "current_directory",
            "recursive": False
        }

    if "python 파일" in query:
        return {
            "action": "find_file",
            "target": "*.py",
            "recursive": True
        }
    if "삭제" in query:
        return {
        "action": "delete_all"
        }

    return {
        "action": "unknown"
    }
