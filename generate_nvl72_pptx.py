"""
NVL72 Data Flows presentation generator.
30 slides, 5 sections, 5x5 format (max 5 bullets x 5 words each).
NVIDIA light-external template.
"""

import sys
import os

SKILL_DIR = os.path.expanduser("~/.claude/skills/generating-nvidia-pptx")
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from load_template import load_nvidia_template, clear_placeholders
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import pptx.util as util

DIAG_DIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "nvl72-pptx", "mermaid")
OUT_PATH = "nvl72_presentation.pptx"

NV_GREEN = RGBColor(0x76, 0xB9, 0x00)
BLACK = RGBColor(0x00, 0x00, 0x00)
GRAY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def E(inches):
    """Convert logical inches (10x5.625 canvas) to 4x EMU."""
    return Emu(int(inches * 914400 * 4))


def get_layout(prs, n):
    """Get slide layout by 1-based index."""
    return prs.slide_layouts[n - 1]


def add_title_text(slide, title, subtitle=None):
    """Populate title and optional subtitle placeholders."""
    for ph in slide.placeholders:
        if ph.placeholder_format.type.name == "TITLE" or ph.placeholder_format.idx == 10:
            ph.text = title
        elif subtitle and ph.placeholder_format.idx in (13, 11):
            ph.text = subtitle


def add_bullets(slide, bullets, font_pt=28):
    """Populate the body text placeholder with bullet lines."""
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 13:
            tf = ph.text_frame
            tf.word_wrap = True
            for i, line in enumerate(bullets):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.level = 0
                run = p.runs[0] if p.runs else p.add_run()
                run.font.size = Pt(font_pt)
                run.font.color.rgb = BLACK
            return


def add_image_slide(prs, title, subtitle, img_path):
    """Slide with title + full-width image below."""
    slide = prs.slides.add_slide(get_layout(prs, 9))  # Title, Subtitle
    add_title_text(slide, title, subtitle)
    # Remove subtitle placeholder — we use the full area for image
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 13:
            sp = ph._element
            sp.getparent().remove(sp)
    # Image below title: x=0.5, y=1.45, w=9, h=3.9 (logical inches)
    slide.shapes.add_picture(img_path, E(0.5), E(1.45), E(9.0), E(3.9))
    return slide


def add_content_slide(prs, title, subtitle, bullets, font_pt=28):
    """5x5 content slide: title + subtitle + up to 5 bullets."""
    layout_idx = 10  # Title, Subtitle, Bullets
    slide = prs.slides.add_slide(get_layout(prs, layout_idx))
    # Populate title
    for ph in slide.placeholders:
        if ph.placeholder_format.type.name == "TITLE":
            ph.text = title
        elif ph.placeholder_format.idx == 14:  # subtitle
            ph.text = subtitle if subtitle else ""
        elif ph.placeholder_format.idx == 13:  # body
            tf = ph.text_frame
            tf.word_wrap = True
            for i, line in enumerate(bullets):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.level = 0
                if p.runs:
                    run = p.runs[0]
                else:
                    run = p.add_run()
                run.font.size = Pt(font_pt)
                run.font.color.rgb = BLACK
    return slide


def add_two_col_slide(prs, title, subtitle, left_header, left_items, right_header, right_items):
    """Two-column slide using Layout 11."""
    slide = prs.slides.add_slide(get_layout(prs, 11))
    for ph in slide.placeholders:
        idx = ph.placeholder_format.idx
        if ph.placeholder_format.type.name == "TITLE":
            ph.text = title
        elif idx == 14:
            ph.text = subtitle if subtitle else ""
        elif idx == 15:  # left column
            tf = ph.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = left_header
            tf.paragraphs[0].runs[0].font.bold = True
            tf.paragraphs[0].runs[0].font.size = Pt(24)
            for item in left_items:
                p = tf.add_paragraph()
                p.text = item
                if p.runs:
                    p.runs[0].font.size = Pt(22)
        elif idx == 16:  # right column
            tf = ph.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = right_header
            tf.paragraphs[0].runs[0].font.bold = True
            tf.paragraphs[0].runs[0].font.size = Pt(24)
            for item in right_items:
                p = tf.add_paragraph()
                p.text = item
                if p.runs:
                    p.runs[0].font.size = Pt(22)
    return slide


