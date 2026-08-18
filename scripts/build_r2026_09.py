#!/usr/bin/env python3
"""
Build r2026-09 from r2026-08b.

Closes four audit items in one pass:
  2. Layer 03 database coverage + the 34 companies named in report tables but
     absent from the search index, plus the security vendors surfaced in Part 2
  3. Part 3 - Adoption & Realized Value (demand-side evidence)
  4. Eight-chart pack (first zero-to-one visualisation in the document)
  5. Methodology & Sources appendix + inline source links

Item 1 (value-chain dependencies) shipped in r2026-08b and is not touched here.
Publish-then-extend: writes a NEW file.
"""
import re, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from charts import (figure, hbar, column, stacked_single, grouped,
                    S1, S2, S3, S4, LAYER)

SRC = pathlib.Path("archive/ai_stack_cross_cutting_r2026-08b.html")
DST = pathlib.Path("src/ai_stack_full_r2026-09.html")
html = SRC.read_text()
applied, failed = [], []

def plain(old, new, label, count=1):
    global html
    if html.count(old) < count:
        failed.append(f"{label}: literal not found ({html.count(old)} found)"); return
    html = html.replace(old, new, count); applied.append(label)

def sub1(pattern, repl, label, flags=0):
    global html
    new, n = re.subn(pattern, repl, html, count=1, flags=flags)
    if n == 1: html = new; applied.append(label)
    else: failed.append(f"{label}: regex matched {n}")

# ══════════════════════════════════════════════════════════════
# 1. CSS
# ══════════════════════════════════════════════════════════════
CSS = """
  /* ── CHART PACK ── */
  .chart {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 1.1rem 1.2rem 1rem; margin: 0 0 1.6rem;
  }
  .chart figcaption { margin-bottom: .9rem; }
  .chart-title {
    font-family: 'Syne', sans-serif; font-size: 14.5px; font-weight: 700;
    color: #fff; line-height: 1.4; margin-bottom: .25rem;
  }
  .chart-sub { font-size: 12.5px; color: var(--muted); line-height: 1.6; }
  .chart svg.cv { width: 100%; height: auto; display: block; overflow: visible; }
  .chart-src {
    font-family: 'JetBrains Mono', monospace; font-size: 9px; color: var(--muted);
    letter-spacing: .04em; margin-top: .75rem; opacity: .8; line-height: 1.6;
  }
  .chart-data { margin-top: .8rem; }
  .chart-data summary {
    font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted); cursor: pointer; padding: .3rem 0;
  }
  .chart-data summary:hover { color: var(--accent); }
  .chart-data table { font-size: 12px; margin-top: .5rem; }
  .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
  @media(max-width: 900px) { .chart-grid { grid-template-columns: 1fr; } }
  .chart-grid .chart { margin-bottom: 0; }

  /* ── ADOPTION SECTION ── */
  .kpi-strip {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem;
  }
  @media(max-width: 860px) { .kpi-strip { grid-template-columns: repeat(2, 1fr); } }
  .kpi {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: .95rem 1.1rem;
  }
  .kpi-val {
    font-family: 'DM Serif Display', serif; font-size: 1.85rem; color: #fff;
    line-height: 1.05; margin-bottom: .3rem;
  }
  .kpi-lab {
    font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: .35rem;
  }
  .kpi-note { font-size: 11.5px; color: var(--text); line-height: 1.55; opacity: .85; }

  /* ── METHODOLOGY ── */
  .method-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-bottom: 2rem; }
  @media(max-width: 860px) { .method-grid { grid-template-columns: 1fr; } }
  .src-list { columns: 2; column-gap: 2rem; font-size: 12.5px; line-height: 1.9; }
  @media(max-width: 720px) { .src-list { columns: 1; } }
  .src-list a { color: var(--text); text-decoration: none; border-bottom: 1px solid rgba(94,231,196,0.25); }
  .src-list a:hover { color: var(--accent); border-bottom-color: var(--accent); }
  .conf-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 8.5px; font-weight: 700;
    letter-spacing: .08em; padding: .12rem .38rem; border-radius: 3px; margin-left: .4rem;
    vertical-align: middle;
  }
  .conf-a { background: rgba(94,231,196,0.14); color: var(--accent); }
  .conf-b { background: rgba(72,219,251,0.12); color: #48dbfb; }
  .conf-c { background: rgba(255,159,67,0.12); color: #ff9f43; }
  a.cite {
    color: inherit; text-decoration: none;
    border-bottom: 1px dotted rgba(94,231,196,0.45);
  }
  a.cite:hover { color: var(--accent); border-bottom-style: solid; }
</style>"""
sub1(r"</style>", CSS, "CSS block")

# ══════════════════════════════════════════════════════════════
# 2. CHARTS
# ══════════════════════════════════════════════════════════════
C = {}

# — 1. Adoption-to-value funnel (the headline demand-side chart)
C["funnel"] = figure("fig-funnel",
  "The adoption cliff: 88% use AI, 6% capture value from it",
  "Share of surveyed enterprises reaching each stage. Bar length encodes the "
  "percentage; the collapse between stage 3 and stage 5 is the finding.",
  hbar([("Use AI in ≥1 function", 88, "88%"),
        ("Use generative AI in ≥1 function", 70, "70%"),
        ("At least experimenting with agents", 62, "62%"),
        ("Scaling an agentic system", 23, "23%"),
        ("Fully scaled AI in any function", 10, "<10%"),
        ("EBIT impact >5% (“high performers”)", 6, "~6%")],
       colors=[S1]*6, highlight={0,1,2,3,4,5}),
  [["Use AI in ≥1 function","88%","Stanford AI Index 2026"],
   ["Use generative AI in ≥1 function","70%","Stanford AI Index 2026"],
   ["At least experimenting with agents","62%","McKinsey State of AI"],
   ["Scaling an agentic system","23%","McKinsey State of AI"],
   ["Fully scaled AI in any function","<10%","Stanford AI Index 2026"],
   ["EBIT impact >5%","~6%","McKinsey State of AI"]],
  ["Stage","Share","Source"],
  "Stanford HAI AI Index 2026; McKinsey State of AI (agentic era, 2026).")

# — 2. Realized value concentration
C["ebit"] = figure("fig-ebit",
  "Only 39% of enterprises attribute any EBIT impact to AI",
  "Expected versus realized return. The 171% figure is anticipated ROI from an "
  "executive survey; the 39% and 6% are self-reported outcomes.",
  hbar([("Anticipate positive agentic ROI", 171, "171% expected"),
        ("Attribute any EBIT impact to AI", 39, "39%"),
        ("EBIT impact above 5%", 6, "~6%")],
       colors=[S4, S1, S3]),
  [["Anticipate positive agentic ROI","171% (expected)","PagerDuty exec survey"],
   ["Attribute any EBIT impact","39%","McKinsey"],
   ["EBIT impact >5%","~6%","McKinsey"]],
  ["Measure","Value","Source"],
  "McKinsey State of AI 2026; PagerDuty survey of 1,000 executives. "
  "Note the first bar is an expectation, not an outcome, and is shown in a "
  "different colour for that reason.")

# — 3. Enterprise LLM spend
C["spend"] = figure("fig-spend",
  "Enterprise LLM API spend, $B",
  "The 2026 figure is a projection and is drawn dashed. Spend roughly doubled "
  "in the six months to mid-2025.",
  column([("Late 2024", 3.5, "$3.5B"), ("Mid 2025", 8.4, "$8.4B"),
          ("End 2026 (proj.)", 15.0, "$15B")],
         colors=[S1, S1, S1], dashed={2}, ylab="$B"),
  [["Late 2024","$3.5B","actual"], ["Mid 2025","$8.4B","actual"],
   ["End 2026","$15B","projected"]],
  ["Period","Spend","Basis"],
  "Menlo Ventures State of Generative AI / mid-year LLM market update.")

# — 4. Enterprise LLM API share
C["share"] = figure("fig-share",
  "Enterprise LLM API market share",
  "Production workloads, late 2025. Anthropic leads by a wider margin in "
  "enterprise API usage than in consumer mindshare.",
  stacked_single([("Anthropic", 40, S1), ("OpenAI", 27, S2),
                  ("Google", 21, S3), ("Other", 12, S4)]),
  [["Anthropic","40%"], ["OpenAI","27%"], ["Google","21%"], ["Other","12%"]],
  ["Provider","Share"],
  "Menlo Ventures Enterprise LLM Report.")

# — 5. Data-centre energy (corrected)
C["energy"] = figure("fig-energy",
  "Global data-centre electricity, TWh",
  "The dashed 2026 column is the superseded projection this report carried "
  "until entry 30. It did not materialise: actual consumption tracked far below it.",
  column([("2024", 415, "415"), ("2025 actual", 485, "485"),
          ("2026 (old proj.)", 1000, "1,000"), ("2030 IEA base", 945, "945")],
         colors=[S1, S1, S2, S1], dashed={2}, ylab="TWh"),
  [["2024","415 TWh","actual"], ["2025","485 TWh","actual"],
   ["2026","1,000 TWh","superseded projection"],
   ["2030","945 TWh","IEA base case"]],
  ["Year","Consumption","Basis"],
  "IEA Energy and AI (Apr 2026); IEA Electricity 2024 for the superseded figure.")

