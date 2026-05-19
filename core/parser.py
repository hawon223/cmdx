def parse(query: str):

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