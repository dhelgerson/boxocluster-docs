# Memory Debugging

```{rubric} Learning Objectives
:heading-level: 3
```

- Use `memcheck` to find memory leaks, invalid reads/writes, and uninitialized values
- Use `helgrind` to detect data races in multithreaded code
- Use `cachegrind` to simulate cache behavior and find cache misses
- Use `callgrind` to find hotspots by instruction count
- Interpret Valgrind output and fix the underlying bugs

---

## Why Valgrind?

Valgrind runs your program on a synthetic CPU — slow, but it sees everything. It's invaluable for:

- **Memory bugs**: leaks, buffer overruns, use-after-free
- **Threading bugs**: data races, deadlocks
- **Performance**: cache misses, hotspots

Valgrind has enough depth to warrant its own topic.

---

## Memcheck — Memory Errors

The most commonly used tool:

```text
valgrind --tool=memcheck --leak-check=full ./program
```

### Common Errors

**Invalid read/write**:

```
Invalid read of size 8
   at 0x4E56789: your_function (your_file.c:42)
  Address 0x52043d0 is 0 bytes after a block of size 80
    alloc'd at 0x4C34567: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    by 0x4E56123: your_function (your_file.c:40)
```

**Memory leak**:

```
definitely lost: 80 bytes in 1 blocks
  at 0x4C34567: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
  by 0x4E56123: your_function (your_file.c:40)
```

**Uninitialized value**:

```
Conditional jump or move depends on uninitialised value(s)
   at 0x4E56789: your_function (your_file.c:45)
```

### Fixing Memory Bugs

```c
// BUG: buffer overrun
char *buf = malloc(10);
strcpy(buf, "This string is too long!");  // writes past end

// FIX: allocate enough or use strncpy
char *buf = malloc(20);
strncpy(buf, "This string is too long!", 19);
buf[19] = '\0';
```

---

## Helgrind — Data Races

Detects threading bugs in POSIX threads and OpenMP:

```text
valgrind --tool=helgrind ./program
```

### Example: Data Race

```
Thread 2:
  Write by thread 2 at 0x52043d0
    at 0x4E56789: counter++ (races.c:15)
  Previous write by thread 1 at 0x52043d0
    at 0x4E56789: counter++ (races.c:15)
```

### Fixing Data Races

```c
// BUG: data race on shared counter
int counter = 0;
#pragma omp parallel for
for (int i = 0; i < 1000; i++) {
  counter++;  // race!
}

// FIX: use reduction
#pragma omp parallel for reduction(+:counter)
for (int i = 0; i < 1000; i++) {
  counter++;
}
```

---

## Cachegrind — Cache Simulation

Simulates cache behavior (no hardware counters needed):

```text
valgrind --tool=cachegrind ./program
cachegrind_annotate cg.out
```

### Output Example

```
Ir         I1         L2i        IL1i       L2d        IL1d       L1d
1000000    1000       500        200        5000       2000       1000
```

- `Ir`: Instructions retired
- `I1`, `L2i`, `IL1i`: L1 instruction cache, L2 instruction cache, etc.
- `L2d`, `IL1d`, `L1d`: L2 data cache, L1 data cache, etc.

High miss rates indicate cache-unfriendly access patterns.

---

## Callgrind — Hotspot Profiling

Finds hotspots by instruction count:

```text
valgrind --tool=callgrind ./program
callgrind_annotate callgrind.out.1
```

### Output Example

```text
events: Ir
450000  (45.0%)  your_function (your_file.c:42)
300000  (30.0%)  another_function (another_file.c:15)
```

The top functions are your hotspots — optimize these first.

---

## Running on ARC Clusters


```{warning}
Valgrind is slow (10–50× overhead). Do **not** run it on compute nodes or with large data.
```


Use login nodes or workstations:

```text
# On login node (check policy first)
valgrind --tool=memcheck ./program

# Or on a workstation
ssh workstation
valgrind --tool=helgrind ./parallel_program
```

---

## References

- [Valgrind Quick Start](https://valgrind.org/docs/manual/quick-start.html)
- [Valgrind Manual](https://valgrind.org/docs/manual/manual.html)