# — 6. Layer market sizing
LAYERS = [("12 Verticals",2500,"$2.5T",12),("11 App Platforms",315,"$315B",11),
          ("04 Cloud",1100,"$1.1T",4),("02 Compute capex",725,"$725B",2),
          ("01 Silicon",500,"$500B",1),("08 Inference",106,"$106B",8),
          ("06 Models (funding)",80,"$80B",6),("05 Data Infra",50,"$50B",5),
          ("03 Networking",20,"$20B",3),("10 Middleware",9,"$8–10B",10),
          ("09 Orchestration",7.6,"$7.6B",9),("07 MLOps",6.5,"$5–8B",7)]
C["layers"] = figure("fig-layers",
  "Market size by layer, $B",
  "Value concentrates at the ends of the stack. Figures span three orders of "
  "magnitude on a single linear scale, so the smallest layers read as slivers "
  "and their direct labels carry the value. The middle layers, where most "
  "startups get built, are the smallest markets here by a wide margin.",
  hbar([(l, v, d) for l, v, d, _ in LAYERS],
       colors=[LAYER[n] for *_, n in LAYERS]),
  [[l, d] for l, _, d, _ in LAYERS], ["Layer","Market size"],
  "Per-layer sizing as cited in Part 1; mixed bases (TAM, capex, funding) noted "
  "in each layer's Market Sizing card. Bars use the report's fixed layer palette.")

# — 7. AI security: two markets
C["sec"] = figure("fig-sec",
  "AI security is two markets, not one",
  "Conflating them is the standard error in vendor reports. AI applied to "
  "security is mature and large; securing AI itself is small and compounding fast.",
  grouped(["2026", "2032"],
          [("AI applied to security", S1, [32, 60]),
           ("Securing AI itself", S2, [1.65, 13.5])],
          disp=[["$30–35B", "~$60B est."], ["$1.65B", "$13.5B"]]),
  [["AI applied to security","2026","$30–35B (bar uses midpoint)"], ["AI applied to security","2032","~$60B (extrapolated)"],
   ["Securing AI itself","2026","$1.65B"], ["Securing AI itself","2032","$13.5B"]],
  ["Segment","Year","Size"],
  "MarketsandMarkets agentic AI security (42% CAGR); Grand View / Precedence for "
  "AI-in-cybersecurity. The 2032 AI-applied figure is extrapolated from published "
  "CAGRs and is the least firm number on this chart.")

# — 8. Labour market
C["labour"] = figure("fig-labour",
  "AI skills wage premium and job growth",
  "Jobs requiring AI skills are growing roughly eight times faster than the "
  "overall market, and command a 62% wage premium.",
  hbar([("Job growth: AI-skilled roles", 69, "+69%"),
        ("Job growth: all roles", 9, "+9%"),
        ("Wage premium, AI skills (2026)", 62, "+62%"),
        ("Wage premium, AI skills (2025)", 57, "+57%")],
       colors=[S1, S1, S3, S3]),
  [["AI-skilled role growth","+69%"], ["Total jobs market","+9%"],
   ["Wage premium 2026","+62%"], ["Wage premium 2025","+57%"]],
  ["Measure","Value"],
  "PwC 2026 Global AI Jobs Barometer, based on over one billion job "
  "advertisements across 27 countries.")

# ══════════════════════════════════════════════════════════════
# 3. Exec-summary chart pack
# ══════════════════════════════════════════════════════════════
PACK = f"""
<!-- EXEC CHART PACK -->
<section class="section" id="chartpack">
  <div class="section-label">Chart Pack</div>
  <h2>The Five Findings, in Data</h2>
  <p class="xc-intro">Six charts carrying the quantitative spine of this report.
  Each has a data table beneath it, and each names its basis. Where a bar is
  <strong>dashed, it is a projection rather than an actual</strong>.</p>
  {C['funnel']}
  <div class="chart-grid">
    {C['spend']}
    {C['share']}
  </div>
  {C['layers']}
  <div class="chart-grid">
    {C['energy']}
    {C['sec']}
  </div>
</section>
"""
sub1(r'(<!-- STACK OVERVIEW -->)', lambda m: PACK + "\n" + m.group(1), "Chart pack insert")

# ══════════════════════════════════════════════════════════════
# 4. Part 3 — Adoption & Realized Value
# ══════════════════════════════════════════════════════════════
ADOPT = f"""
<!-- ══════════════════════════════════════════
     PART 3 — ADOPTION & REALIZED VALUE
═══════════════════════════════════════════ -->
<section class="section" id="adoption">
  <div class="section-label">Part 3 — Adoption &amp; Realized Value</div>
  <h2>What Buyers Actually Did</h2>
  <p class="xc-intro">Parts 1 and 2 are supply-side: who builds what, and which
  forces cut across them. Neither answers the question an investment committee
  asks first, which is <strong>whether any of this is working for the people
  paying for it</strong>. This part is the demand side, and it is deliberately
  less flattering than the rest of the document.<br><br>The headline is a gap.
  Enterprise adoption of AI is close to universal and enterprise <em>value
  capture</em> from AI is rare. Both facts are well evidenced, they are not in
  tension, and the distance between them is the single most important number in
  this report.</p>

  <div class="kpi-strip">
    <div class="kpi">
      <div class="kpi-lab">Adoption</div>
      <div class="kpi-val">88%</div>
      <div class="kpi-note">of organisations use AI in at least one business
      function. Effectively saturated.</div>
    </div>
    <div class="kpi">
      <div class="kpi-lab">Scaled</div>
      <div class="kpi-val">&lt;10%</div>
      <div class="kpi-note">have fully scaled AI in any single function. Adoption
      is broad and shallow.</div>
    </div>
    <div class="kpi">
      <div class="kpi-lab">Any EBIT impact</div>
      <div class="kpi-val">39%</div>
      <div class="kpi-note">attribute any EBIT impact at all to AI. The majority
      cannot point to one.</div>
    </div>
    <div class="kpi">
      <div class="kpi-lab">High performers</div>
      <div class="kpi-val">~6%</div>
      <div class="kpi-note">report EBIT impact above 5%. This group captures a
      disproportionate share of total value.</div>
    </div>
  </div>

  {C['ebit']}

  <div class="layer-body">
    <div class="info-card">
      <h4>What separates the 6%</h4>
      <p>McKinsey's high performers are <strong>three times more likely to have
      fundamentally redesigned workflows</strong> around AI, and three times more
      likely to be scaling agents in a function. The differentiator is not model
      choice, spend, or technical sophistication. It is willingness to change the
      process rather than bolt AI onto the existing one. This is the single most
      actionable finding in the report for an operator, and it argues that the
      binding constraint on enterprise AI value is organisational, not
      technological.</p>
    </div>
    <div class="info-card">
      <h4>The counter-signal</h4>
      <p>Gartner projects that <strong>more than 40% of agentic AI projects will
      be cancelled by 2027</strong>, citing unclear ROI and weak governance rather
      than capability shortfalls. Read alongside the 171% ROI executives say they
      anticipate, this is an expectations problem: buyers are underwriting returns
      the deployed systems are not yet producing. For vendors this is a
      near-term revenue risk that does not show up in any ARR chart, and it is the
      demand-side reason the governance opportunities in Part 4 are rated as
      highly as they are.</p>
    </div>
  </div>

  {C['labour']}

  <div class="xc-conc">
    <div class="xc-conc-label">What this means for the investment case</div>
    <p>The supply side of this stack is priced for broad enterprise value capture
    that has not yet occurred. That does not invalidate the infrastructure thesis,
    because inference demand is real and power-constrained regardless of whether
    buyers can attribute EBIT. But it does mean <strong>the application and
    vertical layers carry more execution risk than their funding multiples
    imply</strong>, and it makes the workflow-redesign and governance layers
    structurally more attractive than a pure capability play. The 6% who capture
    value did so by changing how work happens. Whoever sells that change
    profitably is positioned better than whoever sells the model.</p>
  </div>
</section>
"""
sub1(r'(<section class="section" id="opportunities">)',
     lambda m: ADOPT + "\n" + m.group(1), "Part 3 Adoption insert")

# renumber Opportunities -> Part 4
plain('<div class="section-label">Part 3 — Strategic Gaps &amp; Opportunities</div>',
      '<div class="section-label">Part 4 — Strategic Gaps &amp; Opportunities</div>',
      "Renumber Opportunities to Part 4")
plain('the compliance-tooling opportunity in Part 3 further out than the July reading implied.',
      'the compliance-tooling opportunity in Part 4 further out than the July reading implied.',
      "Xref fix: regulation spine")
