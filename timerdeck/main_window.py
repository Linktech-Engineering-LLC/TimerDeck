# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
Modified: 2026-09-25
 File: timerdeck/ui/main_window.py
 Version: 1.0.0
 Description: Main Window Orchestrator
"""


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QSplitter,
    QStackedWidget, QLabel, QToolBar,
    QMessageBox, QGridLayout, QFrame,
    QRadioButton, QButtonGroup, QHBoxLayout,
    QComboBox, QDockWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon

from .logic import (
    CronManager,
    EnvManager,
    HostManager,
    SystemdManager,
    UserManager
)
from .ui.widgets import icon, make_card
from .ui.widgets import (
    CronTableWidget,
    DashboardWidget,
    SidebarWidget
)

from PythonTools.net.users import get_valid_users

class MainWindow(QMainWindow):
    request_close = Signal()
    def __init__(self):
        super().__init__()
        self.cron_manager = CronManager()
        self.env_manager = EnvManager()
        self.host_manager = HostManager()
        self.user_manager = UserManager()
        self.systemd_manager = SystemdManager()
        self.active_scope = "personal"
        self.active_user = self.user_manager.get_users()[0] if self.user_manager.get_users() else ""
        self.remote_mode = False
        self.active_host = ""
        
        self.setWindowTitle("TimerDeck")
        self.resize(1100, 700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.statusBar().showMessage("Ready")
        self.request_close.connect(self.handle_close_request)

        # --- Main splitter (sidebar + content) ---
        splitter = QSplitter(Qt.Horizontal)

        # --- Sidebar ---
        self.sidebar = SidebarWidget(
            users=self.user_manager.get_users(),
            hosts=self.host_manager.get_hosts()
        )
        dock = QDockWidget("Sidebar", self)
        dock.setWidget(self.sidebar)
        dock.setTitleBarWidget(QWidget())  # hides the title bar
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)  # optional: lock it in place
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.sidebar.viewChanged.connect(self.show_view)
        self.sidebar.scopeChanged.connect(self.set_scope)
        self.sidebar.userChanged.connect(self.load_user_cron)
        self.sidebar.remoteModeChanged.connect(self.update_remote_mode)
        self.sidebar.hostChanged.connect(self.set_host)
        self.sidebar.requestClose.connect(self.close)
        
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
        self.dashboard = DashboardWidget()
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)
        # Populate dashboard immediately
        self.refresh_dashboard()
        
        #Unified Systemd view placeholder
        systemd_view = QLabel(
            "Systemd Timers\n\n"
            "List of systemd timers will appear here."
        )
        systemd_view.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(systemd_view)  # index 1

        self.cron_table = CronTableWidget()
        self.stack.addWidget(self.cron_table)

        # Add widgets to splitter
        splitter.addWidget(self.stack)

        # Set splitter as central widget
        self.setCentralWidget(splitter)
    def show_view(self, view: str):
        if view == "dashboard":
            self.stack.setCurrentIndex(0)
        elif view == "systemd":
            self.stack.setCurrentIndex(1)
        elif view == "cron":
            self.show_cron()
    def load_user_cron(self, user: str):
        self.active_user = user
        rows = self.cron_manager.load_user_cron(user)
        self.dashboard.set_cron_tasks(rows)
    def set_host(self, host: str):
        """Update the active host when the sidebar host selector changes."""
        self.active_host = host

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
    def set_scope(self, scope: str):
        """Update active scope when SidebarWidget changes it."""
        self.active_scope = scope
        self.systemd_manager.set_scope(scope)
        self.statusBar().showMessage(f"Scope changed to: {scope.capitalize()}")

    def show_cron(self):
        scope = self.systemd_manager.active_scope

        if scope == "personal":
            user = self.active_user   # set by load_user_cron()
            rows = self.cron_manager.load_user_cron(user)
        else:
            rows = self.cron_manager.load_system_cron()

        self.cron_table.populate(rows)
        self.stack.setCurrentWidget(self.cron_table)
    def update_remote_mode(self, remote: bool):
        self.remote_mode = remote
        self.host_manager.set_remote_mode(remote)
    def refresh_dashboard(self):
        user = self.sidebar.user_selector.currentText()
        scope = self.sidebar.active_scope

        # Cron
        cron_rows = self.cron_manager.load_user_cron(user)
        self.dashboard.set_cron_tasks(cron_rows)

        # Systemd
        systemd_rows = self.systemd_manager.load_timers(user, scope)
        self.dashboard.set_systemd_tasks(systemd_rows)

        # Environment
        env_rows = self.env_manager.load_env(user, scope)
        self.dashboard.set_environment_variables(env_rows)
        