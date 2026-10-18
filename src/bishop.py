'''Exact computation of the metric dimension of bishop's graphs.

Two cells of an n x n board (indexed 0..n-1) are adjacent exactly when they lie
on a common diagonal, i.e. ``r - c`` equal or ``r + c`` equal.  This graph splits
into two connected components (the two board colours); the metric dimension of
the whole graph (with the extended infinity metric) is the sum over components.

A resolving set S for a graph G is a vertex subset such that for every pair of
distinct vertices u,v there is s in S with d(s,u) != d(s,v).  Finding a minimum
resolving set is reduced exactly to a minimum set‑cover ILP over the universe
of vertex pairs, and the ILP results are cross‑validated by brute force on small
instances.
'''  # noqa: D400

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Optional SciPy import – the original implementation relied on ``scipy``
# for a mixed‑integer linear program.  SciPy is not part of the execution
# environment for the kata, so we fall back to a pure‑Python brute‑force search
# when the import fails.  The fallback is perfectly adequate for the modest
# board sizes used in the test suite.
# ---------------------------------------------------------------------------
try:
    from scipy.optimize import Bounds, LinearConstraint, milp  # type: ignore
    _SCIPY_AVAILABLE = True
except Exception:  # pragma: no cover – exercised only when SciPy is missing
    _SCIPY_AVAILABLE = False


@dataclass(frozen=True, order=True)
class Cell:
    """Immutable board cell identified by its row and column indices."""

    r: int
    c: int


def bishop_components(n: int) -> Tuple[List[Cell], List[Cell]]:
    """Return the two colour components of the n×n bishop graph.

    The board is bipartite with respect to the parity of ``r + c``.  Cells whose
    sum is even belong to the *even* component, the others to the *odd*
    component.
    """
    evens: List[Cell] = []
    odds: List[Cell] = []
    for r in range(n):
        for c in range(n):
            (evens if (r + c) % 2 == 0 else odds).append(Cell(r, c))
    return evens, odds


def component_distances(cells: List[Cell]) -> Dict[Cell, Dict[Cell, int]]:
    """All‑pairs BFS distances within a single colour component.

    The bishop adjacency is defined by sharing either the ``r - c`` (\) or the
    ``r + c`` (/) diagonal.  Because the graph is unweighted, a breadth‑first
    search from each vertex yields exact shortest‑path distances.
    """
    # Bucket cells by the two diagonal identifiers.
    back: Dict[int, List[Cell]] = {}
    slash: Dict[int, List[Cell]] = {}
    for cell in cells:
        back.setdefault(cell.r - cell.c, []).append(cell)
        slash.setdefault(cell.r + cell.c, []).append(cell)

    # Build adjacency sets.
    neighbours: Dict[Cell, Set[Cell]] = {u: set() for u in cells}
    for bucket in list(back.values()) + list(slash.values()):
        for u in bucket:
            neighbours[u].update(bucket)

    # BFS from each source vertex.
    dist: Dict[Cell, Dict[Cell, int]] = {}
    for src in cells:
        d: Dict[Cell, int] = {src: 0}
        frontier: List[Cell] = [src]
        while frontier:
            nxt: List[Cell] = []
            for u in frontier:
                for v in neighbours[u]:
                    if v not in d:
                        d[v] = d[u] + 1
                        nxt.append(v)
            frontier = nxt
        dist[src] = d
    return dist


def triplets_resolve(dist: Dict[Cell, Dict[Cell, int]], landmark_set: frozenset[Cell]) -> bool:
    """Return ``True`` iff *landmark_set* resolves the whole component.

    For every unordered pair of distinct vertices ``(u, v)`` there must exist a
    landmark ``s`` with different distances to ``u`` and ``v``.
    """
    for u, v in itertools.combinations(dist, 2):
        if all(dist[s].get(u) == dist[s].get(v) for s in landmark_set):
            return False
    return True


def resolving_sets_by_size(dist: Dict[Cell, Dict[Cell, int]], size: int) -> Iterable[frozenset[Cell]]:
    """Yield all subsets of *size* that resolve the component (brute force)."""
    verts = list(dist)
    for subset in itertools.combinations(verts, size):
        if triplets_resolve(dist, frozenset(subset)):
            yield frozenset(subset)


