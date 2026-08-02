# Research site contract

- Treat the configured `0-report-html` archive as immutable source material.
- Publish only reports explicitly listed in `content/reports.yaml`.
- Keep project identity and hierarchy in `content/projects.yaml`.
- Never expose credentials, localhost URLs, home-directory paths, or `/data-cache`
  paths in generated public files.
- Preserve report URLs once published. Changed content requires a new report id.
- Run catalog validation, unit tests, a production-base build, and site
  validation before committing.
- Production deployment is allowed only from `main`; publication work should
  arrive through a reviewable branch or pull request.
