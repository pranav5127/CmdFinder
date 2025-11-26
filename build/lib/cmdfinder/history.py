from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re

from rapidfuzz import process, fuzz


@dataclass
class HistoryEntry:
    command: str
    timestamp: datetime | None = None


def load_history() -> list[HistoryEntry]:
    """Load shell history (zsh or bash), with timestamps when available."""
    history_files = [
        Path("~/.zsh_history").expanduser(),
        Path("~/.bash_history").expanduser(),
    ]

    for path in history_files:
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()

        entries: list[HistoryEntry] = []

        for line in lines:
            if line.startswith(": "):
                m = re.match(r"^: (\d+):\d+;(.*)", line)
                if m:
                    ts = datetime.fromtimestamp(int(m.group(1)))
                    cmd = m.group(2).strip()
                    if cmd:
                        entries.append(HistoryEntry(command=cmd, timestamp=ts))
                    continue

            cmd = line.strip()
            if cmd:
                entries.append(HistoryEntry(command=cmd, timestamp=None))

        seen = set()
        unique: list[HistoryEntry] = []
        for e in entries:
            key = (e.timestamp, e.command)
            if key not in seen:
                seen.add(key)
                unique.append(e)
        return unique

    return [HistoryEntry(command="echo 'No history file found'", timestamp=None)]


def fuzzy_search(query: str, entries: list[HistoryEntry], limit: int = 80) -> list[HistoryEntry]:
    query = query.strip()
    if not query:
        return list(reversed(entries[-limit:]))

    q_lower = query.lower()
    words = q_lower.split()

    substring_matches: list[HistoryEntry] = []
    for e in entries:
        cmd_lower = e.command.lower()
        if all(w in cmd_lower for w in words):
            substring_matches.append(e)

    if substring_matches:
        return list(reversed(substring_matches))[:limit]

    commands = [e.command for e in entries]
    results = process.extract(
        query,
        commands,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=80,
    )

    return [entries[idx] for _, _, idx in results]
