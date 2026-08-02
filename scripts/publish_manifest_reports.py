#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from research_site.catalog import CatalogError, load_catalog
from research_site.publication import publish_reports


def main() -> int:
    workspace_root = Path(os.environ.get("RESEARCH_WORKSPACE_ROOT", Path.home()))
    parser = argparse.ArgumentParser(description="Publish sanitized copies of manifest-approved reports")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--archive-root", type=Path, default=workspace_root / "0-report-html")
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    try:
        catalog = load_catalog(site_root / "content")
        results = publish_reports(catalog, args.archive_root.resolve(), site_root / "public" / "reports")
    except CatalogError as exc:
        parser.error(str(exc))
    for result in results:
        print(
            f"{result.report_id}\t{result.size_bytes}\t{result.source_sha256}\t"
            f"{result.published_sha256}\t{result.destination_path}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
