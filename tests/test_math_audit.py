from pathlib import Path

from research_site.math_audit import audit_markdown_math, audit_math_tree


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_math_audit_accepts_structured_latex() -> None:
    text = r"""
$$
F_X(x)=\Pr(X\le x)=\int_{-\infty}^{x} f_X(t)\,dt
$$
"""

    assert audit_markdown_math(Path("cdf.md"), text) == ()


def test_math_audit_reports_prose_ascii_and_malformed_commands() -> None:
    text = r"""
$$ score = mean(scores over folds) $$
$$ F(x)=P(X\lex) $$
$$ ||x||_2 = sqrt(sum_i x_i^2) $$
"""

    rules = {issue.rule for issue in audit_markdown_math(Path("bad.md"), text)}
    assert rules == {
        "ascii-norm",
        "ascii-operator",
        "malformed-command",
        "plain-identifier",
        "prose-in-math",
    }


def test_math_audit_reports_unbalanced_delimiters() -> None:
    issues = audit_markdown_math(Path("broken.md"), "$$ x+y")

    assert [issue.rule for issue in issues] == ["unbalanced-delimiters"]


def test_math_audit_ignores_shell_expansion_in_fenced_code() -> None:
    text = "```bash\nps -p $$\n```\n"

    assert audit_markdown_math(Path("shell.md"), text) == ()


def test_repository_knowledge_math_passes_audit() -> None:
    assert audit_math_tree(SITE_ROOT / "content" / "knowledge") == ()
