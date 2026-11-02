#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from research_site.catalog import CatalogError, load_catalog
from research_site.validation import validate_built_site


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a built research site")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--base-url", default="/research/")
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    output = args.output.resolve() if args.output else site_root / "_site"
    try:
        catalog = load_catalog(site_root / "content")
        validate_built_site(catalog, site_root, output, args.base_url)
    except CatalogError as exc:
        parser.error(str(exc))
    print(
        f"site valid: {len(catalog.research_projects)} research projects, "
        f"{len(catalog.infrastructure_projects)} infrastructure systems, {len(catalog.experiments)} experiments, "
        f"{len(catalog.reports)} reports, and Knowledge at {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
