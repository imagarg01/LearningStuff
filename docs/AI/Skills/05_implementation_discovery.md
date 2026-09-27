# Implementation, Structure, & Discovery

While architectural guidelines dictate *how* a skill should behave, this section covers *where* skills live, how they are structured, and how they are shared across the enterprise to prevent duplication.

## Anatomy of a Skill Directory

A skill is not a single file, but a directory containing instructions and execution logic. 

**Directory Structure:**
```text
.agents/skills/
└── my-enterprise-skill/
    ├── SKILL.md       # The cognitive interface (instructions & metadata)
    ├── scripts/       # The execution runtime
    └── examples/      # Examples of usage
```

### YAML Frontmatter & Progressive Disclosure

Every skill's cognitive interface (`SKILL.md`) should contain YAML frontmatter at the top:
```yaml
---
name: my-enterprise-skill
description: Used to query enterprise user data and order history.
---
```
**Progressive Disclosure:** Modern AI platforms do not load the entire skill into the AI's context window by default. They only load the `name` and `description` to save context space. The full execution logic and instructions are only injected on-demand when the AI decides to activate the tool.

---

## Discovery & Sharing Mechanisms

To prevent hundreds of developers from copy-pasting skills into their local environments, enterprise orchestration layers should provide native discovery mechanisms.

### 1. The Workspace Root (Version Control)
The agent runtime should automatically traverse the directory tree to find a designated configuration folder (e.g., `.agents/` or `.skills/`) at the root of the project/repository.
* **How it works:** Place project-specific skills in `<repo_root>/.agents/skills/`.
* **Benefit:** When developers clone or pull the repository, the orchestration layer automatically discovers and loads the skills contextually for that project. Zero manual setup is required.

### 2. Plugins for Reusability Across Projects
For enterprise-wide skills that aren't tied to a specific project (e.g., standard internal deployment workflows or internal tooling integrations), package them as **Plugins** or Modules.
* **How it works:** A plugin bundles skills, rules, and connection configurations together under a standardized structure (e.g., `plugins/<name>/`).
* **Benefit:** You can maintain a central "Enterprise AI Plugins" repository. Developers pull this repository once and configure their global configuration to reference these centralized paths.

### 3. Explicit Registration (Configuration Files)
For skills located in non-standard network drives, shared volumes, or submodules, developers can use a centralized configuration file (like a `skills.json` or `config.yaml`) in their workspace or global config to explicitly point the AI runtime to the shared network path.

### 4. Dynamic Centralized Registry (Just-In-Time Fetching)
Instead of relying on local configuration files or git repositories, the orchestration layer can integrate with a centralized enterprise registry (e.g., an internal API, Skill Hub, or Vector Database).
* **How it works:** When a developer's agent encounters an intent it cannot solve with local skills, it queries the central registry using semantic search. If a relevant enterprise skill is found, the agent dynamically fetches the skill's cognitive interface (`SKILL.md`) and runtime logic over the network, caching it locally for execution.
* **Benefit:** Ensures absolute centralization, version control, and governance. Developers do not need to pull or configure anything manually; the agent autonomously discovers and downloads the required capability Just-In-Time (JIT) based on the current task's need.
