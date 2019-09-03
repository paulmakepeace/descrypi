"""class MACIPsConfig."""

import os.path
import json

class MACIPsConfig:
  """Hosts database.

  This class maintains a file of the IP -> MAC mappings between runs. Once a MAC is found,
  its IP is recorded. It's then possible to assign a specific IP address for later assignment on the
  machine.

  The format is the same as the Ansible inventory file so it can be used to drive more
  sophisticated automation using Ansible.
  """

  ANSIBLE_INVENTORY_FILE = "hosts.json"
  ANSIBLE_HOST_GROUP = "pi"
  ANSIBLE_SSH_USER = "pi"
  ANSIBLE_PYTHON = "/usr/bin/python"

  INVENTORY_FILE = "hosts.json"
  IP_NOT_SET = 'Set this for a static IP'

  def __init__(self):
    self.file = self.INVENTORY_FILE
    self.config = {
      self.ANSIBLE_HOST_GROUP: {
        "hosts": {},
        "vars": {
          "ansible_ssh_user": self.ANSIBLE_SSH_USER,
          "ansible_python_interpreter": self.ANSIBLE_PYTHON,
        }
      }
    }
    self.load()

  def dump(self):
    """Write out the database."""
    with open(self.file, "w") as f:
      json.dump(self.config, f, indent=4)

  def load(self):
    """Load JSON MAC -> IP assignments."""
    if not os.path.exists(self.file):
      self.dump()
    self.config = json.load(open(self.file))

  def hosts(self):
    """Return the actual hosts part of the inventory data structure."""
    return self.config[self.ANSIBLE_HOST_GROUP]["hosts"]

  def record(self, mac_ips):
    """Record the latest scan with the existing database.

    Return a list of changes where 'new' is previously unseen MAC and 'assigned' is if the existing
    database has a manually assigned IP. In this case, we don't update the database.
    """
    changes = []
    hosts = self.hosts()
    for mac, ip in mac_ips:
      if ip in hosts:
        new = False
        assigned = hosts[ip]['assigned'] != self.IP_NOT_SET and hosts[ip]['assigned']
      else:
        new, assigned = True, False
      changes.append((mac, ip, new, assigned))
      if not assigned:
        hosts[ip] = {'mac': mac, 'assigned': self.IP_NOT_SET}
    self.dump()
    return changes

  def current_hosts(self):
    """Return a list of current hosts."""
    return self.hosts().keys()

def current_hosts():
  """Shortcut to return all known hosts."""
  return MACIPsConfig().current_hosts()
