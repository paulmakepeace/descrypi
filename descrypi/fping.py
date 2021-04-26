#!/usr/bin/env python3

"""Wrapper for `fping` to rapidly ping the network to fill the ARP cache.

This is useful if the ARP cache expires: by pinging all addresses on an
interface any devices that respond will have their MAC address recorded
for descrypi to find.

Usage: descrypi scan [-i <interface, e.g. eth0>]

We rely on `fping` to do the actual pinging. This wrapper takes an interface
name and constructs a command line to perform the ping with the least
amount of traffic (AFAIK), as quickly as possible without requiring root.

Restricted to IPv4 for now.
"""

import subprocess

# Minimize packet size; only send two; single retry; quick timeout; 1ms between pings
# The second packet can help if the computer is asleep.
FPING_COMMAND = (
    "fping --size 40 --count 2 --retry 1 --timeout=50 --interval 1 --generate %s"
)


def fping(network, progress=False):
    """Execute `fping` and return alive hosts.

    A ICMP reply (or not) is reported as,
    169.254.19.148  : xmt/rcv/%loss = 1/1/0%, min/avg/max = 0.25/0.25/0.25
    169.255.255.254 : xmt/rcv/%loss = 0/0/0%
    """

    command = (FPING_COMMAND % network).split()
    response = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout.readlines()
    alive = []
    for line in (line.decode() for line in response):
        if "rcv" not in line:
            continue
        line = line.split()
        ip_address, result = line[0], line[4]
        if result[2] != "0":  # rcv'ed something!
            if progress:
                print("%s is alive" % ip_address)
            alive.append(ip_address)
    return alive


def ping(hosts):
    """Ping 'hosts' using fping."""
    process = subprocess.Popen(
        ["fping"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    with process.stdin as f:
        f.write("\n".join(hosts).encode())
    lines = (line.decode() for line in process.stdout.readlines())
    return (line.split()[0] for line in lines if "is alive" in line)
