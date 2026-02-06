# Multi-processing vs. Multi-threading
When running jobs on HPC clusters using Slurm, understanding the difference between **multi-threading** and **multiprocessing** is crucial for efficient resource usage.

---

## Nomenclature

**Process**
: An independent instance of a program with its own memory space. In HPC, a process typically corresponds to one Slurm task.  

**Thread**
: A lightweight execution unit within a process. Threads share the process’s memory space and are used for multi-threaded parallelism.  

**Rank**
: In MPI programs, a rank is the identifier of a specific process in a communicator. For example, `rank 0` often represents the first, commonly the “master” process.  

**Task**
: Slurm terminology for a unit of work; usually maps to a process.  

**Node**
: A single physical or virtual machine in a cluster. A node can run multiple tasks or threads.  

**Core**
: A hardware CPU core; threads and processes are scheduled on cores.  

**Hybrid Parallelism**
: Using both multiple processes (MPI ranks) and multiple threads per process (OpenMP or threading libraries) simultaneously.

---

## Multi-Threading
Multi-threading uses multiple threads within a single process. Threads share the same memory space, which makes communication fast but limits scalability across multiple nodes. Many interpreted languages, like Python, are effectively **multi-threaded only** because of the Global Interpreter Lock (GIL), which prevents true parallel execution of threads in CPU-bound tasks. Python can use multiple threads for I/O-bound work efficiently, but CPU-bound tasks usually require **multiprocessing** or native extensions.

### Slurm Example: Allocating Threads

```bash
#!/bin/bash
#SBATCH --job-name=threads_example
#SBATCH --output=threads_output.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:10:00
#SBATCH --partition=short

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Run a multi-threaded program (e.g., OpenMP or Python using threads)
./my_multithreaded_program
````

- `--ntasks=1` indicates a single process.
- `--cpus-per-task` specifies the number of threads.
- OpenMP-aware programs or Python thread pools will use `OMP_NUM_THREADS` threads.

---

## Multiprocessing

Multiprocessing uses multiple processes, each with its own memory space. This is ideal for CPU-bound tasks in Python, MPI programs, and distributed workloads. Multiprocessing scales across nodes if combined with MPI or other communication frameworks.

### Slurm Example: Allocating Processes

```bash
#!/bin/bash
#SBATCH --job-name=mpi_example
#SBATCH --output=mpi_output.txt
#SBATCH --ntasks=16
#SBATCH --time=00:10:00
#SBATCH --partition=short

# Run an MPI program
mpirun -np $SLURM_NTASKS ./my_mpi_program
```

- `--ntasks=16` launches 16 separate processes.
- Each process can run on a different core or node.

---

## Combining Threads and Processes

Some HPC applications use **hybrid parallelism**, combining multiple processes with multi-threading inside each process (common with MPI + OpenMP).

### Slurm Example: Hybrid MPI + Threads

```bash
#!/bin/bash
#SBATCH --job-name=hybrid_example
#SBATCH --output=hybrid_output.txt
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=8
#SBATCH --time=00:10:00
#SBATCH --partition=short

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Run a hybrid MPI + OpenMP program
mpirun -np $SLURM_NTASKS ./my_hybrid_program
```

- Launches 4 MPI processes.
- Each MPI process spawns 8 threads for computation.
- Total cores used = `ntasks * cpus-per-task = 32`.

---

### Key Points
- Use **multi-threading** for shared-memory, single-process parallelism (OpenMP, Python threads).
- Use **multiprocessing** for CPU-bound tasks, true parallelism, or multi-node scaling (MPI, Python `multiprocessing`).
- Hybrid models combine both for maximum performance on multi-core nodes.
- Always match Slurm allocations (`ntasks`, `cpus-per-task`) to your program’s parallelization model to avoid over- or under-utilization.