for a, b in [('the Enterprise Context Governance opportunity in Part 3',
              'the Enterprise Context Governance opportunity in Part 4'),
             ('the Agent Compliance opportunity in Part 3',
              'the Agent Compliance opportunity in Part 4'),
             ('the top-ranked opportunity in Part 3',
              'the top-ranked opportunity in Part 4')]:
    while a in html:
        html = html.replace(a, b, 1)
applied.append("Xref fixes: Part 3 -> Part 4")
plain('the governance opportunities in Part 4 are rated', 'the governance opportunities in Part 4 are rated',
      "Adoption xref (already correct)")

# ══════════════════════════════════════════════════════════════
# 5. Methodology & Sources
# ══════════════════════════════════════════════════════════════
SOURCES = [
 ("Stanford HAI AI Index 2026", "https://hai.stanford.edu/ai-index/2026-ai-index-report"),
 ("McKinsey, State of AI trust 2026", "https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-forward/state-of-ai-trust-in-2026-shifting-to-the-agentic-era"),
 ("PwC 2026 Global AI Jobs Barometer", "https://www.pwc.com/gx/en/issues/artificial-intelligence/job-barometer/2026/2026-global-ai-jobs-barometer-global-findings.pdf"),
 ("Menlo Ventures, LLM market update", "https://menlovc.com/perspective/2025-mid-year-llm-market-update/"),
 ("IEA, Energy demand from AI", "https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai"),
 ("IEA, Key Questions on Energy and AI", "https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary"),
 ("Dell'Oro, AI systems security to $8B", "https://www.delloro.com/news/ai-systems-security-market-to-rise-from-zero-to-nearly-8-b-by-2030/"),
 ("MarketsandMarkets, agentic AI security", "https://www.marketsandmarkets.com/Market-Reports/agentic-ai-security-market-97017233.html"),
 ("NVIDIA FY2026 Form 10-K", "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm"),
 ("NVIDIA FY2026 Form 10-Q (Apr 2026)", "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000052/nvda-20260426.htm"),
 ("Cerebras Q2 2026 results", "https://www.cnbc.com/2026/08/12/cerebras-cbrs-q2-earnings-report-2026.html"),
 ("CrowdStrike FY2026 Form 8-K", "https://www.sec.gov/Archives/edgar/data/0001535527/000153552726000022/crwd-20260603xex991.htm"),
 ("Palo Alto completes Protect AI acquisition", "https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-completes-acquisition-of-protect-ai"),
 ("Zenity $125M Series C", "https://www.businesswire.com/news/home/20260803963850/en/Zenity-Raises-$125-Million-to-Secure-the-Era-of-1-Billion-AI-Agents"),
 ("Gray Swan $40M Series A", "https://www.grayswan.ai/news/gray-swan-announces-series-a"),
 ("EU AI Act timeline amendments", "https://www.insideglobaltech.com/2026/05/28/eu-ai-act-update-timeline-relief-targeted-simplification-and-new-prohibitions/"),
 ("Holland & Knight, EU AI Act Aug 2026", "https://www.hklaw.com/en/insights/publications/2026/04/us-companies-face-eu-ai-acts-possible-august-2026-compliance-deadline"),
 ("CFR, AI chip export policy", "https://www.cfr.org/articles/new-ai-chip-export-policy-china-strategically-incoherent-and-unenforceable"),
 ("ERCOT large-load interconnection", "https://www.utilitydive.com/news/texas-facing-438-gw-queue-approves-initial-large-load-interconnection-pro/823367/"),
 ("ITIF, data centre water", "https://itif.org/publications/2026/07/06/the-data-center-water-problem-is-soluble/"),
 ("CSA, MCP security research note", "https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled/"),
 ("NSA, MCP security guidance", "https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf"),
 ("Arista Q2 2026 / AI networking", "https://www.nextplatform.com/connect/2026/08/10/as-ai-networks-scale-in-three-directions-so-does-arista/5285500"),
 ("Astera Labs Q1 FY2026 Form 8-K", "https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000017/q126exhibit991.htm"),
]
src_html = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a><br>'
                   for n, u in SOURCES)

METHOD = f"""
<!-- METHODOLOGY -->
<section class="section" id="methodology">
  <div class="section-label">Appendix — Methodology</div>
  <h2>How This Was Built, and What to Distrust</h2>
  <p class="xc-intro">A landscape report is only as good as its willingness to
  say where it is weak. This appendix states the method, the confidence tiers,
  and the known defects that survived this cycle.</p>

  <div class="method-grid">
    <div class="info-card">
      <h4>Method</h4>
      <p>Every quantified claim is checked against public primary sources on each
      refresh, prioritised by volatility: valuations, ARR, IPO status and
      corporate structure are re-verified every cycle; silicon roadmaps and
      sovereign policy less often. Corrections are logged in the Updates banner
      with the superseded value struck through inline and a superscript link back
      to the entry. <strong>No figure is carried forward on the strength of
      having appeared in a prior edition</strong>, which is exactly how the 1,000
      TWh energy error survived three cycles before entry 30 caught it.</p>
    </div>
    <div class="info-card">
      <h4>Confidence tiers</h4>
      <p><span class="conf-tag conf-a">A</span> Filed or disclosed: SEC filings,
      earnings calls, official press releases. Treat as fact.<br>
      <span class="conf-tag conf-b">B</span> Credible third-party estimate:
      Sacra, Menlo, Dell'Oro, IEA, analyst surveys. Directionally reliable,
      point values soft.<br>
      <span class="conf-tag conf-c">C</span> Market-sizing projection or
      extrapolation. Useful for order of magnitude only. Every TAM in Part 4 is
      tier C, and the 2032 figure in the AI-security chart is the softest number
      in the document.</p>
    </div>
  </div>

  <div class="info-card" style="margin-bottom:2rem;">
    <h4>Known defects in this edition</h4>
    <p><strong>Survey-based demand data is self-reported.</strong> The 88%, 39%
    and 6% figures in Part 3 come from executive surveys, which systematically
    over-report adoption and under-report failure. Read them as upper bounds on
    adoption and lower bounds on disappointment.<br><br>
    <strong>Market sizings use mixed bases.</strong> The layer chart places TAM,
    annual capex and annual funding on one axis because that is how the
    underlying sources report them. It is legitimate for rank order and
    misleading for arithmetic. Do not sum it.<br><br>
    <strong>Newly added companies carry structural data only.</strong> The
    companies added this cycle to close the Layer 03 and search-coverage gaps
    have verified layer placement, taglines and relationships, but financial
    stats only where a figure was verified this cycle. An empty stat is an
    absence of verified data, never an implied zero.<br><br>
    <strong>Private-company revenue is estimated.</strong> ARR figures for
    private companies derive from third-party estimators and should be treated as
    tier B throughout.</p>
  </div>

  <div class="funding-block">
    <div class="funding-block-label"><span>Primary Sources — This Cycle</span>
    <span class="src">External links open in a new tab</span></div>
    <div class="src-list">{src_html}</div>
  </div>
</section>
"""
sub1(r'(<!-- FOOTER -->)', lambda m: METHOD + "\n" + m.group(1), "Methodology insert")

# ══════════════════════════════════════════════════════════════
# 6. Inline source links on load-bearing claims
# ══════════════════════════════════════════════════════════════
CITES = [
 ("40% enterprise API share</strong> (Menlo Ventures, Dec 2025)",
  '40% enterprise API share</strong> (<a class="cite" href="https://menlovc.com/perspective/2025-mid-year-llm-market-update/" target="_blank" rel="noopener">Menlo Ventures, Dec 2025</a>)'),
 ("AI chip revenue in 2026 (Deloitte)",
  'AI chip revenue in 2026 (<a class="cite" href="https://www2.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions.html" target="_blank" rel="noopener">Deloitte</a>)'),
 ("Multi-cloud adoption reached <strong>89% of enterprises</strong> (Flexera 2026)",
  'Multi-cloud adoption reached <strong>89% of enterprises</strong> (<a class="cite" href="https://www.flexera.com/about-us/press-center" target="_blank" rel="noopener">Flexera 2026</a>)'),
]
for old, new in CITES:
    if old in html:
        html = html.replace(old, new, 1); applied.append(f"cite: {old[:34]}…")
    else:
        failed.append(f"cite not found: {old[:44]}")

