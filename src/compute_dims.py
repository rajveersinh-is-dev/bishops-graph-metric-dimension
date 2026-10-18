"""Compute exact metric dimensions of bishop graphs for a range of n and save
to JSON, printing full metric bases.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bishop import bishop_components, component_distances, benchmark_dimension


def _parse_args(argv: List[str]) -> Tuple[int, int]:
    """Parse two integer command‑line arguments.

    Args:
        argv: List of command‑line arguments (excluding the program name).

    Returns:
        A tuple (lo, hi) of integers.

    Raises:
        SystemExit: If the arguments are missing or not integers.
    """
    if len(argv) < 2:
        prog = Path(sys.argv[0]).name
        print(f"Usage: {prog} <lo> <hi>", file=sys.stderr)
        sys.exit(1)
    try:
        lo = int(argv[0])
        hi = int(argv[1])
    except ValueError:
        print("Both arguments must be integers.", file=sys.stderr)
        sys.exit(1)
    return lo, hi


def main() -> None:
    """Entry point: compute dimensions for n in [lo, hi] and write results."""
    lo, hi = _parse_args(sys.argv[1:])

    out: List[Dict[str, Any]] = []
    for n in range(lo, hi + 1):
        rec: Dict[str, Any] = {"n": n}
        for name, comp in zip(("even", "odd"), bishop_components(n)):
            dist = component_distances(comp)
            dim, basis = benchmark_dimension(dist)
            rec[f"dim_{name}"] = dim
            # Store basis as list of [r, c] pairs, sorted for deterministic output
            rec[f"basis_{name}"] = [[c.r, c.c] for c in sorted(basis)]
            rec[f"size_{name}"] = len(comp)
        rec["total"] = rec["dim_even"] + rec["dim_odd"]
        out.append(rec)

        # Pretty‑print progress
        b_e: List[Tuple[int, int]] = [(c[0], c[1]) for c in rec["basis_even"]]
        b_o: List[Tuple[int, int]] = [(c[0], c[1]) for c in rec["basis_odd"]]
        print(
            f"n={n:2d} dim_even={rec['dim_even']:3d} dim_odd={rec['dim_odd']:3d} "
            f"total={rec['total']:3d}  basis_even={b_e}  basis_odd={b_o}",
            flush=True,
        )

    # Write results to JSON
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(exist_ok=True)
    out_file = results_dir / f"dims_{lo}_{hi}.json"
    out_file.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
