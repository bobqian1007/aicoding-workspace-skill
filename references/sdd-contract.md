# SDD Provider Contract

The workspace uses a provider-neutral lifecycle with OpenSpec as the default implementation. This keeps the development policy stable while allowing another SDD component to be added later without changing the knowledge, repository, runtime, or Agent Skill contracts.

## Provider lifecycle

An SDD provider adapter must define these operations:

1. **Detect** — determine whether its CLI or runtime is available and report its version.
2. **Install** — state prerequisites and the exact install command; obtain approval before global or external changes.
3. **Initialize** — initialize the workspace root and generate integrations for the selected agent tools.
4. **Discover** — expose the generated workflows through the host's native skill or command discovery mechanism.
5. **Update** — refresh provider-managed integrations without deleting specifications or change history.
6. **Verify** — prove that configuration, durable artifacts, and agent integrations exist.

Only one provider is the workspace default. Additional providers may coexist only when the user explicitly requests them and their generated paths do not collide. `AGENTS.md` must name the active default and explain how an agent discovers its workflows.

In a multi-repository workspace, the provider runs from a dedicated worktree of the workspace control repository. Requirements, impact analysis, and technical design must identify the affected child repositories before their development branches or worktrees are created. The SDD change remains the coordination record across all child implementations.

## OpenSpec adapter

### Detect

```bash
openspec --version
```

An existing installation wins. Do not silently change how it is installed or upgrade it.

### Install

When OpenSpec is missing, verify `node --version` and `npm --version`. The current npm package requires Node.js 22.12.0 or newer. After user approval, run exactly:

```bash
npm install -g @fission-ai/openspec@latest
```

Verify with `openspec --version`. Do not use `sudo`, install Node, change a version manager, or edit shell startup files on the user's behalf.

### Initialize

For the default Codex workspace:

```bash
openspec init <workspace> --tools codex
```

Add explicitly requested tools to the comma-separated `--tools` value. OpenSpec supports re-running init, but it may reconcile or remove legacy generated integrations; inspect an existing workspace first and disclose affected files.

### Discover

For Codex, OpenSpec generates `.agents/skills/openspec-*/SKILL.md`. Agents discover these through the normal repository skill mechanism. The core profile typically provides explore, propose, apply, update, sync, and archive workflows. Use the actual generated skill names rather than maintaining a parallel catalog.

### Update

```bash
openspec update
```

Run this from the initialized workspace to refresh provider-managed Agent Skills. Do not manually edit generated `openspec-*` skill directories because an update replaces them.

### Verify

Verify all of the following:

- `openspec --version` succeeds.
- `openspec/config.yaml` exists.
- At least one `.agents/skills/openspec-*/SKILL.md` exists for Codex.
- `AGENTS.md` identifies OpenSpec as the default SDD provider.
- `openspec/specs/` and `openspec/changes/`, when present, are not ignored as disposable artifacts.

Report the exact init output and the generated skill names. A missing command file is not a failure for Codex because Codex uses skills directly.

## Alternate provider adapters

Add a separate reference for each new provider and map its behavior to the same six lifecycle operations. Do not modify the portable Agent Skill package contract or reuse OpenSpec-owned `openspec-*` paths. Changing the default provider requires an explicit user decision and a corresponding update to `AGENTS.md`.