def add_transition_slide(prs, section_num, section_title, subtitle=""):
    """Section divider using Layout 3 (Transition)."""
    slide = prs.slides.add_slide(get_layout(prs, 3))
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 11:
            ph.text = f"Section {section_num}  ·  {section_title}"
    return slide


def add_title_slide(prs, title, subtitle, detail):
    """Opening title slide using Layout 1."""
    slide = prs.slides.add_slide(get_layout(prs, 1))
    for ph in slide.placeholders:
        idx = ph.placeholder_format.idx
        if idx == 10:
            ph.text = title
        elif idx == 11:
            ph.text = subtitle
        elif idx == 12:
            ph.text = detail
    return slide


def add_focal_slide(prs, title, focal_text, lines):
    """Slide with large focal phrase + 3–4 supporting lines."""
    slide = prs.slides.add_slide(get_layout(prs, 44))  # Blank
    clear_placeholders(slide)
    # Title bar
    tb = slide.shapes.add_textbox(E(0.5), E(0.15), E(9.0), E(0.7))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.runs[0].font.size = Pt(28)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLACK
    # Focal phrase
    fb = slide.shapes.add_textbox(E(0.5), E(1.1), E(9.0), E(1.4))
    tf = fb.text_frame
    p = tf.paragraphs[0]
    p.text = focal_text
    p.runs[0].font.size = Pt(54)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = NV_GREEN
    # Supporting lines
    y = 2.65
    for line in lines:
        lb = slide.shapes.add_textbox(E(0.7), E(y), E(8.6), E(0.55))
        tf = lb.text_frame
        p = tf.paragraphs[0]
        p.text = line
        p.runs[0].font.size = Pt(26)
        p.runs[0].font.color.rgb = GRAY
        y += 0.6
    return slide


# ─────────────────────────────────────────────
# Build presentation
# ─────────────────────────────────────────────

def diag(name):
    return os.path.join(DIAG_DIR, f"{name}.png")


prs = load_nvidia_template(template_variant="light-external")

# ── Slide 1: Title ───────────────────────────────────────────────────────────
add_title_slide(
    prs,
    title="NVL72 Data Flows",
    subtitle="C2C · MNNVL · RDMA",
    detail="GB200 / GB300 NVL72  ·  HW/SW/Network Engineers  ·  2026",
)

# ═══════════════════════════════════════════════
# SECTION 1: The Three Fabrics
# ═══════════════════════════════════════════════
add_transition_slide(prs, 1, "The Three Fabrics")

# Slide 3
add_content_slide(
    prs,
    title="Three fabrics, three scopes",
    subtitle="Each fabric serves a distinct communication domain",
    bullets=[
        "C2C: Grace CPU ↔ Blackwell GPU",
        "MNNVL: 72 GPUs, one NVLink domain",
        "RDMA: cross-rack, SuperPOD / cluster",
        "Each has distinct BW and semantics",
        "Pick fabric by transfer scope",
    ],
)

# Slide 4: Rack topology diagram
add_image_slide(prs,
    title="NVL72 rack topology",
    subtitle="C2C inside superchip · MNNVL binds 72 GPUs · RDMA leaves rack",
    img_path=diag("d1_rack_topology"),
)

# Slide 5
add_content_slide(
    prs,
    title="Concentric scopes — the mental model",
    subtitle="Three nested domains, three distinct fabrics",
    bullets=[
        "Intra-superchip: C2C (coherent)",
        "Intra-rack: MNNVL / NVLink 5",
        "Inter-rack: RDMA via SuperNIC",
        "TP × EP × CP ≤ 72 (one rack)",
        "DP and PP span racks via RDMA",
    ],
)

