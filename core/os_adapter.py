import platform


def get_os():

    system = platform.system().lower()

    if system == "windows":
        return "windows"

    elif system == "linux":
        return "linux"

    elif system == "darwin":
        return "mac"

    return "unknown"