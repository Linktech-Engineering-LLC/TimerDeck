# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/dashboard.py
 Version: 1.0.0
 Description: Description of this module
"""

# timerdeck/widgets/dashboard_widget.py

from PySide6.QtWidgets import QWidget, QGridLayout

from .cards import make_card  # wherever you put make_card

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = QGridLayout(self)
        grid.setSpacing(16)

        grid.addWidget(make_card("Total Timers", "12", "timer.svg"), 0, 0)
        grid.addWidget(make_card("Active Timers", "9", "systemd-user.svg"), 0, 1)
        grid.addWidget(make_card("Failed Timers", "1", "systemd-system.svg"), 1, 0)
        grid.addWidget(make_card("Next Run", "14:30", "cron.svg"), 1, 1)
        grid.addWidget(make_card("Systemd Version", "252.8", "settings.svg"), 2, 0, 1, 2)

