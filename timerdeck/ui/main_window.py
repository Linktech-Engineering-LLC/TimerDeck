# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-05-16
 File: timerdeck/ui/main_window.py
 Version: 1.0.0
 Description: Main Window Orchestrator
"""

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QSplitter,
    QStackedWidget, QLabel, QToolBar,
    QMessageBox, QGridLayout, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon

from .helpers import icon, make_card

class MainWindow(QMainWindow):
    request_close = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TimerDeck")
        self.resize(1100, 700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.statusBar().showMessage("Ready")
        self.request_close.connect(self.handle_close_request)

        # --- Main splitter (sidebar + content) ---
        splitter = QSplitter(Qt.Horizontal)

        # --- Sidebar ---
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)

        btn_dashboard = QPushButton("Dashboard")
        btn_user_systemd = QPushButton("Personal Systemd")
        btn_system_systemd = QPushButton("System Systemd")
        btn_cron = QPushButton("Cron Jobs")

        btn_close = QPushButton("Close TimerDeck")
        btn_close.setIcon(QIcon.fromTheme("application-exit"))
        btn_close.clicked.connect(self.request_close.emit)

        btn_dashboard.setIcon(icon("dashboard.svg"))
        btn_user_systemd.setIcon(icon("systemd-user.svg"))
        btn_system_systemd.setIcon(icon("systemd-system.svg"))
        btn_cron.setIcon(icon("cron.svg"))
        btn_close.setIcon(icon("exit.svg"))

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_user_systemd)
        sidebar_layout.addWidget(btn_system_systemd)
        sidebar_layout.addWidget(btn_cron)
        sidebar_layout.addWidget(btn_close)
        sidebar_layout.addStretch()

        # --- Tool Bar ---
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        # Example actions
        refresh_action = QAction(icon("refresh.svg"), "Refresh", self)
        settings_action = QAction(icon("settings.svg"), "Settings", self)
        help_action = QAction(icon("help.svg"), "Help", self)

        toolbar.addAction(refresh_action)
        toolbar.addAction(settings_action)
        toolbar.addAction(help_action)
        # --- Main content area ---
        self.stack = QStackedWidget()

        # Dashboard view
        dashboard = QWidget()
        grid = QGridLayout(dashboard)
        grid.setSpacing(16)

        grid.addWidget(make_card("Total Timers", "12", "timer.svg"), 0, 0)
        grid.addWidget(make_card("Active Timers", "9", "systemd-user.svg"), 0, 1)
        grid.addWidget(make_card("Failed Timers", "1", "systemd-system.svg"), 1, 0)
        grid.addWidget(make_card("Next Run", "14:30", "cron.svg"), 1, 1)
        grid.addWidget(make_card("Systemd Version", "252.8", "settings.svg"), 2, 0, 1, 2)

        # Personal Systemd view
        user_systemd_view = QLabel(
            "Personal Systemd Units\n\n"
            "List of user-mode systemd timers/services will appear here."
        )
        user_systemd_view.setAlignment(Qt.AlignCenter)

        # System Systemd view
        system_systemd_view = QLabel(
            "System Systemd Units\n\n"
            "List of system-mode systemd timers/services will appear here."
        )
        system_systemd_view.setAlignment(Qt.AlignCenter)

        # Cron Jobs view
        cron_view = QLabel(
            "Cron Jobs\n\n"
            "List of cron jobs will appear here."
        )
        cron_view.setAlignment(Qt.AlignCenter)

        # Add views to stack
        self.stack.addWidget(dashboard)            # index 0
        self.stack.addWidget(user_systemd_view)    # index 1
        self.stack.addWidget(system_systemd_view)  # index 2
        self.stack.addWidget(cron_view)            # index 3

        # Connect sidebar buttons to stack switching
        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_user_systemd.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_system_systemd.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_cron.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        # Add widgets to splitter
        splitter.addWidget(sidebar)
        splitter.addWidget(self.stack)

        # Set initial sizes
        splitter.setSizes([220, 880])

        # Set splitter as central widget
        self.setCentralWidget(splitter)

    def handle_close_request(self):
        self.close()  # This triggers closeEvent ONCE

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit TimerDeck",
            "Are you sure you want to exit TimerDeck?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        