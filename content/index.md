# Box O' Cluster
## Introduction

<span class="small">Last Update 3 February 2026</span>

Welcome to Boxocluster, an tool for instructors and students to explore the world of distributed computing with a hands-on guided experience through the process of building, configuring, and managing a virtual cluster computer. While the hardware may differ from the systems found on the [Top500](https://top500.org), the fundamentals remain the same. By mastering the principles underlying cluster computing, students will be equipped with valuable skills applicable to both small-scale projects and large-scale infrastructures. These resources can be used as a jumping-off point to demonstrate additional concepts of cluster computing as you see fit.

In this digital era, the demand for scalable and efficient computing solutions continues to rise. Understanding how to harness the power of cluster computing is becoming increasingly essential across various fields, from data science and artificial intelligence to scientific research and beyond.

Users should see [Getting Started](getting-started.md) next or jump to any topic on the left.

Once a functioning cluster is achieved, users may choose to continue learning about parallel programming. First, start with [Theory](parallel-programming/theory.md).

```{toctree}
:maxdepth: 1
:hidden:

about
getting-started
```

```{toctree}
:maxdepth: 1
:numbered: 1
:caption: Modules
:hidden:
:glob:

modules/nfs
modules/ww
modules/chrony
modules/slurm
modules/supporting-software
modules/hello-world
modules/accounting
```

```{toctree}
:maxdepth: 2
:caption: Parallel Programming
:hidden:

parallel-programming/theory.md
parallel-programming/hardware.md
parallel-programming/git-basics.md
parallel-programming/autovec.md
parallel-programming/openmp.md
parallel-programming/stdpar.md
parallel-programming/mpi.md
parallel-programming/profiling.md
parallel-programming/valgrind.md
```

<!--
```{toctree}
:maxdepth: 1

adv/index
```
-->

<!-- TODO: not rn 
<!-- - [Module 11 - Parallel Storage (Optional)](module-11) -->
<!-- - Module 14 - Challenges                        also john -->
