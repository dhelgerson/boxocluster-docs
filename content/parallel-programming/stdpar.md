# C++17 stdpar

```{rubric} Learning Objectives
:heading-level: 3
```

- Explain the three C++17 execution policies: `seq`, `par`, `par_unseq`
- Use `std::transform` with a parallel execution policy for the Stream Triad
- Compile for GPU execution with NVIDIA's `nvc++` and `-stdpar=gpu`
- Compare `std::par` to explicit OpenMP and CUDA implementations

---

## Standard Parallel Algorithms

C++17 added [*execution policies*](https://en.cppreference.com/w/cpp/algorithm/execution_policy_tag_t) to most `<algorithm>` functions. The policy is passed as the first argument and tells the implementation how it may schedule work:

| Policy | Meaning |
|--------|---------|
| `std::execution::seq` | Sequential, in-order — identical to pre-C++17 algorithms |
| `std::execution::par` | Parallel, may execute on multiple threads; order unspecified |
| `std::execution::par_unseq` | Parallel **and** vectorized; may interleave within a thread (SIMD) |

These apply to algorithms: `std::transform`, `std::reduce`, `std::sort`, `std::for_each`, `std::fill`, and others.

```{note}
On CPU, `par` typically dispatches to Intel's libTBB or an OpenMP thread pool. With NVIDIA's `nvc++` compiler and `-stdpar=gpu`, the **same** `par` policy compiles to CUDA kernels with no source changes.
```

---

## Stream Triad with `std::transform`

```cpp
#include <algorithm>
#include <execution>
#include <vector>

void vector_operation(std::vector<double>& c,
                      const std::vector<double>& a,
                      const std::vector<double>& b,
                      double scalar) {
  std::transform(std::execution::par,
                 a.begin(), a.end(),
                 b.begin(),
                 c.begin(),
                 [scalar](double a_val, double b_val) {
                   return a_val + scalar * b_val;
                 });
}
```

Swapping `par` for `seq` or `par_unseq` changes the parallelism strategy. When compiled with `nvc++ -stdpar=gpu`, `par` becomes a GPU kernel automatically.

---

## Build Flags

`````{tab-set}

````{tab-item} CPU (OpenMP backend)

```bash
# GCC with OpenMP
g++ -std=c++17 -O3 -fopenmp triad.cc -o triad
```
````

````{tab-item} GPU (nvc++ / NVIDIA HPC SDK)

```bash
nvc++ -std=c++17 -stdpar=gpu -O3 triad.cc -o triad_gpu
```

`-stdpar=gpu` routes `std::execution::par` to CUDA. Memory management is handled transparently via CUDA Unified Memory.
````

````{tab-item} SLURM cluster

```bash
module load nvhpc
nvc++ -std=c++17 -stdpar=gpu -O3 triad.cc -o triad_gpu
sbatch run.slurm
```
````
`````

---

## Comparison to Other Approaches

| Approach | Code complexity | Portability | Typical overhead |
|----------|----------------|-------------|------------------|
| CUDA | High (explicit kernels) | NVIDIA only | Low |
| OpenMP | Medium (directives) | Multi-vendor | Low |
| `std::par` | Low (standard library) | Compiler-dependent | Varies |

---

## Running on ARC Clusters

For `std::par` GPU builds:

1. **Load NVIDIA HPC SDK**:
   ```bash
   module load nvhpc
   ```

2. **Request GPU**:
   ```bash
   #SBATCH --gres=gpu:1
   ```

3. **Compile and submit**:
   ```bash
   nvc++ -std=c++17 -stdpar=gpu triad.cc -o triad
   sbatch run.slurm
   ```

See [GPU Usage](../gpu-usage/index.md) for available modules and partitions.

---

## References

- [C++17 Execution Policies](https://en.cppreference.com/w/cpp/algorithm/execution_policy_tag_t)
- [NVIDIA HPC SDK Documentation](https://docs.nvidia.com/hpc-sdk/)
