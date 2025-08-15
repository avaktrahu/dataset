"""
avaktrahu/dataset

Script for cloning and updating git repositories in the dataset directory
"""

# =============================================================================
# Imports
#

import os
import csv
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .api import execute, Commit, GitAPI

# =============================================================================
# Configuration
#

DATASET_ROOT =  Path('dataset')
TARGET_VOLUME = DATASET_ROOT / 'software' / 'code'

# Template for metadata file name
META_FILE = '%s.meta.csv'

# TODO: magic number may change, OS specific command
EMPTY_HASH = execute(['hash-object', '-t', 'tree', '/dev/null'])

# =============================================================================
# Main
#

def sync(origin: str):
    """
    Clones, updates, and applies patches for a given Git repository.
    Args:
        origin: The git repository URL.
    """
    git = GitAPI(origin)
    provider = git.provider
    organization, repo = git.name

    target = TARGET_VOLUME / provider / organization / repo
    metadata = TARGET_VOLUME / provider / organization / (META_FILE % repo)
    last_commit = EMPTY_HASH

    target.mkdir(parents=True, exist_ok=True)

    if os.path.exists(metadata):
        # TODO: os specific command
        line = subprocess.check_output(['tail', '-1', metadata])
        last_commit = line.decode().split(',')[0]

    with TemporaryDirectory() as tmp:
        git.clone(tmp)
        patch = git.patch(last_commit)
        git.apply(patch, str(target))

        commits = git.history(last_commit)
        with open(metadata, 'a') as file:
            writer = csv.DictWriter(file, list(Commit.__annotations__.keys()))
            for commit in commits[::-1]:
                writer.writerow(commit)
