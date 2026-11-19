---
name: aicoding-workspace-creator
description: Create or initialize a multi-repository AI coding workspace control repository for a business domain, including indexed business/product/technology knowledge, OpenSpec-backed SDD, staged control/child worktrees, discoverable Agent Skills, service repositories, runtime artifacts, and agent operating rules. Use when a user wants a unified domain workspace for cross-repository development or operational Q&A; do not use for an ordinary single-repository project scaffold.
---

# AI Coding Workspace Creator

Create a workspace that gives coding agents enough domain context to develop, operate, and answer day-to-day business questions without mixing durable knowledge with temporary artifacts.

## Establish the workspace contract

Before creating files, obtain these required facts from the user:

1. The domain name and a concrete introduction: purpose, users, business boundary, key concepts, and important upstream/downstream systems.
2. The workspace control repository: repository root, default branch, remote when any, worktree parent location, and branch naming convention. This repository owns shared knowledge, OpenSpec artifacts, repository inventory, and cross-repository change coordination.
3. The child repositories in the domain: repository/service name, purpose, primary checkout or source URL, default branch, and preferred integration method (`clone`, `worktree`, existing checkout, or inventory only).

Ask only for missing information. Do not create the workspace until the domain introduction and repository list are known. If the user cannot provide all repository details, record unknown fields explicitly and continue only after they confirm an inventory-only workspace is useful.

Also resolve the target directory. Infer Codex as an OpenSpec tool target when this skill runs in Codex. Ask about additional agent tools only when the user mentioned them or compatibility files such as `CLAUDE.md` would be useful.

Before writing, inspect the target for existing workspace files and user changes. Never overwrite an existing `AGENTS.md`, `CLAUDE.md`, knowledge index, repository, or runtime artifact without explicit approval. Prefer extending compatible content surgically.

The workspace target must be the root of its control repository. A new local workspace is not worktree-ready until it is a Git repository with a baseline commit. Obtain approval before `git init`, staging files, or creating that commit. If the user declines, create the files when otherwise authorized but report that cross-repository change worktrees cannot start yet.

## Create the base structure

Read [references/workspace-contract.md](references/workspace-contract.md) before creating or updating a workspace. Use the bundled generator for a new workspace when its defaults fit:

```bash
python3 scripts/create_workspace.py <target> \
  --domain-name "<domain>" \
  --domain-description "<description>" \
  --repository "<name>=<url-or-local-path>"
```

Repeat `--repository` for every service. Add `--claude` only when Claude compatibility is requested. The generator is intentionally non-destructive and stops if a managed output file already exists.

The generated workspace must contain:

- `knowledge/` with a top-level index and separate `business/`, `product/`, and `technology/` indexes.
- `.agents/skills/` as the repository-scoped capability root. Each implemented skill lives at `.agents/skills/<skill-name>/SKILL.md`; do not add a top-level skill index.
- `repositories/` with an inventory index and, when requested and authorized, the domain service checkouts or worktrees.
- `runtime/` for disposable generated artifacts.
- `openspec/` after SDD initialization, containing the OpenSpec configuration, specifications, and change history.
- A root `AGENTS.md` containing the domain description, workspace map, repository lookup rules, and knowledge lookup rules. It must link to `repositories/index.md` instead of copying the repository inventory.

Keep `AGENTS.md` canonical. If `CLAUDE.md` is needed, make it a thin compatibility file that imports or directs the agent to `AGENTS.md`; do not duplicate the rules.

Read [references/multi-repo-change-contract.md](references/multi-repo-change-contract.md) and ensure its control-repository-first workflow is represented in both `AGENTS.md` and `knowledge/technology/multi-repo-change-workflow.md`. Child repository directories must be ignored by the control repository while `repositories/index.md` remains tracked.

## Initialize the SDD provider

Read [references/sdd-contract.md](references/sdd-contract.md) before installing or initializing an SDD provider. OpenSpec is the default provider.

After the base workspace exists:

1. Run `openspec --version`. If it succeeds, preserve that installation method and continue; do not replace or upgrade it implicitly.
2. If `openspec` is unavailable, run `node --version` and `npm --version`. The npm package requires Node.js 22.12.0 or newer. If either prerequisite is missing or Node is too old, stop and report the prerequisite instead of installing Node or changing the user's version manager.
3. Show the user `npm install -g @fission-ai/openspec@latest` and obtain approval immediately before running it. This is a global software installation. Never add `sudo`, edit shell startup files, or retry with a different installation method without direction.
4. Run `openspec --version` after installation. If it is still unavailable, report the npm global prefix or PATH issue and stop; do not edit PATH automatically.
5. For a new Codex workspace, run `openspec init <target> --tools codex`. Include other explicitly requested targets as a comma-separated list, for example `--tools codex,claude`.

