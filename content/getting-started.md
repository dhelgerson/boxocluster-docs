# Getting Started

Running Boxocluster is as simple as grabbing the head node's disk image and the docker-compose file and running the stack.

## Get the VM image
```bash
curl -LO https://boxocluster.com/boxocluster-node-1.qcow2
```

## Run the Container
### Linux

Linux has a host of container run-times, here I'll show one that requires root and one that does not

#### With Docker

Docker is native on linux. Ensure you have docker-compose v2 installed, then do the following:

```bash
git clone https://github.com/dhelgerson/boxocluster.git
cd boxocluster
docker compose up -d
docker compose logs -f &
```

- follow the instructions to connect to your new virtual cluster

#### With Apptainer

If you don't have sudo, you're not out of luck. apptainer runs in userspace and can also be used. Run the following and follow the instructions.

```bash
apptainer run --containall \
  --cwd $PWD \
  --bind /dev/kvm:/dev/kvm \
  --bind $PWD:$PWD \
  docker://ghcr.io/dhelgerson/boxocluster:main &
```

```{note}
There is currently a known bug with apptainer that causes multicast connections to be reset. 
This prevents the compute nodes from booting.
We are currently investigating a solution, but for now, just run all head-node commands as it makes up the majority.
```

### Windows

Docker Desktop is recommended for Windows.

1. **Download Docker Desktop**

   * Go to [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).
   * Download the installer for Windows.

2. **Run the installer**

   * Double-click the `.exe` file and follow the prompts.
   * When asked, enable:

     * **Use WSL 2 instead of Hyper-V** (recommended for most users).
     * Install the **required WSL 2 feature** if you don’t already have it.

3. **Restart your machine** (if prompted).

4. **Verify installation**

   * Open **PowerShell** or **Command Prompt** and run:

     ```powershell
     docker --version
     docker compose version
     ```
   * You should see Docker and Docker Compose versions printed.

5. From here, you can follow the steps for [Docker](#with-docker).

### macOS

Docker Desktop is recommended for macOS.

1. **Download Docker Desktop**

   * Go to [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/).
   * Download the `.dmg` installer for macOS.

2. **Install Docker Desktop**

   * Open the downloaded `.dmg` file.
   * Drag the Docker icon into your **Applications** folder.
   * Launch Docker from **Applications**.

3. **Grant permissions if prompted**

   * You may need to enter your macOS password to allow Docker to install helper tools.

4. **Verify installation**

   * Open **Terminal** and run:

     ```bash
     docker --version
     docker compose version
     ```
   * You should see Docker and Docker Compose versions printed.

5. From here, you can follow the steps for [Docker](#with-docker)

## Log into the head-node
Once the container starts, the head node will boot. Once it is done booting, you can ssh into it with:
```
ssh -p 2222 admin@localhost
```

After the head node boots, allow the compute nodes some time to boot. their status can be viewed by running `tail -f computeX.out` where x is the node number.

Once the Nodes are done booting, it's recommended to control them in parallel with pdsh.
```{warning}
There's currently a bug that 'causes the compute nodes to bind pubkeys to the first user that ssh's to them. This will be fixed in the future. Currently, the workaround is to issue the following command before doing anything else to ensure pubkeys bind to root first.
```

```bash
sudo su -
pdsh -a whoami
```

If all nodes return with 'root' (you may get some messages about accepting the hostkeys), then you're good to go!
