# Jialu Gao Research

Static, project-aware catalog for selected research reports. The sibling source
archive remains immutable; this repository contains only explicitly approved
public copies and metadata.

```bash
python3 -m pip install -e '.[test]'
python3 scripts/validate_catalog.py
python3 scripts/build_site.py --base-url / --output _preview
python3 scripts/validate_site.py --base-url / --output _preview
python3 -m http.server 8000 --directory _preview
```

The deployment workflow builds `_site` with the production `/research/` base
path. Local preview uses `/` so navigation works under a plain local server.

Publishing is event-driven. Project directories are never watched or published
automatically. Use the `publish-research-site` Codex skill for audits and report
publication.
