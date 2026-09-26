# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/sidebar.py
 Version: 1.0.0
 Description: Description of this module
"""

import getpass
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QRadioButton, QComboBox,
    QLabel, QFrame, QHBoxLayout, QButtonGroup,
    QLineEdit
)
from PySide6.QtCore import Signal

from ..widgets.cards import icon

class SidebarWidget(QWidget):
    # Signals emitted upward to MainWindow
    viewChanged = Signal(str)
    scopeChanged = Signal(str)
    userChanged = Signal(str)
    remoteModeChanged = Signal(bool)
    hostChanged = Signal(str)
    passwordModeChanged = Signal(bool)
    requestClose = Signal()

    def __init__(self, users: list[str], hosts: list[str]):
        super().__init__()

        self._init_state(users, hosts)
        self._build_ui()
        self._wire_signals()
        self._apply_initial_visibility()

    @property
    def active_scope(self):
        return "system" if self.scope_system.isChecked() else "user"

    # ------------------------------------------------------------
    # 1. Internal state
    # ------------------------------------------------------------
    def _init_state(self, users, hosts):
        self.users = users
        self.hosts = hosts
        self.current_user = getpass.getuser()

        # Load SSH hosts from ~/.ssh/config
        self.ssh_hosts = self._load_ssh_hosts()

    def _load_ssh_hosts(self):
        config_path = Path.home() / ".ssh" / "config"
        hosts = []

        if not config_path.exists():
            return hosts

        for line in config_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("host "):
                parts = line.split()
                if len(parts) > 1:
                    # Skip wildcard patterns
                    if "*" in parts[1] or "?" in parts[1]:
                        continue
                    hosts.append(parts[1])

        return sorted(set(hosts))

    # ------------------------------------------------------------
    # 2. Build UI
    # ------------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Load icons
        self.icon_systemd_user = icon("systemd-user.svg")
        self.icon_systemd_system = icon("systemd-system.svg")
        self.icon_cron = icon("cron.svg")
        self.icon_close = icon("exit.svg")
        self.icon_dashboard = icon("dashboard.svg")

        # --- Scope Row ---
        scope_frame = QFrame()
        scope_layout = QHBoxLayout(scope_frame)

        self.scope_group = QButtonGroup(self)
        self.scope_personal = QRadioButton("Personal")
        self.scope_system = QRadioButton("System")
        self.scope_personal.setChecked(True)

        self.scope_group.addButton(self.scope_personal)
        self.scope_group.addButton(self.scope_system)

        scope_layout.addWidget(QLabel("Scope:"))
        scope_layout.addWidget(self.scope_personal)
        scope_layout.addWidget(self.scope_system)

        layout.addWidget(scope_frame)

        # --- User Selector ---
        self.user_selector = QComboBox()
        self.user_selector.addItems(self.users)
        layout.addWidget(self.user_selector)

        # --- Password Toggle ---
        self.password_toggle = QRadioButton("Show Password")
        self.password_toggle.setChecked(False)
        layout.addWidget(self.password_toggle)
        # --- Password Textbox ---
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)   # start masked
        self.password_edit.hide()                            # only shown for non-current users
        layout.addWidget(self.password_edit)

        # --- Remote/Local Row ---
        remote_frame = QFrame()
        remote_layout = QHBoxLayout(remote_frame)

        self.rb_local = QRadioButton("Local")
        self.rb_remote = QRadioButton("Remote")
        self.rb_local.setChecked(True)

        remote_layout.addWidget(self.rb_local)
        remote_layout.addWidget(self.rb_remote)

        layout.addWidget(remote_frame)

        # --- Host Selector ---
        self.host_selector = QComboBox()
        self.host_selector.addItem("Select Host...")
        self.host_selector.addItems(self.hosts)
        self.host_selector.hide()
        layout.addWidget(self.host_selector)

        # --- Navigation Buttons ---
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_systemd = QPushButton("Systemd Timers")
        self.btn_cron = QPushButton("Cron Jobs")
        self.btn_close = QPushButton("Close TimerDeck")
        self.btn_dashboard.setIcon(self.icon_dashboard)
        self.btn_systemd.setIcon(self.icon_systemd_user)
        self.btn_cron.setIcon(self.icon_cron)
        self.btn_close.setIcon(self.icon_close)

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_systemd)
        layout.addWidget(self.btn_cron)
        layout.addWidget(self.btn_close)

        layout.addStretch()

    # ------------------------------------------------------------
    # 3. Wire signals
    # ------------------------------------------------------------
    def _wire_signals(self):
        # View buttons
        self.btn_dashboard.clicked.connect(lambda: self.viewChanged.emit("dashboard"))
        self.btn_systemd.clicked.connect(lambda: self.viewChanged.emit("systemd"))
        self.btn_cron.clicked.connect(lambda: self.viewChanged.emit("cron"))
        self.btn_close.clicked.connect(self.requestClose.emit)

        # Scope
        self.scope_personal.toggled.connect(
            lambda checked: checked and self.scopeChanged.emit("personal")
        )
        self.scope_system.toggled.connect(
            lambda checked: checked and self.scopeChanged.emit("system")
        )

        # User
        self.user_selector.currentTextChanged.connect(self._user_changed)
        self.scope_personal.toggled.connect(lambda checked: checked and self._update_systemd_icon())
        self.scope_system.toggled.connect(lambda checked: checked and self._update_systemd_icon())

        # Remote/local
        self.rb_local.toggled.connect(self._remote_mode_update)
        self.rb_remote.toggled.connect(self._remote_mode_update)

        # Host selector
        self.host_selector.currentTextChanged.connect(self.hostChanged.emit)

        # Password toggle
        self.password_toggle.toggled.connect(self._password_mode_changed)

    # ------------------------------------------------------------
    # 4. Initial visibility rules
    # ------------------------------------------------------------
    def _apply_initial_visibility(self):
        selected = self.user_selector.currentText()
        self.password_toggle.setVisible(selected != self.current_user)
        self._update_systemd_icon()

    # ------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------
    def _user_changed(self, user):
        self.userChanged.emit(user)

        is_current = (user == self.current_user)

        # Show password controls only for non-current users
        self.password_toggle.setVisible(not is_current)
        self.password_edit.setVisible(not is_current)

        # Clear password when switching users
        if not is_current:
            self.password_edit.clear()

        # Root always forces system scope
        if user == "root":
            self.scope_system.setChecked(True)

        self._update_systemd_icon()
    def _remote_mode_update(self):
        remote = self.rb_remote.isChecked()
        self.remoteModeChanged.emit(remote)
        self.host_selector.setVisible(remote)

    def _password_mode_changed(self, checked):
        # Update label
        self.password_toggle.setText(
            "Hide Password" if checked else "Show Password"
        )

        # Switch masking
        if checked:
            self.password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)

        self.passwordModeChanged.emit(checked)
    def _update_systemd_icon(self):
        if self.scope_system.isChecked():
            self.btn_systemd.setIcon(self.icon_systemd_system)
        else:
            self.btn_systemd.setIcon(self.icon_systemd_user)
