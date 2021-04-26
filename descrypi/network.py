"""Networking helpers.

Query for local and remote network Interfaces (interface, ip, subnet, gateway).
"""

import ipaddress
import re
import subprocess
import sys

from descrypi.ssh import ssh

# We're using the technically deprecated `ifconfig` because it works nearly
# identically on macOS (BSD) and Linux.


class Interface:
    """Interface is the config for a hardware interface.

    * Interface name, e.g. eth0 (name)
    * IPv4 IP address (ip)
    * IPv4 Network (network)
    * Gateway/router address (gateway)

    Two class methods exist to fill in these fields from `ifconfig` and `ip route`.
    """

    def __init__(self, interface, ip=None, network=None, gateway=None):
        self.name = interface
        self.ip = ip
        self.network = network
        self.gateway = gateway

    # Break the parsing into two stages: extract the interface blocks, then
    # extract the network info. Done as a single regex seemed to trigger a ton of
    # backtracking that took minutes(!)
    IFCONFIG_INTERFACES_RE = re.compile(
        r"^(?P<interface>[a-z]+[0-9]+): .*<UP,.*\n"
        + r"^(?P<block>(?:\s+.*\n)+)",  # indented info
        re.MULTILINE,
    )

    # Linux: inet 169.254.46.250  netmask 255.255.0.0  broadcast 169.254.255.255
    # macOS: inet 169.254.201.244 netmask 0xffff0000 broadcast 169.254.255.255
    IFCONFIG_INET_RE = re.compile(
        r"inet (?P<ip>\S+)\s+netmask\s+(?P<netmask>\S+)\s+broadcast\s+(?P<broadcast>\S+)"
    )

    def ifconfig(self, ifconfig):
        """Parse 'ifconfig' to fill out object info."""
        match = self.IFCONFIG_INET_RE.search(ifconfig)
        if match:
            self.ip, netmask, broadcast = match.groups()
            if netmask[0:2] == "0x":
                netmask = bin(int(netmask, 16)).count("1")
            self.network = str(
                ipaddress.IPv4Network("%s/%s" % (broadcast, netmask), strict=False)
            )
        return self

    @classmethod
    def from_ifconfigs(cls, ifconfigs):
        """Return [Interface, ...] for UP ether interfaces."""
        return (
            cls(interface).ifconfig(block)
            for (interface, block) in cls.IFCONFIG_INTERFACES_RE.findall(ifconfigs)
            if "ether " in block and "inet " in block
        )

    # $ ip route
    # default via 192.168.2.1 dev wlan0 proto dhcp src 192.168.2.65 metric 303
    # 192.168.2.0/24 dev wlan0 proto dhcp scope link src 192.168.2.65 metric 303
    #
    # If there's no route it'll be missing the "via <gw>" (and probably proto):
    # default dev eth0 scope link src 169.254.110.40 metric 202
    # 169.254.0.0/16 dev eth0 scope link src 169.254.110.40 metric 202

    IP_GATEWAY_IFACE_IP_RE = r"dev (?P<interface>(?:eth|wlan)0) .* src (?P<ip>[0-9.]+)"
    IP_GATEWAY_RE = re.compile(
        r"default (?:via (?P<gateway>[0-9.]+) )?" + IP_GATEWAY_IFACE_IP_RE
    )
    IP_SUBNET_RE = re.compile(r"(?P<subnet>[0-9.]+/[0-9]+) " + IP_GATEWAY_IFACE_IP_RE)

    @classmethod
    def from_ip_route(cls, ip_route, host):
        """Return Interface from `ip route` output."""
        # Being pretty defensive cross-checking here as I'm less familiar with all
        # the possibilities.
        interface = ip = gateway = subnet = None
        match = cls.IP_GATEWAY_RE.search(ip_route)
        if match:
            if match.group("ip") != host:
                sys.stderr.write(
                    "Found surprise host %s in `ip route` (expected %s)\n",
                    match.group("ip"),
                    host,
                )
            else:
                gateway, interface, ip = (
                    match.group("gateway"),
                    match.group("interface"),
                    match.group("ip"),
                )
                if gateway is None:
                    sys.stderr.write("Host %s appears to be missing a gateway\n" % host)
        match = cls.IP_SUBNET_RE.search(ip_route)
        if match:
            if match.group("interface") != interface or match.group("ip") != ip:
                sys.stderr.write("Mismatch on interface and/or IP; check `ip route`\n")
                sys.exit(1)
            subnet = match.group("subnet")

        return cls(interface, ip=host, network=subnet, gateway=gateway)


def remote_interface(host):
    """Query `ip route` on 'host' to return Interface."""
    # This currently returns the config for the interface for 'host'. Maybe we
    # want another interface's config. E.g. connect over Wi-Fi but configure
    # Ethernet?
    ip_route = ssh(host, ["ip", "route"])
    if ip_route is None:
        return None
    return Interface.from_ip_route(ip_route, host)


def local_interfaces(interface=None):
    """Query `ifconfig` locally to return [Interface, ...]."""
    command = ["ifconfig"]
    if interface is not None:
        command.append(interface)
    response = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout
    return Interface.from_ifconfigs(response.read().decode())
