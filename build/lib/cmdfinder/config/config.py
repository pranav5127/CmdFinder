import re
from pathlib import Path

DB_PATH = Path("~/.cmdfinder.db").expanduser()
OFFSET_FILE = Path("~/.cmdfinder_offset.offset").expanduser()
DEFAULT_SHELL = "zsh"
ZSH_PATTERN = re.compile(r"^: (\d+):\d+;(.*)$")