# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/systemd_manager.py
 Version: 1.0.0
 Description: Description of this module
"""

from PythonTools.sessions import LocalSession, SystemdRunner

class SystemdManager:
    def __init__(self):
        # Default scope is personal (user-level systemd)
        self.active_scope = "personal"

    def set_scope(self, scope: str):
        """Set the active systemd scope."""
        if scope not in ("personal", "system"):
            scope = "system"

        self.active_scope = scope
        return scope

    def get_scope(self):
        """Return the current systemd scope."""
        return self.active_scope

    # Placeholder for future systemd timer loading
    def load_timers(self, ssh_manager=None):
        session = ssh_manager.session if ssh_manager else LocalSession()
        runner = SystemdRunner(session=session)
        return runner.list_timers(scope=self.active_scope)
