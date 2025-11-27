from os import environ
from pathlib import Path

def get_shell_type() -> str:
    shell = environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh"
    if "bash" in shell:
        return "bash"
    return "unknown"

def get_history_path(shell_type: str) -> Path:
    if shell_type == "zsh":
        return Path("~/.zsh_history").expanduser()
    if shell_type == "bash":
        return Path("~/.bash_history").expanduser()
    raise RuntimeError("Unsupported shell")

def detect_shell_and_history():
    shell_type = get_shell_type()
    history_path = get_history_path(shell_type)
    return shell_type, history_path