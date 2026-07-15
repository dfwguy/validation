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
python3 build_pdf.py -i nvl72.md       # → nvl72-{dark,light}.pdf
python3 build_pdf.py -i nvl72-partner.md   # → nvl72-partner-{dark,light}.pdf
```

Requires `mmdc` (mermaid-cli), `pandoc`, and `uvx`. The PDF step must run with the sandbox disabled (WeasyPrint writes to `~/.cache/uv`). See [CLAUDE.md](CLAUDE.md) for details, internal-content markers, and bandwidth-number conventions.
