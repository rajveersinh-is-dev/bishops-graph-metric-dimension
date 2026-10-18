# The exact metric dimension of the bishop's graph

LaTeX source for the manuscript (author: Rajveersinh Vishal Pardeshi).

## Files

| File | Contents |
|---|---|
| `main.tex` | Manuscript source (compiles with Tectonic 0.17) |
| `references.bib` | Bibliography, 13 entries, source-verified |
| `tables_auto.tex` | Auto-generated: defines `\nmaxverified` (must load before the abstract) |
| `tables_auto_body.tex` | Auto-generated body of Table `tab:results` |
| `fig_n9.tex` | Auto-generated tikzpicture for Figure `fig:figN9` (n=9 optimal set) |
| `README.md` | This file |

`tables_auto.tex`, `tables_auto_body.tex` and `fig_n9.tex` are **generated artefacts**, produced from the certified result data in `results/` by `src/make_paper_assets.py` (run from the repository root). They are checked into this directory for convenience; regenerate whenever `results/dims_*.json` changes. The generator asserts every invariant it prints (component sizes, basis membership, conjecture agreement, and the figure-9 landmark list against this manuscript's caption).

## Compilation

```
cd paper
tectonic main.tex   # Tectonic 0.17
```

All cross-references and citations resolve; the PDF is produced without warnings. BibTeX is not required (thebibliography-style handling is inline in `main.tex`).

## Data provenance

All numbers in the paper come from `results/dims_2_16.json` (exact ILP dimensions n=2..16, certified by two-phase infeasibility + bounded optimum, HiGHS `mip_rel_gap=0`) and, once added, `results/dims_17_24.json` (n=17..24, same certification). Independent cross-checks: BFS re-verification, the structural rule oracle in `src/structure.py`, brute force for n<=5 (`tests/test_bishop.py`), and conjecture regression (`src/conjecture_check.py`). LP relaxation measurements cited in the manuscript are `results/lp_results.json`; canonical optima for exhibits n<=10 are `results/canonical_sets.json`.

## Journal route

Prepared for submission to an Oxford University Press journal via its standard licence route (OA optional, no mandatory author fee); see the journal's published instructions page for current policy.
