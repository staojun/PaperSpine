# PaperSpine

PaperSpine 是一个面向 Codex 和 Claude Code 的论文、报告写作 Skill Suite。

它的核心目标不是“让 AI 直接润色几句话”，而是让 AI 在写作前先理解目标场景、学习优秀样例、确认全文动机，再逐段规划和生成，并把每一处为什么这样写记录下来。

## 仓库结构

```text
PaperSpine/
  dist/
    codex/
      paper-spine/              # Codex 单 skill 发行版
    claude/
      skills/                   # Claude Code 扁平 skill suite
        paper-spine/
        paper-spine-intake/
        paper-spine-research/
        paper-spine-rewrite/
        paper-spine-build/
        paper-spine-latex/
        paper-spine-audit/
      commands/                 # Claude Code slash command
        paperspine.md
        paperspine-ui.md
  src/
    scripts/                    # 共享脚本
    references/                 # 共享流程参考
    agents/                     # 共享 agent 元数据
  .claude-plugin/               # Claude Code 插件元数据
  install.ps1                   # Windows 推荐安装脚本
  README.md
  README.zh-CN.md
```

`dist/` 是真正给用户安装的内容。`src/` 是开发用的共享脚本和参考资料。

## 快速安装

Windows PowerShell：

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git
cd PaperSpine
.\install.ps1 -Target all
```

也可以只安装某一端：

```powershell
.\install.ps1 -Target codex
.\install.ps1 -Target claude
.\install.ps1 -Target all -CleanLegacy
```

`-CleanLegacy` 会清理常见的旧安装目录，例如嵌套的 `PaperSpine`、`PaperSpineV2`、旧的 `paper-spine-*` 副本，避免 Codex 或 Claude Code 出现重复发现、找不到 skill 的问题。

安装到 Codex 后：**Restart Codex**，然后使用 `$paper-spine` 或在 skill 列表里选择 `paper-spine`。

安装到 Claude Code 后：重启或 reload Claude Code，然后使用：

```text
/paperspine
```

## 手动安装

Codex 需要一个自包含的单 skill：

```text
dist/codex/paper-spine
```

复制到：

```text
~/.codex/skills/paper-spine
```

最终结构应类似：

```text
~/.codex/skills/paper-spine/SKILL.md
~/.codex/skills/paper-spine/references/
~/.codex/skills/paper-spine/scripts/
```

Claude Code 需要扁平 skill 目录和可选 slash command：

```text
dist/claude/skills/*
dist/claude/commands/*.md
```

复制到：

```text
~/.claude/skills/
~/.claude/commands/
```

最终结构应包含：

```text
~/.claude/skills/paper-spine/SKILL.md
~/.claude/skills/paper-spine-intake/SKILL.md
~/.claude/skills/paper-spine-research/SKILL.md
~/.claude/commands/paperspine.md
```

## Claude Code 插件安装

也可以使用 Claude Code 插件方式安装：

```text
/plugin marketplace add https://github.com/WUBING2023/PaperSpine
/plugin install paper-spine
/reload-plugins
```

`.claude-plugin` 中的插件配置指向 `dist/claude/skills`，不是 Codex 的单 skill 目录。

## Codex 和 Claude Code 的差异

| 宿主 | 安装单元 | 常用入口 | 原因 |
| --- | --- | --- | --- |
| Codex | `dist/codex/paper-spine` | `$paper-spine` | Codex 使用单个自包含 skill 更稳定，避免重复发现。 |
| Claude Code | `dist/claude/skills/*` 和 `dist/claude/commands/*` | `/paperspine` | Claude Code 按扁平目录发现 skill，并支持 slash command。 |

不要把整个仓库直接复制到 `skills` 目录。这是出现重复 skill 或完全找不到 skill 的主要原因。

## 工作流

PaperSpine 有两条平级主流程：

1. **Rewrite Existing**：改进已有论文或报告，不把任务降级成简单润色。
2. **Build From Materials**：从素材文件夹构筑论文或报告，素材可以包括说明文档、图片、PDF、实验结果、调研材料、初步草稿等。

支持四类目标场景：

- `journal`：期刊论文
- `conference`：会议论文
- `report/review`：课程报告、技术报告、综述
- `competition`：竞赛论文或竞赛报告

研究深度：

- `flash`：3 篇目标任务样例、3 篇同领域近期/高质量论文、官方要求。
- `pro`：6 篇目标任务样例、6 篇同领域近期/高质量论文、官方要求。

输出语言：

- `English`
- `Chinese`

当选择英文输出时，可以额外生成 `translation_package`，把中间产物和最终 Markdown 产物翻译成中文，方便用户理解和复盘。

## 配置 UI

Claude Code 中推荐使用：

```text
/paperspine
```

这个命令会尽量自动启动 PaperSpine intake UI。若宿主终端不支持交互界面，则使用 Python wizard 兜底：

```powershell
python src/scripts/intake_wizard.py
```

配置完成后会生成：

```text
paper_rewriting_output/paper_spine_config.json
paper_rewriting_output/paper_spine_config.md
```

本地预览 TUI：

```powershell
python src/scripts/tui_preview_server.py --port 8765
```

## 关键产物

一次完整运行不应该只有最终论文，而应该留下完整的写作依据：

```text
paper_rewriting_output/
  paper_spine_config.json
  paper_spine_config.md
  downloaded_references/
  research_dossier.md
  motivation_candidates.md
  confirmed_motivation.md
  source_inventory.md
  evidence_bank.md
  figure_asset_map.md
  claim_register.md
  section_blueprint.md
  writing_rationale_matrix.md
  rewrite_matrix.md
  revision_audit.md
  final_paper/
    main.tex
    references.bib
    figures/
    paper.docx              # 可选 Word 版本
    paper.pdf               # 如果本机有 LaTeX 编译器则生成
  translation_package/       # 英文输出时可选
```

其中最重要的是 `writing_rationale_matrix.md`。它需要按论文或报告的真实结构逐段记录：这一小块承担什么功能，如何服务确认后的 motivation，参考了哪些 SOTA 或目标场景样例，使用了哪些证据或引用，最终文本应该通过什么检查。

## 检查命令

检查产物是否完整：

```powershell
python src/scripts/artifact_check.py paper_rewriting_output --markdown --write
```

复制到 skill 内部后，也可能以这种形式出现：

```powershell
python scripts/artifact_check.py paper_rewriting_output --markdown --write
```

检查 LaTeX：

```powershell
python src/scripts/latex_guard.py paper_rewriting_output/final_paper/main.tex --markdown
```

检查 Word：

```powershell
python src/scripts/word_guard.py paper_rewriting_output/final_paper/paper.docx --markdown
```

运行项目测试：

```powershell
python -m unittest discover -s tests
```

## PaperSpine 试图避免的问题

- 只改句子，不改论文逻辑。
- 把期刊、会议、课程报告、综述、比赛论文都按同一种风格写。
- 没确认动机就开始写。
- 添加没有证据支持的 claim。
- 只输出 `main.tex`，但不解释为什么这样设计文章。
- 用户要求翻译包时，只翻译一部分中间产物。

## License

MIT License. See [LICENSE](LICENSE).
