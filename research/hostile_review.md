# Hostile review — pass 1

*Referee persona: skeptical, demanding, checks every quantitative claim against the data, dislikes hand-waving and overclaiming. Goal: find reasons to reject.*

## Manuscript under review

"The exact metric dimension of the bishop's graph: a diamond rook-board reformulation, a structural characterisation of resolving sets, and certified computation" — Rajveersinh Vishal Pardeshi.

## 1. The biggest threat: the disconnected-union lemma

The paper's headline number — "the metric dimension of the bishop's graph is the sum of the two components" — rests on Lemma 1 (union convention). The *unconditional* claim dim(G) = sum dim(C_i) is FALSE in general: two isolated vertices give dim = 1 ≠ 0+0; three components that are all singletons likewise. The revised statement restricts to "at most one component consists of a single vertex" — that repair is valid for the bishop's graph (n≥2: two components each with ≥2 cells), but the reviewer must confirm the *proof* of the converse direction actually uses the hypothesis. In the submitted proof, "every component-pair includes a nonsingleton component whose S_i supplies a landmark in C_i ∪ C_j" — that argument works precisely because at most one component is a singleton. OK, defensible, but the lemma as first drafted was wrong; a hostile referee will note the paper had to correct itself.

Verdict: acceptable *as stated*, but the correction note must stay in the audit trail (evidence_ledger.md records it).

## 2. The even-n odd component is a transpose, not an identical copy

