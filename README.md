# Descry Pi

Find ("descry") freshly installed Raspberry Pi(s) on your network!

This toolset aims to be easier than using `fing` and, ultimately, more useful.

Currently, it's written in Python 3 with no Python package dependencies, and should work on macOS and Linux.

## Installation

### Dependencies

There is an optional external dependency on a common executable though: install `fping`:

* macOS: `brew install fping`
* Ubuntu: `sudo apt-get install fping`
* etc

It also uses `arp` but you almost certainly have that. (If not, it's in the Linux net-tools package.)

### The App

```shell
git clone git@github.com:paulmakepeace/descrypi.git
cd descrypi
# Run bin/descrypi
```

## Flow

### Networks

First, figure out what local networks are available on your workstation and so where your Pi(s) are connected. You'll need this to direct your scans for Pi(s).

```shell
bin/descrypi networks
```

You're interested in the local networks at this stage. Pick out the name of the hardware interface listed in the first column, e.g. eth0, en0, bridge100, etc.

### Scan

To scan for machines, run `bin/descrypi scan [-i <interface>]`. You don't strictly need to do this if your Pi and workstation have been in communication recently but the network (ARP) cache can expire so this will refresh it.

### Find

Then run `bin/descrypi` to find your Pi(s)!

This should report newly found Pi(s) and create a database, `mac_ips.json`. Next time you run `bin/descrypi` it'll recognize that MAC-to-IP mapping.

### Assign

Next, if you want to assign a static IP to the machines update the IP addresses in `mac_ips.json`. Running `bin/descrypi` should report that the IP is updated and won't overwrite it.

A future feature will actually connect to the Pi and assign this address.

### Ping

`bin/descrypi ping` will ping Pi(s) in the `mac_ips.json` database.

## Other Tools

`bin/descrypi check_ieee_macs` will check whether there are new Raspberry Pi MAC prefixes registered with the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries). Realistically you never need to run this but I included this as it's quite interesting to know that there is a query-able database of Raspberry Pi MAC prefixes :-)

## To Do

* Use the existing database to actually assign static IPs
* Ping the database in succession to identify the machines by MAC (blinkenlights)

## Author

Paul Makepeace, 2019

