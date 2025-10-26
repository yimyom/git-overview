#!/usr/bin/env python

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

import subprocess, argparse, sys, csv, itertools, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Set, Tuple
#from icecream import ic

#--------------------------------
# Find git repositories
#--------------------------------

def find_top_git_repo(path: Path) -> Path|None:
    """
    Find the top-level Git repository directory for a given path
    Returns Path object or None if not in a Git repo
    """
    path = Path(path).resolve()
    
    try:
        # Run git rev-parse --show-toplevel
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        
        return Path(result.stdout.strip())
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def find_git_repos(start_path: Path, exclude: List[Path]) -> Set[Path]:
    """
    Recursively find all Git repositories in the given directory
    Returns a list of paths to Git repositories
    """
    git_repos = set()
    if start_path.exists() and start_path.is_dir():
        exclude_set = {p.resolve() for p in exclude}
        
        try:
            for root, dirs, _ in os.walk(str(start_path), topdown=True,  followlinks=True):
                current_path = Path(root)
                
                if current_path.resolve() not in exclude_set:
                    rel_path = current_path.relative_to(start_path)
                    is_dot_dir = any(part.startswith('.') for part in rel_path.parts)
                    
                    if not is_dot_dir:
                        if '.git' in dirs:
                            try:
                                top_git = find_top_git_repo(current_path)
                                git_repos.add(top_git)
                                dirs.clear()  # Prune traversal
                            except (PermissionError, OSError) as e:
                                print(f'Cannot access {current_path}: {e}')
                        
                        # Remove dot directories from further traversal
                        dirs[:] = [d for d in dirs if not d.startswith('.')]
                    else:
                        dirs.clear()  # Prune dot directories
                else:
                    dirs.clear()  # Prune excluded paths
                        
        except Exception as e:
            print(f'Error traversing directory: {e}')
    
    return git_repos

#--------------------------------
# Retrieve git infos 
#--------------------------------

# Data structure to hold repository information

def __check_if_local_branch_exists__(repo_path: Path, branch_name: str) -> bool:
    return (subprocess.run(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'],
                           cwd=repo_path, capture_output=True, timeout=5)).returncode == 0

def __get_remote_info__(repo_path: Path, branch_name:str) -> str|bool:
    # Get _origin_ real name
    # Get the remote branch name corresponding to the local branch
    # Get the latest commit id on the remote without fetching

    # Get remote tracking branch info
    remote_result = subprocess.run(['git', 'config', f'branch.{branch_name}.remote'],
                                  cwd=repo_path, capture_output=True, text=True, timeout=5)
    if remote_result.returncode != 0 or not remote_result.stdout.strip():
        return False
    else:
        remote_name = remote_result.stdout.strip()
    
    # Get the remote branch name
    remote_branch_result = subprocess.run(['git', 'config', f'branch.{branch_name}.merge'],
                                         cwd=repo_path, capture_output=True, text=True, timeout=5)
    if remote_branch_result.returncode != 0:
        return False
    else:
        remote_branch = remote_branch_result.stdout.strip().replace('refs/heads/', '')
    
    # Get remote SHA without fetching
    ls_remote_result = subprocess.run(['git', 'ls-remote', remote_name, f'refs/heads/{remote_branch}'],
                                     cwd=repo_path, capture_output=True, text=True, timeout=10)
    if ls_remote_result.returncode != 0 or not ls_remote_result.stdout.strip():
        return False
    else:
        remote_sha = ls_remote_result.stdout.strip().split()[0]

    #return {'remote_name':remote_name, 'remote_branch':remote_branch, 'remote_sha': remote_sha}
    return remote_sha

def __get_local_info__(repo_path: Path, branch_name:str) -> str|bool:
    """ Get local branch SHA """
    local_sha_result = subprocess.run(['git', 'rev-parse', branch_name],
                                    cwd=repo_path, capture_output=True, text=True, timeout=5)
    if local_sha_result.returncode != 0:
        return False
    else:
        return local_sha_result.stdout.strip()
     
