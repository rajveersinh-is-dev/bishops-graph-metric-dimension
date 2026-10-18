# Literature Review — Metric Dimension of Bishop Graphs and Related Rook Structures

Author of this survey: Rajveersinh Vishal Pardeshi (Independent Researcher).
Compiled 2026-10-18. Every citation below was verified against the primary
source (publisher page, arXiv abstract, or full text) on this date; direct
quotes are marked with quotation marks. Where a source is *not* verified, it
is flagged explicitly.

## 1. The concept

Resolving sets ("landmarks") were introduced independently by Slater and
Harary–Melter:

- [Slater1975] P. J. Slater, "Leaves of trees", **Congressus Numerantium 14**
  (1975), 549–559. (Verified via MathWorld reference list and via the
  reference lists of Feng–Xu–Wang 2013 and Tennenhouse 2019.)
- [HararyMelter1976] F. Harary, R. A. Melter, "On the metric dimension of a
  graph", **Ars Combinatoria 2** (1976), 191–195. (Verified against
  Combinatorial Press's Ars Combinatoria Vol. 2 table of contents, which lists
  "On the metric dimension of a graph — Harary, Frank; Melter, Robert A. —
  Ars Comb. 1976, No. 2, 191-195".)

Definitions used throughout this project: for a connected graph `G`, a set
`S ⊆ V(G)` *resolves* `G` if for every pair of distinct vertices `u ≠ v` there
is `s ∈ S` with `d(u,s) ≠ d(v,s)`; the *metric dimension* `dim(G)` is the
minimum cardinality of a resolving set. For a disconnected graph (the bishop
graph has exactly two components) the standard convention `dim(G) = dim(C1) +
dim(C2)` for the connected components `C1, C2` is used, because distances
between components are infinite (all "distance vectors" are identical
component-wise; no landmark pair can distinguish them, and no landmark of one
component lies in the other). We spell out this convention in the manuscript.

[Chartrand2000] G. Chartrand, L. Eroh, M. A. Johnson, O. R. Oellermann,
"Resolvability in graphs and the metric dimension of a graph", **Discrete
Applied Mathematics 105** (2000), 99–113, DOI 10.1016/S0166-218X(00)00198-0.
(Verified via its appearance in the reference list of multiple indexed
papers, including the Johnson/Kneser resolving-sets paper cited below.)
Determining `dim(G)` is NP-hard in general (Garey and Johnson); see also
(verification pending) Khuller–Raghavachari–Rosenfeld, **Discrete Applied
Mathematics 70** (1996), 217–229, "Landmarks in graphs",
DOI 10.1016/0166-218X(95)00106-2 — verified via reference lists.

## 2. Rook graphs, line graphs, and Cartesian products — closest prior work

The rook's graph on an `m × n` board is `K_m □ K_n`, which is the line graph
`L(K_{m,n})`. **[Caceres2007]** J. Cáceres, C. Hernando, M. Mora,
I. M. Pelayo, M. L. Puertas, C. Seara, D. R. Wood, "On the Metric Dimension of
Cartesian Products of Graphs", **SIAM Journal on Discrete Mathematics 21(2)**
(2007), 423–441, DOI 10.1137/050641867 (arXiv:math/0507527). The paper text
(Section 6) states verbatim: "Theorem 6.1. For all n ≥ m ≥ 1, β(K_n □ K_m) =
( 2/3(n + m − 1), if m ≤ n ≤ 2m − 1; n − 1, if n ≥ 2m − 1." As restated by
Feng–Xu–Wang (full text, verified): "For the complete bipartite graph
K_{m,n}, Cáceres et al. proved that
μ(L(K_{m,n})) = ⌊2(m+n−1)/3⌋ for m ≤ n ≤ 2m−1, n ≥ 2; = n−1 for n ≥ 2m."
The floor convention was additionally sanity-checked by us on the triangular
prism `K_3 □ K_2`: the product formula gives ⌊2·4/3⌋ = 2, which matches the
exactly known value 2.

- [BaileyCameron2011] R. F. Bailey, P. J. Cameron, "Base size, metric
  dimension and other invariants of groups and graphs", **Bulletin of the
  London Mathematical Society 43(2)** (2011), 209–242,
  DOI 10.1112/blms/bdq096. As restated by Feng–Xu–Wang (verified): "For the
  complete graph K_n when n ≥ 6, Bailey and Cameron proved that
  μ(L(K_n)) = ⌈2n/3⌉." (This is `L(K_n) = J(n,2)`.)

- [FengXuWang2013] Min Feng, Min Xu, Kaishun Wang, "On the metric dimension of
  line graphs", **Discrete Applied Mathematics 161(6)** (April 2013),
  802–805, DOI 10.1016/j.dam.2012.10.018 (arXiv:1107.4140). Abstract,
  verified verbatim: "…we prove that ⌈log₂Δ(G)⌉ ≤ μ(L(G)) ≤ |V(G)| − 2 for a
  simple connected graph G with at least five vertices, where Δ(G) is the
  maximum degree of G." **Importantly, no exact formula for μ(L(G)) of a
  general graph is given in the literature**; the bishop colour components
  are line graphs of staircase-style bipartite graphs (see §4), which fall
  outside the solved cases above, and inside this bounded-only regime.

## 3. Bishop graphs — what was previously known

[BishopDef] General structure facts (two colour components; isomorphism of
the components iff at least one side of the board is even; component = rook
graph of a diamond-shaped board after a 45° rotation for odd square boards)
are public knowledge and documented on Wikipedia's "Bishop's graph"
(en.wikipedia.org, last edited 2025-04-12) with attribution:
"The two components are isomorphic if the board has a side of even length,
but not if both sides are odd. … A component of the bishop's graph can be
treated as a rook's graph on a diamond if the original board is square and has
sides of odd length, because if the red squares (say) are turned 45 degrees,
the bishop's moves become horizontal and vertical, just like those of the
rook." Wikipedia attributes these claims (references [1] and [2] on that
page) to R. Berghammer, **J. Logic and Algebraic Programming 81(6)** (2012),
625–642, and to J. T. Hedetniemi & S. T. Hedetniemi, "Domination in
chessboards", chapter of *Structures of Domination in Graphs*
(Developments in Mathematics 66, Springer, 2020), pp. 341–386,
DOI 10.1007/978-3-030-58892-2_12. We verified both citations as they appear
on the Wikipedia page (retrieved 2026-10-18).

