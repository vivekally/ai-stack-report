#!/usr/bin/env python3
"""
Build r2026-08b from r2026-08.

Adds:
  1. CSS for the cross-cutting section (reuses existing design vocabulary)
  2. Value-chain dependency blocks on all 12 layers (closes the spec gap)
  3. Part 2 - Cross-Cutting Concerns (security / regulation / energy spines)
  4. Renumbers Opportunities to Part 3
  5. Sidebar entry
  6. Banner entries 30-34 with inline strikethrough corrections

Publish-then-extend: writes a NEW file, never overwrites the source.
"""
import re, sys, pathlib

SRC = pathlib.Path("archive/ai_stack_unified_search_r2026-08.html")
DST = pathlib.Path("archive/ai_stack_cross_cutting_r2026-08b.html")

html = SRC.read_text()
applied, failed = [], []

def sub1(pattern, repl, label, count=1, flags=0):
    """Replace exactly `count` occurrences; record success/failure."""
    global html
    new, n = re.subn(pattern, repl, html, count=count, flags=flags)
    if n == count:
        html = new; applied.append(f"{label} ({n})")
    else:
        failed.append(f"{label}: expected {count}, got {n}")

def plain(old, new, label, count=1):
    global html
    n = html.count(old)
    if n < count:
        failed.append(f"{label}: expected >={count} literal, got {n}"); return
    html = html.replace(old, new, count); applied.append(f"{label} ({count})")

# ─────────────────────────────────────────────────────────────
# 1. CSS
# ─────────────────────────────────────────────────────────────
CSS = """
  /* ── CROSS-CUTTING CONCERNS (Part 2) ── */
  .dep-block {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--lc, var(--accent));
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 2rem;
  }
  .dep-block-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: .8rem;
  }
  .dep-row { display: grid; grid-template-columns: 132px 1fr; gap: .9rem; padding: .45rem 0; }
  .dep-row + .dep-row { border-top: 1px solid var(--border); }
  .dep-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); padding-top: .15rem;
  }
  .dep-val { font-size: 13px; color: var(--text); line-height: 1.65; }
  .dep-val strong { color: #fff; }
  @media(max-width: 720px) {
    .dep-row { grid-template-columns: 1fr; gap: .2rem; }
  }
  .xc-intro {
    font-size: 14.5px; color: var(--text); line-height: 1.8;
    max-width: 68ch; margin-bottom: 2.4rem;
  }
  .xc-intro strong { color: #fff; }
  .spine { margin-bottom: 3.2rem; }
  .spine-head {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 1rem; flex-wrap: wrap;
    border-bottom: 1px solid var(--border); padding-bottom: .7rem; margin-bottom: 1.4rem;
  }
  .spine-head h3 {
    font-family: 'DM Serif Display', serif; font-size: 1.5rem;
    color: #fff; margin: 0;
  }
  .spine-head .spine-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; font-weight: 500; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--muted);
  }
  .xc-conc {
    background: rgba(94,231,196,0.05);
    border: 1px solid rgba(94,231,196,0.18);
    border-radius: 10px; padding: .9rem 1.2rem; margin-top: 1.2rem;
  }
  .xc-conc .xc-conc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--accent); margin-bottom: .35rem;
  }
  .xc-conc p { font-size: 13px; color: var(--text); line-height: 1.7; margin: 0; }
  .xc-table td:first-child { white-space: nowrap; }
  .xc-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.06em;
    padding: .18rem .45rem; border-radius: 4px;
  }
  .xc-thin { color: var(--muted); font-style: italic; }
</style>"""
sub1(r"</style>", CSS, "CSS block")

