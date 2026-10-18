"""Check the closed-form dimension conjectures against exact results.

Conjectures (n = board side length):
  even n:  dim of either component  = floor((7n - 8) / 6)
           equivalently, with W = n - 1 rows: dim = W + floor(W / 6)
  odd  n:  corner component (the colour class containing the board corners,
           D_{n-1})         = floor((7n - 5) / 6)   (= n-1 + floor((n+1)/6))
           anti component   = floor((7n - 11) / 6)  (= n-2 + floor((n-5)/6)),
                                     with n = 3 an exception (dim = 2).

Run:  python src/conjecture_check.py      (uses every results/dims_*.json)
"""
import json
import math
import sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"


def conjectures(n: int):
    if n % 2 == 0:
        return {
            "even": math.floor((7 * n - 8) / 6),
            "odd": math.floor((7 * n - 8) / 6),
        }
    even = math.floor((7 * n - 5) / 6)
    odd = 2 if n == 3 else math.floor((7 * n - 11) / 6)
    return {"even": even, "odd": odd}


def main() -> int:
    ok = True
    print(f"{'n':>3} {'comp':>5} {'exact':>5} {'conj':>5} {'ok':>3}")
    for path in sorted(RES.glob("dims_*.json")):
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            recs = [{"n": int(key), **val} for key, val in data.items()]
        else:
            recs = data
        for rec in recs:
            n = rec["n"]
            conj = conjectures(n)
            for comp in ("even", "odd"):
                exact = rec[f"dim_{comp}"]
                good = exact == conj[comp]
                ok &= good
                print(f"{n:3d} {comp:>5} {exact:5d} {conj[comp]:5d} {'Y' if good else 'N'}")
    print("\nALL MATCH" if ok else "\nMISMATCH FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
