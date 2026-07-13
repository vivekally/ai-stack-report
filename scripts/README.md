# scripts/

Reference data and build notes.

## `stack_db.js`

The full company database used by both the search modal and the knowledge graph in `src/ai_stack_unified_search.html`. Extracted as a standalone file so it can be edited independently and re-injected into new HTML variants.

**Contents:** 97 companies, 252 mapped relationships.

**Schema:**
```
window.STACK_DB = [
  {
    id:  "anthropic",              // unique key, snake_case
    n:   "Anthropic",              // display name
    a:   ["claude", "sonnet", ...], // aliases for search
    l:   6,                        // primary layer (1-12)
    L:   [9, 11],                  // secondary layers (optional)
    t:   "Frontier model lab...",  // one-line tagline
    s:   [["ARR", "~$43B"], ...],  // key stats
    r:   ["Total Raised", "$72.3B over 18 rounds"],  // funding or market cap
    c:   [                         // connections
      {r: "compute",    t: "aws",       n: "$138B deal"},
      {r: "competitor", t: "openai"},
      // ...
    ]
  },
  // ...
];
window.STACK_LAYERS = { "1": "Silicon", "2": "Compute & DC", ... };
```

**Relationship types** (fixed set): `compute`, `silicon`, `supplier`, `customer`, `product`, `competitor`, `partner`, `investor`, `parent`.

**Validation invariant:** every `c[].t` must reference a valid `id` in the database. Run this check whenever you edit:

```python
import json, re
content = open('stack_db.js').read()
db = json.loads(re.search(r'window\.STACK_DB\s*=\s*(\[.*?\]);', content, re.DOTALL).group(1))
ids = {c['id'] for c in db}
missing = {conn['t'] for c in db for conn in c.get('c', []) if conn['t'] not in ids}
print("Invalid targets:", missing or "none")
```

## Build process (notes)

Prior HTML variants in `archive/` were built with Python injection scripts that:
1. Started from a base HTML file
2. Used `str_replace`-style anchors to inject CSS blocks, HTML fragments, and JS
3. Validated the output with HTMLParser (with void-tag exclusion for `br`, `hr`, `meta`, `link`, `img`, `input`, `area`, `base`, `col`, `embed`, `source`, `track`, `wbr`)

The scripts themselves were disposable process artifacts. What matters is:
- The design system (documented in `../CLAUDE.md`)
- The current canonical file (`../src/ai_stack_unified_search.html`)
- This database (`stack_db.js`)

To build a new variant: hand-edit the current canonical, or ask Claude (with `../CLAUDE.md` loaded) to inject new features while preserving the design system.
