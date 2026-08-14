# OpenMP

```{rubric} Learning Objectives
:heading-level: 3
```

- Describe the OpenMP fork-join execution model
- Add `#pragma omp parallel` and `#pragma omp parallel for` to a serial loop
- Control thread count and query thread ID at runtime
- Time a parallel region and compute speedup
- Recognize data race conditions and use the `reduction` clause to avoid them

---

## OpenMP Basics

[**OpenMP**](https://www.openmp.org/specifications/) is a directive-based API for shared-memory parallelism. It requires no changes to data structures. You annotate loops and parallel regions with `#pragma` directives, link with `-fopenmp`, and the compiler generates multithreaded code. The same source file compiles correctly without `-fopenmp` and runs serially.

### The Fork-Join Model

OpenMP programs follow a **fork-join** execution model:

1. The program begins as a single *master thread*.
2. When execution reaches a `#pragma omp parallel` block, the runtime **forks** a team of threads. All threads execute the block concurrently.
3. At the closing `}`, threads **join** and the master thread continues alone.

### Controlling Threads

| Mechanism | Effect |
|-----------|--------|
| `OMP_NUM_THREADS=N` (env var) | Set default team size before launching the program |
| `omp_set_num_threads(N)` | Set team size in code before entering a parallel region |
| `omp_get_num_threads()` | Query team size from inside a parallel region |
| `omp_get_thread_num()` | Query caller's zero-based rank (0 = master thread) |


```{warning}
Outside a `#pragma omp parallel` block, `omp_get_num_threads()` always returns 1 regardless of `OMP_NUM_THREADS`.
```


---

## Parallel Vector Addition

```c
#include <stdio.h>
#include <omp.h>

#define ARRAY_SIZE 8000000
static double a[ARRAY_SIZE], b[ARRAY_SIZE], c[ARRAY_SIZE];

void vector_add(double *c, double *a, double *b, int n)
{
#pragma omp parallel for
  for (int i = 0; i < n; i++){
    c[i] = a[i] + b[i];
  }
}

int main(int argc, char *argv[]){
  for (int i = 0; i < ARRAY_SIZE; i++) {
    a[i] = 1.0;
    b[i] = 2.0;
  }

  #pragma omp parallel
  if (omp_get_thread_num() == 0)
    printf("Running with %d thread(s)\n", omp_get_num_threads());

  vector_add(c, a, b, ARRAY_SIZE);
}
```

### Building and Running

```bash
# Compile with OpenMP
gcc -fopenmp -O3 vecadd.c -o vecadd

# Set thread count and run
export OMP_NUM_THREADS=8
./vecadd
```

---

## Reduction: Avoiding Data Races

When multiple threads update a shared variable, you get a **data race**. Use `reduction` to safely accumulate:

```c
double sum = 0.0;
#pragma omp parallel for reduction(+:sum)
for (int i = 0; i < n; i++) {
  sum += a[i];  // Each thread gets a private copy; combined at end
}
```

Reduction operators: `+`, `-`, `*`, `&`, `|`, `^`, `min`, `max`.

---

## Running on ARC Clusters

For OpenMP jobs on ARC clusters:

1. **Request CPU cores**:
   ```bash
   #SBATCH --cpus-per-task=8  # Number of OpenMP threads
   ```

2. **Set thread count**:
   ```bash
   export OMP_NUM_THREADS=8
   ```

3. **Submit**:
   ```bash
   sbatch run.slurm
   ```

See [Running Jobs](../running-jobs/index.md) for SLURM details.

---

## References

- [OpenMP Specification](https://www.openmp.org/specifications/)
- [OpenMP Tutorials](https://www.openmp.org/resources/tutorials/)
