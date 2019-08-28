# Descry Pi

Find ("descry") freshly installed Raspberry Pi's on your network!

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
# Run any of the bin/* programs
```

## Flow

First, run `bin/fping eth0` (or `en0` on macOS) or whichever interface your Pi is hanging out at. You don't strictly need to do this if your Pi and workstation have been in communication recently but the network (ARP) cache can expire so this will refresh it.

Then run `bin/descrypi` to find your Pi(s)!

This should report newly found Pi(s) and create a database, `mac_ips.json`. Next time you run `bin/descrypi` it'll recognize that MAC->IP mapping.

Next, if you want to assign a static IP to the machines update the IP addresses in `mac_ips.json`. Running `bin/descrypi` should report that the IP is updated and won't overwrite it.

A future feature will actually connect to the Pi and assign this address.

## Other Tools

`bin/check_rpi_macs` will check whether there are new Raspberry Pi MAC prefixes registered with the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries). Realistically you never need to run this but I included this as it's quite interesting to know that there is a query-able database of Raspberry Pi MAC prefixes :-)

## To Do

* Use the existing database to actually assign static IPs
* Ping the database in succession to identify the machines by MAC (blinkenlights)

## Author

Paul Makepeace, 2019

