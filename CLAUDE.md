# CLAUDE.md

Guidance for working in this repo.

## Publishing the NVL72 doc (`nvl72.md`)

`nvl72.md` is the **single source of truth**. Two artifacts are generated from it and are **git-ignored** (never edit or commit them — rebuild instead):

- `nvl72-partner.md` — external/partner version with internal-only content stripped
- `nvl72{,-partner}-{dark,light}.pdf` — NVIDIA-themed PDFs

### Internal-only content

Wrap anything that must not reach partners in HTML comment markers. Both inline and whole-block forms work:

```markdown
<!-- INTERNAL_START -->*(Source: NVIDIA Internal.)*<!-- INTERNAL_END -->
```

`generate_partner.py` deletes everything between the markers (and collapses the blank lines left behind).

### Regenerate after editing `nvl72.md`

Run these from the repo root, in order:

```bash
# 1. Strip internal content → nvl72-partner.md
python3 generate_partner.py

# 2. Build PDFs (writes <base>-dark.pdf and <base>-light.pdf to CWD)
python3 build_pdf.py -i nvl72.md
python3 build_pdf.py -i nvl72-partner.md
```

Verify the partner doc has no leaks: `grep -c INTERNAL nvl72-partner.md` should print `0`.

### Requirements / gotchas

- **Tools:** `mmdc` (mermaid-cli, via node), `pandoc`, and `uvx` (runs WeasyPrint, the default PDF engine — no browser needed). `build_pdf.py --engine chrome` is the fallback.
- **Sandbox:** WeasyPrint runs through `uvx`, which needs to write its cache under `~/.cache/uv`. That path is outside the sandbox's writable set, so the `build_pdf.py` step must run **with the sandbox disabled**. `generate_partner.py` runs fine sandboxed.
- **Mermaid labels:** rendered as native SVG `<text>` (htmlLabels off) so non-browser renderers don't drop them. Consequence: **no `<br/>` line breaks beyond what already renders** — keep diagram labels on one line where possible.
- The partner doc has fewer diagrams than the full doc when a diagram sits inside an `INTERNAL` block (e.g. the Vera Rubin reference diagram).

## Bandwidth-number conventions (NVL72 fabrics)

Getting these consistent has been a repeated source of churn — hold the line:

- **NVLink 5 (GB200/GB300):** state as **900 GB/s per direction**, 18 links/GPU. Any `1.8 TB/s` / `1800 GB/s` figure must be labeled **bidirectional** and tied to **GB200/GB300**.
- **NVLink-C2C:** its own device↔host link at **~200 GB/s per direction per GPU** (measured on GB300 with `nvbandwidth`). It is a *separate path* from the NVLink GPU-to-GPU fabric — not a slower version of it, and not something that "falls short" of a 900 GB/s figure. Don't add ratio comparisons between C2C and NVLink.
- **Collective busBW** (`>900 GB/s` all-reduce, `~600 GB/s` all-to-all) comes from **NCCL Tests** and is distinct from the per-direction link rate. busBW can exceed the **per-direction** line rate (900) under NVLS — never the bidirectional rate.
- Always name the measurement source/system (GB300; `nvbandwidth` for C2C, NCCL Tests for collectives).
