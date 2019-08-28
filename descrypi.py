#!/usr/bin/env python3

"""
Descry Pi

Find Raspberry Pis on the network by examining `arp` responses.

We restrict `arp` usage to the BSD format so that it works on macOS and Linux
without getting into platform switching.
"""

import csv
import io
import re
import subprocess
import textwrap
import urllib.parse
import urllib.request

# -a shows the current table. -n skips reverse DNS lookup (no use for name)
ARP_COMMAND = "arp -n -a".split()

# Known RPi MAC prefixes, sorted
RASPBERRY_PI_MACS = ['B8:27:EB', 'DC:A6:32']

# URL to query the IEEE MAC Registration Authority for updated MAC prefixes
IEEE_RA_URL = "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/"
IEEE_RA_QUERY = '"raspberry pi"'

# There are two `arp -a` outputs here, Linux and macOS. Fortunately the
# interesting part is the same.
# ? (169.254.201.244) at 00:3e:e1:c7:3b:26 [ether] on eth0
# ? (169.254.46.250) at dc:a6:32:19:1d:88 on en1 [ethernet]
ARP_LINE_RE = re.compile(
    r'^\S+ \((?P<ip>[^)]+)\) at (?P<mac>(?:[0-9a-f]{2}:){5}(?:[0-9a-f]{2}))'
)

# Regex to filter RPi MACs
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

def ieee_ra_url(query):
  """Return a URL to query IEEE Registration Authority's MAC database."""
  # curl "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/?registry=MAC&text=%22raspberry%20pi%22"
  params = urllib.parse.urlencode({'registry': 'MAC', 'text': query})
  return IEEE_RA_URL + "?" + params

def macs_from_ieee_ra(query=IEEE_RA_QUERY):
  """Query IEEE Reg Authority for RPi MAC.

  Data looks like,
  Registry,Assignment,Organization Name,Organization Address
  MA-L,DCA632,Raspberry Pi Trading Ltd,"Maurice Wilkes Building, Cowley Road Cambridge  GB CB4 0DS "
  MA-L,B827EB,Raspberry Pi Foundation,Mitchell Wood House Caldecote Cambridgeshire US CB23 7NU
  """
  try:
    with urllib.request.urlopen(ieee_ra_url(query)) as f:
      r = csv.reader((line.decode() for line in f), delimiter=',', quotechar='"')
      next(r) # skip header
      # Split "01AB23" into "01:AB:23"
      return sorted((":".join(textwrap.wrap(row[1], 2)) for row in r))
  except urllib.error.HTTPError as err:
    print("IEEE RA query failed:", err, "(may be transient; try again?)")
    return []

def verify_ieee_macs(query=IEEE_RA_QUERY, macs=RASPBERRY_PI_MACS):
  """Ensure no new MAC prefixs have popped up."""
  return macs == macs_from_ieee_ra(query)

def print_ip_macs():
  """Main entry point."""
  print("IP Macs of Pis:")
  print(filter_ip_macs(find_ip_macs()))

if __name__ == '__main__':
  print_ip_macs()
