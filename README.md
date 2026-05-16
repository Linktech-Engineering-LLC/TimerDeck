# TimerDeck

![Linktech Engineering Tools](https://img.shields.io/badge/Linktech%20Engineering-Tools%20Suite-0A66C2)
![Status: Under Construction](https://img.shields.io/badge/Status-Under_Construction-orange?style=for-the-badge)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Last Commit](https://img.shields.io/github/last-commit/Linktech-Engineering-LLC/TimerDeck)



TimerDeck is an operator‑grade desktop GUI for inspecting and managing systemd timers on Linux systems.  
Its goal is to provide a clear, unified interface for viewing scheduled tasks, understanding their execution history, and managing timer configurations without relying on command‑line tooling.

## Planned Capabilities

- View systemd timers, units, and next/last run times
- Inspect associated service units and execution results
- Manage both user and system‑level timers
- Optional support for viewing and editing cron jobs
- Privilege‑aware operations with either on‑demand elevation or secure credential storage

## Project Status

This repository contains the initial project structure.  
Development will begin after the next RunUpdates milestone.

## Roadmap

TimerDeck is being developed in structured phases aligned with the Linktech Engineering Tools Suite roadmap.
The following milestones outline the planned progression of the project:

### Phase 1 — Core UI Foundation (Current)

* Project structure and repository initialization
* Main window, sidebar navigation, and stacked views
* Dashboard layout with Breeze‑style cards
* Icon system using local SVG assets
* Initial README, badges, and documentation

### Phase 2 — Data Integration

* Systemd timer enumeration (user + system scopes)
* Parsing next/last run times
* Linking timers to their associated service units
* Basic cron job detection (optional module)
* Dashboard live data updates

### Phase 3 — Interaction & Management

* Timer detail view (unit metadata, logs, execution history)
* Start/stop/reload actions for timers and services
* Privilege‑aware operations (pkexec / sudo integration)
* Editing timer and service unit files with safety checks

### Phase 4 — Advanced Features

* Cron editor (optional, gated behind a setting)
* Search and filtering across timers and units
* Failure diagnostics and log extraction
* Exportable reports (JSON/YAML summaries)

### Phase 5 — Polish & Release

* Dark‑mode palette and icon variants
* Hover/active states for cards and sidebar
* Animated refresh feedback
* Packaging for distribution (AppImage, Flatpak, DEB)
* v1.0 release

## Development

### Requirements

TimerDeck targets modern Linux systems with systemd.
Development requires:

* Python 3.10+
* PySide6
* Access to systemctl and journalctl
* A Linux environment (desktop or VM)

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

From the project root:

```bash
python -m timerdeck
```

Or directly:

```bash
python TimerDeck.py
```

### Project Structure

```code
timerdeck/
 ├─ ui/               # Qt UI components, icons, styles
 ├─ core/             # Application logic and helpers
 ├─ data/             # systemd/cron parsing modules
 ├─ resources/        # stylesheets, themes
 └─ tests/            # unit tests
```

### Contributing

Contributions are welcome once the core architecture stabilizes.
Issues and pull requests should align with the Roadmap phases.

## License

TimerDeck is released under the MIT License.  
See the [LICENSE](LICENSE) file for full details.

