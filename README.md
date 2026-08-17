# AI Stack Landscape Report

Independent, single-file HTML landscape analysis of the AI technology stack across 12 layers, silicon through vertical end-user products. Serves as both a reference document for investors and C-suite audiences, and a demonstration of technical craft.

**Last refresh:** August 17, 2026
**Canonical file:** [`src/ai_stack_full_r2026-09.html`](src/ai_stack_full_r2026-09.html)

---

## What's inside

The report is designed for a C-suite executive or investment committee evaluating where to build or invest in the AI stack. It covers:

- 12 stack layers, each with definition, market sizing, competitive landscape, subcategories, dynamics, and value-chain dependencies
- 77 sub-layers with example companies
- Three cross-cutting spines (security, regulation, energy) running vertically through all 12 layers
- Strategic gaps and whitespace opportunities grouped into three funding tiers (bootstrappable, venture-scale, deep-pocketed)
- Executive summary with five key findings

---

## File map

### `src/` (canonical, current)

| File | Description |
|---|---|
| `ai_stack_full_r2026-09.html` | **Current canonical.** 12 layers, 3 cross-cutting spines, demand-side adoption evidence, an 8-chart pack, and a methodology appendix. 159 companies / 453 relationships in the search index and knowledge graph. Banner 37 entries. |
| `ai_stack_landscape_report_v2.html` | Earliest retained edition. Same report content and update banner, without the search or graph. Kept as the plain-document reference. |

### `archive/` (immutable prior versions)

Preserved per the publish-then-extend discipline. Never modify; only reference.

| File | What it added |
|---|---|
| `ai_stack_landscape_report_with_sublayers.html` | v1 with sub-layer collapsible panels only, no inline corrections yet |
| `ai_stack_sublayers_diagram.html` | Standalone one-page sub-layer decomposition diagram |
| `option_A_text_search.html` | Text search variant, highlight and prev/next through the whole report |
| `option_B_structured_index.html` | Structured company search modal only, no graph |
| `option_C_knowledge_graph.html` | D3 knowledge graph only, no modal |
| `ai_stack_unified_search_r2026-07b.html` | July 13, 2026 refresh. Superseded by `r2026-08`; banner entries 01-19 |
| `ai_stack_unified_search_r2026-08.html` | August 10, 2026 refresh. Banner entries 01-29; 104 companies / 288 connections. Superseded by `r2026-08b` |
| `ai_stack_cross_cutting_r2026-08b.html` | Added Part 2 — Cross-Cutting Concerns and value-chain dependency blocks on all 12 layers. Banner entries 01-34. Superseded by `r2026-09` |

### `scripts/` (build tooling)

Python scripts that produce each HTML variant from the prior canonical by injecting CSS, JS, and content blocks. Preferred over hand-editing because HTML modification token cost is roughly 3-4x lower than direct `str_replace` when many edits are needed.

The chain is cumulative, and each stage reads the previous stage's output from `archive/`:

| Script | Reads | Writes |
|---|---|---|
| `build_cross_cutting.py` | `archive/ai_stack_unified_search_r2026-08.html` | `archive/ai_stack_cross_cutting_r2026-08b.html` |
| `build_r2026_09.py` | `archive/ai_stack_cross_cutting_r2026-08b.html` | `src/ai_stack_full_r2026-09.html` |
| `charts.py` | (module) | inline SVG chart pack, imported by `build_r2026_09.py` |

Chart colours are validated for colour-vision deficiency against the report's own dark surface (`#111318`) before use. Every figure ships a data table so identity is never carried by colour alone.

### `docs/`

| File | Description |
|---|---|
| `initial_prompt.md` | Original commissioning brief that produced the report |
| `concepts.md` | Framing note on Computation / Evaluation / Abstraction, the three axes running through the stack |

---

## How to view the report

Open any HTML file directly in a modern browser. No build step, no server required. All CSS and JS are embedded, and the charts are inline SVG. The only external dependencies are Google Fonts and D3.js from a CDN (for the graph view).

Recommended: start with `src/ai_stack_full_r2026-09.html` and try these entry points:
- Type a company name (for example: `Anthropic`, `Arista`, `Zenity`) in the nav search bar, or press `⌘K`
- Click `⚹ Graph View` for the force-directed knowledge graph of 159 companies
- Click `+ Sub-Layers` in the nav to expand all 77 sub-layers at once
- Click `+ Show` on the Updates banner at the top to see fact-check corrections
- Expand `Data table` beneath any chart to read the underlying figures

---

## Working conventions

- **Publish-then-extend:** completed versions are never overwritten. New features produce new files in `src/`; prior versions move to `archive/`
- **Dark theme, fixed layer palette:** never modified across versions to preserve visual continuity
- **Single-file HTML:** all CSS and JS embedded, no external dependencies beyond Google Fonts and D3
- **Volatility-tiered fact-checking:** high-churn data (valuations, ARR, IPO status) verified first every refresh
- **Update banner discipline:** every refresh cycle logs material changes with source and date, with inline strikethroughs in the report body linking back to the banner

Full working conventions and design system are in `CLAUDE.md` at the repo root.

---

## Data model (embedded database)

The company database covers **159 companies with 453 mapped relationships** (compute, silicon, supplier, customer, product, competitor, partner, investor, parent). It is embedded in the canonical HTML as `window.STACK_DB`.

Every company named in a competitive table is now indexed, and all 12 layers have coverage. Companies added in the r2026-09 pass carry verified layer placement, taglines and relationships; financial stats appear only where a figure was verified that cycle, and an empty stat means unverified rather than zero.

Each company has:
- Primary and secondary layer position
- Tagline
- Key metrics (ARR or revenue)
- Total Raised or Market Cap
- Connection list

The same database powers both the search modal and the knowledge graph.

---

## Sources

Primary and secondary sources referenced across refresh cycles:

Primary: Stanford HAI AI Index Report; State of AI Report (Nathan Benaich / Air Street Capital); McKinsey State of AI; PwC Global AI Jobs Barometer

Secondary: Menlo Ventures Enterprise LLM Report; Sacra; Crunchbase, PitchBook, Tracxn; IEA (energy); a16z and Sequoia market maps; company earnings calls and S-1 filings

---

## License

See `LICENSE` (add one appropriate for your use before making the repo public).
