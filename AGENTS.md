# Research site contract

- Treat the configured `0-report-html` archive as immutable source material.
- Publish only reports explicitly listed in `content/reports.yaml`.
- Keep project identity and hierarchy in `content/projects.yaml`.
- Legacy HTML reports are immutable published bytes. Markdown reports are
  immutable content bundles: front matter, Markdown body, tables, and every
  referenced local image are covered by `bundle_sha256`.
- The shared site shell, navigation, templates, and CSS are presentation code
  and may evolve without creating a new Markdown report id.
- Never expose credentials, localhost URLs, home-directory paths, or `/data-cache`
  paths in generated public files.
- Preserve report URLs once published. Changing a legacy HTML file or a Markdown
  content bundle requires a new report id and a `revision_of` link.
- Run catalog validation, unit tests, a production-base build, and site
  validation before committing.
- Production deployment is allowed only from `main`; publication work should
  arrive through a reviewable branch or pull request.
