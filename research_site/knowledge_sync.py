from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterator

import yaml


SNAPSHOT_SCHEMA_VERSION = 1
SNAPSHOT_DIRECTORIES = ("articles", "graph", "paths", "quality")
SNAPSHOT_FILES = ("manifest.json", "CHANGELOG.md", "review/queue.json")
QUANT_SNAPSHOT_SCHEMA_VERSION = 1
QUANT_SOURCE_ID = "quant-knowledge"
QUANT_SOURCE_NAME = "Quant Knowledge"
QUANT_ROOT_FILES = ("outline.md",)
QUANT_CHAPTER_RE = re.compile(r"^(?P<number>\d+)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
FORBIDDEN_PUBLIC_TOKENS = (b"/home/", b"/data-cache/", b"localhost", b"127.0.0.1")


class KnowledgeSyncError(ValueError):
    pass


def sync_knowledge_snapshot(source_root: Path, destination: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    destination = destination.resolve()
    _validate_source(source_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".deep-ml-sync-", dir=destination.parent))
    backup = destination.parent / f".{destination.name}.previous"
    try:
        for directory in SNAPSHOT_DIRECTORIES:
            shutil.copytree(source_root / directory, temporary / directory)
        for relative in SNAPSHOT_FILES:
            source = source_root / relative
            target = temporary / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        hashes = {
            path.relative_to(temporary).as_posix(): _sha256(path)
            for path in _snapshot_files(temporary)
        }
        manifest = json.loads((source_root / "manifest.json").read_text(encoding="utf-8"))
        snapshot = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "source_schema_version": manifest["schema_version"],
            "source_generated_at": manifest["generated_at"],
            "source_hashes": manifest["hashes"],
            "counts": {
                "concepts": manifest["counts"]["concepts"],
                "learning_units": manifest["counts"]["learning_units"],
                "articles": manifest["counts"]["articles"],
                "relations": _line_count(source_root / "graph" / "relations.jsonl"),
                "paths": len(tuple((source_root / "paths").glob("*.yaml"))),
                "review_queue_items": manifest["counts"]["review_queue_items"],
            },
            "files": hashes,
        }
        (temporary / "snapshot.yaml").write_text(
            yaml.safe_dump(snapshot, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            os.replace(destination, backup)
        os.replace(temporary, destination)
        if backup.exists():
            shutil.rmtree(backup)
        return snapshot
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        if backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise


def sync_quant_knowledge_snapshot(source_root: Path, destination: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    destination = destination.resolve()
    _validate_quant_source(source_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".quant-knowledge-sync-", dir=destination.parent))
    backup = destination.parent / f".{destination.name}.previous"
    try:
        for relative in QUANT_ROOT_FILES:
            shutil.copy2(source_root / relative, temporary / relative)
        shutil.copytree(source_root / "booklet", temporary / "booklet")
        chapters = _quant_chapter_records(source_root)
        sections = _quant_section_records(source_root)
        hashes = {
            path.relative_to(temporary).as_posix(): _sha256(path)
            for path in _snapshot_files(temporary)
        }
        snapshot = {
            "schema_version": QUANT_SNAPSHOT_SCHEMA_VERSION,
            "source_id": QUANT_SOURCE_ID,
            "source_name": QUANT_SOURCE_NAME,
            "counts": {
                "sections": len(sections),
                "chapters": len(chapters),
                "files": len(hashes),
            },
            "sections": sections,
            "chapters": chapters,
            "files": hashes,
        }
        (temporary / "snapshot.yaml").write_text(
            yaml.safe_dump(snapshot, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            os.replace(destination, backup)
        os.replace(temporary, destination)
        if backup.exists():
            shutil.rmtree(backup)
        return snapshot
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        if backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise


def validate_snapshot(snapshot_root: Path) -> dict[str, Any]:
    snapshot_path = snapshot_root / "snapshot.yaml"
    if not snapshot_path.is_file():
        raise KnowledgeSyncError(f"missing knowledge snapshot manifest: {snapshot_path}")
    payload = yaml.safe_load(snapshot_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
        raise KnowledgeSyncError("knowledge snapshot has unsupported schema_version")
    expected = payload.get("files")
    if not isinstance(expected, dict):
        raise KnowledgeSyncError("knowledge snapshot files must be a mapping")
    actual = {
        path.relative_to(snapshot_root).as_posix(): _sha256(path)
        for path in _snapshot_files(snapshot_root)
    }
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        changed = sorted(path for path in set(actual) & set(expected) if actual[path] != expected[path])
        raise KnowledgeSyncError(
            "knowledge snapshot checksum mismatch: "
            f"missing={missing[:3]}, unexpected={unexpected[:3]}, changed={changed[:3]}"
        )
    for path in _snapshot_files(snapshot_root):
        data = path.read_bytes()
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in data:
                raise KnowledgeSyncError(f"{path} contains forbidden public token {token!r}")
    return payload


def validate_quant_snapshot(snapshot_root: Path) -> dict[str, Any]:
    snapshot_path = snapshot_root / "snapshot.yaml"
    if not snapshot_path.is_file():
        raise KnowledgeSyncError(f"missing quant knowledge snapshot manifest: {snapshot_path}")
    payload = yaml.safe_load(snapshot_path.read_text(encoding="utf-8"))
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != QUANT_SNAPSHOT_SCHEMA_VERSION
        or payload.get("source_id") != QUANT_SOURCE_ID
    ):
        raise KnowledgeSyncError("quant knowledge snapshot has unsupported metadata")
    expected = payload.get("files")
    if not isinstance(expected, dict):
        raise KnowledgeSyncError("quant knowledge snapshot files must be a mapping")
    actual = {
        path.relative_to(snapshot_root).as_posix(): _sha256(path)
        for path in _snapshot_files(snapshot_root)
    }
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        changed = sorted(path for path in set(actual) & set(expected) if actual[path] != expected[path])
        raise KnowledgeSyncError(
            "quant knowledge snapshot checksum mismatch: "
            f"missing={missing[:3]}, unexpected={unexpected[:3]}, changed={changed[:3]}"
        )
    for path in _snapshot_files(snapshot_root):
        data = path.read_bytes()
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in data:
                raise KnowledgeSyncError(f"{path} contains forbidden public token {token!r}")
    return payload


def _validate_source(source_root: Path) -> None:
    required = [source_root / directory for directory in SNAPSHOT_DIRECTORIES]
    required.extend(source_root / relative for relative in SNAPSHOT_FILES)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise KnowledgeSyncError("DeepML source is incomplete: " + ", ".join(missing[:5]))
    manifest = json.loads((source_root / "manifest.json").read_text(encoding="utf-8"))
    counts = manifest.get("counts", {})
    queue = json.loads((source_root / "review" / "queue.json").read_text(encoding="utf-8"))
    articles = tuple((source_root / "articles").glob("*.md"))
    if counts.get("articles") != len(articles):
        raise KnowledgeSyncError("DeepML manifest article count does not match article files")
    if counts.get("review_queue_items") != 0 or queue.get("items") != []:
        raise KnowledgeSyncError("DeepML publication snapshot requires an empty editorial blocker queue")
    unpublished = []
    for path in articles:
        metadata = _front_matter(path)
        if metadata.get("status") != "published" or metadata.get("review", {}).get("state") not in {
            "automated_editorial",
            "approved",
        }:
            unpublished.append(path.name)
    if unpublished:
        raise KnowledgeSyncError("DeepML snapshot contains unpublished articles: " + ", ".join(unpublished[:5]))


def _validate_quant_source(source_root: Path) -> None:
    required = [source_root / relative for relative in QUANT_ROOT_FILES]
    required.extend((source_root / "booklet" / relative) for relative in ("README.md", "progress.md"))
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise KnowledgeSyncError("Quant Knowledge source is incomplete: " + ", ".join(missing[:5]))
    chapters = _quant_chapter_records(source_root)
    if not chapters:
        raise KnowledgeSyncError("Quant Knowledge source contains no chapter Markdown files")
    slugs = [str(item["slug"]) for item in chapters]
    if len(slugs) != len(set(slugs)):
        raise KnowledgeSyncError("Quant Knowledge chapter slugs must be unique")
    sequences = [int(item["sequence"]) for item in chapters]
    if sequences != list(range(1, len(chapters) + 1)):
        raise KnowledgeSyncError("Quant Knowledge chapter sequence must be contiguous from 1")
    sections = _quant_section_records(source_root)
    if not sections:
        raise KnowledgeSyncError("Quant Knowledge source contains no numbered sections")
    for record in chapters:
        path = source_root / str(record["source_path"])
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# "):
            raise KnowledgeSyncError(f"{path} must start with an H1 title")
        if "\n## " not in text:
            raise KnowledgeSyncError(f"{path} must contain H2 chapter sections")
        if re.match(r"^#\s+\d+\.\s+", text):
            raise KnowledgeSyncError(f"{path} H1 title must not repeat its filename sequence")
        if record["section_id"] == "06-deep-learning" and not record["part_id"]:
            raise KnowledgeSyncError(f"{path} must belong to a numbered deep-learning part")
        if len(text.encode("utf-8")) < 1000:
            raise KnowledgeSyncError(f"{path} is too short for publication")
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in text.encode("utf-8"):
                raise KnowledgeSyncError(f"{path} contains forbidden public token {token!r}")


def _front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise KnowledgeSyncError(f"{path} is missing YAML front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise KnowledgeSyncError(f"{path} has unterminated YAML front matter")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        raise KnowledgeSyncError(f"{path} front matter must be a mapping")
    return value


def _snapshot_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "snapshot.yaml":
            yield path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _line_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _quant_section_records(source_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for directory in sorted((source_root / "booklet").iterdir()):
        if not directory.is_dir():
            continue
        match = re.match(r"^(?P<number>\d+)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$", directory.name)
        if match is None:
            continue
        chapter_count = len(tuple(_quant_chapter_paths(directory)))
        if chapter_count == 0:
            continue
        records.append(
            {
                "id": directory.name,
                "sequence": int(match.group("number")),
                "title": _quant_section_title(match.group("slug")),
                "directory": f"booklet/{directory.name}",
                "chapter_count": chapter_count,
            }
        )
    return records


def _quant_chapter_records(source_root: Path) -> list[dict[str, Any]]:
    section_by_directory = {
        str(item["directory"]).split("/", 1)[1]: item
        for item in _quant_section_records(source_root)
    }
    records: list[dict[str, Any]] = []
    booklet_root = source_root / "booklet"
    for path in sorted(booklet_root.rglob("*.md")):
        match = QUANT_CHAPTER_RE.match(path.name)
        if match is None:
            continue
        relative = path.relative_to(booklet_root)
        if len(relative.parts) < 2:
            continue
        section = section_by_directory.get(relative.parts[0])
        if section is None:
            continue
        title = _markdown_h1(path)
        part_id = relative.parts[1] if len(relative.parts) >= 3 else ""
        records.append(
            {
                "slug": match.group("slug"),
                "sequence": int(match.group("number")),
                "title": title,
                "section_id": section["id"],
                "section_title": section["title"],
                "part_id": part_id,
                "part_title": _quant_part_title(part_id),
                "source_path": path.relative_to(source_root).as_posix(),
            }
        )
    return sorted(records, key=lambda item: int(item["sequence"]))


def _quant_chapter_paths(directory: Path) -> Iterator[Path]:
    for path in sorted(directory.rglob("*.md")):
        if QUANT_CHAPTER_RE.match(path.name):
            yield path


def _markdown_h1(path: Path) -> str:
    first = path.read_text(encoding="utf-8").splitlines()[0].strip()
    if not first.startswith("# "):
        raise KnowledgeSyncError(f"{path} must start with an H1 title")
    return first[2:].strip()


def _quant_section_title(slug: str) -> str:
    titles = {
        "python": "Python & Data Stack",
        "probability-timeseries": "Probability, Statistics & Time Series",
        "data-structures-algorithms": "Data Structures & Algorithms",
        "brain-teaser-green-book": "Brain Teaser & Green Book",
        "machine-learning": "Machine Learning Practice",
        "deep-learning": "Deep Learning",
        "market-microstructure": "Market Microstructure",
        "computer-science": "Computer Science",
    }
    return titles.get(slug, slug.replace("-", " ").title())


def _quant_part_title(part_id: str) -> str:
    titles = {
        "01-foundations": "Part 1 · Foundations & Correctness",
        "02-training-optimization": "Part 2 · Training & Optimization",
        "03-sequence-models": "Part 3 · Sequence Models",
        "04-attention-transformers": "Part 4 · Attention & Transformers",
        "05-efficient-systems": "Part 5 · Efficient Systems",
    }
    return titles.get(part_id, part_id.replace("-", " ").title() if part_id else "")
