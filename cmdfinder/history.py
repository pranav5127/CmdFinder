from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List

from rapidfuzz import process, fuzz
from cmdfinder.db.db import get_conn


@dataclass
class HistoryEntry:
    command: str
    timestamp: datetime | None = None


def _rows_to_entries(rows: Iterable[tuple]) -> List[HistoryEntry]:
    """Convert (command, ts) rows to HistoryEntry list, deduplicated."""
    entries: list[HistoryEntry] = []
    seen: set[tuple[str, int | None]] = set()

    for command, ts in rows:
        if ts is not None:
            try:
                ts_int = int(ts)
                ts_dt: datetime | None = datetime.fromtimestamp(ts_int)
            except (ValueError, OSError, TypeError):
                ts_dt = None
                ts_int = None
        else:
            ts_dt = None
            ts_int = None

        key = (command, ts_int)
        if key in seen:
            continue
        seen.add(key)

        entries.append(HistoryEntry(command=command, timestamp=ts_dt))

    return entries


def load_history(limit: int = 50) -> list[HistoryEntry]:
    """
    Load the most recent `limit` commands from the DB.

    Results are ordered with the newest command first.
    """
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT command, ts FROM commands ORDER BY id DESC LIMIT ?;",
            (limit,),
        )
        rows = cursor.fetchall()

    if not rows:
        return [HistoryEntry(command="echo 'No commands indexed yet'")]

    return _rows_to_entries(rows)


def fuzzy_search(
        query: str,
        limit: int = 50,
) -> list[HistoryEntry]:
    """
    Search commands using the DB.

    - If query is empty: return last `limit` commands (newest first).
    - First try a multi-word substring search in SQL:
        all words must appear in LOWER(command).
    - If that returns nothing, fall back to fuzzy matching over the
      last N commands (loaded from the DB).
    """
    query = query.strip()
    if not query:
        return load_history(limit)

    q_lower = query.lower()
    words = q_lower.split()

    # ----------  Multi-word substring search via SQL ----------
    where_clauses = ["LOWER(command) LIKE ?"] * len(words)
    where = " AND ".join(where_clauses)
    params = [f"%{w}%" for w in words]

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT command, ts
            FROM commands
            WHERE {where}
            ORDER BY id DESC
            LIMIT ?
            """,
            (*params, limit * 3),
        )
        rows = cursor.fetchall()

    candidates = _rows_to_entries(rows)
    if candidates:
        return candidates[:limit]

    # ----------  Fallback: fuzzy match last N commands ----------
    base = load_history(2000)
    if not base:
        return []

    commands = [e.command for e in base]

    results = process.extract(
        query,
        commands,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=70,
    )

    # results: list of (command_str, score, index)
    return [base[idx] for _, _, idx in results]
