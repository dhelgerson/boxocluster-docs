# Git Basics

```{rubric} Learning Objectives
:heading-level: 3
```

- Initialize and clone Git repositories for version control
- Stage, commit, and push changes with meaningful messages
- Configure `.gitignore` to exclude build artifacts and secrets
- Understand the three-stage workflow: working directory → staging → repository
- Pull from and push to remotes while avoiding conflicts
- Recover from mistakes using `git reset` with appropriate modes

---

Git is a distributed version control system that tracks changes to files over time. Unlike centralized systems, every developer has a complete copy of the repository history, enabling offline work and redundancy.

**Why use Git?**
- Track every change with timestamps and author information
- Revert to any previous state instantly
- Collaborate without overwriting each other's work
- Experiment safely in branches without affecting the main codebase

This guide covers essential operations with the reasoning behind each step.

## Initial Setup

Configure your identity once per system. Git embeds this information in every commit, creating an immutable audit trail of who made each change.

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Creating a Repository

### Local Repository

Initialize a repository when you want to start version-controlling a project. The `-b main` flag creates the default branch named "main" instead of the legacy "master".

```bash
# Navigate to your project directory first
cd my-project

# Create the hidden .git directory that stores all version history
# This directory contains commits, branches, tags, and configuration
# It's hidden (starts with .) to keep it out of your way
git init -b main
```

The `git init` command creates a `.git/` subdirectory containing:
- Object database (all commits, trees, blobs)
- References (branch heads, tags)
- Configuration and hooks
- Working tree metadata

### Clone Existing Repository

Cloning downloads a complete repository history from a remote server, not just the current files.

```bash
git clone <repository-url>
cd <repository-name>
```

## Adding Files

Git refers to versioning files as "tracking" them.
Git uses a three-stage workflow: working directory → staging area (index) → repository.
The staging area lets you craft commits by selecting exactly which changes to include.

```bash
# Stage specific files for the next commit
# Only changes to these files will be included
git add file1.c file2.h

# Add all files in current directory
git add .

# Add all tracked files with changes
git add -u
```

**Why stage incrementally?** Creating focused commits (one logical change per commit) makes history easier to navigate and revert if needed.

## Ignoring Files

Create a `.gitignore` file to prevent unnecessary files from being tracked. Git will never track ignored files unless explicitly forced.

```bash
# Example .gitignore
.env
```

**Why ignore `.env`?** Contains secrets (API keys, passwords) that should never be versioned or shared.

```bash
*.o
*.pyc
__pycache__/
build/
*.log
```

Patterns apply recursively to all subdirectories. A file matching `*.log` in any subdirectory is ignored.

**Common ignore patterns:**
- Build artifacts (`*.o`, `build/`) - regenerateable, bloat repo
- Dependencies (`node_modules/`, `venv/`) - install from manifest
- Secrets (`.env`, `*.pem`) - security risk if committed
- Editor files (`.vscode/`, `*.swp`) - local configuration

## Checking Status

The `git status` command shows the state of the working directory and staging area.

Shows:
- **Changes not staged for commit**: Modified files Git will NOT include in next commit (you must `git add` them)
- **Changes to be committed**: Staged files Git WILL include in next commit
- **Untracked files**: New files Git doesn't know about yet (not in `.gitignore`)

```bash
git status
```

## Committing Changes

A commit is a snapshot of your staged changes, with metadata (author, timestamp, message).

```bash
# Interactive commit (opens editor)
git commit

# Commit with message
git commit -m "Description of changes"

# Commit all modified tracked files (skips unstaged files)
git commit -am "Description of changes"

# View diff while committing
git commit -v -m "Description"
```

```{tip}
To configure your default commit message editor:
```bash
git config --global core.editor vim
# Or for VS Code:
git config --global core.editor "code --wait"
```
```

**Why commit messages matter:** Good messages explain *why* a change was made, not just *what*. Future you (or collaborators) will thank you when debugging months later.

**Commit message structure:**
- First line: imperative, ≤50 chars (e.g., "fix: add bounds check to loop")
- Blank line
- Body: explain motivation, context, trade-offs (wrap at 72 chars)

