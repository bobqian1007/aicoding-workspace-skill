# AI Coding Workspace Contract

Use this contract when creating or updating a domain workspace.

## Canonical layout

```text
<workspace>/
├── AGENTS.md
├── CLAUDE.md                 # optional, points to AGENTS.md
├── knowledge/
│   ├── index.md
│   ├── business/index.md
│   ├── product/index.md
│   └── technology/index.md
├── .agents/
│   └── skills/
│       └── .gitkeep            # keeps an initially empty skill root
├── openspec/                    # created and managed by OpenSpec
├── repositories/
│   └── index.md
└── runtime/
    └── .gitkeep
```

The workspace root is a Git control repository. `knowledge/`, `.agents/skills/`, `openspec/`, `repositories/index.md`, and root agent rules are durable and reviewable. Child checkouts and worktrees may live under `repositories/`, but the control repository must ignore their contents. `runtime/` is disposable and must not become a second knowledge base.

## Knowledge boundaries

### Business

Business vocabulary, actors, policies, workflows, ownership, metrics, compliance constraints, and upstream/downstream responsibilities.

### Product

User journeys, capabilities, product rules, feature behavior, UI/API expectations, edge cases, and known limitations.

### Technology

Architecture, service boundaries, data flows, APIs, schemas, dependencies, environments, deployment, observability, and incident knowledge.

When a document spans dimensions, place it where a future reader is most likely to look first and cross-link it from the other relevant indexes.

## Required lookup protocol

Root agent rules must teach agents to:

1. Read `knowledge/index.md` to understand available knowledge and freshness.
2. Choose one or more dimensions and read their `index.md` files before opening many documents.
3. Search narrowly with repository-local tools such as `rg -n "<term>" knowledge/<dimension>`.
4. Read the matching source documents rather than answering from an index summary alone.
5. Cite workspace-relative source paths in the answer.
6. Distinguish documented facts, code-derived inference, and unknowns. Never manufacture missing domain knowledge.
7. Update an index whenever durable knowledge is added, moved, or retired.

For technical questions, inspect both `knowledge/technology/` and the relevant code repository. If they disagree, identify the discrepancy and treat executable code or current runtime evidence as stronger evidence unless the user specifies otherwise.

## Repository inventory

`repositories/index.md` is the sole stable source of truth for the repository inventory. It records:

- Service or repository name.
- Responsibility in the domain.
- Workspace-relative primary-checkout path.
- Source URL or local source checkout used as the worktree origin.
- Default branch and, when relevant, a pinned base commit.
- Integration mode: clone, worktree, existing checkout, or inventory only.
- Current status and unresolved details.

`AGENTS.md` must link agents to `repositories/index.md` and state when to read and update it, but must not repeat the inventory table or individual repository facts. Change-specific branch and worktree mappings belong in the OpenSpec change design or a linked change document, not in either stable file.

Avoid copying repositories into `runtime/`. A git worktree belongs under `repositories/<service-name>/` and remains governed by its source repository's worktree metadata.

The control repository tracks `repositories/index.md`, not nested child repository contents. Each system change first creates a control-repository worktree. OpenSpec review and technical design happen there before any affected child-repository worktrees are created. Read [multi-repo-change-contract.md](multi-repo-change-contract.md) for the required gates and change mapping.

## Skill discovery contract

Separate the portable skill package from the runtime-specific discovery root:

```text
<skill-root>/
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/       # optional
    ├── references/    # optional
    └── assets/        # optional
```

The portable contract is one skill per directory with a required `SKILL.md`. Its frontmatter `name` and `description` are discovery and routing metadata. A top-level `index.md` is not part of discovery and should not be generated.

The discovery root belongs to the host runtime:

- Codex repository scope: `.agents/skills/`. Codex scans this directory from the current working directory toward the repository root.
- A host exposing a skill loader or configurable capability directories should register `.agents/skills/`, or adapt/symlink that root while preserving each skill package unchanged.
- `AGENTS.md` may require or explain when to use a skill, but it must not duplicate the skill catalog or replace native discovery.

Typical skills may include SDD, log investigation, test-case generation, release checks, incident triage, and environment operations, but create only the skills the user actually needs. Each implemented skill should state its trigger, inputs, procedure, safety boundaries, outputs, and verification in its own `SKILL.md`.

OpenSpec is the default SDD provider. Its generated `openspec-*` skill directories share `.agents/skills/` with workspace-authored skills. OpenSpec owns only its generated directories and marker; workspace-specific skills must use distinct names. See [sdd-contract.md](sdd-contract.md) for provider lifecycle and extension rules.

## Agent rule ownership

`AGENTS.md` is the canonical cross-agent rule file. Keep domain facts concise there and link to the knowledge base for detail. If Claude compatibility is required, use a thin `CLAUDE.md` containing `@AGENTS.md` plus a short explanation; do not maintain parallel copies.

Do not silently replace pre-existing rule systems. If a workspace already uses `.cursor/rules`, `.github/copilot-instructions.md`, or another agent configuration, preserve it and add a small bridge to the canonical contract only with the user's approval.
