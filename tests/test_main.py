import importlib.util
import pathlib
import sys

# Load the module from the repository path without executing top‑level script code.
module_path = pathlib.Path('bishop.py')
spec = importlib.util.spec_from_file_location('bishop', module_path)
bishop = importlib.util.module_from_spec(spec)
sys.modules['bishop'] = bishop
spec.loader.exec_module(bishop)

def test_bishop_dimension_small_cases():
    # n = 1: only one even cell, no odd cells.
    res1 = bishop.bishop_dimension(1)
    assert res1['total'] == 0
    assert res1['even']['dim'] == 0
    assert res1['odd']['dim'] == 0
    # n = 2: each colour component has two cells that are adjacent.
    res2 = bishop.bishop_dimension(2)
    assert res2['even']['dim'] == 1
    assert res2['odd']['dim'] == 1
    assert res2['total'] == 2
    # Verify that the returned basis sets actually resolve their components.
    for comp_name in ('even', 'odd'):
        comp_cells = bishop.bishop_components(2)[0] if comp_name == 'even' else bishop.bishop_components(2)[1]
        dist = bishop.component_distances(comp_cells)
        basis = frozenset(res2[comp_name]['basis'])
        assert bishop.triplets_resolve(dist, basis)
