# Git Overview

A powerful command-line tool to quickly scan directories and display the status of all Git repositories. Get an overview of which repositories are ahead/behind their remotes across your entire projects folder.

![Git Overview Screenshot](screenshot.png) <!-- Add your screenshot here -->

## Features

- 🔍 **Recursive scanning** - Automatically finds all Git repositories in a directory tree
- 📊 **Multi-branch support** - Check status for current branch plus main/master or custom branches
- 🎨 **Beautiful output** - Colorful, formatted tables with Unicode box-drawing characters
- ⚡ **Parallel processing** - Fast scanning using multiple threads
- 📁 **Exclusion support** - Skip specific directories from scanning
- 💾 **Multiple formats** - Pretty, simple, and CSV output formats

## Installation

### Manual Installation
```bash
# Download the script and make it executable
wget https://raw.githubusercontent.com/yourusername/git-overview/main/git-overview.py
chmod +x git-overview.py
sudo mv git-overview.py /usr/local/bin/git-overview
```

### Install from PyPI
```bash
pip install git-overview
```

### Install as DEB Package (Ubuntu/Debian)
```bash
wget https://github.com/yourusername/git-overview/releases/latest/download/git-overview_1.0.0_all.deb
sudo dpkg -i git-overview_1.0.0_all.deb
```

### Install as RPM Package (Fedora/RHEL/CentOS)
```bash
wget https://github.com/yourusername/git-overview/releases/latest/download/git-overview-1.0.0-1.noarch.rpm
sudo rpm -i git-overview-1.0.0-1.noarch.rpm
```

## Usage
It can be invoked
```bash
# Scan current directory
git-overview

# Scan specific directory
git-overview ~/projects

# Include main/master branches
git-overview --main

# Check specific additional branches
git-overview --branch develop,feature/new-feature

# Exclude directories
git-overview --exclude node_modules,dist,build

# Simple output (no colors/Unicode)
git-overview --format simple

# CSV output
git-overview --format csv

# Sort by ahead/behind count
git-overview --sort ahead
```

## Requirements
 - Python 3.6+
 - Git

## License
GPL-3.0 License - See LICENSE file for details.
