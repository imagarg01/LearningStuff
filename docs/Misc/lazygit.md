# Overview

Lazygit is a **terminal-based** user interface (TUI) written in Go that provides a keyboard-driven, intuitive interface for interacting with Git repositories. Instead of typing long commands, you can perform massive operations with single keypresses.

The interface is divided into panels:

- **1. Status**: Repo state (Repo name, branch, etc).
- **2. Files**: Staged/Unstaged changes.
- **3. Branches**: Local/Remote branches.
- **4. Commits**: Commit history (and Reflog).
- **5. Stash**: Stashed changes.

![Lazygit](./images/lazygit.png)

## How to Leverage Lazygit's Power

1. **Install and Set Up**

   ```bash
   brew install lazygit
   # or
   go install github.com/jesseduffield/lazygit@latest
   ```

2. **Launch**: Type `lazygit` in any mapped git directory.

3. **Navigation**:
   - **H/J/K/L** (Vim keys) or **Arrows**: Move selection.
   - **[/]** or **Numbers (1-5)**: Switch Panels.

4. **Essential Operations**:

   - `Space`: Stage/Unstage file
   - `d`: **Discard changes** (Use with caution!)
   - `c`: Commit changes
   - `Enter`: View diff (Stage individual lines)
   - `a`: Stage all
   - `D`: View reset options

   b. **Staging and Committing**:
   - `c`: Commit (opens editor)
   - `C`: Commit using git editor
   - `A`: Amend last commit
   - `Space`: Stage selected line/hunk (in diff view)

   c. **Review and Diff**:
   - `Enter`: Focus main panel (diff view)
   - `[` / `]`: Navigate hunks
   - `Tab`: Switch to Staging Area (left/right)

   d. **Branch Operations**:
   - `n`: New branch
   - `Space`: Checkout branch
   - `d`: Delete branch
   - `r`: Rebase onto...
   - `M`: Merge into current branch

   e. **Remote Operations**:
   - `p`: Pull
   - `P`: Push
   - `f`: Fetch

5. **Killer Features (Why use Lazygit?)**

   **A. The "Oh shoot, I forgot to add this file to the last commit" Fix**
   - Go to Files -> Stage the file -> Press `A` (Amend). Done.

   **B. Interactive Rebase (Time Travel)**
   - Go to **Commits** panel.
   - Press `Enter` on a commit to view its files.
   - **Move Commits**: Press `J` (down) or `K` (up) to reorder commits instantly.
   - **Squash/Fixup**: Press `f` on a commit to "fixup" (merge) it into the one below it.
   - **Edit History**: Press `e` on an old commit to edit it, then continue.

   **C. Cherry Picking**
   - Go to **Commits** (or even another branch's commits).
   - Press `c` (Copy) on the commits you want.
   - Go to your branch -> Press `v` (Paste).

6. **Resolving Merge Conflicts (The Life Saver)**

   Merge conflicts are where Lazygit truly shines. Instead of seeing `<<<<HEAD` markers in a text editor, Lazygit gives you a UI.

   **Workflow**:
   1. When a conflict happens, Lazygit opens the **Files** panel with a "Conflicted" status.
   2. Press `Enter` on the conflicted file.
   3. You will see the **Conflicts Panel**.
   4. **Resolve**:
      - `←` / `→`: Pick "Ours" (Current) or "Theirs" (Incoming).
      - `b`: Pick **Both**.
      - `Space`: Toggle selection.
   5. Once all hunks are resolved, press `Esc`.
   6. Lazygit asks to continue the rebase/merge automatically.

   **Why it's better**: You never accidentally delete a closing brace `}` while deleting conflict markers.

7. **Customization**:
   Edit `~/.config/lazygit/config.yml` (open with `o` in Status panel) to customize keybindings and themes.