# ══════════════════════════════════════════════════════════════
# 7. DATABASE: Layer 03 + missing companies + security vendors
# ══════════════════════════════════════════════════════════════
NEW = [
 # ── Layer 03 Networking (was completely empty) ──
 {"id":"arista","n":"Arista Networks","a":["anet","arista","eos"],"l":3,
  "t":"Ethernet switching and EOS software for AI back-end networks",
  "s":[["FY26 revenue outlook","$11.5B"],["AI networking target","$3.5B"],
       ["Q2 FY26","first $3B+ quarter, +37.7% YoY"]],
  "c":[{"r":"competitor","t":"cisco"},{"r":"competitor","t":"nvidia","n":"Spectrum-X"},
       {"r":"customer","t":"meta"},{"r":"customer","t":"microsoft"},
       {"r":"supplier","t":"broadcom","n":"switch silicon"}],
  "r":["Status","Public (NYSE: ANET)"]},
 {"id":"cisco","n":"Cisco","a":["cisco systems","hypershield","silicon one"],"l":3,"L":[12],
  "t":"Networking incumbent; agentic SOC and AI security via acquisition",
  "s":[["AI security M&A","Robust Intelligence, Astrix"],
       ["RSAC 2026","shipped agentic SOC tooling"]],
  "c":[{"r":"competitor","t":"arista"},{"r":"competitor","t":"nvidia"},
       {"r":"competitor","t":"crowdstrike"},{"r":"competitor","t":"palo_alto"},
       {"r":"parent","t":"astrix"},{"r":"parent","t":"robust_intelligence"}],
  "r":["Status","Public (NASDAQ: CSCO)"]},
 {"id":"astera_labs","n":"Astera Labs","a":["alab","astera","aries","taurus"],"l":3,"L":[1],
  "t":"Connectivity silicon removing bottlenecks inside AI servers",
  "s":[["2025 revenue","~$852M (+115%)"],["Q1 FY26","$308.4M (+93% YoY)"]],
  "c":[{"r":"competitor","t":"credo"},{"r":"competitor","t":"broadcom"},
       {"r":"competitor","t":"marvell"},{"r":"customer","t":"nvidia"},
       {"r":"supplier","t":"tsmc"}],
  "r":["Status","Public (NASDAQ: ALAB)"]},
 {"id":"credo","n":"Credo Technology","a":["crdo","credo","aec"],"l":3,
  "t":"Active electrical cables and optical DSPs for AI clusters",
  "s":[["FY27 growth forecast",">80%"],["FY27 optical revenue",">$600M expected"]],
  "c":[{"r":"competitor","t":"astera_labs"},{"r":"competitor","t":"marvell"},
       {"r":"competitor","t":"broadcom"}],
  "r":["Status","Public (NASDAQ: CRDO)"]},
 {"id":"cornelis","n":"Cornelis Networks","a":["omni-path","cornelis"],"l":3,
  "t":"Omni-Path high-performance fabric for HPC and AI clusters",
  "c":[{"r":"competitor","t":"nvidia","n":"InfiniBand"},{"r":"competitor","t":"arista"}],
  "r":["Total Raised","—"]},
 {"id":"drivenets","n":"DriveNets","a":["drivenets","network cloud"],"l":3,
  "t":"Disaggregated network cloud software for AI fabrics",
  "c":[{"r":"competitor","t":"arista"},{"r":"competitor","t":"cisco"}],
  "r":["Total Raised","—"]},
 {"id":"celestica","n":"Celestica","a":["cls","celestica"],"l":3,"L":[2],
  "t":"ODM for hyperscaler networking and AI hardware platforms",
  "c":[{"r":"customer","t":"meta"},{"r":"competitor","t":"arista"},
       {"r":"supplier","t":"broadcom"}],
  "r":["Status","Public (NYSE: CLS)"]},

 # ── Security vendors surfaced by Part 2 ──
 {"id":"crowdstrike","n":"CrowdStrike","a":["crwd","falcon","charlotte ai","agentworks"],"l":12,
  "t":"Agentic SOC; Charlotte AI security agents on the Falcon platform",
  "s":[["Record net-new ARR","$265M (+73% YoY)"],
       ["Module adoption","51% / 35% / 25% at 6+/7+/8+ modules"]],
  "c":[{"r":"competitor","t":"palo_alto"},{"r":"competitor","t":"microsoft"},
       {"r":"competitor","t":"cisco"},{"r":"competitor","t":"dropzone"},
       {"r":"partner","t":"anthropic"},{"r":"partner","t":"nvidia"},
       {"r":"partner","t":"openai"}],
  "r":["Status","Public (NASDAQ: CRWD)"]},
 {"id":"palo_alto","n":"Palo Alto Networks","a":["panw","prisma airs","cortex","koi"],"l":12,"L":[7],
  "t":"Prisma AIRS AI security platform, built on the Protect AI acquisition",
  "s":[["Protect AI","acquired Jul 22, 2025"],["Koi","acquired 2026, agentic endpoint"]],
  "c":[{"r":"competitor","t":"crowdstrike"},{"r":"competitor","t":"cisco"},
       {"r":"competitor","t":"check_point"},{"r":"parent","t":"protect_ai"}],
  "r":["Status","Public (NASDAQ: PANW)"]},
 {"id":"check_point","n":"Check Point","a":["chkp","check point","lakera"],"l":8,
  "t":"Network security incumbent; acquired Lakera for GenAI guardrails",
  "c":[{"r":"parent","t":"lakera"},{"r":"competitor","t":"palo_alto"},
       {"r":"competitor","t":"prompt_security"}],
  "r":["Status","Public (NASDAQ: CHKP)"]},
 {"id":"zenity","n":"Zenity","a":["zenity","agent security"],"l":9,
  "t":"Security and governance for enterprise AI agent actions",
  "s":[["Series C","$125M led by Norwest (Aug 3, 2026)"],["Employees","230+"]],
  "c":[{"r":"competitor","t":"invariant"},{"r":"competitor","t":"crowdstrike"},
       {"r":"partner","t":"microsoft","n":"Copilot Studio surface"}],
  "r":["Total Raised","~$185M"]},
 {"id":"gray_swan","n":"Gray Swan","a":["gray swan","cygnal","shade","arena"],"l":6,
  "t":"Frontier-model red teaming and pre-release safety evaluation",
  "s":[["Series A","$40M (May 28, 2026)"],["Frontier system cards","cited in 11"]],
  "c":[{"r":"customer","t":"anthropic"},{"r":"customer","t":"openai"},
       {"r":"customer","t":"meta"},{"r":"competitor","t":"irregular"}],
  "r":["Total Raised","~$40M+"]},
 {"id":"irregular","n":"Irregular","a":["irregular","pattern labs"],"l":6,
  "t":"Frontier-model security evaluation and adversarial testing",
  "c":[{"r":"competitor","t":"gray_swan"},{"r":"customer","t":"anthropic"}],
  "r":["Total Raised","—"]},
 {"id":"hiddenlayer","n":"HiddenLayer","a":["hiddenlayer","model scanner"],"l":7,
  "t":"Model artifact scanning and ML detection and response",
  "s":[["Series A","$50M (2023), led by M12"]],
  "c":[{"r":"competitor","t":"protect_ai"},{"r":"competitor","t":"palo_alto"},
       {"r":"investor","t":"microsoft","n":"M12"}],
  "r":["Total Raised","~$56M"]},
 {"id":"protect_ai","n":"Protect AI","a":["protect ai","prisma airs","modelscan"],"l":7,
  "t":"AI model supply-chain security; now Palo Alto's Prisma AIRS",
  "s":[["Acquired","Palo Alto Networks, completed Jul 22, 2025"]],
  "c":[{"r":"parent","t":"palo_alto"},{"r":"competitor","t":"hiddenlayer"}],
  "r":["Status","Acquired by Palo Alto Networks"]},
 {"id":"robust_intelligence","n":"Robust Intelligence","a":["robust intelligence"],"l":8,
  "t":"AI firewall and model validation; acquired by Cisco",
  "c":[{"r":"parent","t":"cisco"},{"r":"competitor","t":"lakera"},
       {"r":"competitor","t":"prompt_security"}],
  "r":["Status","Acquired by Cisco"]},
 {"id":"prompt_security","n":"Prompt Security","a":["prompt security"],"l":8,
  "t":"GenAI runtime security via transparent LLM traffic proxy",
  "c":[{"r":"competitor","t":"lakera"},{"r":"competitor","t":"robust_intelligence"},
       {"r":"competitor","t":"witness_ai"}],
  "r":["Total Raised","—"]},
 {"id":"witness_ai","n":"Witness AI","a":["witness ai","witnessai"],"l":11,
  "t":"Visibility and policy control over employee AI usage",
  "c":[{"r":"competitor","t":"prompt_security"},{"r":"competitor","t":"glean"}],
  "r":["Total Raised","—"]},
 {"id":"invariant","n":"Invariant Labs","a":["invariant labs","invariant"],"l":9,
  "t":"Agent security scanning and MCP vulnerability research",
  "c":[{"r":"competitor","t":"zenity"},{"r":"competitor","t":"e2b"}],
  "r":["Total Raised","—"]},
 {"id":"wiz","n":"Wiz","a":["wiz","wiz.io"],"l":4,
  "t":"Cloud security posture; AI-SPM for model and data exposure",
  "c":[{"r":"competitor","t":"palo_alto"},{"r":"competitor","t":"crowdstrike"},
       {"r":"parent","t":"google"}],
  "r":["Status","Acquired by Google (announced 2025)"]},
 {"id":"astrix","n":"Astrix Security","a":["astrix","non-human identity","nhi"],"l":4,
  "t":"Non-human and AI agent identity security; now part of Cisco",
  "s":[["Raised before acquisition","$85M"]],
  "c":[{"r":"parent","t":"cisco"},{"r":"competitor","t":"oasis_security"}],
  "r":["Status","Acquired by Cisco"]},
 {"id":"oasis_security","n":"Oasis Security","a":["oasis","nhi management"],"l":4,
  "t":"Non-human identity governance across cloud and AI agents",
  "s":[["Series B","$120M (Mar 19, 2026)"],["Cyera LOI","$1B letter of intent"]],
  "c":[{"r":"competitor","t":"astrix"},{"r":"competitor","t":"cyera"}],
  "r":["Total Raised","~$160M"]},
 {"id":"cyera","n":"Cyera","a":["cyera","dspm"],"l":5,
  "t":"Data security posture management for AI training and retrieval corpora",
  "c":[{"r":"competitor","t":"varonis"},{"r":"competitor","t":"bigid"},
       {"r":"customer","t":"oasis_security","n":"$1B LOI"}],
  "r":["Total Raised","—"]},
 {"id":"varonis","n":"Varonis","a":["vrns","varonis"],"l":5,
  "t":"Data access governance; oversharing control for enterprise copilots",
  "c":[{"r":"competitor","t":"cyera"},{"r":"competitor","t":"bigid"}],
  "r":["Status","Public (NASDAQ: VRNS)"]},
 {"id":"bigid","n":"BigID","a":["bigid"],"l":5,
  "t":"Data discovery, classification and PII governance for AI corpora",
  "c":[{"r":"competitor","t":"cyera"},{"r":"competitor","t":"varonis"}],
  "r":["Total Raised","—"]},
 {"id":"dropzone","n":"Dropzone AI","a":["dropzone","ai soc analyst"],"l":12,
  "t":"Autonomous AI SOC analyst investigating alerts end to end",
  "s":[["Total raised","$57.4M ($37M Series B)"],["Customers","100+ enterprise"]],
  "c":[{"r":"competitor","t":"prophet_security"},{"r":"competitor","t":"torq"},
       {"r":"competitor","t":"crowdstrike"}],
  "r":["Total Raised","~$57.4M"]},
 {"id":"prophet_security","n":"Prophet Security","a":["prophet security","prophet"],"l":12,
  "t":"AI SOC analyst; agent-versus-agent alert investigation",
  "s":[["Series A","$30M (Accel, Bain Capital)"]],
  "c":[{"r":"competitor","t":"dropzone"},{"r":"competitor","t":"torq"}],
  "r":["Total Raised","~$41M"]},
 {"id":"torq","n":"Torq","a":["torq","hyperautomation"],"l":12,
  "t":"AI-powered security hyperautomation, successor to SOAR",
  "c":[{"r":"competitor","t":"dropzone"},{"r":"competitor","t":"prophet_security"},
       {"r":"competitor","t":"crowdstrike"}],
  "r":["Total Raised","~$70M+"]},

 # ── Companies named in report tables but previously unsearchable ──
 {"id":"hugging_face","n":"Hugging Face","a":["hf","huggingface","transformers","hub"],"l":7,"L":[6],
  "t":"Model and dataset hub; the default distribution point for open weights",
  "s":[["Valuation","~$4.5B"]],
  "c":[{"r":"competitor","t":"github_copilot"},{"r":"partner","t":"aws"},
       {"r":"customer","t":"meta","n":"Llama distribution"},
       {"r":"competitor","t":"wandb"}],
  "r":["Total Raised","~$400M"]},
 {"id":"perplexity","n":"Perplexity","a":["perplexity ai","comet"],"l":12,"L":[11],
  "t":"AI answer engine positioned against general web search",
  "s":[["Valuation","$23B (Series E-6, Jan 2026)"],["ARR","~$450M (Mar 2026)"]],
  "c":[{"r":"competitor","t":"google"},{"r":"competitor","t":"openai"},
       {"r":"customer","t":"anthropic","n":"model access"}],
  "r":["Total Raised","—"]},
 {"id":"replit","n":"Replit","a":["replit","replit agent"],"l":9,"L":[11],
  "t":"Browser-native agentic app building for non-engineers",
  "s":[["Valuation","$9B"],["ARR","targeting $1B before end-2026"]],
  "c":[{"r":"competitor","t":"cursor"},{"r":"competitor","t":"lovable"},
       {"r":"competitor","t":"bolt"},{"r":"competitor","t":"v0"}],
  "r":["Total Raised","~$400M round (2026)"]},
 {"id":"writer","n":"Writer","a":["writer","palmyra"],"l":11,
  "t":"Full-stack enterprise generative AI platform with in-house models",
  "c":[{"r":"competitor","t":"glean"},{"r":"competitor","t":"jasper"},
       {"r":"competitor","t":"ms_copilot"}],
  "r":["Total Raised","—"]},
 {"id":"jasper","n":"Jasper","a":["jasper ai","jasper"],"l":11,
  "t":"Marketing-focused generative content platform",
  "c":[{"r":"competitor","t":"writer"},{"r":"competitor","t":"notion_ai"}],
  "r":["Total Raised","—"]},
 {"id":"notion_ai","n":"Notion AI","a":["notion","notion ai"],"l":11,
  "t":"AI layer over a workspace and knowledge base",
  "c":[{"r":"competitor","t":"glean"},{"r":"competitor","t":"workspace_ai"},
       {"r":"competitor","t":"ms_copilot"}],
  "r":["Status","Private"]},
 {"id":"mongodb","n":"MongoDB","a":["mdb","atlas","voyage ai"],"l":5,
  "t":"Operational database with native vector search via Atlas and Voyage AI",
  "s":[["Voyage AI","$220M acquisition"]],
  "c":[{"r":"competitor","t":"pinecone"},{"r":"competitor","t":"weaviate"},
       {"r":"competitor","t":"zilliz"},{"r":"competitor","t":"databricks"}],
  "r":["Status","Public (NASDAQ: MDB)"]},
 {"id":"zilliz","n":"Zilliz / Milvus","a":["zilliz","milvus"],"l":5,
  "t":"Billion-scale open-source vector database",
  "c":[{"r":"competitor","t":"pinecone"},{"r":"competitor","t":"weaviate"},
       {"r":"competitor","t":"qdrant"},{"r":"competitor","t":"chroma"}],
  "r":["Total Raised","~$113M"]},
 {"id":"chroma","n":"Chroma","a":["chroma","chromadb"],"l":5,
  "t":"Lightweight embeddable vector database, default for prototyping",
  "c":[{"r":"competitor","t":"pinecone"},{"r":"competitor","t":"qdrant"},
       {"r":"competitor","t":"zilliz"}],
  "r":["Total Raised","~$20M"]},
 {"id":"fivetran","n":"Fivetran / Airbyte","a":["fivetran","airbyte","elt"],"l":5,
  "t":"Managed and open-source ELT pipelines feeding AI data platforms",
  "c":[{"r":"partner","t":"databricks"},{"r":"partner","t":"snowflake"},
       {"r":"competitor","t":"databricks"}],
  "r":["Total Raised","—"]},
 {"id":"ibm","n":"IBM","a":["ibm","watsonx","granite"],"l":4,"L":[6],
  "t":"watsonx enterprise AI platform and Granite open model family",
  "c":[{"r":"competitor","t":"aws"},{"r":"competitor","t":"microsoft"},
       {"r":"competitor","t":"google"},{"r":"investor","t":"hiddenlayer"}],
  "r":["Status","Public (NYSE: IBM)"]},
 {"id":"alibaba_cloud","n":"Alibaba Cloud","a":["alibaba","aliyun","qwen"],"l":4,"L":[6],
  "t":"Leading China hyperscaler; Qwen open model family",
  "c":[{"r":"competitor","t":"aws"},{"r":"competitor","t":"google"},
       {"r":"competitor","t":"deepseek"}],
  "r":["Status","Public (NYSE: BABA)"]},
 {"id":"nebius","n":"Nebius","a":["nbis","nebius"],"l":2,
  "t":"European GPU cloud and AI infrastructure operator",
  "c":[{"r":"competitor","t":"coreweave"},{"r":"competitor","t":"lambda"},
       {"r":"silicon","t":"nvidia"}],
  "r":["Status","Public (NASDAQ: NBIS)"]},
 {"id":"vultr","n":"Vultr","a":["vultr"],"l":2,
  "t":"Independent GPU and cloud compute provider",
  "c":[{"r":"competitor","t":"coreweave"},{"r":"competitor","t":"runpod"},
       {"r":"silicon","t":"nvidia"}],
  "r":["Total Raised","—"]},
 {"id":"runpod","n":"RunPod","a":["runpod"],"l":2,
  "t":"Developer-first GPU cloud with per-second billing",
  "c":[{"r":"competitor","t":"vultr"},{"r":"competitor","t":"modal"},
       {"r":"silicon","t":"nvidia"}],
  "r":["Total Raised","—"]},
 {"id":"anyscale","n":"Anyscale / Ray","a":["anyscale","ray"],"l":7,
  "t":"Distributed compute framework for training and serving at scale",
  "c":[{"r":"competitor","t":"databricks"},{"r":"competitor","t":"modal"},
       {"r":"partner","t":"openai"}],
  "r":["Total Raised","—"]},
 {"id":"vllm","n":"vLLM","a":["vllm","paged attention","uc berkeley"],"l":8,
  "t":"Open-source high-throughput inference engine; de facto serving standard",
  "c":[{"r":"competitor","t":"fireworks"},{"r":"competitor","t":"together_ai"},
       {"r":"competitor","t":"baseten"}],
  "r":["Status","Open source (UC Berkeley origin)"]},
 {"id":"predibase","n":"Predibase","a":["predibase","ludwig","lora"],"l":7,
  "t":"Fine-tuning and LoRA serving infrastructure for open models",
  "c":[{"r":"competitor","t":"together_ai"},{"r":"competitor","t":"fireworks"}],
  "r":["Total Raised","—"]},
 {"id":"litellm","n":"LiteLLM","a":["litellm","llm proxy"],"l":10,
  "t":"Open-source unified proxy across 100+ model providers",
  "c":[{"r":"competitor","t":"openrouter"},{"r":"competitor","t":"portkey"}],
  "r":["Status","Open source"]},
 {"id":"mem0","n":"Mem0 / Zep","a":["mem0","zep","agent memory"],"l":10,
  "t":"Persistent memory layer for agents and assistants",
  "c":[{"r":"competitor","t":"langchain"},{"r":"competitor","t":"coconut"}],
  "r":["Total Raised","—"]},
 {"id":"zapier","n":"Zapier / Make","a":["zapier","make.com","integromat"],"l":10,
  "t":"No-code automation now repositioning as agent tool connectivity",
  "c":[{"r":"competitor","t":"relevance"},{"r":"competitor","t":"temporal"}],
  "r":["Status","Private"]},
 {"id":"relevance","n":"Relevance AI / Lindy","a":["relevance ai","lindy"],"l":9,
  "t":"No-code AI agent builders for business workflows",
  "c":[{"r":"competitor","t":"zapier"},{"r":"competitor","t":"crewai"}],
  "r":["Total Raised","—"]},
 {"id":"datadog","n":"Datadog","a":["ddog","datadog","llm observability"],"l":7,
  "t":"APM incumbent absorbing LLM observability into the main platform",
  "c":[{"r":"competitor","t":"arize"},{"r":"competitor","t":"langsmith"},
       {"r":"competitor","t":"langfuse"},{"r":"competitor","t":"helicone"}],
  "r":["Status","Public (NASDAQ: DDOG)"]},
 {"id":"ai21","n":"AI21 Labs","a":["ai21","jamba"],"l":6,
  "t":"Israeli foundation model lab; Jamba hybrid SSM-Transformer family",
  "c":[{"r":"competitor","t":"cohere"},{"r":"competitor","t":"mistral"}],
  "r":["Total Raised","—"]},
 {"id":"stability","n":"Stability AI / Black Forest Labs","a":["stability ai","black forest labs","flux","stable diffusion"],"l":6,
  "t":"Open-weight image and video generation models",
  "c":[{"r":"competitor","t":"midjourney"},{"r":"competitor","t":"runway"},
       {"r":"competitor","t":"openai"}],
  "r":["Total Raised","—"]},
 {"id":"suki","n":"Suki AI","a":["suki"],"l":12,
  "t":"Voice-first clinical documentation assistant",
  "c":[{"r":"competitor","t":"abridge"},{"r":"competitor","t":"ambience"}],
  "r":["Total Raised","—"]},
 {"id":"viz_ai","n":"Viz.ai","a":["viz ai","viz.ai"],"l":12,
  "t":"AI triage and care coordination for stroke and cardiac imaging",
  "c":[{"r":"competitor","t":"openevidence"},{"r":"competitor","t":"abridge"}],
  "r":["Total Raised","—"]},
]

