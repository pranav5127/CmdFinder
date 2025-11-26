from pathlib import Path
from rapidfuzz import process, fuzz

def load_history() -> list[str]:
    candidates = [
        Path("~/.bash_history").expanduser(),
        Path("~/.zsh_history").expanduser()
    ]

    for path in candidates:
        if path.exists():
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f if line.strip()]

            # remove duplicates
            seen = set()
            unique = []

            for cmd in lines:
                if cmd not in seen:
                    seen.add(cmd)
                    unique.append(cmd)

            return unique

    return ["echo 'No history file found'"]


