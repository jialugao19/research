#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from research_site.audit import audit_payload, audit_report_ownership
from research_site.catalog import CatalogError, load_catalog


def main() -> int:
    # Resolve local discovery roots without exposing them in audit evidence.
    workspace_root = Path(os.environ.get("RESEARCH_WORKSPACE_ROOT", Path.home()))
    registry_root = Path(os.environ.get("RESEARCH_NN_REGISTRY_ROOT", workspace_root / "exp-nn/0-select&report"))
    parser = argparse.ArgumentParser(description="Read-only audit of report ownership across local projects")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--workspace-root", type=Path, default=workspace_root)
    parser.add_argument("--archive-root", type=Path, default=workspace_root / "0-report-html")
    args = parser.parse_args()
    # Audit registered sources without changing reports or publication state.
    try:
        catalog = load_catalog(args.site_root.resolve() / "content")
        matches = audit_report_ownership(
            catalog,
            args.workspace_root.resolve(),
            args.archive_root.resolve(),
            registry_root.resolve(),
        )
    except (CatalogError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(audit_payload(matches), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