# ─────────────────────────────────────────────────────────────
# 2. Per-layer dependency blocks
# ─────────────────────────────────────────────────────────────
DEPS = {
 1: ("TSMC and Samsung foundry capacity, ASML EUV lithography, CoWoS advanced packaging, HBM supply from SK Hynix, Micron and Samsung.",
     "Sets the cost and availability floor for every layer above. L02 buildout timing is gated by accelerator allocation, not by capital.",
     "Hardware root of trust, confidential computing and TEEs on the accelerator itself, die and package attestation, firmware integrity. Blackwell is the first TEE-I/O capable GPU, and the throughput penalty for confidential mode fell from 30&ndash;40% to near parity, which is what moved it from research to procurement.",
     "<strong>Export controls are the binding regulatory constraint in the whole stack.</strong> A January 2026 Commerce rule reopened H200 and MI325X sales to China; late-May 2026 rules re-tightened on Blackwell, required licences for China- and Macau-headquartered entities, and closed the offshore-subsidiary loophole. No approved H200 units have actually shipped.",
     "Perf-per-watt set here compounds through every layer above. A 2&times; efficiency gain at silicon is the cheapest possible relief on the L02 power constraint."),
 2: ("L01 accelerator allocation and HBM, plus grid interconnection rights and firm generation.",
     "Capacity and $/GPU-hour ceiling for L04 and L08. Scarcity here passes straight through to token prices at L06 and L08.",
     "Tenant isolation across multi-tenant GPU fleets, GPU memory residue between tenants, BMC and firmware, physical access. Neocloud tenancy models are generally less hardened than hyperscaler equivalents, and the audit evidence gap is widening.",
     "Siting, permitting and water. More than 200 data-centre bills were introduced across all 50 states in 2025 and over 40 were enacted. DOE has proposed federal jurisdiction over new loads above 20MW to standardise approvals.",
     "<strong>The binding constraint for the entire stack.</strong> ERCOT alone received 198GW of large-load interconnection applications in Q1 2026 against a 438GW queue. Energization runs 4&ndash;7 years in major hubs and up to a decade elsewhere. Roughly 60% of hyperscaler capex is power and shells, not chips."),
 3: ("L01 interconnect silicon from Broadcom and Marvell, plus optics and transceiver supply.",
     "Caps effective cluster scale for L06 training. Tail latency introduced here surfaces directly as p99 latency at L08.",
     "East-west encryption at RDMA line rate, fabric segmentation, and materially different trust models between InfiniBand and Ethernet deployments. Encrypting at 800G without throughput loss remains expensive.",
     "Light and mostly inherited. Exposure arrives via L02 siting rules and via export controls on high-end networking equipment.",
     "Optics and switching are a rising share of rack power as clusters scale, and are one of the few places where efficiency gains are still relatively cheap."),
 4: ("L02 capacity and L03 fabric.",
     "The primary distribution channel for L06 models and the default buying surface for everything from L08 to L12.",
     "Non-human and agent identity, key management, model endpoint access control. NHI is the fastest-consolidating security category in the stack: Cisco acquired Astrix, Cyera signed a $1B letter of intent for Oasis Security, and disclosed NHI rounds passed $340M over the last year.",
     "Data residency and sovereignty. This is the clearest transmission path for EU obligations into US vendors, because residency is enforced at the cloud boundary rather than at the model.",
     "PUE and siting economics set the floor under every price above. Efficiency gains here are largely exhausted at the hyperscalers and still available at the long tail."),
 5: ("L04 storage and compute primitives.",
     "Quality ceiling for L06 training and L08 retrieval. 87% of enterprises still cite data readiness as the primary impediment to AI deployment.",
     "Training-data poisoning, provenance and lineage, and PII or PHI leakage into corpora. This is the layer the Enterprise Context Governance opportunity in Part 3 is built on.",
     "Copyright and lawful basis for training data, plus residency. Regulatory risk concentrates here more than at L06, because the exposure attaches to the corpus rather than the weights.",
     "Storage and ETL draw is small relative to L02 and is not a meaningful constraint."),
 6: ("L01 silicon and L02 capacity set the training frontier; L05 sets the data ceiling.",
     "Capability and price-per-token propagate to every layer above. Opus 5 shipping at half of Fable 5 pricing re-rates the unit economics of L08 through L12 without those layers changing anything.",
     "Weight exfiltration, dangerous-capability evaluation, and pre-release red teaming. Gray Swan raised a $40M Series A in May 2026 and sits inside the pre-release evaluation processes at OpenAI, Anthropic and Meta, cited in 11 frontier model system cards. RAND's weight-security levels are becoming the reference framework.",
     "<strong>The most actively regulated layer.</strong> EU GPAI obligations and Article 50 transparency took effect on schedule August 2, 2026. The June 2026 US Executive Order created a voluntary pre-release framework with government early access.",
     "Training runs are the largest single power events, though inference has now overtaken training in aggregate steady-state draw."),
 7: ("L06 base models and L05 evaluation data.",
     "Determines what fraction of L06 capability actually reaches L08 at acceptable cost and latency.",
     "Model artifact supply chain, unsafe deserialization, and malicious models on public hubs. The model registry is effectively an unguarded package manager. Palo Alto absorbed Protect AI into Prisma AIRS in July 2025; HiddenLayer remains independent on $56M raised.",
     "Documentation, record-keeping and third-party assessment obligations land here first whenever high-risk rules do eventually apply.",
     "Quantization and distillation are the primary demand-side lever on L02 power draw, and the only one that does not require new generation."),
 8: ("L01 inference silicon, L02 capacity, L06 weights.",
     "Sets unit economics for all of L09 through L12. This is where guardrails actually execute, so it is also where policy becomes enforceable rather than advisory.",
     "Runtime prompt injection, output filtering, redaction at the serving boundary, and token flooding. Consolidated fast: Check Point acquired Lakera and Cisco acquired Robust Intelligence, leaving Prompt Security among the few independents.",
     "Article 50 content marking and deepfake labelling are enforced at the serving boundary, which makes this the layer where EU transparency duties actually bind.",
     "Now over 55% of AI infrastructure spend and the dominant steady-state load. Inference efficiency, not training efficiency, is what determines the 2030 power curve."),
 9: ("L08 serving endpoints and L10 tool connectivity.",
     "Agent reliability here determines whether L11 and L12 products can credibly sell outcomes rather than assistance, which is the entire premise of the pricing transition in Finding 5.",
     "<strong>The fastest-moving attack surface in the stack.</strong> Agent permissions, tool-call sandboxing, egress control, human-in-loop gates. Autonomy is outpacing controls: Zenity raised a $125M Series C on August 3, 2026 explicitly against this surface.",
     "Audit trails and action logging. Both the June 2026 US EO and EU record-keeping expectations land here, which is what turned the Agent Compliance opportunity in Part 3 into a procurement gate.",
     "Negligible directly, but multiplies L08 load: a multi-step agent trace can consume 10&ndash;100&times; the tokens of a single completion."),
 10: ("L08 endpoints and L09 agent runtimes.",
      "Gateway policy and spend controls govern what L11 and L12 can safely expose to end users.",
      "<strong>MCP has no standard trust model.</strong> OX Security disclosed a systemic STDIO transport flaw in April 2026 allowing unsanitized OS command execution, with an estimated 200,000 vulnerable instances across a supply chain of 150M+ package downloads. The NSA has since published MCP security guidance, and the May 2026 enterprise-ready spec shifts responsibility to operators rather than solving it in-protocol.",
      "The natural enforcement point for both US voluntary and EU prescriptive evidence requirements, because the gateway is the only place that sees every call.",
      "Negligible."),
 11: ("L09 orchestration, L10 connectivity, L05 enterprise context.",
      "Distribution channel into the enterprise seat base. This is the surface the February 2026 SaaSpocalypse repriced.",
      "DLP for copilots, oversharing through enterprise search, and shadow AI. Oversharing is consistently the most-cited blocker to copilot rollout, and it is a permissions problem inherited from L05, not a model problem.",
      "Workplace surveillance, accessibility and employment law. Underrated exposure, because it attaches to the deploying enterprise rather than the vendor.",
      "Negligible."),
 12: ("Everything below. Most vertical vendors are thin on infrastructure and deep on workflow, which is why they are the least power-exposed and most regulation-exposed layer.",
      "Terminal layer. Where realized ROI either materialises or does not, and therefore where the demand-side evidence for the whole stack has to come from.",
      "<strong>The spine inverts here.</strong> L01 through L11 are about securing AI; L12 is where AI is sold as security. AI-native security overtook identity as the fastest-growing VC category in Q1 2026 at $4.1B, up 47% year over year.",
      "Sectoral certification per vertical is the moat named in the top-ranked opportunity in Part 3: state-by-state insurance rules, HIPAA, FINRA, FDA.",
      "Negligible."),
}
KEYS = ("Upstream", "Downstream", "Security surface", "Regulatory exposure", "Power intensity")

