#!/usr/bin/env python3
"""Generate the SVG assets used by the profile README.

Standard library only. Output is deterministic (fixed RNG seeds), so
re-running the script produces byte-identical files.

    python3 tools/build_assets.py

Every asset is written twice (``*-dark.svg`` / ``*-light.svg``) and selected
in the README with ``<picture>`` + ``prefers-color-scheme``.
All SVGs are self-contained: no external fonts, images or scripts.
"""
from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117", "panel": "#111823", "screen": "#0a0f16",
        "border": "#2b3644", "grid": "#1d2733", "grid2": "#27323f",
        "fg": "#e6edf3", "muted": "#8b98a8", "faint": "#5d6b7b",
        "ch1": "#3ddc97", "ch2": "#f2b84b", "pcb": "#22413a",
        "chip_bg": "#17212d", "chip_fg": "#b9c6d4",
    },
    "light": {
        "bg": "#ffffff", "panel": "#f6f8fa", "screen": "#fbfcfd",
        "border": "#d0d7de", "grid": "#e7ebef", "grid2": "#d8dee4",
        "fg": "#1b2430", "muted": "#57626f", "faint": "#8793a0",
        "ch1": "#0b7a55", "ch2": "#a85d00", "pcb": "#cfe6dd",
        "chip_bg": "#eaeef2", "chip_fg": "#3a4654",
    },
}


def noise_path(x0: float, x1: float, y: float, amp: float, step: float, seed: int) -> str:
    """Band-limited-looking noise trace as an SVG polyline path."""
    rng = random.Random(seed)
    pts, x, v = [], x0, 0.0
    while x <= x1 + 1e-6:
        v = 0.35 * v + 0.65 * rng.gauss(0, 1)  # light low-pass, still spiky
        v = max(-2.4, min(2.4, v))
        pts.append(f"{x:.1f},{y + v * amp / 2.4:.1f}")
        x += step
    return "M" + " L".join(pts)


def bits_path(x0: float, y_hi: float, y_lo: float, cell: float, bits: str) -> str:
    """NRZ square wave for a bit string."""
    d, x = [], x0
    level = y_hi if bits[0] == "1" else y_lo
    d.append(f"M{x:.1f},{level:.1f}")
    for b in bits:
        new = y_hi if b == "1" else y_lo
        if new != level:
            d.append(f"V{new:.1f}")
            level = new
        x += cell
        d.append(f"H{x:.1f}")
    return " ".join(d)


def random_bits(n: int, seed: int) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice("01") for _ in range(n))


