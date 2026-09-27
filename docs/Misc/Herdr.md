# Herdr

Herdr is an terminal multiplexer natively design to work for AI Native world. It like Tmux but for AI Agents.

## Terminologies

### Session

A session is a container for a group of related workspaces. It is a logical grouping of workspaces.
A session is a persistent Herdr server namespace. The default herdr command attaches to the default session.

Most of time you don't need to create session explicitly. Use named sessions when you need completely separate panes, sockets, and persisted runtime state.

Common commands:

```bash
 herdr session list
 herdr session attach work
 herdr session attach side-project
```

### Workspace

A workspace is a collection of panes running within a session. When a session has no workspaces, Herdr opens one automatically. A workspace is a project-level container for tabs, panes, and agents. Give each active project its own workspace to keep agent state readable in the sidebar

### Panes

A pane is a container for a single thread. It is a single terminal window that can be split into multiple panes.

### Threads

## Usage

### Run an Agent

Start your coding agent with command like Claude, Codex or others. Herdr detects it automatically. Across every workspace, the sidebar shows whether each agent is working, blocked, done, or idle, so you always know which project needs you.

### Keyboard shortcuts

Like Tmux use "Ctrl+b" as prefix then action keys.

| Action                  | Key              |
| ----------------------- | ---------------- |
| Split right             | prefix+v         |
| Split down              | prefix+minus     |
| New tab                 | prefix+c         |
| Next / previous tab     | prefix+n / prefix+p |
| Workspace navigation    | prefix+w         |
| New workspace           | prefix+shift+n   |
| Detach client           | prefix+q         |
| Moving between panes    | prefix+h/j/k/l   |
| Close pane              | prefix+x         |
| Resize pane             | prefix+ctrl+arrow |
| Find / replace          | prefix+f / prefix+r |
| Search in workspace     | prefix+s         |
| Toggle search sidebar   | prefix+q         |
| Move files              | prefix+m         |
| Run command             | prefix+m         |
| Kill agent              | prefix+k         |
| Kill workspace          | prefix+shift+k   |

- Press prefix+? inside Herdr to see every active binding.

- Press prefix+q or simply close your terminal window. The Herdr server and every agent keep running.