def dep_html(n):
    up, down, sec, reg, pw = DEPS[n]
    rows = "".join(
        f'\n      <div class="dep-row"><div class="dep-key">{k}</div><div class="dep-val">{v}</div></div>'
        for k, v in zip(KEYS, (up, down, sec, reg, pw)))
    return (f'  <div class="dep-block" style="--lc:var(--l{n})">\n'
            f'    <div class="dep-block-label">Value-Chain Dependencies &mdash; Layer {n:02d}</div>{rows}\n'
            f'  </div>\n')

for n in range(1, 13):
    pat = rf'(<section class="layer-section" id="l{n}">.*?)(  <button class="sublayer-toggle")'
    sub1(pat, lambda m, n=n: m.group(1) + dep_html(n) + m.group(2),
         f"L{n:02d} dependencies", flags=re.S)

SRC_OUT = html
pathlib.Path("/tmp/_stage1.html").write_text(html)
print("STAGE 1 OK")

# ─────────────────────────────────────────────────────────────
# 3. Part 2 - Cross-Cutting Concerns
# ─────────────────────────────────────────────────────────────
def row(n, name, concern, vendors, signal):
    return (f'        <tr><td><span class="layer-badge mono xc-badge" '
            f'style="background:rgba(255,255,255,0.06);color:var(--l{n})">{n:02d}</span></td>'
            f'<td>{concern}</td><td>{vendors}</td><td>{signal}</td></tr>\n')