# --------------------------------------------------------------------------
# Banner
# --------------------------------------------------------------------------
def banner(theme: str) -> str:
    c = THEMES[theme]
    W, H = 1280, 320
    sx, sy, sw, sh = 700, 44, 536, 232  # scope screen
    cell = 536 / 12
    grid = []
    for i in range(1, 12):
        x = sx + i * cell
        grid.append(f'<path d="M{x:.1f},{sy}V{sy + sh}" stroke="{c["grid2"] if i == 6 else c["grid"]}"/>')
    for i in range(1, 6):
        y = sy + i * sh / 6
        grid.append(f'<path d="M{sx},{y:.1f}H{sx + sw}" stroke="{c["grid2"] if i == 3 else c["grid"]}"/>')
    # centre-line tick marks, like a real graticule
    ticks = []
    for i in range(1, 60):
        x = sx + i * cell / 5
        ticks.append(f"M{x:.1f},{sy + sh / 2 - 3}v6")
    bits = random_bits(24, 39)
    bcell = (sw - 40) / len(bits)
    bit_labels = "".join(
        f'<text x="{sx + 20 + (i + 0.5) * bcell:.1f}" y="{sy + sh - 14}" text-anchor="middle">{b}</text>'
        for i, b in enumerate(bits)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Kavin K K — Embedded Systems, Hardware Security, RTOS, Applied Cryptography</title>
<desc id="d">Banner: an oscilloscope screen showing an analog noise trace on channel 1 and the debiased bitstream derived from it on channel 2.</desc>
<defs>
  <clipPath id="screen"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="10"/></clipPath>
  <linearGradient id="sweep" x1="0" x2="1">
    <stop offset="0" stop-color="{c["ch1"]}" stop-opacity="0"/>
    <stop offset="1" stop-color="{c["ch1"]}" stop-opacity="0.16"/>
  </linearGradient>
  <style>
    .sweep {{ animation: sweep 7s linear infinite; }}
    @keyframes sweep {{ from {{ transform: translateX(-80px); }} to {{ transform: translateX({sw}px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .sweep {{ animation: none; opacity: 0; }} }}
  </style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="2"/>

<!-- PCB traces: from the title block to the scope input -->
<g fill="none" stroke="{c["pcb"]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M64,250H430l34,-34H598l40,-40H{sx}"/>
  <path d="M64,268H442l34,-34H610l22,22H{sx}"/>
  <path d="M64,286H520l30,-18"/>
  <path d="M330,32H560l44,44H{sx}"/>
</g>
<g fill="{c["bg"]}" stroke="{c["pcb"]}" stroke-width="4">
  <circle cx="64" cy="250" r="6"/><circle cx="64" cy="268" r="6"/><circle cx="64" cy="286" r="6"/>
  <circle cx="550" cy="268" r="6"/><circle cx="330" cy="32" r="6"/>
</g>

<!-- Title block -->
<text x="60" y="118" font-family="{SANS}" font-size="64" font-weight="700" fill="{c["fg"]}" letter-spacing="-1">Kavin K K</text>
<rect x="62" y="138" width="56" height="4" rx="2" fill="{c["ch1"]}"/>
<rect x="124" y="138" width="20" height="4" rx="2" fill="{c["ch2"]}"/>
<text font-family="{MONO}" font-size="19" fill="{c["muted"]}">
  <tspan x="60" y="178">Embedded Systems · Hardware Security</tspan>
  <tspan x="60" y="206">RTOS · Applied Cryptography</tspan>
</text>

<!-- Scope screen -->
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="10" fill="{c["screen"]}" stroke="{c["border"]}" stroke-width="2"/>
<g clip-path="url(#screen)">
  <g fill="none" stroke-width="1">{"".join(grid)}</g>
  <path d="{" ".join(ticks)}" stroke="{c["grid2"]}" stroke-width="1" fill="none"/>
  <rect class="sweep" x="{sx}" y="{sy}" width="80" height="{sh}" fill="url(#sweep)"/>
  <path d="{noise_path(sx + 4, sx + sw - 4, sy + 78, 40, 2.6, 34476)}" fill="none" stroke="{c["ch1"]}" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="{bits_path(sx + 20, sy + 150, sy + 190, bcell, bits)}" fill="none" stroke="{c["ch2"]}" stroke-width="2.4" stroke-linejoin="round"/>
  <g font-family="{MONO}" font-size="11" fill="{c["faint"]}">{bit_labels}</g>
</g>
<g font-family="{MONO}" font-size="12" font-weight="600">
  <text x="{sx + 14}" y="{sy + 22}" fill="{c["ch1"]}">CH1  ANALOG NOISE</text>
  <text x="{sx + 14}" y="{sy + 138}" fill="{c["ch2"]}">CH2  DEBIASED BITS</text>
  <text x="{sx + sw - 14}" y="{sy + 22}" fill="{c["faint"]}" text-anchor="end">TRIG'D</text>
</g>
<circle cx="{sx + sw - 72}" cy="{sy + 18}" r="4" fill="{c["ch1"]}"/>
</svg>
'''


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------
CW, CH = 480, 250


def chips(items: list[str], c: dict, x: float = 24, y: float = 206) -> str:
    out = []
    for label in items:
        w = len(label) * 7.25 + 18  # 12px monospace advance is ~7.2px
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{c["chip_bg"]}" stroke="{c["border"]}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["chip_fg"]}">{escape(label)}</text>'
        )
        x += w + 8
    assert x - 8 <= CW - 24, f"chips overflow: {items}"
    return "".join(out)


def card(theme: str, *, title: str, kicker: str, hook: list[str], metric: str, unit: str,
         caption: str, tech: list[str], art: str, accent: str, desc: str) -> str:
    c = THEMES[theme]
    a = c[accent]
    hook_t = "".join(f'<tspan x="24" dy="{0 if i == 0 else 18}">{escape(h)}</tspan>' for i, h in enumerate(hook))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-labelledby="t d">
<title id="t">{escape(title)}</title>
<desc id="d">{escape(desc)}</desc>
<defs><clipPath id="r"><rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="12"/></clipPath></defs>
<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}" stroke-width="2"/>
<g clip-path="url(#r)"><rect x="0" y="0" width="{CW}" height="5" fill="{a}"/>{art.format(**c, a=a)}</g>
<text x="24" y="38" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.2" fill="{c["muted"]}">{escape(kicker)}</text>
<text x="24" y="68" font-family="{SANS}" font-size="26" font-weight="700" fill="{c["fg"]}">{escape(title)}</text>
<text x="24" y="92" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{hook_t}</text>
<text x="24" y="168" font-family="{MONO}" font-size="30" font-weight="700" fill="{a}">{escape(metric)}<tspan font-size="15" font-weight="600" dx="8">{escape(unit)}</tspan></text>
<text x="24" y="188" font-family="{MONO}" font-size="12" fill="{c["faint"]}">{escape(caption)}</text>
{chips(tech, c)}
</svg>
'''


def art_phyrand() -> str:
    # noise burst feeding a short bit row
    n = noise_path(318, 456, 62, 22, 2.2, 79997)
    return (f'<path d="{n}" fill="none" stroke="{{a}}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M318,62H456" stroke="{{grid2}}" stroke-dasharray="3 4"/>')


def art_haptic() -> str:
    # two-edge timing diagram: inference posts result -> hazard task wakes
    return ('<g fill="none" stroke-linejoin="round">'
            '<path d="M318,58H366V34H456" stroke="{faint}" stroke-width="2"/>'
            '<path d="M318,92H392V68H456" stroke="{a}" stroke-width="2.4"/>'
            '<path d="M366,26V100M392,26V100" stroke="{grid2}" stroke-dasharray="3 3"/>'
            '<path d="M366,106H392M366,102v8M392,102v8" stroke="{a}" stroke-width="1.5"/></g>'
            f'<text x="379" y="124" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{{faint}}">Δt</text>')


def art_fhss() -> str:
    # time/frequency grid: one channel jammed, the hop pattern steps around it
    x0, y0, cw, ch, cols, rows = 318, 30, 17.25, 15, 8, 6
    hops = [4, 1, 5, 0, 3, 5, 1, 4]  # row per time slot; row 2 is the jammed channel
    out = [f'<rect x="{x0}" y="{y0 + 2 * ch}" width="{cols * cw:.0f}" height="{ch}" fill="{{grid2}}"/>']
    for r in range(rows + 1):
        out.append(f'<path d="M{x0},{y0 + r * ch}H{x0 + cols * cw:.0f}" stroke="{{grid2}}" stroke-width="1"/>')
    for i in range(cols + 1):
        out.append(f'<path d="M{x0 + i * cw:.1f},{y0}V{y0 + rows * ch}" stroke="{{grid2}}" stroke-width="1"/>')
    for i, r in enumerate(hops):
        out.append(f'<rect x="{x0 + i * cw + 2:.1f}" y="{y0 + r * ch + 2}" width="{cw - 4:.1f}" height="{ch - 4}" rx="2" fill="{{a}}"/>')
    out.append(f'<text x="{x0 + cols * cw - 4:.0f}" y="{y0 + 2 * ch + 11}" text-anchor="end" font-family="{MONO}" font-size="9" fill="{{muted}}">JAMMED</text>')
    return "".join(out)


def art_seclab() -> str:
    # correlation-vs-key-guess trace: flat noise, one clear peak at the right guess
    rng = random.Random(3939)
    pts, x = [], 318.0
    while x <= 456:
        y = 96 + rng.gauss(0, 3.2)
        if abs(x - 402) < 1.2:
            y = 40
        pts.append(f"{x:.1f},{y:.1f}")
        x += 2.4
    return ('<path d="M318,34V110H456" fill="none" stroke="{grid2}" stroke-width="1.5"/>'
            '<path d="M318,78H456" stroke="{grid2}" stroke-dasharray="3 4"/>'
            f'<path d="M{" L".join(pts)}" fill="none" stroke="{{a}}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<text x="412" y="46" font-family="{MONO}" font-size="10" fill="{{muted}}">key</text>')


def art_approx() -> str:
    # error-vs-area scatter with the Pareto front picked out
    front = [(332, 44), (350, 66), (374, 80), (404, 92), (440, 98)]
    rest = [(366, 48), (392, 58), (384, 72), (420, 70), (428, 84), (444, 54), (410, 46)]
    d = "M" + " L".join(f"{x},{y}" for x, y in front)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{{faint}}"/>' for x, y in rest)
    fdots = "".join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{{a}}"/>' for x, y in front)
    return ('<path d="M318,34V110H456" fill="none" stroke="{grid2}" stroke-width="1.5"/>'
            f'<path d="{d}" fill="none" stroke="{{a}}" stroke-width="1.6" stroke-linejoin="round" stroke-dasharray="4 3"/>{dots}{fdots}'
            f'<text x="456" y="122" text-anchor="end" font-family="{MONO}" font-size="9" fill="{{faint}}">area →</text>')


def art_gnss() -> str:
    # C/N0 trace: steady, then a drop at onset that crosses the alert threshold
    rng = random.Random(7410)
    pts, x = [], 318.0
    while x <= 456:
        base = 50 if x < 384 else min(92, 50 + (x - 384) * 1.5)
        pts.append(f"{x:.1f},{base + rng.gauss(0, 2.2):.1f}")
        x += 2.4
    return ('<path d="M318,34V110H456" fill="none" stroke="{grid2}" stroke-width="1.5"/>'
            '<path d="M318,74H456" stroke="{faint}" stroke-dasharray="3 4"/>'
            f'<path d="M{" L".join(pts)}" fill="none" stroke="{{a}}" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M400,34V110" stroke="{a}" stroke-width="1.2" stroke-dasharray="2 3"/>'
            '<path d="M400,34l-5,-7h10z" fill="{a}"/>'
            f'<text x="324" y="103" font-family="{MONO}" font-size="9" fill="{{faint}}">C/N0</text>')


def art_glitchsat() -> str:
    # three copies of one register bit feeding a majority voter; a dashed line crosses all three copies
    out = []
    for k, y in enumerate((34, 58, 82)):
        out.append(f'<rect x="326" y="{y}" width="34" height="18" rx="3" fill="none" stroke="{{faint}}" stroke-width="1.5"/>')
        out.append(f'<text x="343" y="{y + 13}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{{muted}}">q{k}</text>')
        out.append(f'<path d="M360,{y + 9}H392" stroke="{{faint}}" stroke-width="1.5"/>')
    out.append('<path d="M392,40L428,58V76L392,94Z" fill="none" stroke="{a}" stroke-width="2" stroke-linejoin="round"/>')
    out.append(f'<text x="406" y="71" font-family="{MONO}" font-size="9" fill="{{muted}}">maj</text>')
    out.append('<path d="M428,67H456" stroke="{a}" stroke-width="2"/>')
    out.append('<path d="M318,28L372,108" stroke="{a}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    out.append(f'<text x="318" y="122" font-family="{MONO}" font-size="9" fill="{{faint}}">one event, three copies?</text>')
    return "".join(out)


def art_sad() -> str:
    # an 8x8 block of absolute differences, a few cells highlighted, feeding a sum
    x0, y0, c = 322, 30, 10
    rng = random.Random(8810)
    out = []
    for r in range(8):
        for q in range(8):
            hot = rng.random() < 0.22
            out.append(f'<rect x="{x0 + q * c}" y="{y0 + r * c}" width="{c - 2}" height="{c - 2}" rx="1.5" '
                       f'fill="{{{"a" if hot else "grid2"}}}"/>')
    out.append('<path d="M406,70H430" stroke="{faint}" stroke-width="1.5"/>')
    out.append(f'<text x="444" y="76" text-anchor="middle" font-family="{SANS}" font-size="20" fill="{{a}}">Σ</text>')
    out.append(f'<text x="322" y="122" font-family="{MONO}" font-size="9" fill="{{faint}}">8x8 SAD</text>')
    return "".join(out)


def art_vcd() -> str:
    # three digital waveforms: a clock, a data bit and a bus
    clk = bits_path(318, 36, 50, 8.6, "1010101010101010")
    dat = bits_path(318, 66, 80, 8.6, "0011100001111000")
    bus = ('<path d="M318,96H352L356,104L352,112H318M356,104L360,96H404L408,104L404,112H360M408,104L412,96H456'
           'M412,112H456" fill="none" stroke="{a}" stroke-width="1.5" stroke-linejoin="round"/>')
    return (f'<path d="{clk}" fill="none" stroke="{{faint}}" stroke-width="1.6"/>'
            f'<path d="{dat}" fill="none" stroke="{{a}}" stroke-width="1.8"/>' + bus)


# Order here is the order of the featured grid in README.md: three flagships, then three supporting projects.
CARDS = {
    "haptic-sense": dict(
        title="Haptic-Sense", kicker="TRON CONTEST 2026 · ENTRY 34476", accent="ch2",
        hook=["Predictive obstacle-alert prototype:", "ToF + IMU, on-device NPU model,", "haptic urgency feedback."],
        metric="3.375", unit="µs", caption="worst-case preemption latency · logic analyzer",
        tech=["STM32N6", "µT-Kernel 3.0", "NPU", "TinyML"], art=art_haptic(),
        desc="Haptic-Sense: TRON Forum Programming Contest 2026 entry 34476. Predictive obstacle-alert benchtop prototype on STM32N6570-DK running µT-Kernel 3.0. Worst-case preemption latency 3.375 microseconds, measured with a logic analyzer.",
    ),
    "glitchsat": dict(
        title="GlitchSAT", kicker="FAULT ANALYSIS · MODEL ONLY", accent="ch1",
        hook=["Finds the fewest modelled bit flips", "that defeat a protection in a netlist.", "2.0 asks: does timing change that?"],
        metric="1 · 1 · 3", unit="modelled flips", caption="designs V0 / V1 / V2 · single-bit model M0",
        tech=["Python", "Yosys", "SAT", "netlists"], art=art_glitchsat(),
        desc="GlitchSAT: an open-source fault-analysis tool for gate-level netlists that searches for the smallest number of modelled bit flips that defeat a protection. Under its single-bit model M0, the three reference designs need 1, 1 and 3 modelled bit flips. These are model results, not physical glitches; version 2.0 asks whether adding timing changes the verdict on one real protected block.",
    ),
    "sad-paper": dict(
        title="Approximate SAD", kicker="RESEARCH INTERNSHIP · MANUSCRIPT", accent="ch2",
        hook=["Approximate compressor cells in an", "8x8 SAD datapath, tested inside", "real video encoders."],
        metric="x264+x265", unit="encoders", caption="Vivado + Genus synthesis · not yet published",
        tech=["Verilog", "Icarus", "C", "Python"], art=art_sad(),
        desc="Approximate SAD: research internship work on approximate compressor cells in a shared 8x8 sum-of-absolute-differences datapath for video motion estimation, synthesised and run inside the x264 and x265 encoders. Co-authored manuscript, not yet published; the repository is private.",
    ),
    "phyrand": dict(
        title="PhyRand", kicker="HARDWARE SECURITY · ENTROPY SOURCE", accent="ch1",
        hook=["Zener-diode noise, sampled and", "Von Neumann-debiased on an STM32.", "The source is not yet validated."],
        metric="7.9997", unit="bits/byte", caption="Shannon, 1 MB · same capture fails chi-square",
        tech=["STM32F401RE", "C", "FastAPI", "Fernet"], art=art_phyrand(),
        desc="PhyRand: Zener-diode noise source on an STM32F401RE with Von Neumann debiasing, a health-tested key pipeline and a file vault. A 1 MB capture has a Shannon entropy of 7.9997 bits per byte, computed with the repository's own analysis; the same capture fails a chi-square test (p = 0.0009). The noise source is unvalidated.",
    ),
    "fhss-link": dict(
        title="FHSS-Link", kicker="RF RESILIENCE · SIMULATION + RTL", accent="ch1",
        hook=["Frequency-hopping link study: breaks", "an LFSR hop schedule, then replaces it", "with a keyed SipHash engine in Verilog."],
        metric="8–9", unit="observed hops", caption="break a 16-bit LFSR hop schedule · all 65,535 seeds",
        tech=["Python", "Verilog", "C", "SymbiYosys"], art=art_fhss(),
        desc="FHSS-Link: simulation study of a frequency-hopping link under interference. An attacker model recovers a 16-bit LFSR hop schedule after 8 or 9 observed hops, exhaustively over all 65,535 seeds; a keyed SipHash-2-4 hop engine in Verilog replaces it. Simulation, RTL and host-tested C only; nothing has run on a radio.",
    ),
    "vcd-studio": dict(
        title="VCD-Studio", kicker="TOOLS · WAVEFORM VIEWER", accent="ch2",
        hook=["Waveform viewer for Verilog .vcd", "dumps in a single HTML file. Nothing", "to install, nothing uploaded."],
        metric="1", unit="HTML file", caption="0 network requests · 0 runtime dependencies",
        tech=["JavaScript", "Python", "VCD"], art=art_vcd(),
        desc="VCD-Studio: a waveform viewer for Verilog VCD dumps that is one offline HTML file, with a signal tree, cursors, search, clock measurements and a short-pulse finder, plus a standard-library Python script for toggle counts.",
    ),
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(banner(theme), encoding="utf-8")
        for name, spec in CARDS.items():
            (OUT / f"card-{name}-{theme}.svg").write_text(card(theme, **spec), encoding="utf-8")
    keep = {f"banner-{t}.svg" for t in THEMES} | {f"card-{n}-{t}.svg" for n in CARDS for t in THEMES}
    for stale in OUT.glob("*.svg"):  # cards that are no longer featured
        if stale.name not in keep:
            stale.unlink()
    print(f"wrote {len(list(OUT.glob('*.svg')))} SVGs to {OUT}")


if __name__ == "__main__":
    main()
