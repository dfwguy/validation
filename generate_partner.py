#!/usr/bin/env python3
"""Generate nvl72-partner.md by stripping INTERNAL_START/END blocks from nvl72.md."""

import re
import sys
from pathlib import Path

SRC = Path(__file__).parent / "nvl72.md"
DST = Path(__file__).parent / "nvl72-partner.md"

content = SRC.read_text()

# Remove block markers (own lines) and their content
content = re.sub(r"\n<!-- INTERNAL_START -->\n.*?<!-- INTERNAL_END -->", "", content, flags=re.DOTALL)

# Remove inline markers and their content
content = re.sub(r"<!-- INTERNAL_START -->.*?<!-- INTERNAL_END -->", "", content)

# Collapse any double blank lines left behind
content = re.sub(r"\n{3,}", "\n\n", content)

DST.write_text(content)
print(f"Written: {DST}")
