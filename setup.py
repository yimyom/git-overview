#   git-overview: a standalone and git extension to retrieve the current
#                 status of all the git repositories in a directory and
#                 its subdirectories.
#
#   Copyright (C) 2025 David Bellot
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   A setuptools based setup module

from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="git-overview",
    version="0.1.0",
    description="Git command to pretty display the status of local repositories compared to remotes",
    url="https://github.com/yimyom/git-overview/",
    author="David Bellot",
    author_email="david.bellot@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    project_urls={
        "Bug Reports": "https://github.com/yimyom/git-overview/issues",
        "Source": "https://github.com/yimyom/git-overview/",
    },
)