# Slide 6: Fabric decision diagram
add_image_slide(prs,
    title="Which fabric for which hop",
    subtitle="NCCL selects transport per rank-pair based on discovered topology",
    img_path=diag("d2_fabric_decision"),
)

# Slide 7: Rule of thumb focal
add_focal_slide(prs,
    title="Rule of thumb",
    focal_text="Stay on the fastest fabric",
    lines=[
        "C2C for CPU ↔ GPU transfers",
        "NVLink for anything inside 72 GPUs",
        "RDMA only when you must leave the rack",
    ],
)

# ═══════════════════════════════════════════════
# SECTION 2: NVLink-C2C
# ═══════════════════════════════════════════════
add_transition_slide(prs, 2, "NVLink-C2C: The Device↔Host Path")

# Slide 9
add_two_col_slide(prs,
    title="What C2C is — and is not",
    subtitle="Understanding the device↔host boundary",
    left_header="C2C IS",
    left_items=[
        "Grace CPU ↔ Blackwell GPU link",
        "Cache-coherent, unified memory",
        "~200 GB/s per direction (measured)",
        "The host↔device path (cudaMemcpy)",
        "Intra-superchip only",
    ],
    right_header="C2C IS NOT",
    right_items=[
        "A GPU-to-GPU data path",
        "A slower version of NVLink",
        "Free capacity or overflow tier",
        "Comparable to 900 GB/s NVLink",
        "Visible in GPU-to-GPU NCCL BW",
    ],
)

# Slide 10: big number
add_focal_slide(prs,
    title="NVLink-C2C bandwidth",
    focal_text="~200 GB/s / direction",
    lines=[
        "Measured on GB300 with nvbandwidth",
        "Per GPU, each direction independently",
        "Faster than PCIe Gen5 x16 (~64 GB/s)",
        "Unchanged between GB200 and GB300",
    ],
)

# Slide 11
add_content_slide(prs,
    title="When C2C is on the critical path",
    subtitle="Three scenarios where ~200 GB/s becomes a binding constraint",
    bullets=[
        "Data ingestion: H2D before forward pass",
        "Optimizer offload: D2H + H2D roundtrip",
        "KV-cache spill for long-context inference",
        "Overlap with compute or it bottlenecks",
        "Measure: step time with offload on/off",
    ],
)

# Slide 12
add_content_slide(prs,
    title="C2C budget per training step",
    subtitle="70B dense model, BS=1 — rough transfer sizes",
    bullets=[
        "Token embedding H2D: negligible",
        "Activation checkpoint D2H: 5–50 ms/layer",
        "ZeRO-3 optimizer D2H + H2D: ~1.4 s",
        "KV-cache spill/reload: 10–100 ms/eviction",
        "Checkpoint save D2H: ~720 ms",
    ],
)

# Slide 13: training step diagram
add_image_slide(prs,
    title="C2C in the full training loop",
    subtitle="H2D before forward pass · optimizer D2H/H2D if CPU offload · checkpoint D2H",
    img_path=diag("d7_training_step"),
)

# ═══════════════════════════════════════════════
# SECTION 3: MNNVL and RDMA
# ═══════════════════════════════════════════════
add_transition_slide(prs, 3, "MNNVL and RDMA: Scale-Up and Scale-Out")

# Slide 15
add_content_slide(prs,
    title="MNNVL: in-rack scale-up",
    subtitle="72 GPUs, one flat NVLink domain, one switch hop",
    bullets=[
        "18 NVLink 5 links per GPU",
        "900 GB/s per direction per GPU",
        "130 TB/s NVSwitch backplane aggregate",
        "AllReduce busBW >900 GB/s measured",
        "AllToAll busBW ~600 GB/s measured",
    ],
)

