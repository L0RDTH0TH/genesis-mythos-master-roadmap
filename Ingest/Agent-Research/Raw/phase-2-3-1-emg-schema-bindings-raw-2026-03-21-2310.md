---
title: Raw captures — Phase 2.3.1 EMG schema bindings research
created: 2026-03-21
tags: [research, agent-research, raw]
linked_phase: Phase-2-3-1-EMG-Schema-Bindings
project_id: genesis-mythos-master
source_urls:
  - https://www.rfc-editor.org/rfc/rfc8785.html
  - https://www.well-typed.com/blog/2019/01/qsm-in-depth/
  - https://github.com/jaspervdj/goldplate
  - https://dl.acm.org/doi/10.1145/103162.103163
  - https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html
agent-generated: true
---

## Source: https://www.rfc-editor.org/rfc/rfc8785.html

RFC 8785 — JSON Canonicalization Scheme (JCS), June 2020 (Informational).

Abstract (excerpt): Cryptographic operations like hashing and signing need data in an invariant format. JCS defines a canonical representation of JSON using ECMAScript strict serialization, I-JSON subset, and deterministic property sorting — output is a "hashable" representation for cryptographic methods.

Key points for ledger binding:
- Canonicalize before hash/compare across languages and log replay.
- I-JSON constraints; duplicate property names forbidden; high-precision numbers as strings recommended (Appendix D pattern referenced in RFC).
- Unicode string data preserved "as is" (normalization not applied in JCS string processing).

Full text: https://www.rfc-editor.org/rfc/rfc8785.html

---

## Source: https://www.well-typed.com/blog/2019/01/qsm-in-depth/

Well-Typed blog — "An in-depth look at quickcheck-state-machine" (Edsko de Vries, 2019).

Excerpt / summary:
- Stateful APIs need generated *sequences* of calls; shrinking must respect dependencies (e.g. cannot drop `open` while keeping `write` on that handle).
- Tests maintain an internal model of expected state; commands run against both model and real system; responses compared.
- **Reify the API**: data type constructors correspond to API calls so generation does not depend on runtime values — enables reproducible replay of the same test case.
- Reference library: quickcheck-state-machine; example: mock file system vs real FS.

Full article: https://www.well-typed.com/blog/2019/01/qsm-in-depth/

---

## Source: https://github.com/jaspervdj/goldplate

README summary (fetch): Golden test runner for CLI applications — deterministic output comparison pattern for regression suites.

Repo: https://github.com/jaspervdj/goldplate

---

## Source: https://dl.acm.org/doi/10.1145/103162.103163

Goldberg, *What Every Computer Scientist Should Know About Floating-Point Arithmetic*, ACM Computing Surveys, 1991.

Bullets (paraphrase for EMG binding):
- Floating-point operations are not associative; reordering changes results.
- Rounding modes and precision differ across languages and hardware; do not assume bitwise-stable floats in cross-platform hashes.
- Use numerically stable algorithms or fixed-point / string encodings when hashes must match.

Full text via ACM DOI above.

---

## Source: https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html

NVIDIA CUDA C Programming Guide (index; see sections on deployment, versioning, math, and reproducibility).

Bullets (guidance class for Tier C):
- GPU results may vary with device, driver, and non-deterministic reductions unless a restricted deterministic subset is used.
- Treat GPU-derived fields as non-hashable for EMG-1 unless project documents an explicit determinism contract.

---

## Note (audit)

The Medium URL used in early synthesis draft is **optional reading** only; demoted in synthesis note callout. Not duplicated here.