## Removing Files

When deleting files, Git needs to know if you want to:
1. Delete from both filesystem and version history
2. Stop tracking but keep the file locally

```bash
# Remove file from both filesystem and git history
# This deletion will be committed and propagated to remotes
git rm <file>

# Remove from git only (keep file)
# Useful when you want to stop tracking but keep locally
git rm --cached <file>

# Remove directory
git rm -r <directory>
```

## Working with Remotes

Remotes are named references to repository copies on other machines (usually a server like GitLab, GitHub, or a shared filesystem).

**Why use remotes?**
- Backup: Remote copy survives local disk failure
- Collaboration: Team members share changes via remote
- Distribution: Deploy code to build/test servers

### Add Remote

Associate a local repository with a remote server. The name `origin` is conventional for the primary remote.

```bash
git remote add origin <repository-url>
```

View existing remotes:

```bash
git remote -v
```

### Pull Changes

Retrieve changes from a remote repository and merge them into your current branch.

**Why pull before working?** Ensures you're building on top of the latest code, avoiding conflicts later.

**How pull works:** `git pull` = `git fetch` (download) + `git merge` (integrate)

```bash
# Download remote changes and merge into current branch
git pull

# Pull with fast-forward only (safer)
# Fails if merge would create a merge commit
git pull --ff
```

### Push Changes

Upload your local commits to a remote repository.

**Why push?** Share your work with teammates or deploy to a CI/CD pipeline.

**How push works:** Git compares local and remote histories, then transfers missing commits.

```bash
# Upload local commits to the configured remote branch
git push

# Push to specific branch
git push origin main
```

```{note}
If the remote has changes your local repo doesn't have, you must `git pull` before `git push`.
```

**Why pull first?** Prevents lost work. If you push without syncing, Git rejects the push to protect remote history. Resolve conflicts locally before sharing.

## Common Workflows

### Daily Development

Standard workflow for contributing to a shared repository.

```bash
# Begin by syncing with remote to get teammates' changes
# This minimizes merge conflicts later
git pull

# Make your changes in the working directory
# Edit files, add features, fix bugs...

# Stage all modified files for commit
git add .

# Create a commit with a descriptive message
git commit -m "Feature X implemented"

# End of day: push changes
git push
```

### Fixing a Mistake

Git provides safety nets for common errors. Choose the reset mode based on what you want to preserve.

```bash
# Undo last commit but preserve changes in working directory
# Changes remain staged, ready to recommit with correction
git reset --soft HEAD~1

# Undo last commit and discard all changes
# WARNING: This permanently deletes uncommitted work
git reset --hard HEAD~1

# Remove a file from staging area only
# File remains modified in working directory
git reset <file>
```

**Understanding reset modes:**
- `--soft`: Move branch pointer only (changes stay staged)
- `--mixed` (default): Move pointer, unstaging changes (changes stay in working directory)
- `--hard`: Move pointer, discard all changes (DANGEROUS)

### Viewing History

Inspect the commit log to understand project evolution or find when a bug was introduced.

```bash
# Show commit log
git log

# Compact one-line view
git log --oneline

# Show changes in last commit
git show
```

**Log formatting tips:**
- `git log --oneline --graph --all`: Visual branch structure
- `git log -p`: Show diffs with each commit
- `git log --author="name"`: Filter by contributor
- `git log --since="2 weeks ago"`: Time-based filtering

## Best Practices

1. **Commit often**: Small, focused commits are easier to review, revert, and cherry-pick
2. **Write clear messages**: Explain *why* the change exists; code shows *what*
3. **Pull before push**: Always sync with remote first to minimize conflicts
4. **Review before committing**: Run `git status` and `git diff --staged` to verify changes
5. **Use `.gitignore`**: Exclude build artifacts, dependencies, and secrets to keep repos clean
6. **Use branches**: Feature branches isolate work and enable safe experimentation
7. **Fetch regularly**: `git fetch` updates remote refs without merging, letting you review before integrating

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Pro Git Book](https://git-scm.com/book/en/v2) (free online)
- [Git Tower Learning Resources](https://www.git-tower.com/learn/)