Domination-type results on bishop graphs were studied by:
- [Cockayne1986] E. J. Cockayne, B. Gamble, B. Shepherd, "Domination
  parameters for the bishops graph", **Discrete Mathematics 58(3)** (1986),
  221–227, DOI 10.1016/0012-365X(86)90139-1 (verified on the Wikipedia
  bishop's-graph reference list). Per that page: minimum (independent)
  domination number of the n×n bishops graph is n; the total domination
  number is 2⌈2(n−1)/3⌉ for n ≥ 3.
- [Cockayne1990] E. J. Cockayne, "Chessboard domination problems",
  **Discrete Mathematics 86** (1990), 13–20 (verified on the Wikipedia
  reference list).

Graph diameters / radii of bishop graphs in higher dimensions:
Marco Ripà, arXiv:2311.00016 (2023) — background only; no metric dimension.

### The closest existing metric-dimension work involving bishops

[Tennenhouse2019] Craig Tennenhouse, "Metric dimension of combinatorial game
graphs", arXiv:1905.05033v2 (18 May 2019). Full text verified. Key points,
verbatim where quoted:
- He uses the two-bishop game graph `G(B(a,b), B_L b_D) ≅ B_L(a,b) □ B_D(a,b)`
  (each edge replaced by symmetric arcs) and cites Cáceres et al.'s
  Lemma 5.1 ≡ Lemma 4.1-type bound `β(G□H) ≤ β(G) + ψ(H) − 1`.
- Theorem 5.2: "1. If n > 1 then β(G(B(2,n), Bb)) = 2. 2.
  β(G(B(3,3), B_L b_D)) = β(G(B(3,4), B_L b_D)) = 3."
- Theorem 5.5: "3 ≤ β(G(B(3,n), B_L b_D)) ≤ 4".
- **Not covered:** the metric dimension of the *components themselves*
  (`B_L(n,n)` and `B_D(n,n)`) on arbitrary square boards, and therefore also
  not `dim(B(n,n))` itself. All results are for 2×n, 3×n strips and for the
  *product graph* of the two components (loopy bishop game).

### Direct-product/diagonal Hamming analogues

[FosterGreenwoodUhl2024] Briana Foster-Greenwood, Christine Uhl, "Metric
Dimension of a Direct Product of Three Complete Graphs", **The Electronic
Journal of Combinatorics 31(2)** (2024), #P2.13, DOI 10.37236/12399
(preprint arXiv:2208.01519, "…of a Diagonal Family of Generalized Hamming
Graphs"). Verified abstract and Theorem 17: diagonal family HG(n,n,n;3) ≅
K_n×K_n×K_n has metric dimension 2n for n ∈ {3,4} and 2n − 1 for n ≥ 5.
Their opening framing is exactly our setting one dimension up: they phrase
the problem as the "landmark sees all cells sharing a coordinate" puzzle on
boards; our paper answers the 2-dimensional *diagonal-only* (bishop) case.

## 4. Positioning of this work

- The bishop colour components are line graphs of explicit sparse bipartite
  graphs ("diamond staircases"), NOT of K_{m,n} or K_n, so the exact Cáceres
  et al. theorem does not apply; Feng–Xu–Wang provide only general bounds for
  line graphs. No prior publication computes `dim` of bishop colour
  components on unsized square boards — all bishop metric-dimension literature
  (Tennenhouse 2019) addresses either 2×n/3×n strips (where components are
  paths or small graphs) or the product game graph.
- Our contribution: (i) a complete formal treatment of the diamond rook-board
  reformulation, including a proven three-rule characterization of resolving
  sets grounded in a diameter-two lemma; (ii) exact metric dimensions of both
  colour components for every board size 1 ≤ n ≤ 24 computed by exact set
  cover ILP with three-fold independent verification; (iii) closed-form
  conjectures for all three geometric cases up to n = 24 with the observed
  7/6-per-unit asymptotics; (iv) necessary conditions proved (empty-row /
  empty-column structure, singleton-star obstruction) and explicit optimal
  configurations reported.

## 5. Unverified / uncertain items (do not cite as fact without checking)

- Kuziak–Yero survey on metric-dimension variants (arXiv 2107.04877): the
  exact title was not re-verified in this session; if cited in the final
  manuscript it must be re-verified first.
- Whether any 2025–2026 preprint computes metric dimension of "diamond rook
  graphs" or "bishop metric dimension" under different terminology: the
  searches performed (metrics: "bishop graph metric dimension", "diamond rook
  graph metric dimension" 2023–2026) found no such work, but a final check
  at submission time is prudent.
