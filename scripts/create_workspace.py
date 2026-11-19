#!/usr/bin/env python3
"""Create a non-destructive AI coding workspace skeleton."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_repository(value: str) -> tuple[str, str]:
    name, separator, source = value.partition("=")
    name = name.strip()
    source = source.strip() if separator else ""
    if not name:
        raise argparse.ArgumentTypeError("repository must use NAME or NAME=SOURCE")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name) or name in {".", ".."}:
        raise argparse.ArgumentTypeError(
            "repository NAME must contain only letters, digits, dots, underscores, and hyphens"
        )
    return name, source


def table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def repository_rows(repositories: list[tuple[str, str]]) -> str:
    if not repositories:
        return "| 待补充 | 待补充 | `repositories/<name>/` | 待补充 | 待补充 | inventory only | 待补充 |"
    rows = []
    for name, source in repositories:
        source_cell = table_cell(source) if source else "待补充"
        rows.append(
            f"| {table_cell(name)} | 待补充 | `repositories/{table_cell(name)}/` | "
            f"{source_cell} | 待补充 | inventory only | 待接入 |"
        )
    return "\n".join(rows)


def build_files(
    domain_name: str,
    domain_description: str,
    repositories: list[tuple[str, str]],
    claude: bool,
) -> dict[str, str]:
    rows = repository_rows(repositories)
    files = {
        "AGENTS.md": f"""# {domain_name} AI Coding Workspace

## 领域说明

{domain_description}

### 领域边界与关键概念

- 业务边界：待补充
- 主要用户/角色：待补充
- 关键概念：待补充
- 上游系统：待补充
- 下游系统：待补充

## 工作空间结构

- `knowledge/`：业务、产品、技术知识；从 `knowledge/index.md` 开始检索。
- `.agents/skills/`：仓库级 Agent Skills；由运行时读取各技能的 `SKILL.md` 元数据进行发现。
- `openspec/`：默认 SDD Provider 的配置、规格与变更历史；由 `openspec init` 创建和维护。
- `repositories/`：领域服务代码与仓库清单。
- `runtime/`：可删除的临时产物，不存放长期知识或正式源码。

## 版本控制拓扑

- 当前 workspace 根目录是多仓系统的控制面主仓，负责知识、OpenSpec 变更和跨仓协调记录。
- 主仓默认分支：待补充
- 主仓远程地址：待补充
- 主仓 worktree 父目录：待补充（必须位于当前主仓检出目录之外）
- 主仓变更分支命名规则：待补充
- `repositories/` 下的子仓内容由各自 Git 仓库管理，主仓只跟踪 `repositories/index.md`。
- 子仓主检出用于只读分析并作为 worktree 来源；不得直接在主检出中实现系统变更。

## 仓库清单查询

- `repositories/index.md` 是稳定仓库清单的唯一事实源，包含子仓职责、主检出、来源、默认分支、接入方式和状态。
- 分析代码、判断影响面或创建 worktree 前，先读取该文件并核对实际文件系统。
- 仓库接入、路径、默认分支或状态变化时，只更新 `repositories/index.md`；不要在本文件复制仓库表格或逐仓事实。
- 某次变更的分支/worktree 映射属于 OpenSpec design 或关联变更文档，不写入稳定清单。

## 知识查询规则

回答领域问题或开始开发前：

1. 先读 `knowledge/index.md`，根据问题选择业务、产品或技术维度。
2. 再读对应维度的 `index.md`，缩小到相关文档；不要仅依据索引摘要作答。
3. 使用 `rg -n "<关键词>" knowledge/<维度>` 做定向搜索并阅读命中文档。
4. 技术问题还要检查相关代码仓库；文档与当前代码不一致时，明确指出差异。
5. 回答中引用工作区相对路径，并区分已记录事实、基于代码的推断和未知项。
6. 不得编造缺失知识；使用“待补充”标记，并说明建议的信息来源。
7. 新增、移动或废弃长期知识时，同步更新相应 `index.md`。

## SDD 开发工作流

- 默认 SDD Provider 是 OpenSpec。除非用户明确切换 Provider，功能开发、缺陷修复和有行为影响的重构都应使用 OpenSpec 工作流。
- 需求尚不明确时先使用 `$openspec-explore`；准备进入交付时使用 `$openspec-propose` 建立可审阅的 proposal、spec、design 和 tasks，再使用生成的 apply、sync、archive 等技能推进生命周期。
- 开始修改代码前，确认对应变更的范围、验收标准和任务已经在 `openspec/` 中记录；若用户明确要求跳过 SDD，说明影响并记录该决定。
- `.agents/skills/openspec-*` 是 OpenSpec 生成物，只能通过 `openspec init` 或 `openspec update` 刷新，不得手工修改。
- `openspec/specs/` 与 `openspec/changes/` 是长期工程记录，应纳入版本控制，不能放入 `runtime/` 或忽略。
- 引入其他 SDD Provider 时，必须在本文件记录其检测、安装、初始化、发现、更新和验证方式；不得静默替换 OpenSpec 或覆盖其生成路径。

