from __future__ import annotations

import argparse
from pathlib import Path

from research_site.knowledge_sync import sync_knowledge_snapshot, sync_quant_knowledge_snapshot


SITE_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync validated knowledge snapshots into the site.")
    parser.add_argument("--deepml-source", type=Path, default=Path("/home/maomao/deep-ml/content"))
    parser.add_argument(
        "--deepml-destination",
        type=Path,
        default=SITE_ROOT / "content" / "knowledge" / "deep-ml",
    )
    parser.add_argument("--quant-source", type=Path, default=Path("/home/maomao/knowledge"))
    parser.add_argument(
        "--quant-destination",
        type=Path,
        default=SITE_ROOT / "content" / "knowledge" / "quant-knowledge",
    )
    parser.add_argument("--skip-deepml", action="store_true")
    parser.add_argument("--skip-quant", action="store_true")
    args = parser.parse_args()
    if not args.skip_deepml:
        snapshot = sync_knowledge_snapshot(args.deepml_source, args.deepml_destination)
        print({"deep-ml": snapshot["counts"]})
    if not args.skip_quant:
        snapshot = sync_quant_knowledge_snapshot(args.quant_source, args.quant_destination)
        print({"quant-knowledge": snapshot["counts"]})


if __name__ == "__main__":
    main()
