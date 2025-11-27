import os
import sys
import shutil
from pathlib import Path

from cmdfinder.db.db import init_db
from cmdfinder.db.insert_command import insert_commands_in_db
from cmdfinder.utils.logger import logger

SERVICE_CONTENT = """[Unit]
Description=CmdFinder History Watcher
After=network.target

[Service]
ExecStart={executable}
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""

def install_service():
    """Create and enable a systemd user service for CmdFinder watcher."""
    logger.info("Setting up CmdFinder Watcher Service...")
    init_db()
    insert_commands_in_db()

    # Locate the installed 'cmdfinder-watcher' executable
    watcher_cmd = shutil.which("cmdfinder-watcher")

    if not watcher_cmd:
        # Fallback: check the directory of the current python interpreter
        bin_dir = Path(sys.executable).parent
        candidate = bin_dir / "cmdfinder-watcher"
        if candidate.exists():
            watcher_cmd = str(candidate)

    if not watcher_cmd:
        logger.error("Could not locate 'cmdfinder-watcher' executable.")
        logger.error("Please ensure the package is installed via pip.")
        sys.exit(1)

    # Systemd user service directory
    systemd_dir = Path("~/.config/systemd/user").expanduser()
    service_file = systemd_dir / "cmdfinder.service"

    # Ensure directory exists
    systemd_dir.mkdir(parents=True, exist_ok=True)

    # Write service content
    content = SERVICE_CONTENT.format(executable=watcher_cmd)
    with open(service_file, "w") as f:
        f.write(content)

    logger.info(f"Created systemd service file at: {service_file}")

    # Reload systemd and enable service
    logger.info("Reloading systemd and enabling service...")
    os.system("systemctl --user daemon-reload")
    os.system("systemctl --user enable --now cmdfinder.service")

    logger.info("Setup complete. The watcher is now running in the background.")
    logger.info("Check status using: systemctl --user status cmdfinder.service")

if __name__ == "__main__":
    install_service()