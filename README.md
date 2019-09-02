# Descry Pi

Find ("descry") freshly installed Raspberry Pi(s) on your network!

This toolset aims to be easier than using `fing` and, ultimately, more useful.

Currently, it's written in Python 3 with no Python package dependencies, and should work on macOS and Linux.

## Installation

### Dependencies

There is an external dependency on a common executable though: install `fping`:

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

### Find

To find your Pi(s) simply run,

 ```shell
bin/descrypi
 ````

This will ping every host on each of your workstation's IPv4 interfaces then report any found Pi(s). Those Pi(s) will be stored in a local a (text file) database, `mac_ips.json`. Next time you run `bin/descrypi` it'll recognize that MAC-to-IP mapping.

### Assign (TODO)

Next, if you want to assign a static IP to the machines update the IP addresses in `mac_ips.json`. Running `bin/descrypi` should report that the IP is updated and won't overwrite it.

A future feature will actually connect to the Pi and assign this address.

### Ping

To ping Pi(s) in the `mac_ips.json` database,

```shell
bin/descrypi ping
```

## Other Tools

### Networks

```shell
bin/descrypi networks
```

This will show you local (workstation) networks, and remote (Pi) networks.

If you want to restrict your scanning to a particular interface this command can be useful to see what local networks are present and the name of their interface.

### SSH

Handy command to `ssh` to the scanned hosts, e.g.,

```shell
bin/descrypi ssh uptime
```

To avoid `descrypi` attempting to parse argument flags, quote them, e.g.,

```shell
bin/descrypi ssh "ls -al"
```

### Check for new MAC prefixes

`bin/descrypi check_ieee_macs` will check whether there are new Raspberry Pi MAC prefixes registered with the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries). Realistically you never need to run this but I included this as it's quite interesting to know that there is a query-able database of Raspberry Pi MAC prefixes :-)

## To Do

* Use the existing database to actually assign static IPs
* Ping the database in succession to identify the machines by MAC (blinkenlights)

## Author

Paul Makepeace, 2019