i = html.index('window.STACK_DB ='); s = html.index('[', i); d = 0
for j in range(s, len(html)):
    if html[j] == '[': d += 1
    elif html[j] == ']':
        d -= 1
        if d == 0: e = j + 1; break
DB = json.loads(html[s:e])
existing = {c['id'] for c in DB}
added = [c for c in NEW if c['id'] not in existing]
DB.extend(added)

# Lakera: correct to reflect the Check Point acquisition
for c in DB:
    if c['id'] == 'lakera':
        c['t'] = "AI guardrails and prompt-injection defence; acquired by Check Point"
        c['s'] = [["Status", "Acquired by Check Point (2025)"]]
        c['r'] = ["Status", "Acquired by Check Point"]
        c.setdefault('c', []).append({"r": "parent", "t": "check_point"})

# prune any dangling targets introduced above
ids = {c['id'] for c in DB}
pruned = 0
for c in DB:
    keep = [x for x in c.get('c', []) if x['t'] in ids]
    pruned += len(c.get('c', [])) - len(keep)
    if 'c' in c: c['c'] = keep

html = html[:s] + json.dumps(DB, separators=(',', ':'), ensure_ascii=False) + html[e:]
applied.append(f"DB: +{len(added)} companies (pruned {pruned} dangling edges)")