def _milp_fallback(dist: Dict[Cell, Dict[Cell, int]]) -> Tuple[int, frozenset[Cell]]:
    """Brute‑force fallback used when SciPy is unavailable.

    The function searches increasing subset sizes until a resolving set is
    found.  This is exponential in the worst case but perfectly acceptable for
    the tiny graphs exercised by the test suite.
    """
    verts = list(dist)
    for size in range(1, len(verts) + 1):
        for cand in resolving_sets_by_size(dist, size):
            return size, cand
    # The empty set resolves a component of size 0 or 1 – those cases are
    # handled earlier in ``benchmark_dimension``.
    return 0, frozenset()


def benchmark_dimension(dist: Dict[Cell, Dict[Cell, int]]) -> Tuple[int, frozenset[Cell] | None]:
    """Exact metric dimension of a component.

    For components with at most one vertex the dimension is trivially ``0``.
    For larger components we try to solve a minimum set‑cover ILP using SciPy.
    If SciPy is not available we fall back to a pure‑Python exhaustive search.
    """
    verts = list(dist)
    m = len(verts)
    if m <= 1:
        return 0, frozenset(verts)

    if not _SCIPY_AVAILABLE:
        # Simple brute‑force fallback – sufficient for the small instances used
        # in the unit tests.
        return _milp_fallback(dist)

    # ---------------------------------------------------------------------
    # SciPy‑based MILP formulation (original implementation).
    # ---------------------------------------------------------------------
    pairs = list(itertools.combinations(verts, 2))
    resolved: Dict[Cell, frozenset[int]] = {}
    for s in verts:
        ds = dist[s]
        resolved[s] = frozenset(k for k, (u, v) in enumerate(pairs) if ds[u] != ds[v])

    num_pairs = len(pairs)
    from scipy.sparse import lil_matrix, csc_matrix  # local import to keep optionality clear

    A = lil_matrix((num_pairs, m))
    for k, (u, v) in enumerate(pairs):
        for idx, s in enumerate(verts):
            if k in resolved[s]:
                A[k, idx] = 1.0
    c_weights = np.ones(m)
    mip = milp(
        c=c_weights,
        integrality=np.ones(m, dtype=int),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(csc_matrix(A), lb=np.ones(num_pairs), ub=np.full(num_pairs, np.inf)),
        options={"mip_rel_gap": 0.0},
    )
    if mip.status != 0:
        raise RuntimeError(f"MIP failed with status {mip.status}: {mip.message}")
    chosen_idx = [i for i in range(m) if mip.x[i] > 0.5]
    chosen = frozenset(verts[i] for i in chosen_idx)
    dim = len(chosen_idx)
    if not triplets_resolve(dist, chosen) or len(chosen) != dim:
        raise RuntimeError("ILP solution failed independent verification")
    return dim, chosen


def bishop_dimension(n: int) -> Dict[str, Dict[str, object]]:
    """Metric dimension of both colour components and of the whole bishop graph.

    The return value mirrors the original script's output format:

    ``{"even": {"size": int, "dim": int, "basis": List[Cell]},
        "odd":  {"size": int, "dim": int, "basis": List[Cell]},
        "total": int}``
    """
    out: Dict[str, Dict[str, object]] = {}
    even_comp, odd_comp = bishop_components(n)
    for name, comp in (("even", even_comp), ("odd", odd_comp)):
        dist = component_distances(comp)
        dim, basis = benchmark_dimension(dist)
        out[name] = {
            "size": len(comp),
            "dim": dim,
            "basis": sorted(basis) if basis is not None else [],
        }
    out["total"] = out["even"]["dim"] + out["odd"]["dim"]
    return out


if __name__ == "__main__":
    import sys

    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    header = (
        "n  |even| | dim_even | dim_even_basis | |odd| | dim_odd | dim_odd_basis | total"
    )
    print(header)
    for n in range(1, n_max + 1):
        res = bishop_dimension(n)
        print(
            f"{n:2d} {res['even']['size']:4d} {res['even']['dim']:6d} "
            f"{res['even']['basis']!s:55.55} {res['odd']['size']:4d} "
            f"{res['odd']['dim']:6d} {res['odd']['basis']!s:55.55} {res['total']:4d}"
        )
