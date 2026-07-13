1. Abstraction
Hiding complexity beneath a simpler interface. Each layer in the stack abstracts the one below — you call claude-sonnet-4-6 via API without knowing whether it's running on H200s, NVLink clusters, or TPUs. Without abstraction, every app developer would need to write CUDA kernels.
2. Evaluation
Measuring whether an AI system is actually doing what you think it's doing. The report flags this as a critical gap — 87% of enterprises can't reliably tell if their RAG pipelines are accurate, or if their agents are improving. It's why "Datadog for RAG" is rated a HIGH opportunity: you can't optimize what you can't measure.
3. Computation
The raw arithmetic (matrix multiplications, mostly) that runs every model forward pass. This is Layer 1–3 of the stack — silicon, data centers, networking. It's the physical constraint on all AI: power limits how much computation you can run, which caps model size, which caps capability. The "1,000 TWh by 2026" figure is literally the cost of today's global AI computation in energy terms.
How they nest together:
Computation  →  makes inference possible
Evaluation   →  tells you if inference is any good  
Abstraction  →  hides both from the app developer
The entire 12-layer stack is essentially a series of abstractions built on top of computation, with evaluation being the mostly-unsolved connective tissue between them.