Before re-running `openspec init` in an existing workspace, inspect existing OpenSpec configuration, generated `openspec-*` skills, legacy command files, and OpenSpec marker blocks. Report any cleanup the command may perform and obtain confirmation when existing generated integration files could be removed or replaced. Never handcraft OpenSpec-generated skills as a substitute for a successful init.

Treat `.agents/skills/openspec-*` as provider-managed output: refresh it with `openspec update`, not manual edits. Treat `openspec/specs/` and `openspec/changes/` as durable project history that belongs in version control.

## Materialize repositories safely

Inventorying a repository does not authorize network cloning or git worktree creation. Perform those actions only when the user asked for them or approves them after seeing the plan.

- For a worktree, confirm the source checkout, target path under `repositories/`, and branch or commit before running `git worktree add`.
- For a clone, confirm the repository URL and target directory before running `git clone`.
- Do not replace a non-empty target directory or change the source repository's current branch.
- After materialization, update `repositories/index.md` so paths and status match reality. Update `AGENTS.md` only when workspace-wide repository policy or topology changes; never copy the inventory table into it.

Primary child-repository checkouts are analysis sources and worktree origins. Keep them on their agreed default branches unless the user explicitly requests otherwise. Do not implement a system change directly in a primary checkout.

## Preserve the change sequence

For future system changes, the generated rules must require this order:

1. Create a dedicated branch and worktree from the workspace control repository.
2. In that control worktree, use OpenSpec for requirement review, code analysis, impact analysis, and technical design.
3. Read child repositories from their primary checkouts during analysis; do not create child development branches or worktrees yet.
4. After the OpenSpec proposal and technical design identify the affected repositories and receive the required review, create a matching branch/worktree only for each affected child repository.
5. Record the mapping from the OpenSpec change and control branch to every child repository, base revision, branch, and worktree path before implementation.
6. Implement and verify in child worktrees. Keep the control worktree as the source of truth for cross-repository status and final archive decisions.

Never create speculative child worktrees for every repository. Never delete or prune a control or child worktree without explicit authorization and a clean-state check.

## Seed knowledge and skills

Knowledge indexes describe what belongs in each knowledge area and how to find it; they are not substitutes for source knowledge. Put durable facts in the appropriate knowledge folder and link every new document from that folder's `index.md`.

Put procedural capabilities in the configured skill root. For Codex repository discovery, use `.agents/skills/<skill-name>/SKILL.md`. Skill discovery comes from the runtime scanning `SKILL.md` metadata, not from an `index.md`; keep `name` and `description` precise. If another agent runtime uses a loader or registered capability directory, preserve the same per-skill package contract and adapt only the discovery root.

Do not invent domain facts. Mark gaps as `待补充` and list the person, system, or document that could resolve them when known.

## Verify completion

Verify that:

1. All required directories and knowledge indexes exist, and `.agents/skills/` is present without a synthetic index.
2. `AGENTS.md` reflects the user's actual domain and every named repository.
3. The knowledge lookup sequence starts at `knowledge/index.md`, routes through a dimension index, uses targeted search, and requires source-path citations plus explicit uncertainty.
4. Repository statuses match the filesystem; a listed worktree passes `git -C <path> status` and appears in `git worktree list` from its source repository.
5. `openspec --version` succeeds, `openspec/config.yaml` exists, and Codex workflow skills exist under `.agents/skills/openspec-*/SKILL.md`.
6. The target is the workspace control-repository root, has a baseline commit, and can create a control worktree without involving a child repository.
7. `repositories/index.md` is the only stable repository inventory; `AGENTS.md` links to it and contains no duplicate repository table. The inventory and `knowledge/technology/multi-repo-change-workflow.md` consistently support the control-first sequence and change-specific child mapping.
8. Every implemented skill is discoverable as `.agents/skills/<skill-name>/SKILL.md`; `runtime/` is treated as disposable and excluded from version control except for a keep file.

Report what was created, which repositories were materialized, and all unresolved knowledge or repository details.
