# Multi-Repository Change Contract

The AI coding workspace is a control repository for a system composed of multiple child repositories. It is not merely a folder containing unrelated checkouts.

## Repository roles

### Workspace control repository

The control repository owns:

- `AGENTS.md` and cross-agent rules.
- `knowledge/` and its indexes.
- `openspec/` specifications and change history.
- `repositories/index.md` and cross-repository status.
- Workspace-authored Agent Skills and runtime policy.

Each system change starts with a branch and worktree of this repository. The control worktree is the coordination root for that change.

### Child repositories

Child repositories contain deployable services, libraries, infrastructure, or clients. Each has a primary checkout used as a read-only analysis source and as the source repository for `git worktree add`.

Do not implement changes in a primary checkout. Do not create child development worktrees until the reviewed technical design identifies that repository as affected.

## Change lifecycle

### 1. Create the control worktree

Resolve and record:

- Change identifier.
- Control repository base branch and exact base commit.
- Control change branch.
- Control worktree path, outside the current control checkout.

Inspect the branch and target path before `git worktree add`. Do not reuse a non-empty target or an existing branch without confirming intent.

### 2. Review and design with OpenSpec

Run the OpenSpec workflows from the control worktree. Requirements review, repository inspection, impact analysis, proposal, specifications, design, acceptance criteria, and tasks happen before child development worktrees are created.

During this phase, inspect child code through the primary checkout paths recorded in `repositories/index.md`. Treat those checkouts as read-only. Record uncertainties rather than creating branches merely to investigate.

### 3. Approve the affected-repository set

The technical design must name every affected child repository and explain why it changes. Repositories inspected but not changed should also be recorded when that distinction matters.

This approval is the gate for child branch and worktree creation.

### 4. Create affected child worktrees

For each approved child repository, resolve and record:

- Repository name and primary checkout.
- Default/base branch and exact base commit.
- Change branch.
- Worktree path under the control worktree's ignored `repositories/` area or another explicitly approved location.
- Responsibility and related OpenSpec tasks.

Use the repository's own naming convention. A shared change identifier should connect the control branch and child branches even when prefixes differ.

### 5. Implement and verify

Implement only inside the affected child worktrees. Keep the OpenSpec tasks and the cross-repository mapping current as scope changes. Adding a newly affected repository requires updating the design and passing the same gate before creating its worktree.

Cross-repository verification must cover interface compatibility, data or event contracts, rollout order, and repository-specific tests when relevant.

### 6. Integrate and close

Record child commit or pull-request references and integration status in the control worktree. Archive the OpenSpec change only when its required repository changes and cross-repository verification are complete, or explicitly document deferred work.

Worktree cleanup is a separate destructive operation. Require explicit authorization, verify each worktree is clean, and never delete branches as an implicit side effect.

## Required change mapping

Maintain a mapping in the OpenSpec change design or a linked change document with at least:

| Repository | Role in change | Base revision | Change branch | Worktree path | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |

The mapping is change-specific. `repositories/index.md` remains the stable inventory of primary checkouts, default branches, and repository responsibilities.
