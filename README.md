# Validation

## Contents

- [Engagement Repos](engagement-repos.md)
- [What Do We Validate](what-do-we-validate.md)
- [AI Factory Testing Plan](ai_factory_testing_plan.md)
- [Runbooks](runbooks/) — operational procedures for executing validation activities (e.g., MNUberGEMM burn-in)

## NVL72 data-flows doc

[`nvl72.md`](nvl72.md) is the source of truth. The partner version and PDFs are **generated** (git-ignored) — rebuild them after any edit rather than editing them directly:

```bash
python3 generate_partner.py            # nvl72.md → nvl72-partner.md (strips INTERNAL blocks)
uv run python build_pdf.py -i nvl72.md            # → nvl72-{dark,light}.pdf
uv run python build_pdf.py -i nvl72-partner.md    # → nvl72-partner-{dark,light}.pdf
```

Requires `mmdc` (mermaid-cli), `pandoc`, and `uv` (manages WeasyPrint automatically).

### Installing `build-pdf` as a global tool

Install once from the repo root and use `build-pdf` anywhere:

```bash
uv tool install /path/to/this/repo
# or, from within the repo:
uv tool install .
```

Then from any directory:

```bash
build-pdf -i report.md [-o /output/dir] [--engine weasyprint|chrome]
```

See [CLAUDE.md](CLAUDE.md) for internal-content markers and bandwidth-number conventions.