def __get_differences_remote_local__(repo_path:Path, remote_sha:str , local_sha:str) -> Tuple[int,int]|bool:
    """ Get ahead and behind commits by comparing remote to local """
    ahead_result = subprocess.run(['git', 'rev-list', '--count', f'{remote_sha}..{local_sha}'],
                                cwd=repo_path, capture_output=True, text=True, timeout=5)
    behind_result = subprocess.run(['git', 'rev-list', '--count', f'{local_sha}..{remote_sha}'],
                                 cwd=repo_path, capture_output=True, text=True, timeout=5)
            
    if ahead_result.returncode == 0 and behind_result.returncode == 0:
        ahead = int(ahead_result.stdout.strip())
        behind = int(behind_result.stdout.strip())
        return ahead, behind
    else:
        return False
        
def get_git_info(repo_path: Path, extra_branches: List[str]|None = None):
    """ Gather Git repository information for the given path
    
    Parameters:
        repo_path: path to the git repository
        extra_branches: additional branches to check besides current branch

    Returns:
        a list of RepoStatus objects or empty list if not a Git repo
    """
    try:
        # update the local repository and fetch remote information
        subprocess.run(['git', 'fetch'], cwd=repo_path, capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"Warning: git fetch timed out for {repo_path}")
        # Continue with stale data rather than failing completely
        
    # Get current branch
    branch_result = subprocess.run(['git', 'branch', '--show-current'], cwd=repo_path, capture_output=True,
                                   text=True, timeout=5)
    current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'Unknown'
        
    # Check status of work in progress in current tree
    status_result = subprocess.run(['git', 'status', '--porcelain'],
                                  cwd=repo_path, capture_output=True, text=True, timeout=5)
    wip_status = len(status_result.stdout.strip()) > 0
        
    # Get info for all requested branches
    if extra_branches is None:
        extra_branches = []
    unique_branches = list(dict.fromkeys([current_branch] + extra_branches))
        
    try:
        results = []
        for branch in unique_branches:
            if __check_if_local_branch_exists__(repo_path, branch):
                remote_sha = __get_remote_info__(repo_path, branch)
                local_sha = __get_local_info__(repo_path, branch)
                diffs = __get_differences_remote_local__(repo_path, remote_sha, local_sha)
                if diffs:
                    ahead, behind = diffs 
                    results.append({'repo': repo_path,
                                    'branch': branch,
                                    'ahead': ahead,
                                    'behind': behind})
        return results
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []

#--------------------------------
# Formatting and output
#--------------------------------

def __pretty_format__():
    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    tlc = '┌' # top left corner
    li = '─'  # line
    tj = '┬'  # top joint
    trc = '┐' # top right corner
    vl = '│'  # vertical line  
    lj = '├'  # left joint
    cj = '┼'  # cross joint
    rj = '┤'  # right joint
    blc= '└'  # bottom left corner
    bj = '┴'  # bottom joint
    brc= '┘'  # bottom right corner

    return GREEN, RED, YELLOW, BLUE, RESET, BOLD, tlc, li, tj, trc, vl, lj, cj, rj, blc, bj, brc

def __simple_format__():
    GREEN = RED = YELLOW = BLUE = RESET = BOLD = ''
    tlc = '+'
    li  = '-'
    tj  = '+'
    trc = '+'
    vl  = '|'
    lj  = '+'
    cj  = '+'
    rj  = '+'
    blc = '+'
    bj  = '+'
    brc = '+'

    return GREEN, RED, YELLOW, BLUE, RESET, BOLD, tlc, li, tj, trc, vl, lj, cj, rj, blc, bj, brc

