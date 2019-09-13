# Installing Images

There's plenty of existing docs on creating bootable SD/eMMC cards so this is aimed at the more experienced user who can operate from a bunch of command lines and search out solutions if they run into problems.

The following examples assume a macOS workstation although the download section should run as-is on Linux.

## SD Cards

TL;DR Samsung EVO Plus are the best for the money right now.

## Find your `/dev/disk`

Before you start erasing disks make sure you're erasing the right one...

```shell script
diskutil list
```

Pick out the SD/eMMC card and, for the following commands, assign `DISK`:

```shell script
DISK=disk2
```

*Note: don't include the `s2` etc partition, just the disk and its number.*

## Image

Pick your OS! Here are two examples.

### Raspbian

If you have a Raspberry Pi, you almost certainly want [Raspberry Pi's OS, Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

Since I'm interested in servers, I'm going for the "Lite" version:

```shell
curl --silent --location https://downloads.raspberrypi.org/raspbian_lite_latest --output raspbian_lite.tgz
tar -xf raspbian_lite.tgz --to-stdout '*.img' > raspbian_lite.img
sudo dd if=raspbian_lite.img of=/dev/r$DISK bs=1m conv=sync
```

*Note: the `disk` here is `rdisk` which is the "raw disk" which means writes happen direct to the hardware without being buffered by the OS. It turns out this is significantly faster.*
 
#### Configure

Raspbian doesn't enable SSH by default so you have to tweak the image by adding an empty `ssh` file to the root of the boot disk:

```shell script
diskutil mountDisk /dev/$DISK # typically happens automatically after the `dd` above
touch /Volumes/boot/ssh
```

If you'd like to have Wi-Fi working out of the box, create a `wpa_supplicant.conf` file:

```shell script
cat > /Volumes/boot/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="<your SSID>"
    psk="<your password>"
    key_mgmt=WPA-PSK
}
^D
```

Or, for an open Wi-Fi network, replace the above `network` stanza with:

```
network={
    ssid="<your SSID>"
    key_mgmt=NONE
}
```

Skip to "First Boot" section below.

### Armbian

Armbian is an OS for "everything-but-Raspberry Pi" single board computers (SBC's).
Their images are compressed using the [7-Zip format](https://www.7-zip.org/7z.html). On macOS, `p7zip` works fine,

```shell script
brew install p7zip
```

As above, figure out the correct disk and assign to `DISK`.

Armbian [provide OS's for many SBC's](https://www.armbian.com/download/) so there's some decisions needed. I have a Rock Pi 4 so:

```shell script
curl --location --remote-name --remote-header-name https://dl.armbian.com/rockpi-4b/Debian_buster_default.7z 
7z x Debian_buster_default.7z
sudo dd if=Armbian*Rockpi-4b_Debian_buster_default_*.img of=/dev/r$DISK bs=1m conv=sync
```

Both Raspbian and Armbian have default user and passwords: `pi` with `raspberry`, and `root` with `1234`, respectively.

However, while Raspbian disables SSH but gives `pi`a full shell, Armbian enables SSH by default but has a restricted shell that initially requires changing the root password and creating a new (non-root) account.

## First Boot

Prepare to remove the card:

```shell script
diskutil umountDisk /dev/$DISK
```

Remove the card, pop it in your Pi, and boot! It'll take a couple of minutes to resize the partition, reboot, etc. If you're running [headless](https://en.wikipedia.org/wiki/Headless_computer) you should at least see the green LED blink. Then, run `bin/descrypi` and setup your computer :-)