SEC_ROWS = [
 (1,"Silicon","Hardware root of trust, TEEs on-accelerator, die and package attestation","NVIDIA Confidential Computing, Intel TDX, AMD SEV-SNP, Arm CCA","Blackwell is the first TEE-I/O capable GPU; confidential-mode throughput penalty fell from 30&ndash;40% to near parity"),
 (2,"Compute","Tenant isolation on shared GPU fleets, memory residue, BMC and firmware","Fortanix, Edgeless Systems, operator-native controls","Neocloud tenancy is less hardened than hyperscaler; audit evidence gap widening"),
 (3,"Networking","East-west encryption at RDMA line rate, fabric segmentation","NVIDIA BlueField DPUs, Cisco Hypershield, Arista","Encryption at 800G without throughput loss remains unsolved cheaply"),
 (4,"Cloud","Non-human and agent identity, KMS, endpoint access control","Astrix (Cisco), Oasis (Cyera $1B LOI), Entro, GitGuardian, Wiz","Fastest-consolidating category; NHI rounds passed $340M in the last year"),
 (5,"Data Infra","Training-data poisoning, provenance and lineage, PII and PHI leakage","Cyera, Varonis, BigID, Unity Catalog","Underpins the Enterprise Context Governance opportunity in Part 3"),
 (6,"Models","Weight exfiltration, dangerous-capability evals, pre-release red teaming","Gray Swan, Irregular, Haize Labs, lab-internal","Gray Swan $40M Series A (May 2026); cited in 11 frontier model system cards"),
 (7,"MLOps","Model artifact supply chain, unsafe deserialization, malicious hub models","HiddenLayer, Prisma AIRS (ex-Protect AI), JFrog ML","Protect AI absorbed by Palo Alto Jul 2025; HiddenLayer independent on $56M"),
 (8,"Inference","Runtime prompt injection, output filtering, redaction, token flooding","Prompt Security, Lakera (Check Point), Robust Intelligence (Cisco)","Two of the three leading independents acquired; this layer is now platform-owned"),
 (9,"Orchestration","Agent permissions, tool-call sandboxing, egress control, human-in-loop gates","Zenity, Invariant Labs, E2B, Browserbase","Zenity $125M Series C (Aug 3, 2026); capital still backing independents here"),
 (10,"Middleware","MCP server trust and authn, gateway policy, spend limits as a control","Cloudflare AI Gateway, Portkey, Kong","OX Security disclosed ~200,000 vulnerable MCP instances (Apr 2026); NSA guidance since issued"),
 (11,"App Platforms","DLP for copilots, oversharing via enterprise search, shadow AI","Microsoft Purview, Netskope, Island, Witness AI","Oversharing is the most-cited blocker to copilot rollout; a permissions problem, not a model problem"),
 (12,"Verticals","<strong>AI applied to security operations</strong> &mdash; detection, triage, response","CrowdStrike Charlotte, Microsoft Security Copilot, Dropzone, Prophet, Torq","Dropzone $57.4M / 100+ enterprise customers; Prophet $41M; all three majors shipped agentic SOC at RSAC 2026"),
]
REG_ROWS = [
 (1,"Silicon","Export controls, entity lists, fab and tooling restrictions","Jan 2026 Commerce rule reopened H200 / MI325X to China; late-May 2026 rules re-tightened on Blackwell and closed the offshore-subsidiary loophole","Chinese vendors took ~41% of China's AI accelerator server market in 2025, up from NVIDIA's ~95% share in 2022 (IDC)"),
 (2,"Compute","Siting, permitting, water disclosure, large-load interconnection","200+ state data-centre bills in 2025, 40+ enacted; DOE proposed federal jurisdiction over loads above 20MW","Regulatory risk is now local and political, not federal"),
 (3,"Networking","Export controls on high-end networking equipment","Inherited from L01 and L02","Low direct exposure"),
 (4,"Cloud","Data residency and sovereignty","EU residency requirements enforced at the cloud boundary","The main transmission path for EU obligations into US vendors"),
 (5,"Data Infra","Copyright, lawful basis for training data, residency","Active litigation across jurisdictions","Exposure attaches to the corpus, not the weights, so it concentrates here rather than at L06"),
 (6,"Models","GPAI obligations, transparency, pre-release evaluation","<strong>EU Article 50 and GPAI enforcement took effect Aug 2, 2026 as scheduled.</strong> High-risk obligations deferred: Annex III to Dec 2027, Annex I to Aug 2028 (Parliament vote, Jun 16, 2026)","US June 2026 EO is voluntary and access-based; the two regimes are diverging in kind, not just in degree"),
 (7,"MLOps","Documentation, record-keeping, third-party assessment","Lands here first when high-risk rules apply","Deferred to Dec 2027, which removes near-term urgency"),
 (8,"Inference","Content marking, deepfake labelling, output disclosure","Article 50 enforced at the serving boundary, live now","The one EU obligation with immediate teeth"),
 (9,"Orchestration","Audit trails, action logging, human oversight","June 2026 US EO and EU record-keeping both land here","Turned agent governance evidence into a procurement gate"),
 (10,"Middleware","Policy enforcement and evidence generation","Natural enforcement point for both regimes","The gateway is the only component that sees every call"),
 (11,"App Platforms","Workplace surveillance, accessibility, employment law","Attaches to the deploying enterprise, not the vendor","Underrated; rarely appears in vendor risk registers"),
 (12,"Verticals","Sectoral certification per vertical","State-by-state insurance, HIPAA, FINRA, FDA","The moat named in the top-ranked opportunity in Part 3"),
]
ENE_ROWS = [
 (1,"Silicon","Wafer and advanced-packaging capacity; perf-per-watt","CoWoS allocation, HBM supply","Every efficiency gain here compounds through all 11 layers above"),
 (2,"Compute","<strong>Grid interconnection, firm generation, water, shells</strong>","ERCOT took 198GW of large-load applications in Q1 2026 against a 438GW queue","Energization runs 4&ndash;7 years in major hubs, up to a decade elsewhere. ~60% of hyperscaler capex is power and shells"),
 (3,"Networking","Optics and switching power draw","Rising share of rack power as clusters scale","One of the few remaining cheap efficiency levers"),
 (4,"Cloud","PUE, siting economics, cooling","Hyperscaler PUE gains largely exhausted; long tail still has headroom","Sets the floor under every price above"),
 (5,"Data Infra","Storage and ETL draw","Small relative to L02","<span class=\"xc-thin\">Not a binding constraint</span>"),
 (6,"Models","Training-run power events","Largest single events, but inference has overtaken training in aggregate","Training is the headline; inference is the curve"),
 (7,"MLOps","Quantization and distillation as demand-side levers","The only relief that does not require new generation","<span class=\"xc-thin\">Lever, not a constraint</span>"),
 (8,"Inference","<strong>Steady-state token-serving load</strong>","Now over 55% of AI infrastructure spend","Inference efficiency, not training efficiency, determines the 2030 power curve"),
 (9,"Orchestration","Multi-step agent traces multiply L08 draw","A single agent trace can consume 10&ndash;100&times; the tokens of one completion","<span class=\"xc-thin\">Indirect multiplier</span>"),
 (10,"Middleware","Routing and caching as efficiency levers","Semantic caching and cheap-model routing","<span class=\"xc-thin\">Lever, not a constraint</span>"),
 (11,"App Platforms","None material","&mdash;","<span class=\"xc-thin\">Not a binding constraint</span>"),
 (12,"Verticals","None material","&mdash;","<span class=\"xc-thin\">Not a binding constraint</span>"),
]

