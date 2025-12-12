# Fuzzy Finder (fzf)

**fzf** is a general-purpose command-line fuzzy finder. It is an interactive Unix filter for command-line usage that can be used with any list; files, command history, processes, hostnames, bookmarks, git commits, etc.

## Core Concept: The Filter Pipeline

Think of **fzf** as a filter that sits between a source of data and a destination.

`Input List -> [ fzf (Selection) ] -> Output (Selected Item)`

1. **Input**: A list of text (files, history, etc.) is piped into fzf.
2. **Filter**: You type to fuzzily match items.
3. **Output**: You press Enter, and the selected item is printed to stdout (or passed to the next command).

## Search Syntax

fzf allows you to refine your search with special characters. You can enter multiple terms separated by spaces; fzf will show items matching **all** terms.

| Token | Match Type | Description |
| :--- | :--- | :--- |
| `sbtrkt` | Fuzzy-match | Items that match `sbtrkt` fuzzily |
| `'wild` | Exact-match (quoted) | Items that include `wild` |
| `^music` | Prefix-exact-match | Items that start with `music` |
| `.mp3$` | Suffix-exact-match | Items that end with `.mp3` |
| `!fire` | Inverse-exact-match | Items that do not include `fire` |
| `!^music` | Inverse-prefix-exact-match | Items that do not start with `music` |

## Key Bindings

Common formatting shortcuts during the search:

- **CTRL-J / CTRL-K** (or Down/Up): Move cursor up and down.
- **Enter**: Select item.
- **TAB / SHIFT-TAB**: Mark multiple items (if `--multi` is enabled).
- **CTRL-C / ESC**: Abort.

## Basic Usage

### Finding Files

The simplest usage is running `fzf` without arguments. It will list files in the current directory.

```bash
fzf
```

### Piping Data

You can feed any list into fzf.

```bash
# Select a process to kill
ps -ef | fzf

# Select a git branch
git branch | fzf
```

## Advanced Workflows

### 1. Opening Files

Combine fzf with your editor to open the selected file immediately.

```bash
vim $(fzf)
```

*Note: This works by taking the output of fzf (the filename) and passing it as an argument to vim.*

### 2. Command History Search

Standard fzf installation provides a key binding (often **CTRL-R**) to search your shell history.

1. Press `CTRL-R`.
2. Type part of a previous command.
3. Press Enter to place it on the command line.

### 3. Git Operations

Checkout a branch easily by fuzzy searching all branches.

```bash
git checkout $(git branch | fzf)
```
