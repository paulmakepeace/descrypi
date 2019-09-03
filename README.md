# Descry Pi

Find Raspberry Pi(s) on your network without connecting a keyboard and monitor, or digging around in DHCP lease tables!

Then, using auto-generated inventory files, harness the power of Ansible to setup your cluster.

## Installation

### Dependencies

DescryPi is written in Python 3 with no Python package dependencies, and should work on macOS and Linux.

You'll need Python 3 and `fping`:

* macOS: `brew install python fping`
* Ubuntu: `sudo apt-get install python3 fping`
* etc

It also uses `arp` but you almost certainly already have that. (If not, it's in the Linux net-tools package.)

### Download

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

This will ping every host on each of your workstation's IPv4 interfaces then report any newly found Pi(s). Those Pi(s) will be stored in a local (text file) database, `hosts.json`. Next time you run `bin/descrypi` it'll recognize that MAC-to-IP mapping.

### Assign (TODO)

Next, if you want to assign a static IP to the machines update the IP addresses in `hosts.json`. Running `bin/descrypi` should report that the IP is updated and won't overwrite it.

A future feature will actually connect to the Pi and assign this address.

## Other Tools

### Ping

To ping Pi(s) in the `hosts.json` database,

```shell
bin/descrypi ping
```

### Networks

```shell
bin/descrypi networks
```

This will show your local (workstation) networks, and remote (Pi) networks.

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

## Ansible

DescryPi writes out an Ansible inventory file `hosts.json`, containing all the discovered Pi(s) grouped under the `pi` hosts group. This opens up the power of Ansible for managing your fleet. As a simple example, the following command will show each Pi's `uptime`,

```shell script
ansible -i hosts.json -m shell -a uptime pi
```

## To Do

* Use the existing database to actually assign static IPs
* Ping the database in succession to identify the machines by MAC (blinkenlights)

## Author

Paul Makepeace, 2019

