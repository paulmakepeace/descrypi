"""class MACIPsConfig."""

import os.path
import json

class MACIPsConfig():
  """MAC -> IP database.

  This class maintains a JSON file of the MAC -> IP mappings between runs. Once a MAC is found,
  its IP is recorded. It's then possible to assign a specific IP address for later assignment on the
  machine.
  """

  MAC_IPS_JSON_FILE = "mac_ips.json"
  IP_NOT_SET = 'Set this for a static IP'

  def __init__(self):
    self.file = self.MAC_IPS_JSON_FILE
    self.config = {}
    self.load()

  def write(self):
    """Write out the database."""
    with open(self.file, "w") as f:
      json.dump(self.config, f, indent=4)

  def load(self):
    """Load JSON MAC -> IP assignments."""
    if not os.path.exists(self.file):
      self.write()
    self.config = json.load(open(self.file))

  def record(self, mac_ips):
    """Record the latest scan with the existing database.

    Return a list of changes where 'new' is previously unseen MAC and 'assigned' is if the existing
    database has a manually assigned IP. In this case, we don't update the database.
    """
    changes = []
    for mac, ip in mac_ips:
      if mac in self.config:
        new = False
        assigned = self.config[mac]['assigned'] != self.IP_NOT_SET and self.config[mac]['assigned']
      else:
        new, assigned = True, False
      changes.append((mac, ip, new, assigned))
      if not assigned:
        self.config[mac] = { 'current': ip, 'assigned': self.IP_NOT_SET }
    self.write()
    return changes
