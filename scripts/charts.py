#!/usr/bin/env python3
"""
Inline SVG chart pack for the AI Stack Landscape Report.

Dark-theme only, matching the report surface (#111318).
Categorical palette validated with the dataviz skill's validator against that
surface: node validate_palette.js "#3987e5,#d95926,#199e70,#c98500" --mode dark
--surface "#111318"  ->  all six checks PASS, worst adjacent CVD dE 8.4
(protan), tritan 24.4, normal-vision 19.8.

Layer-keyed charts use the report's fixed 12-colour layer palette, which
CLAUDE.md marks immutable. That is a documented design-system parameter, not a
palette choice made here.

Every figure ships a <details> data table so identity is never colour-alone.
"""

# validated categorical slots (dark surface #111318)
S1, S2, S3, S4 = "#3987e5", "#d95926", "#199e70", "#c98500"
LAYER = {1:"#ff6b6b",2:"#ff9f43",3:"#ffd32a",4:"#48dbfb",5:"#54a0ff",6:"#a29bfe",
         7:"#fd79a8",8:"#00cec9",9:"#6ab04c",10:"#badc58",11:"#e056fd",12:"#f9ca24"}

INK      = "#d4d8e2"
MUTED    = "#6b7285"
GRID     = "rgba(255,255,255,0.06)"
BASELINE = "rgba(255,255,255,0.14)"
MONO     = "'JetBrains Mono', monospace"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def figure(chart_id, title, subtitle, svg, rows, headers, source):
    """Wrap an SVG in the report's figure shell with a table view and source."""
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"""
  <figure class="chart" id="{chart_id}">
    <figcaption>
      <div class="chart-title">{title}</div>
      <div class="chart-sub">{subtitle}</div>
    </figcaption>
    {svg}
    <details class="chart-data">
      <summary>Data table</summary>
      <div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>
    </details>
    <div class="chart-src">{source}</div>
  </figure>"""


def hbar(data, unit="", width=760, row_h=30, pad_l=190, pad_r=92, colors=None,
         highlight=None):
    """Horizontal bars. data = [(label, value, display), ...]. Length encodes."""
    n = len(data)
    h = n * row_h + 26
    vmax = max(v for _, v, _ in data) or 1
    plot_w = width - pad_l - pad_r
    out = [f'<svg viewBox="0 0 {width} {h}" class="cv" role="img" '
           f'preserveAspectRatio="xMidYMid meet">']
    # recessive gridlines at quartiles
    for q in (0.25, 0.5, 0.75, 1.0):
        x = pad_l + plot_w * q
        out.append(f'<line x1="{x:.1f}" y1="6" x2="{x:.1f}" y2="{n*row_h+4}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
    for i, (label, val, disp) in enumerate(data):
        y = i * row_h + 8
        bw = max(2.0, plot_w * (val / vmax))
        c = (colors[i] if colors else S1)
        op = "1" if (highlight is None or i in highlight) else "0.5"
        out.append(f'<title>{_esc(label)}: {_esc(disp)}</title>')
        # 2px surface gap between adjacent bars via bar height < row_h
        out.append(f'<rect x="{pad_l}" y="{y}" width="{bw:.1f}" height="{row_h-12}" '
                   f'rx="4" fill="{c}" opacity="{op}"><title>{_esc(label)}: '
                   f'{_esc(disp)}</title></rect>')
        out.append(f'<text x="{pad_l-10}" y="{y+(row_h-12)/2+3.5}" text-anchor="end" '
                   f'font-family="{MONO}" font-size="10" fill="{INK}">{_esc(label)}</text>')
        out.append(f'<text x="{pad_l+bw+8:.1f}" y="{y+(row_h-12)/2+3.5}" '
                   f'font-family="{MONO}" font-size="10" fill="{MUTED}">{_esc(disp)}</text>')
    out.append(f'<line x1="{pad_l}" y1="6" x2="{pad_l}" y2="{n*row_h+4}" '
               f'stroke="{BASELINE}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


def column(data, width=760, height=250, pad_b=54, pad_t=34, pad_l=52, pad_r=18,
           colors=None, dashed=None, ylab=""):
    """Vertical columns for change-over-time. data = [(label, value, display)]."""
    n = len(data)
    vmax = max(v for _, v, _ in data) or 1
    plot_h = height - pad_b - pad_t
    plot_w = width - pad_l - pad_r
    slot = plot_w / n
    bw = min(74, slot * 0.52)
    out = [f'<svg viewBox="0 0 {width} {height}" class="cv" role="img" '
           f'preserveAspectRatio="xMidYMid meet">']
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        y = pad_t + plot_h * (1 - q)
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r}" y2="{y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{pad_l-9}" y="{y+3.5:.1f}" text-anchor="end" '
                   f'font-family="{MONO}" font-size="9" fill="{MUTED}">'
                   f'{round(vmax*q):,}</text>')
    for i, (label, val, disp) in enumerate(data):
        cx = pad_l + slot * (i + 0.5)
        bh = max(2.0, plot_h * (val / vmax))
        y = pad_t + plot_h - bh
        c = (colors[i] if colors else S1)
        extra = ' stroke-dasharray="4 3" stroke-width="1.5" fill-opacity="0.28"' \
                if (dashed and i in dashed) else ""
        stroke = f' stroke="{c}"' if (dashed and i in dashed) else ""
        out.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" '
                   f'height="{bh:.1f}" rx="4" fill="{c}"{stroke}{extra}>'
                   f'<title>{_esc(label)}: {_esc(disp)}</title></rect>')
        out.append(f'<text x="{cx:.1f}" y="{y-9:.1f}" text-anchor="middle" '
                   f'font-family="{MONO}" font-size="10.5" fill="#fff">{_esc(disp)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{height-pad_b+20:.1f}" text-anchor="middle" '
                   f'font-family="{MONO}" font-size="9.5" fill="{MUTED}">{_esc(label)}</text>')
    out.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h:.1f}" x2="{width-pad_r}" '
               f'y2="{pad_t+plot_h:.1f}" stroke="{BASELINE}" stroke-width="1"/>')
    if ylab:
        out.append(f'<text x="{pad_l}" y="16" font-family="{MONO}" font-size="9" '
                   f'fill="{MUTED}">{_esc(ylab)}</text>')
    out.append("</svg>")
    return "".join(out)


