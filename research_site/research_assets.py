from __future__ import annotations

import base64
from hashlib import sha256
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image

from research_site.catalog import Catalog, CatalogError, ResearchFigure
from research_site.report_content import load_report_source


class ReportImages(HTMLParser):
    def __init__(self) -> None:
        # Index images in their original published document order.
        super().__init__(convert_charrefs=True)
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Keep legacy figures independent of any source workspace.
        if tag == "img":
            self.sources.append(dict(attrs)["src"] or "")


def figure_bytes(
    figure: ResearchFigure, catalog: Catalog, site_root: Path,
    legacy_images: dict[str, list[str]],
) -> bytes:
    # Read only a figure already covered by an approved report.
    report = catalog.report_by_id[figure.report_id]
    if report.is_markdown:
        source = load_report_source(site_root / "content" / str(report.content_file))
        asset = (source.path.parent / str(figure.asset)).resolve()
        if asset not in source.referenced_assets:
            raise CatalogError(f"figure {figure.asset} is not in the report content bundle")
        return asset.read_bytes()

    # Extract immutable embedded pixels without modifying the published report.
    if report.id not in legacy_images:
        parser = ReportImages()
        parser.feed((site_root / "public" / report.route / "index.html").read_text(encoding="utf-8"))
        legacy_images[report.id] = parser.sources
    index = figure.image_index
    assert index is not None
    if index >= len(legacy_images[report.id]):
        raise CatalogError(f"figure index {index} is missing from report {report.id}")
    uri = legacy_images[report.id][index]
    header, encoded = uri.split(",", 1)
    if not header.startswith("data:image/") or not header.endswith(";base64"):
        raise CatalogError(f"report {report.id} figure {index} must be an embedded raster image")
    return base64.b64decode(encoded, validate=True)


def publish_image(data: bytes, output_root: Path) -> dict[str, Any]:
    # Preserve the original bytes at a content-addressed URL.
    digest = sha256(data).hexdigest()
    with Image.open(BytesIO(data)) as image:
        suffix = {"PNG": "png", "JPEG": "jpg", "WEBP": "webp"}[image.format]
        image.load()
        image_root = output_root / "assets" / "research-images"
        image_root.mkdir(parents=True, exist_ok=True)
        original = image_root / f"{digest}.{suffix}"
        original.write_bytes(data)
        width, height = image.size

        # Use lossless responsive renditions so chart labels and values stay intact.
        renditions: list[dict[str, Any]] = []
        for size in sorted({min(width, requested) for requested in (480, 960, 1440)}):
            path = image_root / f"{digest}-{size}.webp"
            resized = image.convert("RGBA").resize((size, max(1, round(height * size / width))), Image.Resampling.LANCZOS)
            resized.save(path, "WEBP", lossless=True, method=4)
            renditions.append({"width": size, "path": path.relative_to(output_root).as_posix()})
    return {
        "sha256": digest, "original": original.relative_to(output_root).as_posix(),
        "width": width, "height": height, "renditions": renditions,
    }


def build_research_figures(
    catalog: Catalog, site_root: Path, output_root: Path,
) -> dict[str, list[dict[str, Any]]]:
    # Deduplicate assets across experiments while retaining report provenance.
    legacy_images: dict[str, list[str]] = {}
    assets: dict[str, dict[str, Any]] = {}
    by_experiment: dict[str, list[dict[str, Any]]] = {}
    for experiment in catalog.experiments:
        figures: list[dict[str, Any]] = []
        for figure in experiment.figures:
            data = figure_bytes(figure, catalog, site_root, legacy_images)
            digest = sha256(data).hexdigest()
            if digest not in assets:
                assets[digest] = publish_image(data, output_root)
            figures.append({
                **assets[digest], "title": figure.title, "report_id": figure.report_id,
                "source_asset": figure.asset, "source_image_index": figure.image_index,
            })
        by_experiment[experiment.id] = figures
    return by_experiment
