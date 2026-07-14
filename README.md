# AI Stack Landscape Report

Independent, single-file HTML landscape analysis of the AI technology stack across 12 layers, silicon through vertical end-user products. Serves as both a reference document for investors and C-suite audiences, and a demonstration of technical craft.

**Last refresh:** May 26, 2026
**Canonical file:** [`src/ai_stack_unified_search_r2026-07b.html`](src/ai_stack_unified_search_r2026-07b.html)

---

## What's inside

The report is designed for a C-suite executive or investment committee evaluating where to build or invest in the AI stack. It covers:

- 12 stack layers, each with definition, market sizing, competitive landscape, subcategories, dynamics, and dependencies
- 70 sub-layers with example companies
- Strategic gaps and whitespace opportunities grouped into three funding tiers (bootstrappable, venture-scale, deep-pocketed)
- Executive summary with five key findings

---

## File map

### `src/` (canonical, current)

| File | Description |
|---|---|
| `ai_stack_unified_search_r2026-07b.html` | **Current canonical.** 12-layer report with collapsible sub-layer panels, "Updates" banner with inline fact-check corrections, company search modal, D3 knowledge graph overlay, and Total Raised or Market Cap stat for every company. |
| `ai_stack_landscape_report_v2.html` | Prior canonical. Same report content and update banner, without the search or graph. |

### `archive/` (immutable prior versions)

Preserved per the publish-then-extend discipline. Never modify; only reference.

| File | What it added |
|---|---|
| `ai_stack_landscape_report_with_sublayers.html` | v1 with sub-layer collapsible panels only, no inline corrections yet |
| `ai_stack_sublayers_diagram.html` | Standalone one-page sub-layer decomposition diagram |
| `option_A_text_search.html` | Text search variant, highlight and prev/next through the whole report |
| `option_B_structured_index.html` | Structured company search modal only, no graph |
| `option_C_knowledge_graph.html` | D3 knowledge graph only, no modal |

### `scripts/` (build tooling)

Python scripts that produce each HTML variant from the base report by injecting CSS, JS, and content blocks. Preferred over hand-editing because HTML modification token cost is roughly 3-4x lower than direct `str_replace` when many edits are needed.

### `docs/`

| File | Description |
|---|---|
| `initial_prompt.md` | Original commissioning brief that produced the report |
| `concepts.md` | Framing note on Computation / Evaluation / Abstraction, the three axes running through the stack |

---

## How to view the report

Open any HTML file directly in a modern browser. No build step, no server required. All CSS and JS are embedded. The only external dependency is Google Fonts and D3.js from a CDN (for the graph view in `ai_stack_unified_search_r2026-07b.html`).

Recommended: start with `src/ai_stack_unified_search_r2026-07b.html` and try these entry points:
- Type a company name (for example: `Anthropic`, `Cerebras`, `Cursor`) in the nav search bar
- Click `⚹ Graph View` for the force-directed knowledge graph
- Click `+ Sub-Layers` in the nav to expand all 70 sub-layers at once
- Click `+ Show` on the Updates banner at the top to see fact-check corrections

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

The company database, [`scripts/stack_db_v2.js`](scripts/stack_db_v2.js), covers ~97 companies across all 12 layers with 252 mapped relationships (compute, silicon, supplier, customer, product, competitor, partner, investor, parent).

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