def stacked_single(segments, width=760, height=104, pad_l=2, pad_r=2):
    """One horizontal 100% bar. segments = [(label, pct, colour)]."""
    total = sum(p for _, p, _ in segments) or 100
    plot_w = width - pad_l - pad_r
    x = pad_l
    out = [f'<svg viewBox="0 0 {width} {height}" class="cv" role="img" '
           f'preserveAspectRatio="xMidYMid meet">']
    legend = []
    for label, pct, c in segments:
        w = plot_w * (pct / total)
        # 2px surface gap between segments
        out.append(f'<rect x="{x:.1f}" y="26" width="{max(2.0,w-2):.1f}" height="40" '
                   f'rx="4" fill="{c}"><title>{_esc(label)}: {pct}%</title></rect>')
        if w > 58:
            out.append(f'<text x="{x+w/2:.1f}" y="51" text-anchor="middle" '
                       f'font-family="{MONO}" font-size="11" font-weight="700" '
                       f'fill="#0a0c10">{pct}%</text>')
        legend.append((label, pct, c, x + w / 2))
        x += w
    lx = pad_l
    for label, pct, c, _ in legend:
        out.append(f'<rect x="{lx}" y="80" width="9" height="9" rx="2" fill="{c}"/>')
        out.append(f'<text x="{lx+14}" y="88.5" font-family="{MONO}" font-size="9.5" '
                   f'fill="{INK}">{_esc(label)} {pct}%</text>')
        lx += 26 + len(label) * 6.0 + 26
    out.append("</svg>")
    return "".join(out)


def grouped(cats, series, width=760, height=262, pad_b=56, pad_t=34, pad_l=58,
            pad_r=18, disp=None):
    """Grouped columns. series = [(name, colour, [values]), ...]; legend required."""
    vmax = max(max(v) for _, _, v in series) or 1
    plot_h = height - pad_b - pad_t
    plot_w = width - pad_l - pad_r
    slot = plot_w / len(cats)
    k = len(series)
    bw = min(56, (slot * 0.62) / k)
    out = [f'<svg viewBox="0 0 {width} {height}" class="cv" role="img" '
           f'preserveAspectRatio="xMidYMid meet">']
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        y = pad_t + plot_h * (1 - q)
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width-pad_r}" y2="{y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{pad_l-9}" y="{y+3.5:.1f}" text-anchor="end" '
                   f'font-family="{MONO}" font-size="9" fill="{MUTED}">'
                   f'${vmax*q:.0f}B</text>')
    for ci, cat in enumerate(cats):
        base = pad_l + slot * (ci + 0.5) - (bw * k + 2 * (k - 1)) / 2
        for si, (name, c, vals) in enumerate(series):
            v = vals[ci]
            bh = max(2.0, plot_h * (v / vmax))
            x = base + si * (bw + 2)
            y = pad_t + plot_h - bh
            lbl = (disp[si][ci] if disp else f"${v}B")
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                       f'rx="4" fill="{c}"><title>{_esc(name)} {_esc(cat)}: {_esc(lbl)}</title></rect>')
            out.append(f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle" '
                       f'font-family="{MONO}" font-size="9.5" fill="#fff">{_esc(lbl)}</text>')
        out.append(f'<text x="{pad_l+slot*(ci+0.5):.1f}" y="{height-pad_b+21:.1f}" '
                   f'text-anchor="middle" font-family="{MONO}" font-size="9.5" '
                   f'fill="{MUTED}">{_esc(cat)}</text>')
    out.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h:.1f}" x2="{width-pad_r}" '
               f'y2="{pad_t+plot_h:.1f}" stroke="{BASELINE}" stroke-width="1"/>')
    lx = pad_l
    for name, c, _ in series:
        out.append(f'<rect x="{lx}" y="{height-22}" width="9" height="9" rx="2" fill="{c}"/>')
        out.append(f'<text x="{lx+14}" y="{height-13.5}" font-family="{MONO}" '
                   f'font-size="9.5" fill="{INK}">{_esc(name)}</text>')
        lx += 24 + len(name) * 6.2
    out.append("</svg>")
    return "".join(out)
