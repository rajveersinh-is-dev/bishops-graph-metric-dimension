# Evidence Ledger — bishops-graph-metric-dimension

Project: *Exact metric dimension of the bishop colour components of the n×n board*.
Author: Rajveersinh Vishal Pardeshi.
Ledger compiled and continuously updated on **2026-10-18** in one research session.

Purpose: map **every factual claim** that enters the manuscript to the artifact
that verifies it. Status vocabulary:

- **PROVED** — theorem-level statement with a written proof in `paper/main.tex`.
- **COMPUTED** — exact solver output, cross-checked by an independent method;
  exact for the stated range only.
- **CONJECTURE** — pattern statement; not proven; supported only by computation
  on the verified range. Always labeled as conjecture in the manuscript.
- **VERIFIED-SOURCE** — bibliographic fact checked against publisher/arXiv full
  text or an original page (dated, quoted in `research/literature_review.md`).
- **PENDING** — work scheduled in this session; not yet usable in any claim.

---

## 1. Mathematical definitions and the reformulation claim

| Claim | Status | Evidence |
|---|---|---|
| Cells (r,c), r,c ∈ {0..n−1}, of the n×n bishop's graph are adjacent iff r−c or r+c coincide (two diagonals per direction); bishop's graph = graph of that adjacency on all n² cells. | PROVED (definition-level; adjacency is the bishop's move) | `src/bishop.py` docstring; standard bishop move definition as used throughout the literature (Wikipedia "bishop's graph", retrieved 2026-10-18, research/literature_review.md §3) |
| Bishop's graph has exactly **two** connected components = the two board colour classes (indices (r+c) mod 2). | PROVED | Same sources; also verified computationally: `bishop_components(n)` + single-colour BFS stays inside one colour class (`src/bishop.py: bishop_components`, `component_distances`); exercised for n ≤ 16 in `results/dims_2_16.json` pipeline |
| Coordinate map (u,v) = (r−c, r+c) with uniform scaling ½ inside one colour class sends a colour component to a board  𝒟 = {(u,v)} in which adjacency becomes sharing u or sharing v, i.e. a **rook graph on a diamond-shaped board**. | PROVED in manuscript (Theorem A) | Algebraic argument in paper §"diamond reformulation"; cross-checked numerically: `src/structure.py: component_uv` reproduces exactly the same vertex sets for n ≤ 16 (used in rule-verification runs, 0 disagreements) |
| Wikipedia documents the *informal* diamond-rook reformulation of bishop components (attribution: Hedetniemi & Hedetniemi 2020 chapter; Berghammer 2012). | VERIFIED-SOURCE | `research/literature_review.md` §3 (quotes the Wikipedia passage and its two references, retrieved 2026-10-18). Manuscript credits this as prior informal observation |
| The **exact metric dimension** of these components was not previously published | VERIFIED-SOURCE (negative literature claim) | Full text of Tennenhouse arXiv:1905.05033v2 covers only the two-bishop game product graph B_L(a,b)□B_D(a,b) and 2×n/3×n strips (research/literature_review.md §3; quoted theorems); Cáceres et al. 2007 Theorem 6.1 applies only to K_m□K_n (full rook boards); Feng–Xu–Wang 2013 gives bounds only. Search recorded in literature_review.md §5 |

## 2. Diametrical/structural lemmas feeding the theorem

| Claim | Status | Evidence |
|---|---|---|
| Component "rook-graph" distance is 0/1/2 (a diameter-2 lemma: every two cells with distinct rows and columns have at least one cross cell in the diamond). | PROVED in manuscript; COMPUTED cross-check | `tests/test_bishop.py: test_diameter_two` (BFS distances ≤ 2 for all n ≤ 8, all components); proof in paper; also encoded as `rook_distance` in `src/structure.py` and consistent in all rule-verification runs |
| Three-rule characterization of resolution: (R-col) same-column pair resolved ⇔ landmark on row u1 or row u2; (R-row) symmetric; (R-cross) cross pair resolved ⇔ landmark on one of rows u1,u2 / cols v1,v2 other than the two cross cells. | PROVED in manuscript (Theorem on rules); COMPUTED cross-check | `src/structure.py: rules_disagree` counts verdict discrepancies of rules vs direct distance computation: **0 disagreements** for every optimal resolving set reported in `results/*.json` for n ≤ 16; `verify_rules_and_resolution` double-checks actual resolution too |
| Adding a cell that is *not* a cross cell to the corresponding line resolves the pair — the "asymmetric cross" bookkeeping in the theorem. | PROVED in manuscript | Included in the rule proof; machine-checked jointly with the above (rules vs direct) |
| Necessary conditions: a resolving set S has at most 1 landmark-free row and at most 1 landmark-free column; |corner twins {(0,0),(0,B)} obstruction; lower bound min(#lines)−1. | PROVED in manuscript (necessary-condition theorem) | Row 0 spans all columns and all rows pairwise intersect ⇒ row/column coverage argument (paper proof); consistent with every optimal basis in `results/dims_2_16.json` (spot-checked against ILP outputs) |
| The +W/6 growth of dim over W = n−1 comes from cross-pair obstructions | CONJECTURE (not proven in general) | Paper states it explicitly as a conjectured explanation; supporting computation = exact dim values n ≤ 16 (and extended range when jobs finish) |

## 3. Exact metric dimensions (computed column of the paper)

| Range | Status | Artifact / verification |
|---|---|---|
| n = 1 … 16, both components | COMPUTED (exact ILP; verified) | `results/dims_2_16.json` (committed, root commit); `benchmark_dimension` proves optimality via exact MILP with `mip_rel_gap=0` (HiGHS via scipy.optimize.milp) and *independently re-verifies* the returned set resolves (`src/bishop.py` raise on failure); brute-force cross-check n ≤ 5 in `tests/test_bishop.py: test_small_brute_force` |
| n = 17 … 24, both components | PENDING — single background job `python src\fast_verify.py 17 24 results\dims_17_24.json` (shell launched 2026-10-18, ~22 min per component at n=16; n=17+ expected slower). On clean completion: add `results\dims_17_24.json`, regenerate `tables_auto*.tex`/`fig_n9.tex` (nmaxverified extended to exactly the completed range), bump the Computational Theorem range, recompile, commit + push. If any size hits the 1800s/call time limit, keep nmaxverified at the last fully completed n and do not force it. | file existence + JSON contents once written |
| Closed-form conjecture consistency (floor formulas per parity/case) for the full completed range | COMPUTED (regression) | `src/conjecture_check.py` — prints exact vs conjectured for every record in every `results/dims_*.json`; "ALL MATCH" required before "verified to n" can be said in the paper |
| All reported optimal bases are genuine resolving sets | COMPUTED (independent verifier) | `tests/test_bishop.py: test_solution_resolves_all_reported` re-checks every basis in every `results/dims_*.json` via pure-BFS distances |
| ILP formulation correctness (set cover over vertex pairs reproduces resolving-set optimum) | PROVED (standard equivalence, argued in paper's computational section) + brute force | `test_small_brute_force` for all components with n ≤ 5 |

## 4. Manuscript-level claims about asymptotics

| Claim | Status |
|---|---|
| dim(component) = W + ⌊W/6⌋ + O(1) with W = n−1, in each stated case | CONJECTURE (with exact floor forms stated per case); supported by computed table for the completed range; explicitly labeled conjecture |
| For even n both components equal | COMPUTED for completed range (identical dims in JSON) |

## 5. Environment and provenance facts

| Fact | Status | Evidence |
|---|---|---|
| Python 3.14.6 with scipy (HiGHS) used for exact ILP; Tectonic 0.17 available as the only LaTeX engine; git 2.53 | VERIFIED (session env inspection, earlier in session) | recorded in session log; paper "software" section will state these |
| Public GitHub repository created 2026-10-18: `rajveersinh-is-dev/bishops-graph-metric-dimension` | VERIFIED | `gh repo view … --json` output: name= bishops-graph-metric-dimension, owner.login= rajveersinh-is-dev, isPrivate=false, defaultBranch=master, URL https://github.com/rajveersinh-is-dev/bishops-graph-metric-dimension |
| First pushed commit = root commit (code + n≤16 results), hash `1f7dcbd282847d589f496c3a07d67a97e4c3e0bc` | VERIFIED | `git ls-remote origin` returns identical hash; `git rev-parse HEAD` identical |
| Commit author identity | VERIFIED | author/committer name "Rajveersinh Vishal Pardeshi", email `319411334+rajveersinh-is-dev@users.noreply.github.com` — the noreply form of the *actually authenticated* account (`gh api user` → login `rajveersinh-is-dev`, id 319411334, name "Rajveersinh Pardeshi"). **Correction note:** an earlier unpushed version of the root commit (hashes 4418094 → f3839d8) used an email placeholder `daveaddams91-dev@users.noreply.github.com` that does not belong to the authenticated account; it was amended (twice: identity fix, then removal of empty placeholder log files) *before any push*, so no history existed on GitHub. Both real — stale — hashes are recorded here for audit trail |
| All results JSONs and console logs are genuine solver outputs of this session | VERIFIED | produced by `src/compute_dims.py` runs whose PIDs and command lines are recorded in §3; logs `results/out_*.txt` retained untracked (transient) or committed with content when complete |

## 6. Journal-fee verification (Oxford University Press)

Target class: **OUP journal with a verified no-mandatory-author-fee route** (standard/hybrid licence, not a flipped journal).

| Journal | Status | Evidence (official OUP pages, retrieved 2026-10-18 via browser session) |
|---|---|---|
| **Quarterly Journal of Mathematics** (primary) | VERIFIED — hybrid; OA strictly optional | `academic.oup.com/qjmath/pages/General_Instructions` (full text captured in session): "publishing under either a standard licence or an open access licence… Should you wish to publish your article open access… You will need to pay an open access charge to publish under an open access licence." No other fee (submission/page/colour) is mentioned anywhere on the page; OUP central page `academic.oup.com/journals/pages/open_access/charges` confirms "Most OUP journals offer the option…" (optional APC in hybrid journals). QJM prints ISSN 0033-5606 (subscription journal, not flipped) |
| **Journal of Logic and Computation** (fallback) | VERIFIED — explicit no-charge statements | `academic.oup.com/logcom/pages/General_Instructions`: "There is a charge to publish under an open access licence… The standard licence … there is no licence charge." Plus: "Colour charges — the journal does not charge for colour." "Page charges — the journal does not have page charges." |
| **The Computer Journal** (only if above fail) | PENDING — fee policy not verifiable from its instructions page (`General_Instructions` page contains LaTeX templates and no fee text) | would require the OUP charging-tool lookup before use; not used while unverified |
| Journal of Complex Networks | EXCLUDED earlier | fully-OA model ⇒ APC mandatory; fails the fee constraint |

## 7. Open PENDING items (must be closed before final report)

1. n = 17 … 24 exact results landing from background jobs → extend
   `conjecture_check` evidence, update paper's computational theorem range and
   table honestly (include exactly the completed range).
2. Final scoop-check: re-run targeted literature searches ("bishop graph metric
   dimension", "diamond rook graph", "landmarks in queens' graphs" etc.) right
   before submission; documented failure to find prior exact results.
3. Kuziak–Yero metric-dimension survey: DROPPED — not cited anywhere in the manuscript; the paper stands without it (no title/journal verification needed).
4. Hostile internal review passes 1 and 2 documented in
   `research/hostile_review.md`; every objection answered or the manuscript
   adjusted.
5. Final claim-by-claim audit of `paper/main.tex` §-by-§ against this ledger.

## 8. Honesty constraints respected in writing

- Conjectures D are stated as conjectures with their verification range only;
  no "proven" language.
- The computational theorem states exact sizes *and* the verifying methods
  (ILP + independent resolution verification + rules oracle + brute force where
  feasible); it is worded as computer-assisted, not as hand-proof.
- Negative literature claims are phrased as "to the best of our knowledge,
  based on the surveyed sources (listed)".
- No invented affiliation: "Independent Researcher".
- No acceptance-probability numbers unless a defensible basis exists; otherwise
  the report will state plainly that none can be given.