# ══════════════════════════════════════════════════════════════
# 8. Sidebar, banner, footer
# ══════════════════════════════════════════════════════════════
plain('<a href="#crosscutting" data-target="crosscutting">Cross-Cutting</a>',
      '<a href="#chartpack" data-target="chartpack">Chart Pack</a>\n'
      '<a href="#crosscutting" data-target="crosscutting">Cross-Cutting</a>\n'
      '<a href="#adoption" data-target="adoption">Adoption &amp; ROI</a>',
      "Sidebar entries")
plain('<a href="#opportunities" data-target="opportunities">Opportunities</a>',
      '<a href="#opportunities" data-target="opportunities">Opportunities</a>\n'
      '<a href="#methodology" data-target="methodology">Methodology</a>',
      "Sidebar methodology")

BAN = """
        <div class="update-item" id="update-35">
          <div class="update-num">35</div>
          <div class="update-body">
            <div class="update-headline">Demand-side evidence added: <span class="new">88% adopt, ~6% capture EBIT value</span></div>
            <div class="update-detail">Part 3 adds the demand-side lens the report previously lacked entirely. Stanford AI Index 2026 puts enterprise adoption at <span class="new">88% in at least one function</span> but <span class="new">under 10% fully scaled in any function</span>; McKinsey finds <span class="new">only 39% attribute any EBIT impact</span> and <span class="new">~6% report impact above 5%</span>. Gartner projects <span class="new">40%+ of agentic projects cancelled by 2027</span>. This materially qualifies the supply-side valuations throughout Parts 1 and 2.</div>
            <div class="update-source">Source: Stanford HAI AI Index 2026; McKinsey State of AI 2026; PwC Global AI Jobs Barometer 2026</div>
          </div>
        </div>

        <div class="update-item" id="update-36">
          <div class="update-num">36</div>
          <div class="update-body">
            <div class="update-headline">Layer 03 database gap closed; <span class="new">+55 companies indexed</span></div>
            <div class="update-detail">Layer 03 (Networking) previously had <span class="new">zero companies</span> in the search index and knowledge graph despite eight appearing in its own competitive table, so every company modal rendered an empty row for it. Arista, Cisco, Astera Labs, Credo, Cornelis, DriveNets and Celestica are now indexed, along with companies named in report tables but previously unsearchable (Hugging Face, MongoDB, Perplexity, Replit, IBM, Datadog, vLLM and others) and the security vendors introduced in Part 2.</div>
            <div class="update-source">Source: internal database audit, Aug 17, 2026</div>
          </div>
        </div>
"""
plain('\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      BAN + '\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      "Banner entries 35-36")
plain('5 <em>material changes</em> in August 17 refresh (+29 prior)',
      '7 <em>material changes</em> in August 17 refresh (+29 prior)', "Banner headline")
plain('Entries 30&ndash;34 are the August 17, 2026 refresh cycle;',
      'Entries 30&ndash;36 are the August 17, 2026 refresh cycle;', "Banner intro")

plain('<span class="sb-date">Refreshed Aug 10</span>',
      '<span class="sb-date">Refreshed Aug 17</span>', "Suite bar date")

plain('Refreshed against publicly available information as of August 10, 2026.',
      'Refreshed against publicly available information as of August 17, 2026.',
      "Hero sub date")

plain('<div class="hero-meta-item">Layers analyzed <span>12</span></div>',
      '<div class="hero-meta-item">Layers analyzed <span>12</span></div>\n'
      '    <div class="hero-meta-item">Charts <span>8</span></div>', "Hero charts count")

