#!/usr/bin/env python3
"""Sync PaperSpine dist layouts into local Codex and Claude Code installs."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST_CODEX_SKILL = ROOT / "dist" / "codex" / "paper-spine"
DIST_CLAUDE_SKILLS = ROOT / "dist" / "claude" / "skills"
DIST_CLAUDE_COMMANDS = ROOT / "dist" / "claude" / "commands"

SUITE_SKILLS = (
    "paper-spine",
    "paper-spine-intake",
    "paper-spine-research",
    "paper-spine-rewrite",
    "paper-spine-build",
    "paper-spine-latex",
    "paper-spine-audit",
)


def parse_args() -> argparse.Namespace:
    home = Path.home()
    parser = argparse.ArgumentParser(description="Sync PaperSpine dist layouts into local installs.")
    parser.add_argument(
        "--desktop-root",
        type=Path,
        default=home / "Desktop" / "PaperSpine",
        help="Optional desktop export root. Receives dist/ only; skipped when equal to this repository.",
    )
    parser.add_argument(
        "--codex-skills-dir",
        type=Path,
        default=home / ".codex" / "skills",
        help="Codex skills directory. Receives dist/codex/paper-spine.",
    )
    parser.add_argument(
        "--claude-skills-dir",
        type=Path,
        default=home / ".claude" / "skills",
        help="Claude Code flat skills directory. Receives dist/claude/skills/*.",
    )
    parser.add_argument(
        "--claude-commands-dir",
        type=Path,
        default=home / ".claude" / "commands",
        help="Claude Code commands directory. Receives dist/claude/commands/*.md.",
    )
    parser.add_argument("--clean-legacy", action="store_true")
    parser.add_argument("--clean-legacy-claude-nested", action="store_true", help="Deprecated alias for --clean-legacy.")
    return parser.parse_args()


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return left.absolute() == right.absolute()


def remove_path(path: Path) -> None:
    if not path.exists():
        return
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    except PermissionError as exc:
        print(f"Warning: skipped locked legacy path: {path} ({exc})", file=sys.stderr)


def clean_legacy(args: argparse.Namespace) -> None:
    paths = [
        args.desktop_root / "codex",
        args.desktop_root / "claude",
        args.desktop_root / "claude-code",
        args.codex_skills_dir / "PaperSpine",
        args.codex_skills_dir / "PaperSpineV2",
        args.codex_skills_dir / "paper-spine",
        args.claude_skills_dir / "PaperSpine",
        args.claude_skills_dir / "PaperSpineV2",
        args.claude_skills_dir / "paper-writing-assistant",
        args.claude_commands_dir / "paperspine.md",
        args.claude_commands_dir / "paperspine-ui.md",
    ]
    paths.extend(args.claude_skills_dir / skill for skill in SUITE_SKILLS)
    for path in paths:
        remove_path(path)


def sync_desktop_export(desktop_root: Path) -> None:
    if same_path(desktop_root, ROOT):
        print(f"Skipping desktop export because target is repository root: {desktop_root}")
        return
    desktop_root.mkdir(parents=True, exist_ok=True)
    copy_tree(ROOT / "dist", desktop_root / "dist")
    copy_tree(ROOT / "src", desktop_root / "src")
    copy_tree(ROOT / ".claude-plugin", desktop_root / ".claude-plugin")
    shutil.copy2(ROOT / "README.md", desktop_root / "README.md")
    shutil.copy2(ROOT / "README.zh-CN.md", desktop_root / "README.zh-CN.md")
    shutil.copy2(ROOT / "LICENSE", desktop_root / "LICENSE")
    shutil.copy2(ROOT / "install.ps1", desktop_root / "install.ps1")


def sync_local_installs(args: argparse.Namespace) -> None:
    args.codex_skills_dir.mkdir(parents=True, exist_ok=True)
    args.claude_skills_dir.mkdir(parents=True, exist_ok=True)
    args.claude_commands_dir.mkdir(parents=True, exist_ok=True)

    copy_tree(DIST_CODEX_SKILL, args.codex_skills_dir / "paper-spine")
    for skill_dir in DIST_CLAUDE_SKILLS.iterdir():
        if skill_dir.is_dir():
            copy_tree(skill_dir, args.claude_skills_dir / skill_dir.name)
    for command_file in DIST_CLAUDE_COMMANDS.glob("*.md"):
        shutil.copy2(command_file, args.claude_commands_dir / command_file.name)


def main() -> int:
    args = parse_args()
    for required in (DIST_CODEX_SKILL, DIST_CLAUDE_SKILLS, DIST_CLAUDE_COMMANDS):
        if not required.exists():
            raise FileNotFoundError(required)

    if args.clean_legacy or args.clean_legacy_claude_nested:
        clean_legacy(args)
    sync_desktop_export(args.desktop_root)
    sync_local_installs(args)

    print("PaperSpine local sync complete")
    print(f"Desktop dist export: {args.desktop_root / 'dist'}")
    print(f"Codex install: {args.codex_skills_dir / 'paper-spine'}")
    print(f"Claude skills install: {args.claude_skills_dir}")
    print(f"Claude commands install: {args.claude_commands_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
