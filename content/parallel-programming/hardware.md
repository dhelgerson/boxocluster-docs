# Hardware and Data Layout

```{rubric} Learning Objectives
:heading-level: 3
```

- Describe the memory hierarchy and cite approximate latencies at each level
- Explain what a cache line is and how data movement between levels works
- Contrast data-oriented programming (DOP) with object-oriented programming (OOP) and state when each is appropriate
- Identify array allocation patterns that break cache efficiency
- Explain C/C++ row-major vs Fortran column-major ordering and the interoperability pitfall that follows from it

---

## The Memory Hierarchy

Modern CPUs are not compute-limited on most workloads — they are memory-limited. The memory hierarchy exists because fast memory is physically expensive; the solution is to stage data in progressively larger, slower stores and rely on locality to keep the fast levels hot.

### Memory Divide (NUMA)

Most CPUs, since the start of multi-socket solutions, have featured a segregated memory design that makes it so that each socket has its own memory. This solution is called Non-Uniform Memory Access which makes it so that the time it takes one CPU to access a specific part of memory is different than another CPU. As processors continue to become more complex and smaller in process size, we started dividing a single CPU into separate dies. But since every core no longer shares the same L3 cache or memory controllers, they too are considered NUMA. This causes severe cache misses and latency when attempting to access the memory located on another memory controller. To combat this issue, we can treat each compute die as a NUMA node. To calculate how many NUMA nodes, or "sockets", a node has, one can use the following formula: $\text{NUMA Nodes} = \text{Physical Sockets} \times \text{Compute Dies}$.

Although small, not accounting for NUMA when running a HPC job will have a significant and consistent effect on runtime and performance.