FOOT = ('  <p style="margin-top:.5rem;"><strong>Additions in this build:</strong> an eight-chart pack '
 '(the document\'s first data visualisations), <strong>Part 3 &mdash; Adoption &amp; Realized Value</strong> '
 'carrying demand-side evidence from Stanford HAI, McKinsey and PwC, a <strong>Methodology appendix</strong> '
 'with confidence tiers and a stated list of known defects, inline source links, and <strong>55 companies added '
 'to the search index and knowledge graph</strong> including the entirety of Layer 03, which previously had none. '
 'Opportunities renumbered to Part 4. Chart colours were validated for colour-vision deficiency against this '
 'document\'s own dark surface; every figure ships a data table.</p>\n')
sub1(r'(  <p style="margin-top:\.5rem;">Prepared for C-Suite)', lambda m: FOOT + m.group(1), "Footer note")


# ══════════════════════════════════════════════════════════════
# 9. Review fixes
# ══════════════════════════════════════════════════════════════
# F1 — modal showed outbound edges only, so symmetric relations rendered
# differently depending on which company you opened. Resolve inbound at read time.
plain("""  var DB_MAP = {};
  DB.forEach(function(c) { DB_MAP[c.id] = c; });""",
"""  var DB_MAP = {};
  DB.forEach(function(c) { DB_MAP[c.id] = c; });

  // Symmetric relations are stored one-way in the data. Build a reverse index so
  // a modal shows the same competitor/partner set regardless of entry point.
  var SYMMETRIC = { competitor: 1, partner: 1 };
  var REVERSE = {};
  DB.forEach(function(c) {
    (c.c || []).forEach(function(x) {
      if (!SYMMETRIC[x.r]) return;
      (REVERSE[x.t] = REVERSE[x.t] || []).push({ r: x.r, t: c.id, n: x.n });
    });
  });
  function resolveConns(c) {
    var out = (c.c || []).slice(), seen = {};
    out.forEach(function(x) { seen[x.r + '|' + x.t] = 1; });
    (REVERSE[c.id] || []).forEach(function(x) {
      var k = x.r + '|' + x.t;
      if (!seen[k] && x.t !== c.id) { out.push(x); seen[k] = 1; }
    });
    return out;
  }""", "F1: symmetric-relation reverse index")
plain("    var connections = c.c || [];", "    var connections = resolveConns(c);",
      "F1: modal uses resolved connections")

# F6 — force layout was tuned for 104 nodes; labels collide at 159.
plain(".distance(60).strength(0.4))", ".distance(74).strength(0.35))", "F6: link distance")
plain("d3.forceManyBody().strength(-180)", "d3.forceManyBody().strength(-300)", "F6: charge")
plain("d3.forceCollide().radius(14)", "d3.forceCollide().radius(24)", "F6: collision radius")

# F5 — L02 headline stat contradicted its own detail text and the rest of the
# document after the Q2 2026 capex corrections in entry 20.
plain("""      <div class="stat">$650&ndash;700B</div>""",
"""      <div class="stat"><s class="old-val">$650&ndash;700B</s> <span class="new-val">~$725B</span><a class="mark" href="#update-37" title="See update 37">[37]</a></div>""",
      "F5: L02 capex headline correction")

BAN37 = """
        <div class="update-item" id="update-37">
          <div class="update-num">37</div>
          <div class="update-body">
            <div class="update-headline">Layer 02 capex headline corrected: <s>$650&ndash;700B</s> <span class="new">~$725B</span></div>
            <div class="update-detail">The Layer 02 Market Sizing headline still read <span class="new">$650&ndash;700B</span> after the Q2 2026 hyperscaler figures were corrected inline in entry 20. Its own detail text now sums to roughly <span class="new">$732B</span> (AMZN ~$220B, GOOGL $195&ndash;205B, META $130&ndash;145B, MSFT ~$175B calendar 2026), and the FinOps opportunity in Part 4 already cited ~$720&ndash;745B. The headline was the last place carrying the stale range. Found by cross-checking the new layer-sizing chart against the card it summarises.</div>
            <div class="update-source">Source: Q2 2026 hyperscaler earnings, Jul 22&ndash;30, 2026; internal consistency audit</div>
          </div>
        </div>
"""
plain('\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      BAN37 + '\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      "Banner entry 37")
plain('7 <em>material changes</em> in August 17 refresh', '8 <em>material changes</em> in August 17 refresh', "Banner headline 8")
plain('Entries 30&ndash;36 are the August 17, 2026 refresh cycle;',
      'Entries 30&ndash;37 are the August 17, 2026 refresh cycle;', "Banner intro 37")

DST.write_text(html)

# ── Suite bar: group tabs into AI / Robotics, mirroring the hub. Lives in the
# hub repo because the same patch is applied to all five reports. ──
import subprocess
_hub = pathlib.Path("/Users/aially/Desktop/Claude Code/vivekally.github.io/patch_suitebars.py")
if _hub.exists():
    r = subprocess.run(["python3", str(_hub)],
                       cwd="/Users/aially/Desktop/Claude Code", capture_output=True, text=True)
    if r.returncode == 0:
        html = DST.read_text()
        applied.append("Suite bar: AI / Robotics grouping")
    else:
        failed.append("suite bar patch: " + (r.stderr or r.stdout).strip()[:120])
else:
    failed.append("suite bar patch: patch_suitebars.py not found")

# ══════════════════════════════════════════════════════════════
# 10. Scroll-spy correctness
# ══════════════════════════════════════════════════════════════
# The spy took the LAST sidebar link whose section top was above the scroll
# position, which silently assumed sidebar order == document order. Chart Pack
# sits 2nd in the document but was listed after the 12 layers, so it won at
# every layer. Sort by document position so the nav cannot desync again.
plain("""    var sections = Object.keys(idMap).map(function(id) {
      return document.getElementById(id);
    }).filter(Boolean);""",
"""    var sections = Object.keys(idMap).map(function(id) {
      return document.getElementById(id);
    }).filter(Boolean).sort(function(a, b) {
      // Document order, not sidebar order. compareDocumentPosition is
      // layout-independent, so expanded sub-layer panels cannot perturb it.
      return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
    });""", "Scroll-spy: sort sections by document order")

# Sidebar should also *read* in the order a reader meets the sections.
plain("""<a href="#chartpack" data-target="chartpack">Chart Pack</a>\n""", "", "Sidebar: drop misplaced Chart Pack link")
plain("""<a href="#summary" data-target="summary">Executive Summary</a>""",
      """<a href="#summary" data-target="summary">Executive Summary</a>\n"""
      """<a href="#chartpack" data-target="chartpack">Chart Pack</a>""",
      "Sidebar: Chart Pack after Executive Summary")

# Guard: fail the build if the two orders ever diverge again.
_side = re.findall(r'data-target="([a-z0-9]+)"', html)
_docs = re.findall(r'<section class="[a-z\- ]*" id="([a-z0-9]+)"', html)
_docs = [d for d in _docs if d in set(_side)]
if _side != _docs:
    failed.append(f"sidebar/document order mismatch\n         sidebar: {_side}\n         document:{_docs}")
else:
    applied.append(f"Order guard: sidebar matches document ({len(_side)} sections)")

DST.write_text(html)
r = subprocess.run(["python3", str(_hub)], cwd="/Users/aially/Desktop/Claude Code",
                   capture_output=True, text=True)
if r.returncode == 0:
    applied.append("Suite bar re-applied after nav fix")

# ══════════════════════════════════════════════════════════════
# 11. Cross-Cutting: move to last (before Methodology), collapsed by default
# ══════════════════════════════════════════════════════════════
_XC_CSS = """
  .xc-toggle {
    margin: 0.4rem 0 0; display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 7px 14px; background: transparent;
    border: 1px solid rgba(94,231,196,0.3); border-radius: 3px;
    color: var(--accent); font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
    cursor: pointer; transition: all 0.2s ease;
  }
  .xc-toggle:hover { background: rgba(94,231,196,0.08); border-color: var(--accent); }
  .xc-toggle .icon { display:inline-block; transition: transform 0.2s ease; }
  .xc-toggle[aria-expanded="true"] .icon { transform: rotate(90deg); }
  .xc-toggle .label-expanded { display: none; }
  .xc-toggle[aria-expanded="true"] .label-collapsed { display: none; }
  .xc-toggle[aria-expanded="true"] .label-expanded { display: inline; }
  .xc-body { display: none; margin-top: 2rem; }
  .xc-body.open { display: block; animation: xcFade .22s ease; }
  @keyframes xcFade { from { opacity: 0; } to { opacity: 1; } }
</style>"""
sub1(r"</style>", _XC_CSS, "Cross-cutting collapse CSS")

# --- lift the section out whole ---
_s = html.index('<!-- ══════════════════════════════════════════\n     PART 2 — CROSS-CUTTING CONCERNS')
_e = html.index('</section>', html.index('<section class="section" id="crosscutting">')) + len('</section>\n')
_xc = html[_s:_e]
html = html[:_s] + html[_e:]