def spine(anchor, tag, title, sizing_h, sizing, dyn, rows, conc, hdr3="Who sells here"):
    body = "".join(row(n, nm, c, v, s) for n, nm, c, v, s in rows)
    return f"""
  <div class="spine" id="{anchor}">
    <div class="spine-head">
      <h3>{title}</h3>
      <span class="spine-tag">{tag}</span>
    </div>
    <div class="layer-body">
      <div class="info-card">
        <h4>Market Sizing</h4>
        <div class="stat">{sizing_h}</div>
        <p>{sizing}</p>
      </div>
      <div class="info-card">
        <h4>Key Dynamics</h4>
        <p>{dyn}</p>
      </div>
    </div>
    <div class="table-wrap">
      <table class="xc-table">
        <thead><tr><th>Layer</th><th>Exposure at this altitude</th><th>{hdr3}</th><th>Signal</th></tr></thead>
        <tbody>
{body}        </tbody>
      </table>
    </div>
    <div class="xc-conc">
      <div class="xc-conc-label">Where value concentrates</div>
      <p>{conc}</p>
    </div>
  </div>
"""

XC = f"""
<!-- ══════════════════════════════════════════
     PART 2 — CROSS-CUTTING CONCERNS
═══════════════════════════════════════════ -->
<section class="section" id="crosscutting">
  <div class="section-label">Part 2 — Cross-Cutting Concerns</div>
  <h2>Three Spines Through the Stack</h2>
  <p class="xc-intro">Part 1 reads the stack by altitude: each layer consumes the one below and supplies the one above. Three forces do not respect that structure. <strong>Security, regulation and energy cut vertically through all twelve layers</strong>, and none of them can be located at a single altitude. Treating any of them as a thirteenth layer would be a category error, because a layer is defined by what it consumes and what it supplies, and these consume and supply at every level at once.<br><br>Each spine below is the stack transposed: one row per layer, read top to bottom. The pattern each one traces is the finding. Security runs as a defensive concern from L01 to L11 and then <strong>inverts at L12</strong>, where AI is sold as security rather than secured. Regulation concentrates at the two ends and thins in the middle. Energy binds hard at the bottom four layers and is close to irrelevant above them, which is itself worth seeing at a glance rather than asserting.</p>

{spine("xc-security", "Spine 01", "Security &amp; Trust",
  "$1.65B &rarr; $13.5B",
  "Two markets, not one, and conflating them is the standard error. <strong>AI applied to security</strong> is mature at roughly $30&ndash;35B in 2026. <strong>Securing AI itself</strong> is far smaller and far faster: MarketsandMarkets puts agentic AI security at $1.65B in 2026 reaching $13.5B by 2032 (42% CAGR), while Dell'Oro sizes AI systems security at close to $8B by 2030 from a standing start in 2024.",
  "<strong>Consolidation is running ahead of category formation.</strong> Palo Alto absorbed Protect AI, Check Point took Lakera, Cisco took both Robust Intelligence and Astrix, and Cyera signed a $1B letter of intent for Oasis. Independents are being acquired before reaching scale, which implies the durable position in most of this spine is a feature inside a platform rather than a standalone product. The exception is the agent layer, where Zenity's $125M Series C in August 2026 shows capital still funding independents. For an investor the read is straightforward: at L07 and L08 you are underwriting an acqui-exit, at L09 and L12 you are still underwriting a company.",
  SEC_ROWS,
  "<strong>L04, L09 and L12.</strong> Identity (L04) and agent control (L09) are the two surfaces where enterprises are actively writing cheques and where no incumbent yet owns the category. L12 is a genuine vertical with real revenue. Everything else is either already absorbed into platform vendors (L07, L08) or inherited from general infrastructure security (L02, L03), and should be priced as a feature rather than a market.")}

{spine("xc-regulation", "Spine 02", "Regulation &amp; Governance",
  "Two diverging regimes",
  "Not a market so much as a procurement gate and a compliance cost. The adjacent GRC software market is roughly $15B. The material fact for 2026 is <strong>divergence in kind</strong>: the US June 2026 Executive Order is voluntary and access-based, while the EU is prescriptive. Any vendor selling into both now needs dual-regime evidence, and nobody produces it off the shelf.",
  "<strong>The EU timeline just moved, and it moved in the direction that reduces near-term pressure.</strong> On June 16, 2026 the European Parliament deferred most high-risk obligations: Annex III use-based duties slip from August 2026 to December 2027, and Annex I product-regulated duties from August 2027 to August 2028. What did take effect on schedule on August 2, 2026 is Article 50 transparency and AI Office enforcement over general-purpose models. The practical consequence is that near-term obligations are about disclosure and GPAI, not high-risk certification, which pushes the compliance-tooling opportunity in Part 3 further out than the July reading implied.",
  REG_ROWS,
  "<strong>L01 and L06, with a long tail at L12.</strong> Export controls at silicon are the highest-consequence regulatory force in the stack and the one this report has historically under-covered. L06 carries the live EU obligations. L12 carries sectoral certification, which is a moat rather than a cost. The middle of the stack (L03, L07, L10) is largely regulated by inheritance.",
  hdr3="What applies")}

{spine("xc-energy", "Spine 03", "Energy &amp; Physical Constraints",
  "~485 &rarr; ~945 TWh",
  "Global data-centre electricity consumption was approximately <strong>485 TWh in 2025</strong>, and the IEA base case projects roughly <strong>945 TWh by 2030</strong>, about 3% of global electricity, up from 1.5% in 2024. Accelerated servers grow near 30% annually against 9% for conventional servers and account for close to half the net increase. <em>This corrects the 1,000 TWh-in-2026 figure carried in prior editions, which was a 2024-vintage projection that did not materialise.</em>",
  "<strong>The constraint is interconnection, not generation.</strong> There is no shortage of prospective electrons; there is a shortage of approved connections and delivery timelines. ERCOT alone received 198GW of large-load applications in Q1 2026 against a 438GW queue, energization runs 4&ndash;7 years in major hubs, and DOE has moved to assert federal jurisdiction over loads above 20MW specifically to compress that. This is why Amazon can state that $220B of 2026 capex still will not meet demand: capital is not the binding input.",
  ENE_ROWS,
  "<strong>L01 through L04 only.</strong> The thinness of the top eight rows is the finding, not a gap in the research. Physical constraints bind at the bottom of the stack and are close to irrelevant above L04, which is precisely why application-layer companies can scale without capital intensity while infrastructure companies cannot. The one exception worth watching is L08 and L09: inference efficiency and agent-trace multiplication are demand-side levers on L02 power draw, and they are the only levers available on a shorter horizon than grid interconnection.",
  hdr3="Evidence")}
</section>
"""
sub1(r'(<section class="section" id="opportunities">)', lambda m: XC + "\n" + m.group(1),
     "Part 2 section insert")

