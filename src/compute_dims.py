"""Compute exact metric dimensions of bishop graphs for a range of n and save
to JSON, printing full metric bases."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bishop import bishop_components, component_distances, benchmark_dimension


def main() -> None:
    lo, hi = (int(a) for a in sys.argv[1:3])
    out = []
    for n in range(lo, hi + 1):
        rec = {"n": n}
        for name, comp in zip(("even", "odd"), bishop_components(n)):
            dist = component_distances(comp)
            dim, basis = benchmark_dimension(dist)
            rec[f"dim_{name}"] = dim
            rec[f"basis_{name}"] = [[c.r, c.c] for c in sorted(basis)]
            rec[f"size_{name}"] = len(comp)
        rec["total"] = rec["dim_even"] + rec["dim_odd"]
        out.append(rec)
        b_e = [(c[0], c[1]) for c in rec["basis_even"]]
        b_o = [(c[0], c[1]) for c in rec["basis_odd"]]
        print(
            f"n={n:2d} dim_even={rec['dim_even']:3d} dim_odd={rec['dim_odd']:3d} "
            f"total={rec['total']:3d}  basis_even={b_e}  basis_odd={b_o}",
            flush=True,
        )
    path = Path(__file__).resolve().parents[1] / "results"
    path.mkdir(exist_ok=True)
    (path / f"dims_{lo}_{hi}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