To learn more about NUMA and its history, here is the [Wikipedia](https://en.wikipedia.org/wiki/Non-uniform_memory_access) article on it.

### Latencies

| Level | Size (typical) | Latency | Cycles (@ 3 GHz) |
|---|---|---|---|
| Registers (L0) | ~1 KiB | < 1 ns | ~1 |
| L1 cache (SRAM) | 32–64 KiB | ~2 ns | ~3–4 |
| L2 cache | 256 KiB – 1 MiB | ~6 ns | ~15 |
| L3 cache | 8–64 MiB | ~15–25 ns | ~50 |
| DRAM | GiBs | ~100 ns | ~200 |
| NVMe SSD | TiBs | ~20 μs | ~60,000 |
| Spinning disk | TiBs | ~10 ms | ~30,000,000 |

Each level is roughly 10× slower and 10–100× larger than the one above it. The gap between L3 and DRAM (~4–8×) is where most HPC programs lose performance: the CPU can issue memory requests far faster than DRAM can satisfy them.

### Human-Scale Analogy

To make the latency ratios intuitive, scale 1 CPU cycle to 1 second:

| Level | Scaled latency |
|---|---|
| L1 cache | ~4 seconds |
| L2 cache | ~15 seconds |
| L3 cache | ~50 seconds |
| DRAM | ~3–4 minutes |
| NVMe SSD | ~2–3 days |
| Spinning disk | ~1 year |

A thread that stalls on a DRAM fetch is waiting the equivalent of several minutes while the rest of the pipeline is idle. Instructions that read data from an SSD drive are doing the equivalent of fetching each item from a warehouse three time zones away.


```{note}
These latencies are for *random access*. Sequential access saturates the hardware prefetcher, which issues read-ahead requests before the core asks for the data. Effective sequential bandwidth to L3 or DRAM can be 10–50× higher throughput than random access achieves.
```


---

## Cache-Line Mechanics

### Data Moves in 64-Byte Chunks

Data does not move between cache levels one word at a time. It moves in *cache lines* — fixed 64-byte blocks aligned to 64-byte boundaries on all current x86 and ARM server processors. One cache line holds exactly 8 `double` values (8 bytes each).

When your code loads a single `double` from memory, the hardware fetches the entire 64-byte line containing that address. The other 7 doubles in that line land in the cache whether you asked for them or not.

Think of the memory subsystem as a bucket brigade, not a pipe: you order one item and receive a full bucket. If you use the rest of the bucket, the transfer cost is amortized over 8 loads. If you discard it, you paid the full transfer cost for one useful value.

### Sequential vs Random Access

#### "Sequential (cache-friendly)"

```cpp
double sum = 0.0;
for (int i = 0; i < N; ++i) {
  sum += a[i];  // Each cache line covers a[i..i+7]; 8 loads per fetch.
}
```

The hardware prefetcher detects the stride-1 pattern and begins loading the next cache line before the current one is exhausted. Effective bandwidth approaches the hardware peak (~50–200 GB/s on DDR5).

#### "Random (cache-hostile)"

```cpp
double sum = 0.0;
for (int i = 0; i < N; ++i) {
  sum += a[idx[i]];  // idx[i] is random; each load is a different cache line.
}
```

Every access is likely a cache miss. The prefetcher cannot predict the pattern. Effective bandwidth collapses to the random-access rate (~5–20 GB/s), because 64 bytes are fetched to use 8.

### The TLB and Large Pages

The Translation Lookaside Buffer (TLB) caches the mapping from virtual to physical addresses. With default 4 KiB pages, the TLB can cover at most $4096 \times 4096 = 16$ MiB of virtual address space simultaneously. Accessing a large array in a sparse pattern generates TLB misses, each costing a full page-table walk (~100–200 cycles).

**Huge pages** (2 MiB or 1 GiB on x86) extend TLB coverage by a factor of 512 or 262144. For large-array workloads with moderate spatial locality, enabling transparent huge pages or using `mmap(MAP_HUGETLB)` can deliver greater than 10% speedup with no code changes. Sparse access patterns that thrash TLBs can show 20–40% miss rates under default page sizes.

---

## Data-Oriented Programming (DOP)

### OOP and the Array-of-Structs (AoS) Problem

Object-oriented design encourages grouping related fields into a struct or class and then operating on arrays of those objects. This is natural for source-code organization:

```cpp
// Array of Structs (AoS) -- OOP style
struct Circle {
  double r;
  double x;
  double y;
  double z;
};

Circle circles[N];
```

Each `Circle` occupies 32 bytes (4 × 8). When computing total area — iterating over every `r` — each cache line fetch pulls in `r`, `x`, `y`, and `z` for two circles. Only 25% of the fetched bytes are `r`; the rest are wasted bandwidth:

```cpp
for (int i = 0; i < N; ++i) {
  area += M_PI * circles[i].r * circles[i].r;  // loads r, x, y, z; uses only r
}
```

This is not an OOP design failure — it is the correct OOP design. The problem is that OOP *organizes source code around data types* rather than grouping individual fields into arrays that can be streamed efficiently.

### DOP and the Struct-of-Arrays (SoA) Layout

Data-oriented programming separates concerns: field access patterns determine physical layout, not conceptual grouping.

```cpp
// Struct of Arrays (SoA) -- DOP style
struct CircleData {
  double r[N];
  double x[N];
  double y[N];
  double z[N];
};

CircleData circles;
```

Now `r[0..N-1]` is contiguous. Iterating over radii loads only radii; every byte in every cache line is a radius value. For $N = 8$ doubles = 64 bytes = one cache line, the bandwidth utilization is 100%:

```cpp
for (int i = 0; i < N; ++i) {
  area += M_PI * circles.r[i] * circles.r[i];  // every loaded byte is used
}
```


```{tip}
The SoA layout also enables auto-vectorization. A SIMD vector instruction can load 4 or 8 consecutive doubles from `circles.r` and process them in parallel. Loading every fourth double from an AoS layout requires a gather instruction, which is 4–8× slower on current hardware.
```


### Choosing AoS vs SoA

| Pattern | Prefer |
|---|---|
| Operations use all fields of one object at once | AoS (e.g., rigid body: apply transform to r, x, y, z together) |
| Operations scan one field across many objects | SoA (e.g., integrate all positions, then all velocities) |
| SIMD vectorization of a single field | SoA |
| Mixed access (some ops use all fields, some use one) | SoA with manual gather, or AoSoA (tiled hybrid) |

---

## Multi-Dimensional Array Pitfalls

### The Pointer-of-Pointers Anti-Pattern

A common C idiom for dynamic 2D arrays allocates each row separately:

```c
// BAD: rows on different heap pages
int **my_array = malloc(3 * sizeof(int *));
for (int i = 0; i < 3; i++) {
  my_array[i] = malloc(4 * sizeof(int));
}
```

Each `malloc` call returns memory from an arbitrary heap location. Rows are almost certainly not adjacent in memory. Iterating `my_array[0][3]` to `my_array[1][0]` crosses a page boundary; the TLB and cache must load a new line. Freeing requires a loop of `free` calls; forgetting any one is a memory leak.

```c
// GOOD: single contiguous allocation
int my_array[3][4];         // stack — guaranteed contiguous
// or
int (*my_array)[4] = malloc(3 * sizeof(*my_array));  // heap — one allocation
```

In C++:

#### "BAD: vector of vectors"

```cpp
// No contiguity guarantee — each inner vector is a separate heap allocation.
std::vector<std::vector<int>> my_array = {
  {0, 1, 2, 3},
  {4, 5, 6, 7},
  {8, 9, 10, 11}
};
```

#### "GOOD: fixed-size contiguous"

```cpp
// std::array is guaranteed contiguous — a thin wrapper over a plain array.
std::array<std::array<int, 4>, 3> my_array = {{
  {0, 1, 2, 3},
  {4, 5, 6, 7},
  {8, 9, 10, 11}
}};
```

#### "GOOD: single flat vector"

```cpp
// For runtime-determined sizes, use a 1D vector and compute offsets manually.
std::vector<int> my_array(3 * 4);
// Access element [i][j]:
my_array[i * 4 + j] = value;
```


```{warning}
`std::vector<std::vector<T>>` is a frequent source of cache misses in scientific code. Each inner `vector` holds a pointer to an independent heap allocation. A 1000×1000 `vector<vector<double>>` touches 1000 separate memory regions when iterating row by row.
```


---

## Row-Major vs Column-Major Ordering

### C/C++ Row-Major Layout

In C and C++, multi-dimensional arrays are stored in *row-major* order: all elements of row 0 are stored before row 1, all elements of row 1 before row 2, and so on. For `double A[M][N]`:

```
A[0][0]  A[0][1]  A[0][2]  ...  A[0][N-1]  A[1][0]  A[1][1]  ...
```

The rightmost index (`j` in `A[i][j]`) varies fastest. The fastest (most cache-friendly) loop order is:

```cpp
for (int i = 0; i < M; ++i) {
  for (int j = 0; j < N; ++j) {
    A[i][j] = ...;   // j varies in inner loop -> stride-1 access
  }
}
```

Swapping the loops so `i` varies in the inner loop gives stride-N access: every step jumps N doubles (8N bytes) in memory, skipping over cache lines that were just loaded and will never be reused from cache.

### Fortran Column-Major Layout

Fortran stores arrays in *column-major* order: the first index varies fastest. For a Fortran array `A(M, N)`:

```
A(1,1)  A(2,1)  A(3,1)  ...  A(M,1)  A(1,2)  ...
```

The fastest loop order in Fortran is the transpose of what it is in C:

```fortran
do j = 1, N
  do i = 1, M
    A(i, j) = ...   ! i varies in inner loop -> stride-1 access in Fortran
  end do
end do
```

### The Interoperability Pitfall

When calling a Fortran library from C (or vice versa), passing a C 2D array directly without transposing means the library's "row" is your "column." Every access the library makes to its fast index (column in Fortran) hits your slow index (row in C). If the matrix is not square, dimensions will also be swapped.

Common cases:

- LAPACK routines called from C expect column-major storage. Using C row-major arrays produces incorrect results unless you either transpose or pass the transpose flags if the routine supports them.
- BLAS `gemm` has `transa`/`transb` flags precisely to handle this: pass `CblasTrans` when providing a C row-major matrix where column-major is expected.


```{tip}
If you are calling [LAPACK](https://www.netlib.org/lapack/) from C, use the [C LAPACKE](https://www.netlib.org/lapack/lapacke.html) interface (part of the reference LAPACK distribution), which handles the row/column-major translation for you.
```


### Verifying Your Loop Order

Do not guess — measure. Tools like LIKWID (`likwid-perfctr`) expose hardware performance counters for L2 and L3 cache misses and memory bandwidth. A well-ordered loop should achieve bandwidth close to the STREAM benchmark peak for your machine. A poorly ordered loop will show cache-miss rates approaching 100% and bandwidth far below peak.

```bash
# Install LIKWID, then wrap your binary:
likwid-perfctr -C 0 -g MEM_DP ./my_benchmark
```

The `MEM_DP` group reports memory bandwidth and double-precision FLOP rate. If your achieved bandwidth is 10–20% of peak, your access pattern is the bottleneck.

---

## References

- [BLAS](https://www.netlib.org/blas/) — Basic Linear Algebra Subprograms (Netlib reference).
- [LAPACK](https://www.netlib.org/lapack/) — Linear Algebra PACKage.
- [LAPACKE](https://www.netlib.org/lapack/lapacke.html) — the C interface to LAPACK.
- Ulrich Drepper, [*What Every Programmer Should Know About Memory*](https://www.akkadia.org/drepper/cpumemory.pdf) (PDF) — the canonical deep dive on caches, DRAM, and memory-hierarchy effects.
