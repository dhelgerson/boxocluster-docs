# Using Git
Git is a diff-based versioning tool. it has become the gold standard of versioning in open-source projects. the CLI tool git itself is an entire rabbit hole. I'm going to walk you through creating a local repo, adding to it, committing to it, adding a remote, and pushing to that remote. these are the basic operations you'll use on a daily basis while versioning projects.

---

## Initial Setup
Let's say we want to version a directory on a POSIX machine that contains the following files:
- `main.c`
- `main.h`
- `makefile`

---

## Creating a Local Git Repo
Creating the repo is simple:
1. navigate to the directory
2. run `git init -b main`
This will create a new local repository

---

## Adding files
Git refers to the act of versioning files as 'tracking' them. To add files to be tracked, issue the following command:
```bash
git add file1 file2 etc
```

Directories can also be added this way to track all of their contents. For example, to add everything in the current directory:
```bash
git add .
```

---

## Ignoring Unwanted Files
It's very common to want git to ignore files from the repository that may exist on the filesystem. Build artifacts, dependency installations, pycaches are all common examples. To do this, simple create a file called `.gitignore` anywhere in the repo containing the names of files you'd like to ignore; globs may be used. The file will apply to all child directories

Here's an example `.gitignore`:
```bash
.env
*.o
__pycache__
```

---

## Removing Files from Cache
when you run `git add`, you're *'staging'* files for commit. Sometimes it's necessary to *'unstage'* files for commit. Say you ran `git add .` but you have a file 'main.o' you don't want to commit. Just run:
```bash
git rm --cached main.o
```

---

## Checking Tree Status
In order to check the status of your tree: what's changed, what's staged, etc. you can run the following command:
```bash
git status
```

---

## Committing staged files
The backbone of git is the commit. a commit represents the state of a project at any given time. the literal commit consists of a comment, and a diff.

In order to create a commit, ensure your desired changes are staged and run:
```bash
git commit
```

This will open an editor for you to write your commit message.
````{note}
By default, git will use nano to edit the commit. You can change this by running 
```bash
git config --global core.editor vim
``` 
to use vim or whatever you like. If you'd like to use vscode, ensure to use 'code --wait' since by default code will fork instead of blocking
````

You can also skip this step by running:
```bash
git commit -m "my message"
```

Furthermore, if you'd like to commit any changes to existing files on the tree, run:
```bash
git commit -a
```

If you'd like to see the entire diff when editing your commit, run:
```bash
git commit -v
```

---

## Adding a Remote
Versioning your own code is great, but one of the main draws of git is how good it is at allowing others to collaborate on projects. To do this, we need a remote git repository that's reachable by all. 

First, you need to create a remote repository. this can be accomplished by visiting sites like [github.com](https://github.com) or by running your own repo with ssh or gitea. Once you have a remote repo setup, copy it's URI to use in the following command:
```bash
git remote add origin [REMOTE_URI]
```

---

## Pulling from a remote
After adding a remote, it's a good idea to pull from it to ensure that your local repo is in sync with remote. Any time you need to make sure your local repo is in sync with your remote, run:
```bash
git pull
```

Sometimes, such as when somebody else has edited the codebase, there can be mismatches between the remote and local repo. This will cause a pull to fail. the safest option is to use the "fast-forward method to merge the changes"
```bash
git pull --ff
```

---

## Pushing to a remote
After you're committed changes locally, you'll need to *'push'* them to your remote in order for it to contain those changes. This does not have to be done for every commit; all local commits will be pushed in one exchange. to push local changes, run:
```bash
git push
```

```{note}
Attempting to push to a remote that has changes your local repo does not will fail.
The easiest solution is to `git pull` before `git push`ing
```