# ─────────────────────────────────────────────────────────────
# 4. Renumber Opportunities to Part 3
# ─────────────────────────────────────────────────────────────
plain('<div class="section-label">Part 2 — Strategic Gaps &amp; Opportunities</div>',
      '<div class="section-label">Part 3 — Strategic Gaps &amp; Opportunities</div>',
      "Renumber Opportunities to Part 3")

# ─────────────────────────────────────────────────────────────
# 5. Sidebar
# ─────────────────────────────────────────────────────────────
plain('<a href="#opportunities" data-target="opportunities">Opportunities</a>',
      '<a href="#crosscutting" data-target="crosscutting">Cross-Cutting</a>\n'
      '<a href="#opportunities" data-target="opportunities">Opportunities</a>',
      "Sidebar entry")

# ─────────────────────────────────────────────────────────────
# 6. Banner entries 30-34 + inline corrections
# ─────────────────────────────────────────────────────────────
def entry(num, headline, detail, source):
    return f"""
        <div class="update-item" id="update-{num}">
          <div class="update-num">{num}</div>
          <div class="update-body">
            <div class="update-headline">{headline}</div>
            <div class="update-detail">{detail}</div>
            <div class="update-source">Source: {source}</div>
          </div>
        </div>
"""

NEW_ENTRIES = (
 entry(30,
   'Data-centre energy: <s>1,000 TWh in 2026</s> <span class="new">~485 TWh (2025) &rarr; ~945 TWh (2030)</span>',
   'The 1,000 TWh-by-2026 figure carried since the April edition was a 2024-vintage IEA high-growth projection that did not materialise. Actual global data-centre consumption was <span class="new">~485 TWh in 2025</span>, and the IEA April 2026 base case now puts <span class="new">~945 TWh at 2030</span>, roughly 3% of global electricity. The report overstated 2026 consumption by roughly 2&times; and attributed a 2030-scale number to 2026. Corrected in both opportunity cards. <strong>The direction of the thesis is unchanged and the constraint argument actually strengthens</strong>, because the binding limit is interconnection queues rather than aggregate consumption.',
   'IEA, Energy and AI (Apr 2026); S&amp;P Global, Apr 2026'),
 entry(31,
   'Cerebras Q2 2026 reported Aug 12: <span class="new">$210M core revenue, FY26 guide raised</span>',
   'The prior edition flagged Aug 12 as the first hard read on wafer-scale economics. Result: <span class="new">$210M core revenue against ~$194M expected</span>, Q3 guide $214&ndash;216M, and FY26 core revenue guidance raised to <span class="new">$880&ndash;890M</span>. The stock nonetheless fell ~14% in extended trading. This confirms the report\'s existing framing precisely: <strong>the technology thesis is validated and the exit multiple continues to compress</strong>.',
   'CNBC, Aug 12, 2026; Cerebras 8-K'),
 entry(32,
   'EU AI Act high-risk obligations <span class="new">deferred to Dec 2027 / Aug 2028</span>',
   'On June 16, 2026 the European Parliament approved amendments deferring <span class="new">Annex III use-based high-risk obligations from Aug 2026 to Dec 2027</span> and <span class="new">Annex I product-regulated obligations from Aug 2027 to Aug 2028</span>. Article 50 transparency duties and AI Office enforcement over GPAI providers did take effect on schedule Aug 2, 2026. Material for Part 3: the Agent Compliance opportunity was upgraded to HIGH partly on EU prescriptive pressure, and <strong>the near-term EU gate is now disclosure and GPAI rather than high-risk certification</strong>. The US voluntary framework is unaffected.',
   'European Parliament, Jun 16, 2026; Holland &amp; Knight, Apr 2026'),
 entry(33,
   'AI-security consolidation: <span class="new">Lakera, Protect AI, Astrix, Robust Intelligence all acquired</span>',
   'Lakera was listed in the company database as an independent Layer 10 vendor; it was <span class="new">acquired by Check Point (2025)</span>. Also absorbed: <span class="new">Protect AI by Palo Alto Networks (completed Jul 22, 2025, now Prisma AIRS)</span>, <span class="new">Astrix by Cisco</span>, and Robust Intelligence by Cisco. Cyera has signed a $1B letter of intent for Oasis Security. The pattern matters more than any single deal: independents in this category are being acquired before reaching scale.',
   'Palo Alto Networks press release, Jul 22, 2025; Check Point; Cisco'),
 entry(34,
   'Zenity <span class="new">$125M Series C (Aug 3, 2026)</span> &mdash; missed by the Aug 10 refresh',
   'Zenity closed a <span class="new">$125M Series C led by Norwest</span> on Aug 3, 2026, bringing total funding to ~$185M, with SoftBank Vision Fund 2, Hitachi Ventures, Qumra and LG Technology Ventures participating. The round closed seven days before the last refresh and was not captured. Zenity secures AI agent actions inside enterprises, which is the Layer 09 surface the Agent Compliance opportunity in Part 3 targets. Broader context: <span class="new">AI-native security overtook identity as the fastest-growing VC category in Q1 2026 at $4.1B, +47% YoY</span>.',
   'BusinessWire, Aug 3, 2026; Intel Capital'),
)
plain('\n\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      "".join(NEW_ENTRIES) + '\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- KEY FINDINGS -->',
      "Banner entries 30-34")

