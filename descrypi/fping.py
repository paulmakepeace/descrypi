#!/usr/bin/env python3

"""Wrapper for `fping` to rapidly ping the network to fill the ARP cache.

This is useful if the ARP cache expires: by pinging all addresses on an
interface any devices that respond will have their MAC address recorded
for descrypi to find.

Usage: descrypi scan eth0

We rely on `fping` to do the actual pinging. This wrapper takes an interface
name and constructs a command line to perform the ping with the least
amount of traffic (AFAIK), as quickly as possible without requiring root.

Restricted to IPv4 for now.
"""

import subprocess

import descrypi.network

# Minimize packet size; only send one; single retry; quick timeout; 1ms between pings
FPING_COMMAND = "fping --size 40 --count 1 --retry 1 --timeout=50 --interval 1 --generate %s"

def run_fping(network):
  """Execute `fping` and return alive hosts.

  A ICMP reply is reported as,
  169.254.19.148  : xmt/rcv/%loss = 1/1/0%, min/avg/max = 0.25/0.25/0.25
  169.255.255.254 : xmt/rcv/%loss = 0/0/0%
  """

  command = (FPING_COMMAND % network).split()
  response = subprocess.Popen(
      command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()
  alive = []
  for line in (line.decode() for line in response):
    if "xmt" not in line:
      continue
    line = line.split()
    ip_address, result = line[0], line[4]
    if result[2] != "0": # rcv'ed something!
      alive.append(ip_address)
  return alive

def fping(interface):
  """Return list of responsive IP addresses on the interface."""
  return run_fping(descrypi.network.subnet_for_interface(interface))

def ping(hosts):
  """Ping 'hosts' using fping."""
  process = subprocess.Popen(["fping"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
  with process.stdin as f:
    f.write("\n".join(hosts).encode())
  lines = (line.decode() for line in process.stdout.readlines())
  return (line.split()[0] for line in lines if "is alive" in line)
