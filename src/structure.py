"""Structural characterization of resolving sets on bishop colour components.

A colour component of the n x n bishop graph, in coordinates
    u = r - c,  v = r + c  (scaled by 1/2 within one colour class),
is the rook graph of a "diamond board": adjacency <=> shared row or column.
We proved (see paper/):

Lemma (diameter two).  Every two cells of the component are at rook distance
0, 1 or 2; in particular, for any two cells with distinct rows and columns at
least one of the two "cross cells" (u1, v2), (u2, v1) lies in the board.

Theorem (three rules).  A landmark set S resolves the component if and only if
every pair of distinct cells x != y is resolved, and for the 0/1/2 rook metric
this is equivalent to the following rules holding for all relevant pairs:
  (R-col)   same-column pair (u1,v), (u2,v): resolved iff landmark lies on
            row u1 or row u2;
  (R-row)   same-row pair: symmetric in columns;
  (R-cross) cross pair (u1,v1), (u2,v2), u1 != u2, v1 != v2 (exists only when
            a cross cell exists): resolved iff some landmark lies on one of
            the four lines row u1, row u2, col v1, col v2 other than the two
            cross cells (u1,v2), (u2,v1).

This module implements the rule oracle, used to independently verify every
optimal resolving set reported in results/.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass

from bishop import Cell


def to_uv(cell: Cell, comp: str) -> tuple[int, int]:
    """Map a board cell to component rook coordinates."""
    r, c = cell.r, cell.c
    if comp == "even":
        return ((r - c) // 2, (r + c) // 2)
    return ((r - c - 1) // 2, (r + c - 1) // 2)


def component_uv(n: int, comp: str) -> list[tuple[int, int]]:
    """All cells of one colour component in rook coordinates."""
    out = []
    for r in range(n):
        for c in range(n):
            if ((r + c) % 2 == 0) == (comp == "even"):
                out.append(to_uv(Cell(r, c), comp))
    return out


def rook_distance(x: tuple[int, int], y: tuple[int, int]) -> int:
    """Rook-of-diamond distance: 0 same cell, 1 share row/column, else 2.

    Valid because every two cells with distinct rows and columns have at
    least one cross cell in the board (diameter-two lemma)."""
    if x == y:
        return 0
    if x[0] == y[0] or x[1] == y[1]:
        return 1
    return 2


def rules_disagree(
    cells: list[tuple[int, int]], resolving: set[tuple[int, int]]
) -> int:
    """Count cell pairs whose resolution verdict differs between the three
    rules and direct distance computation.  0 means fully consistent."""
    S = set(resolving)
    row_has = {}
    col_has = {}
    for u, v in S:
        row_has.setdefault(u, set()).add(v)
        col_has.setdefault(v, set()).add(u)
    bad = 0
    for x, y in itertools.combinations(cells, 2):
        # direct: is some landmark distinguishing?
        direct = any(
            rook_distance(s, x) != rook_distance(s, y) for s in S
        )
        u1, v1 = x
        u2, v2 = y
        if v1 == v2 and u1 != u2:                      # same column
            rule = bool(row_has.get(u1)) or bool(row_has.get(u2))
        elif u1 == u2 and v1 != v2:                    # same row
            rule = bool(col_has.get(v1)) or bool(col_has.get(v2))
        else:                                          # cross pair
            crosses = {(u1, v2), (u2, v1)}
            marks_on_lines = {
                s for s in S if s[0] in (u1, u2) or s[1] in (v1, v2)
            }
            rule = any(m not in crosses for m in marks_on_lines)
        if direct != rule:
            bad += 1
    return bad


def verify_rules_and_resolution(
    cells: list[tuple[int, int]], resolving: set[tuple[int, int]]
) -> bool:
    """True iff resolving is a resolving set AND the rules agree."""
    if rules_disagree(cells, resolving) != 0:
        return False
    for x, y in itertools.combinations(cells, 2):
        if all(rook_distance(s, x) == rook_distance(s, y) for s in resolving):
            return False
    return True
