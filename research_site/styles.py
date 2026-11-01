from pathlib import Path


STYLE_SOURCES = ("tokens.css", "shell.css", "research.css")


def site_stylesheet(site_root: Path) -> str:
    """Compile the shared site and standalone-report stylesheet from one source."""
    # Keep design tokens, inherited presentation, and research extensions ordered.
    style_root = site_root / "assets" / "styles"
    return "\n".join((style_root / name).read_text(encoding="utf-8") for name in STYLE_SOURCES)
