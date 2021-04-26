"""Parse the ARP table for MAC and IP addresses.

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

# Regex to match known MAC prefixes, e.g., "B8:27:EB|DC:A6:32|EA:62:9D"
MAC_PREFIX_RE = "|".join(descrypi.ieee_ra.MAC_PREFIXES)
# Regex to catch rest of the MAC (suffix), e.g., "12:ab:9"
MAC_OCTET_TRIPLE_RE = ":".join([r"[0-9a-f]{1,2}"] * 3)
# Regex to extract IP, MAC, and its prefix from an `arp -a` line
MACS_RE = re.compile(
    r"""
                    ^\S+[ ]
                    \((?P<ip>[^)]+)\)
                    [ ]at[ ]
                    (?P<mac>(?P<prefix>{prefix}):(?:{rest}))
                    """.format(
        prefix=MAC_PREFIX_RE, rest=MAC_OCTET_TRIPLE_RE
    ),
    re.MULTILINE | re.IGNORECASE | re.VERBOSE,
)


def find_pi_mac_ips():
    """Run `arp -a` and return array of (Pi MAC address, IP) tuples."""
    arp = subprocess.Popen(ARP_COMMAND, stdout=subprocess.PIPE).stdout.read().decode()
    return [
        (
            m.group("mac"),
            m.group("ip"),
            descrypi.ieee_ra.model_by_mac_prefix(m.group("prefix")),
        )
        for m in MACS_RE.finditer(arp)
    ]
