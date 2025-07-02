---

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
```bash
pip install habitpy==0.1.11
```
If your system says some error about being globally installed try installing with *pipx*,
for example in arch linux:
```bash
sudo pacman -S python-pipx
pipx ensurepath
```
close your terminal and:
```bash
pipx install habitpy==0.1.11
```
Or, for development:
```bash
git clone https://github.com/Asunt70/habitpy.git
cd habitpy
python -m venv .venv/
source .venv/bin/activate
pip install .
```

## Usage

First, set up your tracker:
```bash
habitpy setup
```

Then, use these commands:
- `habitpy track` — Log today’s habits
- `habitpy create <habit_name>` — Add a new habit
- `habitpy show` — List your habits
- `habitpy delete <habit_name>` — Remove a habit
- `habitpy graph week|month|year` — See your progress in graphs
- `habitpy export` — Export your data to CSV
- `habitpy reset` — Delete all data and start over

---

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W318WNN8)
