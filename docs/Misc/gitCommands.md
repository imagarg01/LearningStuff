# **git Basics**

## Logging

```cmd
git log
```

This will show all the commits in the current branch. It will show the commit hash, author, date, and commit message.

```cmd
git log -n 5
```

This will show the last 5 commits in the current branch.

```cmd
git log branch1..branch2
```

This will show the commits that are in branch1 but not in branch2.

```cmd
git log branch1 ^branch2
```

This will show the commits that are in branch1 but not in branch2.

```cmd
git log --since="2 weeks ago"
```
This will show the commits that are newer than 2 weeks ago.

```cmd
git log --until="2 weeks ago"
```
This will show the commits that are older than 2 weeks ago.

```cmd
git whatchanged --since="2 weeks ago"
```
This will show changes by files made in the last 2 weeks.

```cmd
git log -p filename.js
```
This will show the diff of the file.

```cmd
git log --stat -p
```
It will show the diff of the file and the number of lines added and removed.

```cmd
git log --pretty=format:"%h %ad | %s%d [%an]" --date=short
```
This will show the commit hash, author, date, and commit message.

```cmd
git log --oneline --decorate --graph
```
It will show the commits in a single line, with the branches and the graph.



## Use "--force-with-lease"

## Signing commits with ssh

## git maintenance

## Switch and Restore

## git checkout -p file.txt

## hooks

### Commit Stuff

- pre-commit
- prepare-commit-msg
- commit-msg
- post-commit

### Merging Stuff

- post-merge
- pre-merge-commit

### Rewriting Stuff

- pre-rebase
- post-rewrite

### Switching/Pushing Stuff

- post-checkout
- reference-transaction
- pre-push

#### Hooks Examples

- commit message formatting
- package install
- update ctags
- submodule status
- tabs or spaces
- linting
- large files
- test passes
- rebasing merger commit prevention

#### Valuable Hooks

- pre-commit
- husky

## Attributes

## Fixup commits

## git rebase --update-refs

## scalar

## Worktrees

**Note:** 
1- Good zsh alias are available by default. Read more [here](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git)
2- There is a website which will help you learn about different git commands. Here is the [link](https://explainshell.com/)

