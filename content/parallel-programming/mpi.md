# MPI

```{rubric} Learning Objectives
:heading-level: 3
```

- Explain the SPMD execution model and the role of *rank*, *size*, and *communicator*
- Write, build, and launch a minimal MPI program with `mpirun`/`srun`
- Exchange data with point-to-point `MPI_Send`/`MPI_Recv` and explain how ordering causes deadlock
- Avoid deadlock using ordered sends, `MPI_Sendrecv`, or non-blocking `MPI_Isend`/`MPI_Irecv`
- Distribute and collect data with collective operations (`MPI_Bcast`, `MPI_Scatter`, `MPI_Gather`)

---

## A Different Axis of Parallelism

Every module so far has used **shared memory**: threads (OpenMP), vector lanes (SIMD), or GPU threads all read and write the *same* address space. [MPI](https://www.mpi-forum.org/docs/) is different. It is the tool for **distributed memory** — many separate processes, each with its own private memory, possibly on different physical nodes of a cluster, cooperating by *passing messages*.

This maps to the **MIMD** category of [Flynn's taxonomy](theory.md): Multiple Instruction, Multiple Data. It is how computation scales *beyond a single node*.


```{note}
MPI and OpenMP are complementary, not competing. Large HPC codes are commonly *hybrid*: MPI between nodes, OpenMP (or CUDA) within each node.
```


---

## The SPMD Model

MPI programs follow the **Single Program, Multiple Data** (SPMD) pattern: you launch *N* copies of the *same* executable, and each copy discovers its identity at runtime.

Four calls form the skeleton:

| Call | Purpose |
|------|---------|
| `MPI_Init(&argc, &argv)` | Start the MPI runtime; create the default communicator |
| `MPI_Comm_rank(comm, &rank)` | Get *this* process's ID (0 to size-1) |
| `MPI_Comm_size(comm, &size)` | Get the total number of processes |
| `MPI_Finalize()` | Tear down the runtime (required) |

A **communicator** is a named group of processes that can talk to each other. `MPI_COMM_WORLD` is the default, created by `MPI_Init`, containing every process in the job. A **rank** is a process's zero-based index within a communicator.

---

## Example 1 — Minimal MPI Program

```c
#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);

  int rank, nprocs;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &nprocs);

  printf("Rank %d of %d\n", rank, nprocs);

  MPI_Finalize();
  return 0;
}
```

### Building and Launching

```bash
# Compile with MPI wrapper
mpicc MinWorkExampleMPI.c -o min_mpi

# Launch with mpirun (on workstations)
mpirun -n 4 ./min_mpi

# Or with SLURM (on cluster)
srun --ntasks 4 ./min_mpi
```

**Expected output** (order is non-deterministic):
```text
Rank 2 of 4
Rank 0 of 4
Rank 3 of 4
Rank 1 of 4
```

---

## Example 2 — Point-to-Point Communication and Deadlock

The most fundamental MPI operation is sending a message from one rank to another:

```c
MPI_Send(buf, count, MPI_DOUBLE, dest, tag, comm);
MPI_Recv(buf, count, MPI_DOUBLE, source, tag, comm, MPI_STATUS_IGNORE);
```

### The Deadlock Problem

If every rank calls `MPI_Recv` *before* `MPI_Send`, all ranks wait forever — a classic **deadlock**.

### Four Ways to Fix It

1. **Send-then-Recv (unsafe)**: Works for small messages (eager protocol) but deadlocks for large ones.
2. **Ordered by parity (correct)**: Even ranks send first, odd ranks receive first.
3. **`MPI_Sendrecv` (clean)**: Combined call, scheduled safely by the library.
4. **Non-blocking (most flexible)**: `MPI_Isend`/`MPI_Irecv` + `MPI_Waitall` — can overlap computation with communication.

---

## Example 3 — Distributed Matrix-Vector Multiply

The problem: $y = Mx$ for an $N \times N$ matrix $M$ and vector $x$, with $N = 10000$.

**Strategy**: Domain decomposition — split the matrix by rows. Each process owns a contiguous block of rows and computes the corresponding block of the result.

### The Four Communication Phases

1. **Broadcast the vector** — every process needs the *whole* vector $x$:
   ```c
   MPI_Bcast(vector.data(), N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   ```

2. **Distribute matrix rows** — rank 0 sends each process its block of rows:
   ```c
   for (int dest = 1; dest < size; dest++) {
     MPI_Send(&matrix[dest_start_row * N], dest_rows * N, MPI_DOUBLE, dest, 0, comm);
   }
   ```
   Or better: use `MPI_Scatter` (library-optimized).

3. **Local computation** — each process multiplies its rows by the vector (no communication).

4. **Gather results** — each non-root process sends its partial result back to rank 0:
   ```c
   MPI_Send(local_result.data(), local_rows, MPI_DOUBLE, 0, 1, comm);
   ```
   Or: use `MPI_Gather`.

### Build and Run

```bash
# Compile
mpicxx vector_matrix_mpi.cpp -o vmm

# Launch
srun -n 4 ./vmm

# Or with SLURM
sbatch run.slurm  # Set --ntasks=4 in the script
```

---

## Running on ARC Clusters

For MPI jobs:

1. **Load MPI module** (if needed):
   ```bash
   module load openmpi
   ```

2. **Request nodes and tasks**:
   ```bash
   #SBATCH --nodes=2
   #SBATCH --ntasks-per-node=8
   ```

3. **Submit**:
   ```bash
   sbatch run.slurm
   ```

See [Running Jobs](../running-jobs/index.md) for SLURM details.

---

## References

- [MPI Forum Standard](https://www.mpi-forum.org/docs/)
- [Open MPI Documentation](https://www.open-mpi.org/doc/)
- [MPICH Documentation](https://www.mpich.org/static/docs/latest/)
