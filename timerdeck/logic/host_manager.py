# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/host_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import socket

from PythonTools.net.ssh import is_ssh_reachable

class HostManager:
    def __init__(self):
        self.remote_mode = False

    def set_remote_mode(self, enabled: bool):
        """Store remote/local mode state."""
        self.remote_mode = enabled
        return enabled

    def get_hosts(self):
        """Return filtered hostnames from /etc/hosts."""
        hosts = []
        current_host = socket.gethostname()

        with open("/etc/hosts") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue

                raw = raw.split("#", 1)[0].strip()
                parts = raw.split()
                if len(parts) < 2:
                    continue

                ip = parts[0]
                names = parts[1:]
                hostname = names[0]

                if ":" in ip:
                    continue
                if ip.startswith("127."):
                    continue
                if any("localhost" in n for n in names):
                    continue
                if any(current_host == n for n in names):
                    continue

                hosts.append(hostname)

        return sorted(set(hosts))
