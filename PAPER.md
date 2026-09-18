# exclusion-display-audit — campaign report

**Full paper: [paper/main.pdf](paper/main.pdf)** (LaTeX source: paper/main.tex)

Cycles: 0 · Experiments: 0 · Promotions: 0 · Final incumbent score: None

> Draft artifact. Before this leaves the building it must pass docs/paper-audit-protocol.md; human-only byline + AI-contribution statement.

## Abstract

The averaged null energy condition (ANEC) states that the null-null stress component, integrated along a complete null geodesic, is non-negative. Graham and Olum (2007) and Wall (2010) derive its achronal form through chains of displayed relations; Borde (1987) is the classical antecedent. We asked whether any derived display in these papers fails on an exact, premise-satisfying instance under the paper's own conventions and expansion order. We froze a registry of the displayed relations, classified each as premise, definition, imported result or derived relation, and built a mechanical verifier that evaluates a derived row in exact arithmetic, reporting a hit only when every printed premise holds and the relation fails. One search run explored 309 candidates. With one exception, every evaluable derived row of Graham and Olum and of Wall was exactly confirmed on every premise-satisfying instance that evaluated (a searcher-recorded outcome, not an engine count). The exception is Wall's equation (30): the ledger records one hit row on it, and the searcher's unreplayed sweep output (not on the ledger) holds four further instances of the family R^(1)_kk = 8 pi T^(1)_kk + 1 that the frozen predicate accepted. Inspection of the frozen evaluator shows that its equation-(30) branch omits the order-hbar Einstein identification R^(1)_kk = 8 pi T^(1)_kk that the equation-(31) branch enforces; we classify the hit as a verifier defect by that inspection alone, pending a re-run under a repaired gate in an approved extension, and claim no error in Wall. The second hit row is the pre-registered calibration control on the Flanagan and Wald kernel constant, printed 12 pi in their Appendix D, Eqs. (D7) and (D13), and independently derived as 16 pi. Neither frozen ship condition is met as written: no hit was re-verified by a source-based reimplementation, and no row carries a symbolic certificate. This is a partial question-status report shipped under a Director ruling, one status per paper: Graham and Olum instance-confirmed on every evaluated derived row; Wall parked on the non-evaluable rows W-23, W-26, W-32 and W-34 and on the equation-(30) gate gap; Borde parked, full text unavailable. The report carries instance-level confirmations for nine evaluable rows plus W-30 under a defective gate, named obstructions for the rest, and a geometry-versus-matter provenance for each step.

## Belief state at close

# PRIORS — exclusion-display-audit

Belief state. Every claim: `[STATUS] claim (evidence)`. Wrong beliefs get status-flipped in place, never deleted.

- [ALIVE] VERIFIED HIT (run 1): {"paper": "W", "row": "30", "instance": {"theta1": "0", "T1_kk": "0", "sigsq1": "0", "R1_kk": "1"}} (SEARCH-1)
- [ALIVE] VERIFIED HIT (run 1): {"paper": "FW", "row": "D7", "instance": {}} (SEARCH-1)
- [DEAD] Search run 1 dead ends: Every evaluable derived row of GO and Wall is exactly confirmed on every premise-satisfying instance that evaluated: GO-5 (32/32), W-7 (27/27 evaluable), W-17-18, W-24, W-25 (all premise-satisfying grid points), W-27/W-31 (all), W-29/W-33 (20/20 evaluable). These rows are identities or linear conseq (SEARCH-1)