## 多仓变更顺序

详细规则见 `knowledge/technology/multi-repo-change-workflow.md`。任何系统变更必须按以下顺序推进：

1. 从 workspace 控制面主仓的约定基线创建变更分支和独立 worktree。
2. 在该主仓 worktree 中先用 OpenSpec 完成需求评审、代码只读分析、影响面分析和技术方案。
3. 方案评审前不得为子仓创建开发分支或 worktree；分析阶段读取 `repositories/index.md` 中登记的子仓主检出。
4. 方案明确受影响子仓后，只为这些子仓创建对应的分支和 worktree。
5. 实现前在 OpenSpec design 或其关联文档中记录主变更与各子仓的基线提交、变更分支、worktree 路径、任务和状态映射。
6. 子仓实现、跨仓验证和集成状态统一回写主仓 worktree；新增受影响子仓必须先更新方案并重新通过同一门禁。

不得为所有子仓预创建投机性 worktree。清理任何主仓或子仓 worktree 前，必须获得明确授权并确认工作区干净。

## 工作规则

- 只把可复用、经过确认的信息写入 `knowledge/`。
- 过程日志、下载文件、生成报告和一次性脚本放入 `runtime/`。
- 优先使用当前 Agent 运行时提供的技能发现或加载能力；本工作区的规范技能根目录是 `.agents/skills/`。
- 新增技能时使用 `.agents/skills/<skill-name>/SKILL.md`；不要创建技能总索引或在本文件复制技能清单。
- 未经用户授权，不 clone 仓库、不创建 worktree、不修改外部仓库状态。
""",
        ".gitignore": """runtime/*
!runtime/.gitkeep
repositories/*
!repositories/index.md
""",
        "knowledge/index.md": f"""# {domain_name} 知识库索引

本知识库服务于 AI 辅助开发、运维和日常业务答疑。

## 顶层结构

- [业务知识](business/index.md)：术语、角色、流程、政策、指标与领域边界。
- [产品知识](product/index.md)：用户旅程、功能行为、产品规则与限制。
- [技术知识](technology/index.md)：架构、服务、接口、数据、部署与可观测性。

## 查询方式

先选择维度并阅读其索引，再用关键词定向搜索源文档。答案应引用实际文档路径，区分事实、推断和未知项。跨维度问题应分别检索相关索引。

## 完整性与新鲜度

- 维护人：待补充
- 最近审阅：待补充
- 已知缺口：领域边界、关键概念及各维度源文档待补充
""",
        "knowledge/business/index.md": """# 业务知识索引

## 收录范围

业务术语、参与角色、端到端流程、政策约束、指标口径、合规要求以及上下游职责。

## 文档

- 待补充：领域概览与术语表
- 待补充：核心业务流程

## 维护信息

- 负责人：待补充
- 最近审阅：待补充
""",
        "knowledge/product/index.md": """# 产品知识索引

## 收录范围

用户旅程、产品能力、功能规则、交互或 API 预期、边界情况和已知限制。

## 文档

- 待补充：产品能力地图
- 待补充：关键用户旅程与规则

## 维护信息

- 负责人：待补充
- 最近审阅：待补充
""",
        "knowledge/technology/index.md": """# 技术知识索引

## 收录范围

系统架构、服务边界、数据流、接口与数据模型、依赖、环境、发布、可观测性和故障经验。

## 文档

- 待补充：系统上下文与架构图
- 待补充：服务、接口和数据清单
- 待补充：部署、监控与故障处理
- [多仓变更与 Worktree 工作流](multi-repo-change-workflow.md)

## 维护信息

- 负责人：待补充
- 最近审阅：待补充
""",
        "knowledge/technology/multi-repo-change-workflow.md": """# 多仓变更与 Worktree 工作流

## 仓库角色

- **workspace 控制面主仓**：跟踪 `AGENTS.md`、`knowledge/`、`openspec/`、`.agents/skills/` 和 `repositories/index.md`，统一管理跨仓变更。
- **子仓主检出**：保持在约定默认分支，用于只读代码分析，并作为创建子仓 worktree 的来源。
- **变更 worktree**：隔离某个系统变更。主仓 worktree 负责协调，受影响子仓 worktree 负责代码实现。

## 强制顺序

### 1. 创建主仓 worktree

从 workspace 控制面主仓记录基线分支和提交，确认目标目录位于当前主检出之外且为空，然后创建独立的变更分支和 worktree。该 worktree 是本次变更的协调根目录。

### 2. OpenSpec 评审与方案

在主仓 worktree 中使用 OpenSpec 完成需求评审、验收标准、子仓代码只读分析、影响面、proposal、spec、design 和 tasks。此阶段只能读取 `repositories/index.md` 登记的子仓主检出，不创建子仓开发分支或 worktree。

### 3. 确认受影响子仓

技术方案必须列出需要修改的子仓及原因，并区分“仅分析”和“需要修改”的仓库。完成约定评审后，才允许进入子仓 worktree 阶段。

### 4. 创建必要的子仓 worktree

只为方案确认的受影响子仓创建分支和 worktree。每个子仓都要记录主检出、基线分支与提交、变更分支、worktree 路径、负责的 OpenSpec 任务和当前状态。

### 5. 实现与跨仓验证

代码只在子仓变更 worktree 中修改。若发现新的受影响子仓，先更新 OpenSpec 方案并重新通过门禁。验证应覆盖相关接口、数据或事件契约、发布顺序和各子仓测试。

### 6. 集成与收尾

在主仓 worktree 中记录各子仓提交或 Pull Request、验证证据和集成状态。满足验收条件后再归档 OpenSpec 变更。worktree 清理是独立的破坏性操作，必须获得明确授权并先确认工作区干净。

## 变更映射模板

将下表放入 OpenSpec design 或其关联变更文档，不要写入长期仓库清单：

| 子仓 | 变更职责 | 基线提交 | 变更分支 | Worktree 路径 | 状态 | 验证证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 待方案确认 | 待补充 | 待补充 | 待补充 | 待补充 | 未开始 | 待补充 |
""",
        ".agents/skills/.gitkeep": "",
        "repositories/index.md": f"""# 代码仓库索引

| 名称 | 职责 | 主检出路径 | 来源 | 默认分支 | 接入方式 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## 接入约定

- `inventory only` 表示只登记，目录中尚无代码。
- 子仓主检出应保持在约定默认分支，只用于代码分析和作为 worktree 来源，不直接承载系统变更实现。
- 系统变更先创建 workspace 主仓 worktree，并在其中完成 OpenSpec 评审和技术方案；方案确认前不得创建子仓开发分支或 worktree。
- 只为方案确认的受影响子仓创建 worktree。创建前必须确认来源、基线提交、目标路径和变更分支，并获得用户授权。
- 变更专属的子仓分支/worktree 映射写入 OpenSpec design 或关联文档，不写入本长期清单。
- 接入后同步更新本文件与根目录 `AGENTS.md`；状态必须反映实际文件系统。
""",
        "runtime/.gitkeep": "",
    }
    if claude:
        files["CLAUDE.md"] = """# Claude workspace instructions

@AGENTS.md

`AGENTS.md` is the canonical source for domain context and workspace rules.
"""
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="workspace directory to create or initialize")
    parser.add_argument("--domain-name", required=True, help="business domain name")
    parser.add_argument("--domain-description", required=True, help="concrete domain introduction")
    parser.add_argument(
        "--repository",
        action="append",
        default=[],
        type=parse_repository,
        metavar="NAME[=SOURCE]",
        help="repository inventory entry; repeat for each service",
    )
    parser.add_argument("--claude", action="store_true", help="add a thin CLAUDE.md bridge")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    domain_name = args.domain_name.strip()
    domain_description = args.domain_description.strip()
    if not domain_name or not domain_description:
        parser.error("domain name and description must not be blank")
    repository_names = [name for name, _ in args.repository]
    if len(repository_names) != len(set(repository_names)):
        parser.error("repository names must be unique")

    files = build_files(domain_name, domain_description, args.repository, args.claude)
    conflicts = [relative for relative in files if (target / relative).exists()]
    if conflicts:
        parser.error("refusing to overwrite existing managed files: " + ", ".join(conflicts))

    target.mkdir(parents=True, exist_ok=True)
    for relative, content in files.items():
        write_new(target / relative, content)

    print(f"Created AI coding workspace at {target}")
    print(f"Managed files: {len(files)}")
    print(f"Repositories inventoried: {len(args.repository)}")
    print("Control repository: Git root and baseline commit required before change worktrees")
    tools = "codex,claude" if args.claude else "codex"
    print("SDD provider: OpenSpec (initialization required)")
    print(f'Next: openspec init "{target}" --tools {tools}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
