"""Networking helpers."""

import ipaddress
import re
import subprocess

# Linux: inet 169.254.46.250  netmask 255.255.0.0  broadcast 169.254.255.255
# macOS: inet 169.254.201.244 netmask 0xffff0000 broadcast 169.254.255.255
IFCONFIG_RE = re.compile(
    r'^(?P<interface>[a-z]+[0-9]+): .*\n' +
    r'(?:\s+.*\n)*' +
    r'\s+inet (?P<ip>\S+)\s+netmask\s+(?P<netmask>\S+)\s+broadcast\s+(?P<broadcast>\S+)',
    re.MULTILINE)

def find_networks(data):
  """Return [(interface, ip, subnet), ...] from `ifconfig` output."""
  networks = []
  for interface, ip, netmask, broadcast in IFCONFIG_RE.findall(data):
    if netmask[0:2] == '0x':
      netmask = bin(int(netmask, 16)).count("1")
    subnet = str(ipaddress.IPv4Network("%s/%s" % (broadcast, netmask), strict=False))
    networks.append((interface, ip, subnet))
  return networks

def subnet_for_interface(interface):
  """Return the subnet for a given interface using `ifconfig`."""
  ifconfig = subprocess.Popen(["ifconfig", interface], stdout=subprocess.PIPE).stdout.read()
  _interface, _ip, subnet = find_networks(ifconfig.decode())[0]
  return subnet