# --- wrap the three spines in a collapsible body + add the toggle ---
_cut = _xc.index('<div class="spine" id="xc-security"')
_head, _spines = _xc[:_cut], _xc[_cut:]
_spines = _spines.replace('</section>\n', '')
_xc = (_head
  + '<button class="xc-toggle" id="xcToggle" aria-expanded="false" aria-controls="xcBody">\n'
    '    <span class="icon">&#9656;</span>\n'
    '    <span class="label-collapsed">Show the three spines</span>\n'
    '    <span class="label-expanded">Hide the three spines</span>\n'
    '  </button>\n'
    '  <div class="xc-body" id="xcBody">\n'
  + _spines
  + '  </div>\n</section>\n')

# --- reinsert immediately before the Methodology appendix ---
_m = html.index('<!-- METHODOLOGY -->')
html = html[:_m] + _xc + '\n' + html[_m:]
applied.append("Cross-Cutting moved before Methodology, wrapped collapsed")

# --- renumber the parts, via placeholders so the swaps cannot collide ---
_num = [('Part 2 — Cross-Cutting Concerns',        '@@P4@@ — Cross-Cutting Concerns'),
        ('Part 3 — Adoption &amp; Realized Value', '@@P2@@ — Adoption &amp; Realized Value'),
        ('Part 4 — Strategic Gaps &amp; Opportunities', '@@P3@@ — Strategic Gaps &amp; Opportunities')]
for a, b in _num:
    plain(a, b, f"renumber: {a[:34]}")

# cross-references: Opportunities 4->3, Cross-Cutting 2->4, Adoption 3->2
html = html.replace('in Part 4', 'in @@P3@@')          # all point at Opportunities
html = html.replace('in Part 2', 'in @@P4@@')          # both point at Cross-Cutting
html = html.replace('figures in Part 3', 'figures in @@P2@@')
applied.append("cross-references retargeted")

# two sentences whose logic (not just numbering) assumed the old order
plain('This materially qualifies the supply-side valuations throughout Parts 1 and 2.',
      'This materially qualifies the supply-side valuations throughout the report.',
      "banner 35: drop stale part reference")
plain('Parts 1 and 2 are supply-side: who builds what, and which\n  forces cut across them. Neither answers',
      'Part 1 is supply-side: who builds what, layer by layer. It does not answer',
      "adoption intro: no longer assumes Cross-Cutting precedes it")

for ph, real in [('@@P2@@','Part 2'), ('@@P3@@','Part 3'), ('@@P4@@','Part 4')]:
    html = html.replace(ph, real)

# --- sidebar: Cross-Cutting sits before Methodology ---
plain('<a href="#crosscutting" data-target="crosscutting">Cross-Cutting</a>\n', "",
      "sidebar: drop old Cross-Cutting position")
plain('<a href="#methodology" data-target="methodology">Methodology</a>',
      '<a href="#crosscutting" data-target="crosscutting">Cross-Cutting</a>\n'
      '<a href="#methodology" data-target="methodology">Methodology</a>',
      "sidebar: Cross-Cutting before Methodology")

# --- toggle wiring ---
plain('</body>',
"""<script>
  (function() {
    var t = document.getElementById('xcToggle');
    var b = document.getElementById('xcBody');
    if (!t || !b) return;
    t.addEventListener('click', function() {
      var open = t.getAttribute('aria-expanded') === 'true';
      t.setAttribute('aria-expanded', open ? 'false' : 'true');
      b.classList.toggle('open', !open);
    });
    // A deep link or in-page jump to a collapsed spine must open it first.
    function revealIfTargeted() {
      if (!/^#xc-/.test(location.hash)) return;
      if (t.getAttribute('aria-expanded') === 'true') return;
      t.setAttribute('aria-expanded', 'true');
      b.classList.add('open');
      var el = document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView();
    }
    window.addEventListener('hashchange', revealIfTargeted);
    revealIfTargeted();
  })();
</script>
</body>""", "toggle JS")

# order guard re-run after the move
_side = re.findall(r'data-target="([a-z0-9]+)"', html)
_docs = [d for d in re.findall(r'<section class="[a-z\- ]*" id="([a-z0-9]+)"', html) if d in set(_side)]
if _side != _docs:
    failed.append(f"order mismatch after move\n         sidebar: {_side}\n         document:{_docs}")
else:
    applied.append(f"Order guard (post-move): {len(_side)} sections aligned")

DST.write_text(html)
r = subprocess.run(["python3", str(_hub)], cwd="/Users/aially/Desktop/Claude Code",
                   capture_output=True, text=True)
print("\n".join("  OK   " + a for a in applied))
if failed:
    print("\nFAILED:"); print("\n".join("  FAIL " + f for f in failed)); sys.exit(1)
print(f"\nWrote {DST} ({len(html):,} bytes)")

# ══════════════════════════════════════════════════════════════
# 12. Accurate provenance: drop "Confidential", add a disclaimer
# ══════════════════════════════════════════════════════════════
# The document called itself a "Confidential Strategy Document" while sitting
# on a public URL, and made invest/build recommendations with nothing saying it
# is not advice. Both are now stated accurately.
_DISC_CSS = """
  .disclaimer {
    border: 1px solid var(--border); border-left: 3px solid var(--accent);
    border-radius: 10px; padding: 1.25rem 1.45rem; margin-bottom: 2.2rem;
    font-family: 'Syne', sans-serif; font-size: 12.5px; line-height: 1.78;
    color: var(--muted); text-transform: none; letter-spacing: normal;
  }
  .disclaimer-label {
    font-family: 'JetBrains Mono', monospace; font-size: 9.5px; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent);
    margin-bottom: .7rem;
  }
  .disclaimer p + p { margin-top: .62rem; }
  .disclaimer strong { color: var(--text); font-weight: 700; }
  .disclaimer a {
    color: var(--accent); text-decoration: none;
    border-bottom: 1px solid rgba(94,231,196,0.35);
  }
  .disclaimer a:hover { border-bottom-color: var(--accent); }
</style>"""
sub1(r"</style>", _DISC_CSS, "Disclaimer CSS")

_DISCLAIMER = """  <div class="disclaimer">
    <div class="disclaimer-label">About this report</div>
    <p><strong>Independent and unaffiliated.</strong> This report was not commissioned,
    sponsored, or reviewed by any company named in it, and no business relationship
    exists with any of them. The analysis and any errors in it are the author's own.</p>
    <p><strong>Compiled from public sources.</strong> Figures come from publicly
    available information: regulatory filings, earnings calls, press releases and
    published research, listed in the Methodology appendix. Revenue and valuation
    figures for private companies are third-party estimates, are marked by confidence
    tier, and should be treated as approximate.</p>
    <p><strong>Not investment advice.</strong> Nothing here is a recommendation to buy,
    sell or hold any security, or to fund any company. It is written for people doing
    that work and is not a substitute for their own diligence.</p>
    <p><strong>Company names and trademarks</strong> are the property of their respective
    owners and are used here for identification and commentary.</p>
    <p><strong>Corrections welcome.</strong> If something about your company is wrong here,
    email <a href="mailto:vivekally@gmail.com">vivekally@gmail.com</a>. Corrections are
    applied in the next refresh cycle and logged in the Updates banner with the superseded
    value struck through, so the change is visible rather than silent.</p>
  </div>
"""
plain("<footer>\n", "<footer>\n" + _DISCLAIMER, "Disclaimer block in footer")

# "Confidential" was untrue on a public site; "Prepared for" implied a commission
plain('Confidential Strategy Document · Refreshed August 17, 2026',
      'Independent Research · Refreshed August 17, 2026', "hero: drop Confidential")
plain('<div class="hero-meta-item">Prepared for <span>C-Suite &amp; Investment Committee</span></div>',
      '<div class="hero-meta-item">Written for <span>C-Suite &amp; Investment Committee</span></div>',
      "hero meta: Written for")
plain('Prepared for C-Suite Executive &amp; Investment Committee &nbsp;·&nbsp; Confidential Strategy Document',
      'Written for C-Suite Executive &amp; Investment Committee &nbsp;·&nbsp; Independent research, unaffiliated',
      "footer: drop Confidential")

# two stale references in the footer prose
plain('publicly available information as of <strong>August 10, 2026</strong>',
      'publicly available information as of <strong>August 17, 2026</strong>',
      "footer: refresh date")
plain('adds <strong>Part 2 — Cross-Cutting Concerns</strong>',
      'adds <strong>Part 4 — Cross-Cutting Concerns</strong>',
      "footer: Cross-Cutting is Part 4")

DST.write_text(html)
r = subprocess.run(["python3", str(_hub)], cwd="/Users/aially/Desktop/Claude Code",
                   capture_output=True, text=True)
print("\n".join("  OK   " + a for a in applied))
if failed:
    print("\nFAILED:"); print("\n".join("  FAIL " + f for f in failed)); sys.exit(1)
print(f"\nWrote {DST} ({len(html):,} bytes)")
