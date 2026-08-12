# Box O' Cluster

Run your own Virtual HPC cluster using QEMU

# Getting Started

Running Boxocluster is as simple as grabbing the head node's disk image and the docker-compose file and running the stack.

## Linux

Linux has a host of container run-times, here I'll show one that requires root and one that does not

### With Docker

Docker is native on linux. Ensure you have docker-compose v2 installed, then do the following:

```bash
git clone https://github.com/dhelgerson/boxocluster.git
cd boxocluster
curl -LO https://boxocluster.com/boxocluster-node-1.qcow2
docker compose up -d
docker compose logs -f &
```

- follow the instructions to connect to your new virtual cluster

### With Apptainer

If you don't have sudo, you're not out of luck. apptainer runs in userspace and can also be used. Run the following and follow the instructions.

```bash
curl -LO https://boxocluster.com/boxocluster-node-1.qcow2
apptainer run --containall \
  --cwd $PWD \
  --bind /dev/kvm:/dev/kvm \
  --bind $PWD:$PWD \
  docker://ghcr.io/dhelgerson/boxocluster:main &
```

## Windows

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

## macOS

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

## What Next

After you have a running virtual cluster, feel free to follow the steps at https://boxocluster.com to continue setting it up.

## Attributions

boxocluster is intended to be an instructional tool to help students new to the world of High Performance Computing through a series of modules that should guide them from a virtual pile of hardware put in front of them to a working miniature compute cluster.

boxocluster was developed by Drew Helgerson, John Bradley, and his students at the [Mississippi State University High Performance Computing Collaboratory (HPC2)](https://hpc.msstate.edu) for students at the university and is released to the public for all to benefit.

If you have any questions, comments, or suggestions for improvement, feel free to send an email to [drew.helgerson@msstate.edu](mailto:drew.helgerson@msstate.edu) or [jbradley@hpc.msstate.edu](mailto:jbradley@hpc.msstate.edu).

Website content is licensed under CC BY-NC-SA 4.0. Code is distributed under MIT.
