# Descry Pi

Find [headless](https://en.wikipedia.org/wiki/Headless_computer) Pi(s) on your network without connecting a keyboard and monitor, or digging around in DHCP lease tables!

In addition to scanning, `descrypi` can perform operations on all Pi hosts,

* check they're up (ping)
* copy SSH keys
* change default passwords
* show local and remote network configurations
* run arbitrary commands remotely using `ssh`

Not only that, `descrypi` will create an [inventory file](https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html) so you can harness the power of [Ansible](https://docs.ansible.com/ansible/latest/index.html) to continue setting up your cluster.

It currently works with [Raspberry Pi](https://www.raspberrypi.org) (fully) and [Rock Pi](http://rockpi.org) (partially).

## Installation

### Dependencies

DescryPi is written in Python 3 with no Python package dependencies, and should work on macOS and Linux.

You'll need Python 3 and `fping`:

* macOS: `brew install python fping`
* Ubuntu: `sudo apt-get install python3 fping`
* etc

It also uses `arp` and `ssh-copy-id` but you almost certainly already have those. (If not, `arp` is in the Linux net-tools package and `ssh-copy-id` is in `openssh-client`.)

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

### Copy SSH Keys

Enable password-less login using [`ssh-copy-id`](https://www.ssh.com/ssh/copy-id):

```shell script
bin/descrypi ssh-copy-id
```

This will prompt for the existing password. You can simply hit Return if it's still the default installed `raspberry`.

Note: if you're asked for the password again (e.g. `pi@192.168.2.65's password:`) then it means the given password was rejected; try again with the correct password.

### Passwd

*Note: Raspberry Pi only*

Raspberry Pi recommends changing the default password for the `pi` user (from `raspberry`) as soon as you can. It's easy to do it with DescryPi:

```shell script
bin/descrypi passwd
```

As for `ssh-copy-id`, you can hit Return to accept the default `raspberry` password.

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

*Note: Raspberry Pi only*

`bin/descrypi check_ieee_macs` will check whether there are new Raspberry Pi MAC prefixes registered with the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries). Realistically you never need to run this but I included this as it's quite interesting to know that there is a query-able database of Raspberry Pi MAC prefixes :-)

## Ansible

DescryPi writes out an Ansible inventory file `hosts.json`, containing all the discovered Pi(s) grouped under the `pi` hosts group. This opens up the power of Ansible for managing your fleet. As a simple example, the following command will show each Pi's `uptime`,

```shell script
ansible -i hosts.json -m shell -a uptime pi
```

## To Do

* While the [Raspberry Pi's OS, Raspbian](https://www.raspberrypi.org/downloads/raspbian/) has a default user and password to login, [Armbian](https://www.armbian.com), which is used on many other Pi-alikes, insists on changing the root password as first order of business. `descrypi` doesn't support this yet.
* Use the existing database to actually assign static IPs
* Ping the database in succession to identify the machines by MAC (blinkenlights)

## More

I've written some brief notes on [installing images](docs/Images.md) to an SD card.

Descry? [Detect, dig out, discover, dredge up, ...](https://www.merriam-webster.com/dictionary/descry)

## Author

Paul Makepeace, 2019

