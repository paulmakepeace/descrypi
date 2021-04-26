"""Change password.

The Pi will quite rightly issue a warning on each login if the default
password is not changed. This command updates the password.
"""

from getpass import getpass
import sys

from descrypi.ssh import ssh
from descrypi.ssh import DEFAULT_SSH_USER


def change_password(hosts):
    """Update user's password on each host using `passwd`."""
    print("Changing password for %s." % DEFAULT_SSH_USER)
    current_password = (
        getpass("Current password (<Return> for default): ") or "raspberry"
    )
    new_password = getpass("New password: ")
    new_password2 = getpass("Retype new password: ")
    if new_password != new_password2:
        sys.stderr.write("Sorry, passwords do not match.\n")
        sys.exit(1)
    passwd_stdin = "%s\n%s\n%s\n" % (current_password, new_password, new_password)
    for host in hosts:
        print("Changing password on %s ..." % host)
        if ssh(host, ["/usr/bin/passwd"], stdin=passwd_stdin):
            print("passwd: password updated successfully!")
