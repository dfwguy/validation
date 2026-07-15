#!/usr/bin/env python3
"""Convert a Markdown file to PDF using NVIDIA themes.

Usage:
    python3 build_pdf.py -i report.md [-o /output/dir] [--engine weasyprint|chrome]

Outputs <basename>-dark.pdf and <basename>-light.pdf in the output directory
(defaults to the current working directory).

PDF engines:
  weasyprint  Pure-Python, no browser required. Needs: uvx (default)
  chrome      Chrome/Chromium headless. Needs: Chrome installed.
              On WSL, set CHROME env var or Chrome is auto-detected.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import os

TMPDIR = os.environ.get("TMPDIR", "/tmp")

# Force Mermaid to emit native SVG <text> elements instead of wrapping labels
# in <foreignObject> (embedded XHTML). foreignObject is a browser-only feature:
# non-browser SVG renderers (WeasyPrint, librsvg) drop it, which is why diagram
# text came out blank and pushed us to raster PNGs. With htmlLabels off, the SVG
# renders identically everywhere and stays vector (smaller + searchable text).
MERMAID_CONFIG = {"htmlLabels": False, "flowchart": {"htmlLabels": False}}

# Chrome locations to try when engine=chrome
_CHROME_CANDIDATES = [
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def find_chrome():
    for path in _CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    sys.exit("Chrome/Chromium not found. Set CHROME env var or install Chrome.")

DARK_CSS = """
:root {
    --nvidia-green: #76b900;
    --bg: #121212;
    --text: #e6e6e6;
    --text-muted: #969696;
    --code-bg: #1e1e1e;
    --table-header-bg: #2d2d2d;
    --table-row-bg: #1e1e1e;
    --table-row-alt: #242424;
    --border: #333;
    --blockquote-border: #444;
    --blockquote-bg: #1a1a1a;
}
"""

LIGHT_CSS = """
:root {
    --nvidia-green: #76b900;
    --bg: #ffffff;
    --text: #333333;
    --text-muted: #646464;
    --code-bg: #f5f5f5;
    --table-header-bg: #76b900;
    --table-header-color: #ffffff;
    --table-row-bg: #fafafa;
    --table-row-alt: #f0f0f0;
    --border: #ddd;
    --blockquote-border: #76b900;
    --blockquote-bg: #f8f8f8;
}
"""

SHARED_CSS = """
* { box-sizing: border-box; }
body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    max-width: 960px;
    margin: 0 auto;
    padding: 32px 48px;
}
h1 { color: var(--nvidia-green); font-size: 22pt; margin-top: 0; border-bottom: 2px solid var(--nvidia-green); padding-bottom: 8px; }
h2 { color: var(--nvidia-green); font-size: 16pt; margin-top: 28px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
h3 { font-size: 13pt; margin-top: 20px; color: var(--text); }
h4 { font-size: 11pt; margin-top: 16px; color: var(--text-muted); }
p { margin: 8px 0 12px; }
a { color: var(--nvidia-green); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
    background: var(--code-bg);
    color: var(--nvidia-green);
    font-family: "Courier New", Courier, monospace;
    font-size: 9pt;
    padding: 1px 5px;
    border-radius: 3px;
}
pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 16px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.4;
}
pre code { background: transparent; color: var(--text); padding: 0; font-size: inherit; }
blockquote {
    border-left: 3px solid var(--blockquote-border);
    background: var(--blockquote-bg);
    margin: 12px 0;
    padding: 8px 16px;
    color: var(--text-muted);
    font-style: italic;
}
blockquote p { margin: 4px 0; }
table {
    border-collapse: collapse;
    width: 100%;
    font-size: 9.5pt;
    margin: 14px 0;
}
th {
    background: var(--table-header-bg);
    color: var(--table-header-color, var(--text));
    padding: 7px 10px;
    text-align: left;
    font-weight: bold;
    border: 1px solid var(--border);
}
td {
    padding: 6px 10px;
    border: 1px solid var(--border);
    vertical-align: top;
}
tr:nth-child(even) td { background: var(--table-row-alt); }
tr:nth-child(odd) td { background: var(--table-row-bg); }
hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
ul, ol { padding-left: 24px; margin: 8px 0; }
li { margin: 3px 0; }
strong { color: var(--text); }
.mermaid-svg { text-align: center; margin: 20px 0; }
.mermaid-svg svg { max-width: 100%; height: auto; }

