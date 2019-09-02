"""Parse the ARP table for Raspberry Pi MAC and IP addresses.

We restrict `arp` usage to the BSD format so that it works on macOS and Linux
without getting into platform switching.
"""

import re
import subprocess

import descrypi.ieee_ra

# -a shows the current table. -n skips reverse DNS lookup (no use for name)
ARP_COMMAND = "arp -n -a".split()

# There are two `arp -a` outputs here, Linux and macOS. Fortunately the
# interesting part is the same.
# ? (169.254.201.244) at 00:3e:e1:c7:3b:26 [ether] on eth0
# ? (169.254.46.250) at dc:a6:32:19:1d:88 on en1 [ethernet]

# Regex to filter MAC suffix, e.g., "12:ab:9", and RPi MACs
MAC_OCTET_TRIPLE_RE = ':'.join([r'[0-9a-f]{1,2}'] * 3)
MAC_PI_PREFIX_RE = '|'.join(descrypi.ieee_ra.RASPBERRY_PI_MACS)

def raspberry_pi_macs_re():
  """Return a regex that'll match a Pi line from `arp -a`."""
  return re.compile(r"""
                    ^\S+[ ]
                    \((?P<ip>[^)]+)\)
                    [ ]at[ ]
                    (?P<mac>(?:{prefix}):(?:{rest}))
                    """.format(prefix=MAC_PI_PREFIX_RE, rest=MAC_OCTET_TRIPLE_RE),
                    re.MULTILINE | re.IGNORECASE | re.VERBOSE)

def find_pi_mac_ips():
  """Run `arp -a` and return array of (Pi MAC address, IP) tuples."""
  arp = subprocess.Popen(ARP_COMMAND, stdout=subprocess.PIPE).stdout.read().decode()
  return [(m.group('mac'), m.group('ip')) for m in raspberry_pi_macs_re().finditer(arp)]
