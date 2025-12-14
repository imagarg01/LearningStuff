# GitHub Copilot CLI

The **GitHub Copilot CLI** allows you to use GitHub Copilot directly in your terminal.

> [!IMPORTANT]
> This guide covers the **new** standalone CLI (`@github/copilot`). The explicit `suggest` and `explain` subcommands from the old extension are **removed**. Usage is primarily interactive.

## 1. Prerequisites

- **Node.js**: Version 18 or higher.
- **npm**: Installed (usually comes with Node.js).
- **Subscription**: Active GitHub Copilot subscription.

## 2. Installation

Install the CLI globally using npm:

```bash
npm install -g @github/copilot
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

## 4. Usage

The `copilot` command is a single entry point for an interactive AI agent.

### 🧠 Interactive Mode (Recommended)

Run `copilot` without arguments to start a chat session. This is the most reliable way to use the tool.

```bash
copilot
```

Once inside the session, you can type your requests in plain English:

- "How do I revert the last git commit?"
- "Explain what 'chmod 777' does"
- "Write a python script to parse a json file"

The AI will respond with modifications, explanations, or code, and you can continue the conversation to refine user requests.

### ⚡ One-Shot Commands (Experimental)

*Note: Direct argument support varies by version. If `copilot "query"` does not work for you, use the interactive mode above.*

Some versions may support the `--prompt` flag or similar mechanisms for single commands, but the interactive session is the primary design.

## 5. Updates

To update to the latest version:

```bash
npm install -g @github/copilot
```
