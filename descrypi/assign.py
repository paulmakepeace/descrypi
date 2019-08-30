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

# import descrypi.network