@media print {
    body { max-width: none; padding: 20px 32px; font-size: 9.5pt; }
    h1 { font-size: 18pt; }
    h2 { font-size: 13pt; page-break-after: avoid; }
    h3 { page-break-after: avoid; }
    pre, blockquote, table { page-break-inside: avoid; }
    .mermaid { page-break-inside: avoid; }
    a { color: var(--nvidia-green); }
}
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NVL72 Data Flows: C2C, MNNVL, and RDMA</title>
    <style>
{theme_css}
{shared_css}
    </style>
</head>
<body>
{body}
</body>
</html>
"""


def _extract_mermaid_blocks(md_text):
    """Pull mermaid fenced blocks out of markdown; return (stripped_md, blocks)."""
    blocks = []

    def extract(m):
        blocks.append(m.group(1))
        return f'\n<!--MERMAID{len(blocks) - 1}-->\n'

    stripped = re.sub(r'```mermaid\n(.*?)```', extract, md_text, flags=re.DOTALL)
    return stripped, blocks


def _render_diagrams(blocks, mermaid_theme, bg_color):
    """Render each mermaid block to an inline SVG and return HTML fragments.

    SVGs are inlined (not base64 <img>) so they inherit the document's fonts
    and scale cleanly. mmdc hardcodes id="my-svg" and scopes every internal CSS
    rule to it, so each diagram gets a unique --svgId to avoid style collisions
    when multiple diagrams share one page.
    """
    cfg_path = os.path.join(TMPDIR, "mermaid_config.json")
    with open(cfg_path, "w") as f:
        json.dump(MERMAID_CONFIG, f)

    imgs = []
    for i, src in enumerate(blocks):
        mmd_path = os.path.join(TMPDIR, f"diagram_{i}.mmd")
        svg_path = os.path.join(TMPDIR, f"diagram_{i}.svg")
        with open(mmd_path, "w") as f:
            f.write(src)
        result = subprocess.run(
            [
                "mmdc", "-i", mmd_path, "-o", svg_path,
                "--configFile", cfg_path,
                "--svgId", f"diagram-{i}",
                "--theme", mermaid_theme,
                "--backgroundColor", bg_color,
                "--quiet",
            ],
            capture_output=True,
        )
        if result.returncode != 0 or not os.path.exists(svg_path):
            print(f"  [warn] mmdc failed on diagram {i}: {result.stderr.decode().strip()}",
                  file=sys.stderr)
            imgs.append(f'<pre class="mermaid-error">{src}</pre>')
            continue
        with open(svg_path) as f:
            svg = f.read()
        imgs.append(f'<div class="mermaid-svg">{svg}</div>')
        print(f"  diagram {i + 1}/{len(blocks)} rendered")
    return imgs


def md_to_html_body(md_text, mermaid_theme, bg_color):
    """
    Convert markdown to HTML with mermaid diagrams pre-rendered to inline SVG.

    Pandoc mangles mermaid source (turns --> into em-dashes, escapes quotes,
    etc.) so blocks are extracted before pandoc runs, rendered to SVG by mmdc,
    then spliced back in as inline <svg> markup.
    """
    stripped, blocks = _extract_mermaid_blocks(md_text)

    result = subprocess.run(
        ["pandoc", "--from=markdown", "--to=html", "--no-highlight"],
        input=stripped.encode(),
        capture_output=True,
    )
    if result.returncode != 0:
        print("pandoc error:", result.stderr.decode(), file=sys.stderr)
        sys.exit(1)

    imgs = _render_diagrams(blocks, mermaid_theme, bg_color)
    html = result.stdout.decode()

    def restore(m):
        return imgs[int(m.group(1))]

    return re.sub(r'<!--MERMAID(\d+)-->', restore, html)


def build_html(body, theme):
    """Wrap body in full HTML with NVIDIA theme."""
    theme_css = DARK_CSS if theme == "dark" else LIGHT_CSS
    return HTML_TEMPLATE.format(
        theme_css=theme_css,
        shared_css=SHARED_CSS,
        body=body,
    )


def html_to_pdf_weasyprint(html_path, pdf_path):
    """Convert HTML to PDF using WeasyPrint via uvx (no browser required)."""
    result = subprocess.run(
        ["uvx", "--from", "weasyprint", "weasyprint", html_path, pdf_path],
        capture_output=True,
    )
    if result.returncode != 0:
        print("WeasyPrint error:", result.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def html_to_pdf_chrome(html_path, pdf_path):
    """Convert HTML to PDF using Chrome headless."""
    chrome = os.environ.get("CHROME") or find_chrome()
    is_wsl = os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")

    def to_file_url(path):
        if is_wsl:
            win = subprocess.check_output(["wslpath", "-w", path]).decode().strip()
            return "file:///" + win.replace("\\", "/")
        return "file://" + path

    if is_wsl:
        # Chrome (Windows EXE) can't write to the WSL filesystem via UNC paths.
        # Write to a Windows-native temp dir first, then move to the destination.
        win_temp_raw = subprocess.check_output(
            ["cmd.exe", "/c", "echo", "%TEMP%"], capture_output=True
        ).stdout.decode().strip()
        win_temp = subprocess.check_output(["wslpath", "-u", win_temp_raw]).decode().strip()
        tmp_pdf = os.path.join(win_temp, os.path.basename(pdf_path))
        tmp_pdf_win = subprocess.check_output(["wslpath", "-w", tmp_pdf]).decode().strip()
    else:
        tmp_pdf = pdf_path
        tmp_pdf_win = pdf_path

    result = subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={tmp_pdf_win}",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            to_file_url(html_path),
        ],
        capture_output=True,
        timeout=60,
    )
    if result.returncode != 0:
        print("Chrome error:", result.stderr.decode(), file=sys.stderr)
        sys.exit(1)

    if is_wsl and tmp_pdf != pdf_path:
        if not os.path.exists(tmp_pdf):
            sys.exit(f"Chrome did not produce output at {tmp_pdf}")
        os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
        shutil.move(tmp_pdf, pdf_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to NVIDIA-themed PDFs (dark + light)."
    )
    parser.add_argument("-i", "--input", required=True, metavar="FILE",
                        help="Input Markdown file")
    parser.add_argument("-o", "--output-dir", default=None, metavar="DIR",
                        help="Output directory (default: current working directory)")
    parser.add_argument("--engine", default="weasyprint", choices=["weasyprint", "chrome"],
                        help="PDF engine: weasyprint (default, no browser) or chrome")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_path))[0]

    with open(input_path) as f:
        md_text = f.read()

    for theme in ("dark", "light"):
        mermaid_theme = "dark" if theme == "dark" else "default"
        bg_color = "#121212" if theme == "dark" else "white"
        print(f"[{theme}] rendering diagrams…")
        body = md_to_html_body(md_text, mermaid_theme, bg_color)

        html_path = os.path.join(TMPDIR, f"{base}-{theme}.html")
        pdf_path = os.path.join(output_dir, f"{base}-{theme}.pdf")

        html_content = build_html(body, theme)
        with open(html_path, "w") as f:
            f.write(html_content)

        if args.engine == "chrome":
            html_to_pdf_chrome(html_path, pdf_path)
        else:
            html_to_pdf_weasyprint(html_path, pdf_path)

        size = os.path.getsize(pdf_path)
        print(f"[{theme}] PDF written: {pdf_path} ({size:,} bytes)")


if __name__ == "__main__":
    main()
