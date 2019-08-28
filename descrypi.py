#!/usr/bin/env python3

"""
Descry Pi

Find Raspberry Pis on the network by examining `arp` responses.

We restrict `arp` usage to the BSD format so that it works on macOS and Linux
without getting into platform switching.
"""

import re
import subprocess

# -a shows the current table. -n skips reverse DNS lookup (no use for name)
ARP_COMMAND = "arp -n -a".split()
RASPBERRY_PI_MACS = ['B8:27:EB', 'DC:A6:32']

# There are two `arp -a` outputs here, Linux and macOS. Fortunately the
# interesting part is the same.
# ? (169.254.201.244) at 00:3e:e1:c7:3b:26 [ether] on eth0
# ? (169.254.46.250) at dc:a6:32:19:1d:88 on en1 [ethernet]
ARP_LINE_RE = re.compile(
    r'^\S+ \((?P<ip>[^)]+)\) at (?P<mac>(?:[0-9a-f]{2}:){5}(?:[0-9a-f]{2}))'
)
RASPBERRY_PI_MACS_RE = re.compile(
    r'^(' + "|".join(RASPBERRY_PI_MACS) + r'):',
    re.IGNORECASE
)

def find_ip_macs():
  """Run `arp -a` and return array of (IP, MAC address) tuples."""
  ip_macs = []
  arp_response = subprocess.Popen(ARP_COMMAND, stdout=subprocess.PIPE).stdout.readlines()
  for line in arp_response:
    match = ARP_LINE_RE.search(line.decode())
    if match:
      ip_macs.append((match.group('ip'), match.group('mac')))
  return ip_macs

def filter_ip_macs(ip_macs, filter_re=RASPBERRY_PI_MACS_RE):
  """Apply the filter_re regex to the MAC address and return matching subset."""
  return [(ip, mac) for (ip, mac) in ip_macs if filter_re.search(mac)]

def print_ip_macs():
  """Main entry point."""
  print("IP Macs of Pis:")
  print(filter_ip_macs(find_ip_macs()))

if __name__ == '__main__':
  print_ip_macs()