# Slide 16
add_two_col_slide(prs,
    title="RDMA: scale-out by generation",
    subtitle="GPUDirect RDMA path differs between GB200 and GB300",
    left_header="GB200 / CX-7",
    left_items=[
        "400 Gb/s (50 GB/s) per GPU",
        "Indirect: GPU → C2C → Grace → PCIe → CX-7",
        "No direct GPUDirect RDMA to HBM",
        "Quantum-2 IB or Spectrum-X fabric",
        "Rail-optimized, 1 NIC per GPU",
    ],
    right_header="GB300 / CX-8",
    right_items=[
        "800 Gb/s (100 GB/s) per GPU",
        "Direct: CX-8 connected to Blackwell GPU",
        "True GPUDirect RDMA — HBM direct",
        "Quantum-X800 IB or Spectrum-X fabric",
        "2× cross-rack BW vs GB200",
    ],
)

# Slide 17: NCCL transport diagram
add_image_slide(prs,
    title="How NCCL selects the transport",
    subtitle="Per rank-pair, per collective, per channel — based on discovered topology",
    img_path=diag("d3_nccl_transport"),
)

# Slide 18
add_content_slide(prs,
    title="NCCL transport ↔ fabric mapping",
    subtitle="Key levers: NCCL_NVLS_ENABLE, NCCL_COLLNET_ENABLE, NCCL_IB_HCA",
    bullets=[
        "P2P (CUMEM): NVLink, in-rack pairs",
        "NVLink SHARP (NVLS): NVSwitch reduction",
        "NET + GPUDirect RDMA: cross-rack pairs",
        "CollNet / SHARP: IB in-network reduction",
        "SHM/host fallback: misconfig, avoid",
    ],
)

# Slide 19
add_two_col_slide(prs,
    title="GB200 vs GB300 — what changes",
    subtitle="Scale-up story is identical; the generational change is scale-out",
    left_header="Unchanged (both gens)",
    left_items=[
        "C2C: ~200 GB/s/dir per GPU",
        "MNNVL: 900 GB/s/dir per GPU",
        "NVLink SHARP (NVLS) in-rack",
        "72-GPU NVLink domain per rack",
        "Rail-optimized topology",
    ],
    right_header="Changed in GB300",
    right_items=[
        "CX-8: 800 Gb/s vs CX-7 400 Gb/s",
        "Direct GPUDirect RDMA to HBM",
        "288 GB HBM3e vs ~192 GB HBM3e",
        "NVLink:RDMA gap 18× → 9× (all-reduce)",
        "Less KV-cache spill needed",
    ],
)

# ═══════════════════════════════════════════════
# SECTION 4: Collectives and MoE
# ═══════════════════════════════════════════════
add_transition_slide(prs, 4, "Collectives: AllReduce vs AllToAll and MoE")

# Slide 21: AllReduce diagram
add_image_slide(prs,
    title="AllReduce: ring steps are neighbor-only",
    subtitle="Two RDMA seam hops per rack boundary — all other steps on NVLink",
    img_path=diag("d4_allreduce"),
)

# Slide 22: AllToAll diagram
add_image_slide(prs,
    title="AllToAll: every rank sends a unique chunk",
    subtitle="No ring/tree shortcut — any cross-rack pair must traverse RDMA",
    img_path=diag("d5_alltoall"),
)

# Slide 23: focal
add_focal_slide(prs,
    title="Why AllToAll punishes fabric boundaries",
    focal_text=">900 → ~100 GB/s",
    lines=[
        "AllReduce: only 2 RDMA seam hops at rack boundary",
        "AllToAll: every pair crossing rack boundary uses RDMA",
        "No NVLS offload — NVLS only reduces, not permutes",
        "Keep EP AllToAll inside the 72-GPU NVLink domain",
    ],
)