Theorem 1 (case 1) now states honestly that the odd class maps onto the transpose of DD_{2k-1} under the canonical board-indexing coordinates. Good — the earlier draft claimed both classes map onto the same diamond, which was false (n=4: image row lengths {3,3,1,1} vs DD_3's {2,4,2}). Since rook distance is transpose-invariant, all *metric* conclusions survive, and the ILP dimension is unchanged. But the phrasing "both components are copies of DD_{2k-1}" needs to be read as "as rook boards". Retained wording is careful enough ("\RRc and \RRr merely exchange roles... which is all the statement claims"). 

Risk: a referee recomputing coordinates from phi directly will see the transposed shape and wonder. The figure (n=9, odd board) avoids this issue entirely.

## 3. Computational claims depend on one solver

Every exact dimension for n=2..16 comes from HiGHS via scipy.optimize.milp with mip_rel_gap=0, plus an independent *resolving-set re-verification* (BFS + rule oracle + brute force n≤5). The lower-bound half ("infeasible at k−1") rests entirely on the solver's branch-and-bound completeness proof — no independently implemented certificate (e.g., dual LP bound, combinatorial lower bound). A hostile referee will ask: could HiGHS report a false infeasibility? Answer: within solver-correctness assumptions, standard for computational graph-theory papers; mitigated by the two-phase self-correcting seed and by independent re-verification of each *upper* bound (the returned set really resolves). The asymmetry — lower bounds solver-only — should be stated plainly rather than implied to be "four independent mechanisms", since mechanism #1 is the one doing the lower-bound work and mechanisms #2–4 only re-verify upper bounds.

Refine wording in §4.5: mechanisms 2–4 establish that the size-k* set is resolving; they do NOT independently establish dim ≥ k*. The paper currently says "Each optimality claim ... is supported by four mutually independent mechanisms" — overstated. Downgrade to: "the upper bound is re-verified by three independent mechanisms; the lower bound rests on the solver's infeasibility certificate."

## 4. Conjectures are conjectures — but the paper skates close to claiming them

Conjecture 1's three floor-formulas match all certified n=2..16 values (n=3 odd exception noted). The paper says "All computed values match ... verified through nmaxverified ... stated as conjectures ... no proof is offered." That framing is honest. The *abstract*, however, says "All computed values match floor-form conjectures ... verified through nmaxverified" — fine — but the intro sentence "the metric dimension is at least max(#rows−1,#cols−1)" combined with the conjecture discussion might lead a reader to think the asymptotic 7n/6 is proved. It is not. Keep "conjectured" prominent in abstract, title-area, and Theorem 3/Conjecture blocks. Already done, but double-check the abstract doesn't say "we prove dim ~ 7/6 n" anywhere.

## 5. The LP-irrelevance remark

The remark cites lp_results.json: n=12 LP relaxation 6.5 vs integer optimum 12, gap growing through n=12. Verified against the file (6.5 exactly; dim 12). But the claim "the gap keeps growing through n=12" — from the file: n=11 gap 12−6.33=5.67; n=12 gap 12−6.5=5.5. 5.5 < 5.67, so the gap does NOT monotonically grow through n=12! Wording must change: e.g. "the gap is large (LP 6.5 vs integer 12 at n=12) and remains large across the measured range" — drop "keeps growing".

Also: the LP file covers n=2..12 only, matching the remark's "measured for n≤12". OK.

## 6. n=1 edge case

Table starts at n=1 with dim_even=0, odd component empty, total 0. Lemma's hypothesis (at most one singleton) — bishop graph n=1 is *connected* (single vertex), dim 0 by convention. Fine.

## 7. Citations

- Cáceres et al. 2007 rook-graph formula ⌊2(m+n−1)/3⌋ — matches literature_review.md; entry caceres2007 in references.bib source-verified.
- Bailey–Cameron L(K_n) = ⌈2n/3⌉ (n≥6) — matches; entry baileycameron2011 verified.
- Tennenhouse remark on chessboard-graph convention — plausible; entry present.
- Berghammer 2012 and Heding... — publisher-verified per ledger.

No obvious citation errors spotted.

## 8. Figure n=9

Caption claims one optimal resolving set of size 9 with listed (u,v) coordinates, component DD_8 with 41 points. Verified against dims_2_16.json n=9: dim_even=9, |C_even|=(81+1)/2=41, and the nine (r,c) cells convert exactly to the caption's (u,v) list via phi. The figure generator asserts equality with the caption list, so figure and text cannot drift. Good.

## 9. Remaining nitpicks

- §4.1 ILP display: fine.
- Abstract uses \nmaxverified; now defined in tables_auto.tex loaded in preamble — compiles.
- Journal: QM (QJM primary) standard licence route, OA optional — fee policy verified on official page (per ledger). No fabricated acceptance probability anywhere in the paper — good; keep it out.

## Required fix before submission

1. Downgrade "four mutually independent mechanisms" claim (mechanisms 2–4 verify only the upper bound).
2. Fix LP-growth wording ("keeps growing through n=12" is false: 5.67 → 5.5).

Everything else is defensible as written, with conjectures clearly labeled.

---

Decision after pass 1: REVISE (minor). Two concrete text edits required (independence wording; LP-growth wording).

## 2. Pass 2 — computation audit

*Referee persona: numerical skeptic. Every dimension number in Table 1 is recomputed against the artefact files.*

### 2.1 Table vs data (n=2..16 from dims_2_16.json)

| n | even | odd | total | formula match? |
|---|------|-----|-------|----------------|
| 2 | 1 | 1 | 2 | Y |
| 3 | 2 | 2 | 4 | Y (odd = n=3 exception, dim 2) |
| 4 | 3 | 3 | 6 | Y |
| 5 | 5 | 4 | 9 | Y |
| 6 | 5 | 5 | 10 | Y |
| 7 | 7 | 6 | 13 | Y |
| 8 | 8 | 8 | 16 | Y |
| 9 | 9 | 8 | 17 | Y (figure basis matches) |
|10 |10 |10 |20 | Y |
|11 |12 |11 |23 | Y |
|12 |12 |12 |24 | Y |
|13 |14 |13 |27 | Y |
|14 |15 |15 |30 | Y |
|15 |16 |15 |31 | Y |
|16 |17 |17 |34 | Y |

All 30 component values match Conjecture 1's floor formulas; n=3 odd is the documented exception (dim 2 vs formula 1). Table 1 and dims_2_16.json agree exactly (cross-checked by make_paper_assets.py asserts: sizes, basis membership, conjecture agreement — all passed, zero problems).

### 2.2 Certification status

- n=2..16: dims_2_16.json (root commit) — exact MILP, mip_rel_gap=0, re-verified resolving by BFS + rule oracle (+ brute force n≤5).
- n=15,16 re-run by fast_verify.py two-phase ladder (dims_fast_test2.json): n=15 → 16/15, n=16 → 17/17, independently re-derived, times ≤ ~22 min/component. Matches dims_2_16.json exactly.
- n=17..24: running in background (dims_17_24.json pending). Not yet in the table; nmaxverified=16 in the current build is correct for the committed data.

### 2.3 Residual computation risks

- Lower bounds (dim ≥ k*) rely solely on HiGHS infeasibility certificates; no independent combinatorial lower bound is provided. Mitigated by self-correcting seeds and phase-B actual optimal sets, but a determined referee could demand a solver-independent lower bound for at least one representative n. State the dependence plainly (see pass 1, item 3).
- Timing: phase A (infeasibility) dominates — n=15 odd took 460s, n=16 ~1100–1300s per component. n=17+ will be substantially harder (|V| grows quadratically, pairs ~ |V|²/2: n=24 has |V|=288 per component, 41k pairs). The 1800s/call time limit may bind; if it does, results must be reported as "time limit reached" rather than forced. Do not extend nmaxverified beyond what the ladder completes cleanly.
- Randomness: HiGHS is deterministic given the same input; no seeds needed, but wall-clock times are not reproducible across machines. Times are logged for provenance only.

### 2.4 Data formats

dims_2_16.json is list-format with (r,c) board bases; fast_verify writes dict-format with (u,v) bases. make_paper_assets.py merges them and converts via structure.to_uv (canonical, shared with fast_verify.py and conjecture_check.py). conjecture_check.py now reads both formats. No format mismatch risk in the table build.

### 2.5 Verdict on computation

Numbers are internally consistent across two independent pipelines and three independent verification mechanisms (for upper bounds). Acceptable for a computational mathematics paper, *provided* the lower-bound solver-dependence is stated honestly and nmaxverified is not overclaimed.

---

### Combined disposition after passes 1–2

REVISE (minor):
1. Downgrade "four mutually independent mechanisms" → mechanisms 2–4 verify upper bounds only; lower bound rests on solver infeasibility certificate. (§4.5)
2. Fix LP remark: drop "the gap keeps growing through n=12" (5.67 → 5.5 is not growth); say gap remains large (LP 6.50 vs integer 12 at n=12).
3. (If n=17–24 run completes cleanly:) add dims_17_24.json, regenerate tables with nmaxverified=24, bump Theorem 3 range, recompile, new commit + push.

If the background run hits time limits on n≥17, keep nmaxverified=16 — do not force it.

