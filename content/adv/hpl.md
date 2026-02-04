# Tuning HPL
HPL (High Performance Linpack) is commonly used to benchmark HPC systems. Achieving good performance requires careful tuning of several parameters, mainly related to the problem size and process grid.

This is a very basic overview. Much more consideration goes into a good HPL run such as balancing [**multi-processing vs multi-threading**](mp-mt.md), choosing a BLAS library, etc.

---

## Understanding the Main Parameters

- **N**: The problem size (matrix dimension). Larger values of N generally lead to higher performance but require more memory. Make sure `N` fits in the total memory across nodes.
- **NB**: Block size. This affects how the matrix is divided among processes. Typical values range from 32 to 256. Smaller blocks reduce memory overhead, larger blocks improve cache utilization.
- **P and Q**: Process grid dimensions. HPL distributes the matrix over a `P x Q` grid of MPI processes. Choosing `P` and `Q` to match the cluster topology often improves performance. A nearly square grid (P≈Q) is usually best.
- **Number of Processes**: Usually matches the total number of available cores across nodes.

---

## Basic Tuning Strategy
- Start with a problem size that uses most of the available memory without swapping.
- Experiment with block sizes (`NB`) and observe performance.
- Adjust the process grid (`P x Q`) for better load balancing and communication efficiency.
- Make incremental changes and monitor the resulting GFLOPS to find the sweet spot.

---

## Running HPL
You typically run HPL with `mpirun` or `srun`, specifying the number of MPI processes. For example:

```bash
srun -np 16 ./xhpl
````

- Ensure that your `HPL.dat` file is configured with the chosen parameters.
- Monitor CPU and network usage to detect bottlenecks.
- Collect performance data and adjust parameters iteratively.

---

## Tips
- Always match the memory usage to physical memory to avoid swapping.
- Use square or slightly rectangular process grids for better communication.
- Tune one parameter at a time to understand its effect on performance.
- Compare results across different nodes and network configurations for optimal setup.