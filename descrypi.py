#!/usr/bin/env python3

"""
Descry Pi

Find Raspberry Pis on the network by examining `arp` responses.

We restrict `arp` usage to the BSD format so that it works on macOS and Linux
without getting into platform switching.
"""

import re
import subprocess

import ieee_ra
import descrypi.macipsconfig

# -a shows the current table. -n skips reverse DNS lookup (no use for name)
ARP_COMMAND = "arp -n -a".split()

# There are two `arp -a` outputs here, Linux and macOS. Fortunately the
# interesting part is the same.
# ? (169.254.201.244) at 00:3e:e1:c7:3b:26 [ether] on eth0
# ? (169.254.46.250) at dc:a6:32:19:1d:88 on en1 [ethernet]
ARP_LINE_RE = re.compile(
    r'^\S+ \((?P<ip>[^)]+)\) at (?P<mac>(?:[0-9a-f]{1,2}:){5}(?:[0-9a-f]{1,2}))'
)

# Regex to filter RPi MACs
RASPBERRY_PI_MACS_RE = re.compile(
    r'^(' + "|".join(ieee_ra.RASPBERRY_PI_MACS) + r'):',
    re.IGNORECASE
)

def find_mac_ips():
  """Run `arp -a` and return array of (IP, MAC address) tuples."""
  mac_ips = []
  arp_response = subprocess.Popen(ARP_COMMAND, stdout=subprocess.PIPE).stdout.readlines()
  for line in arp_response:
    match = ARP_LINE_RE.search(line.decode())
    if match:
      mac_ips.append((match.group('mac'), match.group('ip')))
  return mac_ips

def filter_mac_ips(mac_ips, filter_re=RASPBERRY_PI_MACS_RE):
  """Apply the filter_re regex to the MAC address and return matching subset."""
  return [(mac, ip) for (mac, ip) in mac_ips if filter_re.search(mac)]

def print_mac_ips():
  """Main entry point."""
  mac_ip_config = descrypi.macipsconfig.MACIPsConfig()
  print("MAC -> IPs of Pis:")
  mac_ips = filter_mac_ips(find_mac_ips())
  changes = mac_ip_config.record(mac_ips)
  for mac, ip, new, updated in changes:
    print("%s -> %s %s%s" % (
        mac, ip, ("(new!) " if new else ""), ("updated to %s!" % updated if updated else "")))

if __name__ == '__main__':
  print_mac_ips()
  #print(load_mac_ips())