def format_table(repos_status, max_width: int = 50, simple=False):
    """
    Format the repository status information as a pretty table with colors and Unicode.
    """
    if repos_status:
        # retrieve formatting strings
        format = __pretty_format__() if not simple else __simple_format__()
        GREEN, RED, YELLOW, BLUE, RESET, BOLD, tlc, li, tj, trc, vl, lj, cj, rj, blc, bj, brc = format

        # Calculate column widths
        repo_names = [ x['repo'].name for x in repos_status ]
        path_width = min(max([len(x) for x in repo_names]), max_width)
        branch_names = [ x['branch'] for x in repos_status ]
        branch_width = min(max([len(x) for x in branch_names]), max_width)
        
        # Table header with Unicode box drawing
        header = (f'{BOLD}{tlc}{li*(path_width + 2)}{tj}{li*(branch_width+2)}{tj}'
                 +f'{li*8}{tj}{li*8}{trc}'
                 + '\n'
                 +f"{vl} {'Repository':<{path_width}} "
                 +f"{vl} {'Branch':<{branch_width}} "
                 +f"{vl} {'Ahead':<7}"
                 +f"{vl} {'Behind':<7}{vl}"
                 + '\n'
                 +f'{lj}{li*(path_width + 2)}{cj}{li*(branch_width+2)}{cj}'
                 +f'{li*8}{cj}{li*8}{rj}'
                 +f'{RESET}')
        print(header) 

        # Rows
        for status in repos_status:
            ahead = f"{status['ahead']:>7}"
            behind= f"{status['behind']:>7}"

            # Colorize status if needed
            if status['ahead']>0:
                ahead = f'{GREEN}{ahead}{RESET}'
            if status['behind']>0:
                behind = f'{RED}{behind}{RESET}'

            row = (f"{vl} {status['repo'].name[:path_width]:<{path_width}} "
                 + f"{vl} {BLUE}{status['branch']:<{branch_width}}{RESET} "
                 + f'{vl}{ahead} {vl}{behind} {vl}')
            print(row)
        
        # Table footer
        print(f'{BOLD}{blc}{li*(path_width+2)}{bj}{li*(branch_width+2)}{bj}'+
              f'{li*8}{bj}{li*8}{brc}{RESET}')
    else:
        print("No Git repositories found.")

def format_csv(repos_status):
    """
    Format the repository status information as CSV
    """
    if repos_status:
        writer = csv.writer(sys.stdout)
        writer.writerow(['repository', 'branch', 'ahead', 'behind'])
        
        for status in repos_status:
            writer.writerow([ status['repo'].name, status['branch'], status['ahead'], status['behind'] ])

#--------------------------------
# Main program
#--------------------------------

def parse_list(val):
    return [s.rstrip().strip() for s in val]

def parse_command_line():
    parser = argparse.ArgumentParser(description='Git overview')
    parser.add_argument('directory', type=str, nargs='?', default='.',
                        help='Directory to start searching for Git repositories')

    # Git options
    parser.add_argument('-m', '--main',   action='store_true',
                        help='Include main/master branch if current branch is different')
    parser.add_argument('-b', '--branch', type=parse_list,    
                        help='Additional branches to check (comma-separated)')
    parser.add_argument('-e', '--exclude', type=parse_list, default = [],
                        help='comma-separated list of directories to exclude')

    # Output options
    parser.add_argument('-f', '--format', choices=['pretty','simple', 'csv'], 
                        default='pretty', help='Format output')
    parser.add_argument('-s', '--sort', choices=['repo','ahead','behind'],
                        default='repo', help='Sort output')
    parser.add_argument('-V', '--version', action='store_true', help='Print version')
    args = parser.parse_args()

    return args

def main():
    args = parse_command_line()
    if args.version:
        print('Git overview 0.1')
        print('Copyright (C) 2025 David Bellot')
        print('License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.')
        print('This is free software: you are free to change and redistribute it.')
        print('There is NO WARRANTY, to the extent permitted by law.')
        sys.exit(0)
    
    # Branches to check
    extra_branches = []
    if args.main:
        extra_branches.extend(['main', 'master'])
    if args.branch:
        extra_branches.extend(args.branch.split(','))
    extra_branches = list(set(extra_branches))
    
    # Find all Git repositories
    git_repos = find_git_repos(Path(args.directory), args.exclude)

    # Get status for each repository
    max_workers = min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        repos_status = list(executor.map(
            lambda repo_path: get_git_info(repo_path, extra_branches), 
            git_repos
        ))
    
    repos_status = list(itertools.chain(*repos_status)) # flatten list

    # sort results
    repos_status = sorted(repos_status, key=lambda x: x[args.sort])


    # Display results in the appropriate format
    if sys.stdout.isatty() and args.format=='pretty':
        format_table(repos_status)
    elif args.format=='csv':
        format_csv(repos_status)
    else:
        format_table(repos_status, simple=True)
    
    return 0

if __name__ == '__main__':
    exit(main())
