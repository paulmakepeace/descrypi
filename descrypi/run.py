"""Helper functions for running external programs.
"""

import shutil
import subprocess
import sys


def ensure_executable(app, brew_package=None, apt_package=None):
    """Ensure app is executable in $PATH or suggest how to get it."""
    if not shutil.which(app):
        if brew_package is None:
            brew_package = app
        if apt_package is None:
            apt_package = app
        sys.stderr.write(
            f"Missing `{app}`. Try `brew install {brew_package}`, "
            f"`apt-get install {apt_package}`, etc\n"
        )
        sys.exit(1)


def run(command, stdin=None):
    """Takes an a 'command' (array) and runs it with optional stdin."""
    with subprocess.Popen(
        command,
        stdin=(subprocess.PIPE if stdin else None),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) as process:
        if stdin:
            with process.stdin as f:
                f.write(stdin.encode())
        output = process.stdout.read().decode()
        process.wait()
        if process.returncode != 0:
            sys.stderr.write("Failed: " + output)
            return None
        return output
