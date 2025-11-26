# CmdFinder

**CmdFinder** is a terminal-based user interface (TUI) that lets you fuzzy-search, browse, and execute commands from your shell history. It’s built with [Textual](https://textual.textualize.io/) and [RapidFuzz](https://github.com/maxbachmann/RapidFuzz).

<p align="center">
  <img src="https://raw.githubusercontent.com/pranav5127/CmdFinder/master/media/cmdfinder.gif" alt="CmdFinder TUI demo" width="70%" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/pranav5127/CmdFinder/master/media/img.png" alt="CmdFinder search view" width="70%" />
</p>

---

## Features

- 🔍 **Fuzzy Search:** Quickly find commands even if you don’t remember the exact syntax.
- 🐚 **Shell Support:** Reads history from:
  - Zsh: `~/.zsh_history`
  - Bash: `~/.bash_history`
- ⚡ **Instant Execution:** Select a command and run it immediately in your shell.
- 🧭 **Vim-like Navigation:** Navigate with `j` / `k`.
- 🕒 **Timestamps:** Toggle timestamps on/off.
- 🎨 **Modern TUI:** Built using Textual.

---

## Requirements

- Python **3.10+**
- Bash/Zsh or compatible shell
- Read access to history files

---

## Installation



```bash
pip install cmdfinder
```

Run:

```bash
cmdfinder
```
### or
```bash
cf
```

If the command is not found, add `~/.local/bin` to PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Or for zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### Install from Source

```bash
git clone https://github.com/pranav5127/CmdFinder.git
cd CmdFinder
```

(Optional) create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

Run:

```bash
cmdfinder
```

---

## Usage

To start the TUI:

```bash
cmdfinder
```

### Key Bindings

| Key | Action |
|-----|--------|
| `j` | Move down |
| `k` | Move up |
| `↓` / `↑` | Move cursor |
| `Ctrl+s` | Focus search |
| `l` / `Ctrl+l` | Focus list |
| `t` | Toggle timestamps |
| `Enter` | Run selected command |
| `q` | Quit |

---

Run locally:

```bash
cmdfinder
```

or

```bash
python -m cmdfinder.app
```

---

## License

CmdFinder is released under the **MIT License**.
