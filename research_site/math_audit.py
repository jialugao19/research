from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from latex2mathml.converter import convert


DISPLAY_MATH_RE = re.compile(r"\$\$\s*(.*?)\s*\$\$", re.DOTALL)
ASCII_OPERATOR_RE = re.compile(
    r"(?<!\\)\b(?:argmax|argmin|exp|integral|lim|ln|log|max|mean|min|prod|sigmoid|softmax|sqrt|sum)\b"
)
PLAIN_PROSE_RE = re.compile(
    r"\b(?:and|around|before|comes|each|for|from|instead|into|only|over|per|plus|such|until|uses|when|with)\b",
    re.IGNORECASE,
)
MALFORMED_COMMAND_RE = re.compile(r"\\(?:lex|leb|gex|geb)\b")
PLAIN_IDENTIFIER_RE = re.compile(r"(?<![\\A-Za-z])[A-Za-z]{3,}(?![A-Za-z])")


@dataclass(frozen=True)
class MathIssue:
    path: Path
    block: int
    rule: str
    expression: str


def audit_markdown_math(path: Path, text: str) -> tuple[MathIssue, ...]:
    """Return deterministic display-math issues for one Markdown document."""
    issues: list[MathIssue] = []
    source = _without_fenced_code(text)
    delimiters = source.count("$$")
    if delimiters % 2:
        issues.append(MathIssue(path, 0, "unbalanced-delimiters", ""))

    for block, match in enumerate(DISPLAY_MATH_RE.finditer(source), start=1):
        expression = match.group(1).strip()
        if not expression:
            issues.append(MathIssue(path, block, "empty-expression", expression))
            continue
        try:
            convert(expression)
        except Exception:
            issues.append(MathIssue(path, block, "invalid-latex", expression))
            continue

        normalized = _without_text_commands(expression)
        if MALFORMED_COMMAND_RE.search(normalized):
            issues.append(MathIssue(path, block, "malformed-command", expression))
        if ASCII_OPERATOR_RE.search(normalized):
            issues.append(MathIssue(path, block, "ascii-operator", expression))
        if PLAIN_PROSE_RE.search(normalized):
            issues.append(MathIssue(path, block, "prose-in-math", expression))
        commands_removed = re.sub(r"\\(?:begin|end)\{[^{}]+\}", "", normalized)
        commands_removed = re.sub(r"\\[A-Za-z]+", "", commands_removed)
        commands_removed = re.sub(r"\bd[A-Za-z]\b", "", commands_removed)
        if PLAIN_IDENTIFIER_RE.search(commands_removed):
            issues.append(MathIssue(path, block, "plain-identifier", expression))
        if "||" in normalized:
            issues.append(MathIssue(path, block, "ascii-norm", expression))
        if re.search(r"(?<!\\)\.\.\.", normalized):
            issues.append(MathIssue(path, block, "ascii-ellipsis", expression))
    return tuple(issues)


def audit_math_tree(root: Path) -> tuple[MathIssue, ...]:
    """Audit every Markdown file below root in stable path order."""
    issues: list[MathIssue] = []
    for path in sorted(root.rglob("*.md")):
        issues.extend(audit_markdown_math(path, path.read_text(encoding="utf-8")))
    return tuple(issues)


def _without_text_commands(expression: str) -> str:
    result = expression
    for command in ("operatorname", "mathrm", "text", "mathbf", "mathbb"):
        result = re.sub(rf"\\{command}\{{[^{{}}]*\}}", "", result)
    return result


def _without_fenced_code(text: str) -> str:
    return re.sub(r"^(```|~~~).*?^\1\s*$", "", text, flags=re.MULTILINE | re.DOTALL)
