# PaperSpine

PaperSpine is a motivation-driven paper and report writing skill suite for Codex and Claude Code.

It is designed for writing tasks where the target format matters: journal papers, conference papers, course or technical reports, reviews, and competition papers. The workflow asks the agent to learn the target scene and strong examples before writing, then records why each manuscript unit is planned or changed.

## Repository Layout

```text
PaperSpine/
  dist/
    codex/
      paper-spine/              # Codex single-skill distribution
    claude/
      skills/                   # Claude Code flat skill suite
        paper-spine/
        paper-spine-intake/
        paper-spine-research/
        paper-spine-rewrite/
        paper-spine-build/
        paper-spine-latex/
        paper-spine-audit/
      commands/                 # Claude Code slash-command helpers
        paperspine.md
        paperspine-ui.md
  src/
    scripts/                    # shared deterministic helpers
    references/                 # shared workflow references
    agents/                     # shared agent metadata source
  .claude-plugin/               # Claude Code plugin metadata
  install.ps1                   # recommended Windows installer
  README.md
  README.zh-CN.md
```

The `dist/` directory is the installable output. The `src/` directory keeps shared scripts and references readable for development.

## Quick Install

On Windows PowerShell:

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git
cd PaperSpine
.\install.ps1 -Target all
```

Use a narrower target when needed:

```powershell
.\install.ps1 -Target codex
.\install.ps1 -Target claude
.\install.ps1 -Target all -CleanLegacy
```

`-CleanLegacy` removes common old PaperSpine folders that caused duplicate discovery, such as nested `PaperSpine`, `PaperSpineV2`, and old `paper-spine-*` copies.

After installing for Codex: **Restart Codex**. Then call the skill with `$paper-spine` or select `paper-spine` from the skill list.

After installing for Claude Code: restart or reload Claude Code, then use `/paperspine`.

## Manual Install

Codex expects one self-contained skill folder:

```text
dist/codex/paper-spine
```

Copy it to:

```text
~/.codex/skills/paper-spine
```

The final Codex layout should be:

```text
~/.codex/skills/paper-spine/SKILL.md
~/.codex/skills/paper-spine/references/
~/.codex/skills/paper-spine/scripts/
```

Claude Code expects flat skill folders plus optional slash commands:

```text
dist/claude/skills/*
dist/claude/commands/*.md
```

Copy them to:

```text
~/.claude/skills/
~/.claude/commands/
```

The final Claude Code layout should include:

```text
~/.claude/skills/paper-spine/SKILL.md
~/.claude/skills/paper-spine-intake/SKILL.md
~/.claude/skills/paper-spine-research/SKILL.md
~/.claude/commands/paperspine.md
```

## Claude Code Plugin Install

Claude Code can also use the plugin metadata in `.claude-plugin`.

```text
/plugin marketplace add https://github.com/WUBING2023/PaperSpine
/plugin install paper-spine
/reload-plugins
```

The plugin manifest points to the flat suite under `dist/claude/skills`, not to the Codex distribution.

## Codex vs Claude Code

| Host | Installable unit | Typical entry | Reason |
| --- | --- | --- | --- |
| Codex | `dist/codex/paper-spine` | `$paper-spine` | Codex works best with one bundled skill containing the orchestrator, scripts, and references. |
| Claude Code | `dist/claude/skills/*` plus `dist/claude/commands/*` | `/paperspine` | Claude Code discovers skills as flat folders and supports slash-command helpers. |

Do not copy the whole repository into a `skills` folder. That is the main cause of duplicated or missing skills.

## Main Workflow

PaperSpine has two equal first-class workflows:

1. **Rewrite Existing**: improve an existing manuscript without treating the task as simple polishing.
2. **Build From Materials**: build a manuscript or report from a folder containing notes, figures, PDFs, data summaries, partial drafts, and experiment descriptions.

Supported target scenes:

- `journal`: journal paper
- `conference`: conference paper
- `report/review`: course report, technical report, or review
- `competition`: competition paper or competition report

Research tiers:

- `flash`: 3 target-scene examples, 3 recent/high-quality same-field papers, and official requirements.
- `pro`: 6 target-scene examples, 6 recent/high-quality same-field papers, and official requirements.

Output languages:

- `English`
- `Chinese`

When English output is selected, PaperSpine can also generate a `translation_package` containing Chinese translations of intermediate artifacts and final Markdown outputs.

## Intake UI

Claude Code can launch the PaperSpine intake flow through:

```text
/paperspine
```

The command should launch the PaperSpine intake UI automatically when the host terminal allows it. The fallback is the Python wizard:

```powershell
python src/scripts/intake_wizard.py
```

The intake writes:

```text
paper_rewriting_output/paper_spine_config.json
paper_rewriting_output/paper_spine_config.md
```

Preview the TUI locally:

```powershell
python src/scripts/tui_preview_server.py --port 8765
```

## Required Artifacts

A complete PaperSpine run should produce a transparent audit trail, not just a final manuscript:

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
    paper.docx              # optional Word output
    paper.pdf               # generated when a LaTeX compiler is available
  translation_package/       # optional for English output
```

The central artifact is `writing_rationale_matrix.md`. It must explain the writing plan unit by unit: what the unit does, how it serves the confirmed motivation, what was learned from SOTA or target-scene examples, which evidence supports it, and what final text check should pass.

## Quality Checks

Run the artifact checker:

```powershell
python src/scripts/artifact_check.py paper_rewriting_output --markdown --write
```

For compatibility with copied skill scripts, the same command may appear in skill instructions as:

```powershell
python scripts/artifact_check.py paper_rewriting_output --markdown --write
```

Check LaTeX:

```powershell
python src/scripts/latex_guard.py paper_rewriting_output/final_paper/main.tex --markdown
```

Check Word output:

```powershell
python src/scripts/word_guard.py paper_rewriting_output/final_paper/paper.docx --markdown
```

Run repository tests:

```powershell
python -m unittest discover -s tests
```

## What PaperSpine Tries To Prevent

- Direct sentence-by-sentence polishing with no logic change.
- Treating target journals, competitions, reports, and reviews as the same genre.
- Writing before confirming the motivation.
- Adding claims that are not supported by evidence.
- Producing only `main.tex` without explaining why the paper was written that way.
- Partial translation packages when the user requested translated intermediate and final artifacts.

## License

MIT License. See [LICENSE](LICENSE).
