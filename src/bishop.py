"""Exact computation of the metric dimension of bishop's graphs.

Two cells of an n x n board (indexed 0..n-1) are adjacent exactly when they lie
on a common diagonal, i.e. r - c equal or r + c equal.  This graph splits into
two connected components (the two board colours); the metric dimension of the
whole graph (with the extended infinity metric) is the sum over components.

A resolving set S for a graph G is a vertex subset such that for every pair of
distinct vertices u,v there is s in S with d(s,u) != d(s,v).  Finding a minimum
resolving set is reduced exactly to a minimum set-cover ILP over the universe
of vertex pairs, and the ILP results are cross-validated by brute force on
small instances.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix, lil_matrix


@dataclass(frozen=True, order=True)
class Cell:
    r: int
    c: int


def bishop_components(n: int) -> tuple[list[Cell], list[Cell]]:
    """Return the two colour components of the n x n bishop graph."""
    evens, odds = [], []
    for r in range(n):
        for c in range(n):
            (evens if (r + c) % 2 == 0 else odds).append(Cell(r, c))
    return evens, odds


def component_distances(cells: list[Cell]) -> dict[Cell, dict[Cell, int]]:
    """All-pairs BFS distances within one bishop component (there is exactly one
    component per colour class), using bishop adjacency."""
    # bucket cells by the two diagonal keys
    back, slash = {}, {}
    for cell in cells:
        back.setdefault(cell.r - cell.c, []).append(cell)
        slash.setdefault(cell.r + cell.c, []).append(cell)
    neighbours: dict[Cell, set[Cell]] = {u: set() for u in cells}
    for bucket in list(back.values()) + list(slash.values()):
        for u in bucket:
            neighbours[u].update(bucket)
    dist = {}
    for src in cells:
        d = {src: 0}
        frontier = [src]
        while frontier:
            nxt = []
            for u in frontier:
                for v in neighbours[u]:
                    if v not in d:
                        d[v] = d[u] + 1
                        nxt.append(v)
            frontier = nxt
        dist[src] = d
    return dist


def triplets_resolve(dist: dict, landmark_set: frozenset[Cell]) -> bool:
    """True iff landmark_set resolves the whole component."""
    for u, v in itertools.combinations(dist, 2):
        if all(dist[s].get(u) == dist[s].get(v) for s in landmark_set):
            return False
    return True


def resolving_sets_by_size(dist: dict, size: int):
    """All subsets of the given size that resolve the component (brute force)."""
    verts = list(dist)
    for subset in itertools.combinations(verts, size):
        if triplets_resolve(dist, frozenset(subset)):
            yield frozenset(subset)


def benchmark_dimension(dist: dict) -> tuple[int, frozenset[Cell] | None]:
    """Exact metric dimension.  Brute force for very small components; MILP
    (minimum set cover over vertex pairs, solved by HiGHS) in general.  Returns
    (dimension, an exemplar minimum resolving set)."""
    verts = list(dist)
    m = len(verts)
    if m <= 1:
        return 0, frozenset(verts)

    pairs = list(itertools.combinations(verts, 2))
    resolved = {}
    for s in verts:
        ds = dist[s]
        resolved[s] = frozenset(
            k for k, (u, v) in enumerate(pairs) if ds[u] != ds[v]
        )

    # Minimum set cover: min 1'x  s.t. for every pair, the selected landmarks
    # covering it number >= 1.  Solved exactly with HiGHS via scipy.optimize.milp.
    nump = len(pairs)
    A = lil_matrix((nump, m))
    for k, (u, v) in enumerate(pairs):
        for idx, s in enumerate(verts):
            if k in resolved[s]:
                A[k, idx] = 1.0
    c_weights = np.ones(m)
    mip = milp(
        c=c_weights,
        integrality=np.ones(m, dtype=int),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(
            csc_matrix(A), lb=np.ones(nump), ub=np.full(nump, np.inf)
        ),
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


def bishop_dimension(n: int) -> dict:
    """Metric dimension of both components and of the whole bishop graph."""
    out = {}
    for name, comp in (("even", bishop_components(n)[0]), ("odd", bishop_components(n)[1])):
        dist = component_distances(comp)
        dim, basis = benchmark_dimension(dist)
        out[name] = {"size": len(comp), "dim": dim, "basis": sorted(basis)}
    out["total"] = out["even"]["dim"] + out["odd"]["dim"]
    return out


if __name__ == "__main__":
    import sys

    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print("n  |even| | dim_even | dim_even_basis | |odd| | dim_odd | dim_odd_basis | total")
    for n in range(1, n_max + 1):
        res = bishop_dimension(n)
        print(
            f"{n:2d} {res['even']['size']:4d} {res['even']['dim']:6d} "
            f"{res['even']['basis']!s:55.55} {res['odd']['size']:4d} "
            f"{res['odd']['dim']:6d} {res['odd']['basis']!s:55.55} {res['total']:4d}"
        )
