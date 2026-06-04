import subprocess
import time


def execute(command: str):
    started_at = time.perf_counter()

    try:

        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True
        )
        execution_time = round(time.perf_counter() - started_at, 4)

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time": execution_time,
            "error": None
        }

    except Exception as e:
        execution_time = round(time.perf_counter() - started_at, 4)

        return {
            "success": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "execution_time": execution_time,
            "error": str(e)
        }