# Slide 24
add_content_slide(prs,
    title="MoE basics: why it matters for NVL72",
    subtitle="DeepSeek-V3/R1, Mixtral — MoE is the dominant new model class",
    bullets=[
        "N expert sub-networks replace one FFN",
        "Router selects top-K experts per token",
        "Only K/N experts fire — FLOPs stay fixed",
        "Expert Parallel (EP) introduces AllToAll",
        "AllToAll fires every MoE FFN layer",
    ],
)

# Slide 25: MoE phases diagram
add_image_slide(prs,
    title="Four phases of one MoE FFN layer",
    subtitle="Route (local) → Dispatch AllToAll → Expert compute → Combine AllToAll",
    img_path=diag("d6_moe_phases"),
)

# Slide 26
add_content_slide(prs,
    title="Expert parallel sizing constraint",
    subtitle="EP degree drives AllToAll fabric and bandwidth",
    bullets=[
        "EP=72: one domain, NVLink AllToAll",
        "EP>72: rack boundary, 6× BW penalty",
        "Keep EP ≤ 72 — hard requirement",
        "EP carves into DP dimension (EP ≤ DP)",
        "Volume: tokens × hidden × K × 2 bytes",
    ],
)

# ═══════════════════════════════════════════════
# SECTION 5: Parallelism and Design
# ═══════════════════════════════════════════════
add_transition_slide(prs, 5, "Parallelism Dimensions and Design Heuristics")

# Slide 28
add_content_slide(prs,
    title="Mapping parallelism to fabrics",
    subtitle="Total GPUs = TP × PP × DP  ·  EP carves into DP",
    bullets=[
        "TP: AllReduce every layer → MNNVL",
        "EP: AllToAll every MoE layer → MNNVL",
        "CP: K/V exchange per attention → MNNVL",
        "PP: P2P activations at stage boundary → RDMA",
        "DP: gradient AllReduce once/step → RDMA + SHARP",
    ],
)

# Slide 29: TP/PP/DP diagram
add_image_slide(prs,
    title="Worked example: TP=4, PP=2, DP=2 → 16 GPUs",
    subtitle="TP AllReduce on NVLink · PP activation P2P tolerable on RDMA · DP gradient all-reduce on RDMA",
    img_path=diag("d8_tp_pp_dp"),
)

# Slide 30
add_content_slide(prs,
    title="Memory per GPU: AdamW and ZeRO",
    subtitle="70B model, TP=4, PP=2, DP=2 — excluding activations",
    bullets=[
        "Params BF16 (TP=4, PP=2): 17.5 GB",
        "Gradients BF16: 17.5 GB",
        "AdamW FP32 states (no ZeRO): 70 GB",
        "ZeRO-1 (shards optimizer over DP): 35 GB",
        "ZeRO-3 also shards params and grads",
    ],
)

# Slide 31
add_content_slide(prs,
    title="Configurations filling one NVL72 rack",
    subtitle="Keep TP × EP ≤ 72 so heaviest collectives stay on NVLink",
    bullets=[
        "TP=8 PP=9 DP=1: deep pipeline, 72 GPUs",
        "TP=8 PP=1 DP=9: inference replicas",
        "TP=4 PP=2 DP=9: balanced 70–140B training",
        "TP=4 PP=1 DP=18: small model, high DP",
        "Scale: grow DP and PP across racks",
    ],
)

# Slide 32: closing workflow canvas
add_focal_slide(prs,
    title="Design heuristics — NVL72",
    focal_text="TP × EP ≤ 72",
    lines=[
        "Heaviest collectives must stay on NVLink (>900 GB/s)",
        "DP and PP span racks — SHARP offloads gradients",
        "C2C at ~200 GB/s — size offload, overlap with compute",
        "Verify: NVLS engaged, GPUDirect RDMA active, rail mapping correct",
    ],
)

# ─────────────────────────────────────────────
prs.save(OUT_PATH)
print(f"Saved: {OUT_PATH}  ({len(prs.slides.xml_slides)} slides)")