# banner header
plain('10 <em>material changes</em> in August 10 refresh (+19 prior)',
      '5 <em>material changes</em> in August 17 refresh (+29 prior)', "Banner headline")
plain('<span class="update-banner-count">As of August 10, 2026</span>',
      '<span class="update-banner-count">As of August 17, 2026</span>', "Banner date")
plain('Entries 20&ndash;29 are the August 10, 2026 refresh cycle; entries 07&ndash;19 (July 13, 2026) and 01&ndash;06 (May 26, 2026) are retained below.',
      'Entries 30&ndash;34 are the August 17, 2026 refresh cycle; entries 20&ndash;29 (August 10, 2026), 07&ndash;19 (July 13, 2026) and 01&ndash;06 (May 26, 2026) are retained below.',
      "Banner intro")

# inline corrections — energy
plain('Data center energy projected to reach 1,000 TWh in 2026. Power availability is the #1 bottleneck. ',
      'Data centre energy <s class="old-val">projected to reach 1,000 TWh in 2026</s><span class="new-val">reached ~485 TWh in 2025; IEA base case ~945 TWh by 2030</span><a class="mark" href="#update-30" title="See update 30">[30]</a>. Power availability is the #1 bottleneck, and the binding limit is interconnection queues rather than aggregate consumption. ',
      "Inline TWh correction (post-GPU card)")
