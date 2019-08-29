"""Assign a static IP to a Pi.

Currently, the way to assign a static IP to a Pi is to update /etc/dhcpcd.conf
(Historically it was /etc/network/interfaces; no longer however.)

A sample /etc/dhcpcd.conf stanza:

```
interface eth0 # or wlan0 for WiFi
static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

So for a given assignment of an IP, we have to figure out:
* what interface this is on, i.e. wired (eth0) or wireless (wlan0)
* the subnet ("/24")
* the router (typically, but not necessarily, x.y.z.1)
* the domain name servers (often the same as the router plus ISP extras)

There are two ways of figuring these out:
* query the workstation
* query the Pi

A foundation is that the Pi and the our workstation are on the same network.
For example we find the Pi by relying on the ARP cache which itself requires
being on the same network. Being on the same network means both interfaces
must be configured the same, so we can query either.

Alternatively, we can query the Pi itself. This will yield network information
for interfaces that are up, but won't help us configure down interfaces.
"""

import re
import subprocess
import sys

import descrypi.network

DEFAULT_SSH_USER = "pi"
IP_ROUTER_RE = re.compile(
    r'default via (?P<router>[0-9.]+) dev (?P<interface>(?:eth|wlan)0) ' +
    r'proto dhcp src (?P<ip>[0-9.]+)'
)
IP_SUBNET_RE = re.compile(
    r'(?P<subnet>[0-9.]+/[0-9]+) dev (?P<interface>(?:eth|wlan)0) ' + \
    r'proto dhcp scope link src (?P<ip>[0-9.]+)'
)

def remote_ip_config(host):
  """Query `ip route` on 'host' to return subnet, router, interface.

  $ ip route
  default via 192.168.2.1 dev wlan0 proto dhcp src 192.168.2.65 metric 303
  192.168.2.0/24 dev wlan0 proto dhcp scope link src 192.168.2.65 metric 303
  """
  # This currently returns the config for the interface for 'host'. Maybe we
  # want another interface's config. E.g. connect over Wi-Fi but configure
  # Ethernet?

  # -T disables pseudo-tty since we don't need it (non-interactive)
  process = subprocess.Popen(["ssh", "-T", DEFAULT_SSH_USER + "@" + host], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  with process.stdin as f:
    f.write(b"ip route\n")
  interface = ip = router = subnet = None
  for line in process.stdout.readlines():
    line = line.decode()
    match = IP_ROUTER_RE.search(line)
    if match:
      if match.group('ip') != host:
        sys.stderr.write("Found surprise host %s in `ip route` (expected %s)",
                         match.group('ip'), host)
        continue
      router, interface, ip = match.group('router'), match.group('interface'), match.group('ip')
      continue
    match = IP_SUBNET_RE.search(line)
    if match:
      if match.group('interface') != interface or match.group('ip') != ip:
        sys.stderr.write("Mismatch on interface and/or IP; check `ip route`")
        sys.exit(1)
      subnet = match.group('subnet')

  return interface, host, subnet, router

# macOS notes:
#  IFS=$'\n'; for i in $(networksetup -listallnetworkservices | tail +2 | grep -v '^\*'); do
#    networksetup -getinfo "$i"; echo "-----------"; done

def local_ip_config():
  """Query `ifconfig` locally to return [(interface, ip, subnet), ...]."""
  response = subprocess.Popen(
      ["ifconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode()
  return descrypi.network.find_networks(response)
