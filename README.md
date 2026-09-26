# TimerDeck
Operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite
**Maintainer:** Leon McClatchey, Linktech Engineering LLC
**License:** MIT (source) · Proprietary (binaries, if distributed)
**Requires:** Python 3.12+
**Version:** 0.2.0 (In Development)
**Packaging:** AppImage · Flatpak · DEB · RPM · TGZ · ZIP (planned)
**PythonTools:** 0.2.0 (integration planned)
**Last Updated:** 2026‑09‑26

![Linktech Engineering Tools](https://img.shields.io/badge/Linktech%20Engineering-Tools%20Suite-0A66C2)
![Status: Under Construction](https://img.shields.io/badge/Status-Under_Construction-orange?style=for-the-badge)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Last Commit](https://img.shields.io/github/last-commit/Linktech-Engineering-LLC/TimerDeck)

---

## Table of Contents
1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Planned Capabilities](#3-planned-capabilities)
4. [Project Status](#4-project-status)
5. [Roadmap](#5-roadmap)
6. [Development](#6-development)
7. [Contributing](#7-contributing)
8. [License](#8-license)

---

## 1. Overview
TimerDeck is an operator‑grade desktop GUI for inspecting, editing, and managing **systemd timers**, **cron jobs**, and **environment variables** on Linux systems.
It provides a unified interface for viewing scheduled tasks, understanding execution history, and modifying configurations without relying on command‑line tooling.

TimerDeck is part of the **Linktech Engineering Tools Suite**, designed for deterministic, operator‑focused system management.

---

## 2. Features
* Unified dashboard for cron, systemd, and environment variables
* Interactive column resizing with horizontal scrolling
* Systemd timer parsing (next/last run, unit linkage)
* Cron parsing with:
    * inline comments
    * preceding comments (Kcron‑style)
    * multi‑line comment accumulation
* Systemd comment support:
    * preceding comment lines in unit files
    * inline comments
    * Description= as fallback
* Dedicated editor windows for:
    * Cron entries
    * Systemd timers
    * Environment variables
* Cross‑system move operations:
    * Cron ↔ Systemd
    * Env ↔ Cron/Systemd
* Toolbar system selector (Cron / Systemd / Environment)
* Deterministic parsing and refresh behavior

---

## 3. Planned Capabilities
* View systemd timers, units, and next/last run times
* Inspect associated service units and execution results
* Manage both user and system‑level timers
* View and edit cron jobs
* Unified environment variable management
* Privilege‑aware operations with on‑demand elevation
* SSH/remote host support (planned)

---

## 4. Project Status
TimerDeck is under active development.
Current focus: **Phase‑2 architecture refactor and data integration**, including:
* MainWindow structural cleanup
* Toolbar system selector
* Editor windows for cron/systemd/env
* Unified comment parsing
* Orchestrator‑style manager interfaces

---

## 5. Roadmap
### 5.1 Phase 1 — Core UI Foundation (Complete)
* Project structure and repository initialization
* Main window, sidebar navigation, stacked views
* Dashboard layout and icon system
* Initial documentation

### 5.2 Phase 2 — Data Integration (Current)
* Systemd timer enumeration (user + system)
* Cron job parsing (inline + preceding comments)
* Environment variable extraction
* Dashboard live data updates
* Toolbar system selector
* Orchestrator conversion

### 5.3 Phase 3 — Interaction & Management
* Timer/service detail views
* Cron/Systemd/Env editor windows
* Move operations between systems
* Start/stop/reload actions
* Privilege‑aware operations (sudo/pkexec)

#### 5.4 Phase 4 — Advanced Features
* Search and filtering
* Failure diagnostics and log extraction
* Exportable reports (JSON/YAML)
* SSH remote host support

### 5.5 Phase 5 — Polish & Release
* Dark‑mode palette and icon variants
* Hover/active states and animations
* Packaging (AppImage, Flatpak, DEB, RPM, TGZ, ZIP)
* v1.0 release

---

## 6. Development
### 6.1 Requirements
* Python 3.12+
* PySide6
* Access to `systemctl` and `journalctl`
* Linux environment (desktop or VM)

Install dependencies:

```bash
pip install -r requirements.txt
```

### 6.2 Running the Application
From the project root:

```bash
python -m timerdeck
```
Or:

```bash
python TimerDeck.py
```

### 6.3 Project Structure
```text
timerdeck/
 ├─ ui/               # Qt UI components, icons, styles
 ├─ core/             # Application logic and helpers
 ├─ data/             # systemd/cron/env parsing modules
 ├─ resources/        # stylesheets, themes
 └─ tests/            # unit tests
```

---

## 7. Contributing
Contributions are welcome once the core architecture stabilizes.
Issues and pull requests should align with the roadmap phases and maintain deterministic, operator‑grade behavior.

---

## 8. License
TimerDeck is released under the MIT License.
See the [LICENSE](LICENSE) file for full details.