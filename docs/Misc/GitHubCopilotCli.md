# GitHub Copilot CLI

The **GitHub Copilot CLI** provides a conversational AI agent in your terminal. It helps with explaining commands, generating scripts, debugging errors, and managing your system.

> [!NOTE]
> This guide covers the standalone CLI (`@github/copilot`). The `gh` extension (`gh copilot`) now acts as a wrapper for this tool. The old explicit `suggest` and `explain` subcommands have been replaced by a unified conversational interface.

## 1. Prerequisites

- **Node.js**: Version 18 or higher.
- **npm**: Installed (usually comes with Node.js).
- **Subscription**: Active GitHub Copilot subscription.

![GitHub Copilot Cli](./images/copilotcli.png)

## 2. Installation

Install the CLI globally using npm:

```bash
npm install -g @github/copilot
```

Alternatively, if you use the GitHub CLI (`gh`), it can download and run the Copilot CLI for you:

```bash
gh copilot
```

Verify the installation:

```bash
copilot --version
```

## 3. Authentication

Before using the tool, you must authenticate with your GitHub account:

```bash
copilot auth
```

## 4. Basic Usage

The CLI operates primarily in two modes: **Interactive** (Chat) and **One-Shot** (Prompt).

### 🧠 Interactive Mode (Recommended)

Start a continuous chat session where the agent maintains context:

```bash
copilot
```

Or start with an initial prompt:

```bash
copilot -i "Help me fix the bug in main.js"
```

Inside the session, you can use natural language to:

- Ask about shell commands ("How do I find files larger than 100MB?")
- Debug Git issues ("Undo the last commit but keep changes")
- Write code ("Create a Python script to parse CSV")

### 💬 Interactive Session Commands

Once you are in the conversation mode (`copilot`), you have access to a suite of slash commands to manage the session and environment.

| Command | Description |
| :--- | :--- |
| **/mcp** | **Manage MCP Servers**: List, add, or disable Model Context Protocol servers. |
| **/add-dir** | **File Access**: Add a directory to the allowed list for the current session. |
| **/delegate** | **Agent-to-Agent**: Delegate a task to an autonomous agent that can open PRs. |
| **/model** | **Switch Models**: Change the AI model on the fly (e.g. `/model gpt-5`). |
| **/share** | **Export Session**: Save the conversation to a file or Gist. |
| **/clear** | **Reset Context**: Clear the conversation history to start fresh. |
| **/cwd** | **Navigation**: Change or view the current working directory. |
| **/list-dirs**| **View Permissions**: See all directories the agent currently has access to. |
| **/login** | **Authentication**: Log in to GitHub Copilot. |
| **/usage** | **Stats**: Display token usage and session statistics. |
| **/theme** | **Appearance**: Toggle between `light`, `dark`, or `auto` themes. |

> [!TIP]
> **Keyboard Shortcuts**:
>
> - **Ctrl+C**: Interrupt the current generation.
> - **Ctrl+D**: Exit the session.
> - **Up/Down Arrow**: Navigate command history.

### 6. Common Scenarios

#### 🔍 Scenario 1: Debugging a Local Issue

1. Start Copilot: `copilot`
2. **User**: "My build is failing with a segfault in `src/main.c`."
3. **Copilot**: "I need to see the file."
4. **User**: `/add-dir ./src` (Grant access)
5. **Copilot**: Reads file, analyzes error, and suggests a fix.

#### 🤖 Scenario 2: Connecting a Database Tool via MCP

You can give Copilot access to your database schema using MCP.

1. Start Copilot: `copilot`
2. **User**: `/mcp add sqlite-server uvx mcp-server-sqlite --db-path ./my.db`
3. **User**: "Query the `users` table and tell me the most recent signups."
4. **Copilot**: Uses the `sqlite-server` tool to run a SQL query and presents the data.

### ⚡ One-Shot Mode

Execute a single prompt and exit. Useful for quick answers or scripting.

```bash
copilot -p "Explain chmod 777"
```

To run without asking for confirmation for every tool (useful for automation), use:

```bash
copilot -p "List all PDF files" --allow-all-tools
```

## 5. Advanced Capabilities

### 🗂 File & Directory Access

By default, Copilot may ask for permission to access files. You can explicitly allow access:

```bash
# Allow access to specific project folder
copilot --add-dir ~/my-project

# Allow access to ANY path (use with caution)
copilot --allow-all-paths
```

### 🛠 Tool Management

You can control which "tools" (capabilities) the agent can use:

```bash
# Allow git commands but deny push
copilot --allow-tool 'shell(git:*)' --deny-tool 'shell(git push)'

# Allow all file writing operations
copilot --allow-tool 'write'
```

### 🤖 Model Selection

Copilot CLI supports various AI models. You can select a specific model to optimize for speed or capability:

```bash
# Use GPT-5 (Example)
copilot --model gpt-5

# Use Claude 3.5 Sonnet
copilot --model claude-sonnet-4.5
```

Running `copilot --help` will list all currently available models.

### 🔄 Session Management

You can resume previous conversations:

```bash
# Resume the most recent session
copilot --continue

# Pick a session to resume
copilot --resume
```

### 🔌 Model Context Protocol (MCP)

The CLI supports the Model Context Protocol (MCP), allowing you to connect external tools and data sources.

**Configuration:**
You can configure MCP servers in `~/.copilot/mcp-config.json` or pass them via flags:

```bash
copilot --additional-mcp-config ./my-mcp-config.json
```

**Control:**

- `--disable-builtin-mcps`: Disable default tools.
- `--disable-mcp-server <name>`: Disable a specific server.
- `--enable-all-github-mcp-tools`: Enable extended GitHub tools.

## 6. Updates

To update to the latest version:

```bash
npm install -g @github/copilot
```

## 7. Troubleshooting & Logs

If you encounter issues, you can inspect the logs:

- Default Log Directory: `~/.copilot/logs/`
- Set Log Level: `copilot --log-level debug`

To view all help topics including configuration details:

```bash
copilot help
copilot help config
copilot help permissions
```
