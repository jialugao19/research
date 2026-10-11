from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BuildResult:
    output_root: Path
    file_count: int


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def build_atomically(
    output_root: Path,
    render: Callable[[Path], None],
    validate: Callable[[Path], None],
) -> BuildResult:
    """Render and validate beside the target, then replace it with rollback safety."""
    output_root = output_root.resolve()
    output_root.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{output_root.name}.build-",
            dir=output_root.parent,
        )
    )
    # mkdtemp deliberately creates mode 0700. The published directory is served by
    # an unprivileged Nginx worker, so its root must remain traversable after rename.
    staging.chmod(0o755)
    backup = Path(
        tempfile.mkdtemp(
            prefix=f".{output_root.name}.previous-",
            dir=output_root.parent,
        )
    )
    backup.rmdir()
    old_output_moved = False
    published = False
    try:
        render(staging)
        validate(staging)
        file_count = sum(path.is_file() for path in staging.rglob("*"))
        if output_root.exists() or output_root.is_symlink():
            os.replace(output_root, backup)
            old_output_moved = True
        try:
            os.replace(staging, output_root)
            published = True
        except BaseException:
            if old_output_moved and not output_root.exists():
                os.replace(backup, output_root)
                old_output_moved = False
            raise
        return BuildResult(output_root=output_root, file_count=file_count)
    finally:
        if staging.exists() or staging.is_symlink():
            _remove_path(staging)
        if published and (backup.exists() or backup.is_symlink()):
            _remove_path(backup)