plain('AI data center power consumption projected to reach 1,000 TWh by 2026. Grid capacity is the binding constraint.',
      'AI data centre power consumption <s class="old-val">projected to reach 1,000 TWh by 2026</s><span class="new-val">~485 TWh in 2025 rising to ~945 TWh by 2030 (IEA base case)</span><a class="mark" href="#update-30" title="See update 30">[30]</a>. Grid capacity is the binding constraint: <span class="new-val">ERCOT alone received 198GW of large-load interconnection applications in Q1 2026 against a 438GW queue, with 4&ndash;7 year energization timelines in major hubs</span>.',
      "Inline TWh correction (energy card)")

# inline corrections — Cerebras
plain('~$64B Aug 9, Q2 report Aug 12',
      '~$64B Aug 9; <span class="new-val">Q2 reported Aug 12: $210M core rev vs ~$194M est., FY26 guide raised to $880&ndash;890M, stock &minus;14% after hours</span>',
      "Inline Cerebras Q2 (L01 table)")
plain('with first post-IPO earnings Aug 12',
      'with <span class="new-val">Q2 reported Aug 12: $210M core revenue against ~$194M expected and FY26 guidance raised to $880&ndash;890M, yet the stock fell ~14% after hours &mdash; technology thesis validated, multiple still compressing</span><a class="mark" href="#update-31" title="See update 31">[31]</a>',
      "Inline Cerebras Q2 (opportunity card)")

# ─────────────────────────────────────────────────────────────
# 7. Hero + footer
# ─────────────────────────────────────────────────────────────
plain('Confidential Strategy Document · Refreshed August 10, 2026',
      'Confidential Strategy Document · Refreshed August 17, 2026', "Hero eyebrow")
plain('<div class="hero-meta-item">Data as of <span>August 10, 2026</span></div>',
      '<div class="hero-meta-item">Data as of <span>August 17, 2026</span></div>', "Hero meta")

FOOT_ADD = ('  <p style="margin-top:.5rem;"><strong>August 17, 2026 cycle:</strong> adds <strong>Part 2 — Cross-Cutting Concerns</strong>, '
 'three spines (security, regulation, energy) running vertically through all twelve layers, and <strong>value-chain dependency blocks on every layer</strong>, '
 'closing the upstream/downstream gap carried since the first edition. Opportunities renumbered to Part 3. Five corrections logged (entries 30&ndash;34), '
 'verified across 12 distinct web searches covering AI-security market structure and M&amp;A, AI-SOC funding, non-human identity, MCP vulnerability disclosure, '
 'EU AI Act timeline amendments, US export-control changes, data-centre energy and interconnection-queue data, and Cerebras Q2 results. '
 'The most material correction is entry 30: data-centre energy consumption was overstated by roughly 2&times; in prior editions.</p>\n')
sub1(r'(  <p style="margin-top:\.5rem;">Prepared for C-Suite)', lambda m: FOOT_ADD + m.group(1), "Footer note")

# ─────────────────────────────────────────────────────────────
DST.write_text(html)
print("\n".join("  OK   " + a for a in applied))
if failed:
    print("\nFAILED:")
    print("\n".join("  FAIL " + f for f in failed))
    sys.exit(1)
print(f"\nWrote {DST} ({len(html):,} bytes, was {len(SRC.read_text()):,})")
