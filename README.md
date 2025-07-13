# HabitPy

**Track your habits, analyze your progress, and stay motivated—all from your terminal!**

## Features

- 📅 **Daily & Weekly Tracking:** Log your habits (only numbers)
- ✏️ **Custom Habits:** Add, show, or delete any habit you want to track.
- 📈 **Visualize Progress:** Instantly generate beautiful graphs (with dark mode!) for your week, month, or year.
- 🎉 **Motivational Cheers:** Get random motivational messages to keep you going.
- 📤 **Export Data:** Export all your habit data to CSV for use in Excel, Sheets, or anywhere else.
- 🛠️ **Easy Reset:** Reset your data and start fresh anytime.

## Installation

### Option 1: Build and Install from Source (Recommended)

#### Clone and Build

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Build the distribution
python -m build

# Install the built package globally
pip install dist/habitpy-*.whl
```

#### Using pipx (Recommended for CLI tools)

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Build the distribution
python -m build

# Install with pipx (ensures global availability)
pipx install dist/habitpy-*.whl
```

#### Using uv (Fast Python package installer)

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Build the distribution
python -m build

# Install with uv
uv pip install dist/habitpy-*.whl
```

### Option 2: Development Installation

#### Using pip

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

#### Using uv for Development

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Install with uv
uv sync
uv run habitpy setup
```

#### Using pipx for Development

```bash
git clone https://github.com/asuntx/habitpy.git
cd habitpy

# Install in development mode with pipx
pipx install -e .
```

## Usage

First, set up your tracker:

```bash
habitpy setup
```

Then, use these commands:

- `habitpy track` — Log today's habits
- `habitpy create <habit_name>` — Add a new habit
- `habitpy show` — List your habits
- `habitpy delete <habit_name>` — Remove a habit
- `habitpy graph week|month|year` — See your progress in graphs
- `habitpy export` — Export your data to CSV
- `habitpy reset` — Delete all data and start over

---

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W318WNN8)
