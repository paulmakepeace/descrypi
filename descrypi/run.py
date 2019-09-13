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
    sys.stderr.write("Missing `%s`. Try `brew install %s`, `apt-get install %s`, etc\n" % (
        app, brew_package, apt_package))
    sys.exit(1)

def run(command, stdin=None):
  """Takes an a 'command' (array) and runs it with optional stdin."""
  process = subprocess.Popen(command,
                             stdin=(subprocess.PIPE if stdin else None),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
  if stdin:
    with process.stdin as f:
      f.write(stdin.encode())
  output = process.stdout.read().decode()
  process.wait()
  if process.returncode != 0:
    sys.stderr.write("Failed: " + output)
    return None
  return output
