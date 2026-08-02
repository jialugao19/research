#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from research_site.audit import audit_payload, audit_report_ownership
from research_site.catalog import CatalogError, load_catalog


def main() -> int:
    workspace_root = Path(os.environ.get("RESEARCH_WORKSPACE_ROOT", Path.home()))
    parser = argparse.ArgumentParser(description="Read-only audit of report ownership across local projects")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--workspace-root", type=Path, default=workspace_root)
    parser.add_argument("--archive-root", type=Path, default=workspace_root / "0-report-html")
    parser.add_argument(
        "--central-catalog",
        type=Path,
        default=workspace_root / "exp-nn/all-experiments-research-report/report/report-catalog.json",
    )
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.site_root.resolve() / "content")
        matches = audit_report_ownership(
            catalog,
            args.workspace_root.resolve(),
            args.archive_root.resolve(),
            args.central_catalog.resolve(),
        )
    except (CatalogError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(audit_payload(matches), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
