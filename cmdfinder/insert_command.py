import re
import time
from pathlib import Path
from os import environ

from cmdfinder.db import get_conn
from cmdfinder.logger import logger

SHELL = environ["SHELL"]

ZSH_PATTERN = re.compile(r"^: (\d+):\d+;(.*)$")

def insert_commands_in_db():
    """Store already executed commands to db."""

    insert_query = """
    INSERT INTO commands (command, ts) VALUES (?, ?);
    """

    if "zsh" in SHELL:
        history_file_path = Path("~/.zsh_history").expanduser()

        with open(history_file_path, mode="r", encoding="utf-8", errors="ignore") as f, get_conn() as connection:
            cursor = connection.cursor()

            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                match = ZSH_PATTERN.match(line)
                if match:
                    ts = int(match.group(1))
                    cmd = match.group(2)
                else:
                    ts = int(time.time())
                    cmd = line
                    logger.debug("Zsh line did not match pattern, using current timestamp.")

                cursor.execute(insert_query, (cmd, ts))

        logger.info("Zsh history inserted successfully.")
        return

    elif "bash" in SHELL:
        history_file_path = Path("~/.bash_history").expanduser()

        with open(history_file_path, mode="r", encoding="utf-8", errors="ignore") as f, get_conn() as connection:
            cursor = connection.cursor()

            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                ts = int(time.time())
                cmd = line
                cursor.execute(insert_query, (cmd, ts))

        logger.info("Bash history inserted successfully.")
        return

    else:
        logger.error("Not a valid shell — please use zsh or bash.")
        return


if __name__ == "__main__":
    insert_commands_in_db()
