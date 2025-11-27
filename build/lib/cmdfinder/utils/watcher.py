import sys
import time
from pygtail import Pygtail
from cmdfinder.config.config import ZSH_PATTERN, OFFSET_FILE
from cmdfinder.db.db import get_conn
from cmdfinder.utils.logger import logger
from cmdfinder.utils.shell_utils import detect_shell_and_history

try:
    SHELL_TYPE, HISTORY_FILE = detect_shell_and_history()
except RuntimeError as exc:
    logger.error(f"Cannot start watcher: {exc}")
    sys.exit(1)

def watch():
    """Watch history file and push new commands to DB every 5 sec."""
    insert_query = "INSERT INTO commands (command, ts) VALUES (?, ?);"

    while True:
        # One DB connection per polling cycle
        with get_conn() as connection:
            cursor = connection.cursor()

            # Pygtail reads only *new* lines since last offset
            for raw_line in Pygtail(
                    str(HISTORY_FILE),
                    offset_file=str(OFFSET_FILE),
                    read_from_end=True,
            ):
                line = raw_line.rstrip("\n")

                if not line.strip():
                    continue

                sys.stdout.write(line + "\n")
                sys.stdout.flush()

                if SHELL_TYPE == "zsh":
                    match = ZSH_PATTERN.match(line)
                    if match:
                        ts = int(match.group(1))
                        cmd = match.group(2)
                    else:
                        ts = int(time.time())
                        cmd = line
                        logger.debug(
                            "Zsh line did not match pattern, using current timestamp."
                        )
                else:
                    ts = int(time.time())
                    cmd = line

                cursor.execute(insert_query, (cmd, ts))

        logger.info("Flushed new history lines to DB.")
        time.sleep(5)

