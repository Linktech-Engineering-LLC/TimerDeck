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

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QRadioButton, QComboBox,
    QLabel, QFrame, QHBoxLayout, QButtonGroup
)
from PySide6.QtCore import Signal

from ..widgets.cards import icon

class SidebarWidget(QWidget):
    # Signals emitted to MainWindow
    viewChanged = Signal(str)          # "dashboard", "systemd", "cron"
    scopeChanged = Signal(str)         # "personal", "system"
    userChanged = Signal(str)          # username
    remoteModeChanged = Signal(bool)   # True = remote, False = local
    hostChanged = Signal(str)          # hostname
    requestClose = Signal()            # close TimerDeck

    def __init__(self, users: list[str], hosts: list[str]):
        super().__init__()
        self.icon_user = icon("systemd-user.svg")
        self.icon_system = icon("systemd-system.svg")
        self.icon_root = icon("systemd-user.svg")  # fallback
        self.icon_dashboard = icon("dashboard.svg")
        self.icon_cron = icon("cron.svg")
        self.icon_close = icon("exit.svg")

        layout = QVBoxLayout(self)

        # --- Scope Selector ---
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
        self.user_selector.addItems(users)
        layout.addWidget(self.user_selector)

        # --- Remote/Local Selector ---
        remote_frame = QFrame()
        remote_layout = QHBoxLayout(remote_frame)

        self.rb_local = QRadioButton("Local")
        self.rb_remote = QRadioButton("Remote")
        self.rb_local.setChecked(True)

        self.host_selector = QComboBox()
        self.host_selector.addItems(hosts)
        self.host_selector.hide()

        remote_layout.addWidget(self.rb_local)
        remote_layout.addWidget(self.rb_remote)
        remote_layout.addWidget(self.host_selector)

        layout.addWidget(remote_frame)

        # --- Navigation Buttons ---
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_systemd = QPushButton("Systemd Timers")
        self.btn_cron = QPushButton("Cron Jobs")
        self.btn_close = QPushButton("Close TimerDeck")
        self.btn_systemd.setIcon(self.icon_user)
        self.btn_dashboard.setIcon(self.icon_dashboard)
        self.btn_cron.setIcon(self.icon_cron)
        self.btn_close.setIcon(self.icon_close)

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_systemd)
        layout.addWidget(self.btn_cron)
        layout.addWidget(self.btn_close)

        layout.addStretch()

        # --- Signal Wiring ---
        self.btn_dashboard.clicked.connect(lambda: self.viewChanged.emit("dashboard"))
        self.btn_systemd.clicked.connect(lambda: self.viewChanged.emit("systemd"))
        self.btn_cron.clicked.connect(lambda: self.viewChanged.emit("cron"))
        self.btn_close.clicked.connect(self.requestClose.emit)

        self.scope_personal.toggled.connect(
            lambda checked: checked and self.set_scope("personal")
        )
        self.scope_system.toggled.connect(
            lambda checked: checked and self.set_scope("system")
        )

        self.user_selector.currentTextChanged.connect(self.userChanged.emit)

        self.rb_local.toggled.connect(self._remote_mode_update)
        self.rb_remote.toggled.connect(self._remote_mode_update)

        self.host_selector.currentTextChanged.connect(self.hostChanged.emit)
        self.set_scope("personal")

    def _remote_mode_update(self):
        remote = self.rb_remote.isChecked()
        self.host_selector.setVisible(remote)
        self.remoteModeChanged.emit(remote)
    def set_scope(self, scope):
        if scope == "personal":
            self.btn_systemd.setIcon(self.icon_user)
            self.user_selector.show()
        elif scope == "system":
            self.btn_systemd.setIcon(self.icon_system)
            self.user_selector.hide()
        elif scope == "root":
            self.btn_systemd.setIcon(self.icon_root)
            self.user_selector.hide()

        self.scopeChanged.emit(scope)
