# Slurm Tips & Tricks
Here are a few advanced Slurm usage tricks to the experienced user
 
 ---

## Slurm Job Arrays
Slurm job arrays allow you to submit multiple, similar jobs at once without creating separate scripts for each. Each job in the array is called a _task_ and gets its own **array ID**. This is particularly useful for parameter sweeps, batch simulations, or processing multiple files in parallel.

### Basic Syntax
```bash
sbatch --array=0-9 myscript.sh
```
- `--array=0-9` creates 10 tasks with IDs from 0 to 9.
	- you can also pass a comma-separated list of ids if you wish
- Each task runs `myscript.sh` independently.
- Slurm sets the environment variable `$SLURM_ARRAY_TASK_ID` to the task’s ID.

### Accessing Task ID in Script

Inside `myscript.sh`, you can use the array ID to differentiate tasks. For example:

```bash
#!/bin/bash 
#SBATCH --job-name=array_example 
#SBATCH --output=output_%A_%a.txt 
#SBATCH --error=error_%A_%a.txt 
#SBATCH --time=00:10:00 

# $SLURM_ARRAY_TASK_ID is the task ID 
echo "Running task $SLURM_ARRAY_TASK_ID"  
# Example: process different input files INPUT_FILE="input_$SLURM_ARRAY_TASK_ID.txt" cat $INPUT_FILE`
```

- `%A` → master job ID
- `%a` → array task ID

This ensures each task writes to a separate output file.

### Submitting a Job Array

```bash
sbatch --array=0-99 myscript.sh
```

- Creates 100 tasks (IDs 0–99).
- Slurm can limit concurrent tasks using `%`:

```bash
sbatch --array=0-99%10 myscript.sh
```

- Only 10 tasks run simultaneously; the rest wait in the queue.

## Dumping a Run-script
One of Slurm's best features is accounting. A really handy feature is the ability to dump previous jobs' run-scripts.

First, run `sacct -X` to get the job ID; you may need to add `-S YEAR-MM-DD` to include older jobs. 

Then, dump the run-script.
```bash
sacct --batch-script --jobs <jobid>
```

This will print your subscript exactly as it was submitted to the scheduler, very helpful for when a particular run did well but you don't remember which parameters it used.
