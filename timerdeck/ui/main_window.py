# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
Modified: 2026-09-24
 File: timerdeck/ui/main_window.py
 Version: 1.0.0
 Description: Main Window Orchestrator
"""

import sys
import getpass
import pwd
import subprocess

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QSplitter,
    QStackedWidget, QLabel, QToolBar,
    QMessageBox, QGridLayout, QFrame,
    QRadioButton, QButtonGroup, QHBoxLayout,
    QComboBox, QTableWidget, QAbstractItemView,
    QTableWidgetItem,
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
        self.icon_user = icon("systemd-user.svg")
        self.icon_system = icon("systemd-system.svg")
        self.icon_root = icon("systemd-user.svg")  # fallback

        # --- Main splitter (sidebar + content) ---
        splitter = QSplitter(Qt.Horizontal)

        # --- Sidebar ---
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)

        btn_dashboard = QPushButton("Dashboard")
        btn_systemd = QPushButton("Systemd Timers")
        btn_systemd.setIcon(self.icon_user)  # default
        self.btn_systemd = btn_systemd       # store reference
        btn_cron = QPushButton("Cron Jobs")

        btn_close = QPushButton("Close TimerDeck")
        btn_close.setIcon(QIcon.fromTheme("application-exit"))
        btn_close.clicked.connect(self.request_close.emit)

        btn_dashboard.setIcon(icon("dashboard.svg"))
        btn_cron.setIcon(icon("cron.svg"))
        btn_close.setIcon(icon("exit.svg"))

        # --- Scope Selector ---
        scope_frame = QFrame()
        scope_layout = QHBoxLayout(scope_frame)

        self.scope_group = QButtonGroup(self)

        self.scope_personal = QRadioButton("Personal")
        self.scope_system = QRadioButton("System")
        sidebar_layout.addWidget(scope_frame)
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_systemd)
        sidebar_layout.addWidget(btn_cron)
        sidebar_layout.addWidget(btn_close)
        sidebar_layout.addStretch()

        self.scope_personal.setChecked(True)
        self.active_scope = "personal"

        self.scope_group.addButton(self.scope_personal)
        self.scope_group.addButton(self.scope_system)

        self.scope_personal.toggled.connect(lambda checked: checked and self.set_scope("personal"))
        self.scope_system.toggled.connect(lambda checked: checked and self.set_scope("system"))
        self.user_selector = QComboBox()
        self.user_selector.addItems(get_valid_users())
        self.user_selector.setCurrentIndex(0)  # current user always first

        scope_layout.addWidget(QLabel("Scope:"))
        scope_layout.addWidget(self.scope_personal)
        scope_layout.addWidget(self.scope_system)
        scope_layout.addWidget(self.user_selector)        

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

        #Unified Systemd view placeholder
        systemd_view = QLabel(
            "Systemd Timers\n\n"
            "List of systemd timers will appear here."
        )
        systemd_view.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(systemd_view)  # index 1

        self.cron_table = QTableWidget()
        self.cron_table = QTableWidget()
        self.cron_table.setColumnCount(2)
        self.cron_table.setHorizontalHeaderLabels(["Scheduling", "Command"])
        self.cron_table.horizontalHeader().setStretchLastSection(True)
        self.cron_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stack.addWidget(self.cron_table)

        # Add views to stack
        self.stack.addWidget(dashboard)            # index 0
        self.stack.addWidget(systemd_view)    # index 1
        self.stack.addWidget(self.cron_table)  # index 2

        # Connect sidebar buttons to stack switching
        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_systemd.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_cron.clicked.connect(self.show_cron)

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
    def set_scope(self, scope):
        self.active_scope = scope

        match scope:
            case "personal":
                self.user_selector.setVisible(True)
                self.btn_systemd.setIcon(self.icon_user)
            case "system":
                self.user_selector.setVisible(False)
                self.btn_systemd.setIcon(self.icon_system)
            case _:
                self.user_selector.setVisible(False)
                self.btn_systemd.setIcon(self.icon_system)

        self.statusBar().showMessage(f"Scope changed to: {scope.capitalize()}")
    def load_user_cron(self, user):
        try:
            # If the selected user is the current user, do NOT use -u
            if user == getpass.getuser():
                output = subprocess.check_output(["crontab", "-l"], text=True)
            else:
                # Viewing another user's crontab requires privilege
                output = subprocess.check_output(["sudo", "crontab", "-u", user, "-l"], text=True)
        except subprocess.CalledProcessError:
            output = ""

        lines = [l.strip() for l in output.splitlines() if l.strip() and not l.startswith("#")]

        self.cron_table.setRowCount(len(lines))
        for i, line in enumerate(lines):
            parts = line.split(maxsplit=5)
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = parts[5]
            else:
                schedule = line
                command = ""
            self.cron_table.setItem(i, 0, QTableWidgetItem(schedule))
            self.cron_table.setItem(i, 1, QTableWidgetItem(command))
    def show_cron(self):
        match self.active_scope:
            case "personal":
                user = self.user_selector.currentText()
                self.load_user_cron(user)
                self.stack.setCurrentWidget(self.cron_table)
            case "system":
                self.load_system_cron()
                self.stack.setCurrentWidget(self.cron_table)
        self.cron_table.show()
        self.stack.setCurrentWidget(self.cron_table)
    def show_systemd(self):
        # Later: populate table based on scope + user
       self.cron_table.setVisible(False)
       self.stack.setCurrentIndex(1)

def get_valid_users():
    import pwd, getpass
    current_user = getpass.getuser()
    users = []

    for entry in pwd.getpwall():
        name = entry.pw_name
        uid = entry.pw_uid
        home = entry.pw_dir
        shell = entry.pw_shell

        # Always include root
        if name == "root":
            users.append(name)
            continue

        # Skip system accounts (UID < 1000)
        if uid < 1000:
            continue

        # Skip accounts without a home directory
        if not home or home == "/":
            continue

        # Skip nologin shells
        if shell.endswith("nologin") or shell.endswith("false"):
            continue

        users.append(name)

    # Ensure current user is first and unique
    users = [current_user] + [u for u in users if u != current_user]

    return users
        