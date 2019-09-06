"""Copy SSH keys.

A wrapper for the `ssh-copy-id` tool to copy over SSH keys, enabling
password-less login.
"""

from getpass import getpass

from descrypi import ssh
from descrypi.run import run

def ssh_copy_id(hosts):
  """Copy SSH keys using `ssh-copy-id`."""
  print("Installing SSH keys for %s." % ssh.DEFAULT_SSH_USER)
  current_password = getpass("Current password (<Return> for default): ") or "raspberry"
  ssh_copy_id_stdin = "%s\n" % current_password
  for host in hosts:
    target = ssh.ssh_user_host(host)
    print("Installing SSH keys on %s ..." % target)
    output = run(["/usr/bin/ssh-copy-id", target], stdin=ssh_copy_id_stdin)
    if output:
      print(output)
