import os.path
import json

class MACIPsConfig:
  """MAC -> IP database.

  This class maintains a JSON file of the MAC -> IP mappings between runs. Once a MAC is found,
  its IP is recorded. It's then possible to update this IP address for later assignment on the
  machine.
  """

  MAC_IPS_JSON_FILE = "mac_ips.json"

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

    Return a list of changes where 'new' is previously unseen MAC and 'updated' is if the existing
    database has an IP that isn't what's found. This use case is for assigning a new address to a
    MAC. In this case, we don't update the database.
    """
    changes = []
    for mac, ip in mac_ips:
      new = mac not in self.config
      updated = mac in self.config and self.config[mac] != ip and self.config[mac]
      changes.append((mac, ip, new, updated))
      if not updated:
        self.config[mac] = ip
    self.write()
    return changes
