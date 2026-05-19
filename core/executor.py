import subprocess


def execute(command: str):

    try:

        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True
        )

        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }