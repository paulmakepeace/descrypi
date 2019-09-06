"""SSH helper."""

from descrypi.run import run

DEFAULT_SSH_USER = "pi"

# -T disables pseudo-tty since we don't need it (non-interactive)
SSH_COMMAND = ["ssh", "-T", "-o", "StrictHostKeyChecking=no"]

def ssh_user_host(host):
  return DEFAULT_SSH_USER + "@" + host

def ssh(host, command, stdin=None):
  """Run 'command' (list) on 'host' via ssh.

  stdin is an string to send."""
  return run([*SSH_COMMAND, ssh_user_host(host), *command], stdin=stdin)
