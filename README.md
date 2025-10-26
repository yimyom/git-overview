# Git Overview

A powerful command-line tool to quickly scan directories and display the status of all Git repositories. Get an overview of which repositories are ahead/behind their remotes across your entire projects folder.

<img width="696" height="576" alt="image" src="https://github.com/user-attachments/assets/e03ecd5b-3241-4b2c-b363-9ba4bd8ad916" />

## Features

- 🔍 **Recursive scanning** - Automatically finds all Git repositories in a directory tree
- 📊 **Multi-branch support** - Check status for current branch plus main/master or custom branches
- 🎨 **Beautiful output** - Colorful, formatted tables with Unicode box-drawing characters
- 💾 **Multiple formats** - Pretty, simple, and CSV output formats
- ⚡ **Parallel processing** - Fast scanning using multiple threads
- 📁 **Exclusion support** - Skip specific directories from scanning

## Installation

### Install from PyPI
```bash
pip install git-overview
```

### Manual Installation
```bash
# Download the script and make it executable
wget https://raw.githubusercontent.com/yourusername/git-overview/main/git-overview.py
chmod +x git-overview.py
sudo mv git-overview.py /usr/local/bin/git-overview
```

### Install as DEB Package (Ubuntu/Debian)
```bash
wget https://github.com/yourusername/git-overview/releases/latest/download/git-overview_all.deb
sudo dpkg -i git-overview_all.deb
```

## Usage
It can be invoked
```bash
# Scan current directory
git overview

# Scan specific directory
git overview ~/projects

# Include main/master branches
git overview --main

# Check specific additional branches
git overview --branch develop,feature/new-feature

# Exclude directories
git overview --exclude node_modules,dist,build

# Simple output (no colors/Unicode)
git overview --format simple

# CSV output
git overview --format csv

# Sort by ahead/behind count
git overview --sort ahead
```

## Requirements
 - Python 3.6+
 - Git

## License
GPL-3.0 License - See LICENSE file for details.
