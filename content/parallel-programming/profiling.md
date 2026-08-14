# Profiling & Performance Analysis

```{rubric} Learning Objectives
:heading-level: 3
```

- Apply the "measure, don't guess" discipline and target the bottleneck that matters
- Inspect a machine's topology and bind threads to specific cores
- Measure achieved memory bandwidth and cache behavior with hardware counters or timing
- Find hotspots, cache misses, and memory errors with Valgrind
- Place a kernel on the roofline model and decide whether it is compute- or bandwidth-bound

---

## Measure, Don't Guess

The most common performance mistake is optimizing the wrong thing. [Amdahl's Law](theory.md) is blunt: speeding up code that accounts for 5% of runtime can never give more than 5% improvement. Before you change anything, **measure** where time actually goes.

A disciplined workflow:

1. **Time** the whole program and its phases to find where the time is.
2. **Profile** the hot region to find *why* it is slow (counters, cache misses).
3. **Classify** the bottleneck with the roofline: compute-bound or bandwidth-bound?
4. **Optimize** the dominant cost.
5. **Re-measure** to confirm a real gain.

---

## LIKWID — Hardware Performance Counters

LIKWID is a lightweight command-line toolkit for performance measurement on CPUs.

### Inspect the Machine

```bash
likwid-topology -g
```

This prints the socket/core/cache layout. You need it to interpret everything else — to know how big L1/L2/L3 are, how many physical cores exist, and how hyperthreads and NUMA domains are arranged.

### Measure Hardware Counters

List available performance groups:

```bash
likwid-perfctr -a
```

Then run your program pinned to a core under a group:

```bash
likwid-perfctr -C 0 -g MEM1 ./stream_triad
```

- `-C 0` pins execution to core 0.
- `-g MEM1` selects the memory-bandwidth counter group.

The output reports bytes read/written and achieved bandwidth in GB/s. Compare to your CPU's theoretical peak.

### Pin Threads

For OpenMP code, *where* threads run dominates memory performance on NUMA systems:

```bash
likwid-pin -c 0-7 ./vecadd          # pin 8 threads to cores 0-7
likwid-perfctr -C 0-7 -g MEM ./vecadd
```

Binding threads close to the memory they touch avoids cross-socket traffic.

### Alternative: Linux `perf`

If LIKWID is not installed, use `perf`:

```bash
perf stat -e LLC-loads,LLC-load-misses ./program
```

---

## Valgrind — Hotspots and Correctness

Where LIKWID reads real hardware counters, **Valgrind** runs your program on a synthetic CPU — slow, but needs no privileges.

| Tool | Purpose |
|------|---------|
| `callgrind` | Find hotspots by instruction count |
| `cachegrind` | Simulate cache and branch behavior |
| `memcheck` | Catch memory errors (leaks, overruns) |
| `helgrind` | Detect data races |

### Basic Usage

```bash
# Find hotspots
valgrind --tool=callgrind ./program

# Check for memory errors
valgrind --tool=memcheck ./program

# Check for data races
valgrind --tool=helgrind ./program
```


```{note}
Valgrind slows execution 10–50×. Use it for debugging, not benchmarking.
```


---

## The Roofline Model

The roofline turns measurements into decisions. It plots attainable performance against **arithmetic intensity** (FLOPs per byte):

$$\text{Attainable FLOP/s} = \min\!\left(\text{Peak FLOP/s},\; \text{Peak Bandwidth} \times \text{Arithmetic Intensity}\right)$$

Two ceilings:

- A sloped **bandwidth ceiling** on the left.
- A flat **compute ceiling** on the right.

| Kernel | FLOPs | Bytes | Intensity | Regime |
|--------|-------|-------|-----------|--------|
| Stream Triad | $2N$ | $24N$ | $\approx 0.08$ | bandwidth-bound |
| Dense matmul ($N=1024$) | $2N^3$ | $\approx 24N^2$ | $\approx N/12$ | compute-bound |

---

## Running on ARC Clusters

For LIKWID:

```bash
module load likwid
likwid-perfctr -C 0 -g MEM1 ./stream_triad
```

For Valgrind (workstation or login nodes):

```bash
valgrind --tool=memcheck ./program
```

---

## References

- [LIKWID Wiki](https://github.com/RRZE-HPC/likwid/wiki)
- [Valgrind Documentation](https://valgrind.org/docs/manual/quick-start.html)
