# CmdFinder

CmdFinder is a handy terminal-based user interface (TUI) that lets you fuzzy-search, browse, and execute commands from your shell history. It’s built with **Textual** and **RapidFuzz**.

<p align="center">
  <img src="media/cf.gif" width="70%" alt="Img"/>
</p>

<p align="center">
  <img src="media/img_1.png" alt="CmdFinder search view" width="70%" />
</p>

## Features

- 🔍 **Fuzzy Search:** Quickly find commands even if you don’t remember the exact syntax.
- 🐚 **Shell Support:**
    - Zsh: `~/.zsh_history`
    - Bash: `~/.bash_history`
- ⚡ **Instant Execution:** Pick a command and run it straight away in your shell.
- 🧭 **Vim-like Navigation:** Move around with `j` / `k`.
- 🕒 **Timestamps:** Toggle timestamps on or off.
- 🎨 **Modern Interface:** Built with Textual for a clean look.

## Requirements
- Python 3.10+
- Bash/Zsh or compatible shell
- Read access to history files

## Installation

### 1. Install via pip

```bash
pip install cmdfinder
```

### 2. Setup Background Service (One-time)

Run this after installation:

```bash
cmdfinder-setup
```

### 3. Run the App

```bash
cmdfinder
```

or simply:

```bash
cf
```

## Troubleshooting

If your system can't find `cmdfinder` or `cf`, add `~/.local/bin` to your PATH.

### Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Install from Source

```bash
git clone https://github.com/pranav5127/CmdFinder.git
cd cmdfinder
```

### Optional: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install in Editable Mode

```bash
pip install -e .
```

After installing from source, run:

```bash
cmdfinder-setup
```

## Usage

Start the TUI with:

```bash
cmdfinder
```

## Key Bindings

| Key         | Action              |
|-------------|----------------------|
| j           | Move down           |
| k           | Move up             |
| ↓ / ↑       | Move cursor         |
| Ctrl+s      | Focus search        |
| l / Ctrl+l  | Focus list          |
| t           | Toggle timestamps   |
| Enter       | Run selected command|
| q /Ctrl+q   | Quit                |
| y           | Copy                |

## License

CmdFinder is released under the **MIT License**. Enjoy!
