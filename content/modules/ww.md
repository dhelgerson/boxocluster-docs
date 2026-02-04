# System Provisioning

## Objective

Understand how Warewulf(ww) is setup on the Head Node and how it works.

## References

Resources: [Linux Boot Process](https://en.wikipedia.org/wiki/Booting_process_of_Linux), [WareWulf Docs](https://warewulf.org/docs/v4.5.x/), [PXE](https://en.wikipedia.org/wiki/Preboot_Execution_Environment), [iPXE](https://ipxe.org/docs)

## What is WareWulf?

Warewulf is a purpose-built stateless booting system built for large-scale HPC's. It's what the [HPC2](https://hpc.msstate.edu) uses to boot and maintain the state of thousands(literally) of cluster nodes. It does this by maintaining a "Golden Image" of a compute node as desired and sending it to each node when it boots. This means that every time a node reboots. it's entirely wiped and returned to the desired state. There are some advantages and some drawbacks to this approach. Careful consideration must be taken when building these images so that they will consistently work on all nodes.

## Using WareWulf

Due to the complexity of Warewulf, it has already been setup for you, this doc is to acquaint you with how it works and give some instructions required later on such as how to modify the node image.

## How Warewulf Works

A number of moving parts come together for Warewulf to work. A desired server hosts a number of services including Warewulf's server daemon, dhcp, and tftp which are all needed for different stages of the boot process. Every node booted with Warewulf requires the following during its boot processes: a container which acts as a traditional system's root drive, a linux kernel, and an assortment of overlays which are stacked on top of the container depending on certain environmental differences. These overlays allow a single container to be used for many, if not all, nodes, changing what's necessary between them.

## The Warewulf Boot Process

Bringing an entire working operating system up with no internal storage is no small task. Warewulf accomplishes it in stages.

1. **PXE Boot:** PXE is the the standard net-boot protocol for most machines. The ww server hosts a PXE image for its custom boot environment
2. **iPXE:** iPXE is a similar standard to PXE but much more extensible. iPXE reaches out to the ww server, handshakes, and retrieves necessary files
3. **/bin/init:** once the initramfs is copied, it pulls the container and overlays, sets up the new root, and executes /bin/init. from there the system comes up just as a traditional system.

## Common/Useful Warewulf commands

Chroot'ing into the container to make changes to the compute nodes interactively:

- **Note:** the exit status of the last command dictates whether Warewulf saves changes made in the chroot. this is indicated in the prompt by either a "write" or a "discard". exit the container with either Ctrl+D or `exit`

```bash
wwctl container exec base-rocky9 /bin/bash
```

As above but making the host's `/shared` and `/apps` 
```bash
wwctl container exec --bind /shared:/shared base-rocky9 /bin/bash
```

Copying Contianers, useful when testing changes

```bash
wwctl container cp original-container copy-container
```

Changing a node's container

```bash
wwctl node set --container container-name node-name
```

Rebuilding Overlays, must be rebuild after most config changes

```bash
wwctl overlay build [node]
```

## Reboot the Nodes

```bash
pdsh -a reboot
```
At this point, power on the nodes. They should begin booting and pulling their images. We'll configure these images in future steps.

