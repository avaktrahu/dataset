"""
avaktrahu/dataset

Git commands API for handling git operations
"""

# =============================================================================
# Imports
#

import os
import subprocess
from pathlib import Path
from datetime import datetime

# For typing support
from typing import List, Tuple, TypedDict, Optional

from .log import logger

# =============================================================================
# Types
#

class Commit(TypedDict):
    hash: str
    message: str
    timestamp: str

# =============================================================================
# Configuration
#

# Required for consistent git patching behaviour
ENV = os.environ.copy()
ENV['GIT_CEILING_DIRECTORIES'] = str(Path('dataset').parent.resolve())

# =============================================================================
# Helper methods
#

def execute(
        cmd: List[str],
        input: Optional[str] = None,
        cwd: Optional[str] = None,
        strip: Optional[bool] = True,
    ) -> str:
    """
    Execute a git command and return its stdout. Exits on error.
    Args:
        cmd: The git command to run as a list of strings.
        input: Pass a string to the subprocess's stdin.
        cwd: Working directory to run the command in.
        strip: Remove leading and trailing whitespace.
    Returns:
        The standard output of the command.
    Raises:
        RuntimeError: If the command fails, it raises an error with the command and stderr output
    """
    full_cmd = ['git'] + cmd
    command = " ".join(full_cmd)
    logger.debug(f"Executing command [{command}]")

    result = subprocess.run(
        full_cmd, cwd=cwd,
        input=input,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
        env=ENV
    )
    if result.returncode != 0:
        logger.error(f"Error running {command}: {result.stderr}")
        raise RuntimeError(f"Error running {command}: {result.stderr}")

    if strip:
        return result.stdout.strip()
    else:
        return result.stdout

# =============================================================================
# Git API
#

class GitAPI:
    """
    Class for handling git operations in a modular way.
    """

    def __init__(self, origin: str):
        """
        Initialize the GitAPI with the repository URL.
        Args:
            origin: The git repository URL.
        """
        self.origin = origin
        self.target: str | None = None

    @property
    def name(self) -> Tuple[str, str]:
        """
        Provides Git repository name in [organization, repository] format.
        Returns:
            A tuple containing the organization and repository name.
        """
        if self.origin == '.':
            # TODO: Handle local directories
            return 'avaktrahu', 'dataset'

        parts = self.origin.split('/')
        return parts[-2], parts[-1].replace('.git', '')

    @property
    def provider(self) -> str:
        """
        Returns the service provider based on the repository URL.
        Returns:
            The service provider name (e.g., 'github', 'gitlab').
        """
        if self.origin == '.':
            # TODO: Handle local directories
            return 'github'

        if 'github.com' in self.origin:
            return 'github'
        elif 'gitlab.com' in self.origin:
            return 'gitlab'
        else:
            return 'git' # Default for generic Git repositories

    def clone(self, target: str):
        """
        Clones the Git repository to the specified target location.
        Args:
            target: Directory to be used for cloning the Git repository.
        """
        if self.target is not None:
            # Already cloned
            return

        execute(['clone', self.origin, target])
        self.target = target

    def history(self, hash: Optional[str] = None) -> List[Commit]:
        """
        Retrieves a list of commit hashes, messages, and timestamps that occurred after a given starting commit hash.
        The commits are ordered from newest to oldest.
        Args:
            hash: The commit hash after which to retrieve the history.
        Returns:
            A list of dictionaries, where each dictionary contains 'hash', 'message', and 'timestamp'.
        Raises:
            RuntimeError: If the repository has not been cloned.
        """
        if not self.target:
            raise RuntimeError("Repository not cloned. Call .clone() first.")

        # Use a distinct delimiter for parsing the log output
        # %H: commit hash
        # %s: commit subject (message)
        # %at: author date, UNIX timestamp
        DELIMITER = "---COMMIT-DELIMITER---"
        cmd = ['log', f'--pretty=format:%H%n%s%n%at{DELIMITER}']

        if hash:
            cmd.extend(['HEAD', f'^{hash}'])

        logs = execute(cmd, cwd=self.target)

        commits: List[Commit] = []

        # Split by the custom delimiter and filter out empty strings
        log = [entry.strip() for entry in logs.split(DELIMITER) if entry.strip()]

        for entry in log:
            lines = entry.splitlines()
            if len(lines) >= 3:
                commit_hash = lines[0].strip()
                message = lines[1].strip()
                try:
                    timestamp_unix = int(lines[2].strip())
                    timestamp = datetime.fromtimestamp(timestamp_unix).isoformat()
                except ValueError:
                    timestamp: str = "Invalid Timestamp" # Handle cases where timestamp might be malformed

                commits.append({
                    'hash': commit_hash,
                    'message': message,
                    'timestamp': timestamp
                })
        return commits

    def patch(self, hash: str, end_ref: str = 'HEAD') -> str:
        """
        Generates a patch representing the changes from a specified hash up to an end_ref (defaulting to HEAD).
        This patch can be used to apply these changes to another repository or directory.
        Args:
            hash: The starting commit hash for the patch. Changes *after* this commit will be included.
            end_ref: The ending reference (e.g., branch name, commit hash, or 'HEAD'). Defaults to 'HEAD'.
        Returns:
            A string containing the generated patch.
        Raises:
            RuntimeError: If the repository has not been cloned.
            RuntimeError: If the patch generation fails.
        """
        if not self.target:
            raise RuntimeError("Repository not cloned. Call .clone() first.")

        # The 'git diff <commit1> <commit2>' command generates a patch representing the changes
        # that would transform commit1 into commit2.
        return execute(['diff', hash, end_ref, '--binary'], cwd=self.target, strip=False)

    def apply(self, patch: str, target: str) -> str:
        """
        Applies a patch to the target directory.
        Args:
            patch: The content of the patch to apply (as a string).
            target: Directory to be used for applying the patch.
        Returns:
            The standard output of the git apply command.
        Raises:
            RuntimeError: If applying the patch fails.
        """
        return execute(['apply'], input=patch, cwd=target)
