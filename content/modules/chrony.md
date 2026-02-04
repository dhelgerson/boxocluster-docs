page
Keeping Time
Set up chrony to keep time.

---

# Keeping Time

## Objective: Setup chronyd to keep time

Because of the intercommunication between storage, compute, and head nodes, it's important that every node in the system is in lockstep with each other.

Our goal is to setup a time server and have every node sync time with it using the [NTP](https://en.wikipedia.org/wiki/Network_Time_Protocol) protocol. While Rocky comes with `systemd-timesyncd`, we're going to replace it with `chrony` as it can act as both a NTP server(head) and client(nodes).

## Selecting the Time Server

Before we put hands on keyboards, we need to think about which node should be the time server. Off the bat, a compute or storage node is not appropriate - these should dedicate resources to performing calculations or providing high-speed storage. Furthermore, these nodes will be wiped every boot. In our setup, this leaves us with the head node. This node will need to be the first one to be turned on, and should always be properly shutdown.

## Setting the Time

Resources: [timedatectl](https://www.freedesktop.org/software/systemd/man/timedatectl.html), [grep](https://linux.die.net/man/1/grep)

You can check the current status of the time by using `timedatectl`.

The time zone should automatically be set, but if it isn't, you can set it:

```bash
sudo timedatectl set-timezone <time zone>
```

If you are unsure what time-zones are available, use `timedatectl list-timezones` to list out all available time-zones - `grep` can be useful for narrowing the list down.

The time is set using:

```bash
# if an ntp server is already running, stop if first with:
sudo systemctl stop systemd-timesyncd
# then change the time w/
sudo timedatectl set-time "YYYY-MM-DD HH:mm:ss"
# or individually with: 
sudo timedatectl set-time "YYYY-MM-DD"
sudo timedatectl set-time "HH:mm:ss"
# finally remember to start the NTP service again w/:
sudo systemctl start systemd-timesyncd
```

The examples above show that you can either give it a full timestamp or a partial one. Keep in mind that time is represented using **24-hour time**. You don't want to be 12 hours off!

## Configuring Chrony on the Head

Resources: [systemd-timesyncd](https://wiki.archlinux.org/title/Systemd-timesyncd), [chrony](https://chrony-project.org), [apt](https://linux.die.net/man/8/apt)

Since chrony is initially setup as a client, we'll need to do some configuration. First, stop `chrony`.

```bash
sudo systemctl stop chronyd
```

Now edit `/etc/chrony.conf`. Clear all lines and make sure it only contains these lines:

```bash
driftfile /var/lib/chrony/drift
# grab internet time if available
pool 2.rocky.pool.ntp.org iburst
# sync to local server
server 127.127.1.1
# allow much variance before errors are thrown
local stratum 8
# host server for nodes
allow all
```

The IP address `127.127.1.1` is the loopback address for NTP. You are telling `chrony` to sync with the system's clock driver. This isn't considered best practice, but for our purposes, it'll do the trick. Now restart `chrony`.

```bash
sudo systemctl start chronyd
```

You can check the status of `chrony` using `chronyc tracking` and see if it's actually using the loopback address with `chronyc sources`.

## Replacing timesyncd With chrony on the Nodes

Resources: [pdsh](https://linux.die.net/man/1/pdsh), [grep](https://linux.die.net/man/1/grep)

Enter the Node container chroot (you'll need to be root):

```bash
wwctl container exec base-rocky9 /bin/bash
```

**Note:** while in the Warewulf container chroot, the exit status of the last command deterines whether the changes are commited. This can be viewed in the prompt, either "write" or "exit"

Repeat the above process to stop, disable, and uninstall `systemd-timesyncd`. and to install `chrony`. 

Next, you'll need to edit `/etc/chrony.conf` to be the following:

```bash
driftfile /var/lib/chony/drift
server 10.0.0.11 iburst
```

Note: here, `iburst` is very important; it tells chrony to immediately sync with the server upon boot.

Now `exit` the container and wait for it to rebuild, and reboot the nodes

Once everybody is booted and pretty much within 0 seconds of NTP time, we're ready for the next module.
