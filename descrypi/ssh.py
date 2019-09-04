"""SSH helper."""

import subprocess
import sys

DEFAULT_SSH_USER = "pi"

# -T disables pseudo-tty since we don't need it (non-interactive)
SSH_COMMAND = ["ssh", "-T", "-o", "StrictHostKeyChecking=no"]

def ssh(host, command, stdin=None):
  """Run 'command' on 'host' via ssh.

  'command' can be a string or list.
  """
  process = subprocess.Popen([*SSH_COMMAND, DEFAULT_SSH_USER + "@" + host, *command],
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
