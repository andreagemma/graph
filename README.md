# GA Graph

[![CI](https://github.com/andreagemma/graph/actions/workflows/ci.yml/badge.svg)](https://github.com/andreagemma/graph/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/ga-graph.svg)](https://pypi.org/project/ga-graph/)
[![Python](https://img.shields.io/pypi/pyversions/ga-graph.svg)](https://pypi.org/project/ga-graph/)

GA Graph provides lightweight dictionary-backed graph containers, path
collections, turn classification helpers, and a link-based time-dependent
shortest-path router.

The PyPI distribution is named `ga-graph`; the import package is named `graph`.

## Installation

```bash
python -m pip install ga-graph
```

Development and test tools are available as extras:

```bash
python -m pip install -e ".[test]"
python -m pip install -e ".[dev]"
```

## Quick Start

```python
from graph import Graph

network = Graph(total_time=60, delta_t=15)
network.add_node("A")
network.add_node("B")
network.add_link("ab", "A", "B", cost=5)

assert network.get_link("ab").i == "A"
assert network.get_node_degree("A", include_in_links=False) == 1
```

## Graphs

`Graph` stores nodes, directed links, and turns in dictionary-backed containers.
Each entity keeps a required identifier plus arbitrary extra attributes.

```python
from graph import ActionPolicy, Graph

network = Graph()
network.add_link(
    "ab",
    "A",
    "B",
    on_missing_node=ActionPolicy.REPLACE,
    capacity=1200,
)
network.add_turn("ab_bc", "ab", "bc", on_missing_link=ActionPolicy.IGNORE)
```

Duplicate and missing references can be handled with `ActionPolicy.RAISE`,
`WARN`, `IGNORE`, `REPLACE`, or `SKIP`, depending on the method.

## Paths

`Path` stores a source, target, departure time, optional mode, link sequence, and
cumulative costs. `PathList` stores one path per `(source, target, t_start,
mode)` key. `KPathList` stores multiple ranked paths for the same key.

```python
from graph import KPathList, Path

paths = KPathList()
paths.add_path(Path("A", "C", 0, links=["ab", "bc"], costs=[5, 9], mode="car"))
paths.add_path(Path("A", "C", 0, links=["ac"], costs=[12], mode="car"))

best = paths.path("A", "C", 0, "car", k=0)
second = paths.path("A", "C", 0, "car", k=1)
```

## Time-Dependent Routing

`TimeDependentLinkBasedShortestPath` builds a dense routing view from a `Graph`.
Scalar costs are expanded across the graph time horizon; sequence costs are used
as piecewise-constant time profiles.

```python
from graph import Graph, TimeDependentLinkBasedShortestPath

network = Graph(total_time=60, delta_t=15)
for node in ["A", "B", "C"]:
    network.add_node(node, cost=0)

network.add_link("ab", "A", "B", cost=1)
network.add_link("bc", "B", "C", cost=1)
network.add_link("ac", "A", "C", cost=10)

router = TimeDependentLinkBasedShortestPath.from_graph(network, link_cost_field="cost")
path = router.shortest_paths("A", "C").path("A", "C", 0, None)

assert path.get_links() == ("ab", "bc")
assert path["tot_cost"] == 2
```

The router supports optional mode fields, node costs, turn costs, and prohibited
turn fields.

## API Summary

- `Graph(t0=0, total_time=60, delta_t=15, **kwargs)`
- `Graph.add_node(idx, on_existing=ActionPolicy.RAISE, **kwargs)`
- `Graph.add_link(idx, i, j, on_existing=..., on_missing_node=..., **kwargs)`
- `Graph.add_turn(idx, in_link, out_link, on_existing=..., on_missing_link=..., **kwargs)`
- `Graph.get_node(idx)`, `Graph.get_link(idx)`, `Graph.get_turn(idx)`
- `Graph.remove_node(idx, cascade=False)`, `Graph.remove_link(idx, cascade=False)`
- `Graph.remove_redundants()`
- `Path(source, target, t_start, links=None, costs=None, mode=None, ...)`
- `PathList()`
- `KPathList()`
- `TurnType.parse(value)` and `TurnType.classify_turn(...)`
- `TimeDependentLinkBasedShortestPath.from_graph(graph, ...)`
- `TimeDependentLinkBasedShortestPath.shortest_paths(source, targets=None, t_start=0)`

## Development

GA Graph supports Python 3.10 and newer.

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src
python -m pytest --cov=graph --cov-report=term-missing
ruff format --check .
ruff check .
mypy
python -m pip check
python -m build
python -m twine check dist/*
```

## GitHub Repository Setup

This project is prepared for the future repository `andreagemma/graph`.

1. Create the empty repository on GitHub.
2. Initialize the local repository if needed and push the project to `main`.
3. Confirm the CI workflow passes on GitHub.
4. Configure the PyPI Trusted Publisher for project `ga-graph`, owner
   `andreagemma`, repository `graph`, workflow `release.yml`, and environment
   `pypi`.

## Releases

`src/graph/_version.py` is the only version source. To publish a release:

1. Update `__version__` in `_version.py` and commit the release changes.
2. Push `main` and wait for CI to pass.
3. Run the **Create release** GitHub Actions workflow. With no override it
   creates the `v<version>` tag, creates release notes, and dispatches the build
   and PyPI publication workflow.

PyPI versions are immutable. Increment `_version.py` before publishing different
content.

## License

GA Graph is distributed under the MIT License. See [LICENSE](LICENSE).
