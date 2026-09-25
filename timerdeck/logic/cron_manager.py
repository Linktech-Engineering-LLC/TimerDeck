# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/cron_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import getpass
import subprocess

from PythonTools.sessions import LocalSession, SSHSession

class CronManager:
    def load_user_cron(self, user: str, ssh_manager=None):
        # Determine session type
        session = ssh_manager.session if ssh_manager else LocalSession()

        # Determine current user (local or remote)
        current_user = getpass.getuser() if ssh_manager is None else ssh_manager.session.user

        # Build correct command
        if user == current_user:
            cmd = "crontab -l"
        else:
            cmd = f"sudo crontab -u {user} -l"

        # Run command
        output = session.run(cmd)
        # Parse cron lines
        return self._parse_cron(output.msg)

    def _parse_cron(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and not l.startswith("#")
        ]

        parsed = []
        for line in lines:
            parts = line.split(maxsplit=5)
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = parts[5]
            else:
                schedule = line
                command = ""
            parsed.append((schedule, command))

        return parsed