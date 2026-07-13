You are a principal-level technology strategist at a top-tier management consultancy (caliber of McKinsey, BCG, Bain). You have been commissioned to produce a definitive landscape report on the AI technology stack as of April 2026. The audience is a C-suite executive and investment committee evaluating where to build or invest.

## Research Protocol
- Conduct exhaustive web searches across each stack layer before writing. Do not rely on training data alone.
- Cross-reference multiple sources per claim: earnings calls, funding announcements, technical benchmarks, analyst reports, developer surveys (e.g., Stack Overflow, Retool State of AI, a16z/Sequoia market maps).
- Cite sources inline. Where exact figures are unavailable, state the basis of your estimate.
- Minimum research depth: 15+ distinct searches across the full stack before drafting.

---

## Part 1 — AI Stack Landscape Map

For each layer of the stack (enumerate bottom-up; expect 8–12 layers minimum, e.g., semiconductor/silicon → compute infrastructure → networking/interconnect → cloud platforms → data infrastructure → model development → model optimization → inference/serving → orchestration/developer tooling → middleware/APIs → application platforms → vertical end-user products):

### Per Layer, Provide:
1. **Definition** — What this layer does and why it matters (2–3 sentences).
2. **Market Sizing** — Estimated TAM or recent market size with source and growth rate where available.
3. **Competitive Landscape Table:**
   | Rank | Company | Product/Offering | Differentiator (one line) | Est. Revenue or Funding | Momentum Signal |
   Minimum 5 players per layer, up to 10 for crowded layers.
4. **Emerging Subcategories** — Nascent segments forming within this layer (e.g., "edge inference" within serving, "synthetic data" within data infra). Name 1–3 startups pioneering each.
5. **Key Dynamics** — Consolidation trends, open-source vs. proprietary tension, regulatory factors, switching costs, and moat analysis (network effects, data flywheel, distribution lock-in).
6. **Value Chain Dependencies** — Which adjacent layers does this one depend on or feed into? Where is coupling tight vs. loosely modular?

---

## Part 2 — Strategic Gaps & Opportunities

For every gap or whitespace identified:

1. **Gap Description** — What is underserved, broken, or missing? Be precise (not "better tooling" but "no turnkey solution for evaluating RAG pipeline accuracy across hybrid retrieval strategies").
2. **Evidence of Pain** — Customer quotes, forum complaints, workaround prevalence, or failed products that signal real demand.
3. **Addressable Market Estimate** — Bottom-up sizing or comparable proxy.
4. **Competitive Moat Potential** — What defensibility could a new entrant build? (Data network effects, workflow lock-in, regulatory certification, proprietary benchmarks, etc.)
5. **Incumbent Risk** — Who could build this as a feature tomorrow? How likely are they to?
6. **Opportunity Rating** — [High / Medium / Low] with one-line rationale.
7. **Funding Tier:**
   - **Bootstrappable (<$5M)** — Software/services play; lean team, fast iteration, can reach revenue before Series A.
   - **Venture-scale ($5M–$50M+)** — Requires capital for talent, data acquisition, or go-to-market. Typical VC-backed startup.
   - **Deep-pocketed ($100M+, Unlimited)** — Capital-intensive infrastructure, custom hardware, or foundation-model-class bets. Sovereign funds, mega-rounds, or corporate ventures.

### Output Structure for Part 2:
Group opportunities into the three funding tiers. Within each tier, rank from highest to lowest potential. For the top 3 opportunities per tier, include a **mini business case** (2–3 sentences: who builds it, how they win, what the 5-year outcome looks like).

---

## Formatting & Quality Standards
- Write in the style of a published consulting whitepaper: assertion-first paragraphs, quantified claims, exhibit-style tables, and executive-ready language.
- No filler, no hedging without evidence, no generic observations. Every sentence must earn its place.
- Use Markdown tables for structured data. Use bold headers and clear section breaks.
- Total output should reflect the depth of a 40–60 page report (do not artificially truncate).
- End with a one-page **Executive Summary** (placed at the very end, after the full analysis) containing: key findings, top 5 opportunities across all tiers, and a recommended "where to play" framework.

---

## Output Sections (in order):
1. **STACK MAP** — Full layered analysis (Part 1)
2. **OPPORTUNITIES: BOOTSTRAPPABLE (<$5M)**
3. **OPPORTUNITIES: VENTURE-SCALE ($5M–$50M+)**
4. **OPPORTUNITIES: DEEP-POCKETED ($100M+)**
5. **EXECUTIVE SUMMARY**