# Overview

Lazygit is an terminal-base user interface (TUI) written in Go that provides a keyboard-driven, intuitive interface for interacting with Git repositories. Instead of typing long commands, you can perform these actions with single keypresses.

The interface is divided into panels—such as

- Files
- Commits
- Branches
- Stash
- Status
- Command Log: A command log shows the Git commands executed behind the scenes, making it a great learning tool as well.

Here you can see how, all these panels are arranged in the interface:

![Lazygit](./images/lazygit.png)

## How to Leverage Lazygit's Power

To make the most of Lazygit, here's how you can integrate it into your workflow and harness its capabilities:

1. **Install and Set Up**

```cmd
brew install lazygit
```

1. **Launch Lazygit**: Open it in a Git repository by typing `lazygit` in your terminal.

2. **Navigation**: There are two ways to navigate in Lazygit.

   - Use arrow keys or Vim-style bindings (h, j, k, l) to move between panels and items.
   - Switch panels with number keys (1 for Status, 2 for Files, etc.) or Tab.

3. **Essential Operations**:

   a. **Files Panel Operations**:
   - `Space` to stage/unstage entire file
   - `a` to stage all changes
   - `d` to view inline diff
   - `/` to filter files
   - `Enter` to open file in editor
   - `Ctrl+o` to open file in default program
   - `M` to open external merge tool

   b. **Staging and Committing**:
   - `c` to commit (opens commit message editor)
   - `C` to commit using git editor
   - `A` to amend last commit
   - `m` to commit with message without opening editor
   - `Space` on specific lines to stage them

   c. **Review and Diff**:
   - `Enter` on a file to see diff
   - `]` and `[` to navigate between changed chunks
   - `Tab` to switch to staging view
   - `Ctrl+s` to stash selected lines
   - `Shift+s` to stash all changes

   d. **Branch Operations**:
   - `n` to create new branch
   - `c` to checkout branch
   - `b` to view branch options
   - `Space` to checkout by name
   - `F` to force checkout
   - `d` to delete branch
   - `m` to merge into current branch
   - `r` to rebase onto selected branch

   e. **Remote Operations**:
   - `p` to pull
   - `P` to push
   - `f` to fetch
   - `g` for custom remote options
   - `u` to set upstream branch

   f. **Commit History**:
   - `e` for interactive rebase
   - `s` to squash down
   - `f` to fixup
   - `r` to reword commit
   - `d` to drop commit
   - `v` to paste commit (cherry-pick)
   - `A` to amend commit
   - `Ctrl+z` to undo last action

   g. **Stashing Operations**:
   - `s` to stash all changes
   - `S` to stash staged changes
   - `a` to apply selected stash
   - `g` to pop selected stash
   - `d` to drop selected stash
   - `w` to open stash options menu

   h. **Search and Filter**:
   - `/` to start search in any panel
   - `Ctrl+s` to search commits
   - `t` to filter by files
   - `Esc` to clear filter

   i. **Advanced Features**:
   - `m` to open external merge tool
   - `i` to add to .gitignore
   - `Shift+r` to refresh
   - `x` to open menu for current panel
   - `?` to toggle keybindings popup

4. **Customization**:
   Edit `~/.config/lazygit/config.yml` to customize:
   - Keybindings
   - Theme
   - Behavior

To see these operations in action, try them in a test repository first. The visual feedback makes it easy to understand what's happening with each command.

Integrate with tools like pre-commit hooks, which Lazygit supports, to enforce code quality.
