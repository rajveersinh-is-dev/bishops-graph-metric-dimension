"""Two-phase exact metric-dimension verification for bishop colour components.

Given a target k (e.g. the conjectured dimension), the exact dimension is
certified by combining:
  A) an exact ILP showing that NO resolving set of size <= k-1 exists
     (feasibility problem, expected status "infeasible"), and
  B) an exact ILP minimising |S| among resolving sets subject to |S| <= k,
     which returns a proven-optimal value k' <= k (independently re-verified
     as an actual resolving set by pure distance checks).

If A is infeasible and B returns k', then dim = k' (infeasibility for
<='k-1 implies infeasibility for <='k'-1 since k'-1 <= k-1).  If B comes
back infeasible, k is too small and the ladder retries with k+1+...; if A is
feasible (conjecture too large), the found set shrinks k and the ladder
repeats from the smaller size.

Distance model: component distance = diamond rook distance 0/1/2 (valid by
the diameter-two lemma, proved in paper/ and machine-checked in tests).

Run:  python src/fast_verify.py <lo> <hi> [results_file]
"""
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bishop import bishop_components, component_distances

TIME_LIMIT = 1800  # seconds per ILP call


def to_uv(cell, comp):
    r, c = cell.r, cell.c
    if comp == "even":
        return ((r - c) // 2, (r + c) // 2)
    return ((r - c - 1) // 2, (r + c - 1) // 2)


def d_rook(x, y):
    if x == y:
        return 0
    if x[0] == y[0] or x[1] == y[1]:
        return 1
    return 2


def build(verts):
    """Pair-resolver incidence as a dense 0/1 numpy array (m x nump)."""
    pairs = list(itertools.combinations(verts, 2))
    m, nump = len(verts), len(pairs)
    B = np.zeros((m, nump), dtype=np.float64)
    for k, (x, y) in enumerate(pairs):
        for i, s in enumerate(verts):
            if d_rook(s, x) != d_rook(s, y):
                B[i, k] = 1.0
    return pairs, B


def run_ilp(B, bound, minimize, note):
    """min 1'x  (or 0'x) s.t. B'x >= 1, x binary, sum x <= bound."""
    m, nump = B.shape
    c = np.ones(m) if minimize else np.zeros(m)
    cons = [
        LinearConstraint(csc_matrix(B.T), lb=np.ones(nump), ub=np.full(nump, np.inf)),
    ]
    if bound is not None:
        cons.append(LinearConstraint(np.ones((1, m)), lb=-np.inf, ub=[bound]))
    mip = milp(
        c=c,
        integrality=np.ones(m, dtype=int),
        bounds=Bounds(0, 1),
        constraints=cons,
        options={"mip_rel_gap": 0.0, "time_limit": TIME_LIMIT, "presolve": True},
    )
    status = int(mip.status)
    size = None
    chosen = None
    if mip.x is not None:
        chosen = [i for i in range(m) if mip.x[i] > 0.5]
        size = len(chosen)
    print(
        f"    ILP[{note}]: status={status} size={size} t={time.strftime('%H:%M:%S')}",
        flush=True,
    )
    return status, size, chosen


def verify_resolving(verts, chosen_idx):
    S = [verts[i] for i in chosen_idx]
    for x, y in itertools.combinations(verts, 2):
        if all(d_rook(s, x) == d_rook(s, y) for s in S):
            return False
    return True


def conjecture_dim(n, comp, edge):
    """The closed-form candidates conjectured from the n<=16 data.

    Expressed exactly as in src/conjecture_check.py:
      even n:  dim of either component  = floor((7n - 8) / 6)
      odd  n:  corner ("even") comp     = floor((7n - 5) / 6)
               anti ("odd") comp        = floor((7n - 11) / 6), n>=5
                                        (n=3 exceptional: dim = 2)
    """
    if n % 2 == 0:
        return (7 * n - 8) // 6
    if comp == "even":
        return (7 * n - 5) // 6
    return 2 if n == 3 else (7 * n - 11) // 6


def lower_bound(n, edge):
    """Proved necessary-condition bound min(rows, cols) - 1 = edge - 1."""
    return max(edge - 1, 1)


def solve_component(n, comp, edge, k_start):
    verts = [to_uv(c, comp) for c in bishop_components(n)[0 if comp == "even" else 1]]
    verts = sorted(set(verts))
    pairs, B = build(verts)
    print(f"  n={n} comp={comp}: |V|={len(verts)} pairs={len(pairs)} k_start={k_start}", flush=True)
    k = k_start
    while True:
        t0 = time.time()
        # Phase A: prove infeasibility at <= k-1
        a_status, _, _ = run_ilp(B, k - 1, False, f"A n={n} {comp} bound={k-1}")
        if a_status == 1:
            print(f"    phase A TIME LIMIT at bound {k-1}; cannot certify lower side", flush=True)
            return None
        if a_status == 0:
            print(f"    phase A FEASIBLE at bound {k-1} -> k too large, ladder down", flush=True)
            k -= 1
            continue
        if a_status != 2:
            print(f"    phase A unexpected status {a_status}", flush=True)
            return None
        tA = time.time() - t0
        print(f"    phase A infeasible at {k-1} confirmed ({tA:.1f}s)", flush=True)
        # Phase B: minimise |S| among resolving sets with |S| <= k
        t1 = time.time()
        b_status, b_size, b_chosen = run_ilp(B, k, True, f"B n={n} {comp} bound={k}")
        if b_status == 1:
            print(f"    phase B TIME LIMIT at bound {k}", flush=True)
            return None
        if b_status == 2:
            print(f"    phase B INFEASIBLE at {k} -> ladder up", flush=True)
            k += 1
            continue
        if b_status != 0:
            print(f"    phase B unexpected status {b_status}", flush=True)
            return None
        tB = time.time() - t1
        if not verify_resolving(verts, b_chosen):
            print("    IMPOSSIBLE: phase B solution failed independent verification", flush=True)
            raise RuntimeError("verification failure")
        print(f"    phase B optimal {b_size} verified resolving ({tB:.1f}s)", flush=True)
        result = {
            "dim": b_size,
            "cert": f"infeasible<={k-1} + optimal={b_size}<= {k}",
            "basis_uv": [list(verts[i]) for i in b_chosen],
        }
        return result


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).resolve().parents[1] / "results" / f"dims_fast_{lo}_{hi}.json"
    data = json.loads(out_path.read_text()) if out_path.exists() else {}

    for n in range(lo, hi + 1):
        rec = {"n": n}
        for comp in ("even", "odd"):
            edge = n - 1
            k0 = conjecture_dim(n, comp, edge)
            start = max(lower_bound(n, edge), k0 - 1)
            res = solve_component(n, comp, edge, k0)
            if res is None:
                print(f"  n={n} comp={comp}: NOT CERTIFIED within limits", flush=True)
                continue
            rec[f"dim_{comp}"] = res["dim"]
            rec[f"basis_{comp}"] = res["basis_uv"]
            rec[f"cert_{comp}"] = res["cert"]
        rec["total"] = rec.get("dim_even", -1) + rec.get("dim_odd", -1)
        done = all(k in rec for k in ("dim_even", "dim_odd"))
        if done:
            # merge with any previous record for this n (keep old basis if new missing)
            data[str(n)] = rec
            out_path.write_text(json.dumps(data, indent=1))
            print(f"  n={n} SAVED dim_even={rec['dim_even']} dim_odd={rec['dim_odd']} total={rec['total']}", flush=True)
    print(f"wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
